#!/usr/bin/env python3
"""Inspect ROOT file tree names, branches, entry counts, and trigger-related branch names.

This tool audits the available schema only. A branch name is not proof that a trigger
selection is correctly understood or that the dataset is suitable for a physics claim.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import uproot


def inspect_file(input_path: str) -> dict:
    result = {"input": input_path, "trees": {}}
    with uproot.open(input_path) as root_file:
        for key in root_file.keys(cycle=False):
            obj = root_file[key]
            if not hasattr(obj, "keys") or not hasattr(obj, "num_entries"):
                continue
            branches = sorted(str(name).split(";")[0] for name in obj.keys())
            trigger_candidates = [
                name for name in branches
                if re.search(r"(?:^HLT_|Trigger|trigger|Prescale|prescale|L1_)", name, re.IGNORECASE)
            ]
            result["trees"][key] = {
                "entries": int(obj.num_entries),
                "branch_count": len(branches),
                "branches": branches,
                "trigger_related_name_candidates": trigger_candidates,
            }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Local ROOT file or supported ROOT URL")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON output path")
    args = parser.parse_args()

    report = inspect_file(args.input)
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
