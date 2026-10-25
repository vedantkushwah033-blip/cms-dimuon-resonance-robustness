import awkward as ak
import numpy as np
import pytest

from cms_dimuon_robustness.nanoaod import opposite_charge_pair_masses


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
    assert sorted(flat) == pytest.approx(sorted([20.0, np.sqrt(4 * 10.0 * 7.0 * (1 - np.cos(1.0)))]))


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
