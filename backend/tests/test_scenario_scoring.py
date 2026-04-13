from app.scoring.scenario_scoring import ScenarioScoreInput, score_scenario


def test_score_scenario_returns_weighted_breakdown() -> None:
    result = score_scenario(
        ScenarioScoreInput(
            energy_savings_percent=30,
            scenario_bacs_class="B",
            roi_percent=50,
            payback_years=3,
            capex=0,
            annual_cost_savings=20000,
        )
    )

    assert result["version"] == "comparison-score-v1"
    assert result["score"] == 96.0
    assert result["sub_scores"] == {"energy": 100.0, "bacs": 80.0, "roi": 100.0, "capex": 100.0}
    assert result["contributions"] == {"energy": 35.0, "bacs": 16.0, "roi": 25.0, "capex": 20.0}
    assert result["dominant_contributors"] == ["energy", "roi"]


def test_score_scenario_uses_versioned_custom_rules() -> None:
    result = score_scenario(
        ScenarioScoreInput(
            energy_savings_percent=5,
            scenario_bacs_class="A",
            roi_percent=0,
            payback_years=None,
            capex=500000,
            annual_cost_savings=0,
        ),
        {
            "version": "custom-bacs-only",
            "weights": {"energy": 0, "bacs": 1, "roi": 0, "capex": 0},
        },
    )

    assert result["version"] == "custom-bacs-only"
    assert result["score"] == 100.0
    assert result["weights"] == {"energy": 0.0, "bacs": 1.0, "roi": 0.0, "capex": 0.0}
    assert result["dominant_contributors"] == ["bacs"]
