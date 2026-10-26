#!/usr/bin/env python3
"""Inspect ROOT trees and report candidate branch coverage for a dimuon analysis.

This is a schema inventory, not a physics validation. A branch-name match does not
prove the branch's semantics, trigger efficiency, prescale treatment, or suitability.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import uproot

BRANCH_GROUPS = {
    "muon_kinematics": ["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass"],
    "muon_charge": ["Muon_charge"],
    "event_identity": ["run", "luminosityBlock", "event"],
    "muon_quality_or_isolation_candidates": [
        "Muon_tightId",
        "Muon_mediumId",
        "Muon_softId",
        "Muon_pfRelIso03_all",
        "Muon_pfRelIso04_all",
        "Muon_dxy",
        "Muon_dz",
    ],
}


def inspect_file(input_path: str) -> dict:
    """Return tree metadata and explicitly heuristic branch-presence checks."""
    result = {"input": input_path, "trees": {}}
    with uproot.open(input_path) as root_file:
        for key in root_file.keys(cycle=False):
            obj = root_file[key]
            if not hasattr(obj, "keys") or not hasattr(obj, "num_entries"):
                continue
            branches = sorted(str(name).split(";")[0] for name in obj.keys())
            branch_set = set(branches)
            trigger_candidates = [
                name for name in branches
                if re.search(
                    r"(?:^HLT_|Trigger|trigger|Prescale|prescale|^L1_)",
                    name,
                    re.IGNORECASE,
                )
            ]
            branch_types = {
                str(name): str(type_name)
                for name, type_name in sorted(obj.typenames().items())
            }
            result["trees"][key] = {
                "entries": int(obj.num_entries),
                "branch_count": len(branches),
                "branches": branches,
                "branch_types": branch_types,
                "trigger_related_name_candidates": trigger_candidates,
                "branch_group_presence": {
                    group: {
                        "present": [name for name in candidates if name in branch_set],
                        "missing": [name for name in candidates if name not in branch_set],
                    }
                    for group, candidates in BRANCH_GROUPS.items()
                },
            }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Local ROOT file or supported ROOT URL")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON output path")
    args = parser.parse_args()
    if "://" not in args.input:
        input_path = Path(args.input).expanduser().resolve()
        if args.output is not None and args.output.resolve() == input_path:
            parser.error("--output resolves to the input ROOT file; refusing to overwrite it")

    report = inspect_file(args.input)
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
