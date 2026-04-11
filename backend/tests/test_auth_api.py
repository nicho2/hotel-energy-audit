from fastapi.testclient import TestClient

from scripts.seed_all import DEV_USER_EMAIL, DEV_USER_PASSWORD


def _login(client: TestClient) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": DEV_USER_EMAIL, "password": DEV_USER_PASSWORD},
    )
    assert response.status_code == 200
    body = response.json()
    return body["data"]["access_token"]


def test_login_returns_bearer_token(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": DEV_USER_EMAIL, "password": DEV_USER_PASSWORD},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["token_type"] == "bearer"
    assert body["data"]["access_token"]
    assert body["data"]["user"]["email"] == DEV_USER_EMAIL
    assert body["errors"] == []


def test_oauth_token_endpoint_supports_swagger_authorize(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/token",
        data={"username": DEV_USER_EMAIL, "password": DEV_USER_PASSWORD},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]

    projects_response = client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {body['access_token']}"},
    )
    assert projects_response.status_code == 200


def test_protected_projects_route_rejects_request_without_token(client: TestClient) -> None:
    response = client.get("/api/v1/projects")

    assert response.status_code == 401


def test_me_returns_current_user(client: TestClient) -> None:
    token = _login(client)

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["email"] == DEV_USER_EMAIL
    assert body["data"]["role"] == "org_admin"
