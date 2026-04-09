from fastapi.testclient import TestClient

from app.db.models.project import Project
from app.db.models.scenario import Scenario
from app.db.session import SessionLocal
from test_calculations_api import _login


def _create_project_with_context(client: TestClient) -> tuple[str, str, str]:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Scenario Management Project",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.flush()

        reference_scenario = Scenario(
            project_id=project.id,
            name="Reference",
            description="Baseline scenario",
            is_reference=True,
        )
        db.add(reference_scenario)
        db.commit()
        db.refresh(project)
        db.refresh(reference_scenario)

        return token, str(project.id), str(reference_scenario.id)


def test_scenario_crud_duplicate_and_solution_assignment_flow(client: TestClient) -> None:
    token, project_id, reference_scenario_id = _create_project_with_context(client)

    list_response = client.get(
        f"/api/v1/projects/{project_id}/scenarios",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    assert len(list_response.json()["data"]) == 1

    create_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Scenario Rooms",
            "description": "Room optimization",
            "scenario_type": "custom",
            "is_reference": False,
        },
    )
    assert create_response.status_code == 200
    scenario_id = create_response.json()["data"]["id"]
    assert create_response.json()["data"]["status"] == "draft"

    update_response = client.patch(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Scenario Rooms Updated", "status": "ready", "is_reference": True},
    )
    assert update_response.status_code == 200
    assert update_response.json()["data"]["is_reference"] is True
    assert update_response.json()["data"]["status"] == "ready"

    second_list_response = client.get(
        f"/api/v1/projects/{project_id}/scenarios",
        headers={"Authorization": f"Bearer {token}"},
    )
    scenarios = second_list_response.json()["data"]
    assert any(item["id"] == scenario_id and item["is_reference"] is True for item in scenarios)
    assert any(item["id"] == reference_scenario_id and item["is_reference"] is False for item in scenarios)

    catalog_response = client.get(
        "/api/v1/projects/solutions/catalog",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert catalog_response.status_code == 200
    assert any(item["code"] == "ROOM_AUTOMATION_BASIC" for item in catalog_response.json()["data"])

    create_assignment_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "solution_code": "ROOM_AUTOMATION_BASIC",
            "target_scope": "project",
            "quantity": 1,
            "gain_override_percent": 0.12,
        },
    )
    assert create_assignment_response.status_code == 200
    assignment_id = create_assignment_response.json()["data"]["id"]
    assert create_assignment_response.json()["data"]["solution_name"] == "Room automation basic"

    update_assignment_response = client.patch(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions/{assignment_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"target_scope": "project", "capex_override": 1800, "notes": "Commercial option"},
    )
    assert update_assignment_response.status_code == 200
    assert update_assignment_response.json()["data"]["capex_override"] == 1800

    list_assignment_response = client.get(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_assignment_response.status_code == 200
    assert len(list_assignment_response.json()["data"]) == 1

    duplicate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/duplicate",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Scenario Rooms Copy"},
    )
    assert duplicate_response.status_code == 200
    duplicated_id = duplicate_response.json()["data"]["id"]
    assert duplicate_response.json()["data"]["derived_from_scenario_id"] == scenario_id

    duplicated_assignments_response = client.get(
        f"/api/v1/projects/{project_id}/scenarios/{duplicated_id}/solutions",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert duplicated_assignments_response.status_code == 200
    assert len(duplicated_assignments_response.json()["data"]) == 1


def test_scenario_solution_requires_scope_target_when_needed(client: TestClient) -> None:
    token, project_id, _ = _create_project_with_context(client)

    create_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Scenario Test", "scenario_type": "custom"},
    )
    scenario_id = create_response.json()["data"]["id"]

    response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/solutions",
        headers={"Authorization": f"Bearer {token}"},
        json={"solution_code": "BOILER_REPLACEMENT_CONDENSING", "target_scope": "system"},
    )

    assert response.status_code == 422
