"""Negative integration tests for ROOT input-schema validation in the spectrum CLI."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import awkward as ak
import numpy as np
import uproot

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "reproduce_dimuon_spectrum.py"


def _write_events(
    path: Path,
    *,
    declared_counts=None,
    eta_values=None,
    pt_values=None,
    mass_values=None,
    charge_values=None,
    include_charge=True,
) -> None:
    """Write a tiny synthetic ROOT tree whose schema can be deliberately corrupted."""
    branch_types = {
        "nMuon": "int32",
        "Muon_pt": "var * float64",
        "Muon_eta": "var * float64",
        "Muon_phi": "var * float64",
        "Muon_mass": "var * float64",
    }
    if include_charge:
        branch_types["Muon_charge"] = "var * int32"

    with uproot.recreate(path) as root_file:
        tree = root_file.mktree("Events", branch_types)
        arrays = {
            "nMuon": np.asarray([2] if declared_counts is None else declared_counts, dtype=np.int32),
            "Muon_pt": ak.Array([[10.0, 10.0]] if pt_values is None else pt_values),
            "Muon_eta": ak.Array([[0.0, 0.0]] if eta_values is None else eta_values),
            "Muon_phi": ak.Array([[0.0, np.pi]]),
            "Muon_mass": ak.Array([[0.105658, 0.105658]] if mass_values is None else mass_values),
        }
        if include_charge:
            arrays["Muon_charge"] = ak.Array([[1, -1]] if charge_values is None else charge_values)
        tree.extend(arrays)


def _run_cli(input_path: Path, output_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input",
            str(input_path),
            "--output-dir",
            str(output_dir),
            "--bins",
            "10",
            "--mass-max",
            "100",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_rejects_declared_muon_count_mismatch(tmp_path):
    input_path = tmp_path / "bad_nmuon.root"
    _write_events(input_path, declared_counts=[1])
    completed = _run_cli(input_path, tmp_path / "output")
    assert completed.returncode != 0
    assert "nMuon disagrees with Muon_pt collection length at event 0" in completed.stderr


def test_cli_rejects_secondary_muon_branch_length_mismatch(tmp_path):
    input_path = tmp_path / "bad_eta_length.root"
    _write_events(input_path, eta_values=[[0.0]])
    completed = _run_cli(input_path, tmp_path / "output")
    assert completed.returncode != 0
    assert "Muon_pt and Muon_eta collection lengths differ at event 0" in completed.stderr


def test_cli_names_missing_required_branch(tmp_path):
    input_path = tmp_path / "missing_charge.root"
    _write_events(input_path, include_charge=False)
    completed = _run_cli(input_path, tmp_path / "output")
    assert completed.returncode != 0
    assert "Required branches missing from Events: ['Muon_charge']" in completed.stderr



def test_cli_rejects_invalid_muon_charge_values(tmp_path):
    input_path = tmp_path / "invalid_charge.root"
    _write_events(input_path, charge_values=[[0, -1]])
    completed = _run_cli(input_path, tmp_path / "output")
    assert completed.returncode != 0
    assert "Muon_charge must contain only -1 or +1 values" in completed.stderr


def test_cli_rejects_negative_finite_muon_pt(tmp_path):
    input_path = tmp_path / "negative_pt.root"
    _write_events(input_path, pt_values=[[-10.0, 10.0]])
    completed = _run_cli(input_path, tmp_path / "output")
    assert completed.returncode != 0
    assert "Muon_pt must be non-negative when finite" in completed.stderr


def test_cli_rejects_negative_finite_muon_mass(tmp_path):
    input_path = tmp_path / "negative_mass.root"
    _write_events(input_path, mass_values=[[0.105658, -0.1]])
    completed = _run_cli(input_path, tmp_path / "output")
    assert completed.returncode != 0
    assert "Muon_mass must be non-negative when finite" in completed.stderr
