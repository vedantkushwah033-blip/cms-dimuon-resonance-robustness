"""Integration tests for schema validation in the metadata parity audit."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from scripts.audit_baseline_metadata import audit


def _write_json(path: Path, value: dict[str, Any]) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def _valid_metadata() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    digest = "a" * 64
    reference = {
        "input_sha256": digest,
        "input_bytes": 100,
        "tree": "Events",
        "events_total": 10,
        "events_exactly_two_muons": 5,
        "events_opposite_sign": 4,
        "histogram_regular_bin_total": 3,
        "histogram_underflow": 1,
        "histogram_overflow": 0,
        "bins": 2,
        "mass_min_GeV": 0.25,
        "mass_max_GeV": 300.0,
    }
    candidate = {
        "input_sha256": digest,
        "input_bytes": 100,
        "tree": "Events",
        "tree_entries_available": 10,
        "events_selected": 5,
        "opposite_charge_pairs_total": 4,
        "pairs_in_histogram_range": 3,
        "pairs_below_mass_range": 1,
        "pairs_at_or_above_mass_max": 0,
        "bins": 2,
        "mass_range_GeV": [0.25, 300.0],
        "selection_mode": "exactly-two-opposite-charge",
    }
    histogram = {
        "bin_edges_exactly_equal": True,
        "exact_bin_by_bin_parity": True,
        "bin_count": 2,
        "reference_total_count": 3,
        "candidate_total_count": 3,
    }
    return reference, candidate, histogram


def test_matching_positive_integer_bin_counts_pass(tmp_path: Path) -> None:
    reference, candidate, histogram = _valid_metadata()
    report = audit(
        _write_json(tmp_path / "reference.json", reference),
        _write_json(tmp_path / "candidate.json", candidate),
        _write_json(tmp_path / "histogram.json", histogram),
    )
    assert report["status"] == "PASS"


def test_string_encoded_bin_count_cannot_pass_by_matching(tmp_path: Path) -> None:
    reference, candidate, histogram = _valid_metadata()
    reference["bins"] = "2"
    candidate["bins"] = "2"
    report = audit(
        _write_json(tmp_path / "reference.json", reference),
        _write_json(tmp_path / "candidate.json", candidate),
        _write_json(tmp_path / "histogram.json", histogram),
    )
    assert report["status"] == "FAIL"
    failed_names = {item["name"] for item in report["checks"] if not item["passed"]}
    assert "reference_bins_valid_positive_integer" in failed_names
    assert "candidate_bins_valid_positive_integer" in failed_names


def test_string_encoded_mass_range_cannot_pass_by_matching(tmp_path: Path) -> None:
    reference, candidate, histogram = _valid_metadata()
    reference["mass_min_GeV"] = "0.25"
    reference["mass_max_GeV"] = "300"
    candidate["mass_range_GeV"] = ["0.25", "300"]
    report = audit(
        _write_json(tmp_path / "reference.json", reference),
        _write_json(tmp_path / "candidate.json", candidate),
        _write_json(tmp_path / "histogram.json", histogram),
    )
    assert report["status"] == "FAIL"
    failed_names = {item["name"] for item in report["checks"] if not item["passed"]}
    assert "reference_mass_min_GeV_valid_finite_number" in failed_names
    assert "reference_mass_max_GeV_valid_finite_number" in failed_names
    assert "reference_mass_range_valid" in failed_names
    assert "candidate_mass_range_valid" in failed_names


def test_matching_non_string_tree_names_cannot_pass(tmp_path: Path) -> None:
    reference, candidate, histogram = _valid_metadata()
    reference["tree"] = 1
    candidate["tree"] = 1
    report = audit(
        _write_json(tmp_path / "reference.json", reference),
        _write_json(tmp_path / "candidate.json", candidate),
        _write_json(tmp_path / "histogram.json", histogram),
    )
    assert report["status"] == "FAIL"
    failed_names = {item["name"] for item in report["checks"] if not item["passed"]}
    assert "reference_tree_name_valid_nonempty_string" in failed_names
    assert "candidate_tree_name_valid_nonempty_string" in failed_names