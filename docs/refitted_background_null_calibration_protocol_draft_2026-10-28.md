# Draft protocol: refitted-background null calibration

**Status: draft for review; not preregistered; not a CMS result.**

## Question and estimand

For a specified binned spectrum, fixed null-generating mean vector, fixed-order background family, and fixed set of scan-window widths, what fraction of independent null pseudoexperiments are rejected by the empirical upper-tail rank test at nominal level alpha when the background is refit independently in every pseudoexperiment?

The target is a toy-model operating characteristic, not a discovery claim and not a claim of uniform type-I error control over all plausible CMS backgrounds.

## Procedure currently implemented

1. Freeze the binning, number of bins, null-generating mean vector, background polynomial order, window widths, alpha, calibration/evaluation sample sizes, seeds, and fit-failure policy.
2. For each calibration pseudoexperiment, draw independent Poisson counts from the fixed null-generating mean vector.
3. Fit the same fixed-order log-polynomial Poisson background to those counts. A failed fit aborts the run; it is not silently dropped.
4. Compute the same one-sided Poisson excess scan against that pseudoexperiment's fitted means, and store its maximum scan statistic.
5. Repeat steps 2–4 with a separate random seed for the held-out evaluation sample.
6. For each held-out maximum statistic T, calculate p = (1 + count(T_calibration >= T)) / (M + 1). Ties count in the upper tail.
7. Reject when p <= alpha; report the observed rejection fraction and its Wilson score interval. The Wilson interval summarizes binomial Monte Carlo uncertainty; it is not an exact interval.
8. Report the calibration resolution 1/(M+1). If this exceeds alpha, the procedure cannot reject at the requested level. Also report the discrete rejection grid: under iid continuous null statistics, the unconditional rejection probability of the plus-one rank rule is floor(alpha * (M + 1)) / (M + 1); ties may make it more conservative. This is an unconditional rank property, not the conditional rejection rate for one fixed calibration sample.

## Assumptions and limits

- The null-generating means are treated as fixed and known for this experiment. They may be chosen as a scenario or later as a fitted plug-in value, but plug-in use does not by itself guarantee nominal coverage under nuisance uncertainty or misspecification.
- Bins are independent Poisson draws. Correlations, event-level effects, trigger and detector response, event selection, and non-Poisson fluctuations are not represented.
- The background family and polynomial order are fixed. No model-order selection is included.
- The current scan statistic is a one-sided Poisson excess likelihood-ratio statistic over the declared contiguous windows. It is not automatically equivalent to BumpHunter or any official CMS implementation.
- No real-data fit, observed significance, or CMS validation is implied.
- Fit failures are part of the procedure. If failures occur, record their rate and cause; do not change the failure policy after inspecting which results are favorable.

## Required validation before stronger claims

- Run unit and integration tests on supported Python versions.
- Verify the same binning, fitter, scan widths, and failure policy are used for observed and simulated data.
- Check convergence and boundary behavior over a prespecified range of null scenarios.
- Evaluate multiple background shapes, including deliberate misspecification, without selecting only favorable scenarios.
- Report the number of simulations, seeds, rejection counts, Wilson intervals, failures, and calibration resolution.
- Use independent review to determine whether the chosen null scenarios are scientifically defensible.
- Establish data/reference parity and documented selections before describing any result as a CMS-data analysis.

## Stop conditions

Do not report a calibrated discovery p-value if the observed and pseudoexperiment pipelines differ, fit failures are silently excluded, the scan configuration was selected after examining the observed excess, the calibration sample is too small for the requested alpha, or the null assumptions are not documented. Do not make physics claims from these toy simulations.

## Software entry points

- simulate_refitted_background_null: generates null scan maxima with a refit in every toy.
- evaluate_refitted_background_false_positive_rate: compares independent calibration and held-out toy samples and reports the rejection fraction.

Both are research prototypes. CI success, once established, demonstrates software checks—not scientific validity.

## Discrete rank resolution diagnostic

The code now exposes `empirical_rank_test_resolution(n_calibration, alpha)`. It reports the smallest attainable p-value, the maximum number of calibration statistics that may equal or exceed an evaluation statistic while still allowing rejection, and the nominal unconditional rejection probability on the rank grid under an iid continuous null. For example, with `M=100` and `alpha=0.05`, the grid permits rejection only for at most four calibration exceedances, giving unconditional rank-grid size `5/101 ≈ 0.0495`. This diagnostic does not measure conditional size for a fixed calibration sample, nor does it address whether the null scenario is scientifically adequate. The helper is covered by unit tests; its new commits still require CI verification.
