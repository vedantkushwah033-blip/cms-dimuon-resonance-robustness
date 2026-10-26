"""Awkward-array operations for dimuon pairs in CMS NanoAOD-like files."""

from __future__ import annotations

import awkward as ak
import numpy as np


def opposite_charge_pair_masses(arrays: ak.Array) -> ak.Array:
    """Return jagged invariant masses for all opposite-charge muon pairs per event.

    Required fields are Muon_pt, Muon_eta, Muon_phi, Muon_mass, and Muon_charge.
    This applies no additional trigger, object-quality, or event selection.
    """
    muons = ak.zip(
        {
            "pt": arrays["Muon_pt"],
            "eta": arrays["Muon_eta"],
            "phi": arrays["Muon_phi"],
            "mass": arrays["Muon_mass"],
            "charge": arrays["Muon_charge"],
        }
    )
    pairs = ak.combinations(muons, 2, fields=["mu1", "mu2"])
    keep = pairs.mu1.charge * pairs.mu2.charge < 0

    def energy(mu):
        return np.sqrt((mu.pt * np.cosh(mu.eta)) ** 2 + mu.mass**2)

    e = energy(pairs.mu1) + energy(pairs.mu2)
    px = pairs.mu1.pt * np.cos(pairs.mu1.phi) + pairs.mu2.pt * np.cos(pairs.mu2.phi)
    py = pairs.mu1.pt * np.sin(pairs.mu1.phi) + pairs.mu2.pt * np.sin(pairs.mu2.phi)
    pz = pairs.mu1.pt * np.sinh(pairs.mu1.eta) + pairs.mu2.pt * np.sinh(pairs.mu2.eta)
    mass_squared = e**2 - px**2 - py**2 - pz**2
    masses = np.sqrt(ak.where(mass_squared > 0, mass_squared, 0.0))
    return masses[keep]
