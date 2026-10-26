import numpy as np
import pytest

from cms_dimuon_robustness.histogram import histogram_masses


def test_histogram_range_accounting_and_upper_edge_overflow():
    masses = np.array([0.25, 1.0, 2.0, 3.0, 3.1, np.nan, np.inf, -np.inf])
    counts, summary = histogram_masses(masses, bins=3, mass_min=0.25, mass_max=3.0)
    assert counts.tolist() == [2, 1, 0]
    assert summary == {
        "pairs_total": 8,
        "pairs_nonfinite": 3,
        "pairs_below_range": 0,
        "pairs_in_range": 3,
        "pairs_above_range": 2,
    }
    assert int(counts.sum()) == summary["pairs_in_range"]


def test_empty_input_is_valid():
    counts, summary = histogram_masses([], bins=4, mass_min=0.25, mass_max=4.0)
    assert counts.tolist() == [0, 0, 0, 0]
    assert summary["pairs_total"] == 0
    assert summary["pairs_in_range"] == 0


@pytest.mark.parametrize(
    "kwargs",
    [
        {"bins": 0, "mass_min": 0.25, "mass_max": 3.0},
        {"bins": True, "mass_min": 0.25, "mass_max": 3.0},
        {"bins": 3, "mass_min": 0.0, "mass_max": 3.0},
        {"bins": 3, "mass_min": 3.0, "mass_max": 3.0},
        {"bins": 3, "mass_min": 0.25, "mass_max": np.inf},
    ],
)
def test_invalid_histogram_configuration_raises(kwargs):
    with pytest.raises(ValueError):
        histogram_masses([], **kwargs)
