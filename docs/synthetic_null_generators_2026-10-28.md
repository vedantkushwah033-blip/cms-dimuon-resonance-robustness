# Synthetic null-generating mean functions

**Status:** implementation utilities for mathematical toy experiments; not a CMS background model and not evidence from data.

`log_polynomial_null_means(coefficients, n_bins)` creates strictly positive bin means using an exponential polynomial. Coefficients are ordered intercept-first, then linear, quadratic, and so on. Its coordinate convention deliberately matches the current fitter's `linspace(-1, 1, n_bins)`.

`local_shoulder_null_means(base_coefficients, n_bins, amplitude, center, width)` adds a positive Gaussian-shaped component to the baseline means. This is a deliberately misspecified toy generator when the fitting family remains a log-polynomial of insufficient order. The center and width are dimensionless normalized coordinates, not mass units.

These helpers only construct expected means. They do not select scientifically justified parameters, run simulations, establish realistic CMS backgrounds, or authorize confirmatory inference. Freeze and independently review parameter values before any confirmatory experiment. Keep development, pilot, calibration, and evaluation random seeds separate.
