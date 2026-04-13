from pathlib import Path

from app.reporting.builders.base_report_builder import BaseReportBuilder


class ExecutiveReportBuilder(BaseReportBuilder):
    def __init__(self, templates_dir: Path):
        super().__init__(templates_dir)

    def build_context(self, project, scenario, calculation_run, building, zones, branding: dict | None = None) -> dict:
        context = self.build_base_context(
            project=project,
            scenario=scenario,
            calculation_run=calculation_run,
            building=building,
            zones=zones,
            branding=branding,
            report_type="executive",
            title_prefix="Executive report",
            cover_tagline="Executive energy performance summary",
        )
        summary = calculation_run.result_summary
        economic = calculation_run.economic_result
        recommendations = self._build_recommendations(summary, economic)
        return {**context, "recommendations": recommendations}

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
        if economic.simple_payback_years is not None and economic.simple_payback_years <= 4:
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
