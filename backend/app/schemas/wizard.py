from typing import Literal
from uuid import UUID

from pydantic import BaseModel

WizardStepStatus = Literal["completed", "current", "not_started"]
ReadinessStatus = Literal["not_ready", "ready"]


class WizardStepValidationResponse(BaseModel):
    code: str
    status: Literal["pending"]
    message: str


class WizardStepResponse(BaseModel):
    step: int
    code: str
    name: str
    status: WizardStepStatus
    validations: list[WizardStepValidationResponse]


class WizardReadinessResponse(BaseModel):
    status: ReadinessStatus
    can_calculate: bool
    blocking_steps: list[int]
    pending_validations: list[str]


class WizardStateResponse(BaseModel):
    project_id: UUID
    current_step: int
    steps: list[WizardStepResponse]
    readiness: WizardReadinessResponse
