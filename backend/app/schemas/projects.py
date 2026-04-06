from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    client_name: str | None = None
    country_profile_id: UUID | None = None
    climate_zone_id: UUID | None = None
    building_type: Literal["hotel", "aparthotel", "residence", "other_accommodation"]
    project_goal: str | None = None
    branding_profile_id: UUID | None = None
    template_id: UUID | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    client_name: str | None
    status: str
    wizard_step: int
    building_type: str
    project_goal: str | None
    created_at: datetime
    updated_at: datetime
