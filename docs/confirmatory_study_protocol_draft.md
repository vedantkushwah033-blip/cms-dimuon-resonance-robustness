# Confirmatory study protocol — draft, not yet preregistered

**Status:** design draft only. No confirmatory experiment has been run under this protocol.  
**Last updated:** 2026-10-27  
**Scope:** statistical calibration of a prespecified dimuon bump-hunt pipeline under synthetic, acceptance-like distortions.  
**Data status:** the official Run2012B/C research-level ROOT schema audit is still running; this draft does not claim that the files or trigger fields have been validated.

## 1. Why this protocol exists

A simulation study is easy to make look persuasive by trying many background functions, distortion shapes, mass windows, thresholds, and diagnostics and then reporting the best result. This protocol is intended to prevent that failure mode. It separates development scenarios from confirmatory scenarios, requires comparison to established baselines, and makes null false-positive control a first-class outcome.

This is a **draft**. The confirmatory analysis must not begin until all items marked “freeze before confirmatory runs” below are resolved and committed with a timestamped protocol version.

## 2. Research question (provisional)

For a fixed, fully specified dimuon bump-hunt pipeline, does a prespecified diagnostic identify loss of calibration under previously unseen smooth acceptance-like distortions, while preserving the nominal global false-positive rate on held-out background-only scenarios?

This is a candidate question, not a novelty claim. Existing literature on bump-hunt bias/variance, background sculpting, data-directed searches, and Bayesian background comparison overlaps substantially. The question proceeds only if a documented comparison establishes a precise unresolved gap.

## 3. Scope and non-claims

- Distortions are **synthetic stress tests**. They are not detector simulations, measured CMS trigger efficiencies, or evidence of a real trigger defect.
- The study does not claim a new particle, a new CMS result, or discovery significance.
- A branch name in a ROOT file is not proof that its semantics, prescale handling, certification, or efficiency denominator are appropriate.
- A successful software test or schema inventory is not physics validation.
- Run2012B and Run2012C must be treated as distinct data-taking periods until run-dependent selection and trigger behavior are justified.
- Any real-data spectrum is exploratory unless the selection, background model, fit window, and global test are specified independently of the inspected spectrum.

## 4. Target estimands

For each prespecified scenario family, estimate:

1. **Global type-I error:** proportion of independent background-only pseudoexperiments in which the complete mass scan rejects the null at nominal level alpha.
2. **Calibration-failure detection rate:** proportion of prespecified distorted-background pseudoexperiments in which the diagnostic flags the pipeline as unreliable, under a frozen threshold.
3. **False-alarm rate of the diagnostic:** proportion of nominal background-only pseudoexperiments flagged as unreliable.
4. **Signal-injection power (secondary):** detection probability at frozen signal strengths and mass points, reported alongside type-I error rather than in isolation.
5. **Numerical failure rate:** proportion of fits/scans that fail or return invalid estimates; failures must not be silently dropped.

Primary outputs should include binomial confidence intervals or Monte Carlo standard errors. A point estimate without simulation uncertainty is insufficient.

## 5. Design separation

### Development set

Use only for selecting/implementing the diagnostic, debugging code, and estimating nuisance ranges. Development results are not confirmatory evidence.

### Validation set

Use to check implementation and choose a single diagnostic threshold if the threshold is not determined analytically. After this stage, freeze the threshold and code hash.

### Confirmatory set

Use independently generated random seeds and distortion parameters from families not used in development. Do not tune the model, diagnostic, thresholds, binning, or mass range after inspecting confirmatory results. Publish all prespecified outcomes, including null or unfavorable ones.

The random seed list or deterministic seed-generation rule, scenario grid, code commit, software environment, and analysis configuration must be recorded before confirmatory runs.

## 6. Required scenario families

Exact distributions and parameter ranges remain **unfrozen** and must be justified before confirmatory runs.

- Nominal background-only nulls, including the baseline spectrum family.
- Smooth acceptance-like perturbations with shapes distinct from the development family.
- Alternative smooth background curvature families.
- Fit-window and mass-range boundary cases, if these are part of the intended use.
- Injected localized signals for secondary power assessment.
- Numerical/pathological cases that test failure handling, not scientific performance.

Synthetic transformations must preserve physically meaningful constraints (for example, non-negative expected rates). Their parameter ranges should be motivated, not selected to make the diagnostic win.

## 7. Required comparators

At minimum compare the proposed diagnostic against:

- no diagnostic / the base bump-hunt pipeline alone;
- a simple prespecified goodness-of-fit or residual-based diagnostic;
- a credible existing background-model uncertainty or bump-hunt method selected after the literature review.

The exact implementation and fair tuning budget for each comparator must be frozen. Do not compare a tuned proposed method against deliberately weak or untuned baselines.

## 8. Global significance and multiplicity

If the procedure scans across mass hypotheses, its primary type-I error is the **global** false-positive rate for the complete scan, not a local p-value at a selected mass. The null distribution must reproduce all selection, fitting, scanning, and diagnostic steps. Report local and global quantities separately where relevant; never label local significance as global discovery significance.

## 9. Monte Carlo precision and stopping rule

Choose the number of pseudoexperiments based on the precision required for the primary estimands, before confirmatory results are examined. Report Monte Carlo uncertainty for all key rates. A fixed sample size or a prespecified precision-based stopping rule is required; do not stop when a favorable result appears.

For example, around a true rate of 5%, 2,000 independent trials give a simple binomial standard error of roughly 0.49 percentage points. This is only an illustration; final counts should be selected for the desired interval width and computational budget.

## 10. Missingness, exclusions, and failures

- Predefine event/object selections and any missing-branch behavior.
- Record every attempted pseudoexperiment, including failed fits and invalid scans.
- Report both an intention-to-evaluate denominator (all attempted runs) and any conditional metric among successful fits, with explicit reasons for the distinction.
- Never silently discard outliers, failed fits, or unfavorable scenarios.
- Add unit tests for edge cases, branch mismatches, empty selections, non-finite values, and scan-boundary behavior.

## 11. Data and provenance gate

Before using real CMS data for any trigger-related inference, record:

- exact record ID, file name, file size, checksum, and data-taking period;
- tree path, branch names/types, and entries inspected;
- official semantics documentation for each selected branch;
- good-lumisection certification and run/lumisection selection;
- trigger paths, path availability by run, prescales, and a defensible efficiency denominator;
- muon quality/isolation requirements and any data-quality exclusions;
- the provenance of every plot/table and the exact command/configuration that produced it.

If a suitable efficiency denominator or prescale information is not available, remove the trigger-efficiency claim and keep the work as a synthetic robustness study or a clearly bounded spectrum-reproduction study.

## 12. Reporting and reproducibility

The eventual paper should include:

- a versioned protocol and deviations table;
- complete scenario definitions and configuration files;
- code, dependency versions, deterministic seeds, and execution instructions;
- tests and continuous-integration results;
- plots with uncertainty intervals and denominators;
- a results table for every prespecified primary endpoint;
- limitations, including the difference between synthetic stress tests and detector response.

Any post-freeze deviation must be dated, justified, and reported. Exploratory findings must be labeled exploratory.

## 13. Freeze-before-confirmation checklist

- [ ] Literature review expanded enough to establish the precise gap.
- [ ] Research-level ROOT schema and event semantics inspected.
- [ ] Intended real-data role decided (or explicitly excluded from primary inference).
- [ ] Base bump-hunt algorithm, mass range, binning/unbinned likelihood, fit family, and scan grid specified.
- [ ] Diagnostic formula and threshold specified.
- [ ] Scenario distributions and parameter ranges justified.
- [ ] Comparator implementations and tuning budgets specified.
- [ ] Primary estimands, alpha, confidence intervals, and Monte Carlo precision specified.
- [ ] Failure handling and exclusion rules tested.
- [ ] Independent development/validation/confirmatory seeds fixed.
- [ ] Code commit and environment recorded.
- [ ] Protocol version frozen before confirmatory results are generated.

## 14. Current decision

**Do not launch the confirmatory simulation campaign yet.** The research-level file inspection is pending, and the diagnostic, scenario grid, comparators, and target precision are not frozen. The next valid milestone is to verify the exact file/schema provenance, then revise this protocol based on what the data can actually support and the literature gap that survives review.
