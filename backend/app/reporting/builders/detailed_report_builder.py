from pathlib import Path
from typing import Any

from app.reporting.builders.base_report_builder import BaseReportBuilder
from app.reporting.builders.executive_report_builder import ExecutiveReportBuilder


class DetailedReportBuilder(BaseReportBuilder):
    def __init__(self, templates_dir: Path):
        super().__init__(templates_dir)

    def build_context(
        self,
        *,
        project,
        scenario,
        calculation_run,
        building,
        zones,
        systems,
        bacs_assessment,
        comparison_runs,
        scenario_solutions,
        branding: dict | None = None,
        include_assumptions: bool = True,
        include_regulatory_section: bool = False,
        include_annexes: bool = True,
    ) -> dict[str, Any]:
        context = self.build_base_context(
            project=project,
            scenario=scenario,
            calculation_run=calculation_run,
            building=building,
            zones=zones,
            branding=branding,
            report_type="detailed",
            title_prefix="Detailed report",
            cover_tagline="Detailed energy performance report",
        )
        context["report"]["include_assumptions"] = include_assumptions
        context["report"]["include_regulatory_section"] = include_regulatory_section
        context["report"]["include_annexes"] = include_annexes
        context["systems"] = self._build_systems_payload(systems)
        context["bacs"] = self._build_bacs_payload(bacs_assessment)
        context["scenario"]["solutions"] = self._build_solutions_payload(scenario_solutions)
        context["comparison"] = self._build_comparison_payload(comparison_runs)
        context["assumptions"] = self._build_assumptions_payload(calculation_run.input_snapshot)
        context["recommendations"] = ExecutiveReportBuilder._build_recommendations(
            calculation_run.result_summary,
            calculation_run.economic_result,
        )
        context["limits"] = [
            "Simplified annual estimation for pre-audit and decision support.",
            "Results depend on declared building, zoning, system, BACS and scenario assumptions.",
            "This report is not a dynamic simulation or a regulatory compliance certificate.",
        ]
        return context

    def render_html(self, context: dict) -> str:
        template = self.environment.get_template("detailed/report.html")
        return template.render(**context)

    @staticmethod
    def _build_systems_payload(systems) -> list[dict[str, Any]]:
        return [
            {
                "name": system.name,
                "system_type": system.system_type,
                "energy_source": system.energy_source,
                "technology_type": system.technology_type,
                "efficiency_level": system.efficiency_level,
                "serves": system.serves,
                "quantity": system.quantity,
                "year_installed": system.year_installed,
                "is_primary": system.is_primary,
                "notes": system.notes,
            }
            for system in systems
        ]

    @staticmethod
    def _build_bacs_payload(bacs_assessment) -> dict[str, Any]:
        if bacs_assessment is None:
            return {
                "assessment": None,
                "domains": [],
                "selected_count": 0,
                "total_weight": 0,
            }

        domains: dict[str, dict[str, Any]] = {}
        for selected in bacs_assessment.selected_functions:
            function = selected.function_definition
            domain = domains.setdefault(
                function.domain,
                {
                    "domain": function.domain,
                    "selected_count": 0,
                    "total_weight": 0,
                    "functions": [],
                },
            )
            domain["selected_count"] += 1
            domain["total_weight"] += function.weight
            domain["functions"].append(
                {
                    "code": function.code,
                    "name": function.name,
                    "description": function.description,
                    "weight": function.weight,
                }
            )

        return {
            "assessment": {
                "version": bacs_assessment.version,
                "assessor_name": bacs_assessment.assessor_name,
                "manual_override_class": bacs_assessment.manual_override_class,
                "notes": bacs_assessment.notes,
            },
            "domains": list(domains.values()),
            "selected_count": sum(domain["selected_count"] for domain in domains.values()),
            "total_weight": sum(domain["total_weight"] for domain in domains.values()),
        }

    @staticmethod
    def _build_solutions_payload(scenario_solutions) -> list[dict[str, Any]]:
        return [
            {
                "solution_code": solution.solution_code,
                "target_scope": solution.target_scope,
                "target_zone_id": str(solution.target_zone_id) if solution.target_zone_id else None,
                "target_system_id": str(solution.target_system_id) if solution.target_system_id else None,
                "quantity": solution.quantity,
                "unit_cost_override": solution.unit_cost_override,
                "capex_override": solution.capex_override,
                "maintenance_override": solution.maintenance_override,
                "gain_override_percent": solution.gain_override_percent,
                "notes": solution.notes,
                "is_selected": solution.is_selected,
            }
            for solution in scenario_solutions
        ]

    @staticmethod
    def _build_comparison_payload(comparison_runs) -> list[dict[str, Any]]:
        payload = []
        for run in comparison_runs:
            if run.result_summary is None or run.economic_result is None or run.scenario is None:
                continue
            payload.append(
                {
                    "scenario_id": str(run.scenario_id),
                    "scenario_name": run.scenario.name,
                    "calculation_run_id": str(run.id),
                    "baseline_energy_kwh_year": run.result_summary.baseline_energy_kwh_year,
                    "scenario_energy_kwh_year": run.result_summary.scenario_energy_kwh_year,
                    "energy_savings_percent": run.result_summary.energy_savings_percent,
                    "scenario_bacs_class": run.result_summary.scenario_bacs_class,
                    "total_capex": run.economic_result.total_capex,
                    "subsidies": run.economic_result.subsidies,
                    "net_capex": run.economic_result.net_capex,
                    "baseline_opex_year": run.economic_result.baseline_opex_year,
                    "scenario_opex_year": run.economic_result.scenario_opex_year,
                    "energy_cost_savings": run.economic_result.energy_cost_savings,
                    "maintenance_cost_year": run.economic_result.maintenance_cost_year,
                    "maintenance_savings_year": run.economic_result.maintenance_savings_year,
                    "net_annual_savings": run.economic_result.net_annual_savings,
                    "annual_cost_savings": run.economic_result.annual_cost_savings,
                    "simple_payback_years": run.economic_result.simple_payback_years,
                    "npv": run.economic_result.npv,
                    "irr": run.economic_result.irr,
                }
            )
        return payload

    @staticmethod
    def _build_assumptions_payload(input_snapshot: dict) -> list[dict[str, Any]]:
        sections = []
        for key in sorted(input_snapshot.keys()):
            value = input_snapshot[key]
            sections.append(
                {
                    "key": key,
                    "label": key.replace("_", " ").title(),
                    "value": value,
                }
            )
        return sections
