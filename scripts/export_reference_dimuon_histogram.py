#!/usr/bin/env python3
"""Export a numerical histogram using the official CMS ROOT/RDataFrame recipe.

Requires a ROOT-enabled Python environment (PyROOT). This script intentionally
uses ROOT's four-vector and TH1D implementation rather than the project's
Uproot/NumPy implementation, so the two paths can be compared independently.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path

REFERENCE_SOURCE_COMMIT = "19a4a64fd58ef66a6ee3cf4f2a469fba61c60a09"
REFERENCE_SOURCE_URL = "https://github.com/cms-opendata-analyses/DimuonSpectrumNanoAODOutreachAnalysis/blob/19a4a64fd58ef66a6ee3cf4f2a469fba61c60a09/dimuonSpectrum.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Local CMS ROOT file used by both implementations")
    parser.add_argument("--tree", default="Events")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/reference"))
    parser.add_argument("--sha256-input", action="store_true", help="Hash the full input file (adds one full file read)")
    parser.add_argument("--bins", type=int, default=30000)
    parser.add_argument("--mass-min", type=float, default=0.25)
    parser.add_argument("--mass-max", type=float, default=300.0)
    args = parser.parse_args()
    if args.bins <= 0 or not 0 < args.mass_min < args.mass_max:
        parser.error("bins must be positive and 0 < mass-min < mass-max")
    if not Path(args.input).is_file():
        parser.error("--input must point to an existing local ROOT file")
    return args


def main() -> int:
    args = parse_args()
    try:
        import ROOT
    except ImportError as exc:
        raise RuntimeError(
            "PyROOT is required. Run this exporter in a ROOT-enabled environment; "
            "the regular project test environment does not install ROOT."
        ) from exc

    args.output_dir.mkdir(parents=True, exist_ok=True)
    input_path = Path(args.input).resolve()
    input_sha256 = None
    if args.sha256_input:
        digest = hashlib.sha256()
        with input_path.open("rb") as stream:
            for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
                digest.update(block)
        input_sha256 = digest.hexdigest()
    ROOT.ROOT.EnableImplicitMT(1)
    ROOT.gInterpreter.Declare(
        """
        float computeInvariantMassReference(
            ROOT::VecOps::RVec<float>& pt,
            ROOT::VecOps::RVec<float>& eta,
            ROOT::VecOps::RVec<float>& phi,
            ROOT::VecOps::RVec<float>& mass
        ) {
            ROOT::Math::PtEtaPhiMVector m1(pt[0], eta[0], phi[0], mass[0]);
            ROOT::Math::PtEtaPhiMVector m2(pt[1], eta[1], phi[1], mass[1]);
            return (m1 + m2).mass();
        }
        """
    )

    dataframe = ROOT.RDataFrame(args.tree, args.input)
    exactly_two = dataframe.Filter("nMuon == 2", "Events with exactly two muons")
    opposite_sign = exactly_two.Filter(
        "Muon_charge[0] != Muon_charge[1]", "Muons with opposite charge"
    )
    with_mass = opposite_sign.Define(
        "Dimuon_mass",
        "computeInvariantMassReference(Muon_pt, Muon_eta, Muon_phi, Muon_mass)",
    )
    model = ROOT.RDF.TH1DModel(
        "reference_dimuon_mass",
        "reference_dimuon_mass",
        args.bins,
        args.mass_min,
        args.mass_max,
    )
    histogram_result = with_mass.Histo1D(model, "Dimuon_mass")

    # Force evaluation after all lazy actions have been booked.
    events_total = int(dataframe.Count().GetValue())
    events_exactly_two = int(exactly_two.Count().GetValue())
    events_opposite_sign = int(opposite_sign.Count().GetValue())
    histogram = histogram_result.GetValue()

    csv_path = args.output_dir / "dimuon_mass_histogram.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["mass_low_GeV", "mass_high_GeV", "pair_count"])
        for index in range(1, args.bins + 1):
            writer.writerow(
                [
                    format(float(histogram.GetXaxis().GetBinLowEdge(index)), ".17g"),
                    format(float(histogram.GetXaxis().GetBinUpEdge(index)), ".17g"),
                    str(int(histogram.GetBinContent(index))),
                ]
            )

    metadata = {
        "input": str(input_path),
        "input_bytes": input_path.stat().st_size,
        "input_sha256": input_sha256,
        "tree": args.tree,
        "root_version": str(ROOT.gROOT.GetVersion()),
        "python_version": platform.python_version(),
        "implementation": "official-style ROOT RDataFrame + PtEtaPhiMVector + TH1D",
        "reference_source_commit": REFERENCE_SOURCE_COMMIT,
        "reference_source_url": REFERENCE_SOURCE_URL,
        "selection": [
            "nMuon == 2",
            "Muon_charge[0] != Muon_charge[1]",
        ],
        "bins": args.bins,
        "mass_min_GeV": args.mass_min,
        "mass_max_GeV": args.mass_max,
        "histogram_interval": "[mass_min, mass_max)",
        "events_total": events_total,
        "events_exactly_two_muons": events_exactly_two,
        "events_opposite_sign": events_opposite_sign,
        "histogram_entries_including_flow": int(histogram.GetEntries()),
        "histogram_underflow": int(histogram.GetBinContent(0)),
        "histogram_regular_bin_total": sum(
            int(histogram.GetBinContent(index)) for index in range(1, args.bins + 1)
        ),
        "histogram_overflow": int(histogram.GetBinContent(args.bins + 1)),
        "note": (
            "This is an independently generated numerical reference candidate. "
            "Verify input checksum and source revision externally before treating "
            "it as a reproduction of the published example."
        ),
    }
    metadata_path = args.output_dir / "reference_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
