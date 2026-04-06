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


def test_get_building_returns_null_when_missing(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Project Without Building",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    response = client.get(
        f"/api/v1/projects/{project_id}/building",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"] is None
    assert body["errors"] == []


def test_put_building_creates_and_replaces_building(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Project With Building",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    create_response = client.put(
        f"/api/v1/projects/{project_id}/building",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Hotel Central",
            "construction_period": "1990_2005",
            "gross_floor_area_m2": 5000,
            "heated_area_m2": 4500,
            "cooled_area_m2": 3200,
            "number_of_floors": 6,
            "number_of_rooms": 120,
            "main_orientation": "south",
            "compactness_level": "medium",
            "has_restaurant": True,
            "has_meeting_rooms": True,
            "has_spa": False,
            "has_pool": False,
        },
    )

    assert create_response.status_code == 200
    created_body = create_response.json()
    building_id = created_body["data"]["id"]
    assert created_body["data"]["name"] == "Hotel Central"

    replace_response = client.put(
        f"/api/v1/projects/{project_id}/building",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Hotel Central Renovated",
            "construction_period": "2005_2015",
            "gross_floor_area_m2": 5200,
            "heated_area_m2": 4600,
            "cooled_area_m2": 3300,
            "number_of_floors": 7,
            "number_of_rooms": 125,
            "main_orientation": "mixed",
            "compactness_level": "high",
            "has_restaurant": True,
            "has_meeting_rooms": False,
            "has_spa": True,
            "has_pool": True,
        },
    )

    assert replace_response.status_code == 200
    replaced_body = replace_response.json()
    assert replaced_body["data"]["id"] == building_id
    assert replaced_body["data"]["name"] == "Hotel Central Renovated"
    assert replaced_body["data"]["number_of_floors"] == 7
    assert replaced_body["data"]["has_pool"] is True


def test_put_building_rejects_obvious_surface_inconsistencies(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Invalid Building Project",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    response = client.put(
        f"/api/v1/projects/{project_id}/building",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "gross_floor_area_m2": 1000,
            "heated_area_m2": 1200,
            "cooled_area_m2": 800,
            "number_of_floors": 3,
            "number_of_rooms": 50,
        },
    )

    assert response.status_code == 422
    body = response.json()
    assert body["errors"][0]["code"] == "VALIDATION_ERROR"
    assert body["errors"][0]["field"] == "heated_area_m2"
