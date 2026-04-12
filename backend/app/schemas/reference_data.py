from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.projects import BuildingType


class CountryProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    country_code: str
    name_fr: str
    name_en: str
    regulatory_scope: str
    currency_code: str
    default_language: str
    default_discount_rate: float
    default_energy_inflation_rate: float
    default_analysis_period_years: int
    created_at: datetime
    updated_at: datetime


class ClimateZoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    country_profile_id: UUID
    code: str
    name_fr: str
    name_en: str
    heating_severity_index: float
    cooling_severity_index: float
    solar_exposure_index: float
    default_weather_profile_json: dict
    is_default: bool
    created_at: datetime
    updated_at: datetime


class UsageProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    country_profile_id: UUID
    code: str
    name_fr: str
    name_en: str
    building_type: str
    zone_type: str
    default_occupancy_rate: float
    seasonality_profile_json: dict
    daily_schedule_json: dict
    ecs_intensity_level: str
    created_at: datetime
    updated_at: datetime


class ProjectTemplateCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    description: str | None = None
    building_type: BuildingType
    country_profile_id: UUID
    default_payload_json: dict = Field(default_factory=dict)
    is_active: bool = True


class ProjectTemplateUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=255)
    description: str | None = None
    building_type: BuildingType | None = None
    country_profile_id: UUID | None = None
    default_payload_json: dict | None = None
    is_active: bool | None = None


class ProjectTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    name: str
    description: str | None
    building_type: str
    country_profile_id: UUID
    default_payload_json: dict
    is_active: bool
    created_by_user_id: UUID
    created_at: datetime
    updated_at: datetime
