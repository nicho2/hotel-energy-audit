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


def test_reference_data_endpoints_expose_seeded_country_climate_and_usage_profiles(
    client: TestClient,
) -> None:
    token = _login(client)

    countries_response = client.get(
        "/api/v1/country-profiles",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert countries_response.status_code == 200
    countries = countries_response.json()["data"]
    france = next(country for country in countries if country["country_code"] == "FR")

    climates_response = client.get(
        "/api/v1/climate-zones",
        headers={"Authorization": f"Bearer {token}"},
        params={"country_profile_id": france["id"]},
    )
    assert climates_response.status_code == 200
    climates = climates_response.json()["data"]
    assert {climate["code"] for climate in climates} >= {"FR-TEMP", "FR-MED"}
    assert any(climate["is_default"] for climate in climates)

    usage_response = client.get(
        "/api/v1/usage-profiles",
        headers={"Authorization": f"Bearer {token}"},
        params={"country_profile_id": france["id"], "building_type": "hotel"},
    )
    assert usage_response.status_code == 200
    usage_profiles = usage_response.json()["data"]
    assert {profile["zone_type"] for profile in usage_profiles} >= {
        "guest_rooms",
        "lobby",
        "restaurant",
    }


def test_reference_data_get_unknown_resource_returns_404(client: TestClient) -> None:
    token = _login(client)

    response = client.get(
        f"/api/v1/country-profiles/{uuid4()}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    body = response.json()
    assert body["data"] is None
    assert body["errors"][0]["code"] == "NOT_FOUND"


def test_admin_reference_routes_require_admin_role_and_return_api_response(
    client: TestClient,
) -> None:
    token = _login(client)

    response = client.get(
        "/api/v1/admin/country-profiles",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["errors"] == []
    assert any(country["country_code"] == "FR" for country in body["data"])
