from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class ScenarioComparisonRequest(BaseModel):
    scenario_ids: list[UUID] = Field(min_length=2, max_length=5)

    @model_validator(mode="after")
    def validate_unique_ids(self) -> "ScenarioComparisonRequest":
        if len(set(self.scenario_ids)) != len(self.scenario_ids):
            raise ValueError("scenario_ids must be unique")
        return self


class ScenarioComparisonItemResponse(BaseModel):
    scenario_id: UUID
    scenario_name: str
    calculation_run_id: UUID
    is_reference: bool
    engine_version: str
    scenario_energy_kwh_year: float
    estimated_co2_kg_year: float
    baseline_bacs_class: str | None
    scenario_bacs_class: str | None
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
    npv: float | None = None
    irr: float | None = None
    roi_percent: float
    score: float


class ScenarioComparisonRecommendationResponse(BaseModel):
    scenario_id: UUID
    scenario_name: str
    score: float
    reasons: list[str]


class ScenarioComparisonResponse(BaseModel):
    project_id: UUID
    compared_scenario_ids: list[UUID]
    items: list[ScenarioComparisonItemResponse]
    recommended_scenario: ScenarioComparisonRecommendationResponse
