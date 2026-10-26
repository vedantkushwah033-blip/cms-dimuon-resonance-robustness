# Monte Carlo precision plan for the CMS dimuon robustness study

**Status:** planning aid only. No confirmatory results are reported here. This document does not freeze the protocol, choose a diagnostic, or establish novelty.

## Why replicate counts must be justified

For a scenario with independent pseudoexperiments and an estimated event rate \(\hat p=k/n\), the approximate Monte Carlo standard error is

\[
\operatorname{SE}(\hat p) \approx \sqrt{\hat p(1-\hat p)/n}.
\]

At a nominal global false-positive rate of 5%, the approximate 95% normal half-width is \(1.96\sqrt{0.05(0.95)/n}\). These values are planning approximations, not results; final reporting should use a suitable binomial interval (for example, Wilson or exact) and state the interval method.

| Independent pseudoexperiments per scenario | Approx. SE if rate is 5% | Approx. 95% half-width |
| ---: | ---: | ---: |
| 500 | 0.975 percentage points | 1.91 percentage points |
| 1,000 | 0.689 percentage points | 1.35 percentage points |
| 2,000 | 0.488 percentage points | 0.96 percentage points |
| 5,000 | 0.308 percentage points | 0.60 percentage points |
| 7,300 | 0.255 percentage points | 0.50 percentage points |
| 10,000 | 0.218 percentage points | 0.43 percentage points |
| 20,000 | 0.154 percentage points | 0.30 percentage points |

The table assumes independent Bernoulli outcomes and a true rate near 5%. For rates far from 5%, use the appropriate rate-specific calculation. For many scenario families, each family needs enough precision for its own claims; pooling across scenarios can hide a failure in one family.

## Planning rule

1. Define the primary estimands and the largest tolerable Monte Carlo uncertainty before looking at confirmatory results.
2. Calculate the required replicate count for each primary rate using a stated interval and precision target.
3. Budget separately for development, validation, and held-out confirmation. Development runs do not count as confirmatory evidence.
4. Estimate run time and numerical failure rates in a small pilot. Use pilot data for compute planning only, not to select favorable scientific outcomes.
5. Fix a deterministic seed-generation rule and a fixed replicate count (or a fully specified precision-based stopping rule) before confirmation.
6. Include every attempted replicate in the failure accounting. Report both the all-attempted denominator and any conditional-on-success rate.
7. For comparisons between methods on the same pseudoexperiments, plan uncertainty for the paired difference; do not treat paired outcomes as independent.

## Important interpretation cautions

- A 95% interval that contains 5% does not by itself establish calibration. The study needs a prespecified acceptance criterion and enough precision to evaluate it.
- Failure to reject a calibration discrepancy is not evidence of equivalence.
- A diagnostic's sensitivity is meaningful only alongside its false-alarm rate on nominal null scenarios.
- If the complete procedure scans many mass hypotheses, calibrate the global false-positive rate of that complete scan, not just a local per-mass statistic.
- Monte Carlo precision does not repair an invalid generator, unrealistic distortion family, unfair comparator, or data-provenance problem.

## Freeze-before-confirmation fields still required

- Primary rate(s) and tolerable interval width.
- Binomial interval method and any multiplicity handling.
- Scenario-specific replicate counts and deterministic seed rule.
- Paired-comparison estimand and uncertainty method.
- Runtime budget and numerical-failure policy.
- A documented rationale for the held-out scenario families.

Until these are resolved in the versioned protocol, the existing 500-replicate pilot row is a runtime/failure smoke test only, not confirmatory evidence.
