from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.models.branding_profile import BrandingProfile
from app.db.models.project import Project
from app.db.session import SessionLocal
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
    assert body["file_size_bytes"] > 1500
    assert body["branding_profile_id"] is None
    assert body["generator_version"] == "html_text_pdf_v1"


def test_generate_detailed_report_persists_distinct_metadata_and_file(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]

    response = client.post(
        f"/api/v1/projects/{project_id}/reports",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "scenario_id": scenario_id,
            "calculation_run_id": calculation_run_id,
            "report_type": "detailed",
            "language": "fr",
            "include_assumptions": True,
            "include_regulatory_section": True,
            "include_annexes": True,
        },
    )

    assert response.status_code == 201
    body = response.json()["data"]
    assert body["project_id"] == project_id
    assert body["scenario_id"] == scenario_id
    assert body["calculation_run_id"] == calculation_run_id
    assert body["report_type"] == "detailed"
    assert body["status"] == "generated"
    assert body["mime_type"] == "application/pdf"
    assert body["file_name"] == f"detailed-report-{calculation_run_id}.pdf"
    assert body["file_size_bytes"] > 1500
    assert body["generator_version"] == "html_text_pdf_v1"


def test_list_project_reports_returns_generated_reports(client: TestClient) -> None:
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
    generated_report_id = generate_response.json()["data"]["id"]

    response = client.get(
        f"/api/v1/projects/{project_id}/reports",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    reports = response.json()["data"]
    assert len(reports) == 1
    assert reports[0]["id"] == generated_report_id
    assert reports[0]["project_id"] == project_id
    assert reports[0]["scenario_id"] == scenario_id
    assert reports[0]["calculation_run_id"] == calculation_run_id


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
    assert b"Executive Summary" in response.content
    assert b"Project Context" in response.content
    assert b"Results Overview" in response.content
    assert b"Methodology And Limits" in response.content


def test_generated_detailed_pdf_honors_optional_sections(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]

    generate_response = client.post(
        f"/api/v1/projects/{project_id}/reports",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "scenario_id": scenario_id,
            "calculation_run_id": calculation_run_id,
            "report_type": "detailed",
            "language": "fr",
            "include_assumptions": False,
            "include_regulatory_section": True,
            "include_annexes": False,
        },
    )

    assert generate_response.status_code == 201
    report = generate_response.json()["data"]
    response = client.get(
        f"/api/v1/reports/{report['id']}/download",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF-1.4")
    assert b"Project Context" in response.content
    assert b"Initial Estimated State" in response.content
    assert b"Regulatory Context" in response.content
    assert b"Recommendation And Action Plan" in response.content
    assert b"Assumptions And Limits" not in response.content
    assert b"Technical Annexes" not in response.content


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
    assert 'lang="en"' in body["html"]
    assert "Executive Summary" in body["html"]
    assert "Project Context" in body["html"]
    assert "Building Snapshot" in body["html"]
    assert "BACS Snapshot" in body["html"]
    assert "Results Overview" in body["html"]
    assert "Recommendations" in body["html"]
    assert "Methodology And Limits" in body["html"]
    assert "Scenario Energy" in body["html"]
    assert "CO2 Reduction" in body["html"]
    assert "NPV" in body["html"]
    assert "simplified annual estimate" in body["html"]
    assert body["context"]["project"]["name"] == "Calculation Project"
    assert body["context"]["scenario"]["id"] == scenario_id
    assert body["context"]["branding"]["source"] == "fallback"
    assert body["context"]["methodology"]["disclaimer"]
    assert body["context"]["results"]["summary"]["baseline_co2_kg_year"] >= 0
    assert body["context"]["results"]["summary"]["scenario_energy_kwh_year"] == calculate_response.json()["data"]["summary"]["scenario_energy_kwh_year"]


def test_get_detailed_report_html_returns_extended_sections(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]

    executive_response = client.get(
        f"/api/v1/reports/executive/{calculation_run_id}/html",
        headers={"Authorization": f"Bearer {token}"},
    )
    detailed_response = client.get(
        f"/api/v1/reports/detailed/{calculation_run_id}/html",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert detailed_response.status_code == 200
    body = detailed_response.json()["data"]
    assert body["report_type"] == "detailed"
    assert body["title"] == "Detailed report - Calculation Project"
    assert "Executive Summary" in body["html"]
    assert "Project Context" in body["html"]
    assert "Building Description" in body["html"]
    assert "Initial Estimated State" in body["html"]
    assert "Zone Detail" in body["html"]
    assert "System Detail" in body["html"]
    assert "BACS Analysis By Domain" in body["html"]
    assert "Scenario Comparison" in body["html"]
    assert "Economic Analysis" in body["html"]
    assert "Economic Assumptions" in body["html"]
    assert "Recommendation And Action Plan" in body["html"]
    assert "Assumptions And Limits" in body["html"]
    assert "Technical Annexes" in body["html"]
    assert "This report is not a dynamic simulation" in body["html"]
    assert "Main heating plant" in body["html"]
    assert len(body["html"]) > len(executive_response.json()["data"]["html"])
    assert body["context"]["report"]["report_type"] == "detailed"
    assert body["context"]["methodology"]["traceability"]
    assert {system["name"] for system in body["context"]["systems"]} >= {"Main heating plant", "DHW generation"}


def test_detailed_report_html_honors_optional_section_flags(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]

    response = client.get(
        (
            f"/api/v1/reports/detailed/{calculation_run_id}/html"
            "?include_assumptions=false&include_regulatory_section=true&include_annexes=false&language=fr"
        ),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert 'lang="fr"' in body["html"]
    assert "Assumptions And Limits" not in body["html"]
    assert "Technical Annexes" not in body["html"]
    assert "Regulatory Context" in body["html"]
    assert body["context"]["report"]["include_assumptions"] is False
    assert body["context"]["report"]["include_regulatory_section"] is True
    assert body["context"]["report"]["include_annexes"] is False


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


def test_report_uses_project_branding_when_available(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)

    with SessionLocal() as db:
        project = db.scalar(select(Project).where(Project.id == project_id))
        assert project is not None
        branding_profile = BrandingProfile(
            organization_id=project.organization_id,
            name="Project brand",
            company_name="Legrand Hospitality",
            accent_color="#ff5a1f",
            logo_text="LG",
            contact_email="contact@legrand-hospitality.example.com",
            cover_tagline="Branded executive summary",
            footer_note="Confidential commercial proposal.",
            is_default=False,
        )
        db.add(branding_profile)
        db.flush()
        project.branding_profile_id = branding_profile.id
        db.add(project)
        db.commit()
        db.refresh(branding_profile)
        branding_profile_id = str(branding_profile.id)

    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]

    html_response = client.get(
        f"/api/v1/reports/executive/{calculation_run_id}/html",
        headers={"Authorization": f"Bearer {token}"},
    )
    generate_response = client.post(
        f"/api/v1/reports/executive/{calculation_run_id}/generate",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert html_response.status_code == 200
    html_body = html_response.json()["data"]
    assert html_body["context"]["branding"]["id"] == branding_profile_id
    assert html_body["context"]["branding"]["source"] == "project"
    assert html_body["context"]["branding"]["company_name"] == "Legrand Hospitality"
    assert html_body["context"]["branding"]["accent_color"] == "#ff5a1f"
    assert "Legrand Hospitality" in html_body["html"]
    assert "Branded executive summary" in html_body["html"]
    assert "LG" in html_body["html"]

    assert generate_response.status_code == 200
    generated_report = generate_response.json()["data"]
    assert generated_report["branding_profile_id"] == branding_profile_id


def test_report_uses_organization_default_branding_as_fallback(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)

    with SessionLocal() as db:
        project = db.scalar(select(Project).where(Project.id == project_id))
        assert project is not None
        branding_profile = BrandingProfile(
            organization_id=project.organization_id,
            name="Org default brand",
            company_name="Demo Organization Energy Services",
            accent_color="#0057b8",
            logo_text="DO",
            contact_email="demo-brand@example.com",
            cover_tagline="Organization branded summary",
            is_default=True,
        )
        db.add(branding_profile)
        db.commit()
        db.refresh(branding_profile)
        branding_profile_id = str(branding_profile.id)

    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]

    response = client.get(
        f"/api/v1/reports/executive/{calculation_run_id}/html",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["context"]["branding"]["id"] == branding_profile_id
    assert body["context"]["branding"]["source"] == "organization_default"
    assert body["context"]["branding"]["company_name"] == "Demo Organization Energy Services"
