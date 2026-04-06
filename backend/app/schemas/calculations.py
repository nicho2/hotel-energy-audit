from typing import Any
from uuid import UUID

from pydantic import BaseModel


class CalculationSummaryResponse(BaseModel):
    baseline_energy_kwh_year: float
    scenario_energy_kwh_year: float
    energy_savings_percent: float
    baseline_bacs_class: str | None
    scenario_bacs_class: str | None


class EconomicResultResponse(BaseModel):
    total_capex: float
    annual_cost_savings: float
    simple_payback_years: float
    npv: float
    irr: float


class CalculationResultLatestResponse(BaseModel):
    calculation_run_id: UUID
    project_id: UUID
    scenario_id: UUID
    status: str
    engine_version: str
    summary: CalculationSummaryResponse
    economic: EconomicResultResponse
    messages: list[str]
    warnings: list[str]
    input_snapshot: dict[str, Any]
