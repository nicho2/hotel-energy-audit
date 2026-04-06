from fastapi.testclient import TestClient

from test_calculations_api import _create_ready_project_with_scenario


def test_generate_report_persists_metadata_and_stores_file(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert calculate_response.status_code == 200
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]

    response = client.post(
        f"/api/v1/reports/executive/{calculation_run_id}/generate",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["project_id"] == project_id
    assert body["scenario_id"] == scenario_id
    assert body["calculation_run_id"] == calculation_run_id
    assert body["report_type"] == "executive"
    assert body["status"] == "generated"
    assert body["mime_type"] == "application/pdf"
    assert body["file_name"].endswith(".pdf")
    assert body["file_size_bytes"] > 0
    assert body["generator_version"] == "placeholder_pdf_v1"


def test_get_generated_report_metadata_returns_persisted_report(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]
    generate_response = client.post(
        f"/api/v1/reports/executive/{calculation_run_id}/generate",
        headers={"Authorization": f"Bearer {token}"},
    )
    report_id = generate_response.json()["data"]["id"]

    response = client.get(
        f"/api/v1/reports/{report_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["id"] == report_id
    assert body["project_id"] == project_id
    assert body["scenario_id"] == scenario_id
    assert body["calculation_run_id"] == calculation_run_id


def test_download_generated_report_returns_pdf_file(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]
    generate_response = client.post(
        f"/api/v1/reports/executive/{calculation_run_id}/generate",
        headers={"Authorization": f"Bearer {token}"},
    )
    report = generate_response.json()["data"]

    response = client.get(
        f"/api/v1/reports/{report['id']}/download",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert report["file_name"] in response.headers["content-disposition"]
    assert response.content.startswith(b"%PDF-1.4")


def test_get_executive_report_html_returns_rendered_document(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert calculate_response.status_code == 200
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]

    response = client.get(
        f"/api/v1/reports/executive/{calculation_run_id}/html",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["calculation_run_id"] == calculation_run_id
    assert body["project_id"] == project_id
    assert body["scenario_id"] == scenario_id
    assert body["title"] == "Executive report - Calculation Project"
    assert "Executive Summary" in body["html"]
    assert "Building Snapshot" in body["html"]
    assert "Results Overview" in body["html"]
    assert "Recommendations" in body["html"]
    assert "Scenario Energy" in body["html"]
    assert body["context"]["project"]["name"] == "Calculation Project"
    assert body["context"]["scenario"]["id"] == scenario_id
    assert body["context"]["results"]["summary"]["scenario_energy_kwh_year"] == 980000


def test_get_executive_report_html_returns_404_for_missing_run(client: TestClient) -> None:
    token, _, _ = _create_ready_project_with_scenario(client)

    response = client.get(
        "/api/v1/reports/executive/00000000-0000-0000-0000-000000000123/html",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_get_generated_report_returns_404_for_missing_report(client: TestClient) -> None:
    token, _, _ = _create_ready_project_with_scenario(client)

    response = client.get(
        "/api/v1/reports/00000000-0000-0000-0000-000000000123",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
