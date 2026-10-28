import numpy as np
import pytest

from cms_dimuon_robustness.background_fit import fit_log_polynomial_background


def test_constant_background_fit_recovers_constant_mean():
    counts = np.full(20, 12, dtype=int)
    result = fit_log_polynomial_background(counts, order=0)
    expected = np.asarray(result["expected_counts"], dtype=float)
    assert result["optimizer_success"] is True
    assert expected.shape == counts.shape
    assert np.allclose(expected, 12.0, rtol=1e-5, atol=1e-5)
    assert result["n_parameters"] == 1
    assert result["polynomial_order"] == 0


def test_linear_log_background_tracks_monotonic_synthetic_spectrum():
    x = np.linspace(-1.0, 1.0, 30)
    expected = 20.0 * np.exp(0.55 * x)
    # Deterministic integer fixture is close to the model and avoids Monte Carlo.
    counts = np.rint(expected).astype(int)
    result = fit_log_polynomial_background(counts, order=1)
    fitted = np.asarray(result["expected_counts"], dtype=float)
    assert np.all(np.isfinite(fitted))
    assert fitted[-1] > fitted[0]
    assert result["optimizer_success"] is True


@pytest.mark.parametrize(
    "counts,order,max_iterations",
    [
        ([], 0, 100),
        ([[1, 2]], 0, 100),
        ([1, -1, 2], 0, 100),
        ([1.5, 2, 3], 0, 100),
        ([1, 2, 3], -1, 100),
        ([1, 2, 3], True, 100),
        ([1, 2, 3], 2, 100),
        ([1, 2, 3], 0, 0),
        ([1, 2, 3], 0, True),
    ],
)
def test_background_fit_rejects_invalid_inputs(counts, order, max_iterations):
    with pytest.raises(ValueError):
        fit_log_polynomial_background(counts, order, max_iterations)


def test_all_zero_spectrum_returns_finite_bounded_fit():
    result = fit_log_polynomial_background(np.zeros(12, dtype=int), order=0)
    expected = np.asarray(result["expected_counts"], dtype=float)
    assert np.all(np.isfinite(expected))
    assert np.all(expected > 0)
    assert np.allclose(expected, expected[0])


def test_fit_reports_coefficients_at_optimizer_bounds(monkeypatch):
    from types import SimpleNamespace

    import cms_dimuon_robustness.background_fit as background_fit

    def fake_minimize(*args, **kwargs):
        # Deliberately emulate a nominally successful optimizer returning a
        # coefficient at the hard upper bound; no expensive fit is needed.
        return SimpleNamespace(
            x=np.array([20.0, 0.0]), success=True, message="synthetic boundary fixture"
        )

    monkeypatch.setattr(background_fit, "minimize", fake_minimize)
    result = fit_log_polynomial_background([2, 3, 4, 5], order=1)

    assert result["optimizer_success"] is True
    assert result["coefficient_boundary_active"] is True
    assert result["coefficient_boundary_indices"] == [0]
    assert "inspect fit stability" in result["coefficient_boundary_warning"]


def test_fit_reports_no_boundary_warning_for_interior_solution():
    result = fit_log_polynomial_background(np.full(20, 12, dtype=int), order=0)
    assert result["coefficient_boundary_active"] is False
    assert result["coefficient_boundary_indices"] == []
    assert result["coefficient_boundary_warning"] is None
