from typing import Any
from uuid import UUID

from pydantic import BaseModel


class ExecutiveReportHtmlResponse(BaseModel):
    calculation_run_id: UUID
    project_id: UUID
    scenario_id: UUID
    title: str
    html: str
    context: dict[str, Any]
