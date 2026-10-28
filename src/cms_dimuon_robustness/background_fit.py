"""Fixed-order binned Poisson log-polynomial background fitting.

This is an exploratory modelling primitive, not a validated CMS background model.
It deliberately performs no model selection and provides no uncertainty propagation.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike
from scipy.optimize import minimize


def fit_log_polynomial_background(
    counts: ArrayLike,
    order: int = 1,
    max_iterations: int = 10_000,
) -> dict[str, object]:
    """Fit a fixed-order log-polynomial mean by binned Poisson maximum likelihood.

    For bin index i, the fitted mean is mu_i = exp(sum_j beta_j x_i**j), where
    x is the bin-center coordinate linearly scaled to [-1, 1]. The objective is
    the Poisson negative log likelihood with count-only constants omitted.

    The polynomial order is fixed by the caller; no order selection is performed.
    Coefficients are bounded to [-20, 20] for numerical protection. A failed or
    non-finite optimization raises RuntimeError instead of silently returning a
    background. This model is a software prototype, not a claim of physical
    adequacy for any particular dimuon mass range.
    """
    observed = np.asarray(counts)
    if observed.ndim != 1 or observed.size == 0:
        raise ValueError("counts must be a non-empty one-dimensional array")
    if not np.all(np.isfinite(observed)) or np.any(observed < 0):
        raise ValueError("counts must be finite and non-negative")
    if not np.all(observed == np.floor(observed)):
        raise ValueError("counts must be integer-valued")
    if isinstance(order, bool) or not isinstance(order, (int, np.integer)) or order < 0:
        raise ValueError("order must be a non-negative integer")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, (int, np.integer)):
        raise ValueError("max_iterations must be a positive integer")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be a positive integer")
    if observed.size <= int(order) + 1:
        raise ValueError("number of bins must exceed the number of fitted coefficients")

    y = observed.astype(float, copy=False)
    x = np.linspace(-1.0, 1.0, y.size)
    design = np.vander(x, N=int(order) + 1, increasing=True)
    initial = np.zeros(int(order) + 1, dtype=float)
    initial[0] = np.log(max(float(np.mean(y)), 0.5))

    def objective(beta: np.ndarray) -> tuple[float, np.ndarray]:
        eta = design @ beta
        # Bounds make eta finite and keep exp(eta) in a safe numeric range.
        mu = np.exp(eta)
        value = float(np.sum(mu - y * eta))
        gradient = design.T @ (mu - y)
        return value, gradient

    result = minimize(
        objective,
        initial,
        method="L-BFGS-B",
        jac=True,
        bounds=[(-20.0, 20.0)] * (int(order) + 1),
        options={"maxiter": int(max_iterations), "ftol": 1e-12, "gtol": 1e-8},
    )
    beta = np.asarray(result.x, dtype=float)
    coefficient_bound = 20.0
    # Treat coefficients within this absolute tolerance of a hard optimizer
    # bound as boundary-active; this is a diagnostic, not a fit-failure rule.
    boundary_tolerance = 1e-6
    boundary_indices = [
        int(i)
        for i, value in enumerate(beta)
        if abs(abs(float(value)) - coefficient_bound) <= boundary_tolerance
    ]
    eta = design @ beta
    fitted = np.exp(eta)
    objective_value, gradient = objective(beta)
    # The raw gradient can remain large at a legitimate constrained optimum.
    # Report a box-constraint projected gradient as a separate KKT diagnostic:
    # outward-pointing components at active bounds are zeroed, while inward-
    # pointing components remain visible. This is diagnostic, not a guarantee
    # that the optimizer found a global optimum.
    projected_gradient = gradient.copy()
    at_lower = beta <= -coefficient_bound + boundary_tolerance
    at_upper = beta >= coefficient_bound - boundary_tolerance
    projected_gradient[at_lower & (gradient > 0)] = 0.0
    projected_gradient[at_upper & (gradient < 0)] = 0.0
    if (
        not result.success
        or not np.all(np.isfinite(beta))
        or not np.all(np.isfinite(fitted))
        or not np.isfinite(objective_value)
        or not np.all(np.isfinite(gradient))
    ):
        raise RuntimeError(f"background fit failed: {result.message}")

    return {
        "expected_counts": fitted.tolist(),
        "coefficients": beta.tolist(),
        "polynomial_order": int(order),
        "negative_log_likelihood_without_constants": float(objective_value),
        "gradient_infinity_norm": float(np.max(np.abs(gradient))),
        "projected_gradient_infinity_norm": float(np.max(np.abs(projected_gradient))),
        "coefficient_bound": coefficient_bound,
        "coefficient_boundary_tolerance": boundary_tolerance,
        "coefficient_boundary_indices": boundary_indices,
        "coefficient_boundary_active": bool(boundary_indices),
        "coefficient_boundary_warning": (
            "one or more fitted coefficients are at the optimizer bound; "
            "inspect fit stability before interpreting this fit"
            if boundary_indices
            else None
        ),
        "optimizer_success": True,
        "optimizer_message": str(result.message),
        "n_bins": int(y.size),
        "n_parameters": int(beta.size),
        "interpretation": (
            "fixed-order exploratory Poisson fit; no model selection, parameter "
            "uncertainty propagation, or CMS background validation"
        ),
    }
