"""Explicit synthetic null-generating mean vectors for calibration stress tests.

These are mathematical toy scenarios, not fitted or validated CMS background models.
Coordinates intentionally match the current fitter's linspace(-1, 1, n_bins) convention.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


def _finite_vector(values: ArrayLike, name: str) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    if result.ndim != 1 or result.size == 0:
        raise ValueError(f"{name} must be a non-empty one-dimensional array")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values")
    return result


def log_polynomial_null_means(
    coefficients: ArrayLike,
    n_bins: int,
) -> list[float]:
    """Build strictly positive means mu_i = exp(sum_j beta_j x_i**j).

    Coefficients are ordered from intercept upward. The normalized coordinate
    matches fit_log_polynomial_background: np.linspace(-1, 1, n_bins). This
    helper specifies a generator only; it does not assert physical adequacy.
    """
    beta = _finite_vector(coefficients, "coefficients")
    n_bins = _positive_integer(n_bins, "n_bins")
    if n_bins <= beta.size:
        raise ValueError("n_bins must exceed the number of coefficients")
    x = np.linspace(-1.0, 1.0, n_bins)
    design = np.vander(x, N=beta.size, increasing=True)
    log_means = design @ beta
    if not np.all(np.isfinite(log_means)) or np.any(log_means > np.log(np.finfo(float).max)):
        raise ValueError("coefficients produce non-finite or overflowing means")
    means = np.exp(log_means)
    if not np.all(np.isfinite(means)) or np.any(means <= 0):
        raise ValueError("coefficients must produce finite, strictly positive means")
    return means.tolist()


def local_shoulder_null_means(
    base_coefficients: ArrayLike,
    n_bins: int,
    amplitude: float,
    center: float,
    width: float,
) -> list[float]:
    """Add a positive Gaussian-shaped shoulder to a log-polynomial baseline.

    mu_i = exp(sum_j beta_j x_i**j) + A * exp(-0.5 * ((x_i-center)/width)**2)

    The additive shoulder creates a deliberate departure from the fitted
    log-polynomial family when that family cannot represent the resulting sum.
    All parameters are dimensionless toy-model coordinates, not CMS units.
    """
    beta = _finite_vector(base_coefficients, "base_coefficients")
    n_bins = _positive_integer(n_bins, "n_bins")
    if n_bins <= beta.size:
        raise ValueError("n_bins must exceed the number of base coefficients")
    for value, name in ((amplitude, "amplitude"), (center, "center"), (width, "width")):
        if isinstance(value, bool) or not isinstance(value, (int, float, np.integer, np.floating)):
            raise ValueError(f"{name} must be a finite real number")
        if not np.isfinite(value):
            raise ValueError(f"{name} must be a finite real number")
    if amplitude < 0:
        raise ValueError("amplitude must be non-negative")
    if width <= 0:
        raise ValueError("width must be strictly positive")

    baseline = np.asarray(log_polynomial_null_means(beta, n_bins), dtype=float)
    x = np.linspace(-1.0, 1.0, n_bins)
    shoulder = float(amplitude) * np.exp(-0.5 * ((x - float(center)) / float(width)) ** 2)
    means = baseline + shoulder
    if not np.all(np.isfinite(means)) or np.any(means <= 0):
        raise ValueError("parameters produce invalid null-generating means")
    return means.tolist()
