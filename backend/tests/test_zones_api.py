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


def _create_project_with_building(client: TestClient) -> tuple[str, str]:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Zones Project",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    building_response = client.put(
        f"/api/v1/projects/{project_id}/building",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Hotel Zoning",
            "gross_floor_area_m2": 5000,
            "heated_area_m2": 4200,
            "number_of_floors": 5,
            "number_of_rooms": 100,
            "has_restaurant": True,
            "has_meeting_rooms": True,
            "has_spa": False,
            "has_pool": False,
        },
    )
    assert building_response.status_code == 200
    return token, project_id


def test_generate_zones_creates_initial_hotel_zoning(client: TestClient) -> None:
    token, project_id = _create_project_with_building(client)

    response = client.post(
        f"/api/v1/projects/{project_id}/zones/generate",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "room_distribution": [
                {"orientation": "north", "room_count": 20},
                {"orientation": "east", "room_count": 30},
                {"orientation": "south", "room_count": 30},
                {"orientation": "west", "room_count": 20},
            ],
            "average_room_area_m2": 24,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) >= 7
    assert any(zone["zone_type"] == "guest_rooms" and zone["orientation"] == "north" for zone in body["data"])
    assert any(zone["zone_type"] == "restaurant" for zone in body["data"])
    assert any(zone["zone_type"] == "meeting" for zone in body["data"])
    assert body["meta"]["warnings"] == []


def test_zone_crud_allows_create_update_delete(client: TestClient) -> None:
    token, project_id = _create_project_with_building(client)

    create_response = client.post(
        f"/api/v1/projects/{project_id}/zones",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Lobby",
            "zone_type": "lobby",
            "orientation": "mixed",
            "area_m2": 200,
            "room_count": 0,
            "order_index": 1,
        },
    )
    assert create_response.status_code == 200
    zone_id = create_response.json()["data"]["id"]

    update_response = client.patch(
        f"/api/v1/projects/{project_id}/zones/{zone_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"area_m2": 250, "name": "Main Lobby"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["data"]["name"] == "Main Lobby"

    list_response = client.get(
        f"/api/v1/projects/{project_id}/zones",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    assert len(list_response.json()["data"]) == 1

    delete_response = client.delete(
        f"/api/v1/projects/{project_id}/zones/{zone_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200

    final_list_response = client.get(
        f"/api/v1/projects/{project_id}/zones",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert final_list_response.status_code == 200
    assert final_list_response.json()["data"] == []


def test_zone_validation_returns_checks_and_warnings(client: TestClient) -> None:
    token, project_id = _create_project_with_building(client)

    generate_response = client.post(
        f"/api/v1/projects/{project_id}/zones/generate",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "room_distribution": [
                {"orientation": "north", "room_count": 10},
                {"orientation": "south", "room_count": 10},
            ],
            "average_room_area_m2": 24,
        },
    )
    assert generate_response.status_code == 200
    assert generate_response.json()["meta"]["warnings"]

    validation_response = client.get(
        f"/api/v1/projects/{project_id}/zones/validation",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert validation_response.status_code == 200
    body = validation_response.json()
    assert "is_valid" in body["data"]
    assert "checks" in body["data"]
    assert "warnings" in body["data"]
    assert any(item["status"] == "warning" for item in body["data"]["warnings"])


def test_create_zone_rejects_room_overflow_against_building(client: TestClient) -> None:
    token, project_id = _create_project_with_building(client)

    response = client.post(
        f"/api/v1/projects/{project_id}/zones",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Guest rooms north",
            "zone_type": "guest_rooms",
            "orientation": "north",
            "area_m2": 1500,
            "room_count": 120,
            "order_index": 1,
        },
    )

    assert response.status_code == 422
    body = response.json()
    assert body["errors"][0]["field"] == "room_count"
