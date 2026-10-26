import hashlib
import json
import subprocess
import sys
from pathlib import Path

import awkward as ak
import numpy as np
import uproot

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_spectrum_script_writes_reproducible_smoke_outputs(tmp_path):
    input_path = tmp_path / "tiny_events.root"
    with uproot.recreate(input_path) as root_file:
        tree = root_file.mktree(
            "Events",
            {
                "Muon_pt": "var * float64",
                "Muon_eta": "var * float64",
                "Muon_phi": "var * float64",
                "Muon_mass": "var * float64",
                "Muon_charge": "var * int32",
            },
        )
        tree.extend(
            {
                "Muon_pt": ak.Array([[10.0, 10.0], [12.0, 12.0], [20.0, 20.0]]),
                "Muon_eta": ak.Array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]),
                "Muon_phi": ak.Array([[0.0, np.pi], [0.0, np.pi], [0.0, np.pi]]),
                "Muon_mass": ak.Array([[0.105658, 0.105658]] * 3),
                "Muon_charge": ak.Array([[1, -1]] * 3),
            }
        )

    output_dir = tmp_path / "outputs"
    subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "reproduce_dimuon_spectrum.py"),
            "--input",
            str(input_path),
            "--output-dir",
            str(output_dir),
            "--max-events",
            "2",
            "--bins",
            "20",
            "--mass-max",
            "100",
            "--step-size",
            "1 KB",
            "--sha256-input",
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    metadata = json.loads((output_dir / "run_metadata.json").read_text(encoding="utf-8"))
    assert metadata["events_read"] == 2
    assert metadata["events_selected"] == 2
    assert metadata["events_processed"] == 2
    assert metadata["opposite_charge_pairs_total"] == 2
    assert metadata["pairs_below_mass_range"] + metadata["pairs_in_histogram_range"] + metadata["pairs_above_mass_range"] + metadata["pairs_nonfinite_mass"] == metadata["opposite_charge_pairs_total"]
    assert metadata["pairs_in_histogram_range"] == 2
    assert metadata["input_is_local_file"] is True
    assert metadata["input_bytes"] > 0
    assert metadata["input_sha256"] == hashlib.sha256(input_path.read_bytes()).hexdigest()
    assert metadata["tree_entries_available"] == 3
    assert metadata["branch_types"]["Muon_pt"]
    assert metadata["software"]["python"]
    assert "git_commit" in metadata
    assert metadata["max_events"] == 2
    assert metadata["selection_mode"] == "exactly-two-opposite-charge"
    assert metadata["selection"].startswith("exactly two reconstructed muons")
    assert (output_dir / "dimuon_mass_histogram.csv").is_file()
    assert (output_dir / "dimuon_mass_spectrum.png").is_file()
