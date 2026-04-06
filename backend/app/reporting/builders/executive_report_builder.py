from datetime import UTC, datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


class ExecutiveReportBuilder:
    def __init__(self, templates_dir: Path):
        self.environment = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def build_context(self, project, scenario, calculation_run, building, zones, branding: dict | None = None) -> dict:
        summary = calculation_run.result_summary
        economic = calculation_run.economic_result
        if summary is None or economic is None:
            raise ValueError("Calculation run is missing summary or economic results")

        default_branding = {
            "id": None,
            "source": "fallback",
            "company_name": "Hotel Energy Audit",
            "accent_color": "#0f766e",
            "logo_text": "HEA",
            "contact_email": "contact@hotel-energy-audit.example.com",
            "cover_tagline": "Executive energy performance summary",
            "footer_note": "Prepared for pre-audit and scenario comparison.",
        }
        merged_branding = {**default_branding, **(branding or {})}
        if not merged_branding.get("contact_email"):
            merged_branding["contact_email"] = "contact@hotel-energy-audit.example.com"
        if not merged_branding.get("cover_tagline"):
            merged_branding["cover_tagline"] = "Executive energy performance summary"
        recommendations = self._build_recommendations(summary, economic)
        zones_payload = [
            {
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
                "title": f"Executive report - {project.name}",
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
                "is_reference": scenario.is_reference,
            },
            "building": {
                "name": getattr(building, "name", None),
                "gross_floor_area_m2": getattr(building, "gross_floor_area_m2", None),
                "heated_area_m2": getattr(building, "heated_area_m2", None),
                "cooled_area_m2": getattr(building, "cooled_area_m2", None),
                "number_of_floors": getattr(building, "number_of_floors", None),
                "number_of_rooms": getattr(building, "number_of_rooms", None),
                "main_orientation": getattr(building, "main_orientation", None),
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
                "messages": calculation_run.messages_json,
                "warnings": calculation_run.warnings_json,
            },
            "zones": zones_payload,
            "recommendations": recommendations,
        }

    def render_html(self, context: dict) -> str:
        template = self.environment.get_template("executive/report.html")
        return template.render(**context)

    @staticmethod
    def _build_recommendations(summary, economic) -> list[str]:
        recommendations: list[str] = []
        if summary.energy_savings_percent >= 20:
            recommendations.append(
                "Prioritize this scenario for commercial follow-up because projected savings exceed 20%."
            )
        if economic.simple_payback_years <= 4:
            recommendations.append(
                "Payback is within a commercially attractive range and supports rapid decision-making."
            )
        if summary.scenario_bacs_class and summary.scenario_bacs_class <= "B":
            recommendations.append(
                f"BACS performance improves to class {summary.scenario_bacs_class}, strengthening operational control."
            )
        if not recommendations:
            recommendations.append(
                "Use this scenario as a discussion baseline and refine assumptions before investment commitment."
            )
        return recommendations
