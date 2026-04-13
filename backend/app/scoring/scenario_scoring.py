from __future__ import annotations

from dataclasses import dataclass
from typing import Any


DEFAULT_SCORING_RULES: dict[str, Any] = {
    "version": "comparison-score-v1",
    "weights": {"energy": 0.35, "bacs": 0.20, "roi": 0.25, "capex": 0.20},
    "thresholds": {
        "energy_savings_percent_full_score": 30.0,
        "roi_percent_full_score": 50.0,
        "payback_years_full_score": 3.0,
        "payback_years_zero_score": 12.0,
        "capex_reference": 100000.0,
    },
    "bacs_class_points": {"A": 100.0, "B": 80.0, "C": 60.0, "D": 40.0, "E": 20.0, "F": 0.0},
}


@dataclass(frozen=True)
class ScenarioScoreInput:
    energy_savings_percent: float
    scenario_bacs_class: str | None
    roi_percent: float
    payback_years: float | None
    capex: float
    annual_cost_savings: float


def score_scenario(input_data: ScenarioScoreInput, rules: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _merge_rules(rules)
    weights = _normalised_weights(resolved["weights"])
    thresholds = resolved["thresholds"]
    bacs_class_points = resolved["bacs_class_points"]

    sub_scores = {
        "energy": _bounded(
            input_data.energy_savings_percent / _num(thresholds["energy_savings_percent_full_score"], 30.0) * 100.0,
            0.0,
            100.0,
        ),
        "bacs": _bounded(_num(bacs_class_points.get(input_data.scenario_bacs_class or ""), 0.0), 0.0, 100.0),
        "roi": _roi_sub_score(input_data.roi_percent, input_data.payback_years, thresholds),
        "capex": _capex_sub_score(input_data.capex, thresholds),
    }
    contributions = {
        key: round(sub_scores[key] * weights[key], 2)
        for key in weights
    }
    score = round(sum(contributions.values()), 1)
    return {
        "score": score,
        "version": str(resolved["version"]),
        "weights": weights,
        "sub_scores": {key: round(value, 2) for key, value in sub_scores.items()},
        "contributions": contributions,
        "dominant_contributors": _dominant_contributors(contributions),
    }


def _merge_rules(rules: dict[str, Any] | None) -> dict[str, Any]:
    data = dict(DEFAULT_SCORING_RULES)
    incoming = rules if isinstance(rules, dict) else {}
    data["version"] = incoming.get("version") or data["version"]
    data["weights"] = {**data["weights"], **_dict(incoming.get("weights"))}
    data["thresholds"] = {**data["thresholds"], **_dict(incoming.get("thresholds"))}
    data["bacs_class_points"] = {**data["bacs_class_points"], **_dict(incoming.get("bacs_class_points"))}
    return data


def _normalised_weights(weights: dict[str, Any]) -> dict[str, float]:
    cleaned = {key: max(0.0, _num(weights.get(key), 0.0)) for key in ["energy", "bacs", "roi", "capex"]}
    total = sum(cleaned.values())
    if total <= 0:
        return dict(DEFAULT_SCORING_RULES["weights"])
    return {key: round(value / total, 4) for key, value in cleaned.items()}


def _roi_sub_score(roi_percent: float, payback_years: float | None, thresholds: dict[str, Any]) -> float:
    roi_points = _bounded(roi_percent / _num(thresholds["roi_percent_full_score"], 50.0) * 100.0, 0.0, 100.0)
    if payback_years is None:
        return roi_points * 0.5
    full_score = _num(thresholds["payback_years_full_score"], 3.0)
    zero_score = max(full_score, _num(thresholds["payback_years_zero_score"], 12.0))
    if payback_years <= full_score:
        payback_points = 100.0
    elif payback_years >= zero_score:
        payback_points = 0.0
    else:
        payback_points = (zero_score - payback_years) / (zero_score - full_score) * 100.0
    return _bounded((roi_points + payback_points) / 2.0, 0.0, 100.0)


def _capex_sub_score(capex: float, thresholds: dict[str, Any]) -> float:
    reference = max(1.0, _num(thresholds["capex_reference"], 100000.0))
    return _bounded(100.0 - (capex / reference * 100.0), 0.0, 100.0)


def _dominant_contributors(contributions: dict[str, float]) -> list[str]:
    return [
        key
        for key, value in sorted(contributions.items(), key=lambda item: item[1], reverse=True)
        if value > 0
    ][:2]


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _num(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _bounded(value: float, low: float, high: float) -> float:
    return min(high, max(low, value))
