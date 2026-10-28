"""Deterministic integration checks across the exploratory analysis components.

These tests check plumbing and invariants only. They do not validate the
background family, fit uncertainty, global p-values, or CMS data compatibility.
"""
import numpy as np

from cms_dimuon_robustness.background_fit import fit_log_polynomial_background
from cms_dimuon_robustness.global_scan import scan_for_excess
from cms_dimuon_robustness.residual_diagnostics import poisson_fit_residual_diagnostics


def test_fit_residual_diagnostics_and_scan_share_same_bins_and_finite_values():
    # Deterministic smooth spectrum with a small localized excess.
    x = np.linspace(-1.0, 1.0, 40)
    baseline = 18.0 * np.exp(-0.25 * x)
    observed = np.rint(baseline).astype(int)
    observed[21:24] += np.array([8, 15, 7])

    fit = fit_log_polynomial_background(observed, order=1)
    expected = np.asarray(fit["expected_counts"], dtype=float)
    diagnostics = poisson_fit_residual_diagnostics(
        observed, expected, n_fitted_parameters=fit["n_parameters"]
    )
    scan = scan_for_excess(observed, expected, window_widths=[1, 2, 3, 4])

    assert fit["optimizer_success"] is True
    assert expected.shape == observed.shape
    assert np.all(np.isfinite(expected)) and np.all(expected > 0)
    assert diagnostics["n_bins"] == observed.size
    assert diagnostics["n_fitted_parameters"] == fit["n_parameters"]
    assert np.all(np.isfinite(diagnostics["pearson_residuals"]))
    assert np.all(np.isfinite(diagnostics["deviance_residuals"]))
    assert scan["windows_scanned"] == sum(observed.size - w + 1 for w in [1, 2, 3, 4])
    assert 0 <= scan["start_bin"] <= observed.size - scan["window_width_bins"]
    assert scan["global_statistic_q0"] >= 0
    assert scan["observed_in_best_window"] >= 0
    assert scan["expected_in_best_window"] > 0


def test_no_excess_fixture_does_not_create_negative_scan_statistic():
    observed = np.full(24, 10, dtype=int)
    fit = fit_log_polynomial_background(observed, order=0)
    expected = np.asarray(fit["expected_counts"], dtype=float)
    scan = scan_for_excess(observed, expected, window_widths=[1, 2, 3])
    assert scan["global_statistic_q0"] >= 0
    assert scan["windows_scanned"] == (24 + 23 + 22)
