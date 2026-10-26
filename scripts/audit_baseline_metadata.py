#!/usr/bin/env python3
"""Audit end-to-end parity evidence from reference and candidate run metadata.

This supplements bin-by-bin histogram comparison with input identity, selection,
cut-flow, binning, and flow-count checks. A pass is evidence of software-level
reproduction only, not detector/trigger validation or a resonance discovery.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


def _boolean_matches(value: Any, expected: bool) -> bool:
    """Require a JSON boolean, not an integer that compares equal to it in Python."""
    return type(value) is bool and value is expected


def _finite_json_number(value: Any) -> bool:
    """Accept finite JSON integers/floats while excluding booleans and non-numeric values."""
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    return isinstance(value, float) and math.isfinite(value)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build a JSON object while rejecting ambiguous duplicate keys."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
    except (OSError, ValueError) as exc:
        raise ValueError(f"Cannot read unambiguous valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")
    return value


def audit(reference_path: Path, candidate_path: Path, histogram_report_path: Path) -> dict[str, Any]:
    ref = _read_json(reference_path)
    cand = _read_json(candidate_path)
    hist = _read_json(histogram_report_path)
    checks: list[dict[str, Any]] = []

    def check(name: str, reference: Any, candidate: Any, *, required: bool = True) -> None:
        if reference is None or candidate is None:
            passed = not required
            detail = "required value missing" if required else "optional value unavailable"
        else:
            passed = reference == candidate
            detail = "equal" if passed else "values differ"
        checks.append({
            "name": name,
            "passed": bool(passed),
            "reference": reference,
            "candidate": candidate,
            "detail": detail,
        })

    def check_nonempty_string(name: str, value: Any) -> None:
        valid = isinstance(value, str) and bool(value.strip())
        checks.append({
            "name": f"{name}_valid_nonempty_string",
            "passed": valid,
            "value": value,
            "detail": "non-empty string" if valid else "missing or invalid string value",
        })

    def check_boolean(name: str, expected: bool, actual: Any) -> None:
        passed = _boolean_matches(actual, expected)
        checks.append({
            "name": name,
            "passed": passed,
            "reference": expected,
            "candidate": actual,
            "detail": "strict JSON boolean matches expectation"
            if passed else "value must be a JSON boolean matching the expected value",
        })

    def nonnegative_integer(name: str, value: Any) -> None:
        valid = isinstance(value, int) and not isinstance(value, bool) and value >= 0
        checks.append({
            "name": f"{name}_valid_nonnegative_integer",
            "passed": valid,
            "value": value,
            "detail": "nonnegative integer" if valid else "missing or non-integer count",
        })

    def count_not_exceed(name: str, smaller: Any, larger: Any) -> None:
        valid_types = all(
            isinstance(value, int) and not isinstance(value, bool) and value >= 0
            for value in (smaller, larger)
        )
        passed = valid_types and smaller <= larger
        checks.append({
            "name": name,
            "passed": passed,
            "smaller_count": smaller,
            "larger_count": larger,
            "detail": "count ordering is valid"
            if passed else "counts must be nonnegative integers and smaller_count <= larger_count",
        })

    def finite_number(name: str, value: Any) -> None:
        valid = _finite_json_number(value)
        checks.append({
            "name": f"{name}_valid_finite_number",
            "passed": valid,
            "value": value,
            "detail": "finite numeric value" if valid else "missing or non-finite numeric value",
        })

    def positive_integer(name: str, value: Any) -> None:
        valid = isinstance(value, int) and not isinstance(value, bool) and value > 0
        checks.append({
            "name": f"{name}_valid_positive_integer",
            "passed": valid,
            "value": value,
            "detail": "positive integer" if valid else "missing or non-positive integer",
        })

    # Matching strings are not sufficient: provenance fields must also be well-formed.
    ref_digest = ref.get("input_sha256")
    cand_digest = cand.get("input_sha256")
    digest_valid = all(
        isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None
        for value in (ref_digest, cand_digest)
    )
    checks.append({
        "name": "input_sha256_format",
        "passed": digest_valid,
        "reference": ref_digest,
        "candidate": cand_digest,
        "detail": "both values are lowercase 64-character SHA-256 hex digests"
        if digest_valid else "missing or malformed SHA-256 digest",
    })
    check("input_sha256", ref_digest, cand_digest)
    ref_bytes = ref.get("input_bytes")
    cand_bytes = cand.get("input_bytes")
    sizes_valid = all(
        isinstance(value, int) and not isinstance(value, bool) and value > 0
        for value in (ref_bytes, cand_bytes)
    )
    checks.append({
        "name": "input_bytes_positive_integer",
        "passed": sizes_valid,
        "reference": ref_bytes,
        "candidate": cand_bytes,
        "detail": "both file sizes are positive integers"
        if sizes_valid else "missing or invalid file size",
    })
    check("input_bytes", ref_bytes, cand_bytes)
    check_nonempty_string("reference_tree_name", ref.get("tree"))
    check_nonempty_string("candidate_tree_name", cand.get("tree"))
    check("tree_name", ref.get("tree"), cand.get("tree"))
    # Counts in JSON must be integer counts, not booleans or floats that happen
    # to compare equal to integers (for example, 40.0 == 40 in Python).
    for name, value in (
        ("reference_events_total", ref.get("events_total")),
        ("reference_events_exactly_two_muons", ref.get("events_exactly_two_muons")),
        ("reference_events_opposite_sign", ref.get("events_opposite_sign")),
        ("reference_histogram_entries_including_flow", ref.get("histogram_entries_including_flow")),
        ("reference_histogram_regular_total", ref.get("histogram_regular_bin_total")),
        ("reference_underflow", ref.get("histogram_underflow")),
        ("reference_overflow", ref.get("histogram_overflow")),
        ("candidate_tree_entries", cand.get("tree_entries_available")),
        ("candidate_events_read", cand.get("events_read")),
        ("candidate_events_processed", cand.get("events_processed")),
        ("candidate_events_selected", cand.get("events_selected")),
        ("candidate_opposite_charge_pairs_total", cand.get("opposite_charge_pairs_total")),
        ("candidate_pairs_in_range", cand.get("pairs_in_histogram_range")),
        ("candidate_underflow", cand.get("pairs_below_mass_range")),
        ("candidate_overflow", cand.get("pairs_at_or_above_mass_max")),
        ("candidate_nonfinite_mass_pairs", cand.get("pairs_nonfinite_mass")),
        ("histogram_report_reference_total", hist.get("reference_total_count")),
        ("histogram_report_candidate_total", hist.get("candidate_total_count")),
        ("histogram_report_differing_bin_count", hist.get("differing_bin_count")),
        ("histogram_report_total_absolute_bin_count_difference", hist.get("total_absolute_bin_count_difference")),
        ("histogram_report_maximum_absolute_bin_count_difference", hist.get("maximum_absolute_bin_count_difference")),
    ):
        nonnegative_integer(name, value)
    positive_integer("reference_bins", ref.get("bins"))
    positive_integer("candidate_bins", cand.get("bins"))
    positive_integer("histogram_report_bin_count", hist.get("bin_count"))
    for name, value in (("reference_mass_min_GeV", ref.get("mass_min_GeV")),
                        ("reference_mass_max_GeV", ref.get("mass_max_GeV"))):
        finite_number(name, value)
    candidate_mass_range = cand.get("mass_range_GeV")
    candidate_range_valid = (
        isinstance(candidate_mass_range, list)
        and len(candidate_mass_range) == 2
        and all(
            _finite_json_number(value)
            for value in candidate_mass_range
        )
        and candidate_mass_range[0] > 0
        and candidate_mass_range[1] > candidate_mass_range[0]
    )
    checks.append({
        "name": "candidate_mass_range_valid",
        "passed": candidate_range_valid,
        "value": candidate_mass_range,
        "detail": "two finite numeric bounds with 0 < minimum < maximum"
        if candidate_range_valid else "invalid candidate mass-range schema or ordering",
    })
    reference_min = ref.get("mass_min_GeV")
    reference_max = ref.get("mass_max_GeV")
    reference_range_valid = (
        _finite_json_number(reference_min)
        and _finite_json_number(reference_max)
        and 0 < reference_min < reference_max
    )
    checks.append({
        "name": "reference_mass_range_valid",
        "passed": reference_range_valid,
        "value": [reference_min, reference_max],
        "detail": "finite numeric bounds with 0 < minimum < maximum"
        if reference_range_valid else "invalid reference mass-range schema or ordering",
    })
    count_not_exceed(
        "reference_exactly_two_events_within_total",
        ref.get("events_exactly_two_muons"), ref.get("events_total"),
    )
    count_not_exceed(
        "reference_opposite_sign_events_within_exactly_two",
        ref.get("events_opposite_sign"), ref.get("events_exactly_two_muons"),
    )
    count_not_exceed(
        "candidate_selected_events_within_read_events",
        cand.get("events_selected"), cand.get("events_read"),
    )
    count_not_exceed(
        "candidate_pairs_within_selected_events",
        cand.get("opposite_charge_pairs_total"), cand.get("events_selected"),
    )
    check("available_tree_entries", ref.get("events_total"), cand.get("tree_entries_available"))
    check("full_dataset_events_read", ref.get("events_total"), cand.get("events_read"))
    check("events_read_processed_consistency", cand.get("events_read"), cand.get("events_processed"))
    max_events = cand.get("max_events")
    reference_event_total = ref.get("events_total")
    reference_total_valid = (
        isinstance(reference_event_total, int)
        and not isinstance(reference_event_total, bool)
        and reference_event_total >= 0
    )
    full_run_limit_valid = max_events is None or (
        reference_total_valid
        and isinstance(max_events, int)
        and not isinstance(max_events, bool)
        and max_events >= reference_event_total
    )
    checks.append({
        "name": "full_dataset_event_limit",
        "passed": full_run_limit_valid,
        "value": max_events,
        "detail": "no event cap or cap at least as large as full reference dataset"
        if full_run_limit_valid else "partial-run event cap is not acceptable for full-data parity",
    })

    # The candidate must use the reference-aligned selection, not merely
    # happen to produce a similar selected-event count under another mode.
    check(
        "selection_mode",
        "exactly-two-opposite-charge",
        cand.get("selection_mode"),
    )
    check("exactly_two_muon_events", ref.get("events_exactly_two_muons"), cand.get("events_selected"))
    # With exactly two muons per selected event, every opposite-sign event
    # contributes exactly one opposite-charge pair, independent of its mass.
    check(
        "reference_opposite_sign_histogram_entries",
        ref.get("events_opposite_sign"),
        ref.get("histogram_entries_including_flow"),
    )

    # ROOT's GetEntries counts fills, while regular/underflow/overflow bins
    # account for where those fills landed. These are distinct metadata paths;
    # require both the fill count and the bin-content conservation identity.
    reference_flow_keys = (
        "histogram_regular_bin_total",
        "histogram_underflow",
        "histogram_overflow",
        "histogram_entries_including_flow",
    )
    reference_flow_values = [ref.get(key) for key in reference_flow_keys]
    reference_flow_types_valid = all(
        isinstance(value, int) and not isinstance(value, bool) and value >= 0
        for value in reference_flow_values
    )
    reference_flow_sum = (
        sum(reference_flow_values[:3]) if reference_flow_types_valid else None
    )
    reference_flow_conserved = (
        reference_flow_types_valid
        and reference_flow_sum == ref.get("histogram_entries_including_flow")
    )
    checks.append({
        "name": "reference_histogram_flow_count_conservation",
        "passed": reference_flow_conserved,
        "reference": {
            "regular_bins_plus_underflow_plus_overflow": reference_flow_sum,
            "histogram_entries_including_flow": ref.get("histogram_entries_including_flow"),
        },
        "detail": "regular-bin, underflow, and overflow counts sum to histogram entries"
        if reference_flow_conserved else
        "reference histogram counts must be nonnegative integer counts and conserve all entries",
    })
    check(
        "opposite_sign_event_pair_accounting",
        ref.get("events_opposite_sign"),
        cand.get("opposite_charge_pairs_total"),
    )
    check("bin_count", ref.get("bins"), cand.get("bins"))
    check(
        "mass_range_GeV",
        [ref.get("mass_min_GeV"), ref.get("mass_max_GeV")],
        cand.get("mass_range_GeV"),
    )
    check("regular_bin_total", ref.get("histogram_regular_bin_total"), cand.get("pairs_in_histogram_range"))
    check("underflow_count", ref.get("histogram_underflow"), cand.get("pairs_below_mass_range"))
    check("overflow_count", ref.get("histogram_overflow"), cand.get("pairs_at_or_above_mass_max"))
    accounting_fields_valid = all(
        isinstance(cand.get(key), int) and not isinstance(cand.get(key), bool) and cand.get(key) >= 0
        for key in (
            "pairs_in_histogram_range", "pairs_below_mass_range",
            "pairs_at_or_above_mass_max", "pairs_nonfinite_mass",
            "opposite_charge_pairs_total",
        )
    )
    candidate_pair_accounting = (
        sum(
            cand[key]
            for key in (
                "pairs_in_histogram_range", "pairs_below_mass_range",
                "pairs_at_or_above_mass_max", "pairs_nonfinite_mass",
            )
        )
        if accounting_fields_valid else None
    )
    accounting_passed = (
        accounting_fields_valid
        and candidate_pair_accounting == cand.get("opposite_charge_pairs_total")
    )
    checks.append({
        "name": "candidate_pair_accounting_conservation",
        "passed": accounting_passed,
        "candidate": {
            "opposite_charge_pairs_total": cand.get("opposite_charge_pairs_total"),
            "accounted_pairs_total": candidate_pair_accounting,
        },
        "detail": "in-range, underflow, overflow, and non-finite pairs sum to total pairs"
        if accounting_passed else "pair categories are invalid or do not sum to the total",
    })

    check_boolean("histogram_bin_edges_exactly_equal", True, hist.get("bin_edges_exactly_equal"))
    check_boolean("histogram_exact_bin_by_bin_parity", True, hist.get("exact_bin_by_bin_parity"))

    # Do not trust a parity boolean alone: cross-check the comparator's
    # discrepancy summary so a stale, hand-edited, or internally inconsistent
    # report cannot pass while claiming nonzero bin differences.
    check("histogram_differing_bin_count_zero", 0, hist.get("differing_bin_count"))
    check(
        "histogram_total_absolute_bin_count_difference_zero",
        0,
        hist.get("total_absolute_bin_count_difference"),
    )
    check(
        "histogram_maximum_absolute_bin_count_difference_zero",
        0,
        hist.get("maximum_absolute_bin_count_difference"),
    )

    differing_bins = hist.get("differing_bins")
    differing_bin_count = hist.get("differing_bin_count")
    discrepancy_list_valid = (
        isinstance(differing_bins, list)
        and all(isinstance(item, dict) for item in differing_bins)
        and isinstance(differing_bin_count, int)
        and not isinstance(differing_bin_count, bool)
        and differing_bin_count >= 0
        and len(differing_bins) == differing_bin_count
    )
    checks.append({
        "name": "histogram_discrepancy_list_consistent",
        "passed": discrepancy_list_valid,
        "reference": {
            "differing_bin_count": differing_bin_count,
            "differing_bins_length": (
                len(differing_bins) if isinstance(differing_bins, list) else None
            ),
        },
        "detail": "differing-bin list length matches the strict integer discrepancy count"
        if discrepancy_list_valid else
        "differing_bins must be a list of objects whose length equals differing_bin_count",
    })
    check("histogram_bin_count", ref.get("bins"), hist.get("bin_count"))
    check("histogram_regular_total", ref.get("histogram_regular_bin_total"), hist.get("reference_total_count"))
    check("candidate_regular_total", cand.get("pairs_in_histogram_range"), hist.get("candidate_total_count"))

    passed = all(item["passed"] for item in checks)
    return {
        "status": "PASS" if passed else "FAIL",
        "software_reference_reproduction_only": True,
        "checks_passed": sum(item["passed"] for item in checks),
        "checks_total": len(checks),
        "checks": checks,
        "limitations": [
            "This audit does not establish trigger efficiency, detector-level validity, or physics discovery.",
            "A failed check must be explained; do not relax exact parity silently.",
            "Input SHA-256 must be present in both metadata files and match.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-metadata", type=Path, required=True)
    parser.add_argument("--candidate-metadata", type=Path, required=True)
    parser.add_argument("--histogram-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = audit(args.reference_metadata, args.candidate_metadata, args.histogram_report)
    except ValueError as exc:
        # Invalid input must fail closed, but still leave a machine-readable
        # artifact for CI and downstream review instead of a traceback only.
        report = {
            "status": "FAIL",
            "software_reference_reproduction_only": True,
            "checks_passed": 0,
            "checks_total": 0,
            "checks": [],
            "error": str(exc),
            "limitations": [
                "The audit could not evaluate malformed or ambiguous metadata.",
                "A failed audit is not evidence of real-data parity.",
            ],
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "checks"}, indent=2))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
