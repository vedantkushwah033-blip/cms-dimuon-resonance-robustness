#!/usr/bin/env python3
"""Compare candidate and ROOT-reference run metadata for a bounded baseline.

This checks event cut flow, histogram configuration, and mass-range accounting.
It does not validate trigger semantics, physics quality, or how ROOT handles
non-finite values in histogram flow bins.
"""
from __future__ import annotations

import argparse
import json
import math
import re
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
    """Return explicit checks for cut flow, configuration, and mass accounting."""
    checks: list[dict[str, Any]] = []

    def check_equal(name: str, candidate_value: Any, reference_value: Any) -> None:
        checks.append({
            "check": name,
            "candidate": candidate_value,
            "reference": reference_value,
            "passed": candidate_value == reference_value,
        })

    # Do not compare cut flows unless both outputs identify the same input bytes.
    sha_pattern = re.compile(r"^[0-9a-fA-F]{64}$")
    candidate_sha = candidate.get("input_sha256")
    reference_sha = reference.get("input_sha256")
    candidate_sha_valid = isinstance(candidate_sha, str) and sha_pattern.fullmatch(candidate_sha) is not None
    reference_sha_valid = isinstance(reference_sha, str) and sha_pattern.fullmatch(reference_sha) is not None
    checks.append({
        "check": "candidate_input_sha256_present_and_valid",
        "candidate": candidate_sha,
        "reference": "64 hexadecimal SHA-256 characters required",
        "passed": candidate_sha_valid,
    })
    checks.append({
        "check": "reference_input_sha256_present_and_valid",
        "candidate": reference_sha,
        "reference": "64 hexadecimal SHA-256 characters required",
        "passed": reference_sha_valid,
    })
    checks.append({
        "check": "input_sha256_matches",
        "candidate": candidate_sha.lower() if candidate_sha_valid else candidate_sha,
        "reference": reference_sha.lower() if reference_sha_valid else reference_sha,
        "passed": bool(candidate_sha_valid and reference_sha_valid and candidate_sha.lower() == reference_sha.lower()),
    })

    candidate_bytes = candidate.get("input_bytes")
    reference_bytes = reference.get("input_bytes")
    candidate_bytes_valid = isinstance(candidate_bytes, int) and not isinstance(candidate_bytes, bool) and candidate_bytes > 0
    reference_bytes_valid = isinstance(reference_bytes, int) and not isinstance(reference_bytes, bool) and reference_bytes > 0
    checks.append({
        "check": "candidate_input_bytes_present_and_valid",
        "candidate": candidate_bytes,
        "reference": "positive integer byte count required",
        "passed": candidate_bytes_valid,
    })
    checks.append({
        "check": "reference_input_bytes_present_and_valid",
        "candidate": reference_bytes,
        "reference": "positive integer byte count required",
        "passed": reference_bytes_valid,
    })
    checks.append({
        "check": "input_byte_count_matches",
        "candidate": candidate_bytes,
        "reference": reference_bytes,
        "passed": bool(candidate_bytes_valid and reference_bytes_valid and candidate_bytes == reference_bytes),
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
        ("candidate_pair_total_vs_reference_histogram_entries",
         "opposite_charge_pairs_total", "histogram_entries_including_flow"),
        ("candidate_pairs_below_range_vs_reference_underflow",
         "pairs_below_mass_range", "histogram_underflow"),
        ("candidate_pairs_in_range_vs_reference_regular_bins",
         "pairs_in_histogram_range", "histogram_regular_bin_total"),
        ("candidate_pairs_at_or_above_max_vs_reference_overflow",
         "pairs_at_or_above_mass_max", "histogram_overflow"),
        ("bin_count", "bins", "bins"),
        ("event_limit", "max_events", "max_events"),
    ]
    for name, candidate_key, reference_key in mappings:
        candidate_value = exact_nonnegative_int(candidate, candidate_key, "candidate")
        reference_value = exact_nonnegative_int(reference, reference_key, "reference")
        check_equal(name, candidate_value, reference_value)

    candidate_total = exact_nonnegative_int(candidate, "opposite_charge_pairs_total", "candidate")
    below = exact_nonnegative_int(candidate, "pairs_below_mass_range", "candidate")
    in_range = exact_nonnegative_int(candidate, "pairs_in_histogram_range", "candidate")
    above = exact_nonnegative_int(candidate, "pairs_at_or_above_mass_max", "candidate")
    nonfinite = exact_nonnegative_int(candidate, "pairs_nonfinite_mass", "candidate")
    checks.append({
        "check": "candidate_pair_accounting_reconciles",
        "candidate": below + in_range + above + nonfinite,
        "reference": candidate_total,
        "passed": below + in_range + above + nonfinite == candidate_total,
    })
    checks.append({
        "check": "candidate_nonfinite_mass_count_is_zero_for_flow_parity",
        "candidate": nonfinite,
        "reference": 0,
        "passed": nonfinite == 0,
        "note": (
            "Non-finite masses are counted separately by the candidate but ROOT "
            "flow-bin treatment is not validated; flow-bin parity is interpretable "
            "only when this count is zero."
        ),
    })

    selection = candidate.get("selection_mode")
    expected_reference_selection = ["nMuon == 2", "Muon_charge[0] != Muon_charge[1]"]
    checks.append({
        "check": "candidate_uses_exactly_two_opposite_charge_selection",
        "candidate": selection,
        "reference": expected_reference_selection,
        "passed": selection == "exactly-two-opposite-charge",
    })
    reference_selection = reference.get("selection")
    checks.append({
        "check": "reference_uses_expected_selection",
        "candidate": selection,
        "reference": reference_selection,
        "passed": reference_selection == expected_reference_selection,
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
        "input_provenance_agrees": all(
            item["passed"] for item in checks
            if item["check"].startswith(("candidate_input_", "reference_input_", "input_sha256_", "input_byte_count_"))
        ),
        "checks": checks,
        "interpretation": (
            "Event cut flow, histogram configuration, regular-bin totals, and flow-bin "
            "accounting agree; candidate non-finite mass count is zero."
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
    output_path = args.output.resolve()
    protected_inputs = {
        args.candidate.resolve(): "--candidate",
        args.reference.resolve(): "--reference",
    }
    if output_path in protected_inputs:
        parser.error(
            f"--output resolves to the same path as {protected_inputs[output_path]}; "
            "refusing to overwrite an input metadata file"
        )
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
