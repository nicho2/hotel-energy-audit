from typing import Literal
from uuid import UUID

from pydantic import BaseModel

ConfidenceLevel = Literal["low", "medium", "high"]


class ReadinessIssue(BaseModel):
    code: str
    message: str
    severity: Literal["error", "warning"]
    step_code: str | None = None
    step: int | None = None


class CalculationReadinessResponse(BaseModel):
    project_id: UUID
    is_ready: bool
    blocking_issues: list[ReadinessIssue]
    warnings: list[ReadinessIssue]
    confidence_level: ConfidenceLevel
