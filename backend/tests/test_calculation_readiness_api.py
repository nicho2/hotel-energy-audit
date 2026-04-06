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


def _create_project(client: TestClient, name: str) -> tuple[str, str]:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name=name,
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    return token, project_id


def test_calculation_readiness_blocks_when_building_and_zones_are_missing(client: TestClient) -> None:
    token, project_id = _create_project(client, "Readiness Empty Project")

    response = client.get(
        f"/api/v1/projects/{project_id}/calculation-readiness",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["is_ready"] is False
    assert body["confidence_level"] == "low"
    assert [issue["code"] for issue in body["blocking_issues"]] == [
        "building_missing",
        "zones_missing",
    ]
    assert [warning["code"] for warning in body["warnings"]] == [
        "heating_system_missing",
        "dhw_system_missing",
        "reference_scenario_implicit",
    ]


def test_calculation_readiness_is_ready_with_warnings_when_systems_are_missing(client: TestClient) -> None:
    token, project_id = _create_project(client, "Readiness Partial Project")

    building_response = client.put(
        f"/api/v1/projects/{project_id}/building",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Hotel Ready",
            "gross_floor_area_m2": 4000,
            "heated_area_m2": 3500,
            "number_of_floors": 4,
            "number_of_rooms": 80,
        },
    )
    assert building_response.status_code == 200

    zone_response = client.post(
        f"/api/v1/projects/{project_id}/zones",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Guest rooms south",
            "zone_type": "guest_rooms",
            "orientation": "south",
            "area_m2": 1500,
            "room_count": 60,
            "order_index": 1,
        },
    )
    assert zone_response.status_code == 200

    response = client.get(
        f"/api/v1/projects/{project_id}/calculation-readiness",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["is_ready"] is True
    assert body["blocking_issues"] == []
    assert body["confidence_level"] == "low"
    assert [warning["code"] for warning in body["warnings"]] == [
        "heating_system_missing",
        "dhw_system_missing",
        "reference_scenario_implicit",
    ]


def test_calculation_readiness_confidence_increases_with_major_systems(client: TestClient) -> None:
    token, project_id = _create_project(client, "Readiness Full Project")

    assert client.put(
        f"/api/v1/projects/{project_id}/building",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Hotel Full",
            "gross_floor_area_m2": 5000,
            "heated_area_m2": 4200,
            "number_of_floors": 5,
            "number_of_rooms": 100,
        },
    ).status_code == 200

    assert client.post(
        f"/api/v1/projects/{project_id}/zones",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Guest rooms north",
            "zone_type": "guest_rooms",
            "orientation": "north",
            "area_m2": 1800,
            "room_count": 80,
            "order_index": 1,
        },
    ).status_code == 200

    assert client.post(
        f"/api/v1/projects/{project_id}/systems",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Main heating plant",
            "system_type": "heating",
            "energy_source": "natural_gas",
            "quantity": 2,
        },
    ).status_code == 200

    assert client.post(
        f"/api/v1/projects/{project_id}/systems",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "DHW generation",
            "system_type": "dhw",
            "energy_source": "natural_gas",
            "quantity": 1,
        },
    ).status_code == 200

    response = client.get(
        f"/api/v1/projects/{project_id}/calculation-readiness",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["is_ready"] is True
    assert body["blocking_issues"] == []
    assert body["confidence_level"] == "high"
    assert [warning["code"] for warning in body["warnings"]] == ["reference_scenario_implicit"]
