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

    The calculation uses transverse masses and rapidities, and evaluates
    cosh(delta_y)-1 and 1-cos(delta_phi) with half-angle identities. This avoids
    subtracting nearly equal O(E**2) terms for highly boosted, nearly collinear
    pairs, where the direct E**2-|p|**2 expression can erase the physical mass.
    """
    values = [
        np.asarray(v, dtype=float)
        for v in (pt1, eta1, phi1, mass1, pt2, eta2, phi2, mass2)
    ]
    if any(not np.all(np.isfinite(v)) for v in values):
        raise ValueError("all kinematic inputs must be finite")

    pta, etaa, phia, ma, ptb, etab, phib, mb = np.broadcast_arrays(*values)
    if np.any(pta < 0) or np.any(ptb < 0):
        raise ValueError("transverse momentum must be non-negative")
    if np.any(ma < 0) or np.any(mb < 0):
        raise ValueError("particle mass must be non-negative")

    mt1 = np.hypot(pta, ma)
    mt2 = np.hypot(ptb, mb)
    # y = asinh(pz / mT), rewritten to avoid forming large pz values directly.
    ratio1 = np.divide(pta, mt1, out=np.zeros_like(pta), where=mt1 > 0)
    ratio2 = np.divide(ptb, mt2, out=np.zeros_like(ptb), where=mt2 > 0)
    y1 = np.arcsinh(ratio1 * np.sinh(etaa))
    y2 = np.arcsinh(ratio2 * np.sinh(etab))
    delta_y = y1 - y2
    delta_phi = phia - phib

    # Rationalize mT1*mT2 - pt1*pt2; direct subtraction loses the small
    # mass-dependent term when both transverse momenta are very large.
    denominator = mt1 * mt2 + pta * ptb
    numerator = ma**2 * ptb**2 + mb**2 * pta**2 + ma**2 * mb**2
    transverse_mass_difference = np.divide(
        numerator,
        denominator,
        out=np.zeros_like(denominator),
        where=denominator > 0,
    )
    mass_squared = (
        ma**2
        + mb**2
        + 2.0
        * (
            transverse_mass_difference
            + 2.0 * mt1 * mt2 * np.sinh(delta_y / 2.0) ** 2
            + 2.0 * pta * ptb * np.sin(delta_phi / 2.0) ** 2
        )
    )
    # The terms above are non-negative for valid inputs, so a negative result
    # would indicate an arithmetic or input problem rather than a physical mass.
    return np.sqrt(np.maximum(mass_squared, 0.0))
