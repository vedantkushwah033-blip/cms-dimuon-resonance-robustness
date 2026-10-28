import numpy as np
import pytest

from cms_dimuon_robustness.calibration import empirical_upper_tail_pvalue


def test_plus_one_rank_pvalue():
    result = empirical_upper_tail_pvalue(5.0, [1, 2, 3, 4])
    assert result["empirical_pvalue"] == 0.2
    assert result["minimum_resolvable_pvalue"] == 0.2
    assert result["exceedances_or_ties"] == 0
    assert result["n_calibration"] == 4


def test_calibration_counts_ties_in_upper_tail():
    result = empirical_upper_tail_pvalue(3.0, [2, 3, 3, 4])
    assert result["exceedances_or_ties"] == 3
    assert result["empirical_pvalue"] == 0.8


@pytest.mark.parametrize(
    "observed,null",
    [
        (float("nan"), [1.0]),
        (1.0, []),
        (1.0, [[1.0, 2.0]]),
        (1.0, [1.0, float("inf")]),
    ],
)
def test_calibration_rejects_invalid_inputs(observed, null):
    with pytest.raises(ValueError):
        empirical_upper_tail_pvalue(observed, null)


def test_fixed_background_null_simulation_is_reproducible_and_runs_full_scan():
    from cms_dimuon_robustness.calibration import simulate_fixed_background_null

    first = simulate_fixed_background_null([4.0, 5.0, 4.0], [1, 2], 25, seed=71)
    second = simulate_fixed_background_null([4.0, 5.0, 4.0], [1, 2], 25, seed=71)
    assert first == second
    assert first["n_experiments"] == 25
    assert len(first["null_statistics"]) == 25
    assert all(value >= 0 for value in first["null_statistics"])


def test_fixed_background_null_simulation_rejects_invalid_experiment_count():
    import pytest

    from cms_dimuon_robustness.calibration import simulate_fixed_background_null

    with pytest.raises(ValueError):
        simulate_fixed_background_null([4.0, 5.0], [1], 0, seed=71)


@pytest.mark.parametrize(
    "expected,widths,n_experiments,seed",
    [
        ([], [1], 2, 1),
        ([1.0, float("nan")], [1], 2, 1),
        ([1.0, 0.0], [1], 2, 1),
        ([1.0, 2.0], [], 2, 1),
        ([1.0, 2.0], [3], 2, 1),
        ([1.0, 2.0], [1], 2, -1),
        ([1.0, 2.0], [1], True, 1),
    ],
)
def test_fixed_background_null_simulation_rejects_invalid_configuration(
    expected, widths, n_experiments, seed
):
    from cms_dimuon_robustness.calibration import simulate_fixed_background_null

    with pytest.raises(ValueError):
        simulate_fixed_background_null(expected, widths, n_experiments, seed)



def test_wilson_interval_is_non_degenerate_at_zero_rejections():
    from cms_dimuon_robustness.calibration import wilson_interval

    interval = wilson_interval(0, 100)
    assert interval["lower"] == 0.0
    assert 0.0 < interval["upper"] < 0.1


def test_wilson_interval_validates_counts():
    from cms_dimuon_robustness.calibration import wilson_interval

    with pytest.raises(ValueError):
        wilson_interval(11, 10)
    with pytest.raises(ValueError):
        wilson_interval(0, 0)


def test_held_out_false_positive_evaluation_is_reproducible_and_reports_resolution():
    from cms_dimuon_robustness.calibration import evaluate_fixed_background_false_positive_rate

    kwargs = dict(
        expected_background=[4.0, 5.0, 4.0],
        window_widths=[1, 2],
        n_calibration=99,
        n_evaluation=120,
        alpha=0.05,
        seed_calibration=101,
        seed_evaluation=202,
    )
    first = evaluate_fixed_background_false_positive_rate(**kwargs)
    second = evaluate_fixed_background_false_positive_rate(**kwargs)
    assert first == second
    assert first["n_calibration"] == 99
    assert first["n_evaluation"] == 120
    assert first["calibration_minimum_resolvable_pvalue"] == 0.01
    assert first["calibration_resolution_allows_alpha_rejection"] is True
    assert 0 <= first["rejections"] <= 120
    assert 0 <= first["false_positive_rate"] <= 1
    assert 0 <= first["wilson_95_interval"]["lower"] <= first["false_positive_rate"]
    assert first["false_positive_rate"] <= first["wilson_95_interval"]["upper"] <= 1
    assert "not CMS validation" in first["interpretation"]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"n_calibration": 0},
        {"n_evaluation": 0},
        {"alpha": 0.0},
        {"alpha": 1.0},
        {"alpha": "0.05"},
        {"alpha": True},
        {"seed_calibration": 4, "seed_evaluation": 4},
        {"seed_calibration": -1},
    ],
)
def test_held_out_false_positive_evaluation_rejects_invalid_configuration(kwargs):
    from cms_dimuon_robustness.calibration import evaluate_fixed_background_false_positive_rate

    parameters = dict(
        expected_background=[4.0, 5.0],
        window_widths=[1],
        n_calibration=20,
        n_evaluation=20,
        alpha=0.05,
        seed_calibration=10,
        seed_evaluation=11,
    )
    parameters.update(kwargs)
    with pytest.raises(ValueError):
        evaluate_fixed_background_false_positive_rate(**parameters)

@pytest.mark.parametrize("confidence_z", [float("nan"), float("inf"), 0, -1, "1.96", True])
def test_wilson_interval_rejects_invalid_confidence_z(confidence_z):
    from cms_dimuon_robustness.calibration import wilson_interval

    with pytest.raises(ValueError):
        wilson_interval(1, 10, confidence_z=confidence_z)


def test_wilson_interval_has_exact_boundary_endpoints_and_reports_requested_level():
    from cms_dimuon_robustness.calibration import wilson_interval

    all_failures = wilson_interval(0, 100)
    all_successes = wilson_interval(100, 100)
    custom = wilson_interval(5, 10, confidence_z=1.0)

    assert all_failures["lower"] == 0.0
    assert all_successes["upper"] == 1.0
    assert custom["confidence_level_approx"] == pytest.approx(0.682689492)

def test_held_out_evaluation_rejects_identical_seeds_and_invalid_alpha():
    from cms_dimuon_robustness.calibration import evaluate_fixed_background_false_positive_rate

    base = dict(
        expected_background=[3.0, 4.0],
        window_widths=[1],
        n_calibration=20,
        n_evaluation=20,
        alpha=0.05,
        seed_calibration=7,
        seed_evaluation=8,
    )
    with pytest.raises(ValueError, match="seeds must differ"):
        evaluate_fixed_background_false_positive_rate(**{**base, "seed_evaluation": 7})
    with pytest.raises(ValueError, match="alpha"):
        evaluate_fixed_background_false_positive_rate(**{**base, "alpha": 1.0})


def test_held_out_evaluation_reports_when_calibration_resolution_is_too_coarse():
    from cms_dimuon_robustness.calibration import evaluate_fixed_background_false_positive_rate

    result = evaluate_fixed_background_false_positive_rate(
        expected_background=[2.0, 3.0],
        window_widths=[1],
        n_calibration=9,
        n_evaluation=20,
        alpha=0.05,
        seed_calibration=31,
        seed_evaluation=32,
    )
    assert result["calibration_minimum_resolvable_pvalue"] == pytest.approx(0.1)
    assert result["calibration_resolution_allows_alpha_rejection"] is False
    assert result["rejections"] == 0

def test_refitted_background_null_simulation_is_reproducible():
    from cms_dimuon_robustness.calibration import simulate_refitted_background_null

    means = [18.0, 16.0, 14.0, 12.0, 11.0, 10.0, 9.0, 8.0]
    first = simulate_refitted_background_null(
        means, [1, 2, 3], n_experiments=12, seed=20261028, background_order=1
    )
    second = simulate_refitted_background_null(
        means, [1, 2, 3], n_experiments=12, seed=20261028, background_order=1
    )
    assert first == second
    assert first["n_experiments"] == 12
    assert first["background_order"] == 1
    assert len(first["null_statistics"]) == 12
    assert all(value >= 0 for value in first["null_statistics"])
    assert 0 <= first["n_boundary_fits"] <= 12
    assert first["boundary_fit_rate"] == first["n_boundary_fits"] / 12
    assert len(first["boundary_fit_indices"]) == first["n_boundary_fits"]
    assert "not CMS validation" in first["interpretation"]


@pytest.mark.parametrize(
    "means,widths,n_experiments,seed,order",
    [
        ([], [1], 2, 1, 0),
        ([1.0, 0.0, 2.0], [1], 2, 1, 0),
        ([1.0, float("nan"), 2.0], [1], 2, 1, 0),
        ([1.0, 2.0], [1], 0, 1, 0),
        ([1.0, 2.0], [1], 2, -1, 0),
        ([1.0, 2.0], [1], 2, 1, True),
        ([1.0, 2.0], [1], 2, 1, 1),
    ],
)
def test_refitted_background_null_simulation_rejects_invalid_configuration(
    means, widths, n_experiments, seed, order
):
    from cms_dimuon_robustness.calibration import simulate_refitted_background_null

    with pytest.raises(ValueError):
        simulate_refitted_background_null(means, widths, n_experiments, seed, order)

def test_refitted_background_held_out_false_positive_evaluation_is_reproducible():
    from cms_dimuon_robustness.calibration import (
        evaluate_refitted_background_false_positive_rate,
    )

    kwargs = dict(
        null_generating_means=[18.0, 16.0, 14.0, 12.0, 11.0, 10.0, 9.0, 8.0],
        window_widths=[1, 2, 3],
        n_calibration=19,
        n_evaluation=25,
        alpha=0.05,
        seed_calibration=20261028,
        seed_evaluation=20261029,
        background_order=1,
    )
    first = evaluate_refitted_background_false_positive_rate(**kwargs)
    second = evaluate_refitted_background_false_positive_rate(**kwargs)
    assert first == second
    assert first["n_calibration"] == 19
    assert first["n_evaluation"] == 25
    assert first["background_order"] == 1
    assert 0 <= first["calibration_n_boundary_fits"] <= 19
    assert 0 <= first["evaluation_n_boundary_fits"] <= 25
    assert first["calibration_boundary_fit_rate"] == first["calibration_n_boundary_fits"] / 19
    assert first["evaluation_boundary_fit_rate"] == first["evaluation_n_boundary_fits"] / 25
    assert first["calibration_minimum_resolvable_pvalue"] == pytest.approx(0.05)
    assert first["calibration_resolution_allows_alpha_rejection"] is True
    assert 0 <= first["false_positive_rate"] <= 1
    assert first["wilson_95_interval"]["lower"] <= first["false_positive_rate"]
    assert first["false_positive_rate"] <= first["wilson_95_interval"]["upper"]
    assert first["interpretation"] == "refitted fixed-order toy null only; not CMS validation"


def test_refitted_background_held_out_evaluation_rejects_identical_seeds():
    from cms_dimuon_robustness.calibration import (
        evaluate_refitted_background_false_positive_rate,
    )

    with pytest.raises(ValueError, match="seeds must differ"):
        evaluate_refitted_background_false_positive_rate(
            null_generating_means=[5.0, 4.0, 3.0, 2.0],
            window_widths=[1],
            n_calibration=5,
            n_evaluation=5,
            alpha=0.05,
            seed_calibration=7,
            seed_evaluation=7,
            background_order=0,
        )


def test_empirical_rank_test_resolution_reports_discrete_size_grid():
    from cms_dimuon_robustness.calibration import empirical_rank_test_resolution

    result = empirical_rank_test_resolution(99, 0.05)
    assert result["minimum_resolvable_pvalue"] == 0.01
    assert result["max_null_exceedances_to_reject"] == 4
    assert result["unconditional_rejection_probability_under_iid_continuous_null"] == 0.05

    non_grid_aligned = empirical_rank_test_resolution(100, 0.05)
    assert non_grid_aligned["max_null_exceedances_to_reject"] == 4
    assert non_grid_aligned["unconditional_rejection_probability_under_iid_continuous_null"] == 5 / 101

    # This boundary is vulnerable to binary-float multiplication:
    # 0.29 * 100 can evaluate just below 29. The decimal input means
    # 29 of 100 rank slots are allowed at alpha=0.29.
    boundary = empirical_rank_test_resolution(99, 0.29)
    assert boundary["max_null_exceedances_to_reject"] == 28
    assert boundary["unconditional_rejection_probability_under_iid_continuous_null"] == 0.29


@pytest.mark.parametrize("n_calibration,alpha", [(0, 0.05), (True, 0.05), (100, 0.0), (100, 1.0)])
def test_empirical_rank_test_resolution_rejects_invalid_inputs(n_calibration, alpha):
    from cms_dimuon_robustness.calibration import empirical_rank_test_resolution

    with pytest.raises(ValueError):
        empirical_rank_test_resolution(n_calibration, alpha)



def test_refitted_null_reports_indices_of_boundary_active_fits(monkeypatch):
    import cms_dimuon_robustness.background_fit as background_fit
    from cms_dimuon_robustness.calibration import simulate_refitted_background_null

    calls = {"n": 0}

    def fake_fit(counts, order=1):
        index = calls["n"]
        calls["n"] += 1
        return {
            "expected_counts": np.ones(len(counts), dtype=float),
            "coefficient_boundary_active": index in {1, 3},
        }

    monkeypatch.setattr(background_fit, "fit_log_polynomial_background", fake_fit)
    result = simulate_refitted_background_null(
        [4.0, 5.0, 6.0, 7.0],
        [1, 2],
        n_experiments=5,
        seed=20261028,
        background_order=1,
    )

    assert result["n_boundary_fits"] == 2
    assert result["boundary_fit_rate"] == pytest.approx(0.4)
    assert result["boundary_fit_indices"] == [1, 3]


def test_refitted_evaluator_reports_boundary_rates_for_both_samples(monkeypatch):
    import cms_dimuon_robustness.calibration as calibration

    outputs = iter(
        [
            {
                "null_statistics": [0.0, 1.0, 2.0, 3.0],
                "n_boundary_fits": 2,
                "boundary_fit_rate": 0.5,
            },
            {
                "null_statistics": [0.0, 0.0, 1.0, 2.0],
                "n_boundary_fits": 1,
                "boundary_fit_rate": 0.25,
            },
        ]
    )

    def fake_simulator(*args, **kwargs):
        return next(outputs)

    monkeypatch.setattr(calibration, "simulate_refitted_background_null", fake_simulator)
    result = calibration.evaluate_refitted_background_false_positive_rate(
        null_generating_means=[3.0, 4.0, 5.0, 6.0],
        window_widths=[1],
        n_calibration=4,
        n_evaluation=4,
        alpha=0.5,
        seed_calibration=101,
        seed_evaluation=202,
        background_order=1,
    )

    assert result["calibration_n_boundary_fits"] == 2
    assert result["calibration_boundary_fit_rate"] == 0.5
    assert result["evaluation_n_boundary_fits"] == 1
    assert result["evaluation_boundary_fit_rate"] == 0.25
