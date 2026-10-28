#!/usr/bin/env python3
"""Estimate floating-point bin-flip sensitivity for the dimuon mass formula.

Compares the project's cancellation-resistant formula with a direct Cartesian
E^2 - |p|^2 evaluation in float64 on float32-like NanoAOD inputs. Synthetic
kinematics only: this is not a substitute for a real-data comparison.
"""
from __future__ import annotations
import argparse
import json
import numpy as np
from cms_dimuon_robustness.invariant_mass import pair_invariant_mass

MUON_MASS = 0.1056583755

def direct_mass(pt1, eta1, phi1, m1, pt2, eta2, phi2, m2):
    pt1, eta1, phi1, m1, pt2, eta2, phi2, m2 = (
        np.asarray(x, dtype=np.float64) for x in (pt1, eta1, phi1, m1, pt2, eta2, phi2, m2)
    )
    def cart(pt, eta, phi, mass):
        px, py, pz = pt * np.cos(phi), pt * np.sin(phi), pt * np.sinh(eta)
        energy = np.sqrt(px * px + py * py + pz * pz + mass * mass)
        return px, py, pz, energy
    a, b = cart(pt1, eta1, phi1, m1), cart(pt2, eta2, phi2, m2)
    mass_squared = (a[3] + b[3]) ** 2 - (a[0] + b[0]) ** 2 - (a[1] + b[1]) ** 2 - (a[2] + b[2]) ** 2
    return np.where(mass_squared >= 0, np.sqrt(np.abs(mass_squared)), -np.sqrt(np.abs(mass_squared)))

def sample(kind: str, n: int, rng: np.random.Generator):
    f32 = np.float32
    if kind == "generic":
        pt = [np.exp(rng.uniform(np.log(3), np.log(150), n)).astype(f32) for _ in range(2)]
        eta = [rng.uniform(-2.4, 2.4, n).astype(f32) for _ in range(2)]
        phi = [rng.uniform(-np.pi, np.pi, n).astype(f32) for _ in range(2)]
    elif kind == "collinear":
        pt1 = rng.uniform(20, 200, n).astype(f32)
        pt = [pt1, (pt1 * rng.uniform(0.8, 1.2, n)).astype(f32)]
        eta1 = rng.uniform(-2.4, 2.4, n).astype(f32)
        eta = [eta1, (eta1 + rng.normal(0, 0.002, n)).astype(f32)]
        phi1 = rng.uniform(-3, 3, n).astype(f32)
        phi = [phi1, (phi1 + rng.normal(0, 0.002, n)).astype(f32)]
    else:
        raise ValueError(kind)
    mass = np.full(n, MUON_MASS, dtype=f32)
    return pt[0], eta[0], phi[0], mass, pt[1], eta[1], phi[1], mass

def run(n_per_batch: int, batches: int, seed: int, bins: int = 30000, lo: float = 0.25, hi: float = 300.0) -> dict:
    if n_per_batch <= 0 or batches <= 0 or bins <= 0 or not lo < hi:
        raise ValueError("batch size, batch count, and bins must be positive and lo < hi")
    edges = np.linspace(lo, hi, bins + 1)
    out = {"seed": seed, "pairs_per_kind": n_per_batch * batches, "bins": bins, "range_GeV": [lo, hi], "kinds": {}}
    rng = np.random.default_rng(seed)
    for kind in ("generic", "collinear"):
        in_range = both_in_range = flips_numpy = flips_axis_arith = membership = 0
        max_rel = 0.0
        for _ in range(batches):
            values = sample(kind, n_per_batch, rng)
            stable, direct = pair_invariant_mass(*values), direct_mass(*values)
            stable_in, direct_in = (stable >= lo) & (stable < hi), (direct >= lo) & (direct < hi)
            membership += int(np.count_nonzero(stable_in != direct_in))
            in_range += int(np.count_nonzero(stable_in))
            both = stable_in & direct_in
            both_in_range += int(np.count_nonzero(both))
            ia = np.searchsorted(edges, stable[both], side="right") - 1
            ib = np.searchsorted(edges, direct[both], side="right") - 1
            flips_numpy += int(np.count_nonzero(ia != ib))
            ir = np.floor(bins * (stable[both] - lo) / (hi - lo)).astype(int)
            flips_axis_arith += int(np.count_nonzero(ia != ir))
            if np.any(both):
                max_rel = max(max_rel, float(np.max(np.abs(stable[both] - direct[both]) / stable[both])))
        out["kinds"][kind] = {
            "pairs_in_range_stable_formula": in_range,
            "pairs_in_range_for_both_formulas": both_in_range,
            "bin_disagreements_stable_vs_direct": flips_numpy,
            "range_membership_disagreements": membership,
            "disagreements_numpy_edges_vs_root_arithmetic_same_mass": flips_axis_arith,
            "max_relative_mass_difference": max_rel,
            "upper_95pct_conditional_bin_flip_rate_if_zero_observed_rule_of_three": (
                3.0 / both_in_range if both_in_range and not flips_numpy else None
            ),
        }
    return out

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--batch", type=int, default=2_000_000)
    ap.add_argument("--batches", type=int, default=10)
    ap.add_argument("--seed", type=int, default=20261028)
    a = ap.parse_args()
    print(json.dumps(run(a.batch, a.batches, a.seed), indent=2))

if __name__ == "__main__":
    main()
