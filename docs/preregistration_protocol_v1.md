# Preregistered Statistical Experiment Protocol (v1.0 — proposed, not frozen)

**Status:** Draft protocol. Do not describe experiments as preregistered until the team records a dated, immutable release/commit and documents any deviations.

## 1. Purpose and claim boundary

Evaluate the empirical false-positive rate of a fully specified *local* dimuon bump-hunt procedure under a limited, declared family of background-generating conditions. This protocol does not search for or claim discovery of a new particle. It does not estimate a detector trigger efficiency unless the necessary trigger, prescale, selection, and luminosity information is independently established.

## 2. Research question

For a prespecified local resonance-search procedure, how does false-positive calibration change when the background-generating distribution departs from the fitted background family, and how well does a diagnostic specified before evaluation identify such miscalibration on held-out scenarios?

The novelty of this question is **not established**. A literature review must compare the exact estimand, background families, selection procedure, diagnostics, and validation design with prior work before any originality claim is made.

## 3. Units, estimand, and hypotheses

- **Experimental unit:** one independently generated background-only pseudoexperiment, including the entire analysis procedure.
- **Primary estimand:** empirical probability that the prespecified local test rejects the background-only null at nominal level alpha under each declared generating scenario.
- **Primary alpha:** 0.05, unless a dated protocol amendment made before examining main-run results justifies another value.
- **Calibration comparison:** empirical rejection rate minus nominal alpha, with a binomial confidence interval and Monte Carlo standard error.
- **Secondary estimands:** fit-failure rate, interval coverage where defined, and power under separately declared signal-injection scenarios. Power results must not be mixed with null calibration results.

## 4. Data roles

Keep these sources separate in all code, tables, plots, and prose:

1. **Real CMS data:** used for provenance checks and baseline-spectrum reproduction only, subject to documented selections and available metadata.
2. **In-model null pseudoexperiments:** generated under the fitted background family to check implementation and nominal calibration.
3. **Misspecified null pseudoexperiments:** generated from prespecified alternative distributions to measure robustness.
4. **Signal-injection pseudoexperiments:** optional, reported separately as power/sensitivity studies.

Synthetic distortion parameters are not measurements of CMS trigger performance. If trigger-related effects cannot be identified from official documentation and available data, describe them as generic acceptance-like stress tests.

## 5. Scenarios and selection safeguards

Before the main run, define and version:
- The fit range and binning or unbinned likelihood.
- The background candidate family and parameter bounds.
- The signal shape, mass points, and local test statistic.
- Whether background-family selection occurs, and exactly how it occurs.
- The alternative generating families and parameter ranges.
- The diagnostic and its decision threshold.
- Fit-failure and boundary-fit handling.
- The random-number generator and seed-generation scheme.

Use development scenarios to implement and debug. Freeze a separate held-out scenario set before main evaluation. Do not tune the diagnostic or choose the preferred model using held-out outcomes. Any exploratory changes must be labeled exploratory and followed by a fresh held-out evaluation.

## 6. Monte Carlo size and precision

Use a small smoke test first, then a pilot (initial planning value: 500 pseudoexperiments per scenario) to measure runtime, convergence, and failure rates. The pilot is not a confirmatory result.

For a rejection-rate estimate p-hat from N independent pseudoexperiments, report the binomial confidence interval and Monte Carlo standard error sqrt[p-hat(1-p-hat)/N]. Choose the main N based on a prespecified precision target and observed pilot behaviour; 10,000 per scenario is only an initial planning candidate, not an automatic guarantee of adequacy.

Do not claim empirical validation of extremely small tail probabilities (for example, five-sigma probabilities) from a simulation budget incapable of resolving those tails. Any rare-event method requires separate validation and explicit assumptions.

## 7. Fit failures and missing outcomes

Predefine failure categories: optimizer failure, invalid covariance/Hessian, non-finite likelihood or statistic, parameter-boundary solution, and invalid generated sample. Report counts and rates by scenario.

Never silently drop failed fits. The primary analysis must state whether failures count as non-rejections, trigger a prespecified retry, or make a scenario inconclusive. Report sensitivity to the chosen rule. Retries must be deterministic and logged.

## 8. Reproducibility requirements

Every run must record:
- Git commit SHA and clean/dirty state when available.
- Configuration file and its checksum.
- Data record identifier, file path, file size, and SHA-256 for local input files.
- Python and dependency versions.
- RNG algorithm and master seed.
- Scenario identifier, replicate count, and runtime.
- Counts of successful fits, failures, exclusions, and rejections.
- Output checksums.

Store raw per-replicate outcomes or sufficient audit data, not only aggregated plots. A fresh environment should be able to reproduce a small test run from documented commands.

## 9. Statistical reporting

For every scenario report N attempted, N valid, failures, number of rejections, empirical rejection rate, confidence interval, and Monte Carlo standard error. Show all prespecified scenarios, including null or unfavorable outcomes. Distinguish Monte Carlo error from uncertainty in the choice of generating model and from uncertainty in the real-data baseline.

Avoid selective reporting, post-hoc threshold tuning, and causal claims about real detector behaviour from synthetic stress tests.

## 10. Validation and independent scrutiny

Required before a strong scientific conclusion:
1. Unit tests for likelihood, test statistic, and fit-failure handling.
2. Independent numerical checks on a small subset of fits.
3. Simulation-based calibration under a known correctly specified null.
4. Repeated-seed reproducibility check.
5. Held-out scenario evaluation.
6. Independent review by a technically qualified person who is given the protocol, code, and results before seeing a persuasive narrative.
7. Recorded issues and responses; unresolved issues must remain visible.

Automated tests establish software behaviour in tested cases; they do not by themselves establish scientific validity or novelty.

## 11. Decision gates

- **Gate A — data:** actual file schema, provenance, selections, and reference baseline are checked.
- **Gate B — literature:** closest prior work is reviewed and the precise contribution is defensible.
- **Gate C — implementation:** tests and independent numerical checks pass.
- **Gate D — protocol freeze:** scenarios, estimands, thresholds, seeds, failure rules, and main N are versioned before main outcomes are examined.
- **Gate E — validation:** held-out results and sensitivity checks are complete.
- **Gate F — scrutiny:** independent technical feedback is documented and addressed.

If a gate fails, repair the issue or narrow the claims. Do not bypass a gate to preserve a preferred conclusion.

## 12. Deviations log

Record each deviation with date, commit, reason, whether outcomes had been inspected, and which analyses it affects. Label results affected by post-hoc changes exploratory.

## 13. Current status

This is a proposed protocol, not evidence that the data have been reproduced, the novelty gap has been established, the main experiment has run, or an independent review has occurred. Those claims may be updated only when supported by inspectable artifacts.
