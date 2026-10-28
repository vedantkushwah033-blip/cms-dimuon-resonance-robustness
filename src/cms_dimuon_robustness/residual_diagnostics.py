"""Descriptive residual diagnostics for binned Poisson background fits.

These diagnostics summarize fit discrepancies; they are not calibrated goodness-of-fit
p-values and do not account for leverage, model selection, or parameter uncertainty.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def poisson_fit_residual_diagnostics(
    observed_counts: ArrayLike,
    expected_counts: ArrayLike,
    n_fitted_parameters: int,
) -> dict[str, object]:
    """Return Pearson/deviance residuals and descriptive aggregate diagnostics.

    The observed and expected arrays must correspond to the same bins. Expected
    means must be strictly positive. The reported Pearson statistic and deviance
    are descriptive only: comparing either with a naive chi-square reference
    distribution is not justified automatically after fitting or selecting a model.
    """
    try:
        observed = np.asarray(observed_counts, dtype=float)
        expected = np.asarray(expected_counts, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("observed_counts and expected_counts must be numeric arrays") from exc
    if (
        observed.ndim != 1
        or expected.ndim != 1
        or observed.size == 0
        or observed.shape != expected.shape
    ):
        raise ValueError("observed_counts and expected_counts must be same-length non-empty 1D arrays")
    if not np.all(np.isfinite(observed)) or np.any(observed < 0):
        raise ValueError("observed_counts must be finite and non-negative")
    if not np.all(observed == np.floor(observed)):
        raise ValueError("observed_counts must be integer-valued")
    if not np.all(np.isfinite(expected)) or np.any(expected <= 0):
        raise ValueError("expected_counts must be finite and strictly positive")
    if (
        isinstance(n_fitted_parameters, bool)
        or not isinstance(n_fitted_parameters, (int, np.integer))
        or n_fitted_parameters < 0
        or n_fitted_parameters >= observed.size
    ):
        raise ValueError("n_fitted_parameters must be an integer in [0, n_bins)")

    y = observed.astype(float, copy=False)
    pearson = (y - expected) / np.sqrt(expected)
    deviance_terms = np.empty_like(y)
    positive = y > 0
    deviance_terms[positive] = (
        2.0 * (y[positive] * np.log(y[positive] / expected[positive])
               - (y[positive] - expected[positive]))
    )
    deviance_terms[~positive] = 2.0 * expected[~positive]
    # Small negative values can arise from floating-point cancellation at y ~= mu.
    deviance_terms = np.maximum(deviance_terms, 0.0)
    deviance = np.sign(y - expected) * np.sqrt(deviance_terms)

    pearson_statistic = float(np.sum(pearson**2))
    deviance_statistic = float(np.sum(deviance_terms))
    return {
        "pearson_residuals": pearson.tolist(),
        "deviance_residuals": deviance.tolist(),
        "pearson_chi_square_descriptive": pearson_statistic,
        "poisson_deviance_descriptive": deviance_statistic,
        "n_bins": int(y.size),
        "n_fitted_parameters": int(n_fitted_parameters),
        "nominal_residual_degrees_of_freedom": int(y.size - n_fitted_parameters),
        "max_absolute_pearson_residual": float(np.max(np.abs(pearson))),
        "max_absolute_deviance_residual": float(np.max(np.abs(deviance))),
        "interpretation": (
            "descriptive residual diagnostics only; no calibrated goodness-of-fit p-value, "
            "leverage adjustment, model-selection correction, or parameter-uncertainty treatment"
        ),
    }
