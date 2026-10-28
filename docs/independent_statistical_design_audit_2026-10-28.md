# Independent statistical-design audit

**Status:** review memo; not preregistration, not an independent external review, not a CMS result.

## Scope

This is a methodological review of the repository's refitted-background empirical-rank calibration prototype and proposed scenario grid. It is based on the current source and design documents. It does not certify the scientific validity of the analysis, the physical relevance of the scenarios, or any CMS-data result.

## Summary decision

**Software-validation gate: pass on the checked revision. Confirmatory-simulation gate: NO-GO until the design below is frozen and reviewed. CMS-data interpretation gate: NO-GO until provenance, event selection, and reference-spectrum parity are independently established.**

The current estimator answers a narrow and useful question: for a specified vector of Poisson generating means, fixed fit family/order, binning, and scan windows, what is the held-out rejection fraction of an empirical upper-tail rank test calibrated on independent toys? It does not establish uniform type-I error control over unspecified backgrounds or a calibrated discovery claim for CMS data.

## Findings

### 1. Define the estimand narrowly

For each fixed scenario, report the held-out rejection fraction at the declared nominal level. Do not describe it as a universal false-positive rate, a guarantee over nuisance parameters, or a CMS discovery p-value. Distinguish:
- the nominal test level alpha;
- the Monte Carlo estimate of rejection probability under one scenario;
- uncertainty due to finite calibration/evaluation samples;
- uncertainty about whether the scenario represents relevant backgrounds.

These are different quantities.

### 2. Calibration resolution is necessary but not sufficient

With M calibration toys, the plus-one rank p-value has minimum value 1/(M+1). Requiring 1/(M+1) <= alpha only makes rejection arithmetically possible. It does not ensure adequate precision or power to diagnose modest calibration error. Before a confirmatory run, specify a precision target for the held-out rejection fraction and justify both calibration and evaluation sizes against it. Record the exact integer rejection count alongside the fraction and interval.

### 3. State the dependence structure of the reported interval

Conditional on a fixed calibration sample, held-out toys are independent draws, so the held-out rejection indicators are conditionally Bernoulli under the fixed scenario. A Wilson interval summarizes finite evaluation-sample uncertainty for that conditional rejection probability. It does not include uncertainty about scenario choice, calibration-sample variation, nuisance-model uncertainty, or scientific realism. If the intended estimand averages over calibration samples too, design a separate repeated-calibration experiment rather than silently interpreting one Wilson interval that way.

### 4. Treat the complete scan as the test

The maximum statistic must be formed using the full prespecified collection of windows. Freeze bin edges, mass range, allowed widths, edge conventions, statistic, and tie handling before any observed-data inspection used to motivate a result. Any change to the scan after examining an observed feature creates a new analysis and requires new independent calibration.

### 5. Make the null family a real design, not a list of labels

S0–S3 are currently families of mathematical examples, not fully specified scenarios. Before confirmatory work, record for each scenario:
- the exact mean-vector formula and numerical parameters;
- bin count, bin edges, and expected total count;
- fit order and scan widths;
- why the perturbation is relevant to the intended statistical failure mode;
- whether its parameters were chosen in development/pilot work;
- the limitations of the scenario.

Do not choose the final grid because it yields striking rejection rates. Include all prespecified scenarios in the report. S5 must remain excluded until an overdispersed generator and its tests are implemented and independently checked.

### 6. Fit failures and convergence are part of the result

The current policy aborts on a failed fit, which avoids silently conditioning the result on successful fits. A pilot should quantify optimizer failure and boundary behavior. Freeze a deterministic policy before confirmatory work: abort the full scenario and report failure, or define a scientifically justified alternative policy in advance. Never change the policy after seeing whether the result is favorable.

### 7. Matched-model behavior does not validate misspecification robustness

A log-linear generating mean with a log-linear fitted model is a baseline implementation check. Curvature, higher-order shapes, and a local shoulder test specific forms of misspecification. Results generalize only to the scenarios and parameter ranges tested. They do not establish robustness to all smooth backgrounds, data-driven model selection, event-level effects, trigger/selection effects, detector response, or non-Poisson fluctuations.

### 8. Separate statistical software validation from data validation

CI and synthetic ROOT tests establish software properties only. A CMS-data claim additionally requires data provenance, validated object definitions, documented event and muon selections, invariant-mass construction, trigger/data-taking interpretation, and quantitative reference-spectrum parity under matching binning and selection. A visible feature near a trigger threshold must not be presented as a resonance without a validated physics interpretation.

## Pre-confirmatory checklist

- [ ] Independent reviewer approves the estimand and limits of interpretation.
- [ ] Exact bin edges, mass range, scan widths, statistic, and tie convention are frozen.
- [ ] All scenario mean vectors and numerical parameters are frozen with written rationale.
- [ ] Calibration and evaluation sample sizes meet a stated precision target, not merely the minimum p-value-resolution condition.
- [ ] Development/pilot seeds are separated from confirmatory seeds; all seeds and software versions are recorded.
- [ ] Fit-failure and optimizer-convergence reporting policy is frozen.
- [ ] Every prespecified scenario will be reported, regardless of outcome.
- [ ] The exact commit passes tests and lint before the run.
- [ ] The resulting artifacts include the full design, per-scenario counts, fractions, intervals, failures, seeds, and commit SHA.
- [ ] Any planned CMS-data interpretation has a separate data-provenance and reference-parity sign-off.

## Stop conditions

Do not launch a confirmatory run if numerical scenario choices are still being adjusted based on attractive results, if the sample-size target is unstated, if the fit-failure policy is ambiguous, or if the analysis pipeline differs between the observed statistic and pseudoexperiments. Do not claim a CMS-calibrated discovery probability from this toy framework.

## Recommended next milestone

Have a researcher who is not implementing this code review the estimand, scenario rationale, scan definition, and sample-size target. Incorporate their comments before freezing the design. Until that review is available, continue only software checks and clearly labeled development work.
