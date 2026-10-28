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
