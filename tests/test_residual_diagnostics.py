import numpy as np
import pytest

from cms_dimuon_robustness.residual_diagnostics import poisson_fit_residual_diagnostics


def test_exact_mean_has_zero_residuals_and_statistics():
    result = poisson_fit_residual_diagnostics([5, 10, 15], [5, 10, 15], 1)
    assert np.allclose(result["pearson_residuals"], 0.0)
    assert np.allclose(result["deviance_residuals"], 0.0)
    assert result["pearson_chi_square_descriptive"] == pytest.approx(0.0)
    assert result["poisson_deviance_descriptive"] == pytest.approx(0.0)
    assert result["nominal_residual_degrees_of_freedom"] == 2


def test_residual_signs_and_zero_observation_deviance_are_correct():
    result = poisson_fit_residual_diagnostics([0, 8, 20], [4, 8, 10], 1)
    pearson = np.asarray(result["pearson_residuals"])
    deviance = np.asarray(result["deviance_residuals"])
    assert pearson[0] < 0 < pearson[2]
    assert deviance[0] == pytest.approx(-np.sqrt(8.0))
    assert deviance[1] == pytest.approx(0.0)
    assert deviance[2] > 0
    assert result["max_absolute_pearson_residual"] == pytest.approx(np.max(np.abs(pearson)))


@pytest.mark.parametrize(
    "observed, expected, n_parameters",
    [
        ([], [], 0),
        ([1, 2], [1], 0),
        ([[1, 2]], [[1, 2]], 0),
        ([1, -1], [1, 2], 0),
        ([1.5, 2], [1, 2], 0),
        ([1, 2], [1, 0], 0),
        ([1, 2], [1, np.inf], 0),
        (["not-a-count", 2], [1, 2], 0),
        ([1, 2], [1, "not-a-mean"], 0),
        ([1, 2], [1, 2], -1),
        ([1, 2], [1, 2], 2),
        ([1, 2], [1, 2], True),
    ],
)
def test_residual_diagnostics_reject_invalid_inputs(observed, expected, n_parameters):
    with pytest.raises(ValueError):
        poisson_fit_residual_diagnostics(observed, expected, n_parameters)


def test_zero_counts_are_handled_without_log_zero():
    result = poisson_fit_residual_diagnostics([0, 0, 0], [0.2, 1.0, 3.0], 1)
    assert np.all(np.isfinite(result["deviance_residuals"]))
    assert result["poisson_deviance_descriptive"] == pytest.approx(8.4)
