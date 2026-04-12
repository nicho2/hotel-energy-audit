from datetime import datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.models.audit_log import AuditLog
from app.db.models.organization import Organization
from app.db.models.user import User
from app.db.session import SessionLocal
from test_assumption_sets_api import _create_assumption_set
from test_calculations_api import _create_ready_project_with_scenario
from test_solution_catalog_api import _get_org_catalog_id
from test_admin_api import _login


def test_project_and_scenario_history_use_audit_logs(client: TestClient) -> None:
    token, _user = _login(client)

    project_response = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Audited Project",
            "building_type": "hotel",
            "project_goal": "traceability",
            "country_profile_id": str(uuid4()),
            "climate_zone_id": str(uuid4()),
        },
    )
    assert project_response.status_code == 200
    project_id = project_response.json()["data"]["id"]

    archive_response = client.patch(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"status": "archived"},
    )
    assert archive_response.status_code == 200

    scenario_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Audited Scenario", "scenario_type": "custom"},
    )
    assert scenario_response.status_code == 200
    scenario_id = scenario_response.json()["data"]["id"]

    update_scenario_response = client.patch(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Audited Scenario Updated"},
    )
    assert update_scenario_response.status_code == 200

    project_history_response = client.get(
        f"/api/v1/projects/{project_id}/history",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert project_history_response.status_code == 200
    project_actions = [item["action"] for item in project_history_response.json()["data"]]
    assert project_actions[:4] == [
        "scenario_updated",
        "scenario_created",
        "project_archived",
        "project_created",
    ]

    scenario_history_response = client.get(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/history",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert scenario_history_response.status_code == 200
    scenario_actions = [item["action"] for item in scenario_history_response.json()["data"]]
    assert scenario_actions == ["scenario_updated", "scenario_created"]

    delete_scenario_response = client.delete(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_scenario_response.status_code == 200

    updated_history_response = client.get(
        f"/api/v1/projects/{project_id}/history",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert updated_history_response.status_code == 200
    assert updated_history_response.json()["data"][0]["action"] == "scenario_deleted"


def test_admin_audit_filters_cover_calculation_report_date_and_scope(
    client: TestClient,
) -> None:
    token, user = _login(client)
    _, project_id, scenario_id = _create_ready_project_with_scenario(client)

    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert calculate_response.status_code == 200
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]

    report_response = client.post(
        f"/api/v1/reports/executive/{calculation_run_id}/generate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert report_response.status_code == 200

    with SessionLocal() as db:
        other_organization = Organization(
            name="Other Audit Organization",
            slug=f"audit-other-{uuid4().hex[:8]}",
            default_language="fr",
            is_active=True,
        )
        db.add(other_organization)
        db.flush()
        other_user = User(
            organization_id=other_organization.id,
            email=f"audit-{uuid4().hex[:8]}@example.com",
            password_hash="not-used",
            first_name="Other",
            last_name="Audit",
            role="org_admin",
            preferred_language="fr",
            is_active=True,
        )
        db.add(other_user)
        db.flush()
        db.add(
            AuditLog(
                entity_type="calculation_run",
                entity_id=uuid4(),
                action="scenario_calculated",
                before_json=None,
                after_json={"project_id": "hidden"},
                user_id=other_user.id,
                organization_id=other_organization.id,
            )
        )
        db.commit()

    calculation_logs_response = client.get(
        "/api/v1/admin/audit-logs?action=scenario_calculated&date_from=2000-01-01T00:00:00Z",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert calculation_logs_response.status_code == 200
    calculation_logs = calculation_logs_response.json()["data"]
    assert len(calculation_logs) == 1
    assert calculation_logs[0]["organization_id"] == user["organization_id"]
    assert calculation_logs[0]["after_json"]["project_id"] == project_id
    assert calculation_logs[0]["after_json"]["scenario_id"] == scenario_id

    report_logs_response = client.get(
        "/api/v1/admin/audit-logs?entity_type=generated_report&action=report_generated",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert report_logs_response.status_code == 200
    report_logs = report_logs_response.json()["data"]
    assert len(report_logs) == 1
    assert report_logs[0]["after_json"]["calculation_run_id"] == calculation_run_id


def test_admin_sensitive_configuration_changes_are_audited(client: TestClient) -> None:
    token, _user = _login(client)
    assumption_set = _create_assumption_set(client, token, "audit-1.0.0")

    update_assumption_response = client.patch(
        f"/api/v1/admin/assumption-sets/{assumption_set['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={"notes": "Audited update"},
    )
    assert update_assumption_response.status_code == 200

    assumption_logs_response = client.get(
        (
            "/api/v1/admin/audit-logs"
            f"?entity_type=calculation_assumption_set&entity_id={assumption_set['id']}"
        ),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert assumption_logs_response.status_code == 200
    assumption_logs = assumption_logs_response.json()["data"]
    assert [item["action"] for item in assumption_logs] == ["assumption_set_updated"]
    assert assumption_logs[0]["after_json"]["changed_fields"] == ["notes"]

    catalog_id = _get_org_catalog_id(client, token)
    solution_code = f"AUDIT_OFFER_{uuid4().hex[:8].upper()}"
    create_solution_response = client.post(
        "/api/v1/admin/solutions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "catalog_id": catalog_id,
            "code": solution_code,
            "name": "Audited solution",
            "description": "Audited organization offer.",
            "family": "bacs",
            "target_scopes": ["project"],
            "applicable_countries": ["FR"],
            "applicable_building_types": ["hotel"],
            "applicable_zone_types": [],
            "bacs_impact_json": {"domains": ["monitoring"], "target_class_gain": 1},
            "lifetime_years": 10,
            "default_quantity": 1,
            "default_unit": "project",
            "default_unit_cost": 10000,
            "default_capex": 10000,
            "priority": 25,
            "is_commercial_offer": True,
            "offer_reference": "AUDIT-OFFER-001",
            "is_active": True,
        },
    )
    assert create_solution_response.status_code == 201
    solution_id = create_solution_response.json()["data"]["id"]

    update_solution_response = client.patch(
        f"/api/v1/admin/solutions/{solution_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"priority": 3},
    )
    assert update_solution_response.status_code == 200

    solution_logs_response = client.get(
        f"/api/v1/admin/audit-logs?entity_type=solution_definition&entity_id={solution_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert solution_logs_response.status_code == 200
    solution_actions = [item["action"] for item in solution_logs_response.json()["data"]]
    assert solution_actions == ["solution_updated", "solution_created"]

    timestamps = [item["timestamp"] for item in solution_logs_response.json()["data"]]
    assert all(datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None for value in timestamps)
