from typing import Literal
from uuid import UUID

from pydantic import BaseModel

ConfidenceLevel = Literal["low", "medium", "high"]


class ReadinessIssue(BaseModel):
    code: str
    message: str


class CalculationReadinessResponse(BaseModel):
    project_id: UUID
    is_ready: bool
    blocking_issues: list[ReadinessIssue]
    warnings: list[ReadinessIssue]
    confidence_level: ConfidenceLevel
