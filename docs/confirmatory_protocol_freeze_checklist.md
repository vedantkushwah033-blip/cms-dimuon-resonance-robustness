# Confirmatory protocol freeze checklist

**Status:** planning template; intentionally not frozen.  
**Date:** 2026-10-27  
**Rule:** do not run or interpret a confirmatory simulation campaign until every required item below has a recorded decision, a rationale, and a versioned implementation. Completing this checklist does not establish novelty.

## 1. Decision the study is intended to support

Write one sentence describing the scientific or methodological decision that would change because of the result.

- **Decision statement:** [UNRESOLVED]
- **Target user:** [UNRESOLVED]
- **Why existing procedures do not already answer it:** [UNRESOLVED; cite methods-level evidence]
- **Fallback if no distinct gap survives review:** reproducibility/benchmark study with no new-method claim.

A project about “background mismatch is dangerous” is not sufficiently specific: this is established prior work. A new diagnostic is not justified merely by a new name or implementation.

## 2. Define the estimand before selecting scenarios

Choose one primary estimand and distinguish it from secondary diagnostics.

Candidate estimands requiring justification:
- Global type-I error: probability the *entire frozen search procedure* rejects at least once under a specified null-generating scenario.
- Diagnostic false-alarm rate: probability a frozen diagnostic flags a scenario/event under a precisely defined null condition.
- Difference in global type-I error between two procedures, paired on the same generated datasets.
- Power at prespecified signal strengths, reported only alongside null calibration and the signal-generation assumptions.

**Primary estimand:** [UNRESOLVED]  
**Population of scenarios to which it applies:** [UNRESOLVED]  
**Unit of analysis / independent replicate:** [UNRESOLVED]  
**Target uncertainty interval:** [UNRESOLVED]  
**Multiplicity family:** [UNRESOLVED]

Do not call a per-mass local p-value “global significance.” If the analysis scans masses, tries multiple fit windows, selects background models, or tunes a diagnostic, the calibration must reproduce the complete selection-and-scan procedure.

## 3. Separate development from held-out evaluation

Create and version an explicit scenario manifest before confirmatory runs.

| Partition | Permitted use | Required rule |
|---|---|---|
| Development | Debugging, exploring algorithms and plotting | May be repeatedly inspected; never used as final evidence |
| Calibration/tuning | Choosing thresholds or tuning comparator settings | Must be kept separate from final evaluation |
| Held-out null evaluation | Estimating the primary null operating characteristic | Generator families and seeds/manifest fixed before opening results; no tuning on outcomes |
| Signal-injection evaluation | Secondary power/robustness study | Signal models, strengths, mass points and acceptance assumptions prespecified |
| Failure/edge cases | Stressing numerical and fit failure handling | Include in a transparent failure table; do not silently discard failures |

**Held-out scenario family definitions:** [UNRESOLVED]  
**What makes each family scientifically relevant:** [UNRESOLVED]  
**How each family differs from development/calibration:** [UNRESOLVED]  
**Who controls or reviews the sealed manifest:** [UNRESOLVED]

“Held out” must mean more than new random seeds from the same generator if the claim concerns robustness to new kinds of misspecification. If only seeds are held out, describe the evaluation as within-generator validation.

## 4. Freeze the complete search pipeline

Before confirmatory simulation, specify:

- Observable and units; input selection and exclusions.
- Fit range and any blinded/excluded regions.
- Candidate background families and their parameter constraints.
- Signal template, width/resolution assumptions, and allowed mass range.
- Fit objective, optimizer, starting values, convergence criteria, and retry policy.
- Rule for selecting the background model; all selection steps included in null calibration.
- Test statistic at each mass and how it is combined across the mass scan.
- Treatment of fit-window or hyperparameter scans, if any.
- Global calibration method and finite-Monte-Carlo correction.
- Diagnostic definition, threshold selection, and whether it changes the primary test.
- Handling of boundaries, singular fits, non-convergence, empty bins, and invalid pseudoexperiments.

**Frozen implementation commit/hash:** [UNRESOLVED]  
**Independent reference implementation:** [UNRESOLVED]  
**Determinism/reproducibility test:** [UNRESOLVED]

## 5. Comparators and fairness

A claimed improvement requires at least one relevant existing comparator. The baseline must be implemented and validated, not described only in prose.

Candidate comparison targets to investigate—not an approved final list:
- A prespecified fixed background family with a standard likelihood-ratio/profile-likelihood scan and global calibration.
- A data-driven background-selection approach relevant to Williams (2017).
- A background-mismodeling-aware procedure relevant to Algeri (2020), if its assumptions and output match the estimand.
- Any method in the closest literature that directly addresses the same estimand.

For every comparator, record: source and version, assumptions, inputs, tuning budget, calibration procedure, convergence/failure rules, and known limitations. Do not compare a tuned new method against an untuned baseline.

**Primary comparator:** [UNRESOLVED]  
**Secondary comparator(s):** [UNRESOLVED]  
**Fairness/tuning budget:** [UNRESOLVED]  
**Method-specific assumptions and implementation validation:** [UNRESOLVED]

## 6. Monte Carlo precision and analysis plan

Choose the number of independent pseudoexperiments from the target precision and estimand, not from a desire for a large headline number.

- Primary rate/difference and target confidence-interval half-width: [UNRESOLVED]
- Replicates per held-out scenario: [UNRESOLVED]
- Paired design and pairing unit: [UNRESOLVED]
- Interval method: [UNRESOLVED]
- Seed-generation and storage policy: [UNRESOLVED]
- Interim looks / stopping rule: [UNRESOLVED; default is no outcome-driven stopping]
- Treatment of failed fits and missing outputs: [UNRESOLVED]
- Planned tables/figures and exact summary statistics: [UNRESOLVED]

For a binomial rate near 5%, 10,000 independent trials give a rough normal-approximation 95% margin of about 0.43 percentage points. This is a planning approximation only; use an appropriate interval and account for multiple scenarios, paired comparisons, clustering/dependence, and failed trials. More trials do not fix a misspecified generator or an unfair comparator.

## 7. CMS data feasibility gate

The schema audit confirms branch presence in one sampled Run2012B DoubleMuParked file and one sampled Run2012C file; it does not validate trigger semantics or a physics analysis.

Before making a trigger-aware or real-data claim, obtain and review:
- Exact official input records, URLs, checksums, file sizes, tree entry counts, and branch types.
- A reproducible run/lumisection certification procedure and the correct official JSON where applicable.
- Event-level trigger-bit counts by run range, with path versions and logical OR semantics documented.
- Prescale treatment and a defensible denominator for any efficiency estimate.
- Candidate/reference cut-flow and per-bin histogram comparisons on the same input, including edge conventions.
- Discrepancy investigation and signed-off acceptance criteria.

**Baseline run/artifact:** [NOT AVAILABLE IN CURRENT STATUS]  
**Reference parity:** [NOT ESTABLISHED]  
**Trigger semantics / prescales / denominator:** [NOT ESTABLISHED]  
**Decision if trigger information is insufficient:** narrow the real-data claim to a validated spectrum reconstruction and keep synthetic trigger/acceptance distortions explicitly synthetic.

A 100,000-entry prefix is a software smoke test, not full-data reproduction. The 2012 outreach spectrum's known feature near 30 GeV is a data-taking/trigger effect, not evidence of a new resonance.

## 8. Go/no-go criteria

### GO only when all are true
1. Methods-level literature table compares the closest methods on estimand, generators, model-selection steps, calibration, and assumptions.
2. A distinct question survives that comparison—or the project is explicitly reframed as a benchmark/reproduction.
3. The baseline pipeline and independent implementation pass documented validation.
4. The primary estimand, comparator, scenario manifest, complete search pipeline, Monte Carlo precision, and failure rules are frozen and versioned.
5. Development and held-out results are technically separated.
6. An independent reviewer can reproduce the analysis from the manifest and repository instructions.

### NO-GO / narrow the claim if any are true
- Novelty depends only on generic misspecification, more pseudoexperiments, a new label, or a new implementation.
- The global scan or model-selection process is omitted from calibration.
- The comparator is not validated or is given a weaker tuning budget.
- Held-out scenarios are repeatedly inspected and then used to tune the method.
- Real-data provenance, selection, trigger semantics, or reference agreement cannot be established.
- Failures are dropped without accounting or the result changes materially under reasonable prespecified alternatives.

## 9. Reporting and claim boundaries

Report null calibration before signal-injection power. Include all scenario-level results, uncertainty intervals, failed-fit counts, and deviations from the frozen protocol. Show negative or inconclusive findings. Distinguish software tests, data reproduction, statistical validity, novelty, and independent review.

Never claim a new resonance from this project unless an appropriately validated analysis supports that conclusion; the present project plan and schema checks do not.

## 10. Sign-off log

| Gate | Evidence/link | Reviewer/date | Decision |
|---|---|---|---|
| Methods-level literature comparison | [PENDING] | [PENDING] | OPEN |
| Baseline data provenance and parity | [PENDING] | [PENDING] | OPEN |
| Trigger/selection feasibility | [PENDING] | [PENDING] | OPEN |
| Estimand and comparator frozen | [PENDING] | [PENDING] | OPEN |
| Held-out scenario manifest frozen | [PENDING] | [PENDING] | OPEN |
| MC precision and failure rules frozen | [PENDING] | [PENDING] | OPEN |
| Independent reproduction/review | [PENDING] | [PENDING] | OPEN |
