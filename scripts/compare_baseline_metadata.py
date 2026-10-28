#!/usr/bin/env python3
"""Compare candidate and ROOT-reference run metadata for a bounded baseline.

This checks event cut flow, histogram configuration, and mass-range accounting.
It does not validate trigger semantics, physics quality, or how ROOT handles
non-finite values in histogram flow bins.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
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


def histogram_csv_summary(path: Path) -> dict[str, Any]:
    """Return the bin count and exact integer total of a histogram CSV."""
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"mass_low_GeV", "mass_high_GeV", "pair_count"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path}: required CSV columns are {sorted(required)}")
        rows = list(reader)
    total = 0
    for line_number, row in enumerate(rows, start=2):
        value = row.get("pair_count")
        if value is None or re.fullmatch(r"[0-9]+", value) is None:
            raise ValueError(f"{path}: line {line_number}: pair_count must be an unsigned integer string")
        total += int(value, 10)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"bins": len(rows), "total": total, "sha256": digest}


def compare(
    candidate: dict[str, Any],
    reference: dict[str, Any],
    expected_sha256: str | None = None,
    expected_bytes: int | None = None,
    candidate_csv: dict[str, Any] | None = None,
    reference_csv: dict[str, Any] | None = None,
    expected_max_events: int | None = None,
) -> dict[str, Any]:
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

    if expected_sha256 is not None:
        expected_sha_valid = isinstance(expected_sha256, str) and sha_pattern.fullmatch(expected_sha256) is not None
        checks.append({
            "check": "expected_manifest_sha256_present_and_valid",
            "candidate": expected_sha256,
            "reference": "64 hexadecimal SHA-256 characters required",
            "passed": expected_sha_valid,
        })
        checks.append({
            "check": "candidate_sha256_matches_manifest",
            "candidate": candidate_sha.lower() if candidate_sha_valid else candidate_sha,
            "reference": expected_sha256.lower() if expected_sha_valid else expected_sha256,
            "passed": bool(expected_sha_valid and candidate_sha_valid and candidate_sha.lower() == expected_sha256.lower()),
        })
        checks.append({
            "check": "reference_sha256_matches_manifest",
            "candidate": reference_sha.lower() if reference_sha_valid else reference_sha,
            "reference": expected_sha256.lower() if expected_sha_valid else expected_sha256,
            "passed": bool(expected_sha_valid and reference_sha_valid and reference_sha.lower() == expected_sha256.lower()),
        })

    if expected_bytes is not None:
        expected_bytes_valid = isinstance(expected_bytes, int) and not isinstance(expected_bytes, bool) and expected_bytes > 0
        checks.append({
            "check": "expected_manifest_input_bytes_present_and_valid",
            "candidate": expected_bytes,
            "reference": "positive integer byte count required",
            "passed": expected_bytes_valid,
        })
        checks.append({
            "check": "candidate_input_bytes_match_manifest",
            "candidate": candidate_bytes,
            "reference": expected_bytes,
            "passed": bool(expected_bytes_valid and candidate_bytes_valid and candidate_bytes == expected_bytes),
        })
        checks.append({
            "check": "reference_input_bytes_match_manifest",
            "candidate": reference_bytes,
            "reference": expected_bytes,
            "passed": bool(expected_bytes_valid and reference_bytes_valid and reference_bytes == expected_bytes),
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

    # Bind each histogram summary to the metadata from the same exporter.
    for label, meta, csv_summary, total_key in (
        ("candidate", candidate, candidate_csv, "pairs_in_histogram_range"),
        ("reference", reference, reference_csv, "histogram_regular_bin_total"),
    ):
        if csv_summary is None:
            continue
        meta_bins, meta_total = meta.get("bins"), meta.get(total_key)
        valid_bins = isinstance(meta_bins, int) and not isinstance(meta_bins, bool) and meta_bins >= 0
        valid_total = isinstance(meta_total, int) and not isinstance(meta_total, bool) and meta_total >= 0
        checks.append({
            "check": f"{label}_csv_bin_count_matches_metadata",
            "candidate": csv_summary["bins"], "reference": meta_bins,
            "passed": bool(valid_bins and csv_summary["bins"] == meta_bins),
        })
        checks.append({
            "check": f"{label}_csv_total_matches_metadata_in_range_count",
            "candidate": csv_summary["total"], "reference": meta_total,
            "passed": bool(valid_total and csv_summary["total"] == meta_total),
        })

        metadata_csv_sha = meta.get("histogram_csv_sha256")
        metadata_csv_sha_valid = isinstance(metadata_csv_sha, str) and re.fullmatch(r"[0-9a-fA-F]{64}", metadata_csv_sha) is not None
        checks.append({
            "check": f"{label}_csv_sha256_present_and_valid_in_metadata",
            "candidate": metadata_csv_sha,
            "reference": "64 hexadecimal SHA-256 characters required",
            "passed": metadata_csv_sha_valid,
        })
        checks.append({
            "check": f"{label}_csv_sha256_matches_metadata",
            "candidate": csv_summary.get("sha256"),
            "reference": metadata_csv_sha.lower() if metadata_csv_sha_valid else metadata_csv_sha,
            "passed": bool(metadata_csv_sha_valid and csv_summary.get("sha256") == metadata_csv_sha.lower()),
        })

    if expected_max_events is not None:
        valid_limit = isinstance(expected_max_events, int) and not isinstance(expected_max_events, bool) and expected_max_events > 0
        for label, meta, read_key in (("candidate", candidate, "events_read"), ("reference", reference, "events_total")):
            for key in ("max_events", read_key):
                value = meta.get(key)
                checks.append({
                    "check": f"{label}_{key}_equals_expected_event_prefix",
                    "candidate": value, "reference": expected_max_events,
                    "passed": bool(valid_limit and isinstance(value, int) and not isinstance(value, bool)
                                   and value == expected_max_events),
                })

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

    provenance_checks = [
        item for item in checks
        if item["check"].startswith((
            "candidate_input_", "reference_input_", "input_sha256_", "input_byte_count_",
            "expected_manifest_", "candidate_sha256_matches_manifest",
            "reference_sha256_matches_manifest", "candidate_input_bytes_match_manifest",
            "reference_input_bytes_match_manifest"
        ))
    ]
    non_provenance_checks = [item for item in checks if item not in provenance_checks]
    passed = all(item["passed"] for item in checks)
    return {
        "candidate_metadata": "candidate",
        "reference_metadata": "reference",
        "check_count": len(checks),
        "failed_check_count": sum(not item["passed"] for item in checks),
        "cutflow_and_configuration_agree": all(item["passed"] for item in non_provenance_checks),
        "input_provenance_agrees": all(item["passed"] for item in provenance_checks),
        "comparison_passed": passed,
        "checks": checks,
        "interpretation": (
            "Cut flow, configuration, mass accounting, and input provenance all agree; "
            "candidate non-finite mass count is zero."
            if passed else
            "Metadata comparison failed; inspect every failed check before interpreting histogram parity."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--expected-sha256", help="Expected SHA-256 from the downloaded-input manifest")
    parser.add_argument("--expected-bytes", type=int, help="Expected input byte count from the downloaded-input manifest")
    parser.add_argument("--candidate-csv", type=Path, help="Candidate histogram CSV to bind to candidate metadata")
    parser.add_argument("--reference-csv", type=Path, help="Reference histogram CSV to bind to reference metadata")
    parser.add_argument("--expected-max-events", type=int, help="Intended event prefix; both outputs must have read exactly this many events")
    args = parser.parse_args()
    if (args.candidate_csv is None) != (args.reference_csv is None):
        parser.error("--candidate-csv and --reference-csv must be supplied together")
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
        report = compare(
            load_json(args.candidate),
            load_json(args.reference),
            expected_sha256=args.expected_sha256,
            expected_bytes=args.expected_bytes,
            candidate_csv=histogram_csv_summary(args.candidate_csv) if args.candidate_csv else None,
            reference_csv=histogram_csv_summary(args.reference_csv) if args.reference_csv else None,
            expected_max_events=args.expected_max_events,
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        report = {
            "cutflow_and_configuration_agree": False,
            "input_provenance_agrees": False,
            "comparison_passed": False,
            "comparison_error": str(exc),
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report.get("comparison_passed", False) else 2


if __name__ == "__main__":
    raise SystemExit(main())
