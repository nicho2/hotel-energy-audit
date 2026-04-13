from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

AssumptionSetScope = Literal["platform_default", "country_default", "organization_override"]


class AssumptionSetBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    version: str = Field(min_length=1, max_length=50)
    scope: AssumptionSetScope
    country_profile_id: UUID | None = None
    heating_model_json: dict[str, Any]
    cooling_model_json: dict[str, Any]
    ventilation_model_json: dict[str, Any] = Field(default_factory=dict)
    dhw_model_json: dict[str, Any]
    lighting_model_json: dict[str, Any]
    auxiliaries_model_json: dict[str, Any] = Field(default_factory=dict)
    economic_defaults_json: dict[str, Any]
    bacs_rules_json: dict[str, Any]
    scoring_rules_json: dict[str, Any] = Field(default_factory=dict)
    co2_factors_json: dict[str, Any]
    notes: str | None = None
    is_active: bool = False

    @model_validator(mode="after")
    def validate_assumption_payloads(self) -> "AssumptionSetBase":
        validate_scope(self.scope, self.country_profile_id)
        validate_assumption_json_payloads(self.model_dump())
        return self


class AssumptionSetCreate(AssumptionSetBase):
    pass


class AssumptionSetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    version: str | None = Field(default=None, min_length=1, max_length=50)
    scope: AssumptionSetScope | None = None
    country_profile_id: UUID | None = None
    heating_model_json: dict[str, Any] | None = None
    cooling_model_json: dict[str, Any] | None = None
    ventilation_model_json: dict[str, Any] | None = None
    dhw_model_json: dict[str, Any] | None = None
    lighting_model_json: dict[str, Any] | None = None
    auxiliaries_model_json: dict[str, Any] | None = None
    economic_defaults_json: dict[str, Any] | None = None
    bacs_rules_json: dict[str, Any] | None = None
    scoring_rules_json: dict[str, Any] | None = None
    co2_factors_json: dict[str, Any] | None = None
    notes: str | None = None
    is_active: bool | None = None


class AssumptionSetCloneRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    version: str = Field(min_length=1, max_length=50)
    scope: AssumptionSetScope | None = None
    country_profile_id: UUID | None = None
    notes: str | None = None
    is_active: bool = False


class AssumptionSetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID | None
    country_profile_id: UUID | None
    cloned_from_id: UUID | None
    name: str
    version: str
    scope: str
    heating_model_json: dict[str, Any]
    cooling_model_json: dict[str, Any]
    ventilation_model_json: dict[str, Any]
    dhw_model_json: dict[str, Any]
    lighting_model_json: dict[str, Any]
    auxiliaries_model_json: dict[str, Any]
    economic_defaults_json: dict[str, Any]
    bacs_rules_json: dict[str, Any]
    scoring_rules_json: dict[str, Any]
    co2_factors_json: dict[str, Any]
    notes: str | None
    is_active: bool
    is_locked: bool
    historical_calculation_count: int
    created_at: datetime
    updated_at: datetime


def validate_scope(scope: str, country_profile_id: UUID | None) -> None:
    if scope == "country_default" and country_profile_id is None:
        raise ValueError("country_profile_id is required for country_default scope")
    if scope != "country_default" and country_profile_id is not None:
        raise ValueError("country_profile_id is only supported for country_default scope")


def validate_assumption_json_payloads(payload: dict[str, Any]) -> None:
    for field_name in [
        "heating_model_json",
        "cooling_model_json",
        "ventilation_model_json",
        "lighting_model_json",
        "auxiliaries_model_json",
    ]:
        _validate_reference_intensity_m2(
            field_name,
            payload.get(field_name, {}),
            required=field_name not in {"ventilation_model_json", "auxiliaries_model_json"},
        )
    _validate_dhw_model(payload.get("dhw_model_json", {}))
    _validate_economic_defaults(payload.get("economic_defaults_json", {}))
    _validate_bacs_rules(payload.get("bacs_rules_json", {}))
    _validate_scoring_rules(payload.get("scoring_rules_json", {}))
    _validate_co2_factors(payload.get("co2_factors_json", {}))


def _validate_reference_intensity_m2(
    field_name: str,
    data: dict[str, Any],
    *,
    required: bool,
) -> None:
    if not isinstance(data, dict):
        raise ValueError(f"{field_name} must be an object")
    value = data.get("reference_intensity_kwh_m2")
    if value is None:
        if required:
            raise ValueError(f"{field_name}.reference_intensity_kwh_m2 is required")
        return
    _require_positive_number(f"{field_name}.reference_intensity_kwh_m2", value)


def _validate_dhw_model(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise ValueError("dhw_model_json must be an object")
    if "reference_intensity_kwh_room" in data:
        _require_positive_number(
            "dhw_model_json.reference_intensity_kwh_room",
            data["reference_intensity_kwh_room"],
        )
        return
    if "reference_intensity_kwh_m2" in data:
        _require_positive_number(
            "dhw_model_json.reference_intensity_kwh_m2",
            data["reference_intensity_kwh_m2"],
        )
        return
    raise ValueError("dhw_model_json.reference_intensity_kwh_room is required")


def _validate_economic_defaults(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise ValueError("economic_defaults_json must be an object")
    for key in ["discount_rate", "energy_inflation_rate"]:
        value = data.get(key)
        if not isinstance(value, int | float) or value < 0 or value > 1:
            raise ValueError(f"economic_defaults_json.{key} must be between 0 and 1")
    period = data.get("analysis_period_years")
    if not isinstance(period, int) or period <= 0:
        raise ValueError("economic_defaults_json.analysis_period_years must be a positive integer")


def _validate_bacs_rules(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise ValueError("bacs_rules_json must be an object")
    score_to_class = data.get("score_to_class")
    if not isinstance(score_to_class, dict):
        raise ValueError("bacs_rules_json.score_to_class is required")
    for class_name in ["A", "B", "C", "D"]:
        bounds = score_to_class.get(class_name)
        if not isinstance(bounds, list) or len(bounds) != 2:
            raise ValueError(f"bacs_rules_json.score_to_class.{class_name} must contain two bounds")
        lower, upper = bounds
        if not isinstance(lower, int | float) or not isinstance(upper, int | float):
            raise ValueError(f"bacs_rules_json.score_to_class.{class_name} bounds must be numeric")
        if lower < 0 or upper > 100 or lower > upper:
            raise ValueError(
                f"bacs_rules_json.score_to_class.{class_name} bounds must be ordered within 0..100"
            )


def _validate_scoring_rules(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        raise ValueError("scoring_rules_json must be an object")
    if not data:
        return
    weights = data.get("weights")
    if not isinstance(weights, dict):
        raise ValueError("scoring_rules_json.weights must be an object")
    for key in ["energy", "bacs", "roi", "capex"]:
        value = weights.get(key)
        if not isinstance(value, int | float) or value < 0:
            raise ValueError(f"scoring_rules_json.weights.{key} must be a positive number or zero")
    thresholds = data.get("thresholds", {})
    if thresholds is not None and not isinstance(thresholds, dict):
        raise ValueError("scoring_rules_json.thresholds must be an object")


def _validate_co2_factors(data: dict[str, Any]) -> None:
    if not isinstance(data, dict) or not data:
        raise ValueError("co2_factors_json must be a non-empty object")
    for key, value in data.items():
        if not isinstance(key, str) or not key:
            raise ValueError("co2_factors_json keys must be non-empty strings")
        if not isinstance(value, int | float) or value < 0:
            raise ValueError(f"co2_factors_json.{key} must be a positive number or zero")


def _require_positive_number(field_name: str, value: Any) -> None:
    if not isinstance(value, int | float) or value <= 0:
        raise ValueError(f"{field_name} must be a positive number")
