from app.calculation.engine import CalculationEngine
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
