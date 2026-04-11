from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.models.project import Project
from app.db.models.scenario import Scenario
from app.db.session import SessionLocal
from test_admin_api import _login


def _get_org_catalog_id(client: TestClient, token: str) -> str:
    response = client.get(
        "/api/v1/admin/solution-catalogs",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    catalogs = response.json()["data"]
    org_catalogs = [item for item in catalogs if item["scope"] == "organization_specific"]
    assert org_catalogs
    return org_catalogs[0]["id"]


def _create_project_and_scenario(user: dict) -> tuple[str, str]:
    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Solution Catalog Project",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.flush()
        scenario = Scenario(project_id=project.id, name="Solution Scenario")
        db.add(scenario)
        db.commit()
        return str(project.id), str(scenario.id)


def test_solution_catalog_filters_by_country_family_and_building_type(client: TestClient) -> None:
    token, _user = _login(client)

    response = client.get(
        "/api/v1/projects/solutions/catalog?country=FR&family=bacs&building_type=hotel",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    codes = {item["code"] for item in response.json()["data"]}
    assert "ROOM_AUTOMATION_BASIC" in codes
    assert "FR_BACS_SUPERVISION_PLUS" in codes
    assert "DEMO_ROOM_AUTOMATION_OFFER" in codes
    assert "LED_RETROFIT_COMMON" not in codes


def test_admin_can_create_organization_specific_commercial_offer(client: TestClient) -> None:
    token, _user = _login(client)
    catalog_id = _get_org_catalog_id(client, token)
    code = f"ORG_OFFER_{uuid4().hex[:8].upper()}"

    response = client.post(
        "/api/v1/admin/solutions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "catalog_id": catalog_id,
            "code": code,
            "name": "Organization HVAC offer",
            "description": "Packaged organization-specific HVAC offer.",
            "family": "hvac",
            "target_scopes": ["project"],
            "applicable_countries": ["FR"],
            "applicable_building_types": ["hotel"],
            "applicable_zone_types": [],
            "bacs_impact_json": {"domains": ["heating"], "target_class_gain": 0},
            "lifetime_years": 15,
            "default_quantity": 1,
            "default_unit": "project",
            "default_unit_cost": 45000,
            "default_capex": 45000,
            "priority": 7,
            "is_commercial_offer": True,
            "offer_reference": "ORG-HVAC-001",
            "is_active": True,
        },
    )

    assert response.status_code == 201
    body = response.json()["data"]
    assert body["code"] == code
    assert body["scope"] == "organization_specific"
    assert body["is_commercial_offer"] is True
    assert body["offer_reference"] == "ORG-HVAC-001"


def test_deactivated_solution_is_not_proposed_but_existing_assignment_is_readable(
    client: TestClient,
) -> None:
    token, user = _login(client)
    project_id, scenario_id = _create_project_and_scenario(user)

    admin_list_response = client.get(
        "/api/v1/admin/solutions?family=bacs&include_inactive=true",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert admin_list_response.status_code == 200
    solution = next(
        item for item in admin_list_response.json()["data"] if item["code"] == "ROOM_AUTOMATION_BASIC"
    )

    assignment_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "solution_code": solution["code"],
            "target_scope": "project",
            "quantity": 1,
        },
    )
    assert assignment_response.status_code == 200

    deactivate_response = client.post(
        f"/api/v1/admin/solutions/{solution['id']}/deactivate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["data"]["is_active"] is False

    catalog_response = client.get(
        "/api/v1/projects/solutions/catalog",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert "ROOM_AUTOMATION_BASIC" not in {item["code"] for item in catalog_response.json()["data"]}

    assignments_response = client.get(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert assignments_response.status_code == 200
    assert assignments_response.json()["data"][0]["solution_name"] == "Room automation basic"
