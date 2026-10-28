import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.compare_baseline_metadata import compare, histogram_csv_summary
from tests.test_compare_baseline_metadata import candidate_metadata, reference_metadata

COMPARATOR = Path(__file__).resolve().parents[1] / "scripts" / "compare_baseline_metadata.py"


def write_csv(path, counts):
    lines = ["mass_low_GeV,mass_high_GeV,pair_count"]
    width = (300.0 - 0.25) / len(counts)
    lines += [f"{0.25 + i * width:.17g},{0.25 + (i + 1) * width:.17g},{c}" for i, c in enumerate(counts)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _checks(report):
    return {c["check"]: c["passed"] for c in report["checks"]}


def test_csv_summary_uses_exact_integers(tmp_path):
    p = tmp_path / "h.csv"
    write_csv(p, [2**60 + 1, 3])
    summary = histogram_csv_summary(p)
    assert summary["bins"] == 2
    assert summary["total"] == 2**60 + 4
    assert summary["sha256"] == hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.mark.parametrize("bad", ["1.5", "-1", "abc", ""])
def test_csv_summary_rejects_non_integer_counts(tmp_path, bad):
    p = tmp_path / "h.csv"
    p.write_text(f"mass_low_GeV,mass_high_GeV,pair_count\n0,1,{bad}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        histogram_csv_summary(p)


def test_csv_totals_bound_to_metadata_pass_and_fail():
    cand, ref = candidate_metadata(), reference_metadata()
    cand["bins"] = ref["bins"] = 3
    cand["histogram_csv_sha256"] = "a" * 64
    ref["histogram_csv_sha256"] = "b" * 64
    ok = compare(cand, ref,
                 candidate_csv={"bins": 3, "total": cand["pairs_in_histogram_range"], "sha256": "a" * 64, "range_low": 0.25, "range_high": 300.0},
                 reference_csv={"bins": 3, "total": ref["histogram_regular_bin_total"], "sha256": "b" * 64, "range_low": 0.25, "range_high": 300.0})
    assert ok["comparison_passed"] is True
    stale = compare(cand, ref,
                    candidate_csv={"bins": 3, "total": cand["pairs_in_histogram_range"] + 1, "sha256": "a" * 64, "range_low": 0.25, "range_high": 300.0},
                    reference_csv={"bins": 3, "total": ref["histogram_regular_bin_total"], "sha256": "b" * 64, "range_low": 0.25, "range_high": 300.0})
    assert stale["comparison_passed"] is False
    assert _checks(stale)["candidate_csv_total_matches_metadata_in_range_count"] is False
    assert _checks(stale)["reference_csv_total_matches_metadata_in_range_count"] is True
    wrong_bins = compare(cand, ref,
                         candidate_csv={"bins": 2, "total": cand["pairs_in_histogram_range"], "sha256": "a" * 64, "range_low": 0.25, "range_high": 300.0},
                         reference_csv={"bins": 3, "total": ref["histogram_regular_bin_total"], "sha256": "b" * 64})
    assert _checks(wrong_bins)["candidate_csv_bin_count_matches_metadata"] is False


@pytest.mark.parametrize("contents", [
    "mass_low_GeV,mass_high_GeV,pair_count\n",
    "mass_low_GeV,mass_high_GeV,pair_count\n0.25,1,2\n1.1,300,3\n",
])
def test_csv_rejects_empty_or_noncontiguous_bins(tmp_path, contents):
    p = tmp_path / "bad.csv"
    p.write_text(contents, encoding="utf-8")
    with pytest.raises(ValueError):
        histogram_csv_summary(p)


def test_csv_rejects_contiguous_but_nonuniform_grid_when_metadata_is_supplied(tmp_path):
    p = tmp_path / "nonuniform.csv"
    p.write_text(
        "mass_low_GeV,mass_high_GeV,pair_count\\n"
        "0.25,100,2\\n"
        "100,300,3\\n",
        encoding="utf-8",
    )
    # The file is contiguous and spans the configured range, but it is not
    # the two-bin uniform grid implied by the metadata.
    with pytest.raises(ValueError, match="configured uniform grid"):
        histogram_csv_summary(p, expected_bins=2, expected_range=(0.25, 300.0))


def test_csv_sha256_must_match_metadata_even_when_summary_matches(tmp_path):
    cand, ref = candidate_metadata(), reference_metadata()
    cand["bins"] = ref["bins"] = 2
    write_csv(tmp_path / "c.csv", [20, 7])
    write_csv(tmp_path / "r.csv", [20, 7])
    cand["histogram_csv_sha256"] = "0" * 64
    ref["histogram_csv_sha256"] = hashlib.sha256((tmp_path / "r.csv").read_bytes()).hexdigest()
    report = compare(
        cand,
        ref,
        candidate_csv=histogram_csv_summary(tmp_path / "c.csv"),
        reference_csv=histogram_csv_summary(tmp_path / "r.csv"),
    )
    assert report["comparison_passed"] is False
    assert _checks(report)["candidate_csv_sha256_matches_metadata"] is False
    assert _checks(report)["reference_csv_sha256_matches_metadata"] is True
    assert report["artifact_integrity_agrees"] is False
    assert report["cutflow_and_configuration_agree"] is True


def test_event_prefix_must_equal_expected_in_both_outputs():
    cand, ref = candidate_metadata(), reference_metadata()
    assert compare(cand, ref, expected_max_events=100)["comparison_passed"] is True
    short = compare(cand, ref, expected_max_events=200)
    assert short["comparison_passed"] is False
    both_truncated = dict(cand, events_read=50, max_events=50)
    ref_truncated = dict(ref, events_total=50, max_events=50)
    report = compare(both_truncated, ref_truncated, expected_max_events=100)
    assert report["comparison_passed"] is False
    assert _checks(report)["candidate_events_read_equals_expected_event_prefix"] is False


def test_bool_expected_prefix_is_rejected():
    report = compare(candidate_metadata(), reference_metadata(), expected_max_events=True)
    assert report["comparison_passed"] is False


def test_cli_binds_csvs_and_fails_on_stale_csv(tmp_path):
    cand, ref = candidate_metadata(), reference_metadata()
    cand["bins"] = ref["bins"] = 2
    (tmp_path / "c.json").write_text(json.dumps(cand), encoding="utf-8")
    (tmp_path / "r.json").write_text(json.dumps(ref), encoding="utf-8")
    write_csv(tmp_path / "c.csv", [20, 7])
    write_csv(tmp_path / "r.csv", [20, 8])
    import hashlib
    cand["histogram_csv_sha256"] = hashlib.sha256((tmp_path / "c.csv").read_bytes()).hexdigest()
    ref["histogram_csv_sha256"] = hashlib.sha256((tmp_path / "r.csv").read_bytes()).hexdigest()
    (tmp_path / "c.json").write_text(json.dumps(cand), encoding="utf-8")
    (tmp_path / "r.json").write_text(json.dumps(ref), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(COMPARATOR), "--candidate", str(tmp_path / "c.json"), "--reference", str(tmp_path / "r.json"),
         "--candidate-csv", str(tmp_path / "c.csv"), "--reference-csv", str(tmp_path / "r.csv"),
         "--expected-max-events", "100", "--output", str(tmp_path / "out.json")],
        capture_output=True, text=True, check=False)
    assert result.returncode == 2
    report = json.loads((tmp_path / "out.json").read_text(encoding="utf-8"))
    assert _checks(report)["reference_csv_total_matches_metadata_in_range_count"] is False
    assert _checks(report)["candidate_csv_total_matches_metadata_in_range_count"] is True


def test_cli_requires_csv_arguments_as_a_pair(tmp_path):
    cand, ref = candidate_metadata(), reference_metadata()
    (tmp_path / "c.json").write_text(json.dumps(cand), encoding="utf-8")
    (tmp_path / "r.json").write_text(json.dumps(ref), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(COMPARATOR), "--candidate", str(tmp_path / "c.json"), "--reference", str(tmp_path / "r.json"),
         "--candidate-csv", str(tmp_path / "absent.csv"), "--output", str(tmp_path / "out.json")],
        capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert "--candidate-csv and --reference-csv must be supplied together" in result.stderr
