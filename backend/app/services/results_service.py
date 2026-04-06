from app.core.exceptions import NotFoundError
from app.repositories.results_repository import ResultsRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.schemas.calculations import (
    CalculationResultLatestResponse,
    CalculationSummaryResponse,
    EconomicResultResponse,
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
    def __init__(
        self,
        project_service: ProjectService,
        scenario_repository: ScenarioRepository,
        results_repository: ResultsRepository,
    ):
        self.project_service = project_service
        self.scenario_repository = scenario_repository
        self.results_repository = results_repository

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
                annual_cost_savings=economic.annual_cost_savings,
                simple_payback_years=economic.simple_payback_years,
                npv=economic.npv,
                irr=economic.irr,
            ),
            messages=run.messages_json,
            warnings=run.warnings_json,
            input_snapshot=run.input_snapshot,
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
