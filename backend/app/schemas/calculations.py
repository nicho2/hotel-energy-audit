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
    subsidies: float | None = None
    net_capex: float | None = None
    baseline_opex_year: float | None = None
    scenario_opex_year: float | None = None
    energy_cost_savings: float | None = None
    maintenance_cost_year: float | None = None
    maintenance_savings_year: float | None = None
    net_annual_savings: float | None = None
    annual_cost_savings: float
    simple_payback_years: float | None
    npv: float
    irr: float | None
    analysis_period_years: int | None = None
    discount_rate: float | None = None
    energy_inflation_rate: float | None = None
    cash_flows: list[dict[str, Any]] | None = None
    is_roi_calculable: bool | None = None


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
