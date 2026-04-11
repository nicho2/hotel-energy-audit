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
                    "energy_savings_percent": summary.energy_savings_percent,
                    "baseline_bacs_class": summary.baseline_bacs_class,
                    "scenario_bacs_class": summary.scenario_bacs_class,
                },
                "economic": {
                    "total_capex": economic.total_capex,
                    "annual_cost_savings": economic.annual_cost_savings,
                    "simple_payback_years": economic.simple_payback_years,
                    "npv": economic.npv,
                    "irr": economic.irr,
                },
                "by_use": [
                    {
                        "usage_type": item.usage_type,
                        "baseline_energy_kwh_year": item.baseline_energy_kwh_year,
                        "scenario_energy_kwh_year": item.scenario_energy_kwh_year,
                        "energy_savings_percent": item.energy_savings_percent,
                    }
                    for item in getattr(calculation_run, "results_by_use", [])
                ],
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
