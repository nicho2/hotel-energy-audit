from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel


class ReportHtmlResponse(BaseModel):
    calculation_run_id: UUID
    project_id: UUID
    scenario_id: UUID
    report_type: str
    title: str
    html: str
    context: dict[str, Any]


ExecutiveReportHtmlResponse = ReportHtmlResponse


class GenerateReportRequest(BaseModel):
    scenario_id: UUID
    calculation_run_id: UUID
    report_type: Literal["executive", "detailed"] = "executive"
    language: Literal["fr", "en"] = "en"
    branding_profile_id: UUID | None = None
    include_assumptions: bool = True
    include_regulatory_section: bool = False
    include_annexes: bool = True


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
