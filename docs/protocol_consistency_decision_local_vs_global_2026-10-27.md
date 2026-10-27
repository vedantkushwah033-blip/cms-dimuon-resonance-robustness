# Protocol consistency decision: local versus global calibration

**Date:** 2026-10-27  
**Status:** design-control note; not preregistered; no confirmatory simulation authorized  
**Branch:** `research-plan/initial-protocol`

## Why this note exists

The candidate calibration protocol currently defines its primary estimand as the difference between an empirical **local** null rejection probability and a nominal local test size. The primary-source literature audit proposes a question about **global** type-I error when the pipeline includes a mass scan. These are different statistical targets. They must not be mixed in the same primary result or described interchangeably.

## Decision rule

The project must choose one of these designs before confirmatory pseudoexperiments:

### Design A — fixed local-window calibration

Use this only if the research question is explicitly restricted to a single prespecified mass window and no search over alternative windows, masses, or analysis configurations is part of the inferential procedure.

- Primary target: end-to-end rejection probability at the declared local test size.
- Repeat every data-dependent operation used inside that fixed-window pipeline in each null toy.
- Do not make global-discovery or look-elsewhere claims.
- A mass scan may be shown only as exploratory unless separately calibrated.

### Design B — global scan calibration

Use this if the procedure scans mass locations, windows, histogram configurations, thresholds, or other alternatives and then reports the most significant result.

- Primary target: global null rejection probability of the *entire prespecified search pipeline*.
- Define one global test statistic (for example, the maximum prespecified local test statistic over the scan) and the exact rejection rule.
- Every null toy must repeat the same fitting, model-selection, scan, and maximization steps as the analysis applied to observed data.
- The nominal global size must be declared before confirmatory runs. Local p-values may be diagnostics, not substitutes for the primary target.
- The calibration generator must represent a defensible background-only null; its adequacy and held-out misspecification scenarios must be justified independently.

## Current project decision

**No primary estimand is frozen. No confirmatory Monte Carlo is authorized.** Given that the proposed scientific motivation involves a bump hunt and scan calibration, Design B is the more coherent candidate *if* a complete scan is actually part of the pipeline. This is not an endorsement of novelty. If implementing and validating the full scan is not yet feasible, use Design A only as a clearly labelled software/calibration pilot—not as evidence for a global claim.

## Minimum gates before choosing/finalizing either design

1. Extract the methods, supplements, calibration targets, and failure handling from the closest primary papers; record page/section evidence in the comparison matrix.
2. Numerically reproduce the relevant documented baseline and define exactly which parts are and are not being reproduced.
3. Write a test-statistic specification with equations, fit range, binning, candidate background families, selection rule, scan grid, and boundary handling.
4. Define terminal statuses for every toy, including fit failure, retry, invalid statistic, rejection, and non-rejection. The end-to-end denominator is all generated toys.
5. Validate the implementation with analytic/toy controls and independently checked calculations before large simulation.
6. Freeze the selected estimand, generator families, comparator, random-seed scheme, sample-size/precision target, and stopping rule in a versioned protocol.

## Reporting guardrails

- Never call a local p-value a global discovery significance.
- Never imply that a larger simulation count repairs a mismatched estimand or weak baseline.
- Report empirical rejection rates with denominator and binomial uncertainty, and report failure rates separately.
- Do not silently remove failed fits from the primary denominator.
- Describe any result as a controlled simulation result unless an appropriate real-data analysis and its assumptions are separately justified.
- Do not claim a novel method or publishability until the literature gap is evidenced and the complete analysis passes validation.

## Immediate next action

Continue primary-source methods extraction and the bounded real-data baseline reproduction. Do not launch the confirmatory simulation campaign yet. No new data from the user is needed for this protocol decision.