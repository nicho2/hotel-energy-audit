from dataclasses import dataclass
from typing import Any
from uuid import UUID

from app.core.exceptions import ValidationError
from app.db.models.project import Project
from app.repositories.bacs_repository import BacsRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.scenario_solution_repository import ScenarioSolutionRepository
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.repositories.wizard_step_payload_repository import WizardStepPayloadRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.wizard import (
    WizardReadinessResponse,
    WizardStateResponse,
    WizardStepResponse,
    WizardStepSaveResponse,
    WizardStepValidationResponse,
    WizardStepValidationResult,
)
from app.services.project_service import ProjectService


@dataclass(frozen=True)
class WizardStepDefinition:
    step: int
    code: str
    name: str


WIZARD_STEP_DEFINITIONS: tuple[WizardStepDefinition, ...] = (
    WizardStepDefinition(step=1, code="project", name="Project"),
    WizardStepDefinition(step=2, code="context", name="Context"),
    WizardStepDefinition(step=3, code="building", name="Building"),
    WizardStepDefinition(step=4, code="zones", name="Zones"),
    WizardStepDefinition(step=5, code="usage", name="Usage"),
    WizardStepDefinition(step=6, code="systems", name="Systems"),
    WizardStepDefinition(step=7, code="bacs", name="BACS"),
    WizardStepDefinition(step=8, code="solutions", name="Solutions"),
    WizardStepDefinition(step=9, code="scenarios", name="Scenarios"),
    WizardStepDefinition(step=10, code="review", name="Review"),
)


STEP_BY_CODE = {definition.code: definition for definition in WIZARD_STEP_DEFINITIONS}


class WizardService:
    def __init__(
        self,
        project_service: ProjectService,
        payload_repository: WizardStepPayloadRepository,
        building_repository: BuildingRepository,
        zone_repository: ZoneRepository,
        technical_system_repository: TechnicalSystemRepository,
        bacs_repository: BacsRepository,
        scenario_repository: ScenarioRepository,
        scenario_solution_repository: ScenarioSolutionRepository,
    ):
        self.project_service = project_service
        self.payload_repository = payload_repository
        self.building_repository = building_repository
        self.zone_repository = zone_repository
        self.technical_system_repository = technical_system_repository
        self.bacs_repository = bacs_repository
        self.scenario_repository = scenario_repository
        self.scenario_solution_repository = scenario_solution_repository

    def get_wizard_state(self, project_id, current_user) -> WizardStateResponse:
        project = self.project_service.get_project(project_id, current_user)
        current_step = min(max(project.wizard_step, 1), len(WIZARD_STEP_DEFINITIONS))
        payloads = self._build_step_payloads(project)
        validations_by_step = {
            definition.step: self._validate_definition(project, definition, payloads).valid
            for definition in WIZARD_STEP_DEFINITIONS
        }
        steps = [
            WizardStepResponse(
                step=definition.step,
                code=definition.code,
                name=definition.name,
                status=self._get_step_status(definition.step, current_step, validations_by_step[definition.step]),
                validations=self._build_step_validations(definition, project, payloads),
            )
            for definition in WIZARD_STEP_DEFINITIONS
        ]
        return WizardStateResponse(
            project_id=project.id,
            current_step=current_step,
            steps=steps,
            readiness=self._build_readiness(validations_by_step),
            step_payloads=payloads,
        )

    @staticmethod
    def _get_step_status(step: int, current_step: int, is_valid: bool) -> str:
        if step < current_step and is_valid:
            return "completed"
        if step == current_step:
            return "current"
        return "not_started"

    def save_step(self, project_id, step_code: str, payload: dict[str, Any], current_user) -> WizardStepSaveResponse:
        definition = self._get_definition(step_code)
        project = self.project_service.get_project(project_id, current_user)
        normalized_payload = dict(payload)

        if definition.code == "project":
            normalized_payload = self._save_project_payload(project, normalized_payload)
        elif definition.code == "context":
            normalized_payload = self._save_context_payload(project, normalized_payload)
        else:
            self.payload_repository.upsert(project.id, definition.code, normalized_payload)

        self._advance_to(project, definition.step)
        return WizardStepSaveResponse(
            project_id=project.id,
            step_code=definition.code,
            saved=True,
            payload=normalized_payload,
        )

    def validate_step(self, project_id, step_code: str, current_user) -> WizardStepValidationResult:
        definition = self._get_definition(step_code)
        project = self.project_service.get_project(project_id, current_user)
        result = self._validate_definition(project, definition, self._build_step_payloads(project))
        if result.valid:
            self._advance_to(project, min(definition.step + 1, len(WIZARD_STEP_DEFINITIONS)))
        return result

    def _get_definition(self, step_code: str) -> WizardStepDefinition:
        definition = STEP_BY_CODE.get(step_code)
        if definition is None:
            raise ValidationError(
                "Unknown wizard step",
                field="step_name",
                details={"allowed_steps": list(STEP_BY_CODE)},
            )
        return definition

    def _save_project_payload(self, project: Project, payload: dict[str, Any]) -> dict[str, Any]:
        allowed_fields = {
            "name",
            "client_name",
            "reference_code",
            "description",
            "building_type",
            "project_goal",
        }
        updates = {key: value for key, value in payload.items() if key in allowed_fields}
        if updates:
            self.project_service.repo.update(project, **updates)
        return self._project_payload(project)

    def _save_context_payload(self, project: Project, payload: dict[str, Any]) -> dict[str, Any]:
        updates = {
            key: self._to_uuid(value) if key in {"country_profile_id", "climate_zone_id"} else value
            for key, value in payload.items()
            if key in {"country_profile_id", "climate_zone_id"}
        }
        if updates:
            self.project_service.repo.update(project, **updates)

        draft_payload = {
            key: value
            for key, value in payload.items()
            if key not in {"country_profile_id", "climate_zone_id"}
        }
        if draft_payload:
            self.payload_repository.upsert(project.id, "context", draft_payload)
        return self._context_payload(project) | draft_payload

    def _advance_to(self, project: Project, step_number: int) -> None:
        next_step = min(max(step_number, 1), len(WIZARD_STEP_DEFINITIONS))
        if project.wizard_step < next_step:
            self.project_service.repo.update(project, wizard_step=next_step)

    def _build_step_payloads(self, project: Project) -> dict[str, dict[str, Any]]:
        payloads = {
            payload.step_code: dict(payload.payload_json)
            for payload in self.payload_repository.list_by_project_id(project.id)
        }
        payloads["project"] = self._project_payload(project) | payloads.get("project", {})
        payloads["context"] = self._context_payload(project) | payloads.get("context", {})
        return payloads

    @staticmethod
    def _to_uuid(value: Any) -> UUID | None:
        if value in {None, ""}:
            return None
        if isinstance(value, UUID):
            return value
        try:
            return UUID(str(value))
        except ValueError as exc:
            raise ValidationError("Invalid UUID value", details={"value": str(value)}) from exc

    @staticmethod
    def _to_float(value: Any) -> float | None:
        if value in {None, ""}:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _project_payload(project: Project) -> dict[str, Any]:
        return {
            "name": project.name,
            "client_name": project.client_name,
            "reference_code": project.reference_code,
            "description": project.description,
            "building_type": project.building_type,
            "project_goal": project.project_goal,
        }

    @staticmethod
    def _context_payload(project: Project) -> dict[str, Any]:
        return {
            "country_profile_id": str(project.country_profile_id) if project.country_profile_id else "",
            "climate_zone_id": str(project.climate_zone_id) if project.climate_zone_id else "",
        }

    def _build_step_validations(
        self,
        definition: WizardStepDefinition,
        project: Project,
        payloads: dict[str, dict[str, Any]],
    ) -> list[WizardStepValidationResponse]:
        return self._validate_definition(project, definition, payloads).validations

    def _build_readiness(self, validations_by_step: dict[int, bool]) -> WizardReadinessResponse:
        blocking_steps = [
            definition.step
            for definition in WIZARD_STEP_DEFINITIONS
            if not validations_by_step[definition.step]
        ]
        return WizardReadinessResponse(
            status="ready" if not blocking_steps else "not_ready",
            can_calculate=not blocking_steps,
            blocking_steps=blocking_steps,
            pending_validations=[
                definition.code
                for definition in WIZARD_STEP_DEFINITIONS
                if not validations_by_step[definition.step]
            ],
        )

    def _validate_definition(
        self,
        project: Project,
        definition: WizardStepDefinition,
        payloads: dict[str, dict[str, Any]],
    ) -> WizardStepValidationResult:
        checks = self._checks_for_step(project, definition.code, payloads)
        is_valid = not any(check.status == "error" for check in checks)
        message = "Step validation passed." if is_valid else "Step validation failed."
        return WizardStepValidationResult(
            step_code=definition.code,
            valid=is_valid,
            message=message,
            validations=checks,
        )

    def _checks_for_step(
        self,
        project: Project,
        step_code: str,
        payloads: dict[str, dict[str, Any]],
    ) -> list[WizardStepValidationResponse]:
        if step_code == "project":
            return [
                self._check(bool(project.name and len(project.name.strip()) >= 3), "project_name", "Project name is required."),
                self._check(bool(project.building_type), "building_type", "Building type is required."),
            ]

        if step_code == "context":
            return [
                self._check(project.country_profile_id is not None, "country_profile_id", "Country profile is required."),
                self._check(project.climate_zone_id is not None, "climate_zone_id", "Climate zone is required."),
            ]

        if step_code == "building":
            building = self.building_repository.get_by_project_id(project.id)
            return [
                self._check(building is not None, "building_present", "Building data is required."),
                self._check(
                    bool(building and (building.heated_area_m2 or building.gross_floor_area_m2)),
                    "building_area",
                    "A reference building area is required.",
                ),
                self._check(
                    bool(building and building.number_of_rooms is not None),
                    "building_rooms",
                    "Number of rooms is required.",
                ),
            ]

        if step_code == "zones":
            zones = self.zone_repository.list_by_project_id(project.id)
            total_area = sum(zone.area_m2 for zone in zones)
            return [
                self._check(bool(zones), "zones_present", "At least one functional zone is required."),
                self._check(total_area > 0, "zones_area", "Zone area must be greater than zero."),
            ]

        if step_code == "usage":
            usage_payload = payloads.get("usage", {})
            occupancy = usage_payload.get("average_occupancy_rate")
            occupancy_value = self._to_float(occupancy)
            return [
                self._check(occupancy is not None, "average_occupancy_rate", "Average occupancy is required."),
                self._check(
                    occupancy_value is not None and 0 <= occupancy_value <= 1,
                    "average_occupancy_rate_range",
                    "Average occupancy must be between 0 and 1.",
                ),
                self._check(bool(usage_payload.get("ecs_intensity_level")), "ecs_intensity_level", "DHW intensity is required."),
            ]

        if step_code == "systems":
            systems = self.technical_system_repository.list_by_project_id(project.id)
            return [
                self._check(bool(systems), "systems_present", "At least one technical system is required."),
                self._check(
                    any(system.system_type == "heating" for system in systems),
                    "heating_system",
                    "A heating system is required.",
                ),
            ]

        if step_code == "bacs":
            assessment = self.bacs_repository.get_assessment_by_project_id(project.id)
            selected_count = len(assessment.selected_functions) if assessment else 0
            return [
                self._check(assessment is not None, "bacs_assessment", "BACS assessment is required."),
                self._check(selected_count > 0, "bacs_functions", "At least one BACS function must be selected."),
            ]

        if step_code == "solutions":
            solutions_payload = payloads.get("solutions", {})
            selected_codes = solutions_payload.get("selected_solution_codes") or []
            return [
                self._check(bool(selected_codes), "selected_solution_codes", "At least one solution must be selected."),
            ]

        if step_code == "scenarios":
            scenarios = self.scenario_repository.list_by_project_id(project.id)
            scenario_payload = payloads.get("scenarios", {})
            has_payload_scenarios = bool(
                scenario_payload.get("reference_scenario_name")
                and scenario_payload.get("improvement_scenario_name")
            )
            return [
                self._check(
                    len(scenarios) >= 1 or has_payload_scenarios,
                    "scenarios_present",
                    "At least one saved scenario or scenario draft is required.",
                ),
            ]

        if step_code == "review":
            review_payload = payloads.get("review", {})
            previous_steps_valid = all(
                self._validate_definition(project, definition, payloads).valid
                for definition in WIZARD_STEP_DEFINITIONS
                if definition.code != "review"
            )
            return [
                self._check(previous_steps_valid, "previous_steps", "All previous wizard steps must be valid."),
                self._check(review_payload.get("ready_for_report") is True, "ready_for_report", "Review must be confirmed."),
            ]

        return [self._check(False, "unknown_step", "Unknown wizard step.")]

    @staticmethod
    def _check(condition: bool, code: str, message: str) -> WizardStepValidationResponse:
        return WizardStepValidationResponse(
            code=code,
            status="ok" if condition else "error",
            message=message if not condition else f"{code} ok.",
        )
