#!/usr/bin/env python3
"""Fail-closed structural gate for a confirmatory global-calibration protocol.

This validates completeness and authorization fields only. It does not validate
statistical correctness, physical realism, scientific novelty, or data quality.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

import yaml


def validate_protocol(document: Any) -> list[str]:
    """Return protocol errors; an empty list means structural gates are satisfied."""
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["protocol root must be a YAML mapping"]

    def require_mapping(parent: dict[str, Any], key: str, label: str) -> dict[str, Any]:
        value = parent.get(key)
        if not isinstance(value, dict):
            errors.append(f"{label} must be a mapping")
            return {}
        return value

    def require_nonempty_string(value: Any, label: str) -> None:
        if not isinstance(value, str) or not value.strip() or value.strip().upper() == "UNRESOLVED":
            errors.append(f"{label} must be a resolved, non-empty string")

    def require_positive_int(value: Any, label: str) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            errors.append(f"{label} must be a positive integer")

    if document.get("status") != "frozen":
        errors.append("status must be 'frozen' before confirmatory use")

    require_nonempty_string(document.get("protocol_version"), "protocol_version")
    require_nonempty_string(document.get("research_question"), "research_question")

    estimand = require_mapping(document, "estimand", "estimand")
    require_nonempty_string(estimand.get("name"), "estimand.name")
    require_nonempty_string(estimand.get("definition"), "estimand.definition")
    alpha = estimand.get("nominal_alpha")
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float)) or not math.isfinite(alpha) or not 0 < alpha < 1:
        errors.append("estimand.nominal_alpha must be finite and strictly between 0 and 1")

    analysis = require_mapping(document, "analysis", "analysis")
    mass_range = analysis.get("mass_range_GeV")
    if (
        not isinstance(mass_range, list)
        or len(mass_range) != 2
        or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in mass_range)
        or mass_range[0] <= 0
        or mass_range[0] >= mass_range[1]
    ):
        errors.append("analysis.mass_range_GeV must be two finite increasing positive bounds")
    require_positive_int(analysis.get("histogram_bins"), "analysis.histogram_bins")
    for key in ("local_test_statistic", "global_statistic", "likelihood", "nuisance_parameter_policy", "fit_range_policy"):
        require_nonempty_string(analysis.get(key), f"analysis.{key}")
    if not isinstance(analysis.get("scan_windows"), list) or not analysis["scan_windows"]:
        errors.append("analysis.scan_windows must be a non-empty, explicitly declared list")

    models = document.get("background_models")
    if not isinstance(models, list) or not models:
        errors.append("background_models must be a non-empty list")
    else:
        seen_model_ids: set[str] = set()
        for index, model in enumerate(models):
            label = f"background_models[{index}]"
            if not isinstance(model, dict):
                errors.append(f"{label} must be a mapping")
                continue
            model_id = model.get("id")
            require_nonempty_string(model_id, f"{label}.id")
            if isinstance(model_id, str) and model_id in seen_model_ids:
                errors.append(f"duplicate background model id: {model_id}")
            if isinstance(model_id, str):
                seen_model_ids.add(model_id)
            for key in ("functional_form", "role"):
                require_nonempty_string(model.get(key), f"{label}.{key}")
            if not isinstance(model.get("parameter_bounds"), dict) or not model["parameter_bounds"]:
                errors.append(f"{label}.parameter_bounds must explicitly define parameter bounds")

    selection = require_mapping(document, "model_selection", "model_selection")
    if not isinstance(selection.get("enabled"), bool):
        errors.append("model_selection.enabled must be explicitly true or false")
    if selection.get("enabled") is True:
        for key in ("algorithm", "tie_breaking"):
            require_nonempty_string(selection.get(key), f"model_selection.{key}")
    elif selection.get("enabled") is False:
        if selection.get("algorithm") not in ("not-applicable", "none"):
            errors.append("model_selection.algorithm must explicitly be 'not-applicable' or 'none' when disabled")

    generators = require_mapping(document, "generators", "generators")
    partition_names = ("development", "calibration", "held_out_evaluation")
    partitions: dict[str, set[str]] = {}
    for partition in partition_names:
        values = generators.get(partition)
        if not isinstance(values, list) or not values:
            errors.append(f"generators.{partition} must be a non-empty list")
            partitions[partition] = set()
            continue
        normalized: set[str] = set()
        for index, value in enumerate(values):
            require_nonempty_string(value, f"generators.{partition}[{index}]")
            if isinstance(value, str):
                normalized.add(value)
        if len(normalized) != len(values):
            errors.append(f"generators.{partition} contains duplicate scenario IDs")
        partitions[partition] = normalized
    for left, right in (
        ("development", "calibration"),
        ("development", "held_out_evaluation"),
        ("calibration", "held_out_evaluation"),
    ):
        overlap = partitions[left] & partitions[right]
        if overlap:
            errors.append(f"generator partitions {left} and {right} overlap: {sorted(overlap)}")
    if generators.get("held_out_outside_candidate_family") is not True:
        errors.append("generators.held_out_outside_candidate_family must be true and justified")

    calibration = require_mapping(document, "calibration", "calibration")
    for key in ("threshold_method", "quantile_convention", "primary_comparison"):
        require_nonempty_string(calibration.get(key), f"calibration.{key}")
    require_positive_int(calibration.get("calibration_replicates"), "calibration.calibration_replicates")
    require_positive_int(calibration.get("evaluation_replicates_per_scenario"), "calibration.evaluation_replicates_per_scenario")
    if calibration.get("confidence_interval") != "two-sided Clopper-Pearson exact binomial interval":
        errors.append("calibration.confidence_interval must use the declared exact binomial interval or be explicitly reviewed and changed")

    failures = require_mapping(document, "failure_policy", "failure_policy")
    for key in ("definition", "primary_handling", "sensitivity_analysis"):
        require_nonempty_string(failures.get(key), f"failure_policy.{key}")

    randomness = require_mapping(document, "randomness", "randomness")
    require_nonempty_string(randomness.get("seed_strategy"), "randomness.seed_strategy")
    if randomness.get("independent_streams_for_partitions") is not True:
        errors.append("randomness.independent_streams_for_partitions must be true")

    artifacts = require_mapping(document, "artifacts", "artifacts")
    for key in ("per_replicate_schema", "environment_lock", "manifest", "output_checksums"):
        require_nonempty_string(artifacts.get(key), f"artifacts.{key}")

    gates = require_mapping(document, "gates", "gates")
    required_gates = {
        "real_data_baseline_parity": "passed",
        "literature_novelty_review": "completed",
        "expert_protocol_review": "completed",
        "confirmatory_execution_authorized": True,
    }
    for key, expected in required_gates.items():
        if gates.get(key) != expected:
            errors.append(f"gates.{key} must equal {expected!r} before confirmatory execution")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("protocol", type=Path, help="Path to the machine-readable YAML protocol")
    args = parser.parse_args()
    try:
        document = yaml.safe_load(args.protocol.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot read valid YAML protocol: {exc}")
        return 2

    errors = validate_protocol(document)
    if errors:
        print(f"BLOCKED: {len(errors)} protocol gate(s) remain unresolved.")
        for error in errors:
            print(f"- {error}")
        return 2

    print("STRUCTURAL GATE PASSED. This does not validate scientific correctness or authorize a run beyond the declared gate fields.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
