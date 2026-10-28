import pytest

from cms_dimuon_robustness.calibration import empirical_upper_tail_pvalue


def test_plus_one_rank_pvalue():
    result = empirical_upper_tail_pvalue(5.0, [1, 2, 3, 4])
    assert result["empirical_pvalue"] == 0.2
    assert result["minimum_resolvable_pvalue"] == 0.2
    assert result["exceedances_or_ties"] == 0
    assert result["n_calibration"] == 4


def test_calibration_counts_ties_in_upper_tail():
    result = empirical_upper_tail_pvalue(3.0, [2, 3, 3, 4])
    assert result["exceedances_or_ties"] == 3
    assert result["empirical_pvalue"] == 0.8


@pytest.mark.parametrize(
    "observed,null",
    [
        (float("nan"), [1.0]),
        (1.0, []),
        (1.0, [[1.0, 2.0]]),
        (1.0, [1.0, float("inf")]),
    ],
)
def test_calibration_rejects_invalid_inputs(observed, null):
    with pytest.raises(ValueError):
        empirical_upper_tail_pvalue(observed, null)
