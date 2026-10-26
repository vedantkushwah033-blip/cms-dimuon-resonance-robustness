#!/usr/bin/env python3
"""Compare two dimuon histogram CSVs with strict bin-edge and count checks.

Both inputs must contain mass_low_GeV,mass_high_GeV,pair_count columns.
Writes a machine-readable JSON report and exits 0 only for exact bin-by-bin parity.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

COLUMNS = ("mass_low_GeV", "mass_high_GeV", "pair_count")


def load_histogram(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Load and validate bin edges and nonnegative integer counts from a CSV."""
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not set(COLUMNS).issubset(reader.fieldnames):
            raise ValueError(f"{path}: required CSV columns are {', '.join(COLUMNS)}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{path}: histogram has no bins")
    try:
        lows = np.asarray([float(row["mass_low_GeV"]) for row in rows], dtype=np.float64)
        highs = np.asarray([float(row["mass_high_GeV"]) for row in rows], dtype=np.float64)
        raw_counts = [float(row["pair_count"]) for row in rows]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{path}: bin edges and counts must be numeric") from exc
    counts_as_float = np.asarray(raw_counts, dtype=np.float64)
    if not np.all(np.isfinite(lows)) or not np.all(np.isfinite(highs)):
        raise ValueError(f"{path}: bin edges must be finite")
    if np.any(highs <= lows):
        raise ValueError(f"{path}: every bin must have high edge greater than low edge")
    if len(lows) > 1 and not np.array_equal(highs[:-1], lows[1:]):
        raise ValueError(f"{path}: bins must be contiguous and ordered")
    if not np.all(np.isfinite(counts_as_float)) or np.any(counts_as_float < 0):
        raise ValueError(f"{path}: counts must be finite and nonnegative")
    if not np.all(counts_as_float == np.floor(counts_as_float)):
        raise ValueError(f"{path}: pair_count values must be integers")
    return lows, highs, counts_as_float.astype(np.int64)


def compare(reference_path: Path, candidate_path: Path) -> dict:
    """Compare histograms and summarize exact discrepancies."""
    ref_low, ref_high, ref_counts = load_histogram(reference_path)
    cand_low, cand_high, cand_counts = load_histogram(candidate_path)
    if ref_counts.shape != cand_counts.shape:
        raise ValueError(
            f"histogram bin-count differs: reference={len(ref_counts)}, "
            f"candidate={len(cand_counts)}"
        )
    if not np.array_equal(ref_low, cand_low) or not np.array_equal(ref_high, cand_high):
        low_mismatch = np.flatnonzero(ref_low != cand_low)
        high_mismatch = np.flatnonzero(ref_high != cand_high)
        first = min(
            [int(i) for i in low_mismatch] + [int(i) for i in high_mismatch],
            default=-1,
        )
        raise ValueError(f"histogram bin edges differ; first mismatching bin index={first}")
    delta = cand_counts - ref_counts
    differing = np.flatnonzero(delta != 0)
    intervals = [
        {
            "bin_index": int(i),
            "mass_low_GeV": float(ref_low[i]),
            "mass_high_GeV": float(ref_high[i]),
            "reference_count": int(ref_counts[i]),
            "candidate_count": int(cand_counts[i]),
            "candidate_minus_reference": int(delta[i]),
        }
        for i in differing
    ]
    return {
        "reference_csv": str(reference_path),
        "candidate_csv": str(candidate_path),
        "bin_count": int(len(ref_counts)),
        "bin_edges_exactly_equal": True,
        "reference_total_count": int(ref_counts.sum()),
        "candidate_total_count": int(cand_counts.sum()),
        "total_absolute_bin_count_difference": int(np.abs(delta).sum()),
        "maximum_absolute_bin_count_difference": int(np.abs(delta).max(initial=0)),
        "differing_bin_count": int(len(differing)),
        "exact_bin_by_bin_parity": bool(len(differing) == 0),
        "differing_bins": intervals,
        "interpretation": (
            "Exact integer parity across all bins."
            if len(differing) == 0
            else "Parity not established; investigate every listed discrepancy."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=Path, help="Reference histogram CSV")
    parser.add_argument("--candidate", required=True, type=Path, help="Candidate histogram CSV")
    parser.add_argument("--output", required=True, type=Path, help="Path for JSON comparison report")
    args = parser.parse_args()
    report = compare(args.reference, args.candidate)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "differing_bins"}, indent=2))
    return 0 if report["exact_bin_by_bin_parity"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
