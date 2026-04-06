from app.calculation.engine import CalculationEngine
from app.calculation.types import CalculationInput
from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.bacs_repository import BacsRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.calculation_repository import CalculationRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.calculations import (
    CalculationResultLatestResponse,
    CalculationSummaryResponse,
    EconomicResultResponse,
)
from app.services.project_service import ProjectService
from app.services.readiness_service import ReadinessService


class CalculationService:
    def __init__(
        self,
        project_service: ProjectService,
        scenario_repository: ScenarioRepository,
        calculation_repository: CalculationRepository,
        building_repository: BuildingRepository,
        zone_repository: ZoneRepository,
        technical_system_repository: TechnicalSystemRepository,
        bacs_repository: BacsRepository,
        readiness_service: ReadinessService,
        engine: CalculationEngine,
    ):
        self.project_service = project_service
        self.scenario_repository = scenario_repository
        self.calculation_repository = calculation_repository
        self.building_repository = building_repository
        self.zone_repository = zone_repository
        self.technical_system_repository = technical_system_repository
        self.bacs_repository = bacs_repository
        self.readiness_service = readiness_service
        self.engine = engine

    def calculate(self, project_id, scenario_id, current_user) -> CalculationResultLatestResponse:
        project = self.project_service.get_project(project_id, current_user)
        scenario = self.scenario_repository.get_by_id(scenario_id, project.id)
        if scenario is None:
            raise NotFoundError("Scenario not found")

        readiness = self.readiness_service.get_calculation_readiness(project.id, current_user)
        if not readiness.is_ready:
            raise ValidationError(
                "Validation failed",
                field="project_id",
                details={"reason": "project is not ready for calculation"},
            )

        input_data = self._build_input(project.id, scenario.id)
        output = self.engine.run(input_data)

        run = self.calculation_repository.create_run(
            project_id=project.id,
            scenario_id=scenario.id,
            status="completed",
            engine_version="placeholder-v1",
            input_snapshot=input_data.model_dump(mode="json"),
            messages_json=output.messages,
            warnings_json=output.warnings,
        )
        self.calculation_repository.create_result_summary(run.id, **output.summary)
        self.calculation_repository.create_economic_result(run.id, **output.economic)
        self.calculation_repository.create_results_by_use(run.id, output.by_use)
        self.calculation_repository.create_results_by_zone(run.id, output.by_zone)
        latest = self.calculation_repository.get_latest_by_scenario(scenario.id, project.id)
        if latest is None:
            raise NotFoundError("Calculation result not found")
        return self._to_response(latest)

    def get_latest_result(self, project_id, scenario_id, current_user) -> CalculationResultLatestResponse:
        project = self.project_service.get_project(project_id, current_user)
        scenario = self.scenario_repository.get_by_id(scenario_id, project.id)
        if scenario is None:
            raise NotFoundError("Scenario not found")

        latest = self.calculation_repository.get_latest_by_scenario(scenario.id, project.id)
        if latest is None:
            raise NotFoundError("Latest result not found")
        return self._to_response(latest)

    def _build_input(self, project_id, scenario_id) -> CalculationInput:
        building = self.building_repository.get_by_project_id(project_id)
        zones = self.zone_repository.list_by_project_id(project_id)
        systems = self.technical_system_repository.list_by_project_id(project_id)
        assessment = self.bacs_repository.get_assessment_by_project_id(project_id)
        bacs_functions = []
        if assessment is not None:
            bacs_functions = [
                {
                    "id": str(selection.function_definition.id),
                    "code": selection.function_definition.code,
                    "domain": selection.function_definition.domain,
                    "weight": selection.function_definition.weight,
                }
                for selection in self.bacs_repository.list_selected_for_assessment(assessment.id)
            ]

        return CalculationInput(
            project_id=str(project_id),
            scenario_id=str(scenario_id),
            building=self._serialize_model(building),
            zones=[self._serialize_model(zone) for zone in zones],
            systems=[self._serialize_model(system) for system in systems],
            bacs_functions=bacs_functions,
            selected_solutions=[],
            assumptions={"engine_version": "placeholder-v1"},
        )

    @staticmethod
    def _serialize_model(model) -> dict:
        if model is None:
            return {}
        return {
            key: (str(value) if hasattr(value, "hex") else value)
            for key, value in vars(model).items()
            if not key.startswith("_")
        }

    @staticmethod
    def _to_response(run) -> CalculationResultLatestResponse:
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
