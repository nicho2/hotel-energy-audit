from fastapi.testclient import TestClient

from scripts.demo_seed_data import DEMO_PROJECT_REFERENCE_CODES
from scripts.seed_all import seed_demo_showcase_data, seed_dev_auth_data
from test_admin_api import _login


def test_demo_recette_smoke_covers_critical_paths(client: TestClient) -> None:
    seed_dev_auth_data()
    seed_demo_showcase_data()
    token, _user = _login(client)

    projects_response = client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert projects_response.status_code == 200
    projects = {
        project["reference_code"]: project
        for project in projects_response.json()["data"]
        if project["reference_code"] in DEMO_PROJECT_REFERENCE_CODES
    }
    assert set(projects) == set(DEMO_PROJECT_REFERENCE_CODES)

    project = projects["DEMO-HOTEL-001"]
    scenarios_response = client.get(
        f"/api/v1/projects/{project['id']}/scenarios",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert scenarios_response.status_code == 200
    scenarios = scenarios_response.json()["data"]
    assert len(scenarios) == 2
    scenario_ids = [scenario["id"] for scenario in scenarios]

    comparison_response = client.post(
        f"/api/v1/projects/{project['id']}/scenarios/compare",
        headers={"Authorization": f"Bearer {token}"},
        json={"scenario_ids": scenario_ids},
    )
    assert comparison_response.status_code == 200
    comparison = comparison_response.json()["data"]
    assert len(comparison["items"]) == 2
    assert comparison["recommended_scenario"]["scenario_name"] == "Smart rooms + HVAC optimization"

    target_scenario_id = comparison["recommended_scenario"]["scenario_id"]
    latest_response = client.get(
        f"/api/v1/projects/{project['id']}/scenarios/{target_scenario_id}/results/latest",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert latest_response.status_code == 200
    calculation_run_id = latest_response.json()["data"]["calculation_run_id"]

    executive_response = client.post(
        f"/api/v1/reports/executive/{calculation_run_id}/generate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert executive_response.status_code == 200
    assert executive_response.json()["data"]["report_type"] == "executive"

    detailed_response = client.post(
        f"/api/v1/reports/detailed/{calculation_run_id}/generate?language=fr",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert detailed_response.status_code == 200
    assert detailed_response.json()["data"]["report_type"] == "detailed"
