import json
import subprocess
import sys
from pathlib import Path

import awkward as ak
import numpy as np
import uproot

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_schema_inspector_lists_trees_branches_and_trigger_candidates(tmp_path):
    root_path = tmp_path / "schema.root"
    with uproot.recreate(root_path) as root_file:
        tree = root_file.mktree(
            "Events",
            {
                "Muon_pt": "var * float64",
                "Muon_charge": "var * int32",
                "HLT_DoubleMu4": "bool",
                "run": "int32",
            },
        )
        tree.extend(
            {
                "Muon_pt": ak.Array([[10.0, 11.0], [12.0]]),
                "Muon_charge": ak.Array([[1, -1], [1]]),
                "HLT_DoubleMu4": np.array([True, False]),
                "run": np.array([200001, 200002], dtype=np.int32),
            }
        )

    output_path = tmp_path / "schema.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "inspect_root_schema.py"),
            "--input",
            str(root_path),
            "--output",
            str(output_path),
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    report = json.loads(output_path.read_text(encoding="utf-8"))
    events = report["trees"]["Events"]
    assert events["entries"] == 2
    assert events["branch_count"] >= 4
    assert "HLT_DoubleMu4" in events["trigger_related_name_candidates"]
    assert "Muon_pt" in events["branches"]
    assert events["branch_group_presence"]["muon_kinematics"]["missing"] == [
        "Muon_eta",
        "Muon_mass",
        "Muon_phi",
    ]
    assert "run" in events["branch_group_presence"]["event_identity"]["present"]
    assert json.loads(completed.stdout)["input"] == str(root_path)
