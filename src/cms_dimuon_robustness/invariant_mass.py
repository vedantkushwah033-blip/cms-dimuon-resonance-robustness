"""Kinematic helpers for validating dimuon invariant-mass reconstruction.

These functions calculate kinematics from per-muon (pt, eta, phi, mass) values.
They do not implement CMS trigger, object-quality, luminosity, or event-selection rules.
All momentum and mass values must use the same units (normally GeV).
"""
from __future__ import annotations

import numpy as np


def pair_invariant_mass(
    pt1: np.ndarray | float,
    eta1: np.ndarray | float,
    phi1: np.ndarray | float,
    mass1: np.ndarray | float,
    pt2: np.ndarray | float,
    eta2: np.ndarray | float,
    phi2: np.ndarray | float,
    mass2: np.ndarray | float,
) -> np.ndarray:
    """Return invariant mass for one or more muon pairs, using cylindrical coordinates.

    Inputs are broadcast using NumPy rules. pt and masses must be non-negative;
    all values must be finite. The output has the broadcast shape and is in the
    same momentum units as the input.
    """
    values = [np.asarray(v, dtype=float) for v in
              (pt1, eta1, phi1, mass1, pt2, eta2, phi2, mass2)]
    if any(not np.all(np.isfinite(v)) for v in values):
        raise ValueError("all kinematic inputs must be finite")

    pta, etaa, phia, ma, ptb, etab, phib, mb = np.broadcast_arrays(*values)
    if np.any(pta < 0) or np.any(ptb < 0):
        raise ValueError("transverse momentum must be non-negative")
    if np.any(ma < 0) or np.any(mb < 0):
        raise ValueError("particle mass must be non-negative")

    px1 = pta * np.cos(phia)
    py1 = pta * np.sin(phia)
    pz1 = pta * np.sinh(etaa)
    e1 = np.sqrt((pta * np.cosh(etaa)) ** 2 + ma**2)

    px2 = ptb * np.cos(phib)
    py2 = ptb * np.sin(phib)
    pz2 = ptb * np.sinh(etab)
    e2 = np.sqrt((ptb * np.cosh(etab)) ** 2 + mb**2)

    mass_squared = (e1 + e2) ** 2 - (px1 + px2) ** 2 - (py1 + py2) ** 2 - (pz1 + pz2) ** 2
    # Small negative values can arise from floating-point cancellation at very low mass.
    return np.sqrt(np.maximum(mass_squared, 0.0))
