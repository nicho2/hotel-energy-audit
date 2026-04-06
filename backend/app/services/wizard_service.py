from dataclasses import dataclass

from app.schemas.wizard import (
    WizardReadinessResponse,
    WizardStateResponse,
    WizardStepResponse,
    WizardStepValidationResponse,
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


class WizardService:
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    def get_wizard_state(self, project_id, current_user) -> WizardStateResponse:
        project = self.project_service.get_project(project_id, current_user)
        current_step = min(max(project.wizard_step, 1), len(WIZARD_STEP_DEFINITIONS))
        steps = [
            WizardStepResponse(
                step=definition.step,
                code=definition.code,
                name=definition.name,
                status=self._get_step_status(definition.step, current_step),
                validations=self._build_step_validations(definition.step, current_step),
            )
            for definition in WIZARD_STEP_DEFINITIONS
        ]
        return WizardStateResponse(
            project_id=project.id,
            current_step=current_step,
            steps=steps,
            readiness=self._build_readiness(current_step),
        )

    @staticmethod
    def _get_step_status(step: int, current_step: int) -> str:
        if step < current_step:
            return "completed"
        if step == current_step:
            return "current"
        return "not_started"

    @staticmethod
    def _build_step_validations(step: int, current_step: int) -> list[WizardStepValidationResponse]:
        if step > current_step:
            return [
                WizardStepValidationResponse(
                    code="step_validation_pending",
                    status="pending",
                    message="Validation rules will be evaluated when this step is reached.",
                )
            ]
        return []

    @staticmethod
    def _build_readiness(current_step: int) -> WizardReadinessResponse:
        blocking_steps = [
            definition.step
            for definition in WIZARD_STEP_DEFINITIONS
            if definition.step >= current_step
        ]
        return WizardReadinessResponse(
            status="ready" if not blocking_steps else "not_ready",
            can_calculate=False,
            blocking_steps=blocking_steps,
            pending_validations=["wizard_step_rules"],
        )
