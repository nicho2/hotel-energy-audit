from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

Orientation = Literal["north", "south", "east", "west", "mixed"]
ZoneType = Literal[
    "guest_rooms",
    "circulation",
    "lobby",
    "restaurant",
    "meeting",
    "technical",
    "spa",
    "pool",
    "other",
]
ValidationStatus = Literal["ok", "warning", "error"]


class BuildingZoneCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    zone_type: ZoneType
    orientation: Orientation = "mixed"
    area_m2: float = Field(gt=0)
    room_count: int = Field(default=0, ge=0)
    order_index: int = Field(default=0, ge=0)


class BuildingZoneUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    zone_type: ZoneType | None = None
    orientation: Orientation | None = None
    area_m2: float | None = Field(default=None, gt=0)
    room_count: int | None = Field(default=None, ge=0)
    order_index: int | None = Field(default=None, ge=0)


class BuildingZoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    name: str
    zone_type: ZoneType
    orientation: Orientation
    area_m2: float
    room_count: int
    order_index: int


class ZoneDistributionInput(BaseModel):
    orientation: Orientation
    room_count: int = Field(ge=1)


class BuildingZoneGenerateRequest(BaseModel):
    room_distribution: list[ZoneDistributionInput] = Field(min_length=1)
    average_room_area_m2: float = Field(default=28.0, gt=0)
    total_guest_room_area_m2: float | None = Field(default=None, gt=0)
    replace_existing: bool = True


class ZoneValidationItem(BaseModel):
    code: str
    status: ValidationStatus
    message: str


class ZoneValidationResponse(BaseModel):
    is_valid: bool
    checks: list[ZoneValidationItem]
    warnings: list[ZoneValidationItem]
