from fastapi.testclient import TestClient

from test_calculations_api import _create_ready_project_with_scenario


def test_get_results_by_use_returns_latest_result_details(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert calculate_response.status_code == 200

    response = client.get(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/results/by-use",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["errors"] == []
    assert body["meta"] == {"version": None, "warnings": []}
    assert body["data"]["result_set"]["project_id"] == project_id
    assert body["data"]["result_set"]["scenario_id"] == scenario_id
    usage_types = [item["usage_type"] for item in body["data"]["items"]]
    assert usage_types == ["auxiliaries", "cooling", "dhw", "heating", "lighting", "ventilation"]
    heating = next(item for item in body["data"]["items"] if item["usage_type"] == "heating")
    assert heating["baseline_energy_kwh_year"] > 0
    assert heating["scenario_energy_kwh_year"] == heating["baseline_energy_kwh_year"]


def test_get_results_by_zone_returns_latest_zone_breakdown(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert calculate_response.status_code == 200

    response = client.get(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/results/by-zone",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["result_set"]["engine_version"] == "simplified-annual-v1"
    assert len(body["items"]) == 1
    zone = body["items"][0]
    assert zone["zone_name"] == "Guest rooms east"
    assert zone["zone_type"] == "guest_rooms"
    assert zone["orientation"] == "east"
    assert zone["baseline_energy_kwh_year"] > 0
    assert zone["scenario_energy_kwh_year"] == zone["baseline_energy_kwh_year"]


def test_get_results_by_use_returns_404_when_no_run_exists(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)

    response = client.get(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/results/by-use",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
