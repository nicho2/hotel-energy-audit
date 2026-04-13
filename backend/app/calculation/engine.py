from __future__ import annotations

from copy import deepcopy
from math import isfinite
from typing import Any

from app.calculation.types import CalculationInput, CalculationOutput

ENGINE_VERSION = "simplified-annual-v1"
USAGES = ["heating", "cooling", "ventilation", "dhw", "lighting", "auxiliaries"]

DEFAULT_ASSUMPTIONS: dict[str, Any] = {
    "engine_version": ENGINE_VERSION,
    "heating_model_json": {
        "reference_intensity_kwh_m2": 85,
        "construction_factors": {"before_1975": 1.35, "1975_1990": 1.20, "1991_2005": 1.05, "2006_2012": 0.92, "after_2012": 0.82},
        "compacity_factors": {"very_compact": 0.90, "compact": 0.97, "medium": 1.00, "low": 1.08, "very_low": 1.18},
        "infiltration_factors": {"low": 0.92, "medium": 1.00, "high": 1.10, "very_high": 1.20},
        "orientation_factors": {"north": 1.08, "east": 1.02, "south": 0.94, "west": 1.00, "mixed": 1.00},
        "zone_factors": {"guest_rooms": 1.00, "circulation": 0.75, "lobby": 1.10, "restaurant": 1.05, "meeting": 0.95, "technical": 0.50, "spa": 1.15, "pool": 1.35, "other": 1.00},
        "system_factors": {"very_high": 0.80, "high": 0.90, "standard": 1.00, "low": 1.12, "very_low": 1.25},
    },
    "cooling_model_json": {
        "reference_intensity_kwh_m2": 18,
        "construction_factors": {"before_1975": 1.10, "1975_1990": 1.05, "1991_2005": 1.00, "2006_2012": 0.95, "after_2012": 0.90},
        "infiltration_factors": {"low": 0.98, "medium": 1.00, "high": 1.04, "very_high": 1.08},
        "orientation_factors": {"north": 0.88, "east": 1.00, "south": 1.18, "west": 1.12, "mixed": 1.00},
        "solar_factors": {"low": 0.90, "medium": 1.00, "high": 1.12, "very_high": 1.22},
        "zone_factors": {"guest_rooms": 1.00, "circulation": 0.60, "lobby": 1.20, "restaurant": 1.15, "meeting": 1.10, "technical": 0.40, "spa": 1.10, "pool": 0.70, "other": 1.00},
        "system_factors": {"very_high": 0.82, "high": 0.92, "standard": 1.00, "low": 1.10, "very_low": 1.22},
    },
    "ventilation_model_json": {
        "reference_intensity_kwh_m2": 12,
        "zone_factors": {"guest_rooms": 1.00, "circulation": 0.60, "lobby": 1.10, "restaurant": 1.30, "meeting": 1.20, "technical": 0.50, "spa": 1.25, "pool": 1.40, "other": 1.00},
        "schedule_factors": {"continuous": 1.15, "extended_day": 1.00, "optimized": 0.88, "demand_controlled": 0.75},
        "system_factors": {"very_high": 0.82, "high": 0.90, "standard": 1.00, "low": 1.12, "very_low": 1.25},
    },
    "dhw_model_json": {
        "reference_intensity_kwh_room": 2200,
        "service_factors": {"none": 1.00, "restaurant": 1.08, "spa": 1.18, "pool": 1.12, "restaurant_spa": 1.24, "restaurant_spa_pool": 1.32},
        "system_factors": {"very_high": 0.82, "high": 0.92, "standard": 1.00, "low": 1.10, "very_low": 1.20},
    },
    "lighting_model_json": {
        "reference_intensity_kwh_m2": 22,
        "zone_factors": {"guest_rooms": 1.00, "circulation": 0.80, "lobby": 1.25, "restaurant": 1.20, "meeting": 1.10, "technical": 0.70, "spa": 1.10, "pool": 0.90, "other": 1.00},
        "technology_factors": {"led_dimming": 0.65, "led": 0.78, "mixed": 0.92, "fluorescent": 1.00, "old": 1.20},
    },
    "auxiliaries_model_json": {"ratio_by_complexity": {"low": 0.05, "standard": 0.08, "high": 0.11, "very_high": 0.14}},
    "economic_defaults_json": {
        "discount_rate": 0.06,
        "energy_inflation_rate": 0.03,
        "analysis_period_years": 15,
        "maintenance_rate": 0.02,
        "maintenance_savings_rate": 0.0,
        "performance_degradation_rate": 0.005,
        "subsidy_rate": 0.0,
        "subsidies": 0.0,
        "energy_prices": {"electricity": 0.18, "gas": 0.09, "district_heating": 0.12},
    },
    "bacs_rules_json": {
        "score_to_class": {"A": [85, 100], "B": [65, 84], "C": [40, 64], "D": [0, 39]},
        "domain_weights": {"heating": 18, "cooling": 14, "ventilation": 12, "dhw": 10, "lighting": 12, "supervision": 12, "monitoring": 10, "room_automation": 12},
        "gain_caps": {"heating": 0.40, "cooling": 0.40, "ventilation": 0.45, "dhw": 0.25, "lighting": 0.60, "auxiliaries": 0.35},
    },
    "co2_factors_json": {"electricity": 0.055, "gas": 0.227, "natural_gas": 0.227, "district_heating": 0.120},
}


class CalculationEngine:
    def run(self, input_data: CalculationInput) -> CalculationOutput:
        assumptions = _merge_assumptions(input_data.assumptions)
        warnings = _initial_warnings(input_data)
        zones = _normalise_zones(input_data)
        systems = input_data.systems or []
        usage_payload = _dict(input_data.assumptions.get("usage_payload"))

        baseline_by_zone = _compute_zone_baseline(input_data, zones, systems, assumptions, usage_payload)
        _add_dhw_to_zones(input_data, baseline_by_zone, assumptions, systems, usage_payload)
        _add_auxiliaries_to_zones(baseline_by_zone, assumptions, systems)
        baseline_by_zone = _apply_factors_by_zone(baseline_by_zone, _bacs_baseline_factors(input_data.bacs_functions))
        baseline_by_zone = _freeze_zone_baselines(baseline_by_zone)

        baseline_totals = _sum_by_usage_from_key(baseline_by_zone, "baseline_uses")
        solution_impacts = _solution_impacts(input_data.selected_solutions)
        input_data.assumptions["applied_impacts"] = _impact_trace(solution_impacts)
        scenario_by_zone = _apply_solution_impacts(baseline_by_zone, solution_impacts, assumptions)
        scenario_totals = _sum_by_usage_from_key(scenario_by_zone, "uses")

        baseline_total = sum(baseline_totals.values())
        scenario_total = sum(scenario_totals.values())
        current_bacs_score = _compute_bacs_score(input_data.bacs_functions, assumptions)
        baseline_bacs_class = _class_from_score(current_bacs_score, assumptions)
        scenario_bacs_score = min(100.0, current_bacs_score + _scenario_bacs_score_gain(input_data.selected_solutions))
        scenario_bacs_class = _class_from_score(scenario_bacs_score, assumptions)
        capex = _total_capex(input_data.selected_solutions)
        economic = _economic_results(baseline_totals, scenario_totals, systems, assumptions, capex, input_data.selected_solutions)
        input_data.assumptions["economic_inputs"] = _economic_trace(assumptions["economic_defaults_json"], economic)

        return CalculationOutput(
            summary={
                "baseline_energy_kwh_year": round(baseline_total, 2),
                "scenario_energy_kwh_year": round(scenario_total, 2),
                "energy_savings_percent": _percent_savings(baseline_total, scenario_total),
                "baseline_bacs_class": baseline_bacs_class,
                "scenario_bacs_class": scenario_bacs_class,
            },
            by_use=[
                {
                    "usage_type": usage,
                    "baseline_energy_kwh_year": round(baseline_totals[usage], 2),
                    "scenario_energy_kwh_year": round(scenario_totals[usage], 2),
                    "energy_savings_percent": _percent_savings(baseline_totals[usage], scenario_totals[usage]),
                }
                for usage in USAGES
            ],
            by_zone=[_zone_output(row) for row in scenario_by_zone],
            economic=economic,
            bacs={"estimated_bacs_class": baseline_bacs_class, "scenario_bacs_class": scenario_bacs_class, "current_score": round(current_bacs_score, 1), "scenario_score": round(scenario_bacs_score, 1)},
            messages=_messages(baseline_totals, baseline_total, _percent_savings(baseline_total, scenario_total), economic["simple_payback_years"], baseline_bacs_class, scenario_bacs_class, zones, input_data.selected_solutions, solution_impacts),
            warnings=warnings,
        )


def _merge_assumptions(raw: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(DEFAULT_ASSUMPTIONS)
    raw = _dict(raw)
    for key, value in raw.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    merged["engine_version"] = raw.get("engine_version", ENGINE_VERSION)
    return merged


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    data = deepcopy(base)
    for key, value in override.items():
        if key in data and isinstance(data[key], dict) and isinstance(value, dict):
            data[key] = _deep_merge(data[key], value)
        else:
            data[key] = value
    return data


def _initial_warnings(input_data: CalculationInput) -> list[str]:
    warnings = []
    if not input_data.assumptions.get("assumption_set_id"):
        warnings.append("Aucun jeu d'hypotheses actif trouve: valeurs produit V1 par defaut appliquees.")
    if not input_data.zones:
        warnings.append("Aucune zone detaillee: une zone mixte equivalente a ete generee pour le calcul.")
    if not input_data.systems:
        warnings.append("Aucun systeme technique renseigne: performances standard appliquees.")
    if not _dict(input_data.assumptions.get("climate_zone")):
        warnings.append("Zone climatique absente du snapshot: indices climatiques neutres appliques.")
    return warnings


def _normalise_zones(input_data: CalculationInput) -> list[dict[str, Any]]:
    zones = [dict(zone) for zone in input_data.zones if _num(zone.get("area_m2")) > 0]
    if zones:
        return zones

    building = input_data.building or {}
    area = _num(building.get("gross_floor_area_m2")) or _num(building.get("heated_area_m2")) or 1.0
    return [{
        "id": None,
        "name": building.get("name") or "Zone mixte",
        "zone_type": "other",
        "orientation": building.get("main_orientation") or "mixed",
        "area_m2": area,
        "room_count": _num(building.get("number_of_rooms")),
    }]


def _compute_zone_baseline(
    input_data: CalculationInput,
    zones: list[dict[str, Any]],
    systems: list[dict[str, Any]],
    assumptions: dict[str, Any],
    usage_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    building = input_data.building or {}
    climate = _dict(assumptions.get("climate_zone"))
    heat_climate = _num(climate.get("heating_severity_index"), 1.0)
    cool_climate = _num(climate.get("cooling_severity_index"), 1.0)
    solar_index = _num(climate.get("solar_exposure_index"), 1.0)
    construction = _normalise_key(building.get("construction_period"), "1991_2005")
    compacity = _normalise_key(building.get("compactness_level"), "medium")
    occupancy = _bounded(_num(usage_payload.get("average_occupancy_rate"), 0.70), 0.0, 1.0)
    occ = 0.75 + 0.5 * occupancy
    total_zone_area = sum(_num(zone.get("area_m2")) for zone in zones) or 1.0
    heated_area = _num(building.get("heated_area_m2")) or total_zone_area
    cooled_area = _num(building.get("cooled_area_m2")) or total_zone_area * 0.70
    heat_area_factor = heated_area / total_zone_area
    cool_area_factor = min(cooled_area / total_zone_area, 1.0)

    heat_model = assumptions["heating_model_json"]
    cool_model = assumptions["cooling_model_json"]
    vent_model = assumptions["ventilation_model_json"]
    light_model = assumptions["lighting_model_json"]
    rows = []
    for zone in zones:
        area = _num(zone.get("area_m2"))
        zone_type = _normalise_key(zone.get("zone_type"), "other")
        orientation = _normalise_key(zone.get("orientation") or building.get("main_orientation"), "mixed")
        infiltration = _normalise_key(zone.get("infiltration_level"), "medium")
        solar = _solar_bucket(_normalise_key(zone.get("solar_exposure_level"), ""), solar_index)
        glazing_ratio = _bounded(_num(zone.get("window_ratio"), 0.25), 0.05, 0.80)
        heating = (
            area * heat_area_factor * _num(heat_model.get("reference_intensity_kwh_m2"), 85)
            * heat_climate * _factor(heat_model, "construction_factors", construction)
            * _factor(heat_model, "compacity_factors", compacity)
            * _factor(heat_model, "infiltration_factors", infiltration)
            * _setpoint_factor(zone.get("heating_setpoint_c"), reference=21, slope=0.05, mode="heating")
            * _factor(heat_model, "orientation_factors", orientation)
            * _factor(heat_model, "zone_factors", zone_type)
            * _system_factor(systems, "heating", heat_model)
        )
        cooling = (
            area * cool_area_factor * _num(cool_model.get("reference_intensity_kwh_m2"), 18)
            * cool_climate * _factor(cool_model, "construction_factors", construction)
            * _factor(cool_model, "infiltration_factors", infiltration)
            * _factor(cool_model, "orientation_factors", orientation)
            * _factor(cool_model, "solar_factors", solar)
            * (1 + 0.8 * (glazing_ratio - 0.25))
            * _setpoint_factor(zone.get("cooling_setpoint_c"), reference=24, slope=0.06, mode="cooling")
            * _factor(cool_model, "zone_factors", zone_type)
            * occ * _system_factor(systems, "cooling", cool_model)
        )
        ventilation = (
            area * _num(vent_model.get("reference_intensity_kwh_m2"), 12)
            * _factor(vent_model, "zone_factors", zone_type)
            * occ * _ventilation_schedule_factor(systems, vent_model)
            * _system_factor(systems, "ventilation", vent_model)
        )
        lighting = (
            area * _num(light_model.get("reference_intensity_kwh_m2"), 22)
            * _factor(light_model, "zone_factors", zone_type)
            * _lighting_technology_factor(systems, light_model)
        )
        rows.append({
            "zone_id": zone.get("id"),
            "zone_name": zone.get("name", "Unnamed zone"),
            "zone_type": zone_type,
            "orientation": orientation,
            "room_count": _num(zone.get("room_count")),
            "area_m2": area,
            "uses": {
                "heating": max(0.0, heating),
                "cooling": max(0.0, cooling),
                "ventilation": max(0.0, ventilation),
                "dhw": 0.0,
                "lighting": max(0.0, lighting),
                "auxiliaries": 0.0,
            },
        })
    return rows


def _add_dhw_to_zones(
    input_data: CalculationInput,
    zone_rows: list[dict[str, Any]],
    assumptions: dict[str, Any],
    systems: list[dict[str, Any]],
    usage_payload: dict[str, Any],
) -> None:
    building = input_data.building or {}
    rooms = _num(building.get("number_of_rooms")) or sum(_num(row.get("room_count")) for row in zone_rows)
    rooms = rooms if rooms > 0 else 1.0
    occupancy = _bounded(_num(usage_payload.get("average_occupancy_rate"), 0.70), 0.0, 1.0)
    model = assumptions["dhw_model_json"]
    dhw_total = (
        rooms * _num(model.get("reference_intensity_kwh_room"), 2200)
        * (0.50 + occupancy) * _factor(model, "service_factors", _dhw_services_key(building))
        * _system_factor(systems, "dhw", model)
    )
    guest_total = sum(_zone_weight(row, prefer_rooms=True) for row in zone_rows if row["zone_type"] == "guest_rooms")
    all_total = sum(_zone_weight(row, prefer_rooms=True) for row in zone_rows) or 1.0
    for row in zone_rows:
        if guest_total:
            row["uses"]["dhw"] = dhw_total * (_zone_weight(row, prefer_rooms=True) if row["zone_type"] == "guest_rooms" else 0.0) / guest_total
        else:
            row["uses"]["dhw"] = dhw_total * _zone_weight(row, prefer_rooms=True) / all_total


def _add_auxiliaries_to_zones(zone_rows: list[dict[str, Any]], assumptions: dict[str, Any], systems: list[dict[str, Any]]) -> None:
    ratio = _aux_ratio(assumptions, systems)
    for row in zone_rows:
        row["uses"]["auxiliaries"] = (row["uses"]["heating"] + row["uses"]["cooling"] + row["uses"]["ventilation"]) * ratio


def _freeze_zone_baselines(zone_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    frozen = deepcopy(zone_rows)
    for row in frozen:
        row["baseline_uses"] = dict(row["uses"])
        row["baseline_total"] = sum(_num(value) for value in row["baseline_uses"].values())
    return frozen


def _apply_factors_by_zone(zone_rows: list[dict[str, Any]], factors: dict[str, float]) -> list[dict[str, Any]]:
    updated = deepcopy(zone_rows)
    for row in updated:
        for usage, factor in factors.items():
            row["uses"][usage] *= factor
    return updated


def _sum_by_usage_from_key(zone_rows: list[dict[str, Any]], key: str) -> dict[str, float]:
    return {usage: sum(_num(row[key].get(usage)) for row in zone_rows) for usage in USAGES}


def _bacs_baseline_factors(functions: list[dict[str, Any]]) -> dict[str, float]:
    gains = {usage: [] for usage in USAGES}
    for item in functions:
        code = str(item.get("code", "")).lower()
        domain = str(item.get("domain", "")).lower()
        if "window" in code or "fenetre" in code:
            gains["heating"].append(0.03)
            gains["cooling"].append(0.03)
        if "night" in code or "abaissement" in code:
            gains["heating"].append(0.02)
            gains["cooling"].append(0.02)
        if "presence" in code or "occup" in code or "absence" in code:
            gains["heating"].append(0.03)
            gains["cooling"].append(0.04)
            gains["lighting"].append(0.05)
        if "schedule" in code or "horaire" in code or domain == "ventilation":
            gains["ventilation"].append(0.04)
        if domain in {"dhw", "ecs"}:
            gains["dhw"].append(0.03)
        if domain == "lighting":
            gains["lighting"].append(0.06)
        if domain in {"supervision", "monitoring"}:
            for usage in USAGES:
                gains[usage].append(0.015)
    return {usage: _residual_factor(values) for usage, values in gains.items()}


def _solution_impacts(selected_solutions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    impacts = []
    for solution in selected_solutions:
        if solution.get("is_selected") is False:
            continue
        code = str(solution.get("solution_code") or solution.get("code") or "").upper()
        family = str(solution.get("family") or solution.get("solution_family") or "").lower()
        gains = _dict(solution.get("gain_model"))
        if not gains:
            gains = _dict(_dict(solution.get("bacs_impact_json")).get("gain_model")).get("default", {})
        if not isinstance(gains, dict) or not gains:
            gains = _inferred_solution_gains(code, family, _num(solution.get("gain_override_percent"), 0.0))
        if solution.get("gain_override_percent") is not None:
            override = _bounded(_num(solution.get("gain_override_percent")), 0.0, 0.9)
            gains = {usage: override for usage in _default_solution_uses(code, family)}
        if solution.get("target_scope") == "system" and solution.get("target_system_type"):
            allowed_uses = _uses_for_system_type(str(solution["target_system_type"]))
            gains = {usage: value for usage, value in gains.items() if usage in allowed_uses}
        impacts.append({
            "code": code,
            "target_scope": solution.get("target_scope", "project"),
            "target_zone_id": solution.get("target_zone_id"),
            "target_system_id": solution.get("target_system_id"),
            "target_system_type": solution.get("target_system_type"),
            "gains": {usage: _bounded(_num(value), 0.0, 0.9) for usage, value in gains.items() if usage in USAGES},
        })
    return impacts


def _impact_trace(impacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "solution_code": impact["code"],
            "target_scope": impact["target_scope"],
            "target_zone_id": impact.get("target_zone_id"),
            "target_system_id": impact.get("target_system_id"),
            "target_system_type": impact.get("target_system_type"),
            "gains": {usage: round(gain, 4) for usage, gain in impact["gains"].items()},
            "application_order": index + 1,
        }
        for index, impact in enumerate(impacts)
    ]


def _uses_for_system_type(system_type: str) -> set[str]:
    system_type = system_type.lower()
    mapping = {
        "heating": {"heating"},
        "cooling": {"cooling"},
        "ventilation": {"ventilation", "auxiliaries"},
        "dhw": {"dhw"},
        "lighting": {"lighting"},
    }
    return mapping.get(system_type, set(USAGES))


def _apply_solution_impacts(zone_rows: list[dict[str, Any]], impacts: list[dict[str, Any]], assumptions: dict[str, Any]) -> list[dict[str, Any]]:
    updated = deepcopy(zone_rows)
    caps = _dict(assumptions["bacs_rules_json"].get("gain_caps"))
    for impact in impacts:
        for row in updated:
            if impact["target_scope"] == "zone" and str(row.get("zone_id")) != str(impact.get("target_zone_id")):
                continue
            for usage, gain in impact["gains"].items():
                baseline_usage = row["baseline_uses"].get(usage, 0.0)
                cap = _num(caps.get(usage), 0.5)
                row["uses"][usage] = max(baseline_usage * (1 - cap), row["uses"].get(usage, 0.0) * (1 - gain))
    return updated


def _inferred_solution_gains(code: str, family: str, override: float = 0.0) -> dict[str, float]:
    if override > 0:
        return {usage: override for usage in USAGES}
    if "ROOM" in code or "CHAMBER" in code:
        return {"heating": 0.08, "cooling": 0.10, "lighting": 0.12}
    if "LED" in code or family == "lighting":
        return {"lighting": 0.28}
    if "CO2" in code or "VENT" in code or family == "ventilation":
        return {"ventilation": 0.12, "auxiliaries": 0.05}
    if "DHW" in code or "ECS" in code or family == "dhw":
        return {"dhw": 0.06}
    if "PAC" in code or "HVAC" in code or family == "hvac":
        return {"heating": 0.12, "cooling": 0.08}
    if "INSULATION" in code or "ENVELOPE" in code or family == "envelope":
        return {"heating": 0.15, "cooling": 0.04}
    if "BACS" in code or "GTB" in code or "SUPERVISION" in code or family == "bacs":
        return {"heating": 0.06, "cooling": 0.06, "ventilation": 0.06, "dhw": 0.03, "lighting": 0.05}
    return {"heating": 0.03, "cooling": 0.03, "ventilation": 0.03, "lighting": 0.03}


def _default_solution_uses(code: str, family: str) -> list[str]:
    return list(_inferred_solution_gains(code, family).keys())


def _total_capex(selected_solutions: list[dict[str, Any]]) -> float:
    total = 0.0
    for solution in selected_solutions:
        if solution.get("is_selected") is False:
            continue
        capex = _num(solution.get("capex_override")) or _num(solution.get("default_capex"))
        if capex <= 0:
            capex = _num(solution.get("quantity"), 1.0) * _num(solution.get("default_unit_cost"))
        if capex <= 0:
            capex = _fallback_capex(str(solution.get("solution_code") or ""), str(solution.get("family") or ""))
        total += capex
    return round(total, 2)


def _fallback_capex(code: str, family: str) -> float:
    code = code.upper()
    family = family.lower()
    if "ROOM" in code:
        return 18000
    if "LED" in code or family == "lighting":
        return 12000
    if family == "hvac":
        return 45000
    if family in {"dhw", "ventilation"}:
        return 15000
    return 10000


def _economic_results(
    baseline_totals: dict[str, float],
    scenario_totals: dict[str, float],
    systems: list[dict[str, Any]],
    assumptions: dict[str, Any],
    capex: float,
    selected_solutions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    economic = assumptions["economic_defaults_json"]
    baseline_energy_cost = _energy_cost(baseline_totals, systems, assumptions)
    scenario_energy_cost = _energy_cost(scenario_totals, systems, assumptions)
    energy_cost_savings = baseline_energy_cost - scenario_energy_cost
    maintenance_cost = _annual_maintenance_cost(selected_solutions or [], capex, economic)
    maintenance_savings = capex * _bounded(_num(economic.get("maintenance_savings_rate"), 0.0), 0.0, 1.0)
    baseline_opex = baseline_energy_cost
    scenario_opex = scenario_energy_cost + maintenance_cost - maintenance_savings
    net_annual_savings = baseline_opex - scenario_opex
    subsidies = _subsidies(capex, economic)
    net_capex = max(0.0, capex - subsidies)
    period = max(1, int(_num(economic.get("analysis_period_years"), 15)))
    discount_rate = _num(economic.get("discount_rate"), 0.06)
    inflation = _num(economic.get("energy_inflation_rate"), 0.03)
    degradation = _bounded(_num(economic.get("performance_degradation_rate"), 0.005), 0.0, 0.50)
    payback = _simple_payback(net_capex, net_annual_savings)
    npv = -net_capex
    cash_flow_values = [-net_capex]
    cumulative = -net_capex
    cash_flows = [{
        "year": 0,
        "energy_cost_savings": 0.0,
        "maintenance_savings": 0.0,
        "maintenance_cost": 0.0,
        "net_cash_flow": round(-net_capex, 2),
        "discounted_cash_flow": round(-net_capex, 2),
        "cumulative_cash_flow": round(cumulative, 2),
    }]
    for year in range(1, period + 1):
        effective_energy_savings = energy_cost_savings * ((1 + inflation) ** (year - 1)) * ((1 - degradation) ** (year - 1))
        cash_flow = effective_energy_savings + maintenance_savings - maintenance_cost
        discounted = cash_flow / ((1 + discount_rate) ** year)
        cash_flow_values.append(cash_flow)
        npv += discounted
        cumulative += cash_flow
        cash_flows.append({
            "year": year,
            "energy_cost_savings": round(effective_energy_savings, 2),
            "maintenance_savings": round(maintenance_savings, 2),
            "maintenance_cost": round(maintenance_cost, 2),
            "net_cash_flow": round(cash_flow, 2),
            "discounted_cash_flow": round(discounted, 2),
            "cumulative_cash_flow": round(cumulative, 2),
        })
    irr = _irr(cash_flow_values)
    return {
        "total_capex": round(capex, 2),
        "subsidies": round(subsidies, 2),
        "net_capex": round(net_capex, 2),
        "baseline_opex_year": round(baseline_opex, 2),
        "scenario_opex_year": round(scenario_opex, 2),
        "energy_cost_savings": round(energy_cost_savings, 2),
        "maintenance_cost_year": round(maintenance_cost, 2),
        "maintenance_savings_year": round(maintenance_savings, 2),
        "net_annual_savings": round(net_annual_savings, 2),
        "annual_cost_savings": round(net_annual_savings, 2),
        "simple_payback_years": round(payback, 1) if payback is not None else None,
        "npv": round(npv, 2),
        "irr": _rounded_optional(irr, 4),
        "analysis_period_years": period,
        "discount_rate": round(discount_rate, 4),
        "energy_inflation_rate": round(inflation, 4),
        "cash_flows": cash_flows,
        "is_roi_calculable": payback is not None or irr is not None,
    }


def _annual_maintenance_cost(selected_solutions: list[dict[str, Any]], capex: float, economic: dict[str, Any]) -> float:
    overrides = [
        _num(solution.get("maintenance_override"))
        for solution in selected_solutions
        if solution.get("is_selected") is not False and solution.get("maintenance_override") is not None
    ]
    if overrides:
        return max(0.0, sum(overrides))
    return max(0.0, capex * _num(economic.get("maintenance_rate"), 0.02))


def _subsidies(capex: float, economic: dict[str, Any]) -> float:
    fixed = max(0.0, _num(economic.get("subsidies"), 0.0))
    rated = capex * _bounded(_num(economic.get("subsidy_rate"), 0.0), 0.0, 1.0)
    return min(capex, fixed + rated)


def _simple_payback(net_capex: float, annual_savings: float) -> float | None:
    if net_capex <= 0 and annual_savings > 0:
        return 0.0
    if net_capex > 0 and annual_savings > 0:
        return net_capex / annual_savings
    return None


def _economic_trace(economic: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    return {
        "discount_rate": result["discount_rate"],
        "energy_inflation_rate": result["energy_inflation_rate"],
        "analysis_period_years": result["analysis_period_years"],
        "maintenance_rate": _num(economic.get("maintenance_rate"), 0.02),
        "maintenance_savings_rate": _num(economic.get("maintenance_savings_rate"), 0.0),
        "performance_degradation_rate": _num(economic.get("performance_degradation_rate"), 0.005),
        "subsidy_rate": _num(economic.get("subsidy_rate"), 0.0),
        "subsidies": result["subsidies"],
        "energy_prices": _dict(economic.get("energy_prices")),
    }


def _energy_cost(totals: dict[str, float], systems: list[dict[str, Any]], assumptions: dict[str, Any]) -> float:
    prices = _dict(assumptions["economic_defaults_json"].get("energy_prices"))
    return sum(totals[usage] * _num(prices.get(_energy_source_for_usage(usage, systems)), 0.16) for usage in USAGES)


def _energy_source_for_usage(usage: str, systems: list[dict[str, Any]]) -> str:
    system_type = "dhw" if usage == "dhw" else usage
    for system in systems:
        if str(system.get("system_type")) == system_type and system.get("energy_source"):
            return _normalise_energy_source(str(system["energy_source"]))
    return "electricity" if usage in {"cooling", "ventilation", "lighting", "auxiliaries"} else "gas"


def _normalise_energy_source(value: str) -> str:
    value = value.lower()
    if value in {"natural_gas", "gas_boiler", "gaz"}:
        return "gas"
    if value in {"district", "district_heating"}:
        return "district_heating"
    return value


def _irr(cash_flows: list[float]) -> float | None:
    if not cash_flows or not any(value < 0 for value in cash_flows) or not any(value > 0 for value in cash_flows):
        return None
    low, high = -0.95, 1.0
    low_value = sum(cash_flow / ((1 + low) ** index) for index, cash_flow in enumerate(cash_flows))
    high_value = sum(cash_flow / ((1 + high) ** index) for index, cash_flow in enumerate(cash_flows))
    if low_value == 0:
        return low
    if high_value == 0:
        return high
    if (low_value > 0) == (high_value > 0):
        return None
    for _ in range(80):
        mid = (low + high) / 2
        value = sum(cash_flow / ((1 + mid) ** index) for index, cash_flow in enumerate(cash_flows))
        if value > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def _rounded_optional(value: float | None, digits: int) -> float | None:
    return round(value, digits) if value is not None else None


def _compute_bacs_score(functions: list[dict[str, Any]], assumptions: dict[str, Any]) -> float:
    if not functions:
        return 35.0
    domain_weights = _dict(assumptions["bacs_rules_json"].get("domain_weights"))
    scores = {domain: 20.0 for domain in domain_weights}
    for item in functions:
        domain = str(item.get("domain") or "supervision").lower()
        if domain == "ecs":
            domain = "dhw"
        if domain in scores:
            scores[domain] = min(100.0, scores[domain] + _num(item.get("weight"), 15.0))
    weight_total = sum(_num(value) for value in domain_weights.values()) or 1.0
    return sum(scores[domain] * _num(weight) for domain, weight in domain_weights.items()) / weight_total


def _scenario_bacs_score_gain(selected_solutions: list[dict[str, Any]]) -> float:
    gain = 0.0
    for solution in selected_solutions:
        if solution.get("is_selected") is False:
            continue
        code = str(solution.get("solution_code") or "").upper()
        family = str(solution.get("family") or solution.get("solution_family") or "").lower()
        if family == "bacs" or "BACS" in code or "ROOM" in code or "GTB" in code:
            gain += 12.0
    return min(gain, 35.0)


def _class_from_score(score: float, assumptions: dict[str, Any]) -> str:
    score_to_class = _dict(assumptions["bacs_rules_json"].get("score_to_class"))
    for class_name in ["A", "B", "C", "D"]:
        lower, upper = score_to_class.get(class_name, [0, 100])
        if _num(lower) <= score <= _num(upper):
            return class_name
    return "D"


def _messages(
    baseline_totals: dict[str, float],
    baseline_total: float,
    energy_savings_percent: float,
    payback: float,
    baseline_bacs_class: str,
    scenario_bacs_class: str,
    zones: list[dict[str, Any]],
    selected_solutions: list[dict[str, Any]],
    solution_impacts: list[dict[str, Any]],
) -> list[str]:
    messages = []
    if baseline_total > 0:
        dominant_usage, dominant_value = max(baseline_totals.items(), key=lambda item: item[1])
        if dominant_value / baseline_total > 0.30:
            messages.append(f"Le poste {dominant_usage} constitue le principal poste de consommation estime.")
        if baseline_totals["dhw"] / baseline_total > 0.25:
            messages.append("L'ECS represente un levier important pour ce batiment d'hebergement.")
    exposed_area = sum(_num(zone.get("area_m2")) for zone in zones if zone.get("zone_type") == "guest_rooms" and zone.get("orientation") in {"south", "west"})
    total_area = sum(_num(zone.get("area_m2")) for zone in zones) or 1.0
    if exposed_area / total_area > 0.20:
        messages.append("Les chambres sud/ouest concentrent un potentiel eleve d'optimisation estivale.")
    if selected_solutions:
        messages.append(f"Le bouquet selectionne genere un gain energetique estime de {energy_savings_percent:.1f} %.")
    if solution_impacts:
        applied = ", ".join(
            f"{impact['code']} ({'/'.join(sorted(impact['gains']))})"
            for impact in solution_impacts
            if impact["gains"]
        )
        if applied:
            messages.append(f"Impacts appliques dans l'ordre: {applied}.")
    if baseline_bacs_class != scenario_bacs_class:
        messages.append(f"Le scenario ameliore la classe BACS estimee de {baseline_bacs_class} vers {scenario_bacs_class}.")
    if payback:
        messages.append(f"Le temps de retour simple du bouquet est estime a {payback:.1f} ans.")
    if not messages:
        messages.append("Le calcul annuel simplifie est consolide avec les hypotheses V1 disponibles.")
    return messages


def _zone_output(row: dict[str, Any]) -> dict[str, Any]:
    baseline = _num(row.get("baseline_total"), sum(row["baseline_uses"].values()))
    scenario = sum(_num(value) for value in row["uses"].values())
    return {
        "zone_id": row.get("zone_id"),
        "zone_name": row.get("zone_name", "Unnamed zone"),
        "zone_type": row.get("zone_type", "other"),
        "orientation": row.get("orientation", "mixed"),
        "baseline_energy_kwh_year": round(baseline, 2),
        "scenario_energy_kwh_year": round(scenario, 2),
        "energy_savings_percent": _percent_savings(baseline, scenario),
    }


def _factor(model: dict[str, Any], family: str, key: str, default: float = 1.0) -> float:
    return _num(_dict(model.get(family)).get(key), default)


def _system_factor(systems: list[dict[str, Any]], system_type: str, model: dict[str, Any]) -> float:
    system = _primary_system(systems, system_type)
    if system is None:
        return 1.0
    level = _normalise_efficiency(system.get("efficiency_level") or system.get("technology_type"))
    return _factor(model, "system_factors", level)


def _primary_system(systems: list[dict[str, Any]], system_type: str) -> dict[str, Any] | None:
    candidates = [system for system in systems if str(system.get("system_type")) == system_type]
    if not candidates:
        return None
    primary = [system for system in candidates if system.get("is_primary")]
    return (primary or candidates)[0]


def _normalise_efficiency(value: Any) -> str:
    value = _normalise_key(value, "standard")
    mapping = {
        "very_performant": "very_high",
        "high_performance": "high",
        "performant": "high",
        "efficient": "high",
        "basic": "low",
        "poor": "low",
        "old": "very_low",
    }
    return mapping.get(value, value)


def _ventilation_schedule_factor(systems: list[dict[str, Any]], model: dict[str, Any]) -> float:
    system = _primary_system(systems, "ventilation")
    if system is None:
        return 1.0
    notes = f"{system.get('technology_type') or ''} {system.get('notes') or ''}".lower()
    if "co2" in notes or "presence" in notes:
        key = "demand_controlled"
    elif "schedule" in notes or "horaire" in notes:
        key = "optimized"
    elif "continuous" in notes or "continu" in notes:
        key = "continuous"
    else:
        key = "extended_day"
    return _factor(model, "schedule_factors", key)


def _lighting_technology_factor(systems: list[dict[str, Any]], model: dict[str, Any]) -> float:
    system = _primary_system(systems, "lighting")
    if system is None:
        return 1.0
    tech = _normalise_key(system.get("technology_type") or system.get("efficiency_level"), "fluorescent")
    if "dimming" in tech or "gradation" in tech:
        tech = "led_dimming"
    elif "led" in tech:
        tech = "led"
    elif "old" in tech or "halogen" in tech:
        tech = "old"
    elif "mixed" in tech:
        tech = "mixed"
    return _factor(model, "technology_factors", tech)


def _aux_ratio(assumptions: dict[str, Any], systems: list[dict[str, Any]]) -> float:
    count = len(systems)
    if count <= 2:
        complexity = "low"
    elif count <= 4:
        complexity = "standard"
    elif count <= 6:
        complexity = "high"
    else:
        complexity = "very_high"
    return _factor(assumptions["auxiliaries_model_json"], "ratio_by_complexity", complexity, 0.08)


def _dhw_services_key(building: dict[str, Any]) -> str:
    has_restaurant = bool(building.get("has_restaurant"))
    has_spa = bool(building.get("has_spa"))
    has_pool = bool(building.get("has_pool"))
    if has_restaurant and has_spa and has_pool:
        return "restaurant_spa_pool"
    if has_restaurant and has_spa:
        return "restaurant_spa"
    if has_restaurant:
        return "restaurant"
    if has_spa:
        return "spa"
    if has_pool:
        return "pool"
    return "none"


def _setpoint_factor(value: Any, *, reference: float, slope: float, mode: str) -> float:
    if value is None:
        return 1.0
    if mode == "cooling":
        return max(0.6, 1 - slope * (_num(value) - reference))
    return max(0.6, 1 + slope * (_num(value) - reference))


def _solar_bucket(value: str, index: float) -> str:
    if value:
        return value
    if index >= 1.18:
        return "very_high"
    if index >= 1.08:
        return "high"
    if index <= 0.92:
        return "low"
    return "medium"


def _zone_weight(row: dict[str, Any], *, prefer_rooms: bool) -> float:
    if prefer_rooms and _num(row.get("room_count")) > 0:
        return _num(row.get("room_count"))
    return max(1.0, _num(row.get("area_m2")))


def _percent_savings(baseline: float, scenario: float) -> float:
    if baseline <= 0:
        return 0.0
    return round(max(0.0, (baseline - scenario) / baseline * 100), 1)


def _residual_factor(gains: list[float]) -> float:
    factor = 1.0
    for index, gain in enumerate(gains):
        adjusted = gain * (0.75 if index > 0 else 1.0)
        factor *= 1 - _bounded(adjusted, 0.0, 0.9)
    return factor


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _num(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if isfinite(number) else default


def _bounded(value: float, low: float, high: float) -> float:
    return min(high, max(low, value))


def _normalise_key(value: Any, default: str) -> str:
    if value is None:
        return default
    return str(value).strip().lower().replace("-", "_").replace(" ", "_") or default
