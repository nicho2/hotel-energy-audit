from fastapi.testclient import TestClient

from app.db.models.economic_result import EconomicResult
from app.db.models.project import Project
from app.db.models.result_summary import ResultSummary
from app.db.models.scenario import Scenario
from app.db.models.calculation_run import CalculationRun
from app.db.session import SessionLocal
from test_calculations_api import _login


def _create_project_with_scenarios(client: TestClient, scenario_count: int = 3) -> tuple[str, str, list[str]]:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Compare Project",
            building_type="hotel",
            project_goal="compare_scenarios",
        )
        db.add(project)
        db.flush()

        scenarios: list[Scenario] = []
        for index in range(scenario_count):
            scenario = Scenario(
                project_id=project.id,
                name=f"Scenario {index + 1}",
                description=f"Comparison scenario {index + 1}",
                is_reference=index == 0,
            )
            db.add(scenario)
            scenarios.append(scenario)

        db.commit()
        db.refresh(project)
        for scenario in scenarios:
            db.refresh(scenario)

        project_id = str(project.id)
        scenario_ids = [str(scenario.id) for scenario in scenarios]

    assert client.put(
        f"/api/v1/projects/{project_id}/building",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Hotel Compare",
            "gross_floor_area_m2": 5000,
            "heated_area_m2": 4200,
            "number_of_floors": 5,
            "number_of_rooms": 100,
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
            "name": "Lighting system",
            "system_type": "lighting",
            "energy_source": "electricity",
            "quantity": 1,
        },
    ).status_code == 200

    return token, project_id, scenario_ids


def _persist_run(
    *,
    project_id: str,
    scenario_id: str,
    engine_version: str,
    scenario_energy_kwh_year: float,
    energy_savings_percent: float,
    scenario_bacs_class: str,
    total_capex: float,
    annual_cost_savings: float,
    simple_payback_years: float | None,
    npv: float = 100000,
    irr: float | None = 0.2,
) -> None:
    with SessionLocal() as db:
        run = CalculationRun(
            project_id=project_id,
            scenario_id=scenario_id,
            status="completed",
            engine_version=engine_version,
            input_snapshot={"project_id": project_id, "scenario_id": scenario_id},
            messages_json=[f"Run for {scenario_id}"],
            warnings_json=[],
        )
        db.add(run)
        db.flush()
        db.add(
            ResultSummary(
                calculation_run_id=run.id,
                baseline_energy_kwh_year=1200000,
                scenario_energy_kwh_year=scenario_energy_kwh_year,
                energy_savings_percent=energy_savings_percent,
                baseline_bacs_class="C",
                scenario_bacs_class=scenario_bacs_class,
            )
        )
        db.add(
            EconomicResult(
                calculation_run_id=run.id,
                total_capex=total_capex,
                net_capex=total_capex,
                baseline_opex_year=100000,
                scenario_opex_year=100000 - annual_cost_savings,
                energy_cost_savings=annual_cost_savings,
                net_annual_savings=annual_cost_savings,
                annual_cost_savings=annual_cost_savings,
                simple_payback_years=simple_payback_years,
                npv=npv,
                irr=irr,
                cash_flows=[],
                is_roi_calculable=simple_payback_years is not None or irr is not None,
            )
        )
        db.commit()


def test_compare_scenarios_returns_tabular_comparison_and_recommendation(client: TestClient) -> None:
    token, project_id, scenario_ids = _create_project_with_scenarios(client, scenario_count=3)

    _persist_run(
        project_id=project_id,
        scenario_id=scenario_ids[0],
        engine_version="compare-v1",
        scenario_energy_kwh_year=1000000,
        energy_savings_percent=16.7,
        scenario_bacs_class="C",
        total_capex=60000,
        annual_cost_savings=18000,
        simple_payback_years=3.3,
    )
    _persist_run(
        project_id=project_id,
        scenario_id=scenario_ids[1],
        engine_version="compare-v1",
        scenario_energy_kwh_year=880000,
        energy_savings_percent=26.7,
        scenario_bacs_class="B",
        total_capex=85000,
        annual_cost_savings=32000,
        simple_payback_years=2.7,
    )
    _persist_run(
        project_id=project_id,
        scenario_id=scenario_ids[2],
        engine_version="compare-v1",
        scenario_energy_kwh_year=930000,
        energy_savings_percent=22.5,
        scenario_bacs_class="A",
        total_capex=140000,
        annual_cost_savings=30000,
        simple_payback_years=4.7,
    )

    response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/compare",
        headers={"Authorization": f"Bearer {token}"},
        json={"scenario_ids": scenario_ids},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["project_id"] == project_id
    assert body["compared_scenario_ids"] == scenario_ids
    assert len(body["items"]) == 3
    second = body["items"][1]
    assert second["scenario_id"] == scenario_ids[1]
    assert second["scenario_energy_kwh_year"] == 880000
    assert second["estimated_co2_kg_year"] > 0
    assert second["scenario_bacs_class"] == "B"
    assert second["total_capex"] == 85000
    assert second["net_capex"] == 85000
    assert second["baseline_opex_year"] == 100000
    assert second["scenario_opex_year"] == 68000
    assert second["npv"] == 100000
    assert second["irr"] == 0.2
    assert second["annual_cost_savings"] == 32000
    assert second["roi_percent"] > 0
    assert second["score"] > 0
    assert body["recommended_scenario"]["scenario_id"] == scenario_ids[1]
    assert len(body["recommended_scenario"]["reasons"]) == 3


def test_compare_scenarios_exposes_not_calculable_roi(client: TestClient) -> None:
    token, project_id, scenario_ids = _create_project_with_scenarios(client, scenario_count=2)
    _persist_run(
        project_id=project_id,
        scenario_id=scenario_ids[0],
        engine_version="compare-v1",
        scenario_energy_kwh_year=1200000,
        energy_savings_percent=0,
        scenario_bacs_class="C",
        total_capex=0,
        annual_cost_savings=0,
        simple_payback_years=None,
        npv=0,
        irr=None,
    )
    _persist_run(
        project_id=project_id,
        scenario_id=scenario_ids[1],
        engine_version="compare-v1",
        scenario_energy_kwh_year=1190000,
        energy_savings_percent=0.8,
        scenario_bacs_class="C",
        total_capex=50000,
        annual_cost_savings=-1000,
        simple_payback_years=None,
        npv=-65000,
        irr=None,
    )

    response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/compare",
        headers={"Authorization": f"Bearer {token}"},
        json={"scenario_ids": scenario_ids},
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["items"][1]["simple_payback_years"] is None
    assert body["items"][1]["irr"] is None
    assert body["items"][1]["npv"] == -65000


def test_compare_scenarios_rejects_missing_scenario(client: TestClient) -> None:
    token, project_id, scenario_ids = _create_project_with_scenarios(client, scenario_count=2)
    _persist_run(
        project_id=project_id,
        scenario_id=scenario_ids[0],
        engine_version="compare-v1",
        scenario_energy_kwh_year=950000,
        energy_savings_percent=20.8,
        scenario_bacs_class="B",
        total_capex=70000,
        annual_cost_savings=24000,
        simple_payback_years=2.9,
    )
    _persist_run(
        project_id=project_id,
        scenario_id=scenario_ids[1],
        engine_version="compare-v1",
        scenario_energy_kwh_year=910000,
        energy_savings_percent=24.2,
        scenario_bacs_class="A",
        total_capex=95000,
        annual_cost_savings=28000,
        simple_payback_years=3.4,
    )

    response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/compare",
        headers={"Authorization": f"Bearer {token}"},
        json={"scenario_ids": [scenario_ids[0], "00000000-0000-0000-0000-000000000999"]},
    )

    assert response.status_code == 404


def test_compare_scenarios_rejects_scenario_without_calculation(client: TestClient) -> None:
    token, project_id, scenario_ids = _create_project_with_scenarios(client, scenario_count=2)
    _persist_run(
        project_id=project_id,
        scenario_id=scenario_ids[0],
        engine_version="compare-v1",
        scenario_energy_kwh_year=980000,
        energy_savings_percent=18.3,
        scenario_bacs_class="B",
        total_capex=75000,
        annual_cost_savings=25000,
        simple_payback_years=3.0,
    )

    response = client.post(
        f"/api/v1/projects/{project_id}/scenarios/compare",
        headers={"Authorization": f"Bearer {token}"},
        json={"scenario_ids": scenario_ids},
    )

    assert response.status_code == 422
    assert response.json()["errors"][0]["code"] == "VALIDATION_ERROR"
