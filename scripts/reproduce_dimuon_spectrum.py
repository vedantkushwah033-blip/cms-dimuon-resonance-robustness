#!/usr/bin/env python3
"""Build a baseline opposite-charge dimuon spectrum from a selected CMS ROOT sample.

This is a baseline reconstruction, not a trigger-efficiency analysis or a resonance search.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import uproot

from cms_dimuon_robustness.nanoaod import opposite_charge_pair_masses

DEFAULT_INPUT = (
    "root://eospublic.cern.ch//eos/opendata/cms/derived-data/"
    "AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root"
)
BRANCHES = ["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Explicit local ROOT file or supported ROOT URL; choose and document the dataset before running")
    parser.add_argument("--tree", default="Events", help="ROOT tree name (default: Events)")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/baseline"))
    parser.add_argument("--step-size", default="100 MB", help="Uproot chunk size, e.g. '100 MB'")
    parser.add_argument("--max-events", type=int, default=None, help="Optional event limit for a smoke test")
    parser.add_argument("--bins", type=int, default=1200)
    parser.add_argument("--mass-min", type=float, default=0.0)
    parser.add_argument("--mass-max", type=float, default=120.0)
    args = parser.parse_args()
    if args.max_events is not None and args.max_events <= 0:
        parser.error("--max-events must be positive")
    if args.bins <= 0 or not args.mass_min < args.mass_max:
        parser.error("bins must be positive and mass-min must be below mass-max")
    return args


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    counts = np.zeros(args.bins, dtype=np.int64)
    edges = np.linspace(args.mass_min, args.mass_max, args.bins + 1)
    events_processed = 0
    opposite_charge_pairs = 0

    with uproot.open(args.input) as root_file:
        if args.tree not in root_file:
            raise KeyError(f"Tree {args.tree!r} not found in {args.input!r}")
        tree = root_file[args.tree]
        missing = sorted(set(BRANCHES) - set(tree.keys()))
        if missing:
            raise KeyError(f"Required branches missing from {args.tree}: {missing}")

        for chunk in tree.iterate(expressions=BRANCHES, step_size=args.step_size, library="ak"):
            if args.max_events is not None:
                remaining = args.max_events - events_processed
                if remaining <= 0:
                    break
                chunk = chunk[:remaining]

            masses = opposite_charge_pair_masses(chunk)
            flat = ak.to_numpy(ak.flatten(masses, axis=None))
            opposite_charge_pairs += int(len(flat))
            counts += np.histogram(flat, bins=edges)[0]
            events_processed += len(chunk[BRANCHES[0]])

            if args.max_events is not None and events_processed >= args.max_events:
                break

    csv_path = args.output_dir / "dimuon_mass_histogram.csv"
    metadata_path = args.output_dir / "run_metadata.json"
    plot_path = args.output_dir / "dimuon_mass_spectrum.png"

    np.savetxt(
        csv_path,
        np.column_stack([edges[:-1], edges[1:], counts]),
        delimiter=",",
        header="mass_low_GeV,mass_high_GeV,pair_count",
        comments="",
        fmt=["%.8g", "%.8g", "%d"],
    )
    metadata = {
        "input": args.input,
        "tree": args.tree,
        "branches": BRANCHES,
        "events_processed": events_processed,
        "opposite_charge_pairs_total": opposite_charge_pairs,
        "pairs_in_histogram_range": int(counts.sum()),
        "bins": args.bins,
        "mass_range_GeV": [args.mass_min, args.mass_max],
        "step_size": args.step_size,
        "max_events": args.max_events,
        "selection": "all opposite-charge muon pairs; no extra quality or trigger selection applied",
        "status": "baseline reconstruction only; must be compared with official reference before interpretation",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    centers = (edges[:-1] + edges[1:]) / 2
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.step(centers, counts, where="mid")
    ax.set_yscale("log")
    ax.set_xlabel("Dimuon invariant mass [GeV]")
    ax.set_ylabel("Opposite-charge pair count per bin")
    ax.set_title("CMS 2012 dimuon spectrum — unselected opposite-charge baseline")
    ax.grid(True, which="both", alpha=0.25)
    fig.tight_layout()
    fig.savefig(plot_path, dpi=160)
    plt.close(fig)

    print(json.dumps({"metadata": str(metadata_path), "histogram": str(csv_path), "plot": str(plot_path), **metadata}, indent=2))


if __name__ == "__main__":
    main()
