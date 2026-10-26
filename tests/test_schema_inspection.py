"""Regression coverage for schema-inspection branch-count semantics.

Uproot may expose additional split branches for jagged collections, so tests must
not assume the visible branch count equals the number of user-declared fields.
"""
import json
import subprocess
import sys
from pathlib import Path

import awkward as ak
import numpy as np
import uproot

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_schema_inspection_accepts_split_branches(tmp_path):
    root_path = tmp_path / "split_schema.root"
    with uproot.recreate(root_path) as root_file:
        tree = root_file.mktree(
            "Events",
            {
                "Muon_pt": "var * float64",
                "Muon_charge": "var * int32",
                "HLT_Mu13_Mu8": "bool",
                "run": "int32",
            },
        )
        tree.extend(
            {
                "Muon_pt": ak.Array([[10.0, 11.0], [12.0]]),
                "Muon_charge": ak.Array([[1, -1], [1]]),
                "HLT_Mu13_Mu8": np.array([True, False]),
                "run": np.array([193900, 193901], dtype=np.int32),
            }
        )

    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "inspect_root_schema.py"),
            "--input",
            str(root_path),
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    events = json.loads(completed.stdout)["trees"]["Events"]
    assert events["entries"] == 2
    assert events["branch_count"] >= 4
    assert "HLT_Mu13_Mu8" in events["trigger_related_name_candidates"]
    assert set(events["branch_types"]) == set(events["branches"])
