import importlib.util
import json
import pathlib
import subprocess
import sys

import awkward as ak
import numpy as np
import pytest
import uproot


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.mark.skipif(
    importlib.util.find_spec("ROOT") is None,
    reason="PyROOT integration test runs in the dedicated ROOT-enabled CI job",
)
def test_reference_exporter_on_tiny_synthetic_root_file(tmp_path):
    root_path = tmp_path / "synthetic_reference.root"
    with uproot.recreate(root_path) as root_file:
        tree = root_file.mktree(
            "Events",
            {
                "nMuon": "int32",
                "Muon_pt": "var * float32",
                "Muon_eta": "var * float32",
                "Muon_phi": "var * float32",
                "Muon_mass": "var * float32",
                "Muon_charge": "var * int32",
            },
        )
        tree.extend(
            {
                "nMuon": np.array([2, 2, 1], dtype=np.int32),
                "Muon_pt": ak.Array([[10.0, 10.0], [10.0, 10.0], [8.0]]),
                "Muon_eta": ak.Array([[0.0, 0.0], [0.0, 0.0], [0.2]]),
                "Muon_phi": ak.Array([[0.0, np.pi], [0.0, np.pi], [1.0]]),
                "Muon_mass": ak.Array(
                    [[0.105658, 0.105658], [0.105658, 0.105658], [0.105658]]
                ),
                "Muon_charge": ak.Array([[1, -1], [1, 1], [-1]]),
            }
        )

    output_dir = tmp_path / "reference"
    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "export_reference_dimuon_histogram.py"),
            "--input",
            str(root_path),
            "--output-dir",
            str(output_dir),
            "--bins",
            "40",
            "--mass-min",
            "0.25",
            "--mass-max",
            "40",
            "--sha256-input",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr

    metadata = json.loads(
        (output_dir / "reference_metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["events_total"] == 3
    assert metadata["events_exactly_two_muons"] == 2
    assert metadata["events_opposite_sign"] == 1
    assert metadata["histogram_regular_bin_total"] == 1
    assert metadata["histogram_underflow"] == 0
    assert metadata["histogram_overflow"] == 0
    assert metadata["input_bytes"] == root_path.stat().st_size
    assert metadata["input_sha256"] is not None
    assert len(metadata["input_sha256"]) == 64
    assert metadata["reference_source_commit"] == (
        "19a4a64fd58ef66a6ee3cf4f2a469fba61c60a09"
    )
    assert metadata["project_git_commit"]

    rows = (output_dir / "dimuon_mass_histogram.csv").read_text(
        encoding="utf-8"
    ).splitlines()
    assert rows[0] == "mass_low_GeV,mass_high_GeV,pair_count"
    assert len(rows) == 41
    assert sum(int(row.rsplit(",", 1)[1]) for row in rows[1:]) == 1

    # Run the separate Uproot/NumPy candidate on the exact same file and
    # require strict bin-by-bin parity on this synthetic fixture.
    candidate_dir = tmp_path / "candidate"
    candidate = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "reproduce_dimuon_spectrum.py"),
            "--input",
            str(root_path),
            "--output-dir",
            str(candidate_dir),
            "--max-events",
            "3",
            "--bins",
            "40",
            "--mass-min",
            "0.25",
            "--mass-max",
            "40",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert candidate.returncode == 0, candidate.stderr

    comparison_path = tmp_path / "comparison.json"
    comparison = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "compare_histograms.py"),
            "--reference",
            str(output_dir / "dimuon_mass_histogram.csv"),
            "--candidate",
            str(candidate_dir / "dimuon_mass_histogram.csv"),
            "--output",
            str(comparison_path),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert comparison.returncode == 0, comparison.stderr
    report = json.loads(comparison_path.read_text(encoding="utf-8"))

    assert report["exact_bin_by_bin_parity"] is True
    assert report["differing_bin_count"] == 0

    # A bounded reference smoke test must stop at the requested entry count.
    limited_dir = tmp_path / "limited-reference"
    limited = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "export_reference_dimuon_histogram.py"),
            "--input",
            str(root_path),
            "--output-dir",
            str(limited_dir),
            "--max-events",
            "1",
            "--bins",
            "40",
            "--mass-min",
            "0.25",
            "--mass-max",
            "40",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert limited.returncode == 0, limited.stderr
    limited_metadata = json.loads(
        (limited_dir / "reference_metadata.json").read_text(encoding="utf-8")
    )
    assert limited_metadata["max_events"] == 1
    assert limited_metadata["events_total"] == 1
    assert limited_metadata["events_exactly_two_muons"] == 1
    assert limited_metadata["events_opposite_sign"] == 1
    assert limited_metadata["histogram_regular_bin_total"] == 1

@pytest.mark.skipif(
    importlib.util.find_spec("ROOT") is None,
    reason="PyROOT integration test runs in the dedicated ROOT-enabled CI job",
)
def test_reference_exporter_rejects_missing_required_branch(tmp_path):
    root_path = tmp_path / "missing_charge.root"
    with uproot.recreate(root_path) as root_file:
        tree = root_file.mktree(
            "Events",
            {
                "nMuon": "int32",
                "Muon_pt": "var * float32",
                "Muon_eta": "var * float32",
                "Muon_phi": "var * float32",
                "Muon_mass": "var * float32",
            },
        )
        tree.extend(
            {
                "nMuon": np.array([2], dtype=np.int32),
                "Muon_pt": ak.Array([[10.0, 10.0]]),
                "Muon_eta": ak.Array([[0.0, 0.0]]),
                "Muon_phi": ak.Array([[0.0, np.pi]]),
                "Muon_mass": ak.Array([[0.105658, 0.105658]]),
            }
        )

    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "export_reference_dimuon_histogram.py"),
            "--input",
            str(root_path),
            "--output-dir",
            str(tmp_path / "missing-branch-output"),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "missing required branches: ['Muon_charge']" in completed.stderr

@pytest.mark.skipif(
    importlib.util.find_spec("ROOT") is None,
    reason="PyROOT integration test runs in the dedicated ROOT-enabled CI job",
)
def test_reference_exporter_rejects_inconsistent_muon_collection_lengths(tmp_path):
    root_path = tmp_path / "inconsistent_collections.root"
    with uproot.recreate(root_path) as root_file:
        tree = root_file.mktree(
            "Events",
            {
                "nMuon": "int32",
                "Muon_pt": "var * float32",
                "Muon_eta": "var * float32",
                "Muon_phi": "var * float32",
                "Muon_mass": "var * float32",
                "Muon_charge": "var * int32",
            },
        )
        tree.extend(
            {
                "nMuon": np.array([2], dtype=np.int32),
                "Muon_pt": ak.Array([[10.0, 10.0]]),
                "Muon_eta": ak.Array([[0.0]]),
                "Muon_phi": ak.Array([[0.0, np.pi]]),
                "Muon_mass": ak.Array([[0.105658, 0.105658]]),
                "Muon_charge": ak.Array([[1, -1]]),
            }
        )

    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "export_reference_dimuon_histogram.py"),
            "--input",
            str(root_path),
            "--output-dir",
            str(tmp_path / "invalid-collection-output"),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "inconsistent nMuon or muon collection lengths" in completed.stderr




def test_reference_exporter_cli_rejects_nonfinite_mass_bounds_before_input_check(
    tmp_path,
):
    missing_input = tmp_path / "does-not-exist.root"
    script = REPO_ROOT / "scripts" / "export_reference_dimuon_histogram.py"
    for invalid_bound in ("nan", "inf", "-inf"):
        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--input",
                str(missing_input),
                "--mass-max=" + invalid_bound,
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 2
        assert "mass bounds must be finite" in completed.stderr
        assert "does-not-exist.root" not in completed.stderr


def test_reference_exporter_rejects_nonpositive_event_limit_before_file_access(tmp_path):
    missing_input = tmp_path / "does-not-exist.root"
    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "export_reference_dimuon_histogram.py"),
            "--input",
            str(missing_input),
            "--max-events",
            "0",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 2
    assert "--max-events must be positive" in completed.stderr
    assert "must point to an existing local ROOT file" not in completed.stderr


@pytest.mark.skipif(
    importlib.util.find_spec("ROOT") is None,
    reason="PyROOT integration test runs in the dedicated ROOT-enabled CI job",
)
def test_reference_exporter_rejects_nonphysical_muon_charge(tmp_path):
    root_path = tmp_path / "invalid_charge.root"
    with uproot.recreate(root_path) as root_file:
        tree = root_file.mktree(
            "Events",
            {
                "nMuon": "int32",
                "Muon_pt": "var * float32",
                "Muon_eta": "var * float32",
                "Muon_phi": "var * float32",
                "Muon_mass": "var * float32",
                "Muon_charge": "var * int32",
            },
        )
        tree.extend(
            {
                "nMuon": np.array([2], dtype=np.int32),
                "Muon_pt": ak.Array([[10.0, 10.0]]),
                "Muon_eta": ak.Array([[0.0, 0.0]]),
                "Muon_phi": ak.Array([[0.0, np.pi]]),
                "Muon_mass": ak.Array([[0.105658, 0.105658]]),
                "Muon_charge": ak.Array([[0, 1]]),
            }
        )

    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "export_reference_dimuon_histogram.py"),
            "--input",
            str(root_path),
            "--output-dir",
            str(tmp_path / "invalid-charge-output"),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "invalid charge values" in completed.stderr


@pytest.mark.skipif(
    importlib.util.find_spec("ROOT") is None,
    reason="PyROOT integration test runs in the dedicated ROOT-enabled CI job",
)
def test_reference_exporter_rejects_negative_finite_kinematics(tmp_path):
    root_path = tmp_path / "negative_pt.root"
    with uproot.recreate(root_path) as root_file:
        tree = root_file.mktree(
            "Events",
            {
                "nMuon": "int32",
                "Muon_pt": "var * float32",
                "Muon_eta": "var * float32",
                "Muon_phi": "var * float32",
                "Muon_mass": "var * float32",
                "Muon_charge": "var * int32",
            },
        )
        tree.extend(
            {
                "nMuon": np.array([2], dtype=np.int32),
                "Muon_pt": ak.Array([[-10.0, 10.0]]),
                "Muon_eta": ak.Array([[0.0, 0.0]]),
                "Muon_phi": ak.Array([[0.0, np.pi]]),
                "Muon_mass": ak.Array([[0.105658, 0.105658]]),
                "Muon_charge": ak.Array([[1, -1]]),
            }
        )

    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "export_reference_dimuon_histogram.py"),
            "--input",
            str(root_path),
            "--output-dir",
            str(tmp_path / "negative-pt-output"),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "negative finite kinematics" in completed.stderr


@pytest.mark.skipif(
    importlib.util.find_spec("ROOT") is None,
    reason="PyROOT integration test runs in the dedicated ROOT-enabled CI job",
)
def test_reference_exporter_does_not_charge_validate_unselected_events(tmp_path):
    root_path = tmp_path / "unselected_invalid_charge.root"
    with uproot.recreate(root_path) as root_file:
        tree = root_file.mktree(
            "Events",
            {
                "nMuon": "int32",
                "Muon_pt": "var * float32",
                "Muon_eta": "var * float32",
                "Muon_phi": "var * float32",
                "Muon_mass": "var * float32",
                "Muon_charge": "var * int32",
            },
        )
        tree.extend(
            {
                "nMuon": np.array([1], dtype=np.int32),
                "Muon_pt": ak.Array([[8.0]]),
                "Muon_eta": ak.Array([[0.2]]),
                "Muon_phi": ak.Array([[1.0]]),
                "Muon_mass": ak.Array([[0.105658]]),
                "Muon_charge": ak.Array([[0]]),
            }
        )

    output_dir = tmp_path / "unselected-output"
    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "export_reference_dimuon_histogram.py"),
            "--input",
            str(root_path),
            "--output-dir",
            str(output_dir),
            "--bins",
            "10",
            "--mass-min",
            "0.25",
            "--mass-max",
            "40",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    metadata = json.loads(
        (output_dir / "reference_metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["events_total"] == 1
    assert metadata["events_exactly_two_muons"] == 0
    assert metadata["events_opposite_sign"] == 0
    assert metadata["histogram_regular_bin_total"] == 0
