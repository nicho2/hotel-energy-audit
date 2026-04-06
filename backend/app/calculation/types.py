from pydantic import BaseModel
from typing import Any


class CalculationInput(BaseModel):
    project_id: str
    scenario_id: str
    building: dict[str, Any]
    zones: list[dict[str, Any]]
    systems: list[dict[str, Any]]
    bacs_functions: list[dict[str, Any]]
    selected_solutions: list[dict[str, Any]]
    assumptions: dict[str, Any]


class CalculationOutput(BaseModel):
    summary: dict[str, Any]
    by_use: list[dict[str, Any]]
    by_zone: list[dict[str, Any]]
    economic: dict[str, Any]
    bacs: dict[str, Any]
    messages: list[str]
    warnings: list[str]
