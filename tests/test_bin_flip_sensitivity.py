import numpy as np
from scripts.estimate_bin_flip_sensitivity import direct_mass, run
from cms_dimuon_robustness.invariant_mass import pair_invariant_mass

def test_direct_and_stable_formulas_agree_to_rounding_on_generic_pairs():
    rng = np.random.default_rng(3)
    n = 20000
    s = (rng.uniform(5, 80, n).astype(np.float32), rng.uniform(-2, 2, n).astype(np.float32),
         rng.uniform(-3, 3, n).astype(np.float32), np.full(n, 0.10566, np.float32),
         rng.uniform(5, 80, n).astype(np.float32), rng.uniform(-2, 2, n).astype(np.float32),
         rng.uniform(-3, 3, n).astype(np.float32), np.full(n, 0.10566, np.float32))
    a, b = pair_invariant_mass(*s), direct_mass(*s)
    assert np.max(np.abs(a - b) / a) < 1e-8

def test_small_run_is_deterministic_and_reports_both_kinds():
    r1, r2 = run(50_000, 2, seed=1), run(50_000, 2, seed=1)
    assert r1 == r2 and set(r1["kinds"]) == {"generic", "collinear"}
    for item in r1["kinds"].values():
        assert item["pairs_in_range_stable_formula"] > 0
        assert item["pairs_in_range_for_both_formulas"] > 0
        assert item["bin_disagreements_stable_vs_direct"] >= 0
        bound = item["upper_95pct_conditional_bin_flip_rate_if_zero_observed_rule_of_three"]
        if item["bin_disagreements_stable_vs_direct"] == 0:
            assert np.isclose(
                bound, 3.0 / item["pairs_in_range_for_both_formulas"]
            )
        else:
            assert bound is None
