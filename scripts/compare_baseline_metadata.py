#!/usr/bin/env python3
"""Compare candidate and ROOT-reference run metadata for a bounded baseline.

This checks selection cut flow and common histogram configuration. It does not
validate trigger semantics, physics quality, or non-finite ROOT flow-bin behavior.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

EDGE_ATOL_GEV = 1e-12


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object and reject non-object roots."""
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: metadata JSON root must be an object")
    return value


def exact_nonnegative_int(metadata: dict[str, Any], key: str, source: str) -> int:
    """Read an exact nonnegative integer metadata field, rejecting bool/float."""
    value = metadata.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{source}: {key} must be a nonnegative integer")
    return value


def compare(candidate: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    """Return explicit checks for common event cut flow and histogram settings."""
    checks: list[dict[str, Any]] = []

    def check_equal(name: str, candidate_value: Any, reference_value: Any) -> None:
        checks.append({
            "check": name,
            "candidate": candidate_value,
            "reference": reference_value,
            "passed": candidate_value == reference_value,
        })

    mappings = [
        ("events_read_vs_events_total", "events_read", "events_total"),
        ("events_selected_vs_exactly_two_muons", "events_selected", "events_exactly_two_muons"),
        (
            "events_with_opposite_charge_pair_vs_opposite_sign",
            "events_with_opposite_charge_pair",
            "events_opposite_sign",
        ),
        ("candidate_pair_total_vs_reference_opposite_sign_events",
         "opposite_charge_pairs_total", "events_opposite_sign"),
        ("bin_count", "bins", "bins"),
        ("event_limit", "max_events", "max_events"),
    ]
    for name, candidate_key, reference_key in mappings:
        candidate_value = candidate.get(candidate_key)
        reference_value = reference.get(reference_key)
        if candidate_key != "max_events":
            candidate_value = exact_nonnegative_int(candidate, candidate_key, "candidate")
            reference_value = exact_nonnegative_int(reference, reference_key, "reference")
        check_equal(name, candidate_value, reference_value)

    selection = candidate.get("selection_mode")
    checks.append({
        "check": "candidate_uses_exactly_two_opposite_charge_selection",
        "candidate": selection,
        "reference": ["nMuon == 2", "Muon_charge[0] != Muon_charge[1]"],
        "passed": selection == "exactly-two-opposite-charge",
    })
    candidate_range = candidate.get("mass_range_GeV")
    reference_range = [reference.get("mass_min_GeV"), reference.get("mass_max_GeV")]
    valid_ranges = (
        isinstance(candidate_range, list)
        and len(candidate_range) == 2
        and all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
                for x in candidate_range)
        and all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
                for x in reference_range)
    )
    range_passed = bool(
        valid_ranges
        and math.isclose(candidate_range[0], reference_range[0], rel_tol=0.0, abs_tol=EDGE_ATOL_GEV)
        and math.isclose(candidate_range[1], reference_range[1], rel_tol=0.0, abs_tol=EDGE_ATOL_GEV)
    )
    checks.append({
        "check": "mass_range_matches_within_tolerance",
        "candidate": candidate_range,
        "reference": reference_range,
        "absolute_tolerance_GeV": EDGE_ATOL_GEV,
        "passed": range_passed,
    })

    passed = all(item["passed"] for item in checks)
    return {
        "candidate_metadata": "candidate",
        "reference_metadata": "reference",
        "check_count": len(checks),
        "failed_check_count": sum(not item["passed"] for item in checks),
        "cutflow_and_configuration_agree": passed,
        "checks": checks,
        "interpretation": (
            "Common event cut flow and histogram configuration agree."
            if passed else
            "Metadata comparison failed; inspect every failed check before interpreting histogram parity."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = compare(load_json(args.candidate), load_json(args.reference))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        report = {
            "cutflow_and_configuration_agree": False,
            "comparison_error": str(exc),
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["cutflow_and_configuration_agree"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
