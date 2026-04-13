from app.calculation.engine import CalculationEngine, _economic_results
from app.calculation.types import CalculationInput


def _build_input(
    *,
    building: dict | None = None,
    zones: list[dict] | None = None,
    systems: list[dict] | None = None,
    selected_solutions: list[dict] | None = None,
    assumptions: dict | None = None,
) -> CalculationInput:
    return CalculationInput(
        project_id="project-1",
        scenario_id="scenario-1",
        building=building
        or {
            "name": "Hotel Demo",
            "gross_floor_area_m2": 5000,
            "heated_area_m2": 4200,
            "cooled_area_m2": 3500,
            "number_of_rooms": 100,
            "construction_period": "1975_1990",
            "compactness_level": "medium",
            "has_restaurant": True,
        },
        zones=zones or [],
        systems=systems or [],
        bacs_functions=[],
        selected_solutions=selected_solutions or [],
        assumptions=assumptions
        or {
            "climate_zone": {
                "heating_severity_index": 1.0,
                "cooling_severity_index": 1.0,
                "solar_exposure_index": 1.0,
            },
            "usage_payload": {"average_occupancy_rate": 0.72},
        },
    )


def test_run_builds_annual_baseline_without_placeholder_constants() -> None:
    output = CalculationEngine().run(_build_input())

    assert output.summary["baseline_energy_kwh_year"] > 700000
    assert output.summary["scenario_energy_kwh_year"] == output.summary["baseline_energy_kwh_year"]
    assert {item["usage_type"] for item in output.by_use} == {
        "heating",
        "cooling",
        "ventilation",
        "dhw",
        "lighting",
        "auxiliaries",
    }
    assert output.by_zone[0]["zone_type"] == "other"
    assert output.warnings


def test_run_varies_by_zone_orientation_and_scenario_solution() -> None:
    output = CalculationEngine().run(
        _build_input(
            zones=[
                {"id": "zone-1", "name": "Rooms South", "zone_type": "guest_rooms", "orientation": "south", "area_m2": 1500, "room_count": 60},
                {"id": "zone-2", "name": "Technical North", "zone_type": "technical", "orientation": "north", "area_m2": 500},
            ],
            selected_solutions=[
                {
                    "solution_code": "ROOM_AUTOMATION_BASIC",
                    "family": "bacs",
                    "target_scope": "project",
                    "is_selected": True,
                    "default_capex": 18000,
                }
            ],
        )
    )

    assert len(output.by_zone) == 2

    first_zone = output.by_zone[0]
    second_zone = output.by_zone[1]

    assert first_zone["zone_id"] == "zone-1"
    assert first_zone["baseline_energy_kwh_year"] > second_zone["baseline_energy_kwh_year"]
    assert first_zone["scenario_energy_kwh_year"] < first_zone["baseline_energy_kwh_year"]
    assert output.summary["energy_savings_percent"] > 0
    assert second_zone["zone_id"] == "zone-2"


def test_run_varies_significantly_by_climate_and_system_performance() -> None:
    mild_efficient = CalculationEngine().run(
        _build_input(
            systems=[{"system_type": "heating", "efficiency_level": "high"}],
            assumptions={"climate_zone": {"heating_severity_index": 0.75, "cooling_severity_index": 0.8}},
        )
    )
    cold_poor = CalculationEngine().run(
        _build_input(
            systems=[{"system_type": "heating", "efficiency_level": "very_low"}],
            assumptions={"climate_zone": {"heating_severity_index": 1.30, "cooling_severity_index": 0.8}},
        )
    )

    mild_heating = next(item for item in mild_efficient.by_use if item["usage_type"] == "heating")
    cold_heating = next(item for item in cold_poor.by_use if item["usage_type"] == "heating")
    assert cold_heating["baseline_energy_kwh_year"] > mild_heating["baseline_energy_kwh_year"] * 2


def test_run_combines_solution_impacts_sequentially_and_traces_order() -> None:
    output = CalculationEngine().run(
        _build_input(
            zones=[{"id": "zone-1", "name": "Lobby", "zone_type": "lobby", "orientation": "mixed", "area_m2": 1000}],
            selected_solutions=[
                {
                    "solution_code": "LED_RETROFIT_COMMON",
                    "family": "lighting",
                    "target_scope": "project",
                    "gain_override_percent": 0.20,
                    "is_selected": True,
                },
                {
                    "solution_code": "LIGHTING_PRESENCE_CONTROL",
                    "family": "lighting",
                    "target_scope": "project",
                    "gain_override_percent": 0.20,
                    "is_selected": True,
                },
            ],
        )
    )

    lighting = next(item for item in output.by_use if item["usage_type"] == "lighting")
    assert lighting["energy_savings_percent"] == 36.0
    assert "Impacts appliques dans l'ordre" in output.messages[-1] or any(
        "Impacts appliques dans l'ordre" in message for message in output.messages
    )


def test_economic_results_compute_opex_npv_irr_payback_and_cash_flows() -> None:
    assumptions = {
        "economic_defaults_json": {
            "energy_prices": {"electricity": 0.20},
            "discount_rate": 0.0,
            "energy_inflation_rate": 0.0,
            "analysis_period_years": 2,
            "maintenance_rate": 0.0,
            "subsidies": 1000,
            "performance_degradation_rate": 0.0,
        }
    }
    baseline = {usage: 0.0 for usage in ["heating", "cooling", "ventilation", "dhw", "lighting", "auxiliaries"]}
    scenario = dict(baseline)
    baseline["heating"] = 10000
    scenario["heating"] = 5000

    economic = _economic_results(
        baseline,
        scenario,
        [{"system_type": "heating", "energy_source": "electricity"}],
        assumptions,
        3000,
        [],
    )

    assert economic["baseline_opex_year"] == 2000
    assert economic["scenario_opex_year"] == 1000
    assert economic["energy_cost_savings"] == 1000
    assert economic["subsidies"] == 1000
    assert economic["net_capex"] == 2000
    assert economic["simple_payback_years"] == 2.0
    assert economic["npv"] == 0
    assert economic["irr"] == 0.0
    assert [flow["net_cash_flow"] for flow in economic["cash_flows"]] == [-2000, 1000, 1000]


def test_economic_results_marks_roi_not_calculable_without_positive_savings() -> None:
    assumptions = {
        "economic_defaults_json": {
            "energy_prices": {"electricity": 0.20},
            "discount_rate": 0.06,
            "energy_inflation_rate": 0.0,
            "analysis_period_years": 3,
            "maintenance_rate": 0.02,
        }
    }
    baseline = {usage: 0.0 for usage in ["heating", "cooling", "ventilation", "dhw", "lighting", "auxiliaries"]}
    scenario = dict(baseline)
    baseline["lighting"] = 5000
    scenario["lighting"] = 5000

    economic = _economic_results(
        baseline,
        scenario,
        [{"system_type": "lighting", "energy_source": "electricity"}],
        assumptions,
        10000,
        [],
    )

    assert economic["annual_cost_savings"] < 0
    assert economic["simple_payback_years"] is None
    assert economic["irr"] is None
    assert economic["is_roi_calculable"] is False
