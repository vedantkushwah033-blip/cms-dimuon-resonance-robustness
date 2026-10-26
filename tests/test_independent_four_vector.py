import numpy as np

from cms_dimuon_robustness.invariant_mass import pair_invariant_mass


def _independent_four_vector_mass(pt1, eta1, phi1, m1, pt2, eta2, phi2, m2):
    """Independent reference using explicit (E, px, py, pz) four-vectors."""
    def vector(pt, eta, phi, mass):
        px = pt * np.cos(phi)
        py = pt * np.sin(phi)
        pz = pt * np.sinh(eta)
        energy = np.sqrt(px**2 + py**2 + pz**2 + mass**2)
        return energy, px, py, pz

    a = vector(pt1, eta1, phi1, m1)
    b = vector(pt2, eta2, phi2, m2)
    mass_squared = (a[0] + b[0])**2 - sum((a[i] + b[i])**2 for i in (1, 2, 3))
    return np.sqrt(max(mass_squared, 0.0))


def test_vectorized_mass_matches_independent_four_vector_reference():
    rng = np.random.default_rng(20261026)
    count = 250
    pt1 = rng.uniform(0.5, 100.0, count)
    pt2 = rng.uniform(0.5, 100.0, count)
    eta1 = rng.uniform(-2.4, 2.4, count)
    eta2 = rng.uniform(-2.4, 2.4, count)
    phi1 = rng.uniform(-np.pi, np.pi, count)
    phi2 = rng.uniform(-np.pi, np.pi, count)
    mass1 = rng.uniform(0.105, 0.106, count)
    mass2 = rng.uniform(0.105, 0.106, count)

    actual = pair_invariant_mass(pt1, eta1, phi1, mass1, pt2, eta2, phi2, mass2)
    expected = np.array([
        _independent_four_vector_mass(*row)
        for row in zip(pt1, eta1, phi1, mass1, pt2, eta2, phi2, mass2)
    ])
    np.testing.assert_allclose(actual, expected, rtol=2e-12, atol=2e-10)
