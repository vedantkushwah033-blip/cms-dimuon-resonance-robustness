import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPARATOR = REPO_ROOT / "scripts" / "compare_baseline_metadata.py"


def candidate_metadata():
    return {
        "input_sha256": "a" * 64,
        "input_bytes": 123456,
        "events_read": 100,
        "events_selected": 40,
        "events_with_opposite_charge_pair": 31,
        "opposite_charge_pairs_total": 31,
        "pairs_below_mass_range": 2,
        "pairs_in_histogram_range": 27,
        "pairs_at_or_above_mass_max": 2,
        "pairs_nonfinite_mass": 0,
        "bins": 30000,
        "max_events": 100,
        "mass_range_GeV": [0.25, 300.0],
        "selection_mode": "exactly-two-opposite-charge",
    }


def reference_metadata():
    return {
        "input_sha256": "a" * 64,
        "input_bytes": 123456,
        "events_total": 100,
        "events_exactly_two_muons": 40,
        "events_opposite_sign": 31,
        "histogram_entries_including_flow": 31,
        "histogram_underflow": 2,
        "histogram_regular_bin_total": 27,
        "histogram_overflow": 2,
        "bins": 30000,
        "max_events": 100,
        "mass_min_GeV": 0.25,
        "mass_max_GeV": 300.0,
        "selection": ["nMuon == 2", "Muon_charge[0] != Muon_charge[1]"],
    }


def run_comparison(tmp_path, candidate, reference):
    candidate_path = tmp_path / "candidate.json"
    reference_path = tmp_path / "reference.json"
    output_path = tmp_path / "comparison.json"
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    reference_path.write_text(json.dumps(reference), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(COMPARATOR),
            "--candidate",
            str(candidate_path),
            "--reference",
            str(reference_path),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result, output_path


def test_matching_cutflow_configuration_and_mass_accounting_pass(tmp_path):
    result, report_path = run_comparison(
        tmp_path, candidate_metadata(), reference_metadata()
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 0, result.stderr
    assert report["cutflow_and_configuration_agree"] is True
    assert report["failed_check_count"] == 0
    assert report_path.read_bytes().endswith(b"\n")


def test_mismatched_input_hash_fails_even_when_cutflow_matches(tmp_path):
    reference = reference_metadata()
    reference["input_sha256"] = "b" * 64
    result, report_path = run_comparison(
        tmp_path, candidate_metadata(), reference
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    assert report["input_provenance_agrees"] is False
    failed = {item["check"] for item in report["checks"] if not item["passed"]}
    assert "input_sha256_matches" in failed


def test_missing_or_malformed_input_hash_fails(tmp_path):
    candidate = candidate_metadata()
    candidate.pop("input_sha256")
    reference = reference_metadata()
    reference["input_sha256"] = "not-a-sha256"
    result, report_path = run_comparison(tmp_path, candidate, reference)
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    assert report["input_provenance_agrees"] is False
    failed = {item["check"] for item in report["checks"] if not item["passed"]}
    assert "candidate_input_sha256_present_and_valid" in failed
    assert "reference_input_sha256_present_and_valid" in failed
    assert "input_sha256_matches" in failed


def test_mismatched_input_byte_count_fails(tmp_path):
    reference = reference_metadata()
    reference["input_bytes"] += 1
    result, report_path = run_comparison(
        tmp_path, candidate_metadata(), reference
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    assert report["input_provenance_agrees"] is False
    failed = {item["check"] for item in report["checks"] if not item["passed"]}
    assert "input_byte_count_matches" in failed


def test_missing_or_invalid_input_byte_count_fails(tmp_path):
    candidate = candidate_metadata()
    candidate["input_bytes"] = True
    reference = reference_metadata()
    reference.pop("input_bytes")
    result, report_path = run_comparison(tmp_path, candidate, reference)
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    assert report["input_provenance_agrees"] is False
    failed = {item["check"] for item in report["checks"] if not item["passed"]}
    assert "candidate_input_bytes_present_and_valid" in failed
    assert "reference_input_bytes_present_and_valid" in failed


def test_cutflow_mismatch_fails_with_machine_readable_report(tmp_path):
    candidate = candidate_metadata()
    candidate["events_selected"] = 41
    result, report_path = run_comparison(
        tmp_path, candidate, reference_metadata()
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    assert report["cutflow_and_configuration_agree"] is False
    failed = {item["check"] for item in report["checks"] if not item["passed"]}
    assert "events_selected_vs_exactly_two_muons" in failed


def test_flow_bin_mismatch_fails(tmp_path):
    reference = reference_metadata()
    reference["histogram_overflow"] = 3
    result, report_path = run_comparison(
        tmp_path, candidate_metadata(), reference
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    failed = {item["check"] for item in report["checks"] if not item["passed"]}
    assert "candidate_pairs_at_or_above_max_vs_reference_overflow" in failed


def test_nonfinite_masses_prevent_flow_parity_claim(tmp_path):
    candidate = candidate_metadata()
    candidate["pairs_nonfinite_mass"] = 1
    candidate["pairs_in_histogram_range"] = 26
    result, report_path = run_comparison(
        tmp_path, candidate, reference_metadata()
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    failed = {item["check"] for item in report["checks"] if not item["passed"]}
    assert "candidate_nonfinite_mass_count_is_zero_for_flow_parity" in failed


def test_float_count_is_rejected_not_silently_coerced(tmp_path):
    candidate = candidate_metadata()
    candidate["events_read"] = 100.0
    result, report_path = run_comparison(
        tmp_path, candidate, reference_metadata()
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    assert report["cutflow_and_configuration_agree"] is False
    assert "must be a nonnegative integer" in report["comparison_error"]


def test_reference_selection_mismatch_fails(tmp_path):
    reference = reference_metadata()
    reference["selection"] = ["nMuon >= 2", "Muon_charge[0] != Muon_charge[1]"]
    result, report_path = run_comparison(
        tmp_path, candidate_metadata(), reference
    )
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result.returncode == 2
    assert report["cutflow_and_configuration_agree"] is False
    failed = {item["check"] for item in report["checks"] if not item["passed"]}
    assert "reference_uses_expected_selection" in failed


def test_output_cannot_overwrite_candidate_metadata(tmp_path):
    candidate_path = tmp_path / "candidate.json"
    reference_path = tmp_path / "reference.json"
    candidate_path.write_text(json.dumps(candidate_metadata()), encoding="utf-8")
    reference_path.write_text(json.dumps(reference_metadata()), encoding="utf-8")
    original_bytes = candidate_path.read_bytes()
    result = subprocess.run(
        [
            sys.executable,
            str(COMPARATOR),
            "--candidate",
            str(candidate_path),
            "--reference",
            str(reference_path),
            "--output",
            str(candidate_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "refusing to overwrite an input metadata file" in result.stderr
    assert candidate_path.read_bytes() == original_bytes
