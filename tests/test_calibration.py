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

