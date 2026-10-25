import numpy as np
import pytest

from cms_dimuon_robustness.invariant_mass import pair_invariant_mass


def test_back_to_back_massless_pair_has_mass_twice_pt():
    result = pair_invariant_mass(10, 0, 0, 0, 10, 0, np.pi, 0)
    assert float(result) == pytest.approx(20.0, abs=1e-12)


def test_collinear_massless_pair_has_zero_mass():
    result = pair_invariant_mass(10, 0, 0, 0, 15, 0, 0, 0)
    assert float(result) == pytest.approx(0.0, abs=1e-7)


def test_vectorized_inputs_broadcast():
    result = pair_invariant_mass(
        np.array([10.0, 10.0]), 0, 0, 0,
        np.array([10.0, 20.0]), 0, np.array([np.pi, np.pi]), 0,
    )
    assert result.shape == (2,)
    assert result == pytest.approx(np.array([20.0, 30.0]))


def test_nonzero_muon_mass_produces_physical_result():
    muon_mass = 0.105658
    result = pair_invariant_mass(0, 0, 0, muon_mass, 0, 0, 1, muon_mass)
    assert float(result) == pytest.approx(2 * muon_mass, rel=1e-12)


@pytest.mark.parametrize("bad_pt", [-1.0, np.nan, np.inf])
def test_invalid_transverse_momentum_rejected(bad_pt):
    with pytest.raises(ValueError):
        pair_invariant_mass(bad_pt, 0, 0, 0, 10, 0, 1, 0)


def test_negative_mass_rejected():
    with pytest.raises(ValueError):
        pair_invariant_mass(10, 0, 0, -0.1, 10, 0, 1, 0)
