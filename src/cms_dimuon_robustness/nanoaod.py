"""Awkward-array operations for dimuon pairs in CMS NanoAOD-like files."""

from __future__ import annotations

import awkward as ak
import numpy as np


def opposite_charge_pair_masses(arrays: ak.Array) -> ak.Array:
    """Return jagged invariant masses for all opposite-charge muon pairs per event.

    Required fields are Muon_pt, Muon_eta, Muon_phi, Muon_mass, and Muon_charge.
    This applies no additional trigger, object-quality, or event selection.
    """
    required_fields = ("Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge")
    missing_fields = [field for field in required_fields if field not in arrays.fields]
    if missing_fields:
        raise KeyError(f"Required muon fields missing: {missing_fields}")

    # Detect inconsistent per-event collection lengths explicitly before zipping.
    # A mismatched branch can otherwise cause opaque broadcasting errors or,
    # worse, make selection and kinematics refer to different muon objects.
    multiplicities = {
        field: ak.num(arrays[field], axis=1)
        for field in required_fields
    }
    reference_counts = ak.to_numpy(multiplicities["Muon_pt"])
    for field, counts in multiplicities.items():
        field_counts = ak.to_numpy(counts)
        mismatches = np.flatnonzero(field_counts != reference_counts)
        if mismatches.size:
            event_index = int(mismatches[0])
            raise ValueError(
                "Per-event muon multiplicities differ: "
                f"event {event_index} has Muon_pt={int(reference_counts[event_index])} "
                f"and {field}={int(field_counts[event_index])}"
            )

    # The official reference uses charge inequality (charge[0] != charge[1]).
    # For this to be equivalent to a physical opposite-sign selection, charges
    # must be exactly -1 or +1. Reject malformed values instead of silently
    # treating them differently from the reference.
    charges = ak.to_numpy(ak.flatten(arrays["Muon_charge"], axis=None))
    if not np.all(np.isin(charges, (-1, 1))):
        raise ValueError("Muon_charge must contain only -1 or +1 values")

    # ROOT NanoAOD kinematic branches are commonly float32. Promote the
    # kinematic inputs before transcendental functions and invariant-mass
    # arithmetic: otherwise Awkward/NumPy may perform intermediate operations
    # in float32, increasing cancellation error in E^2 - |p|^2 and creating
    # avoidable negative mass-squared values. Keep charge values in their
    # original integer representation for exact selection semantics.
    muons = ak.zip(
        {
            "pt": ak.values_astype(arrays["Muon_pt"], np.float64),
            "eta": ak.values_astype(arrays["Muon_eta"], np.float64),
            "phi": ak.values_astype(arrays["Muon_phi"], np.float64),
            "mass": ak.values_astype(arrays["Muon_mass"], np.float64),
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
    scale = e**2 + px**2 + py**2 + pz**2
    tolerance = 64 * np.finfo(float).eps * scale
    # Clamp only small negative round-off. Preserve non-finite inputs as non-finite
    # so data-quality problems cannot silently become zero-mass pairs.
    roundoff_negative = (
        np.isfinite(mass_squared)
        & np.isfinite(scale)
        & (mass_squared < 0)
        & (mass_squared >= -tolerance)
    )
    stable_mass_squared = ak.where(
        mass_squared >= 0,
        mass_squared,
        ak.where(roundoff_negative, 0.0, np.nan),
    )
    masses = np.sqrt(stable_mass_squared)
    return masses[keep]
