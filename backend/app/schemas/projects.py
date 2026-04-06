from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

BuildingType = Literal["hotel", "aparthotel", "residence", "other_accommodation"]


class ProjectCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    client_name: str | None = None
    reference_code: str | None = Field(default=None, max_length=100)
    description: str | None = None
    country_profile_id: UUID | None = None
    climate_zone_id: UUID | None = None
    building_type: BuildingType
    project_goal: str | None = None
    branding_profile_id: UUID | None = None
    template_id: UUID | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=255)
    client_name: str | None = None
    reference_code: str | None = Field(default=None, max_length=100)
    description: str | None = None
    status: str | None = Field(default=None, max_length=50)
    wizard_step: int | None = Field(default=None, ge=1)
    building_type: BuildingType | None = None
    project_goal: str | None = Field(default=None, max_length=100)
    branding_profile_id: UUID | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    created_by_user_id: UUID
    name: str
    client_name: str | None
    reference_code: str | None
    description: str | None
    status: str
    wizard_step: int
    building_type: str
    project_goal: str | None
    branding_profile_id: UUID | None
    created_at: datetime
    updated_at: datetime
