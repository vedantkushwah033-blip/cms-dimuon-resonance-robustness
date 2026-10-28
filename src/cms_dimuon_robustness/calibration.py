"""Finite-sample empirical calibration utilities."""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def empirical_upper_tail_pvalue(observed_statistic: float, null_statistics: ArrayLike) -> dict[str, int | float]:
    """Compute plus-one upper-tail rank p-value from supplied null statistics.

    Null values must be generated independently by the same fully specified
    analysis pipeline as the observed statistic. This function cannot verify
    that scientific assumption or generate pseudoexperiments.
    """
    observed = float(observed_statistic)
    null = np.asarray(null_statistics, dtype=float)
    if not np.isfinite(observed):
        raise ValueError("observed_statistic must be finite")
    if null.ndim != 1 or null.size == 0:
        raise ValueError("null_statistics must be a non-empty 1D array")
    if not np.all(np.isfinite(null)):
        raise ValueError("null_statistics must contain only finite values")
    exceedances = int(np.count_nonzero(null >= observed))
    n_calibration = int(null.size)
    return {
        "empirical_pvalue": float((exceedances + 1) / (n_calibration + 1)),
        "exceedances_or_ties": exceedances,
        "n_calibration": n_calibration,
        "minimum_resolvable_pvalue": float(1 / (n_calibration + 1)),
    }


def simulate_fixed_background_null(
    expected_background: ArrayLike,
    window_widths: tuple[int, ...] | list[int],
    n_experiments: int,
    seed: int,
) -> dict[str, int | list[float]]:
    """Generate null scan maxima under a fixed, known Poisson background.

    Each pseudoexperiment draws independent bin counts from Poisson means given
    by expected_background and runs the identical scan over window_widths. The
    fixed background is treated as known: this does not include fitted-background
    uncertainty, model selection, detector effects, or CMS data validation. Use a
    separate random stream/sample for calibration and held-out type-I-error tests.
    """
    expected = np.asarray(expected_background, dtype=float)
    if expected.ndim != 1 or expected.size == 0:
        raise ValueError("expected_background must be a non-empty 1D array")
    if not np.all(np.isfinite(expected)) or np.any(expected <= 0):
        raise ValueError("expected_background must be finite and strictly positive")
    if isinstance(n_experiments, bool) or not isinstance(n_experiments, (int, np.integer)):
        raise ValueError("n_experiments must be a positive integer")
    if n_experiments <= 0:
        raise ValueError("n_experiments must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)) or seed < 0:
        raise ValueError("seed must be a non-negative integer")

    from cms_dimuon_robustness.global_scan import scan_poisson_excess

    rng = np.random.default_rng(int(seed))
    maxima: list[float] = []
    for _ in range(int(n_experiments)):
        counts = rng.poisson(expected)
        result = scan_poisson_excess(counts, expected, window_widths)
        maxima.append(float(result["global_statistic_q0"]))

    return {
        "null_statistics": maxima,
        "n_experiments": int(n_experiments),
        "seed": int(seed),
    }
