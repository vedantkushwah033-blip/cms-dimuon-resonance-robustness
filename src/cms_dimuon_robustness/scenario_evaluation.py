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
from cms_dimuon_robustness.global_scan import scan_poisson_excess


def evaluate_null_scenarios(
    scenario_means: Mapping[str, Sequence[float]],
    window_widths: Sequence[int],
    n_calibration: int,
    n_evaluation: int,
    alpha: float,
    scenario_seeds: Mapping[str, tuple[int, int]],
    background_order: int = 1,
) -> dict[str, Any]:
    """Evaluate named mean vectors with independent calibration/evaluation seeds.

    Scenarios must have explicit non-empty names, positive finite means, the
    same number of bins, and distinct non-negative integer seeds. All scenario
    roles use unique seeds. Common binning is required because changing the bin
    count changes the candidate-window set and the null law of the maximum.

    Shared design inputs are validated before any evaluator is called, so a bad
    scan or sample-size setting cannot trigger partial scenario evaluation.
    Duplicate window widths are normalized to their first occurrence, matching
    the underlying scan's behavior, and the normalized list is recorded.
    This utility does not choose scenario parameters or imply physical realism.
    """
    if not isinstance(scenario_means, Mapping) or not scenario_means:
        raise ValueError("scenario_means must be a non-empty mapping")
    if not isinstance(scenario_seeds, Mapping):
        raise ValueError("scenario_seeds must be a mapping")
    names = list(scenario_means)
    if any(not isinstance(name, str) or not name.strip() for name in names):
        raise ValueError("scenario names must be non-empty strings")
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
    n_bins = next(iter(bin_counts))

    for value, label in ((n_calibration, "n_calibration"), (n_evaluation, "n_evaluation")):
        if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value <= 0:
            raise ValueError(f"{label} must be a positive integer")
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float, np.integer, np.floating)):
        raise ValueError("alpha must be finite and strictly between 0 and 1")
    if not np.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must be finite and strictly between 0 and 1")
    if (
        isinstance(background_order, bool)
        or not isinstance(background_order, (int, np.integer))
        or background_order < 0
    ):
        raise ValueError("background_order must be a non-negative integer")
    if n_bins <= int(background_order) + 1:
        raise ValueError("number of bins must exceed the number of fitted coefficients")
    if isinstance(window_widths, (str, bytes)):
        raise ValueError("window_widths must be a non-empty sequence of integer widths")
    try:
        requested_widths = list(window_widths)
    except TypeError as exc:
        raise ValueError("window_widths must be a non-empty sequence of integer widths") from exc
    if not requested_widths:
        raise ValueError("window_widths must contain at least one width")
    # Validate every shared scan parameter before any Monte Carlo work starts.
    normalized_widths: list[int] = []
    for width in requested_widths:
        if isinstance(width, bool) or not isinstance(width, (int, np.integer)):
            raise ValueError("window widths must be integers")
        if width <= 0 or width > n_bins:
            raise ValueError("each window width must be between 1 and number of bins")
        if int(width) not in normalized_widths:
            normalized_widths.append(int(width))
    scan_poisson_excess(
        np.zeros(n_bins, dtype=np.int64),
        np.ones(n_bins, dtype=float),
        normalized_widths,
    )

    results: list[dict[str, Any]] = []
    for name in names:
        calibration_seed, evaluation_seed = scenario_seeds[name]
        result = evaluate_refitted_background_false_positive_rate(
            null_generating_means=validated_means[name],
            window_widths=normalized_widths,
            n_calibration=int(n_calibration),
            n_evaluation=int(n_evaluation),
            alpha=float(alpha),
            seed_calibration=int(calibration_seed),
            seed_evaluation=int(evaluation_seed),
            background_order=int(background_order),
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
            "window_widths_bins": normalized_widths,
            "n_calibration": int(n_calibration),
            "n_evaluation": int(n_evaluation),
            "alpha": float(alpha),
            "background_order": int(background_order),
            "scenario_count": len(names),
            "n_bins": n_bins,
            "interpretation": (
                "per-scenario fixed toy nulls; no guarantee of uniform type-I control "
                "or CMS validity"
            ),
        },
        "results": results,
    }
