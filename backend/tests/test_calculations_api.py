from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.models.calculation_run import CalculationRun
from app.db.models.economic_result import EconomicResult
from app.db.models.project import Project
from app.db.models.result_summary import ResultSummary
from app.db.models.scenario import Scenario
from app.db.models.wizard_step_payload import WizardStepPayload
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


def _create_ready_project_with_scenario(client: TestClient) -> tuple[str, str, str]:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Calculation Project",
            country_profile_id=uuid4(),
            climate_zone_id=uuid4(),
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.flush()

        scenario = Scenario(
            project_id=project.id,
            name="Reference Scenario",
            description="Placeholder scenario for first calculation",
            is_reference=True,
        )
        db.add(scenario)
        db.add(
            WizardStepPayload(
                project_id=project.id,
                step_code="usage",
                payload_json={"average_occupancy_rate": 0.72, "ecs_intensity_level": "medium"},
            )
        )
        db.commit()
        db.refresh(project)
        db.refresh(scenario)
        project_id = str(project.id)
        scenario_id = str(scenario.id)

    assert client.put(
        f"/api/v1/projects/{project_id}/building",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Hotel Compute",
            "gross_floor_area_m2": 5000,
            "heated_area_m2": 4200,
            "number_of_floors": 5,
            "number_of_rooms": 100,
        },
    ).status_code == 200

    assert client.post(
        f"/api/v1/projects/{project_id}/zones",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Guest rooms east",
            "zone_type": "guest_rooms",
            "orientation": "east",
            "area_m2": 1800,
            "room_count": 80,
            "order_index": 1,
        },
    ).status_code == 200

    assert client.post(
        f"/api/v1/projects/{project_id}/systems",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Main heating plant",
            "system_type": "heating",
            "energy_source": "natural_gas",
            "quantity": 2,
        },
    ).status_code == 200

    assert client.post(
        f"/api/v1/projects/{project_id}/systems",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "DHW generation",
            "system_type": "dhw",
            "energy_source": "natural_gas",
            "quantity": 1,
        },
    ).status_code == 200

    return token, project_id, scenario_id


def test_calculate_scenario_persists_run_and_result(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)

    response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["project_id"] == project_id
    assert body["scenario_id"] == scenario_id
    assert body["engine_version"] == "placeholder-v1"
    assert body["summary"]["baseline_energy_kwh_year"] == 1200000
    assert body["economic"]["total_capex"] == 92000
    assert body["messages"] == ["Starter output from placeholder engine."]
    assert body["input_snapshot"]["project_id"] == project_id

    with SessionLocal() as db:
        runs = db.query(CalculationRun).filter(CalculationRun.scenario_id == scenario_id).all()
        assert len(runs) == 1


def test_get_latest_result_returns_latest_persisted_payload(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)

    calculate_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert calculate_response.status_code == 200

    latest_response = client.get(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/results/latest",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert latest_response.status_code == 200
    body = latest_response.json()["data"]
    assert body["summary"]["scenario_energy_kwh_year"] == 980000
    assert body["economic"]["annual_cost_savings"] == 28000
    assert body["messages"] == ["Starter output from placeholder engine."]


def test_get_latest_result_returns_404_when_no_run_exists(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)

    response = client.get(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/results/latest",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_get_latest_result_selects_most_recent_run(client: TestClient) -> None:
    token, project_id, scenario_id = _create_ready_project_with_scenario(client)

    first_response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert first_response.status_code == 200
    first_run_id = first_response.json()["data"]["calculation_run_id"]

    with SessionLocal() as db:
        latest_run = CalculationRun(
            project_id=project_id,
            scenario_id=scenario_id,
            status="completed",
            engine_version="placeholder-v2",
            input_snapshot={"project_id": project_id, "scenario_id": scenario_id},
            messages_json=["Most recent persisted output."],
            warnings_json=[],
        )
        db.add(latest_run)
        db.flush()
        db.add(
            ResultSummary(
                calculation_run_id=latest_run.id,
                baseline_energy_kwh_year=1300000,
                scenario_energy_kwh_year=900000,
                energy_savings_percent=30.8,
                baseline_bacs_class="C",
                scenario_bacs_class="A",
            )
        )
        db.add(
            EconomicResult(
                calculation_run_id=latest_run.id,
                total_capex=110000,
                annual_cost_savings=36000,
                simple_payback_years=3.0,
                npv=120000,
                irr=0.24,
            )
        )
        db.commit()

    latest_response = client.get(
        f"/api/v1/projects/{project_id}/scenarios/{scenario_id}/results/latest",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert latest_response.status_code == 200
    body = latest_response.json()["data"]
    assert body["calculation_run_id"] != first_run_id
    assert body["engine_version"] == "placeholder-v2"
    assert body["summary"]["scenario_energy_kwh_year"] == 900000
    assert body["economic"]["annual_cost_savings"] == 36000
    assert body["messages"] == ["Most recent persisted output."]


def test_calculate_returns_404_when_scenario_missing(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Missing Scenario Project",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/00000000-0000-0000-0000-000000000001/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
