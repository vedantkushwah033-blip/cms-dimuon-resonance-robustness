# Focused supplement: acceptance-induced spectral distortion

**Status:** exploratory supplement to `docs/confirmatory_study_protocol_draft.md`, not a replacement or freeze. It is proposed, not preregistered or executed.  
**Prepared:** 2026-10-30  
**Code branch:** research/acceptance-distortion-calibration-2026-10-30  
**Primary evidence class:** model-generated null pseudoexperiments.  
**Observed CMS data role:** descriptive reproduction and external context only until trigger, prescale, certification, and efficiency semantics are independently validated.

## Relationship to the existing protocol\n\nThis document does not resolve the open items in the main confirmatory protocol: the end-to-end pipeline, fair comparator, numerical scenario matrix, fit-failure policy, Monte Carlo precision target, real-data baseline parity, and external review remain open. Do not interpret the candidate P0/P1/P2 procedure labels below as approved implementation choices. The existing repository decision remains NO-GO for confirmatory simulation.\n\n## 1. Narrow research question

For a fully specified local dimuon bump-hunt pipeline, how does its null false-positive rate change when the observed spectrum contains a localized or smoothly varying acceptance distortion that is not represented in the fitted background model? Can a predeclared acceptance-aware model or sideband-only diagnostic improve calibration without absorbing a genuine narrow signal?

This is a candidate methodological question, not an established novelty claim. The known trigger/data-taking-related structure near 30 GeV in the CMS outreach example motivates studying this class of failure mode; it does not establish that a particular acceptance model describes CMS detector response.

## 2. Scope and claims boundary

The study will distinguish three evidence classes in every table and figure:

1. Observed collision data: only exact, versioned CERN records and files with checksums, documented selection, and a reproducible spectrum.
2. Model-generated pseudoexperiments: generated from explicit mathematical null models, with all parameters and random seeds recorded.
3. Stress tests: deliberately misspecified scenarios used to probe failure modes; these are not detector simulations.

No claim of a new resonance, a CMS discovery, a measured trigger efficiency, or a detector-level false-positive rate is permitted. A result from pseudoexperiments is conditional on its generator and fitted procedure. Trigger bits alone do not supply an unbiased trigger-efficiency denominator or prescale correction.

## 3. Primary estimand

For each prespecified null scenario s, estimate the probability that the complete pipeline rejects the null at nominal alpha=0.05, conditional on s. The complete pipeline includes all data-dependent fit-window, background-choice, nuisance-fit, scan, and local-to-global calibration steps that are actually part of the declared analysis. If a step is not implemented, it must not be described as part of the evaluated pipeline.

Report attempted trials, valid fits, failures, rejection count, empirical rejection rate, and a two-sided 95% Clopper-Pearson interval. The nominal 5% target is a reference point, not an acceptance criterion that can be inferred from a single finite simulation.

## 4. Candidate procedures

Freeze a minimal comparison before the main run:

- P0 — fixed background: a single prespecified smooth background family, fit using the declared sideband/window rule.
- P1 — acceptance-aware: the same background plus a low-dimensional, prespecified acceptance-distortion term. Its form and bounds must be justified before evaluation.
- P2 — diagnostic-gated: P0 is used unless a prespecified sideband-only diagnostic triggers P1. The diagnostic must not inspect the signal-window excess used for the test statistic.

P1 and P2 are candidates only. Do not add or remove models after inspecting held-out results. If the proposed acceptance term is not identifiable from sidebands, report that failure; do not silently regularize until the desired answer appears.

## 5. Null-generating scenarios

Use a declared grid of null scenarios, with no injected narrow signal in the primary calibration experiment:

- smooth baseline continuum;
- continuum with a broad curvature change;
- continuum multiplied by a smooth turn-on/turn-off acceptance component;
- continuum with a localized, trigger-like shoulder or efficiency transition;
- combinations of continuum curvature and acceptance distortion;
- boundary and low-count regimes to test numerical stability.

The functional forms, parameter ranges, mass domain, event-count distribution, and parameter-generation distributions must be specified in a machine-readable configuration before the confirmatory run. Do not label any one functional form as the CMS trigger response without detector documentation.

Separate development scenarios (used to debug and tune) from held-out scenarios (used once for final evaluation). Use disjoint random-seed namespaces and record them in the run manifest.

## 6. Signal-injection guardrail

After null calibration is assessed, use a separate signal-injection study to test whether P1/P2 can absorb a narrow excess. Vary signal location, width, and strength over a prespecified grid. Report power and interval coverage separately from null rejection. A method that reduces false positives by erasing injected signals is not an improvement.

The injected signal is a mathematical template, not a claim about a physical resonance.

## 7. Numerical and statistical requirements

- Prefer an unbinned extended likelihood if its intensity and normalization are correctly implemented; otherwise justify binning and verify bin-width invariance.
- Define the test statistic, parameter constraints, fit bounds, optimizer, convergence criteria, and failure policy before the confirmatory run.
- If the mass location is scanned, calibrate the maximum test statistic across the full scan in each pseudoexperiment. A local p-value is not a global discovery significance.
- Refit nuisance parameters under null and alternative exactly as specified.
- Validate likelihood normalization and nested-model behavior on analytic/synthetic edge cases.
- Use independent implementation checks for invariant mass and, where feasible, the likelihood/test statistic.
- Do not discard failed fits. Report them; define in advance whether they count as non-rejections, trigger a pipeline failure, or are handled by a declared retry rule.
- Report Monte Carlo uncertainty (exact binomial interval) separately from parameter-fit uncertainty.
- Run enough trials to meet a precision target. For a 5% rejection rate, roughly 1,825 independent trials give a 95% normal-approximation half-width near 1 percentage point; use exact intervals for final reporting and increase N if needed.

## 8. Data gate and CMS inputs

The 2012 DoubleMuParked data are not interchangeable across records:

- The public outreach NanoAOD-like record (DOI 10.7483/OPENDATA.CMS.LVG5.QT81) contains 61,540,413 events in one 2.1 GiB file, with reduced muon kinematics and charge. CERN explicitly says no further validation was performed on the reduced output. Use for education/software checks unless additional validation supports a stronger role.
- The research-level Run2012B and Run2012C records are distinct inputs and must be assessed separately. A schema inspection of one file from each period is not equivalent to validating all files, trigger semantics, prescales, or selection efficiency.
- The 2012 public dimuon analysis example warns that a feature near 30 GeV is related to trigger/data-taking conditions. It is a known analysis caveat, not a resonance candidate.

For each observed-data file, store record DOI, file URI, run period, exact file name, byte count, SHA-256, tree name, entry count, branch inventory, software versions, event-selection definition, and a machine-readable provenance manifest. Never infer a branch's semantics from its name alone.

## 9. Reproducibility and audit

Every run must emit:
- frozen configuration and protocol version;
- code commit and environment lock/version report;
- seed per replicate or deterministic seed derivation;
- raw replicate-level CSV/Parquet output;
- aggregate JSON with attempted/valid/failed counts;
- fit-status and boundary-hit diagnostics;
- SHA-256 manifest;
- independent auditor that reconstructs summaries and headline metrics from raw records.

The auditor must not simply compare a saved summary with a duplicate of itself. Where the generator is deterministic and fully specified, independently replay a sample or all seeds. Keep audit code logically separate from the primary analysis implementation.

## 10. Decision rules

- If P1/P2 does not improve calibration on held-out scenarios, report that result and do not tune on the held-out set.
- If P1/P2 improves null calibration but materially reduces signal-injection power, quantify the trade-off; do not declare it superior without a prespecified utility criterion.
- If all candidate methods fail under some scenario, identify the scenario and failure mode rather than hiding it.
- If the novelty review finds an equivalent prior study, narrow the claim to reproducibility/benchmarking or stop the novelty claim.
- No manuscript abstract may report numerical findings until a clean run and independent audit have completed.

## 11. Required outputs before manuscript claims

1. A completed literature comparison of the closest bump-hunt and trigger/acceptance studies.
2. A validated CMS spectrum reproduction with input provenance and a documented explanation of the known 30 GeV feature.
3. A frozen machine-readable experiment configuration.
4. Passing unit, integration, numerical, and independent-audit tests.
5. Confirmatory null-calibration and signal-injection outputs.
6. A manuscript with explicit separation of observed-data, pseudoexperiment, and stress-test evidence.
7. Independent review by a particle-physics/statistics researcher.

**Current decision: NO-GO for confirmatory simulation remains unchanged.** This supplement only sharpens one candidate acceptance-distortion direction. The governing documents remain `docs/confirmatory_study_protocol_draft.md`, `docs/confirmatory_protocol_freeze_checklist.md`, and `docs/next_experiment_decision.md`. No confirmatory experiment, real-data parity result, detector-level trigger validation, or novelty finding is claimed by this document.
