# Fixed-background Poisson pseudoexperiments: exploratory scope

**Status: exploratory software component; not a CMS result.**

`simulate_fixed_background_null` generates binned counts from independent Poisson distributions with a supplied, fixed expected-background vector. It applies the same declared contiguous-window scan to every pseudoexperiment and records the maximum one-sided Poisson likelihood-ratio statistic. A fixed integer seed makes a run reproducible.

## What this component can test

- Reproducibility for a fixed seed and configuration.
- Whether the scan and calibration functions can be composed into a transparent toy example.
- The behavior of the maximum statistic under a known, fixed Poisson null.

## What it cannot establish

- Correctness of any fitted background model or uncertainty propagation.
- Validity under background misspecification, adaptive model selection, correlated bins, detector effects, trigger selection, or real CMS data.
- Type-I error control merely because pseudoexperiments have been generated. That requires a separate held-out evaluation sample, a predeclared rejection threshold, Monte Carlo uncertainty intervals, and sufficient trial counts.
- Novelty or equivalence to established bump-hunting implementations.

## Required follow-up before inference

1. Verify all tests and lint checks on the branch.
2. Use `evaluate_fixed_background_false_positive_rate` to create separate calibration and held-out evaluation samples with distinct seeds. The function applies plus-one empirical upper-tail p-values to held-out scan maxima and rejects at the supplied `alpha`.
3. Report the held-out false-positive fraction with the returned Wilson score interval. This interval is an approximate binomial interval, not an exact Clopper-Pearson interval. Prespecify the null scenarios, threshold, calibration/evaluation sizes, and seeds before interpreting results.
4. Add background fitting only after its objective, parameter constraints, fit-failure policy, and uncertainty treatment are frozen.
5. Keep the CMS baseline parity and literature novelty gates independent from toy-model software tests.


## Held-out evaluation helper added (2026-10-28)

The code now includes a bounded-memory held-out evaluation helper and a Wilson score interval for the observed rejection fraction. It returns the calibration/evaluation sample sizes, distinct seeds, rejection count, estimated false-positive rate, approximate 95% interval, and whether the calibration sample has enough p-value resolution to permit rejection at the chosen alpha.

This is an implementation milestone, not a validation result. The helper still assumes the supplied background expectation is exactly known and the bins are independent Poisson variables. It does not evaluate fitted-background uncertainty, model misspecification, or detector-level effects. Tests have been added but must pass in CI before the component is considered verified.
