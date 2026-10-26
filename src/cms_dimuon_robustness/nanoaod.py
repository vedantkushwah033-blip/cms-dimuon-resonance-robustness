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
    multiplicities = {field: ak.num(arrays[field], axis=1) for field in required_fields}
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

    # ROOT NanoAOD kinematic branches are commonly float32. Promote before
    # arithmetic, then use a cancellation-resistant expression for the mass.
    # The direct E**2-|p|**2 form can lose the physical mass for highly boosted,
    # nearly collinear pairs because it subtracts large, nearly equal values.
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

    pt1, eta1, phi1, mass1 = (
        pairs.mu1.pt, pairs.mu1.eta, pairs.mu1.phi, pairs.mu1.mass
    )
    pt2, eta2, phi2, mass2 = (
        pairs.mu2.pt, pairs.mu2.eta, pairs.mu2.phi, pairs.mu2.mass
    )
    mt1 = np.hypot(pt1, mass1)
    mt2 = np.hypot(pt2, mass2)
    ratio1 = ak.where(mt1 > 0, pt1 / mt1, 0.0)
    ratio2 = ak.where(mt2 > 0, pt2 / mt2, 0.0)
    y1 = np.arcsinh(ratio1 * np.sinh(eta1))
    y2 = np.arcsinh(ratio2 * np.sinh(eta2))
    delta_y = y1 - y2
    delta_phi = phi1 - phi2

    # Rationalized mT1*mT2 - pt1*pt2 avoids cancellation of the mass-dependent
    # term at high pT. Half-angle identities avoid cancellation near delta=0.
    denominator = mt1 * mt2 + pt1 * pt2
    numerator = mass1**2 * pt2**2 + mass2**2 * pt1**2 + mass1**2 * mass2**2
    transverse_mass_difference = ak.where(
        denominator > 0, numerator / denominator, 0.0
    )
    mass_squared = (
        mass1**2
        + mass2**2
        + 2.0
        * (
            transverse_mass_difference
            + 2.0 * mt1 * mt2 * np.sinh(delta_y / 2.0) ** 2
            + 2.0 * pt1 * pt2 * np.sin(delta_phi / 2.0) ** 2
        )
    )
    masses = np.sqrt(np.maximum(mass_squared, 0.0))
    return masses[keep]
