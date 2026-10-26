#!/usr/bin/env python3
"""Compare two dimuon histogram CSVs with strict bin-edge and count checks.

Both inputs must contain mass_low_GeV,mass_high_GeV,pair_count columns.
Writes a machine-readable JSON report and exits 0 only for exact bin-by-bin parity.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np

COLUMNS = ("mass_low_GeV", "mass_high_GeV", "pair_count")
# ROOT and NumPy can construct mathematically identical uniform edges with
# slightly different last-bit rounding. This tolerance is tiny relative to
# the 0.00999 GeV bins and does not permit a physically meaningful rebinning.
BIN_EDGE_ATOL_GEV = 1e-12


def load_histogram(path: Path) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """Load and validate bin edges and exact nonnegative integer counts from CSV."""
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not set(COLUMNS).issubset(reader.fieldnames):
            raise ValueError(f"{path}: required CSV columns are {', '.join(COLUMNS)}")
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError(f"{path}: duplicate CSV column names are not allowed")
        rows = list(reader)
        for line_number, row in enumerate(rows, start=2):
            if None in row or any(row[column] is None for column in COLUMNS):
                raise ValueError(
                    f"{path}: malformed CSV row at line {line_number}; "
                    "field count does not match header"
                )
    if not rows:
        raise ValueError(f"{path}: histogram has no bins")
    try:
        lows = np.asarray([float(row["mass_low_GeV"]) for row in rows], dtype=np.float64)
        highs = np.asarray([float(row["mass_high_GeV"]) for row in rows], dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{path}: bin edges must be numeric") from exc
    try:
        # Parse counts as Python integers, never via float: float loses unit
        # precision above 2**53, which is unacceptable for exact parity checks.
        raw_counts = [row["pair_count"] for row in rows]
        if any(value is None or re.fullmatch(r"[0-9]+", value) is None for value in raw_counts):
            raise ValueError("pair_count values must be unsigned base-10 integer strings")
        counts = [int(value, 10) for value in raw_counts]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{path}: pair_count values must be exact base-10 integers") from exc
    if not np.all(np.isfinite(lows)) or not np.all(np.isfinite(highs)):
        raise ValueError(f"{path}: bin edges must be finite")
    if np.any(highs <= lows):
        raise ValueError(f"{path}: every bin must have high edge greater than low edge")
    if len(lows) > 1 and not np.allclose(
        highs[:-1], lows[1:], rtol=0.0, atol=BIN_EDGE_ATOL_GEV
    ):
        max_gap = float(np.max(np.abs(highs[:-1] - lows[1:])))
        raise ValueError(
            f"{path}: bins must be contiguous and ordered within "
            f"{BIN_EDGE_ATOL_GEV:g} GeV; maximum adjacent-edge mismatch="
            f"{max_gap:.17g} GeV"
        )
    if any(count < 0 for count in counts):
        raise ValueError(f"{path}: counts must be nonnegative integers")
    return lows, highs, counts


def compare(reference_path: Path, candidate_path: Path) -> dict:
    """Compare histograms and summarize exact discrepancies."""
    ref_low, ref_high, ref_counts = load_histogram(reference_path)
    cand_low, cand_high, cand_counts = load_histogram(candidate_path)
    if len(ref_counts) != len(cand_counts):
        raise ValueError(
            f"histogram bin-count differs: reference={len(ref_counts)}, "
            f"candidate={len(cand_counts)}"
        )
    low_difference = np.abs(ref_low - cand_low)
    high_difference = np.abs(ref_high - cand_high)
    max_edge_difference = float(max(np.max(low_difference), np.max(high_difference)))
    if not np.allclose(ref_low, cand_low, rtol=0.0, atol=BIN_EDGE_ATOL_GEV) or not np.allclose(
        ref_high, cand_high, rtol=0.0, atol=BIN_EDGE_ATOL_GEV
    ):
        low_mismatch = np.flatnonzero(low_difference > BIN_EDGE_ATOL_GEV)
        high_mismatch = np.flatnonzero(high_difference > BIN_EDGE_ATOL_GEV)
        first = min(
            [int(i) for i in low_mismatch] + [int(i) for i in high_mismatch],
            default=-1,
        )
        raise ValueError(
            "histogram bin edges differ beyond tolerance "
            f"{BIN_EDGE_ATOL_GEV:g} GeV; first mismatching bin index={first}, "
            f"maximum absolute edge difference={max_edge_difference:.17g} GeV"
        )
    delta = [candidate - reference for reference, candidate in zip(ref_counts, cand_counts)]
    differing = [i for i, difference in enumerate(delta) if difference != 0]
    intervals = [
        {
            "bin_index": i,
            "mass_low_GeV": float(ref_low[i]),
            "mass_high_GeV": float(ref_high[i]),
            "reference_count": ref_counts[i],
            "candidate_count": cand_counts[i],
            "candidate_minus_reference": delta[i],
        }
        for i in differing
    ]
    return {
        "reference_csv": str(reference_path),
        "candidate_csv": str(candidate_path),
        "bin_count": len(ref_counts),
        "bin_edges_compatible_within_tolerance": True,
        "bin_edge_absolute_tolerance_GeV": BIN_EDGE_ATOL_GEV,
        "maximum_absolute_bin_edge_difference_GeV": max_edge_difference,
        "reference_total_count": sum(ref_counts),
        "candidate_total_count": sum(cand_counts),
        "total_absolute_bin_count_difference": sum(abs(value) for value in delta),
        "maximum_absolute_bin_count_difference": max((abs(value) for value in delta), default=0),
        "differing_bin_count": len(differing),
        "exact_bin_by_bin_parity": len(differing) == 0,
        "differing_bins": intervals,
        "interpretation": (
            "Exact integer parity across all bins."
            if not differing
            else "Parity not established; investigate every listed discrepancy."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=Path, help="Reference histogram CSV")
    parser.add_argument("--candidate", required=True, type=Path, help="Candidate histogram CSV")
    parser.add_argument("--output", required=True, type=Path, help="Path for JSON comparison report")
    args = parser.parse_args()
    output_path = args.output.resolve()
    protected_inputs = {
        args.reference.resolve(): "--reference",
        args.candidate.resolve(): "--candidate",
    }
    if output_path in protected_inputs:
        parser.error(
            f"--output resolves to the same path as {protected_inputs[output_path]}; "
            "refusing to overwrite an input histogram"
        )
    try:
        report = compare(args.reference, args.candidate)
    except (OSError, ValueError) as exc:
        # Keep machine-readable failure evidence for CI artifacts, including
        # incompatible bin edges or malformed input CSVs.
        report = {
            "reference_csv": str(args.reference),
            "candidate_csv": str(args.candidate),
            "exact_bin_by_bin_parity": False,
            "comparison_error": str(exc),
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        print(f"comparison failed: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "differing_bins"}, indent=2))
    return 0 if report["exact_bin_by_bin_parity"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
