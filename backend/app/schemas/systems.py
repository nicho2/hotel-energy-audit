from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

SystemType = Literal[
    "heating",
    "cooling",
    "ventilation",
    "dhw",
    "lighting",
    "auxiliaries",
    "control",
]
EnergySource = Literal[
    "electricity",
    "natural_gas",
    "fuel_oil",
    "district_heating",
    "district_cooling",
    "lpg",
    "biomass",
    "solar",
    "ambient",
    "other",
]
TechnologyType = Literal[
    "gas_boiler",
    "oil_boiler",
    "electric_boiler",
    "heat_pump",
    "chiller",
    "dx_unit",
    "ahu",
    "cmv",
    "storage_tank",
    "instantaneous_heater",
    "led",
    "fluorescent",
    "pump",
    "fan",
    "bms",
    "other",
]
EfficiencyLevel = Literal["low", "standard", "high", "premium"]


class TechnicalSystemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    system_type: SystemType
    energy_source: EnergySource | None = None
    technology_type: TechnologyType | None = None
    efficiency_level: EfficiencyLevel | None = None
    serves: str | None = Field(default=None, max_length=255)
    quantity: int | None = Field(default=None, ge=1)
    year_installed: int | None = Field(default=None, ge=1900, le=datetime.now().year + 1)
    is_primary: bool = False
    notes: str | None = None
    order_index: int = Field(default=0, ge=0)


class TechnicalSystemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    system_type: SystemType | None = None
    energy_source: EnergySource | None = None
    technology_type: TechnologyType | None = None
    efficiency_level: EfficiencyLevel | None = None
    serves: str | None = Field(default=None, max_length=255)
    quantity: int | None = Field(default=None, ge=1)
    year_installed: int | None = Field(default=None, ge=1900, le=datetime.now().year + 1)
    is_primary: bool | None = None
    notes: str | None = None
    order_index: int | None = Field(default=None, ge=0)


class TechnicalSystemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    name: str
    system_type: SystemType
    energy_source: EnergySource | None
    technology_type: TechnologyType | None
    efficiency_level: EfficiencyLevel | None
    serves: str | None
    quantity: int | None
    year_installed: int | None
    is_primary: bool
    notes: str | None
    order_index: int
