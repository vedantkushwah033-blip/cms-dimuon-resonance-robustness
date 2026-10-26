"""Histogram helpers with ROOT-compatible half-open mass-range semantics."""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def histogram_masses(
    masses: ArrayLike,
    *,
    bins: int,
    mass_min: float,
    mass_max: float,
) -> tuple[NDArray[np.int64], dict[str, int]]:
    """Count finite masses using [mass_min, mass_max), as ROOT histograms do.

    Values exactly at the upper edge are overflow, not part of the final bin.
    Non-finite values are counted separately and excluded from all range counters.
    """
    if isinstance(bins, bool) or not isinstance(bins, int) or bins <= 0:
        raise ValueError("bins must be a positive integer")
    if not np.isfinite(mass_min) or not np.isfinite(mass_max) or not 0 < mass_min < mass_max:
        raise ValueError("require finite bounds with 0 < mass_min < mass_max")

    values = np.asarray(masses, dtype=float).reshape(-1)
    finite = values[np.isfinite(values)]
    in_range = finite[(finite >= mass_min) & (finite < mass_max)]
    edges = np.linspace(mass_min, mass_max, bins + 1)
    counts = np.histogram(in_range, bins=edges)[0].astype(np.int64, copy=False)
    summary = {
        "pairs_total": int(values.size),
        "pairs_nonfinite": int(values.size - finite.size),
        "pairs_below_range": int(np.count_nonzero(finite < mass_min)),
        "pairs_in_range": int(in_range.size),
        "pairs_above_range": int(np.count_nonzero(finite >= mass_max)),
    }
    if int(counts.sum()) != summary["pairs_in_range"]:
        raise RuntimeError("histogram accounting invariant violated")
    return counts, summary
