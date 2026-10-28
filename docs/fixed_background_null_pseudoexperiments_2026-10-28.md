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
2. Add a separate held-out evaluation stream not used to estimate the empirical p-value.
3. Report false-positive rate with a binomial uncertainty interval across a prespecified set of null scenarios.
4. Add background fitting only after its objective, parameter constraints, fit-failure policy, and uncertainty treatment are frozen.
5. Keep the CMS baseline parity and literature novelty gates independent from toy-model software tests.
