# Exploratory fit-stability audit plan — 2026-10-28

## Status and scope

**Status: proposed exploratory protocol; not preregistered, not externally reviewed, and not run.**

This plan addresses one narrow question: when the fixed-order log-polynomial Poisson background fitter is applied to declared synthetic spectra, how often does it encounter numerical boundary activity or fit failure, and how sensitive is the resulting global scan statistic to those conditions?

This is a software/statistical diagnostic plan. It is not evidence about CMS data, not a resonance search result, and not a substitute for a validated detector-level analysis.

## Primary estimands

For each fully specified generating-mean vector and fixed polynomial order, report:

1. Boundary-active fit fraction: number of successful fits with one or more coefficients within the declared tolerance of the hard coefficient bound, divided by the number of attempted fits.
2. Fit-failure fraction: number of attempted fits that raise a fitting exception or return invalid outputs, divided by the number attempted.
3. Scan-statistic distribution among successful fits, with the count of successful fits shown explicitly.
4. Fit diagnostics among successful fits: coefficient vectors, gradient infinity norm, optimizer message, fitted expected counts, and whether any coefficient was boundary-active.
5. If a comparison is performed, the paired difference in the global scan statistic for the same generated count vector under two explicitly defined analysis variants. Report the paired distribution, not only separate averages.

Do not combine fit failures with ordinary scan-statistic values, and do not silently drop failures from the denominator. A run that fails to complete the prespecified number of attempts must report that fact.

## Scenario construction

Use only scenarios whose numerical parameters, bin count, polynomial order, and rationale have been recorded before generating the audit sample. Candidate families already represented in the repository include:

- a baseline log-polynomial mean;
- a smooth-curvature mean;
- a positive localized shoulder added to a baseline.

The scenario definitions must be explicit vectors of strictly positive expected counts. The shoulder is a deliberately simplified stress test, not a detector or physical background model. Do not choose scenario parameters after examining which ones produce favorable false-positive rates.

## Randomness and reproducibility

- Assign a fixed, documented seed to each scenario and each distinct purpose.
- Keep exploratory diagnostic samples separate from any future calibration and held-out evaluation samples.
- Record the repository commit, Python and dependency versions, scenario parameters, bin count, scan widths, fit order, coefficient bound, boundary tolerance, and all seeds.
- Re-running the same code, inputs, and environment should reproduce the same generated data and summaries.

## Interpretation of boundary activity

Boundary activity is a warning signal, not automatically proof that a fit is invalid. A boundary-active fit can still be numerically finite and optimizer-successful, while its solution may nevertheless be sensitive to the imposed bound or model form.

Therefore:
- report boundary activity rather than automatically excluding such fits;
- do not treat optimizer success alone as evidence of model adequacy;
- do not change the bound or tolerance after seeing results without documenting the change as a new exploratory analysis;
- if a boundary-active fit has an unusually large gradient or a materially unstable fitted shape, record that as a separate diagnostic;
- define any exclusion, retry, or failure-handling rule before a confirmatory run.

## Minimum audit outputs

Produce a machine-readable table with one row per attempted pseudoexperiment, or an equivalent lossless record, containing at minimum:

`scenario_id`, `replicate_id`, `seed`, `fit_succeeded`, `failure_reason`, `optimizer_success`, `boundary_active`, `boundary_indices`, `gradient_infinity_norm`, `negative_log_likelihood_without_constants`, and `global_statistic_q0` when available.

Also produce a scenario-level summary with attempted count, successful count, failure count and rate, boundary-active count and rate among successful fits, and a clear statement of the denominator used for each rate. If boundary rate among all attempts is reported, failures must not be silently counted as non-boundary fits.

## Stop conditions

Stop and resolve the software or protocol issue before interpreting the scenario if any of the following occurs:

- non-finite fitted means, coefficients, objective, gradient, or scan statistic;
- fit failure or invalid output is not recorded with the replicate identity;
- the number of attempted replicates differs from the declared target without explicit reporting;
- scenario parameters, scan widths, or fit settings differ between samples intended to be comparable;
- a result cannot be reproduced from the recorded commit, configuration, and seed.

## Decision gates

1. **Software gate:** tests and lint pass; a deterministic test verifies that a fit failure is attributable to the correct replicate and is not silently dropped.
2. **Exploratory gate:** the audit completes with all attempts accounted for, and diagnostics are inspected without selecting scenarios based on favorable calibration outcomes.
3. **Protocol gate:** an independent reviewer agrees on the estimand, scenarios, fit-failure policy, scan definition, calibration sample size, and acceptance criteria.
4. **Confirmatory gate:** only after the protocol is frozen may a confirmatory simulation be considered. The current project status remains NO-GO until these gates are satisfied.

## Claims explicitly not supported

This audit cannot establish realistic CMS background modelling, trigger efficiency, detector response, reference-spectrum parity, uniform type-I error across unknown backgrounds, or evidence for a physical resonance. Any false-positive estimate is conditional on the exact declared toy-generating scenario and analysis procedure.
