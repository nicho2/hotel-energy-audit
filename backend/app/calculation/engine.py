from app.calculation.types import CalculationInput, CalculationOutput


class CalculationEngine:
    def run(self, input_data: CalculationInput) -> CalculationOutput:
        by_use = [
            {
                "usage_type": "heating",
                "baseline_energy_kwh_year": 420000,
                "scenario_energy_kwh_year": 344000,
                "energy_savings_percent": 18.1,
            },
            {
                "usage_type": "cooling",
                "baseline_energy_kwh_year": 180000,
                "scenario_energy_kwh_year": 154000,
                "energy_savings_percent": 14.4,
            },
            {
                "usage_type": "ventilation",
                "baseline_energy_kwh_year": 125000,
                "scenario_energy_kwh_year": 108000,
                "energy_savings_percent": 13.6,
            },
            {
                "usage_type": "dhw",
                "baseline_energy_kwh_year": 310000,
                "scenario_energy_kwh_year": 258000,
                "energy_savings_percent": 16.8,
            },
            {
                "usage_type": "lighting",
                "baseline_energy_kwh_year": 165000,
                "scenario_energy_kwh_year": 116000,
                "energy_savings_percent": 29.7,
            },
        ]
        zones = input_data.zones or []
        by_zone = []
        if zones:
            total_area = sum(float(zone.get("area_m2", 0) or 0) for zone in zones) or float(len(zones))
            baseline_total = 1200000.0
            scenario_total = 980000.0
            for zone in zones:
                zone_area = float(zone.get("area_m2", 0) or 0)
                share = zone_area / total_area if total_area else 1 / len(zones)
                baseline_zone = round(baseline_total * share, 2)
                scenario_zone = round(scenario_total * share, 2)
                by_zone.append(
                    {
                        "zone_id": zone.get("id"),
                        "zone_name": zone.get("name", "Unnamed zone"),
                        "zone_type": zone.get("zone_type", "other"),
                        "orientation": zone.get("orientation", "mixed"),
                        "baseline_energy_kwh_year": baseline_zone,
                        "scenario_energy_kwh_year": scenario_zone,
                        "energy_savings_percent": round(
                            ((baseline_zone - scenario_zone) / baseline_zone) * 100,
                            1,
                        )
                        if baseline_zone
                        else 0.0,
                    }
                )

        return CalculationOutput(
            summary={
                "baseline_energy_kwh_year": 1200000,
                "scenario_energy_kwh_year": 980000,
                "energy_savings_percent": 18.3,
                "baseline_bacs_class": "C",
                "scenario_bacs_class": "B",
            },
            by_use=by_use,
            by_zone=by_zone,
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
