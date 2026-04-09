from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

ScenarioType = Literal["baseline", "improved", "target_bacs", "custom"]
ScenarioStatus = Literal["draft", "ready", "archived"]
TargetScope = Literal["project", "zone", "system"]


class ScenarioCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    scenario_type: ScenarioType = "custom"
    derived_from_scenario_id: UUID | None = None
    is_reference: bool = False


class ScenarioUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    scenario_type: ScenarioType | None = None
    status: ScenarioStatus | None = None
    is_reference: bool | None = None


class ScenarioDuplicateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)


class ScenarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    name: str
    description: str | None
    scenario_type: ScenarioType
    status: ScenarioStatus
    derived_from_scenario_id: UUID | None
    is_reference: bool
    created_at: datetime
    updated_at: datetime


class SolutionCatalogItemResponse(BaseModel):
    code: str
    name: str
    description: str
    solution_family: str
    target_scopes: list[TargetScope]
    default_quantity: float | None = None
    default_unit: str | None = None


class ScenarioSolutionAssignmentCreate(BaseModel):
    solution_code: str
    target_scope: TargetScope = "project"
    target_zone_id: UUID | None = None
    target_system_id: UUID | None = None
    quantity: float | None = Field(default=None, gt=0)
    unit_cost_override: float | None = Field(default=None, ge=0)
    capex_override: float | None = Field(default=None, ge=0)
    maintenance_override: float | None = Field(default=None, ge=0)
    gain_override_percent: float | None = Field(default=None, ge=0, le=1)
    notes: str | None = None
    is_selected: bool = True

    @model_validator(mode="after")
    def validate_target(self) -> "ScenarioSolutionAssignmentCreate":
        if self.target_scope == "zone" and self.target_zone_id is None:
            raise ValueError("target_zone_id is required when target_scope is zone")
        if self.target_scope == "system" and self.target_system_id is None:
            raise ValueError("target_system_id is required when target_scope is system")
        return self


class ScenarioSolutionAssignmentUpdate(BaseModel):
    target_scope: TargetScope | None = None
    target_zone_id: UUID | None = None
    target_system_id: UUID | None = None
    quantity: float | None = Field(default=None, gt=0)
    unit_cost_override: float | None = Field(default=None, ge=0)
    capex_override: float | None = Field(default=None, ge=0)
    maintenance_override: float | None = Field(default=None, ge=0)
    gain_override_percent: float | None = Field(default=None, ge=0, le=1)
    notes: str | None = None
    is_selected: bool | None = None


class ScenarioSolutionAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    scenario_id: UUID
    solution_code: str
    target_scope: TargetScope
    target_zone_id: UUID | None
    target_system_id: UUID | None
    quantity: float | None
    unit_cost_override: float | None
    capex_override: float | None
    maintenance_override: float | None
    gain_override_percent: float | None
    notes: str | None
    is_selected: bool
    created_at: datetime
    updated_at: datetime


class ScenarioSolutionDetailedResponse(ScenarioSolutionAssignmentResponse):
    solution_name: str
    solution_description: str
    solution_family: str
