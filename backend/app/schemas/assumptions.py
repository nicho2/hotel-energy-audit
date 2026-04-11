from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

AssumptionSource = Literal["configured", "defaulted", "calculated"]


class AssumptionItemResponse(BaseModel):
    key: str
    label: str
    value: str
    source: AssumptionSource
    note: str | None = None
    warning: bool = False


class AssumptionSectionResponse(BaseModel):
    key: str
    title: str
    items: list[AssumptionItemResponse]


class ProjectAssumptionsResponse(BaseModel):
    project_id: UUID
    calculation_run_id: UUID | None
    scenario_name: str | None
    engine_version: str
    generated_at: datetime | None
    warnings: list[str]
    sections: list[AssumptionSectionResponse]
