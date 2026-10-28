from cms_dimuon_robustness.calibration import empirical_upper_tail_pvalue


def test_plus_one_rank_pvalue():
    result = empirical_upper_tail_pvalue(5.0, [1, 2, 3, 4])
    assert result["empirical_pvalue"] == 0.2
