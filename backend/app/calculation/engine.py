from app.calculation.types import CalculationInput, CalculationOutput


class CalculationEngine:
    def run(self, input_data: CalculationInput) -> CalculationOutput:
        return CalculationOutput(
            summary={
                "baseline_energy_kwh_year": 1200000,
                "scenario_energy_kwh_year": 980000,
                "energy_savings_percent": 18.3,
                "baseline_bacs_class": "C",
                "scenario_bacs_class": "B",
            },
            by_use=[],
            by_zone=[],
            economic={
                "total_capex": 92000,
                "annual_cost_savings": 28000,
                "simple_payback_years": 3.1,
                "npv": 105000,
                "irr": 0.21,
            },
            bacs={"estimated_bacs_class": "C", "scenario_bacs_class": "B"},
            messages=["Starter output from placeholder engine."],
            warnings=[],
        )
