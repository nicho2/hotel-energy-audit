from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from app.schemas.zones import Orientation, ZoneType

UsageType = Literal["heating", "cooling", "ventilation", "dhw", "lighting", "auxiliaries"]


class ResultSeriesMetadata(BaseModel):
    calculation_run_id: UUID
    project_id: UUID
    scenario_id: UUID
    status: str
    engine_version: str


class ResultByUseItemResponse(BaseModel):
    usage_type: UsageType
    baseline_energy_kwh_year: float
    scenario_energy_kwh_year: float
    energy_savings_percent: float


class ResultsByUseResponse(BaseModel):
    result_set: ResultSeriesMetadata
    items: list[ResultByUseItemResponse]


class ResultByZoneItemResponse(BaseModel):
    zone_id: UUID | None
    zone_name: str
    zone_type: ZoneType
    orientation: Orientation
    baseline_energy_kwh_year: float
    scenario_energy_kwh_year: float
    energy_savings_percent: float


class ResultsByZoneResponse(BaseModel):
    result_set: ResultSeriesMetadata
    items: list[ResultByZoneItemResponse]
