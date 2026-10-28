import numpy as np
import pytest

from cms_dimuon_robustness.null_scenarios import (
    local_shoulder_null_means,
    log_polynomial_null_means,
)


def test_log_polynomial_generator_matches_exponential_definition():
    coefficients = [np.log(12.0), 0.25]
    actual = np.asarray(log_polynomial_null_means(coefficients, 9))
    x = np.linspace(-1.0, 1.0, 9)
    expected = np.exp(coefficients[0] + coefficients[1] * x)
    np.testing.assert_allclose(actual, expected, rtol=1e-13, atol=0.0)
    assert np.all(actual > 0)


def test_quadratic_generator_has_symmetric_curvature_for_zero_slope():
    means = np.asarray(log_polynomial_null_means([1.0, 0.0, 0.7], 11))
    np.testing.assert_allclose(means, means[::-1], rtol=1e-13, atol=0.0)
    assert means[0] > means[5]


def test_local_shoulder_is_additive_and_centered_on_nearest_bin():
    baseline = np.asarray(log_polynomial_null_means([2.0, 0.0], 9))
    actual = np.asarray(local_shoulder_null_means([2.0, 0.0], 9, 3.0, 0.0, 0.2))
    assert actual[4] == pytest.approx(baseline[4] + 3.0)
    assert actual[0] > baseline[0]
    assert np.all(actual >= baseline)
