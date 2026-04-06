from app.calculation.engine import CalculationEngine
from app.calculation.types import CalculationInput


def _build_input(*, zones: list[dict] | None = None) -> CalculationInput:
    return CalculationInput(
        project_id="project-1",
        scenario_id="scenario-1",
        building={"name": "Hotel Demo"},
        zones=zones or [],
        systems=[],
        bacs_functions=[],
        selected_solutions=[],
        assumptions={},
    )


def test_run_returns_placeholder_summary_without_zone_breakdown() -> None:
    output = CalculationEngine().run(_build_input())

    assert output.summary["baseline_energy_kwh_year"] == 1200000
    assert output.summary["scenario_energy_kwh_year"] == 980000
    assert output.by_zone == []
    assert output.messages == ["Starter output from placeholder engine."]


def test_run_distributes_zone_results_proportionally_to_area() -> None:
    output = CalculationEngine().run(
        _build_input(
            zones=[
                {"id": "zone-1", "name": "Rooms East", "area_m2": 1500},
                {"id": "zone-2", "name": "Rooms West", "area_m2": 500},
            ]
        )
    )

    assert len(output.by_zone) == 2

    first_zone = output.by_zone[0]
    second_zone = output.by_zone[1]

    assert first_zone["zone_id"] == "zone-1"
    assert first_zone["baseline_energy_kwh_year"] == 900000.0
    assert first_zone["scenario_energy_kwh_year"] == 735000.0
    assert first_zone["energy_savings_percent"] == 18.3

    assert second_zone["zone_id"] == "zone-2"
    assert second_zone["baseline_energy_kwh_year"] == 300000.0
    assert second_zone["scenario_energy_kwh_year"] == 245000.0
    assert second_zone["energy_savings_percent"] == 18.3
