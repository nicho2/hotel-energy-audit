from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field

WizardStepStatus = Literal["completed", "current", "not_started"]
ReadinessStatus = Literal["not_ready", "ready"]


class WizardStepValidationResponse(BaseModel):
    code: str
    status: Literal["ok", "warning", "error", "pending"]
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
    blocking_reasons: list[WizardStepValidationResponse] = Field(default_factory=list)
    warnings: list[WizardStepValidationResponse] = Field(default_factory=list)


class WizardStateResponse(BaseModel):
    project_id: UUID
    current_step: int
    steps: list[WizardStepResponse]
    readiness: WizardReadinessResponse
    step_payloads: dict[str, dict[str, Any]] = Field(default_factory=dict)


class WizardStepSaveRequest(BaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class WizardStepSaveResponse(BaseModel):
    project_id: UUID
    step_code: str
    saved: bool
    payload: dict[str, Any] = Field(default_factory=dict)


class WizardStepValidationResult(BaseModel):
    step_code: str
    valid: bool
    message: str
    validations: list[WizardStepValidationResponse] = Field(default_factory=list)
