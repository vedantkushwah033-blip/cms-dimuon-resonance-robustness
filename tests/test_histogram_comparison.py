import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPARATOR = REPO_ROOT / "scripts" / "compare_histograms.py"
FIELDS = ["mass_low_GeV", "mass_high_GeV", "pair_count"]


def write_histogram(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def run_comparison(tmp_path, reference_rows, candidate_rows):
    reference = tmp_path / "reference.csv"
    candidate = tmp_path / "candidate.csv"
    report = tmp_path / "comparison.json"
    write_histogram(reference, reference_rows)
    write_histogram(candidate, candidate_rows)
    result = subprocess.run(
        [
            sys.executable,
            str(COMPARATOR),
            "--reference",
            str(reference),
            "--candidate",
            str(candidate),
            "--output",
            str(report),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result, report


def test_exact_histogram_parity_exits_zero_and_writes_report(tmp_path):
    rows = [
        {"mass_low_GeV": 0.25, "mass_high_GeV": 1.0, "pair_count": 3},
        {"mass_low_GeV": 1.0, "mass_high_GeV": 2.0, "pair_count": 0},
    ]
    result, report_path = run_comparison(tmp_path, rows, rows)
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 0, result.stderr
    assert report["exact_bin_by_bin_parity"] is True
    assert report["differing_bin_count"] == 0
    assert report["reference_total_count"] == 3
    assert report["candidate_total_count"] == 3


def test_count_discrepancy_exits_two_and_lists_affected_interval(tmp_path):
    reference = [
        {"mass_low_GeV": 0.25, "mass_high_GeV": 1.0, "pair_count": 3},
        {"mass_low_GeV": 1.0, "mass_high_GeV": 2.0, "pair_count": 0},
    ]
    candidate = [
        {"mass_low_GeV": 0.25, "mass_high_GeV": 1.0, "pair_count": 2},
        {"mass_low_GeV": 1.0, "mass_high_GeV": 2.0, "pair_count": 1},
    ]
    result, report_path = run_comparison(tmp_path, reference, candidate)
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    assert report["exact_bin_by_bin_parity"] is False
    assert report["differing_bin_count"] == 2
    assert report["total_absolute_bin_count_difference"] == 2
    assert report["maximum_absolute_bin_count_difference"] == 1
    assert [row["bin_index"] for row in report["differing_bins"]] == [0, 1]


def test_different_bin_edges_fail_closed(tmp_path):
    reference = [{"mass_low_GeV": 0.25, "mass_high_GeV": 1.0, "pair_count": 3}]
    candidate = [{"mass_low_GeV": 0.25, "mass_high_GeV": 1.1, "pair_count": 3}]
    result, _ = run_comparison(tmp_path, reference, candidate)

    assert result.returncode != 0
    assert "histogram bin edges differ" in result.stderr


@pytest.mark.parametrize("bad_count", [-1, 1.5, "nan", "3.0"])
def test_invalid_counts_are_rejected(tmp_path, bad_count):
    reference = [{"mass_low_GeV": 0.25, "mass_high_GeV": 1.0, "pair_count": 1}]
    candidate = [{"mass_low_GeV": 0.25, "mass_high_GeV": 1.0, "pair_count": bad_count}]
    result, _ = run_comparison(tmp_path, reference, candidate)

    assert result.returncode != 0
    assert "pair_count values must be exact base-10 integers" in result.stderr or "counts must be nonnegative integers" in result.stderr


def test_counts_above_float_exactness_limit_are_compared_without_precision_loss(tmp_path):
    reference = [{"mass_low_GeV": 0.25, "mass_high_GeV": 1.0, "pair_count": "9007199254740993"}]
    candidate = [{"mass_low_GeV": 0.25, "mass_high_GeV": 1.0, "pair_count": "9007199254740994"}]
    result, report_path = run_comparison(tmp_path, reference, candidate)
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    assert report["reference_total_count"] == 9007199254740993
    assert report["candidate_total_count"] == 9007199254740994
    assert report["total_absolute_bin_count_difference"] == 1
    assert report["maximum_absolute_bin_count_difference"] == 1
