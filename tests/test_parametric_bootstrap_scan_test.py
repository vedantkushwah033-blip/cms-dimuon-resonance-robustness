import numpy as np
import pytest

from cms_dimuon_robustness.calibration import parametric_bootstrap_scan_test
from cms_dimuon_robustness.null_scenarios import log_polynomial_null_means


def test_parametric_bootstrap_scan_test_is_reproducible_and_reports_rank():
    means = np.asarray(log_polynomial_null_means([2.7, 0.12], n_bins=60))
    observed = np.random.default_rng(20261030).poisson(means)

    first = parametric_bootstrap_scan_test(
        observed,
        window_widths=[2, 4, 6],
        n_calibration=30,
        seed=8123,
        background_order=1,
    )
    second = parametric_bootstrap_scan_test(
        observed,
        window_widths=[2, 4, 6],
        n_calibration=30,
        seed=8123,
        background_order=1,
    )

    assert first["observed_scan"] == second["observed_scan"]
    assert first["calibration"]["null_statistics"] == second["calibration"]["null_statistics"]
    assert first["empirical_rank"] == second["empirical_rank"]
    assert first["n_calibration"] == 30
    assert first["window_widths_bins"] == [2, 4, 6]
    assert first["empirical_rank"]["n_calibration"] == 30
    assert first["empirical_rank"]["empirical_pvalue"] == pytest.approx(
        (first["empirical_rank"]["exceedances_or_ties"] + 1) / 31
    )
    assert "plug-in parametric bootstrap" in first["interpretation"]


@pytest.mark.parametrize(
    ("observed", "n_calibration", "seed", "order", "message"),
    [
        ([], 10, 1, 1, "non-empty"),
        ([1.0, np.nan, 2.0], 10, 1, 1, "finite"),
        ([1.0, -1.0, 2.0], 10, 1, 1, "non-negative"),
        ([1.0, 1.5, 2.0], 10, 1, 1, "integer-valued"),
        ([1.0, 2.0, 3.0], 0, 1, 1, "n_calibration"),
        ([1.0, 2.0, 3.0], 10, -1, 1, "seed"),
        ([1.0, 2.0, 3.0], 10, 1, -1, "background_order"),
    ],
)
def test_parametric_bootstrap_scan_test_rejects_invalid_inputs(
    observed, n_calibration, seed, order, message
):
    with pytest.raises(ValueError, match=message):
        parametric_bootstrap_scan_test(
            observed,
            window_widths=[1],
            n_calibration=n_calibration,
            seed=seed,
            background_order=order,
        )


def test_parametric_bootstrap_scan_test_rejects_too_few_bins_for_fit():
    with pytest.raises(ValueError, match="number of bins"):
        parametric_bootstrap_scan_test(
            [3, 4],
            window_widths=[1],
            n_calibration=10,
            seed=1,
            background_order=1,
        )


def test_parametric_bootstrap_scan_test_validates_scan_before_fit():
    with pytest.raises(ValueError, match="window width"):
        parametric_bootstrap_scan_test(
            [3, 4, 5, 6],
            window_widths=[0],
            n_calibration=10,
            seed=1,
            background_order=1,
        )
