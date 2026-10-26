#!/usr/bin/env python3
"""Build a baseline opposite-charge dimuon spectrum from a selected CMS ROOT sample.

This is a baseline reconstruction, not a trigger-efficiency analysis or a resonance search.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
from pathlib import Path

import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import uproot

from cms_dimuon_robustness.nanoaod import opposite_charge_pair_masses
from cms_dimuon_robustness.histogram import histogram_masses

BRANCHES = ["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"]


def sha256_file(path: Path) -> str:
    """Calculate a streaming SHA-256 checksum for a local input file."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def package_version(name: str) -> str | None:
    """Return an installed package version, or None if distribution metadata is absent."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Explicit local ROOT file or supported ROOT URL; choose and document the dataset before running")
    parser.add_argument("--tree", default="Events", help="ROOT tree name (default: Events)")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/baseline"))
    parser.add_argument("--step-size", default="100 MB", help="Uproot chunk size, e.g. '100 MB'")
    parser.add_argument("--max-events", type=int, default=None, help="Optional event limit for a smoke test")
    parser.add_argument("--sha256-input", action="store_true", help="Compute SHA-256 for a local input file (adds one full file read)")
    parser.add_argument("--bins", type=int, default=30000)
    parser.add_argument("--mass-min", type=float, default=0.25)
    parser.add_argument("--mass-max", type=float, default=300.0)
    parser.add_argument(
        "--selection",
        choices=["exactly-two-opposite-charge", "all-opposite-charge-pairs"],
        default="exactly-two-opposite-charge",
        help="Event/pair selection; default matches the public example's exactly-two-muon selection",
    )
    args = parser.parse_args()
    if args.max_events is not None and args.max_events <= 0:
        parser.error("--max-events must be positive")
    if args.bins <= 0 or not 0 < args.mass_min < args.mass_max:
        parser.error("bins must be positive and 0 < mass-min < mass-max (logarithmic x axis)")
    return args


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    local_input = Path(args.input).expanduser()
    is_local_file = "://" not in args.input and local_input.is_file()
    if args.sha256_input and not is_local_file:
        raise ValueError("--sha256-input requires a local input file")
    input_sha256 = sha256_file(local_input) if args.sha256_input else None
    input_bytes = local_input.stat().st_size if is_local_file else None
    counts = np.zeros(args.bins, dtype=np.int64)
    edges = np.linspace(args.mass_min, args.mass_max, args.bins + 1)
    events_read = 0
    events_selected = 0
    opposite_charge_pairs = 0
    pairs_below_range = 0
    pairs_at_or_above_upper_edge = 0
    pairs_nonfinite = 0
    tree_entries = None
    branch_types = None

    with uproot.open(args.input) as root_file:
        if args.tree not in root_file:
            raise KeyError(f"Tree {args.tree!r} not found in {args.input!r}")
        tree = root_file[args.tree]
        tree_entries = int(tree.num_entries)
        branch_types = {str(name): str(value) for name, value in tree.typenames().items() if name in BRANCHES}
        missing = sorted(set(BRANCHES) - set(tree.keys()))
        if missing:
            raise KeyError(f"Required branches missing from {args.tree}: {missing}")

        for chunk in tree.iterate(expressions=BRANCHES, step_size=args.step_size, library="ak"):
            if args.max_events is not None:
                remaining = args.max_events - events_read
                if remaining <= 0:
                    break
                chunk = chunk[:remaining]

            events_read += len(chunk[BRANCHES[0]])
            if args.selection == "exactly-two-opposite-charge":
                selected = chunk[ak.num(chunk["Muon_pt"], axis=1) == 2]
            else:
                selected = chunk
            events_selected += len(selected[BRANCHES[0]])
            masses = opposite_charge_pair_masses(selected)
            flat = ak.to_numpy(ak.flatten(masses, axis=None))
            opposite_charge_pairs += int(len(flat))
            chunk_counts, accounting = histogram_masses(
                flat,
                bins=args.bins,
                mass_min=args.mass_min,
                mass_max=args.mass_max,
            )
            counts += chunk_counts
            if accounting["pairs_total"] != len(flat):
                raise RuntimeError("histogram helper pair total does not match the input chunk")
            pairs_nonfinite += accounting["pairs_nonfinite"]
            pairs_below_range += accounting["pairs_below_range"]
            pairs_at_or_above_upper_edge += accounting["pairs_above_range"]
            if args.max_events is not None and events_read >= args.max_events:
                break

    accounted_pairs = (
        pairs_below_range
        + int(counts.sum())
        + pairs_at_or_above_upper_edge
        + pairs_nonfinite
    )
    if accounted_pairs != opposite_charge_pairs:
        raise RuntimeError(
            "pair accounting invariant violated: "
            f"accounted={accounted_pairs}, total={opposite_charge_pairs}"
        )

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
        "input_is_local_file": is_local_file,
        "input_bytes": input_bytes,
        "input_sha256": input_sha256,
        "tree": args.tree,
        "tree_entries_available": tree_entries,
        "branch_types": branch_types,
        "software": {
            "python": platform.python_version(),
            "numpy": package_version("numpy"),
            "awkward": package_version("awkward"),
            "uproot": package_version("uproot"),
            "matplotlib": package_version("matplotlib"),
        },
        "git_commit": os.environ.get("GITHUB_SHA"),
        "branches": BRANCHES,
        "events_read": events_read,
        "events_selected": events_selected,
        "events_processed": events_read,
        "opposite_charge_pairs_total": opposite_charge_pairs,
        "pairs_below_mass_range": pairs_below_range,
        "pairs_in_histogram_range": int(counts.sum()),
        "pairs_at_or_above_mass_max": pairs_at_or_above_upper_edge,
        "pairs_nonfinite_mass": pairs_nonfinite,
        "bins": args.bins,
        "mass_range_GeV": [args.mass_min, args.mass_max],
        "histogram_interval": "[mass_min, mass_max); values exactly at mass_max are overflow",
        "selection_mode": args.selection,
        "step_size": args.step_size,
        "max_events": args.max_events,
        "selection": (
            "exactly two reconstructed muons per event, then opposite-charge pair"
            if args.selection == "exactly-two-opposite-charge"
            else "all opposite-charge muon pairs per event; events may contain more than two muons"
        ),
        "status": "baseline reconstruction only; must be compared with official reference before interpretation",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    centers = (edges[:-1] + edges[1:]) / 2
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.step(centers, counts, where="mid")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Dimuon invariant mass [GeV]")
    ax.set_ylabel("Opposite-charge pair count per bin")
    ax.set_title("CMS 2012 dimuon spectrum — baseline reconstruction")
    ax.grid(True, which="both", alpha=0.25)
    fig.tight_layout()
    fig.savefig(plot_path, dpi=160)
    plt.close(fig)

    print(json.dumps({"metadata": str(metadata_path), "histogram": str(csv_path), "plot": str(plot_path), **metadata}, indent=2))


if __name__ == "__main__":
    main()
