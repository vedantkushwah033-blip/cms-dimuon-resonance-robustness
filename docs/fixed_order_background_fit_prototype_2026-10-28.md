# Fixed-order Poisson background-fit prototype

**Status:** exploratory software primitive, not a validated dimuon analysis.

## Model

For bin index i, the prototype fits

\[
Y_i \sim \operatorname{Poisson}(\mu_i), \qquad
\log \mu_i = \sum_{j=0}^{p} \beta_j x_i^j,
\]

where x is the equally spaced bin coordinate scaled to [-1, 1] and p is a caller-specified polynomial order. The fit minimizes the binned Poisson negative log likelihood with count-only constants omitted. L-BFGS-B is used with coefficient bounds [-20, 20]. Non-convergence or non-finite outputs raise an error instead of silently returning a model.

## What this does and does not establish

The module is intended to make the next modelling step testable and explicit. It is **not** a claim that a log-polynomial is a physically suitable background for any particular dimuon mass range.

It currently does not:
- choose the polynomial order or compare candidate background families;
- define a signal region, sideband, fit range, or blinded analysis;
- model signal-plus-background hypotheses;
- propagate fitted-background parameter uncertainty through the scan;
- implement fit diagnostics, goodness-of-fit calibration, or an established-method comparator;
- calibrate the full procedure's global false-positive probability;
- establish agreement with the CMS reference spectrum or detector response.

The order and range must be frozen from a scientific rationale, not chosen because a desired bump becomes more or less significant. The returned coefficient values and gradient norm are diagnostics, not proof of model adequacy. Sparse or pathological spectra may still make a mathematically converged model scientifically unsuitable.

## Tests

`tests/test_background_fit.py` covers a constant-rate fixture, a deterministic monotonic log-linear fixture, invalid inputs, and an all-zero spectrum. These tests check software behavior; they are not evidence of coverage, calibration, physical realism, or real-data performance.

## Gate before connecting it to a scan

Before using this module in a full scan, decide and document: mass range and binning; candidate orders/families and their rationale; fitting constraints; fit-failure handling; residual and goodness-of-fit diagnostics; parameter-uncertainty treatment; model-selection policy; and the exact null generator used to calibrate the complete pipeline. Then validate against an independent comparator and preserve a separate held-out evaluation sample. Confirmatory simulation remains NO-GO until these gates and independent protocol review are complete.
