from fastapi.testclient import TestClient


def test_openapi_exposes_only_official_api_routes(client: TestClient) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = set(response.json()["paths"])
    assert not any("__placeholder__" in path for path in paths)

    expected_paths = {
        "/health",
        "/api/v1/auth/login",
        "/api/v1/projects",
        "/api/v1/project-templates",
        "/api/v1/country-profiles",
        "/api/v1/climate-zones",
        "/api/v1/usage-profiles",
    }
    assert expected_paths <= paths
