from fastapi.testclient import TestClient


def test_health_endpoint_returns_standard_response(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "data": {"status": "ok"},
        "meta": {"version": None, "warnings": []},
        "errors": [],
    }
