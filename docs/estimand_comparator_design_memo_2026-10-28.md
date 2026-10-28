# Estimand and comparator design memo — 2026-10-28

**Status:** design memo only. Not a frozen analysis protocol, not an execution authorization, and not a novelty claim.

## 1. Decision the study should answer

For a specified nominal type-I error level, does a fully specified adaptive dimuon bump-hunt procedure maintain its intended global false-positive probability under null-generating scenarios that are both represented by and deliberately outside its fitted background-model family?

This question is narrower than “which background fit is best?” and different from confidence-interval coverage, local p-value calibration, or signal-injection power. The estimand must be finalized after detailed review of the closest prior work.

## 2. Primary estimand

Let:
- (g) index a prespecified background-only generator scenario;
- (A) denote the complete frozen analysis algorithm, including all data-dependent fitting/model choice and the mass scan;
- (T_A(X)) be the algorithm's final global test statistic or global p-value for spectrum (X);
- (c_\alpha) be a rejection threshold fixed without using the evaluation replicates;
- (R=1\{T_A(X)\text{ rejects at level }\alpha\}\).

For each generator (g), the target is:

\[
p_g = \Pr_g(R=1),
\]

the global type-I error probability under that specific background-only generator. The estimated value from (N_g) independent evaluation pseudo-experiments is (\hat p_g = K_g/N_g), with (K_g=\sum R_i). Report a binomial interval (Wilson or exact), the numerator and denominator, and the fit-failure rate.

**Critical detail:** the global test statistic must account for the full search, not just a local excess at a chosen mass. If model family or hyperparameters are selected from the observed spectrum, the same selection operation must be repeated inside every pseudo-experiment. Otherwise the experiment does not evaluate the claimed adaptive procedure.

## 3. Separate three data roles

| Partition | Allowed use | Forbidden use |
|---|---|---|
| Development generators / replicates | Debug code, select candidate algorithms, establish numerical stability, estimate runtime | Final performance claims presented as held-out evidence |
| Calibration generators / replicates | Set a prespecified global threshold or calibrate the procedure according to a frozen rule | Repeated tuning after inspecting final held-out outcomes |
| Held-out evaluation generators / replicates | Estimate (p_g), uncertainty, and failure rate for each frozen scenario | Choosing the threshold, changing the algorithm, or silently dropping difficult scenarios |

Use separate random streams and record seeds, generator definitions, software versions, and code commit. If held-out outcomes cause a method change, label the changed study exploratory and create a new untouched evaluation partition before confirmatory claims.

## 4. Comparator table

| Comparator | Question it answers | Required fairness condition |
|---|---|---|
| Frozen single-background-family fit + full mass scan | Does the adaptive model-selection layer change global error relative to a simpler fit? | Same bins, mass range, signal hypotheses, fitting conventions, and calibration/evaluation generators |
| Established scan-level bump-hunt baseline (e.g., BumpHunter-style maximum statistic) | Does the proposed pipeline behave differently from an existing global-search approach? | Compare the same global estimand and account for each method's own prescribed calibration |
| Same adaptive algorithm under in-family null generators | Is the algorithm calibrated when its fitted family contains the generator? | Generators and parameter values must be specified before evaluation |
| Same adaptive algorithm under out-of-family null generators | How sensitive is calibration to declared background misspecification? | Define misspecification mechanisms and severity before evaluation; do not tune them to produce a preferred outcome |
| Signal-injection study (secondary, separate) | What is the probability of detecting a specified signal at each mass/yield? | Keep signal injection separate from background-only type-I-error estimation; define success criterion in advance |

This table does not select the final method or imply that the proposed comparison is novel. The prior-work review may require changing the question or treating the work as a replication/benchmark.

## 5. Monte Carlo precision planning (illustrative, not a run authorization)

For a binomial estimate near a target rate (p), the approximate standard error is (\sqrt{p(1-p)/N}). The table gives rough replicate counts for a normal-approximation 95% interval half-width (h); final reporting should use Wilson or exact binomial intervals, particularly when counts are small.

| Rate near which precision is planned | Approx. 95% half-width | Approx. independent evaluation replicates |
|---:|---:|---:|
| 0.05 | 0.010 | 1,825 |
| 0.05 | 0.005 | 7,300 |
| 0.01 | 0.005 | 1,522 |
| 0.01 | 0.002 | 9,508 |

These values are planning approximations, not guarantees. If the number of failed fits is non-negligible, report it separately and predefine whether the analysis failure counts as rejection, non-rejection, or an explicit indeterminate outcome. Never silently exclude failed fits and report the remaining fraction as if it represented all replicates.

A single 10,000-replicate cell near (p=0.05) has an approximate 95% half-width of 0.0043 before accounting for any additional uncertainty from fitting, generator estimation, or threshold selection. A large replicate count cannot compensate for an invalid null generator or a flawed analysis definition.

## 6. Mandatory algorithm freeze fields

Before confirmatory execution, the protocol must identify:
- event/data provenance and the exact real-data baseline target, if any;
- observable, mass range, bin edges, and event/object selection;
- candidate signal shapes/widths and the exact scanned hypotheses;
- all background families, parameter constraints, fit ranges, optimization and model-selection rule;
- the test statistic, global calibration method, threshold rule, and nuisance-parameter treatment;
- generator families, parameter values, and explicit in-family/out-of-family labels;
- independent development/calibration/evaluation partition definitions and random-stream strategy;
- treatment of non-convergence, boundary fits, invalid spectra, and incomplete outputs;
- primary estimand, secondary estimands, planned contrasts, and multiplicity policy;
- Monte Carlo interval method and precision target;
- signal-injection scenarios and power definition, if included;
- reproducibility manifest, environment, artifacts, and independent review sign-off.

## 7. Go/no-go rules

**GO for exploratory implementation tests** only when they are clearly labelled as development and cannot be mistaken for confirmatory results.

**NO-GO for confirmatory simulation** until the protocol validator passes with all evidence gates satisfied, the closest literature has been reviewed beyond abstracts, the baseline parity question is resolved or explicitly excluded from the scientific estimand, and an independent reviewer has checked the statistical design.

**NO-GO for novelty or physics claims** based on passing software tests, synthetic spectra alone, a reproduced educational histogram, or a large number of pseudo-experiments.

## 8. Reviewer questions to resolve before freeze

1. Is the primary method really an adaptive model-selection procedure, or does the implementation currently only fit one specified model? The estimand must match the implemented algorithm.
2. What is the primary global test statistic, and what published method is the fairest comparator?
3. Are null generator parameters treated as known, estimated from real data, or varied over a nuisance grid? These choices change the interpretation of the calibration result.
4. Does the calibration procedure use a threshold fixed from an independent calibration set, or does it use a standard global-p-value algorithm? These should not be conflated.
5. What specific out-of-family generator is scientifically defensible, and what range of misspecification is meaningful rather than adversarial?
6. What will count as evidence of practical miscalibration, including uncertainty and multiple scenarios, rather than a noisy difference in point estimates?

Until these are answered, retain the project status as a reproducible research-design scaffold rather than a validated statistical result.
