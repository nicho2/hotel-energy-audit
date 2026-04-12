from uuid import uuid4

from fastapi.testclient import TestClient

from scripts.seed_all import DEV_USER_EMAIL, DEV_USER_PASSWORD


def _login(client: TestClient) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": DEV_USER_EMAIL, "password": DEV_USER_PASSWORD},
    )
    assert response.status_code == 200
    return response.json()["data"]["access_token"]


def _first_country_profile_id(client: TestClient, token: str) -> str:
    response = client.get(
        "/api/v1/country-profiles",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    return response.json()["data"][0]["id"]


def _first_climate_zone_id(client: TestClient, token: str, country_profile_id: str) -> str:
    response = client.get(
        f"/api/v1/climate-zones?country_profile_id={country_profile_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    return response.json()["data"][0]["id"]


def test_project_template_crud_roundtrip(client: TestClient) -> None:
    token = _login(client)
    country_profile_id = _first_country_profile_id(client, token)
    name = f"Template {uuid4().hex[:8]}"

    create_response = client.post(
        "/api/v1/project-templates",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": name,
            "description": "Template for API roundtrip",
            "building_type": "hotel",
            "country_profile_id": country_profile_id,
            "default_payload_json": {"wizard_mode": "express"},
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()["data"]
    assert created["name"] == name
    assert created["country_profile_id"] == country_profile_id

    get_response = client.get(
        f"/api/v1/project-templates/{created['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 200
    assert get_response.json()["data"]["default_payload_json"] == {"wizard_mode": "express"}

    update_response = client.patch(
        f"/api/v1/project-templates/{created['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "Updated", "is_active": True},
    )
    assert update_response.status_code == 200
    assert update_response.json()["data"]["description"] == "Updated"

    delete_response = client.delete(
        f"/api/v1/project-templates/{created['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["data"]["is_active"] is False


def test_project_template_rejects_unknown_country_profile(client: TestClient) -> None:
    token = _login(client)

    response = client.post(
        "/api/v1/project-templates",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"Invalid Template {uuid4().hex[:8]}",
            "building_type": "hotel",
            "country_profile_id": str(uuid4()),
            "default_payload_json": {},
        },
    )

    assert response.status_code == 404
    assert response.json()["errors"][0]["message"] == "Country profile not found"


def test_project_template_rejects_duplicate_name_in_organization(client: TestClient) -> None:
    token = _login(client)
    country_profile_id = _first_country_profile_id(client, token)
    name = f"Duplicate Template {uuid4().hex[:8]}"
    payload = {
        "name": name,
        "building_type": "hotel",
        "country_profile_id": country_profile_id,
        "default_payload_json": {},
    }

    first_response = client.post(
        "/api/v1/project-templates",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/project-templates",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )

    assert second_response.status_code == 422
    body = second_response.json()
    assert body["errors"][0]["field"] == "name"


def test_project_can_be_created_from_project_template(client: TestClient) -> None:
    token = _login(client)
    country_profile_id = _first_country_profile_id(client, token)
    climate_zone_id = _first_climate_zone_id(client, token, country_profile_id)

    template_response = client.post(
        "/api/v1/project-templates",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"Apply Template {uuid4().hex[:8]}",
            "building_type": "hotel",
            "country_profile_id": country_profile_id,
            "default_payload_json": {
                "mode": "express",
                "zoning_standard": "hotel_standard",
                "usage_standard": "standard",
                "favorite_solution_codes": ["ROOM_AUTOMATION_BASIC"],
            },
        },
    )
    assert template_response.status_code == 201
    template_id = template_response.json()["data"]["id"]

    project_response = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"Project from template {uuid4().hex[:8]}",
            "country_profile_id": country_profile_id,
            "climate_zone_id": climate_zone_id,
            "building_type": "hotel",
            "project_goal": "pre_audit",
            "template_id": template_id,
        },
    )

    assert project_response.status_code == 200
    body = project_response.json()["data"]
    assert body["template_id"] == template_id
    assert body["wizard_step"] == 1
