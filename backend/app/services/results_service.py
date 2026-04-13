from uuid import UUID

from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.repositories.results_repository import ResultsRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.schemas.calculations import (
    CalculationResultLatestResponse,
    CalculationSummaryResponse,
    EconomicResultResponse,
)
from app.schemas.scenario_comparison import (
    ScenarioComparisonItemResponse,
    ScenarioComparisonRecommendationResponse,
    ScenarioComparisonResponse,
)
from app.schemas.results import (
    ResultByUseItemResponse,
    ResultByZoneItemResponse,
    ResultSeriesMetadata,
    ResultsByUseResponse,
    ResultsByZoneResponse,
)
from app.services.project_service import ProjectService


class ResultsService:
    CO2_FACTORS_KG_PER_KWH = {
        "electricity": 0.055,
        "natural_gas": 0.227,
        "fuel_oil": 0.324,
        "district_heating": 0.18,
        "district_cooling": 0.12,
        "lpg": 0.274,
        "biomass": 0.03,
        "solar": 0.0,
        "ambient": 0.0,
        "other": 0.2,
    }
    BACS_CLASS_POINTS = {"A": 100.0, "B": 80.0, "C": 60.0, "D": 40.0, "E": 20.0, "F": 0.0}

    def __init__(
        self,
        project_service: ProjectService,
        scenario_repository: ScenarioRepository,
        results_repository: ResultsRepository,
        technical_system_repository: TechnicalSystemRepository | None = None,
    ):
        self.project_service = project_service
        self.scenario_repository = scenario_repository
        self.results_repository = results_repository
        self.technical_system_repository = technical_system_repository

    def get_results_by_use(self, project_id, scenario_id, current_user) -> ResultsByUseResponse:
        run = self._get_latest_run(project_id, scenario_id, current_user)
        return ResultsByUseResponse(
            result_set=self._build_result_set(run),
            items=[
                ResultByUseItemResponse(
                    usage_type=item.usage_type,
                    baseline_energy_kwh_year=item.baseline_energy_kwh_year,
                    scenario_energy_kwh_year=item.scenario_energy_kwh_year,
                    energy_savings_percent=item.energy_savings_percent,
                )
                for item in run.results_by_use
            ],
        )

    def get_results_by_zone(self, project_id, scenario_id, current_user) -> ResultsByZoneResponse:
        run = self._get_latest_run(project_id, scenario_id, current_user)
        return ResultsByZoneResponse(
            result_set=self._build_result_set(run),
            items=[
                ResultByZoneItemResponse(
                    zone_id=item.zone_id,
                    zone_name=item.zone_name,
                    zone_type=item.zone_type,
                    orientation=item.orientation,
                    baseline_energy_kwh_year=item.baseline_energy_kwh_year,
                    scenario_energy_kwh_year=item.scenario_energy_kwh_year,
                    energy_savings_percent=item.energy_savings_percent,
                )
                for item in run.results_by_zone
            ],
        )

    def get_latest_result(self, project_id, scenario_id, current_user) -> CalculationResultLatestResponse:
        run = self._get_latest_run(project_id, scenario_id, current_user)
        summary = run.result_summary
        economic = run.economic_result
        if summary is None or economic is None:
            raise NotFoundError("Persisted result is incomplete")

        return CalculationResultLatestResponse(
            calculation_run_id=run.id,
            project_id=run.project_id,
            scenario_id=run.scenario_id,
            status=run.status,
            engine_version=run.engine_version,
            summary=CalculationSummaryResponse(
                baseline_energy_kwh_year=summary.baseline_energy_kwh_year,
                scenario_energy_kwh_year=summary.scenario_energy_kwh_year,
                energy_savings_percent=summary.energy_savings_percent,
                baseline_bacs_class=summary.baseline_bacs_class,
                scenario_bacs_class=summary.scenario_bacs_class,
            ),
            economic=EconomicResultResponse(
                total_capex=economic.total_capex,
                subsidies=economic.subsidies,
                net_capex=economic.net_capex,
                baseline_opex_year=economic.baseline_opex_year,
                scenario_opex_year=economic.scenario_opex_year,
                energy_cost_savings=economic.energy_cost_savings,
                maintenance_cost_year=economic.maintenance_cost_year,
                maintenance_savings_year=economic.maintenance_savings_year,
                net_annual_savings=economic.net_annual_savings,
                annual_cost_savings=economic.annual_cost_savings,
                simple_payback_years=economic.simple_payback_years,
                npv=economic.npv,
                irr=economic.irr,
                analysis_period_years=economic.analysis_period_years,
                discount_rate=economic.discount_rate,
                energy_inflation_rate=economic.energy_inflation_rate,
                cash_flows=economic.cash_flows,
                is_roi_calculable=economic.is_roi_calculable,
            ),
            messages=run.messages_json,
            warnings=run.warnings_json,
            input_snapshot=run.input_snapshot,
        )

    def compare_scenarios(
        self,
        project_id,
        scenario_ids: list[UUID],
        current_user,
    ) -> ScenarioComparisonResponse:
        project = self.project_service.get_project(project_id, current_user)
        scenarios = self.scenario_repository.list_by_ids(scenario_ids, project.id)
        found_ids = {scenario.id for scenario in scenarios}
        missing_ids = [scenario_id for scenario_id in scenario_ids if scenario_id not in found_ids]
        if missing_ids:
            raise NotFoundError(
                "One or more scenarios were not found",
                details={"scenario_ids": [str(value) for value in missing_ids]},
            )

        runs = self.results_repository.get_latest_by_scenario_ids(scenario_ids, project.id)
        run_by_scenario_id = {run.scenario_id: run for run in runs}
        missing_runs = [scenario_id for scenario_id in scenario_ids if scenario_id not in run_by_scenario_id]
        if missing_runs:
            raise ValidationError(
                "Comparison requires a completed calculation for each scenario",
                field="scenario_ids",
                details={"missing_calculation_scenario_ids": [str(value) for value in missing_runs]},
            )

        co2_factor = self._estimate_project_co2_factor(project.id)
        comparison_items: list[ScenarioComparisonItemResponse] = []
        ordered_scenarios = {scenario.id: scenario for scenario in scenarios}
        for scenario_id in scenario_ids:
            scenario = ordered_scenarios[scenario_id]
            run = run_by_scenario_id[scenario_id]
            summary = run.result_summary
            economic = run.economic_result
            if summary is None or economic is None:
                raise ValidationError(
                    "Comparison requires complete persisted results",
                    field="scenario_ids",
                    details={"scenario_id": str(scenario_id)},
                )

            scenario_energy = summary.scenario_energy_kwh_year
            estimated_co2 = round(scenario_energy * co2_factor, 2)
            roi_percent = round(
                (economic.annual_cost_savings / economic.total_capex) * 100.0,
                1,
            ) if economic.total_capex > 0 else 0.0
            score = self._compute_score(
                energy_savings_percent=summary.energy_savings_percent,
                scenario_bacs_class=summary.scenario_bacs_class,
                roi_percent=roi_percent,
                payback_years=economic.simple_payback_years,
                capex=economic.total_capex,
                annual_cost_savings=economic.annual_cost_savings,
            )
            comparison_items.append(
                ScenarioComparisonItemResponse(
                    scenario_id=scenario.id,
                    scenario_name=scenario.name,
                    calculation_run_id=run.id,
                    is_reference=scenario.is_reference,
                    engine_version=run.engine_version,
                    scenario_energy_kwh_year=scenario_energy,
                    estimated_co2_kg_year=estimated_co2,
                    baseline_bacs_class=summary.baseline_bacs_class,
                    scenario_bacs_class=summary.scenario_bacs_class,
                    total_capex=economic.total_capex,
                    subsidies=economic.subsidies,
                    net_capex=economic.net_capex,
                    baseline_opex_year=economic.baseline_opex_year,
                    scenario_opex_year=economic.scenario_opex_year,
                    energy_cost_savings=economic.energy_cost_savings,
                    maintenance_cost_year=economic.maintenance_cost_year,
                    maintenance_savings_year=economic.maintenance_savings_year,
                    net_annual_savings=economic.net_annual_savings,
                    annual_cost_savings=economic.annual_cost_savings,
                    simple_payback_years=economic.simple_payback_years,
                    npv=economic.npv,
                    irr=economic.irr,
                    roi_percent=roi_percent,
                    score=score,
                )
            )

        recommended_item = max(
            comparison_items,
            key=lambda item: (item.score, item.annual_cost_savings, -item.total_capex),
        )
        recommendation = ScenarioComparisonRecommendationResponse(
            scenario_id=recommended_item.scenario_id,
            scenario_name=recommended_item.scenario_name,
            score=recommended_item.score,
            reasons=self._build_recommendation_reasons(recommended_item),
        )
        return ScenarioComparisonResponse(
            project_id=project.id,
            compared_scenario_ids=scenario_ids,
            items=comparison_items,
            recommended_scenario=recommendation,
        )

    def _get_latest_run(self, project_id, scenario_id, current_user):
        project = self.project_service.get_project(project_id, current_user)
        scenario = self.scenario_repository.get_by_id(scenario_id, project.id)
        if scenario is None:
            raise NotFoundError("Scenario not found")

        run = self.results_repository.get_latest_by_scenario(scenario.id, project.id)
        if run is None:
            raise NotFoundError("Latest result not found")
        return run

    @staticmethod
    def _build_result_set(run) -> ResultSeriesMetadata:
        return ResultSeriesMetadata(
            calculation_run_id=run.id,
            project_id=run.project_id,
            scenario_id=run.scenario_id,
            status=run.status,
            engine_version=run.engine_version,
        )

    def _estimate_project_co2_factor(self, project_id) -> float:
        if self.technical_system_repository is None:
            return 0.2

        systems = self.technical_system_repository.list_by_project_id(project_id)
        weighted_factors = [
            self.CO2_FACTORS_KG_PER_KWH.get(system.energy_source or "other", 0.2)
            for system in systems
            if system.system_type in {"heating", "cooling", "dhw", "ventilation", "lighting"}
        ]
        if not weighted_factors:
            return 0.2
        return round(sum(weighted_factors) / len(weighted_factors), 3)

    def _compute_score(
        self,
        *,
        energy_savings_percent: float,
        scenario_bacs_class: str | None,
        roi_percent: float,
        payback_years: float | None,
        capex: float,
        annual_cost_savings: float,
    ) -> float:
        bacs_points = self.BACS_CLASS_POINTS.get(scenario_bacs_class or "", 0.0)
        payback_points = max(0.0, 100.0 - (payback_years * 10.0)) if payback_years is not None else 0.0
        capex_penalty = min(capex / 5000.0, 20.0)
        savings_bonus = min(annual_cost_savings / 1000.0, 20.0)
        raw_score = (
            energy_savings_percent * 2.0
            + bacs_points * 0.2
            + roi_percent * 0.8
            + payback_points * 0.2
            + savings_bonus
            - capex_penalty
        )
        return round(max(raw_score, 0.0), 1)

    def _build_recommendation_reasons(
        self,
        item: ScenarioComparisonItemResponse,
    ) -> list[str]:
        payback_label = f"{item.simple_payback_years:.1f} years" if item.simple_payback_years is not None else "not calculable"
        return [
            f"Best composite score based on energy savings, BACS level, ROI and payback ({item.score}).",
            f"Estimated annual savings are {item.annual_cost_savings:.0f} with a payback of {payback_label}.",
            f"Projected BACS class is {item.scenario_bacs_class or 'unknown'} and estimated CO2 is {item.estimated_co2_kg_year:.0f} kg/year.",
        ]
