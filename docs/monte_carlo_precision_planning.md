# Monte Carlo Precision Planning

**Status:** planning note; no pseudoexperiments have been run for these calculations.

## Why the replicate count must be justified

For N independent Bernoulli outcomes and a true rejection probability p, the Monte Carlo standard error of the observed rejection fraction is approximately

\[
\operatorname{SE}(\hat p)=\sqrt{p(1-p)/N}.
\]

A normal-approximation 95% half-width is approximately 1.96 times this standard error. This is a planning approximation: the final analysis should use a prespecified binomial confidence interval and should account for any dependence, weighting, exclusions, or fit-failure policy.

## Illustrative planning values at nominal alpha = 0.05

Assuming the true rejection probability is 0.05, the following values are approximate:

| Independent pseudoexperiments N | Expected rejections | Monte Carlo SE | Approximate 95% half-width |
|---:|---:|---:|---:|
| 500 | 25 | 0.00975 | 0.0191 |
| 1,000 | 50 | 0.00689 | 0.0135 |
| 5,000 | 250 | 0.00308 | 0.00604 |
| 10,000 | 500 | 0.00218 | 0.00427 |
| 30,000 | 1,500 | 0.00126 | 0.00247 |
| 100,000 | 5,000 | 0.000689 | 0.00135 |

These are not results from the CMS dataset. They are binomial precision calculations under the stated illustrative value p = 0.05.

## Approximate N for absolute half-width targets

Using the normal approximation

\[
N \approx p(1-p)\left(\frac{1.96}{h}\right)^2,
\]

where h is the target absolute half-width:

| Assumed p | Target half-width h | Approximate N |
|---:|---:|---:|
| 0.05 | 0.0100 | 1,825 |
| 0.05 | 0.0050 | 7,300 |
| 0.05 | 0.0025 | 29,200 |
| 0.05 | 0.0010 | 182,500 |
| 0.01 | 0.0020 | 9,600 |

Rounded values are intentionally approximate. Exact intervals and pilot observations should inform the final budget.

## Rare-event limitation

If zero rejections occur in N independent trials, the estimated rate is zero, but the underlying rate is not thereby proven to be zero. A useful approximate 95% upper bound is about 3/N; use the exact binomial interval for reporting. For example, zero rejections in 10,000 trials is compatible with a rate on the order of 3e-4. This is nowhere near sufficient to validate a five-sigma tail probability.

## Recommended budget decision

1. Run deterministic unit tests and tiny smoke tests first.
2. Use a pilot to measure runtime and fit-failure rates, not to claim calibration.
3. Choose the main N from a written precision target, plausible rejection rates, scenario count, compute budget, and the required treatment of failed fits.
4. Report attempted and valid trial counts, failures, rejections, exact confidence intervals, and Monte Carlo standard errors for every scenario.
5. Do not silently drop failed fits or treat a failed fit as a non-rejection unless that rule was prespecified and justified.
6. Keep null-calibration and signal-power studies separate.

**Decision remains open:** no confirmatory N is frozen until the statistical procedure, scenarios, and failure policy are fully specified.
