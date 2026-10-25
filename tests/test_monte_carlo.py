import pytest

from cms_dimuon_robustness.monte_carlo import (
    approximate_trials_for_absolute_precision,
    clopper_pearson,
)


def test_point_estimate_and_interval_are_ordered():
    result = clopper_pearson(50, 1000)
    assert result.estimate == pytest.approx(0.05)
    assert 0 < result.lower < result.estimate < result.upper < 1
    assert result.confidence_level == pytest.approx(0.95)


def test_zero_successes_does_not_claim_zero_uncertainty():
    result = clopper_pearson(0, 1000)
    assert result.estimate == 0
    assert result.lower == 0
    assert result.upper > 0


def test_all_successes_interval():
    result = clopper_pearson(100, 100)
    assert result.estimate == 1
    assert result.upper == 1
    assert result.lower < 1


def test_invalid_inputs_raise():
    for args in [(-1, 10), (11, 10), (0, 0), (1.5, 10)]:
        with pytest.raises(ValueError):
            clopper_pearson(*args)
    with pytest.raises(ValueError):
        clopper_pearson(1, 10, 1.0)


def test_precision_planning_ordering():
    n_1pct = approximate_trials_for_absolute_precision(0.05, 0.01)
    n_halfpct = approximate_trials_for_absolute_precision(0.05, 0.005)
    assert n_halfpct > n_1pct
    assert n_1pct == 1825
