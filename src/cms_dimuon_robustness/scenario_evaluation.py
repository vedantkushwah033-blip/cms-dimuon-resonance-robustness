"""Run a declared set of refitted-background toy-null scenarios.

This is orchestration only: scenario means and numerical design are supplied
explicitly by the caller. Results are toy-model diagnostics, not CMS validation.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np

from cms_dimuon_robustness.calibration import (
    evaluate_refitted_background_false_positive_rate,
)


def evaluate_null_scenarios(
    scenario_means: Mapping[str, Sequence[float]],
    window_widths: Sequence[int],
    n_calibration: int,
    n_evaluation: int,
    alpha: float,
    scenario_seeds: Mapping[str, tuple[int, int]],
    background_order: int = 1,
) -> dict[str, Any]:
    """Evaluate each named mean vector using independent calibration/evaluation seeds.

    Every scenario must have an explicit non-empty name, positive finite means,
    the same number of bins, and a pair of distinct non-negative integer seeds.
    Seeds must be unique across all scenario roles to reduce accidental stream
    reuse. Common binning is required because changing the number of bins also
    changes the scan's number of candidate windows and therefore its null law.
    This function does not choose scenario parameters or imply physical realism.
    """
    if not isinstance(scenario_means, Mapping) or not scenario_means:
        raise ValueError("scenario_means must be a non-empty mapping")
    if not isinstance(scenario_seeds, Mapping):
        raise ValueError("scenario_seeds must be a mapping")
    names = list(scenario_means)
    if any(not isinstance(name, str) or not name.strip() for name in names):
        raise ValueError("scenario names must be non-empty strings")
    if len(set(names)) != len(names):
        raise ValueError("scenario names must be unique")
    if set(scenario_seeds) != set(names):
        raise ValueError("scenario_seeds must contain exactly the scenario names")

    validated_means: dict[str, list[float]] = {}
    all_seeds: list[int] = []
    for name in names:
        means = np.asarray(scenario_means[name], dtype=float)
        if means.ndim != 1 or means.size == 0:
            raise ValueError(f"{name}: means must be a non-empty 1D vector")
        if not np.all(np.isfinite(means)) or np.any(means <= 0):
            raise ValueError(f"{name}: means must be finite and strictly positive")
        seeds = scenario_seeds[name]
        if not isinstance(seeds, (tuple, list)) or len(seeds) != 2:
            raise ValueError(f"{name}: seeds must be (calibration_seed, evaluation_seed)")
        for seed in seeds:
            if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)) or seed < 0:
                raise ValueError(f"{name}: seeds must be non-negative integers")
            all_seeds.append(int(seed))
        if int(seeds[0]) == int(seeds[1]):
            raise ValueError(f"{name}: calibration and evaluation seeds must differ")
        validated_means[name] = means.tolist()

    bin_counts = {len(means) for means in validated_means.values()}
    if len(bin_counts) != 1:
        raise ValueError("all scenarios must use the same number of bins for comparable scans")
    if len(set(all_seeds)) != len(all_seeds):
        raise ValueError("all calibration/evaluation seeds must be unique across scenarios")

    results: list[dict[str, Any]] = []
    for name in names:
        calibration_seed, evaluation_seed = scenario_seeds[name]
        result = evaluate_refitted_background_false_positive_rate(
            null_generating_means=validated_means[name],
            window_widths=list(window_widths),
            n_calibration=n_calibration,
            n_evaluation=n_evaluation,
            alpha=alpha,
            seed_calibration=int(calibration_seed),
            seed_evaluation=int(evaluation_seed),
            background_order=background_order,
        )
        results.append(
            {
                "scenario": name,
                "n_bins": len(validated_means[name]),
                "null_generating_means": validated_means[name],
                **result,
            }
        )

    return {
        "design": {
            "window_widths_bins": list(window_widths),
            "n_calibration": int(n_calibration),
            "n_evaluation": int(n_evaluation),
            "alpha": float(alpha),
            "background_order": int(background_order),
            "scenario_count": len(names),
            "n_bins": next(iter(bin_counts)),
            "interpretation": (
                "per-scenario fixed toy nulls; no guarantee of uniform type-I control "
                "or CMS validity"
            ),
        },
        "results": results,
    }
