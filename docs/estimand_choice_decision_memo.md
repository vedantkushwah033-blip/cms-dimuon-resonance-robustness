# Choosing the primary estimand: decision memo

**Date:** 2026-10-27  
**Status:** provisional recommendation for discussion; not a frozen preregistration.  
**Current gate:** baseline validation and methods-level comparator selection remain open.

## Executive recommendation

If the project remains about the calibration of a complete dimuon bump-hunt procedure, use **global type-I error under a specified null-generating scenario** as the leading candidate primary estimand. Treat diagnostic false-alarm rate as a separate secondary estimand only if a diagnostic is explicitly defined and thresholded. Do not use interval coverage as a substitute for discovery calibration; coverage is a different inferential property.

This is a recommendation about coherence between the research question and the metric—not a claim that this estimand is novel or that a suitable new method exists.

## Why the estimands must not be conflated

### A. Global type-I error
**Operational meaning:** Under a specified null-generating scenario, the probability that the complete frozen search pipeline produces at least one discovery-level rejection anywhere in the prespecified scan.

**Why it fits:** The project's motivating concern is false-positive calibration after the full procedure, potentially including model selection and a diagnostic. It directly measures the final decision's false-alarm behavior.

**What it requires:**
- Define the null scenario family and the discovery threshold.
- Run every selection, fit, model-choice, diagnostic, retry, and mass-scan step in each pseudoexperiment.
- Recompute the global statistic and apply the same decision rule in every replicate.
- Report scenario-specific rates and uncertainty intervals; do not average away a failing scenario without a prespecified target-population rationale.
- Clearly distinguish empirical global type-I error from a local per-mass p-value.

**Limitation:** A calibrated global rate under a finite set of synthetic scenarios does not establish calibration for real CMS data or every possible background.

### B. Diagnostic false-alarm rate
**Operational meaning:** Under a specified null condition, the probability that a frozen diagnostic triggers an alert.

**Why it is secondary:** It is useful only if the diagnostic has a clear operational role. A diagnostic can flag harmless deviations, miss important deviations, or flag a condition that does not change the final search decision. Its rate alone cannot tell whether the complete bump hunt is calibrated.

**Required companion measures:** sensitivity to prespecified mismatch classes, rate of missed warnings, and the relationship between diagnostic outcomes and the primary global decision. Thresholds must be selected using development/calibration data, not held-out outcomes.

### C. Confidence-interval coverage
**Operational meaning:** Across repeated datasets generated at a specified parameter value, the fraction of intervals that contain that value.

**Why it is distinct:** Coverage evaluates uncertainty intervals for a parameter such as signal strength. It does not by itself measure the false-positive rate of a maximum-over-mass discovery scan. The literature, including Williams (2017), already treats bias, uncertainty and coverage under model selection, so this metric alone is especially weak as a novelty claim.

**When to use it:** If the project explicitly targets signal-strength inference and interval validity, define a separate study with its own estimand and calibration. Do not add coverage as another headline result without a coherent inferential target.

### D. Power under signal injection
**Operational meaning:** Probability the complete procedure rejects under a prespecified signal-plus-background generator.

**Why it is secondary:** Power is only interpretable alongside null calibration. A method that rejects often under both null and signal can look powerful while being poorly calibrated. Signal-injection results should follow, not replace, null evaluation.

## Candidate analysis hierarchy

| Role | Candidate metric | Decision status |
|---|---|---|
| Primary | Scenario-specific global type-I error of the complete frozen pipeline | Recommended for consideration; not frozen |
| Secondary | Difference in global type-I error versus one fair, validated comparator, using paired generated datasets where appropriate | Depends on comparator and pairing design |
| Secondary diagnostic metric | Diagnostic false-alarm rate and missed-warning rate at a threshold fixed without held-out outcomes | Only if diagnostic is retained |
| Secondary | Power at prespecified signal strengths and mass points, after null calibration | Deferred |
| Separate possible project | Signal-strength interval coverage/bias | Do not mix into primary estimand without a separate protocol |

## Unit, scenarios and uncertainty

The natural independent unit for a Monte Carlo estimate is one independently generated pseudoexperiment, not one mass bin. Mass bins and scan points within one pseudoexperiment are dependent and must not be counted as independent trials for the global false-alarm rate.

The target population of null scenarios is a scientific design choice. At minimum, separate:
1. Correctly specified baseline nulls (software/calibration sanity check).
2. Misspecification families used for development and threshold tuning.
3. Independently held-out families chosen before final evaluation.
4. Numerical/fit failure cases, which must be counted and reported rather than silently discarded.

New random seeds from the same generator test repeatability under that generator; they do not alone test generalization to new forms of mismatch.

For every scenario, report the estimate and a prespecified interval. If comparing two methods on the same generated pseudoexperiments, define the paired outcome and uncertainty method before observing results. Choose replicate counts from the desired precision, and account for failures, dependence, and any sequential looks.

## Comparator implications

A comparator should be selected only after its output and assumptions are shown to align with the primary estimand. Williams-style model-selection-aware local inference and Algeri's comparison-density/deviance approach are not interchangeable by name. Either may require adaptation, and an adaptation must be labeled as such and validated. The CMS physics search of Cesarotti et al. is an analysis precedent, not automatically a statistical-method comparator for a synthetic global-calibration experiment.

Do not compare against a deliberately weak baseline. Document each comparator's source/version, inputs, tuning budget, calibration, convergence/failure policy, and any assumptions unavailable to the candidate.

## Stop/go implications

**Proceed toward protocol freeze only if:**
- The project can define a complete global decision rule.
- A relevant comparator can be implemented fairly.
- The null scenario population is defensible and separated into development/calibration/held-out partitions.
- The CMS baseline-validation limitations are handled by narrowing the claim or completing the required evidence.

**Reframe as a benchmark/reproduction if:**
- No decision-relevant gap survives the methods review.
- A published method cannot be implemented faithfully enough for a fair comparison.
- The result can only support claims about a finite synthetic benchmark.

**Do not claim:** a new resonance, validated CMS trigger efficiency, universal robustness, or a novel method from the estimand choice alone.

## Sign-off
- Primary estimand approved: **OPEN**
- Comparator approved: **OPEN**
- Scenario manifest frozen: **OPEN**
- Baseline validation complete: **OPEN**
- Independent review: **OPEN**
