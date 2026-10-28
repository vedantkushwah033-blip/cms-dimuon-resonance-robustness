"""Finite-sample empirical calibration utilities."""
from __future__ import annotations

import math

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

    # Validate the scan configuration once, before allocating simulation work.
    # The all-zero fixture exercises the same width validation as each replicate.
    scan_poisson_excess(np.zeros(expected.size, dtype=np.int64), expected, window_widths)

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


def wilson_interval(
    successes: int, trials: int, confidence_z: float = 1.959963984540054
) -> dict[str, float]:
    """Return a two-sided Wilson score interval for a binomial proportion.

    This is a normal-score interval, not an exact Clopper-Pearson interval.
    It is useful for reporting Monte Carlo uncertainty without returning
    degenerate [0, 0] bounds when no false positives are observed.
    """
    if isinstance(successes, bool) or not isinstance(successes, (int, np.integer)):
        raise ValueError("successes must be an integer")
    if isinstance(trials, bool) or not isinstance(trials, (int, np.integer)):
        raise ValueError("trials must be a positive integer")
    if trials <= 0 or successes < 0 or successes > trials:
        raise ValueError("require trials > 0 and 0 <= successes <= trials")
    if isinstance(confidence_z, bool) or not isinstance(confidence_z, (int, float, np.integer, np.floating)):
        raise ValueError("confidence_z must be a finite positive number")
    if not np.isfinite(confidence_z) or confidence_z <= 0:
        raise ValueError("confidence_z must be finite and positive")

    p_hat = successes / trials
    z2 = confidence_z**2
    denominator = 1 + z2 / trials
    center = (p_hat + z2 / (2 * trials)) / denominator
    half_width = (
        confidence_z
        * np.sqrt(p_hat * (1 - p_hat) / trials + z2 / (4 * trials**2))
        / denominator
    )
    # The mathematical Wilson endpoints are exactly 0 or 1 at the
    # corresponding all-failure/all-success boundary. Clamp explicitly to
    # prevent floating-point roundoff from leaking tiny positive/negative
    # values through those known endpoints.
    lower = 0.0 if successes == 0 else max(0.0, center - half_width)
    upper = 1.0 if successes == trials else min(1.0, center + half_width)
    confidence_level = math.erf(float(confidence_z) / math.sqrt(2))
    return {
        "lower": float(lower),
        "upper": float(upper),
        "confidence_level_approx": float(confidence_level),
    }


def evaluate_fixed_background_false_positive_rate(
    expected_background: ArrayLike,
    window_widths: tuple[int, ...] | list[int],
    n_calibration: int,
    n_evaluation: int,
    alpha: float,
    seed_calibration: int,
    seed_evaluation: int,
) -> dict[str, int | float | bool | dict[str, float]]:
    """Evaluate empirical-rank rejection rate on a separate held-out toy null sample.

    A calibration sample defines the plus-one empirical upper-tail p-value for
    each held-out maximum scan statistic. The held-out false-positive fraction
    and Wilson score interval are returned. This is a fixed-known-background
    simulation only; it does not validate fitted-background uncertainty, model
    selection, detector effects, or real CMS data. Use distinct seeds and freeze
    the scan, alpha, and simulation design before interpreting the result.
    """
    for value, name in ((n_calibration, "n_calibration"), (n_evaluation, "n_evaluation")):
        if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value <= 0:
            raise ValueError(f"{name} must be a positive integer")
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float, np.integer, np.floating)):
        raise ValueError("alpha must be a finite number strictly between 0 and 1")
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must be finite and strictly between 0 and 1")
    for seed, name in ((seed_calibration, "seed_calibration"), (seed_evaluation, "seed_evaluation")):
        if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)) or seed < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    if seed_calibration == seed_evaluation:
        raise ValueError("calibration and evaluation seeds must differ")

    calibration = simulate_fixed_background_null(
        expected_background, window_widths, int(n_calibration), int(seed_calibration)
    )["null_statistics"]
    evaluation = simulate_fixed_background_null(
        expected_background, window_widths, int(n_evaluation), int(seed_evaluation)
    )["null_statistics"]
    calibration_array = np.asarray(calibration, dtype=float)
    evaluation_array = np.asarray(evaluation, dtype=float)

    # Apply the same plus-one rank convention to every held-out replicate.
    # Sorting keeps memory bounded and reduces evaluation to O(N log M),
    # avoiding a potentially huge N-by-M comparison matrix.
    sorted_calibration = np.sort(calibration_array)
    tail_counts = int(n_calibration) - np.searchsorted(
        sorted_calibration, evaluation_array, side="left"
    )
    p_values = (1 + tail_counts) / (int(n_calibration) + 1)
    rejected = int(np.count_nonzero(p_values <= alpha))
    interval = wilson_interval(rejected, int(n_evaluation))
    return {
        "alpha": float(alpha),
        "n_calibration": int(n_calibration),
        "n_evaluation": int(n_evaluation),
        "seed_calibration": int(seed_calibration),
        "seed_evaluation": int(seed_evaluation),
        "rejections": rejected,
        "false_positive_rate": float(rejected / int(n_evaluation)),
        "wilson_95_interval": interval,
        "calibration_minimum_resolvable_pvalue": float(1 / (int(n_calibration) + 1)),
        "calibration_resolution_allows_alpha_rejection": bool(1 / (int(n_calibration) + 1) <= alpha),
        "interpretation": "fixed-known-background toy simulation only; not CMS validation",
    }
