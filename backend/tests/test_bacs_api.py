from fastapi.testclient import TestClient

from app.db.models.project import Project
from app.db.session import SessionLocal
from scripts.seed_all import DEV_USER_EMAIL, DEV_USER_PASSWORD


def _login(client: TestClient) -> tuple[str, dict]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": DEV_USER_EMAIL, "password": DEV_USER_PASSWORD},
    )
    assert response.status_code == 200
    body = response.json()
    return body["data"]["access_token"], body["data"]["user"]


def _create_project(client: TestClient) -> tuple[str, str]:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="BACS Project",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    return token, project_id


def test_get_current_bacs_returns_seeded_catalog(client: TestClient) -> None:
    token, project_id = _create_project(client)

    response = client.get(
        f"/api/v1/projects/{project_id}/bacs/current",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["assessment_id"] is None
    assert body["data"]["version"] == "v1"
    assert len(body["data"]["functions"]) == 10
    assert all(item["is_selected"] is False for item in body["data"]["functions"])


def test_bacs_current_and_functions_persist_and_summary_is_computed(client: TestClient) -> None:
    token, project_id = _create_project(client)

    create_response = client.post(
        f"/api/v1/projects/{project_id}/bacs/current",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "assessor_name": "Nicolas",
            "manual_override_class": "C",
            "notes": "Initial BACS walk-through",
        },
    )
    assert create_response.status_code == 200
    current_body = create_response.json()
    assert current_body["data"]["assessor_name"] == "Nicolas"
    assert current_body["data"]["manual_override_class"] == "C"

    functions = current_body["data"]["functions"]
    selected_ids = [
        next(item["id"] for item in functions if item["code"] == "monitoring.central_supervision"),
        next(item["id"] for item in functions if item["code"] == "heating.schedule_control"),
        next(item["id"] for item in functions if item["code"] == "lighting.occupancy_control"),
    ]

    put_response = client.put(
        f"/api/v1/projects/{project_id}/bacs/current/functions",
        headers={"Authorization": f"Bearer {token}"},
        json={"selected_function_ids": selected_ids},
    )
    assert put_response.status_code == 200
    selected_codes = {
        item["code"] for item in put_response.json()["data"]["functions"] if item["is_selected"]
    }
    assert selected_codes == {
        "monitoring.central_supervision",
        "heating.schedule_control",
        "lighting.occupancy_control",
    }

    summary_response = client.get(
        f"/api/v1/projects/{project_id}/bacs/current/summary",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert summary_response.status_code == 200
    summary = summary_response.json()["data"]
    assert summary["overall_score"] == 35.6
    assert summary["estimated_bacs_class"] == "D"
    assert summary["manual_override_class"] == "C"
    assert summary["bacs_class"] == "C"
    assert summary["confidence_score"] == 0.3
    assert summary["selected_function_count"] == 3
    assert summary["total_function_count"] == 10

    domain_scores = {item["domain"]: item["score"] for item in summary["domain_scores"]}
    assert domain_scores == {
        "monitoring": 60.0,
        "heating": 55.6,
        "cooling_ventilation": 0.0,
        "dhw": 0.0,
        "lighting": 55.6,
    }

    top_missing_codes = [item["code"] for item in summary["top_missing_functions"]]
    assert top_missing_codes[:3] == [
        "cooling_ventilation.cooling_schedule",
        "cooling_ventilation.ventilation_demand_control",
        "monitoring.alarm_reporting",
    ]


def test_put_bacs_functions_rejects_unknown_function_ids(client: TestClient) -> None:
    token, project_id = _create_project(client)

    response = client.put(
        f"/api/v1/projects/{project_id}/bacs/current/functions",
        headers={"Authorization": f"Bearer {token}"},
        json={"selected_function_ids": ["00000000-0000-0000-0000-000000000001"]},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["errors"][0]["code"] == "VALIDATION_ERROR"
    assert body["errors"][0]["field"] == "selected_function_ids"
