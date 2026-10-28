"""Exploratory scan-level Poisson excess statistic for binned spectra.

This module deliberately does not fit a background, select a model, or claim
CMS detector-level validity. It accepts an externally supplied expected
background and computes the maximum one-sided Poisson likelihood-ratio
statistic over a declared set of contiguous bin windows.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _validate_spectrum(counts: ArrayLike, expected_background: ArrayLike) -> tuple[NDArray, NDArray]:
    observed = np.asarray(counts)
    expected = np.asarray(expected_background, dtype=float)
    if observed.ndim != 1 or expected.ndim != 1 or observed.shape != expected.shape:
        raise ValueError("counts and expected_background must be same-length 1D arrays")
    if observed.size == 0:
        raise ValueError("spectrum must contain at least one bin")
    if not np.all(np.isfinite(observed)) or np.any(observed < 0):
        raise ValueError("counts must be finite and non-negative")
    if not np.all(observed == np.floor(observed)):
        raise ValueError("counts must be integer-valued")
    if not np.all(np.isfinite(expected)) or np.any(expected <= 0):
        raise ValueError("expected_background must be finite and strictly positive")
    return observed.astype(np.int64, copy=False), expected


def poisson_excess_log_likelihood_ratio(observed: int | float, expected: float) -> float:
    """Return q0 for a one-bin upward-only Poisson excess, with signal >= 0.

    q0 = 2 * [n log(n/b) - (n-b)] when n > b, and zero otherwise.
    The n=0 term is handled by its continuous limit.
    """
    n = float(observed)
    b = float(expected)
    if not np.isfinite(n) or n < 0 or n != np.floor(n):
        raise ValueError("observed must be a finite non-negative integer")
    if not np.isfinite(b) or b <= 0:
        raise ValueError("expected must be finite and strictly positive")
    if n <= b:
        return 0.0
    return float(2.0 * (n * np.log(n / b) - (n - b)))


def scan_poisson_excess(
    counts: ArrayLike,
    expected_background: ArrayLike,
    window_widths: tuple[int, ...] | list[int],
) -> dict[str, int | float | list[int]]:
    """Return the largest one-sided Poisson LLR over all contiguous bin windows.

    Each width is measured in bins. Every valid start position is scanned.
    The returned global statistic is the maximum local q0; its null distribution
    must be calibrated for the same frozen scan, including the look-elsewhere
    effect. This function does not produce a calibrated p-value.
    """
    observed, expected = _validate_spectrum(counts, expected_background)
    if not window_widths:
        raise ValueError("window_widths must contain at least one width")
    widths: list[int] = []
    for width in window_widths:
        if isinstance(width, bool) or not isinstance(width, (int, np.integer)):
            raise ValueError("window widths must be integers")
        if width <= 0 or width > observed.size:
            raise ValueError("each window width must be between 1 and number of bins")
        if int(width) not in widths:
            widths.append(int(width))

    best_q = 0.0
    best_start = 0
    best_width = widths[0]
    best_n = 0
    best_b = 0.0
    scanned = 0
    for width in widths:
        obs_sum = np.convolve(observed, np.ones(width, dtype=np.int64), mode="valid")
        exp_sum = np.convolve(expected, np.ones(width, dtype=float), mode="valid")
        for start, (n, b) in enumerate(zip(obs_sum, exp_sum, strict=True)):
            scanned += 1
            q = poisson_excess_log_likelihood_ratio(int(n), float(b))
            if q > best_q:
                best_q = q
                best_start = start
                best_width = width
                best_n = int(n)
                best_b = float(b)

    return {
        "global_statistic_q0": float(best_q),
        "start_bin": int(best_start),
        "window_width_bins": int(best_width),
        "observed_in_best_window": int(best_n),
        "expected_in_best_window": float(best_b),
        "windows_scanned": int(scanned),
    }
