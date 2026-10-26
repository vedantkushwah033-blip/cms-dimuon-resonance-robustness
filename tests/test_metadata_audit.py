from __future__ import annotations

import json
import sys

import pytest
from pathlib import Path

# The CLI scripts are repository-local, not installed package modules.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.audit_baseline_metadata import audit, main  # noqa: E402


def _write(path: Path, data: dict) -> Path:
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _fixtures(tmp_path: Path):
    reference = {
        "input_sha256": "a" * 64,
        "input_bytes": 1000,
        "tree": "Events",
        "events_total": 100,
        "events_exactly_two_muons": 40,
        "events_opposite_sign": 8,
        "histogram_entries_including_flow": 8,
        "bins": 3,
        "mass_min_GeV": 0.25,
        "mass_max_GeV": 300.0,
        "histogram_regular_bin_total": 5,
        "histogram_underflow": 1,
        "histogram_overflow": 2,
    }
    candidate = {
        "input_sha256": "a" * 64,
        "input_bytes": 1000,
        "tree": "Events",
        "tree_entries_available": 100,
        "events_read": 100,
        "events_processed": 100,
        "max_events": None,
        "events_selected": 40,
        "opposite_charge_pairs_total": 8,
        "selection_mode": "exactly-two-opposite-charge",
        "bins": 3,
        "mass_range_GeV": [0.25, 300.0],
        "pairs_in_histogram_range": 5,
        "pairs_below_mass_range": 1,
        "pairs_at_or_above_mass_max": 2,
        "pairs_nonfinite_mass": 0,
    }
    histogram = {
        "bin_edges_exactly_equal": True,
        "exact_bin_by_bin_parity": True,
        "bin_count": 3,
        "reference_total_count": 5,
        "candidate_total_count": 5,
        "differing_bin_count": 0,
        "total_absolute_bin_count_difference": 0,
        "maximum_absolute_bin_count_difference": 0,
        "differing_bins": [],
    }
    return (
        _write(tmp_path / "reference.json", reference),
        _write(tmp_path / "candidate.json", candidate),
        _write(tmp_path / "histogram.json", histogram),
    )


def test_metadata_audit_passes_only_when_all_evidence_agrees(tmp_path: Path) -> None:
    paths = _fixtures(tmp_path)
    report = audit(*paths)
    assert report["status"] == "PASS"
    assert report["checks_passed"] == report["checks_total"]


def test_metadata_audit_fails_on_different_input_checksum(tmp_path: Path) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["input_sha256"] = "b" * 64
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    failed = {check["name"] for check in report["checks"] if not check["passed"]}
    assert "input_sha256" in failed


def test_metadata_audit_fails_if_checksum_is_missing(tmp_path: Path) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["input_sha256"] = None
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    assert any(
        check["name"] == "input_sha256" and not check["passed"]
        for check in report["checks"]
    )


def test_metadata_audit_fails_when_histogram_parity_is_false(tmp_path: Path) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    histogram = json.loads(histogram_path.read_text(encoding="utf-8"))
    histogram["exact_bin_by_bin_parity"] = False
    histogram_path.write_text(json.dumps(histogram), encoding="utf-8")
    assert audit(reference_path, candidate_path, histogram_path)["status"] == "FAIL"



def test_metadata_audit_rejects_matching_but_malformed_sha256(tmp_path: Path) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    for path in (reference_path, candidate_path):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["input_sha256"] = "not-a-real-digest"
        path.write_text(json.dumps(data), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    assert any(
        check["name"] == "input_sha256_format" and not check["passed"]
        for check in report["checks"]
    )


def test_metadata_audit_rejects_nonpositive_file_size(tmp_path: Path) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["input_bytes"] = 0
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    assert any(
        check["name"] == "input_bytes_positive_integer" and not check["passed"]
        for check in report["checks"]
    )



def test_metadata_audit_rejects_wrong_selection_mode(tmp_path: Path) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["selection_mode"] = "all-opposite-charge-pairs"
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    assert any(
        check["name"] == "selection_mode" and not check["passed"]
        for check in report["checks"]
    )


def test_metadata_audit_rejects_opposite_sign_cutflow_mismatch(tmp_path: Path) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["opposite_charge_pairs_total"] = 7
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    assert any(
        check["name"] == "opposite_sign_event_pair_accounting" and not check["passed"]
        for check in report["checks"]
    )



def test_metadata_audit_rejects_float_encoded_count_even_when_equal(tmp_path: Path) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate["events_selected"] = 40.0
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    assert any(
        check["name"] == "candidate_events_selected_valid_nonnegative_integer"
        and not check["passed"]
        for check in report["checks"]
    )


def test_metadata_audit_rejects_reference_flow_counts_that_do_not_conserve_entries(
    tmp_path: Path,
) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    # Keep GetEntries and cut-flow internally consistent while corrupting the
    # independently recorded regular/flow-bin accounting.
    reference["histogram_overflow"] = 3
    reference_path.write_text(json.dumps(reference), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    assert any(
        check["name"] == "reference_histogram_flow_count_conservation"
        and not check["passed"]
        for check in report["checks"]
    )


def test_metadata_audit_rejects_boolean_reference_flow_count(tmp_path: Path) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    reference["histogram_underflow"] = True
    reference_path.write_text(json.dumps(reference), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    assert any(
        check["name"] == "reference_histogram_flow_count_conservation"
        and not check["passed"]
        for check in report["checks"]
    )


def test_metadata_audit_rejects_parity_boolean_with_nonzero_discrepancy_summary(
    tmp_path: Path,
) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    histogram = json.loads(histogram_path.read_text(encoding="utf-8"))
    histogram["exact_bin_by_bin_parity"] = True
    histogram["differing_bin_count"] = 1
    histogram["total_absolute_bin_count_difference"] = 2
    histogram["maximum_absolute_bin_count_difference"] = 2
    histogram_path.write_text(json.dumps(histogram), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    failed = {check["name"] for check in report["checks"] if not check["passed"]}
    assert "histogram_differing_bin_count_zero" in failed
    assert "histogram_total_absolute_bin_count_difference_zero" in failed
    assert "histogram_maximum_absolute_bin_count_difference_zero" in failed


def test_metadata_audit_rejects_missing_comparator_discrepancy_metrics(
    tmp_path: Path,
) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    histogram = json.loads(histogram_path.read_text(encoding="utf-8"))
    del histogram["differing_bin_count"]
    del histogram["total_absolute_bin_count_difference"]
    del histogram["maximum_absolute_bin_count_difference"]
    histogram_path.write_text(json.dumps(histogram), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    failed = {check["name"] for check in report["checks"] if not check["passed"]}
    assert "histogram_report_differing_bin_count_valid_nonnegative_integer" in failed
    assert "histogram_report_total_absolute_bin_count_difference_valid_nonnegative_integer" in failed
    assert "histogram_report_maximum_absolute_bin_count_difference_valid_nonnegative_integer" in failed
    assert "histogram_differing_bin_count_zero" in failed
    assert "histogram_total_absolute_bin_count_difference_zero" in failed
    assert "histogram_maximum_absolute_bin_count_difference_zero" in failed


def test_metadata_audit_rejects_nonempty_discrepancy_list_with_zero_count(
    tmp_path: Path,
) -> None:
    reference_path, candidate_path, histogram_path = _fixtures(tmp_path)
    histogram = json.loads(histogram_path.read_text(encoding="utf-8"))
    histogram["differing_bin_count"] = 0
    histogram["differing_bins"] = [
        {
            "bin_index": 1,
            "mass_low_GeV": 1.0,
            "mass_high_GeV": 2.0,
            "reference_count": 4,
            "candidate_count": 5,
            "candidate_minus_reference": 1,
        }
    ]
    histogram_path.write_text(json.dumps(histogram), encoding="utf-8")
    report = audit(reference_path, candidate_path, histogram_path)
    assert report["status"] == "FAIL"
    assert any(
        check["name"] == "histogram_discrepancy_list_consistent"
        and not check["passed"]
        for check in report["checks"]
    )



@pytest.mark.parametrize("metadata_index", [0, 1, 2])
def test_metadata_audit_rejects_duplicate_json_keys(
    tmp_path: Path, metadata_index: int,
) -> None:
    paths = _fixtures(tmp_path)
    # JSON parsers commonly accept duplicate keys and silently keep the last
    # value, which can conceal contradictory provenance or count metadata.
    paths[metadata_index].write_text(
        '{"events_total": 100, "events_total": 99}', encoding="utf-8"
    )
    with pytest.raises(ValueError, match="duplicate JSON object key"):
        audit(*paths)



def test_audit_cli_writes_structured_failure_for_duplicate_json_keys(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    paths = _fixtures(tmp_path)
    paths[0].write_text(
        '{"events_total": 100, "events_total": 99}', encoding="utf-8"
    )
    output = tmp_path / "audit-failure.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "audit_baseline_metadata.py",
            "--reference-metadata", str(paths[0]),
            "--candidate-metadata", str(paths[1]),
            "--histogram-report", str(paths[2]),
            "--output", str(output),
        ],
    )
    assert main() == 2
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["status"] == "FAIL"
    assert report["checks_total"] == 0
    assert "duplicate JSON object key" in report["error"]
