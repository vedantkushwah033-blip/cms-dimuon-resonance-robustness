# Descriptive Poisson residual diagnostics — 2026-10-28

**Status:** implemented as a software diagnostic; not yet a validated goodness-of-fit test.

## What is implemented

`poisson_fit_residual_diagnostics` accepts observed integer bin counts, strictly positive expected bin means, and the number of fitted parameters. It returns signed Pearson residuals,

\[
r_i^{(P)} = \frac{y_i-\mu_i}{\sqrt{\mu_i}},
\]

signed Poisson deviance residuals,

\[
r_i^{(D)} = \operatorname{sign}(y_i-\mu_i)
\sqrt{2\left[y_i\log(y_i/\mu_i)-(y_i-\mu_i)\right]},
\]

with the continuous-limit convention for zero observed counts, plus descriptive sums of squared Pearson residuals and deviance, maximum absolute residuals, and a nominal residual-degree-of-freedom count.

The implementation validates shapes, finite values, nonnegative integer observations, positive expected means, and parameter-count inputs. Tests include exact-fit zero residuals, positive/negative residual signs, zero-count handling, and invalid inputs.

## Interpretation boundary

These outputs are **descriptive diagnostics**, not calibrated p-values. The nominal residual degrees of freedom do not by themselves justify a chi-square reference distribution. Parameter fitting, leverage, sparse bins, model selection, and uncertainty in the expected background all affect the null distribution. In particular, this helper does not correct for choosing a background order after looking at the spectrum and does not propagate fitted-parameter uncertainty into a scan statistic.

## Next validation gates

1. Complete CI on the commit containing this helper and its tests.
2. Add independently generated misspecified-background fixtures and characterize residual behavior without treating the fixture as a physical CMS model.
3. Decide and freeze mass range, bin edges, candidate background families, and fit-failure rules before connecting residual diagnostics to the scan.
4. Calibrate the *complete frozen procedure* on held-out pseudoexperiments and compare with an established method only after real-data baseline parity and the novelty review are resolved.

No CMS data result, calibrated goodness-of-fit claim, discovery claim, or novelty claim follows from this helper. Confirmatory simulations remain on hold.
