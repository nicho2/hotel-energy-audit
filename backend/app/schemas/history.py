from datetime import datetime
from typing import Literal

from pydantic import BaseModel

AuditEventAction = Literal[
    "project_created",
    "project_updated",
    "scenario_created",
    "scenario_updated",
    "report_generated",
]


class ProjectHistoryEventResponse(BaseModel):
    action: AuditEventAction
    actor: str
    occurred_at: datetime
    summary: str
