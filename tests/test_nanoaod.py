import awkward as ak
import numpy as np
import pytest

from cms_dimuon_robustness.nanoaod import opposite_charge_pair_masses
from cms_dimuon_robustness.invariant_mass import pair_invariant_mass


def test_opposite_charge_pairs_only_and_known_mass():
    events = ak.Array({
        "Muon_pt": [[10.0, 10.0, 7.0]],
        "Muon_eta": [[0.0, 0.0, 0.0]],
        "Muon_phi": [[0.0, np.pi, 1.0]],
        "Muon_mass": [[0.0, 0.0, 0.0]],
        "Muon_charge": [[1, -1, 1]],
    })
    result = opposite_charge_pair_masses(events)
    flat = ak.to_list(ak.flatten(result, axis=None))
    assert len(flat) == 2
    assert sorted(flat) == pytest.approx(sorted([20.0, np.sqrt(140.0 * (1 + np.cos(1.0)))]))


def test_event_with_fewer_than_two_muons_has_no_pairs():
    events = ak.Array({
        "Muon_pt": [[12.0], []],
        "Muon_eta": [[0.0], []],
        "Muon_phi": [[0.0], []],
        "Muon_mass": [[0.105658], []],
        "Muon_charge": [[1], []],
    })
    result = opposite_charge_pair_masses(events)
    assert ak.to_list(result) == [[], []]


def test_same_sign_pair_is_excluded():
    events = ak.Array({
        "Muon_pt": [[10.0, 10.0]],
        "Muon_eta": [[0.0, 0.0]],
        "Muon_phi": [[0.0, np.pi]],
        "Muon_mass": [[0.105658, 0.105658]],
        "Muon_charge": [[1, 1]],
    })
    assert ak.to_list(opposite_charge_pair_masses(events)) == [[]]


def test_nonfinite_kinematics_are_not_silently_changed_to_zero_mass():
    events = ak.Array(
        {
            "Muon_pt": [[float("nan"), 10.0]],
            "Muon_eta": [[0.0, 0.0]],
            "Muon_phi": [[0.0, np.pi]],
            "Muon_mass": [[0.105658, 0.105658]],
            "Muon_charge": [[1, -1]],
        }
    )
    result = ak.to_list(opposite_charge_pair_masses(events))[0]
    assert len(result) == 1
    assert np.isnan(result[0])



def test_awkward_and_vectorized_invariant_mass_implementations_agree():
    rng = np.random.default_rng(20261026)
    n_events = 100
    fields = {
        "Muon_pt": rng.uniform(1.0, 150.0, (n_events, 2)),
        "Muon_eta": rng.uniform(-2.4, 2.4, (n_events, 2)),
        "Muon_phi": rng.uniform(-np.pi, np.pi, (n_events, 2)),
        "Muon_mass": rng.uniform(0.105, 0.106, (n_events, 2)),
        "Muon_charge": np.tile([1, -1], (n_events, 1)),
    }
    events = ak.Array(fields)
    actual = ak.to_numpy(ak.flatten(opposite_charge_pair_masses(events), axis=None))
    expected = pair_invariant_mass(
        fields["Muon_pt"][:, 0],
        fields["Muon_eta"][:, 0],
        fields["Muon_phi"][:, 0],
        fields["Muon_mass"][:, 0],
        fields["Muon_pt"][:, 1],
        fields["Muon_eta"][:, 1],
        fields["Muon_phi"][:, 1],
        fields["Muon_mass"][:, 1],
    )
    assert actual.shape == expected.shape == (n_events,)
    np.testing.assert_allclose(actual, expected, rtol=2e-12, atol=2e-10)



def test_invalid_muon_charge_values_are_rejected():
    events = ak.Array(
        {
            "Muon_pt": [[10.0, 10.0]],
            "Muon_eta": [[0.0, 0.0]],
            "Muon_phi": [[0.0, np.pi]],
            "Muon_mass": [[0.105658, 0.105658]],
            "Muon_charge": [[0, -1]],
        }
    )
    with pytest.raises(ValueError, match="Muon_charge must contain only"):
        opposite_charge_pair_masses(events)


def test_inconsistent_muon_branch_multiplicities_are_rejected():
    events = ak.Array({
        "Muon_pt": [[10.0, 10.0]],
        "Muon_eta": [[0.0]],
        "Muon_phi": [[0.0, np.pi]],
        "Muon_mass": [[0.105658, 0.105658]],
        "Muon_charge": [[1, -1]],
    })
    with pytest.raises(ValueError, match="multiplicities differ"):
        opposite_charge_pair_masses(events)


def test_multiplicity_error_identifies_first_mismatching_event():
    events = ak.Array({
        "Muon_pt": [[10.0, 10.0], [12.0, 8.0]],
        "Muon_eta": [[0.0, 0.0], [0.0]],
        "Muon_phi": [[0.0, np.pi], [0.0, np.pi]],
        "Muon_mass": [[0.105658, 0.105658], [0.105658, 0.105658]],
        "Muon_charge": [[1, -1], [1, -1]],
    })
    with pytest.raises(ValueError, match=r"event 1 has Muon_pt=2 and Muon_eta=1"):
        opposite_charge_pair_masses(events)

