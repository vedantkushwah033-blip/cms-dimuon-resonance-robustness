import json
import pathlib
import subprocess
import sys

import awkward as ak
import numpy as np
import uproot


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_baseline_script_on_tiny_synthetic_root_file(tmp_path):
    root_path = tmp_path / "synthetic.root"
    with uproot.recreate(root_path) as root_file:
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
                "nMuon": np.array([2, 2], dtype=np.int32),
                "Muon_pt": ak.Array([[10.0, 10.0], [10.0, 10.0]]),
                "Muon_eta": ak.Array([[0.0, 0.0], [0.0, 0.0]]),
                "Muon_phi": ak.Array([[0.0, np.pi], [0.0, np.pi]]),
                "Muon_mass": ak.Array([[0.105658, 0.105658], [0.105658, 0.105658]]),
                "Muon_charge": ak.Array([[1, -1], [1, 1]]),
            }
        )

    output_dir = tmp_path / "baseline"
    command = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "reproduce_dimuon_spectrum.py"),
        "--input",
        str(root_path),
        "--output-dir",
        str(output_dir),
        "--max-events",
        "2",
        "--bins",
        "40",
        "--mass-min",
        "0.25",
        "--mass-max",
        "40",
    ]
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    metadata = json.loads((output_dir / "run_metadata.json").read_text(encoding="utf-8"))
    histogram = np.genfromtxt(
        output_dir / "dimuon_mass_histogram.csv",
        delimiter=",",
        names=True,
    )
    assert metadata["events_processed"] == 2
    assert metadata["opposite_charge_pairs_total"] == 1
    assert metadata["pairs_in_histogram_range"] == 1
    assert int(histogram["pair_count"].sum()) == 1
    assert (output_dir / "dimuon_mass_spectrum.png").is_file()
    assert '"events_processed": 2' in completed.stdout


def test_baseline_script_rejects_nmuon_collection_mismatch(tmp_path):
    root_path = tmp_path / "inconsistent.root"
    with uproot.recreate(root_path) as root_file:
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
                "nMuon": np.array([2], dtype=np.int32),
                "Muon_pt": ak.Array([[10.0]]),
                "Muon_eta": ak.Array([[0.0]]),
                "Muon_phi": ak.Array([[0.0]]),
                "Muon_mass": ak.Array([[0.105658]]),
                "Muon_charge": ak.Array([[1]]),
            }
        )

    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "reproduce_dimuon_spectrum.py"),
            "--input",
            str(root_path),
            "--output-dir",
            str(tmp_path / "mismatch-output"),
            "--max-events",
            "1",
            "--bins",
            "10",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "nMuon disagrees with Muon_pt collection length at event 0" in completed.stderr


def test_baseline_script_rejects_malformed_nonselected_event(tmp_path):
    root_path = tmp_path / "malformed_nonselected.root"
    with uproot.recreate(root_path) as root_file:
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
                "nMuon": np.array([1], dtype=np.int32),
                "Muon_pt": ak.Array([[10.0]]),
                "Muon_eta": ak.Array([[]]),
                "Muon_phi": ak.Array([[0.0]]),
                "Muon_mass": ak.Array([[0.105658]]),
                "Muon_charge": ak.Array([[1]]),
            }
        )

    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "reproduce_dimuon_spectrum.py"),
            "--input",
            str(root_path),
            "--output-dir",
            str(tmp_path / "malformed-output"),
            "--max-events",
            "1",
            "--bins",
            "10",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "Muon_pt and Muon_eta collection lengths differ at event 0" in completed.stderr
