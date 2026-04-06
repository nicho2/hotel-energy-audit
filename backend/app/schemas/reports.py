from datetime import datetime
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


class GeneratedReportResponse(BaseModel):
    id: UUID
    organization_id: UUID
    project_id: UUID
    scenario_id: UUID
    calculation_run_id: UUID
    branding_profile_id: UUID | None
    report_type: str
    status: str
    title: str
    file_name: str
    mime_type: str
    file_size_bytes: int
    generator_version: str
    created_at: datetime
