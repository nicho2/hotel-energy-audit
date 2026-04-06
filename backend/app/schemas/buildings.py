from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

Orientation = Literal["north", "south", "east", "west", "mixed"]


class BuildingUpsert(BaseModel):
    name: str | None = None
    construction_period: str | None = None
    gross_floor_area_m2: float | None = None
    heated_area_m2: float | None = None
    cooled_area_m2: float | None = None
    number_of_floors: int | None = None
    number_of_rooms: int | None = None
    main_orientation: Orientation | None = None
    compactness_level: str | None = None
    has_restaurant: bool = False
    has_meeting_rooms: bool = False
    has_spa: bool = False
    has_pool: bool = False


class BuildingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    name: str | None
    construction_period: str | None
    gross_floor_area_m2: float | None
    heated_area_m2: float | None
    cooled_area_m2: float | None
    number_of_floors: int | None
    number_of_rooms: int | None
    main_orientation: Orientation | None
    compactness_level: str | None
    has_restaurant: bool
    has_meeting_rooms: bool
    has_spa: bool
    has_pool: bool
