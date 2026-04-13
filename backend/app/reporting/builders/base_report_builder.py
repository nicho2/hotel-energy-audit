from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


class BaseReportBuilder:
    def __init__(self, templates_dir: Path):
        self.environment = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def build_base_context(
        self,
        *,
        project,
        scenario,
        calculation_run,
        building,
        zones,
        branding: dict | None = None,
        report_type: str,
        title_prefix: str,
        cover_tagline: str,
    ) -> dict[str, Any]:
        summary = calculation_run.result_summary
        economic = calculation_run.economic_result
        if summary is None or economic is None:
            raise ValueError("Calculation run is missing summary or economic results")

        merged_branding = self._merge_branding(branding, cover_tagline)
        by_use_payload = [
            {
                "usage_type": item.usage_type,
                "baseline_energy_kwh_year": item.baseline_energy_kwh_year,
                "scenario_energy_kwh_year": item.scenario_energy_kwh_year,
                "energy_savings_percent": item.energy_savings_percent,
            }
            for item in getattr(calculation_run, "results_by_use", [])
        ]
        input_snapshot = calculation_run.input_snapshot if isinstance(calculation_run.input_snapshot, dict) else {}
        assumptions = input_snapshot.get("assumptions", {}) if isinstance(input_snapshot, dict) else {}
        systems = input_snapshot.get("systems", []) if isinstance(input_snapshot, dict) else []
        co2 = self._estimate_co2(by_use_payload, systems, assumptions)
        gross_area = getattr(building, "gross_floor_area_m2", None) or 0
        energy_savings_kwh = summary.baseline_energy_kwh_year - summary.scenario_energy_kwh_year
        dominant_usage = max(
            by_use_payload,
            key=lambda item: item["baseline_energy_kwh_year"],
            default=None,
        )
        zones_payload = [
            {
                "id": str(zone.id),
                "name": zone.name,
                "zone_type": zone.zone_type,
                "orientation": zone.orientation,
                "area_m2": zone.area_m2,
                "room_count": zone.room_count,
            }
            for zone in zones
        ]

        return {
            "report": {
                "title": f"{title_prefix} - {project.name}",
                "report_type": report_type,
                "language": "en",
                "generated_at": datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC"),
            },
            "branding": merged_branding,
            "project": {
                "id": str(project.id),
                "name": project.name,
                "client_name": project.client_name,
                "reference_code": project.reference_code,
                "description": project.description,
                "building_type": project.building_type,
                "project_goal": project.project_goal,
            },
            "scenario": {
                "id": str(scenario.id),
                "name": scenario.name,
                "description": scenario.description,
                "scenario_type": getattr(scenario, "scenario_type", None),
                "status": getattr(scenario, "status", None),
                "is_reference": scenario.is_reference,
            },
            "building": {
                "name": getattr(building, "name", None),
                "construction_period": getattr(building, "construction_period", None),
                "gross_floor_area_m2": getattr(building, "gross_floor_area_m2", None),
                "heated_area_m2": getattr(building, "heated_area_m2", None),
                "cooled_area_m2": getattr(building, "cooled_area_m2", None),
                "number_of_floors": getattr(building, "number_of_floors", None),
                "number_of_rooms": getattr(building, "number_of_rooms", None),
                "main_orientation": getattr(building, "main_orientation", None),
                "compactness_level": getattr(building, "compactness_level", None),
                "has_restaurant": getattr(building, "has_restaurant", False),
                "has_meeting_rooms": getattr(building, "has_meeting_rooms", False),
                "has_spa": getattr(building, "has_spa", False),
                "has_pool": getattr(building, "has_pool", False),
            },
            "results": {
                "summary": {
                    "baseline_energy_kwh_year": summary.baseline_energy_kwh_year,
                    "scenario_energy_kwh_year": summary.scenario_energy_kwh_year,
                    "energy_savings_kwh_year": round(energy_savings_kwh, 2),
                    "energy_savings_percent": summary.energy_savings_percent,
                    "baseline_energy_intensity_kwh_m2": round(summary.baseline_energy_kwh_year / gross_area, 1) if gross_area else None,
                    "scenario_energy_intensity_kwh_m2": round(summary.scenario_energy_kwh_year / gross_area, 1) if gross_area else None,
                    "baseline_co2_kg_year": co2["baseline_co2_kg_year"],
                    "scenario_co2_kg_year": co2["scenario_co2_kg_year"],
                    "co2_savings_kg_year": co2["co2_savings_kg_year"],
                    "co2_savings_percent": co2["co2_savings_percent"],
                    "baseline_bacs_class": summary.baseline_bacs_class,
                    "scenario_bacs_class": summary.scenario_bacs_class,
                },
                "economic": {
                    "total_capex": economic.total_capex,
                    "subsidies": economic.subsidies,
                    "net_capex": economic.net_capex,
                    "baseline_opex_year": economic.baseline_opex_year,
                    "scenario_opex_year": economic.scenario_opex_year,
                    "energy_cost_savings": economic.energy_cost_savings,
                    "maintenance_cost_year": economic.maintenance_cost_year,
                    "maintenance_savings_year": economic.maintenance_savings_year,
                    "net_annual_savings": economic.net_annual_savings,
                    "annual_cost_savings": economic.annual_cost_savings,
                    "simple_payback_years": economic.simple_payback_years,
                    "npv": economic.npv,
                    "irr": economic.irr,
                    "analysis_period_years": economic.analysis_period_years,
                    "discount_rate": economic.discount_rate,
                    "energy_inflation_rate": economic.energy_inflation_rate,
                    "cash_flows": economic.cash_flows or [],
                    "is_roi_calculable": economic.is_roi_calculable,
                },
                "by_use": by_use_payload,
                "dominant_usage": dominant_usage,
                "by_zone": [
                    {
                        "zone_id": str(item.zone_id) if item.zone_id else None,
                        "zone_name": item.zone_name,
                        "zone_type": item.zone_type,
                        "orientation": item.orientation,
                        "baseline_energy_kwh_year": item.baseline_energy_kwh_year,
                        "scenario_energy_kwh_year": item.scenario_energy_kwh_year,
                        "energy_savings_percent": item.energy_savings_percent,
                    }
                    for item in getattr(calculation_run, "results_by_zone", [])
                ],
                "messages": calculation_run.messages_json,
                "warnings": calculation_run.warnings_json,
            },
            "calculation": {
                "id": str(calculation_run.id),
                "engine_version": calculation_run.engine_version,
                "created_at": calculation_run.created_at.isoformat(),
                "input_snapshot": calculation_run.input_snapshot,
                "notes": calculation_run.notes,
            },
            "methodology": {
                "disclaimer": (
                    "This report is a simplified annual estimate for pre-audit, commercial discussion "
                    "and scenario comparison. It is not a dynamic thermal simulation, statutory audit "
                    "or regulatory compliance certificate."
                ),
                "traceability": (
                    "Results are tied to the calculation run, engine version, input snapshot and active "
                    "assumption set captured at calculation time."
                ),
                "economic_assumptions": assumptions.get("economic_inputs", {}),
            },
            "zones": zones_payload,
        }

    @staticmethod
    def _merge_branding(branding: dict | None, cover_tagline: str) -> dict:
        default_branding = {
            "id": None,
            "source": "fallback",
            "company_name": "Hotel Energy Audit",
            "accent_color": "#0f766e",
            "logo_text": "HEA",
            "contact_email": "contact@hotel-energy-audit.example.com",
            "cover_tagline": cover_tagline,
            "footer_note": "Prepared for pre-audit and scenario comparison.",
        }
        merged_branding = {**default_branding, **(branding or {})}
        if not merged_branding.get("contact_email"):
            merged_branding["contact_email"] = "contact@hotel-energy-audit.example.com"
        if not merged_branding.get("cover_tagline"):
            merged_branding["cover_tagline"] = cover_tagline
        return merged_branding

    @staticmethod
    def _estimate_co2(by_use: list[dict[str, Any]], systems: list[dict[str, Any]], assumptions: dict[str, Any]) -> dict[str, float]:
        factors = assumptions.get("co2_factors_json", {}) if isinstance(assumptions, dict) else {}
        if not isinstance(factors, dict):
            factors = {}
        baseline = 0.0
        scenario = 0.0
        for item in by_use:
            factor = BaseReportBuilder._co2_factor_for_usage(item["usage_type"], systems, factors)
            baseline += item["baseline_energy_kwh_year"] * factor
            scenario += item["scenario_energy_kwh_year"] * factor
        savings = baseline - scenario
        savings_percent = round(max(0.0, savings / baseline * 100), 1) if baseline > 0 else 0.0
        return {
            "baseline_co2_kg_year": round(baseline, 2),
            "scenario_co2_kg_year": round(scenario, 2),
            "co2_savings_kg_year": round(max(0.0, savings), 2),
            "co2_savings_percent": savings_percent,
        }

    @staticmethod
    def _co2_factor_for_usage(usage: str, systems: list[dict[str, Any]], factors: dict[str, Any]) -> float:
        system_type = "dhw" if usage == "dhw" else usage
        for system in systems:
            if str(system.get("system_type")) == system_type and system.get("energy_source"):
                source = str(system["energy_source"])
                return float(factors.get(source, factors.get("gas" if source == "natural_gas" else source, 0.2)))
        return float(factors.get("electricity" if usage in {"cooling", "ventilation", "lighting", "auxiliaries"} else "gas", 0.2))
