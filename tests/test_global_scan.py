import numpy as np
import pytest

from cms_dimuon_robustness.global_scan import (
    poisson_excess_log_likelihood_ratio,
    scan_poisson_excess,
)


def test_poisson_excess_statistic_is_zero_for_downward_or_equal_fluctuation():
    assert poisson_excess_log_likelihood_ratio(4, 5.0) == 0.0
    assert poisson_excess_log_likelihood_ratio(5, 5.0) == 0.0


def test_poisson_excess_statistic_matches_formula_for_upward_fluctuation():
    expected = 2.0 * (10 * np.log(10 / 5) - (10 - 5))
    assert poisson_excess_log_likelihood_ratio(10, 5.0) == pytest.approx(expected)


def test_scan_finds_injected_contiguous_excess_and_reports_number_of_windows():
    counts = np.array([5, 5, 30, 30, 5, 5])
    background = np.full(6, 5.0)
    result = scan_poisson_excess(counts, background, [1, 2, 3])
    assert result["start_bin"] == 2
    assert result["window_width_bins"] == 2
    assert result["observed_in_best_window"] == 60
    assert result["expected_in_best_window"] == 10.0
    assert result["windows_scanned"] == 15
    assert result["global_statistic_q0"] > 0


def test_scan_statistic_is_zero_when_all_windows_are_downward_fluctuations():
    result = scan_poisson_excess([1, 2, 3], [5, 5, 5], [1, 2])
    assert result["global_statistic_q0"] == 0.0
    # Metadata must identify a real scanned window even when every q0 is zero.
    assert result["start_bin"] == 0
    assert result["window_width_bins"] == 1
    assert result["observed_in_best_window"] == 1
    assert result["expected_in_best_window"] == 5.0


@pytest.mark.parametrize(
    "counts,background,widths",
    [
        ([1, 2], [1], [1]),
        ([[1, 2]], [[1, 2]], [1]),
        ([1, -1], [1, 1], [1]),
        ([1.5, 2], [1, 1], [1]),
        ([1, 2], [1, 0], [1]),
        ([1, 2], [1, 1], []),
        ([1, 2], [1, 1], [0]),
        ([1, 2], [1, 1], [3]),
        ([1, 2], [1, 1], [True]),
    ],
)
def test_scan_rejects_invalid_inputs(counts, background, widths):
    with pytest.raises(ValueError):
        scan_poisson_excess(counts, background, widths)


def test_duplicate_window_widths_do_not_duplicate_scan():
    result = scan_poisson_excess([1, 20, 1], [2, 2, 2], [1, 2, 1])
    assert result["windows_scanned"] == 5



@pytest.mark.parametrize(
    "counts,background,widths",
    [
        ([0, 1, 0, 4], [0.5, 1.5, 2.0, 1.0], [1, 2]),
        ([8, 0, 2, 7, 1], [2.0, 1.0, 2.0, 2.0, 1.0], [3, 1, 2]),
        ([3, 3, 3], [3.0, 3.0, 3.0], [1, 2, 3]),
    ],
)
def test_scan_matches_independent_brute_force_reference(counts, background, widths):
    """Cross-check the optimized scan against a simple, independent loop."""
    observed = np.asarray(counts, dtype=int)
    expected = np.asarray(background, dtype=float)
    unique_widths = list(dict.fromkeys(widths))
    candidates = []
    for width in unique_widths:
        for start in range(len(observed) - width + 1):
            n = int(sum(int(x) for x in observed[start : start + width]))
            b = float(sum(float(x) for x in expected[start : start + width]))
            q = 0.0 if n <= b else 2.0 * (n * np.log(n / b) - (n - b))
            candidates.append((q, start, width, n, b))

    # Python max with the explicit scan-order key reproduces the documented
    # first-encountered tie rule without calling the production statistic.
    best_q = max(candidate[0] for candidate in candidates)
    best = next(candidate for candidate in candidates if candidate[0] == best_q)
    result = scan_poisson_excess(counts, background, widths)

    assert result["global_statistic_q0"] == pytest.approx(best[0])
    assert result["start_bin"] == best[1]
    assert result["window_width_bins"] == best[2]
    assert result["observed_in_best_window"] == best[3]
    assert result["expected_in_best_window"] == pytest.approx(best[4])
    assert result["windows_scanned"] == len(candidates)
