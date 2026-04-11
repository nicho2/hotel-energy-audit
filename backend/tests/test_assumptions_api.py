from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.models.building import Building
from app.db.models.calculation_run import CalculationRun
from app.db.models.economic_result import EconomicResult
from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.models.result_summary import ResultSummary
from app.db.models.scenario import Scenario
from app.db.models.user import User
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


def test_project_assumptions_exposes_grouped_defaults_and_latest_engine(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Assumptions Project",
            client_name="Hotel Group",
            building_type="hotel",
            project_goal="compare",
        )
        db.add(project)
        db.flush()

        db.add(
            Building(
                project_id=project.id,
                name="Main building",
                gross_floor_area_m2=5000,
                heated_area_m2=4200,
                number_of_rooms=110,
                main_orientation="south",
            )
        )

        scenario = Scenario(project_id=project.id, name="Reference")
        db.add(scenario)
        db.flush()

        run = CalculationRun(
            project_id=project.id,
            scenario_id=scenario.id,
            status="completed",
            engine_version="placeholder-v2",
            input_snapshot={"assumptions": {"engine_version": "placeholder-v2"}},
            messages_json=[],
            warnings_json=["Review default climate profile."],
        )
        db.add(run)
        db.flush()
        db.add(
            ResultSummary(
                calculation_run_id=run.id,
                baseline_energy_kwh_year=1200000,
                scenario_energy_kwh_year=980000,
                energy_savings_percent=18.3,
                baseline_bacs_class="C",
                scenario_bacs_class="B",
            )
        )
        db.add(
            EconomicResult(
                calculation_run_id=run.id,
                total_capex=92000,
                annual_cost_savings=28000,
                simple_payback_years=3.1,
                npv=105000,
                irr=0.21,
            )
        )
        db.commit()
        project_id = str(project.id)
        run_id = str(run.id)

    response = client.get(
        f"/api/v1/projects/{project_id}/assumptions",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["calculation_run_id"] == run_id
    assert body["scenario_name"] == "Reference"
    assert body["engine_version"] == "placeholder-v2"
    assert body["warnings"] == ["Review default climate profile."]
    section_keys = [section["key"] for section in body["sections"]]
    assert section_keys == ["context", "climate", "building", "economic", "bacs", "engine"]
    building_items = {item["label"]: item for item in body["sections"][2]["items"]}
    assert building_items["Gross floor area"]["value"] == "5000 m2"
    assert building_items["Gross floor area"]["source"] == "configured"


def test_project_assumptions_returns_safe_defaults_without_calculation(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="No Calculation Project",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.commit()
        project_id = str(project.id)

    response = client.get(
        f"/api/v1/projects/{project_id}/assumptions",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["calculation_run_id"] is None
    assert body["engine_version"] == "placeholder-v1"
    assert body["warnings"] == ["No calculation run is available yet."]


def test_project_assumptions_rejects_other_organization_project(client: TestClient) -> None:
    token, _user = _login(client)

    with SessionLocal() as db:
        other_organization = Organization(
            name="Other Organization",
            slug=f"assumptions-other-{uuid4().hex[:8]}",
            default_language="fr",
            is_active=True,
        )
        db.add(other_organization)
        db.flush()

        other_user = User(
            organization_id=other_organization.id,
            email=f"assumptions-{uuid4().hex[:8]}@example.com",
            password_hash="not-used",
            first_name="Other",
            last_name="User",
            role="org_admin",
            preferred_language="fr",
            is_active=True,
        )
        db.add(other_user)
        db.flush()

        project = Project(
            organization_id=other_organization.id,
            created_by_user_id=other_user.id,
            name="Hidden Assumptions",
            building_type="hotel",
            project_goal="hidden",
        )
        db.add(project)
        db.commit()
        project_id = str(project.id)

    response = client.get(
        f"/api/v1/projects/{project_id}/assumptions",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
