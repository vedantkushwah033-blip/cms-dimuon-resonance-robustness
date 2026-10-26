"""Integration tests that distinguish event selection from pair selection."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import awkward as ak
import numpy as np
import uproot

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "reproduce_dimuon_spectrum.py"


def _write_mixed_multiplicity_sample(path: Path) -> None:
    """Create 2-muon OS, 3-muon mixed-charge, and 2-muon same-sign events."""
    with uproot.recreate(path) as root_file:
        tree = root_file.mktree(
            "Events",
            {
                "nMuon": "int32",
                "Muon_pt": "var * float64",
                "Muon_eta": "var * float64",
                "Muon_phi": "var * float64",
                "Muon_mass": "var * float64",
                "Muon_charge": "var * int32",
            },
        )
        tree.extend(
            {
                "nMuon": np.asarray([2, 3, 2], dtype=np.int32),
                "Muon_pt": ak.Array([[20.0, 18.0], [25.0, 21.0, 16.0], [12.0, 14.0]]),
                "Muon_eta": ak.Array([[0.1, -0.2], [0.0, 0.2, -0.3], [0.1, -0.1]]),
                "Muon_phi": ak.Array([[0.0, 2.5], [0.0, 2.0, -2.0], [0.0, 2.5]]),
                "Muon_mass": ak.Array([[0.105658, 0.105658], [0.105658, 0.105658, 0.105658], [0.105658, 0.105658]]),
                "Muon_charge": ak.Array([[1, -1], [1, -1, 1], [1, 1]]),
            }
        )


def _run(input_path: Path, output_dir: Path, selection: str) -> dict:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input",
            str(input_path),
            "--output-dir",
            str(output_dir),
            "--bins",
            "20",
            "--mass-max",
            "100",
            "--selection",
            selection,
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads((output_dir / "run_metadata.json").read_text(encoding="utf-8"))


def test_default_selection_matches_exactly_two_muon_reference_contract(tmp_path):
    input_path = tmp_path / "mixed.root"
    _write_mixed_multiplicity_sample(input_path)

    metadata = _run(
        input_path,
        tmp_path / "exactly_two",
        "exactly-two-opposite-charge",
    )

    assert metadata["events_read"] == 3
    assert metadata["events_selected"] == 2
    assert metadata["opposite_charge_pairs_total"] == 1
    assert metadata["selection_mode"] == "exactly-two-opposite-charge"


def test_all_pair_mode_keeps_three_muon_event_and_counts_each_os_pair(tmp_path):
    input_path = tmp_path / "mixed.root"
    _write_mixed_multiplicity_sample(input_path)

    metadata = _run(
        input_path,
        tmp_path / "all_pairs",
        "all-opposite-charge-pairs",
    )

    assert metadata["events_read"] == 3
    assert metadata["events_selected"] == 3
    # One pair from the 2-muon opposite-sign event, two from the 3-muon event.
    assert metadata["opposite_charge_pairs_total"] == 3
    assert metadata["selection_mode"] == "all-opposite-charge-pairs"
