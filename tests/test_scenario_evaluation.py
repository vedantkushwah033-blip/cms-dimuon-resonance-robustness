import numpy as np
import pytest

import cms_dimuon_robustness.scenario_evaluation as module


def test_scenario_runner_returns_declared_scenarios_in_input_order(monkeypatch):
    calls = []

    def fake_evaluate(**kwargs):
        calls.append(kwargs)
        return {
            "false_positive_rate": 0.04,
            "rejections": 2,
            "n_evaluation": kwargs["n_evaluation"],
        }

    monkeypatch.setattr(module, "evaluate_refitted_background_false_positive_rate", fake_evaluate)
    result = module.evaluate_null_scenarios(
        scenario_means={"matched": [10.0] * 8, "shoulder": [10.0, 11.0] * 4},
        window_widths=[1, 2],
        n_calibration=20,
        n_evaluation=50,
        alpha=0.05,
        scenario_seeds={"matched": (10, 11), "shoulder": (12, 13)},
        background_order=1,
    )
    assert [row["scenario"] for row in result["results"]] == ["matched", "shoulder"]
    assert result["design"]["scenario_count"] == 2
    assert calls[0]["seed_calibration"] == 10
    assert calls[1]["seed_evaluation"] == 13
    assert all(row["interpretation"] if "interpretation" in row else True for row in result["results"])


@pytest.mark.parametrize(
    "means,seeds",
    [
        ({"a": [1.0]}, {"a": (1, 1)}),
        ({"a": [1.0]}, {"a": (1, 2), "extra": (3, 4)}),
        ({"a": [1.0]}, {"a": (1, 2), "b": (3, 4)}),
        ({"a": [1.0, float("nan")]}, {"a": (1, 2)}),
        ({"a": [0.0, 1.0]}, {"a": (1, 2)}),
        ({"a": []}, {"a": (1, 2)}),
        ({"a": [1.0]}, {"a": (1, 2), "b": (2, 3)}),
    ],
)
def test_scenario_runner_rejects_invalid_means_or_seed_design(means, seeds):
    with pytest.raises(ValueError):
        module.evaluate_null_scenarios(
            scenario_means=means,
            window_widths=[1],
            n_calibration=10,
            n_evaluation=10,
            alpha=0.05,
            scenario_seeds=seeds,
        )


def test_scenario_runner_requires_unique_seeds_across_roles():
    with pytest.raises(ValueError, match="unique"):
        module.evaluate_null_scenarios(
            scenario_means={"a": [2.0, 2.0], "b": [3.0, 3.0]},
            window_widths=[1],
            n_calibration=10,
            n_evaluation=10,
            alpha=0.05,
            scenario_seeds={"a": (1, 2), "b": (3, 2)},
        )
