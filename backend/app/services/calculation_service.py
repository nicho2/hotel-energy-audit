from datetime import date, datetime

from app.calculation.engine import ENGINE_VERSION, CalculationEngine
from app.calculation.types import CalculationInput
from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.assumption_set_repository import AssumptionSetRepository
from app.repositories.bacs_repository import BacsRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.calculation_repository import CalculationRepository
from app.repositories.reference_data_repository import ReferenceDataRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.scenario_solution_repository import ScenarioSolutionRepository
from app.repositories.solution_catalog_repository import SolutionCatalogRepository
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.repositories.wizard_step_payload_repository import WizardStepPayloadRepository
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
        wizard_step_payload_repository: WizardStepPayloadRepository,
        scenario_solution_repository: ScenarioSolutionRepository,
        solution_catalog_repository: SolutionCatalogRepository,
        assumption_set_repository: AssumptionSetRepository,
        reference_data_repository: ReferenceDataRepository,
        readiness_service: ReadinessService,
        engine: CalculationEngine,
        audit_service=None,
    ):
        self.project_service = project_service
        self.scenario_repository = scenario_repository
        self.calculation_repository = calculation_repository
        self.building_repository = building_repository
        self.zone_repository = zone_repository
        self.technical_system_repository = technical_system_repository
        self.bacs_repository = bacs_repository
        self.wizard_step_payload_repository = wizard_step_payload_repository
        self.scenario_solution_repository = scenario_solution_repository
        self.solution_catalog_repository = solution_catalog_repository
        self.assumption_set_repository = assumption_set_repository
        self.reference_data_repository = reference_data_repository
        self.readiness_service = readiness_service
        self.engine = engine
        self.audit_service = audit_service

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

        input_data = self._build_input(project, scenario.id)
        output = self.engine.run(input_data)

        run = self.calculation_repository.create_run(
            project_id=project.id,
            scenario_id=scenario.id,
            status="completed",
            engine_version=input_data.assumptions.get("engine_version", ENGINE_VERSION),
            input_snapshot=input_data.model_dump(mode="json"),
            messages_json=output.messages,
            warnings_json=output.warnings,
        )
        self.calculation_repository.create_result_summary(run.id, **output.summary)
        self.calculation_repository.create_economic_result(run.id, **output.economic)
        self.calculation_repository.create_results_by_use(run.id, output.by_use)
        self.calculation_repository.create_results_by_zone(run.id, output.by_zone)
        if self.audit_service is not None:
            self.audit_service.log(
                entity_type="calculation_run",
                entity_id=run.id,
                action="scenario_calculated",
                current_user=current_user,
                after_json={
                    "id": run.id,
                    "project_id": project.id,
                    "scenario_id": scenario.id,
                    "status": run.status,
                    "engine_version": run.engine_version,
                    "baseline_energy_kwh_year": output.summary["baseline_energy_kwh_year"],
                    "scenario_energy_kwh_year": output.summary["scenario_energy_kwh_year"],
                    "energy_savings_percent": output.summary["energy_savings_percent"],
                },
                project_id=project.id,
                scenario_id=scenario.id,
            )
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

    def _build_input(self, project, scenario_id) -> CalculationInput:
        building = self.building_repository.get_by_project_id(project.id)
        zones = self.zone_repository.list_by_project_id(project.id)
        systems = self.technical_system_repository.list_by_project_id(project.id)
        assessment = self.bacs_repository.get_assessment_by_project_id(project.id)
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
        usage_payload = self.wizard_step_payload_repository.get_by_project_and_step(project.id, "usage")
        climate_zone = (
            self.reference_data_repository.get_climate_zone(project.climate_zone_id)
            if project.climate_zone_id is not None
            else None
        )
        country_profile = (
            self.reference_data_repository.get_country_profile(project.country_profile_id)
            if project.country_profile_id is not None
            else None
        )
        assumption_set = self.assumption_set_repository.get_active_for_context(
            organization_id=project.organization_id,
            country_profile_id=project.country_profile_id,
        )

        return CalculationInput(
            project_id=str(project.id),
            scenario_id=str(scenario_id),
            building=self._serialize_model(building),
            zones=[self._serialize_model(zone) for zone in zones],
            systems=[self._serialize_model(system) for system in systems],
            bacs_functions=bacs_functions,
            selected_solutions=self._selected_solutions(scenario_id, project.id, project.organization_id),
            assumptions=self._build_assumptions(
                assumption_set=assumption_set,
                country_profile=country_profile,
                climate_zone=climate_zone,
                usage_payload=usage_payload.payload_json if usage_payload is not None else {},
            ),
        )

    def _selected_solutions(self, scenario_id, project_id, organization_id) -> list[dict]:
        selected = []
        for assignment in self.scenario_solution_repository.list_by_scenario_id(scenario_id):
            data = self._serialize_model(assignment)
            if assignment.target_system_id is not None:
                system = self.technical_system_repository.get_by_id(assignment.target_system_id, project_id)
                if system is not None:
                    data["target_system_type"] = system.system_type
            solution = self.solution_catalog_repository.get_solution_by_code(
                assignment.solution_code,
                organization_id,
                include_inactive=True,
            )
            if solution is not None:
                data.update(
                    {
                        "family": solution.family,
                        "default_capex": solution.default_capex,
                        "default_unit_cost": solution.default_unit_cost,
                        "default_quantity": solution.default_quantity,
                        "default_unit": solution.default_unit,
                        "bacs_impact_json": solution.bacs_impact_json,
                    }
                )
            selected.append(data)
        return selected

    @staticmethod
    def _build_assumptions(*, assumption_set, country_profile, climate_zone, usage_payload: dict) -> dict:
        assumptions = {"engine_version": ENGINE_VERSION, "usage_payload": usage_payload}
        if assumption_set is not None:
            assumptions.update(
                {
                    "assumption_set_id": str(assumption_set.id),
                    "assumption_set_version": assumption_set.version,
                    "assumption_set_scope": assumption_set.scope,
                    "heating_model_json": assumption_set.heating_model_json,
                    "cooling_model_json": assumption_set.cooling_model_json,
                    "ventilation_model_json": assumption_set.ventilation_model_json,
                    "dhw_model_json": assumption_set.dhw_model_json,
                    "lighting_model_json": assumption_set.lighting_model_json,
                    "auxiliaries_model_json": assumption_set.auxiliaries_model_json,
                    "economic_defaults_json": assumption_set.economic_defaults_json,
                    "bacs_rules_json": assumption_set.bacs_rules_json,
                    "scoring_rules_json": assumption_set.scoring_rules_json,
                    "co2_factors_json": assumption_set.co2_factors_json,
                }
            )
        if country_profile is not None:
            economic = dict(assumptions.get("economic_defaults_json", {}))
            economic.setdefault("discount_rate", country_profile.default_discount_rate)
            economic.setdefault("energy_inflation_rate", country_profile.default_energy_inflation_rate)
            economic.setdefault("analysis_period_years", country_profile.default_analysis_period_years)
            assumptions["economic_defaults_json"] = economic
            assumptions["country_profile"] = {
                "id": str(country_profile.id),
                "country_code": country_profile.country_code,
                "currency_code": country_profile.currency_code,
            }
        if climate_zone is not None:
            assumptions["climate_zone"] = {
                "id": str(climate_zone.id),
                "code": climate_zone.code,
                "heating_severity_index": climate_zone.heating_severity_index,
                "cooling_severity_index": climate_zone.cooling_severity_index,
                "solar_exposure_index": climate_zone.solar_exposure_index,
            }
        return assumptions

    @staticmethod
    def _serialize_model(model) -> dict:
        if model is None:
            return {}
        return {
            key: CalculationService._serialize_value(value)
            for key, value in vars(model).items()
            if not key.startswith("_")
        }

    @staticmethod
    def _serialize_value(value):
        if hasattr(value, "hex"):
            return str(value)
        if isinstance(value, datetime | date):
            return value.isoformat()
        return value

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
