from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

TargetScope = Literal["project", "zone", "system"]
CatalogScope = Literal["global", "country_specific", "organization_specific"]


class SolutionCatalogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID | None
    name: str
    version: str
    scope: CatalogScope
    country_code: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class SolutionDefinitionBase(BaseModel):
    catalog_id: UUID
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    family: str = Field(min_length=1, max_length=50)
    target_scopes: list[TargetScope] = Field(min_length=1)
    applicable_countries: list[str] = Field(default_factory=list)
    applicable_building_types: list[str] = Field(default_factory=list)
    applicable_zone_types: list[str] = Field(default_factory=list)
    bacs_impact_json: dict = Field(default_factory=dict)
    lifetime_years: int | None = Field(default=None, gt=0)
    default_quantity: float | None = Field(default=None, gt=0)
    default_unit: str | None = Field(default=None, max_length=50)
    default_unit_cost: float | None = Field(default=None, ge=0)
    default_capex: float | None = Field(default=None, ge=0)
    priority: int = Field(default=100, ge=0)
    is_commercial_offer: bool = False
    offer_reference: str | None = Field(default=None, max_length=100)
    is_active: bool = True

    @model_validator(mode="after")
    def validate_offer_reference(self) -> "SolutionDefinitionBase":
        if self.is_commercial_offer and not self.offer_reference:
            raise ValueError("offer_reference is required for commercial offers")
        return self


class SolutionDefinitionCreate(SolutionDefinitionBase):
    pass


class SolutionDefinitionUpdate(BaseModel):
    catalog_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    family: str | None = Field(default=None, min_length=1, max_length=50)
    target_scopes: list[TargetScope] | None = Field(default=None, min_length=1)
    applicable_countries: list[str] | None = None
    applicable_building_types: list[str] | None = None
    applicable_zone_types: list[str] | None = None
    bacs_impact_json: dict | None = None
    lifetime_years: int | None = Field(default=None, gt=0)
    default_quantity: float | None = Field(default=None, gt=0)
    default_unit: str | None = Field(default=None, max_length=50)
    default_unit_cost: float | None = Field(default=None, ge=0)
    default_capex: float | None = Field(default=None, ge=0)
    priority: int | None = Field(default=None, ge=0)
    is_commercial_offer: bool | None = None
    offer_reference: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None


class SolutionDefinitionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    catalog_id: UUID
    catalog_name: str
    catalog_version: str
    scope: CatalogScope
    country_code: str | None
    organization_id: UUID | None
    code: str
    name: str
    description: str
    family: str
    target_scopes: list[TargetScope]
    applicable_countries: list[str]
    applicable_building_types: list[str]
    applicable_zone_types: list[str]
    bacs_impact_json: dict
    lifetime_years: int | None
    default_quantity: float | None
    default_unit: str | None
    default_unit_cost: float | None
    default_capex: float | None
    priority: int
    is_commercial_offer: bool
    offer_reference: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
