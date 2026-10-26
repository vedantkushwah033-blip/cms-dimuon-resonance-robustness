# Interpreting Monte Carlo calibration uncertainty

**Status:** methodological guidance; not a report of completed simulation results.

## What the interval estimates

For a prespecified scenario, let each valid pseudoexperiment produce a binary outcome indicating whether the complete analysis rejects the null hypothesis at the chosen threshold. If these outcomes are independent and identically distributed Bernoulli trials under the scenario, the rejection count can be summarized with a binomial proportion and an exact two-sided Clopper–Pearson confidence interval.

The interval quantifies finite-Monte-Carlo uncertainty in the estimated rejection probability. It does not establish that the generating model is scientifically realistic, that the fitted model is correct, or that the analysis code is free of defects. Those require separate validation.

## Zero observed rejections is not zero false-positive probability

With zero rejections in 1,000 independent trials, the estimate is 0/1,000 = 0, but the 95% two-sided Clopper–Pearson interval has an upper endpoint of approximately 0.00368 (0.368%). Therefore, this result would not demonstrate a zero false-positive rate, nor would it by itself demonstrate calibration at a nominal 0.1% or 0.01% level.

For zero successes in n trials, the exact two-sided upper endpoint at confidence level 1 - alpha is:

`1 - (alpha / 2) ** (1 / n)`

This is a useful sanity check for both implementation and interpretation. A one-sided upper confidence bound uses a different tail probability and must be labelled as one-sided; do not interchange the two.

## Trial design matters

Before running the main simulation, document:

- The scenario and data-generating parameter values.
- The complete rejection procedure, including any scan, fitting, refitting, selection, and multiplicity correction.
- The definition of a trial and the treatment of fit failures, invalid outputs, and boundary solutions.
- The nominal rejection threshold and whether the reported metric is local or global.
- The number of trials, random seed/stream policy, and stopping rule.
- The confidence-interval method and confidence level.

The binomial interval assumes the counted outcomes correspond to independent trials with a common rejection probability for the stated scenario. Reusing correlated pseudoexperiments, selectively dropping failed trials, changing the procedure mid-run, or stopping based on interim results can invalidate the naive interpretation. Fit failures should be accounted for under a prespecified rule and reported separately; they should not silently disappear from the denominator.

## Planning precision is not achieved precision

The helper `approximate_trials_for_absolute_precision` uses a normal-approximation formula to plan an approximate trial count. It is not a guarantee that the final exact interval will have the requested half-width, especially for rare rejection probabilities or estimates near zero or one. Report the observed exact interval from the completed run and justify whether it is sufficiently informative for the scientific decision.

## Required reporting

For every prespecified scenario, report at least:

| Quantity | Why it matters |
| --- | --- |
| Rejections / eligible trials | Makes the empirical numerator and denominator auditable |
| Estimated rejection probability | Point estimate, not a certainty |
| Exact interval and confidence level | Communicates Monte Carlo uncertainty |
| Fit failures and boundary hits | Reveals numerical or model-fitting fragility |
| Nominal threshold and test scope | Distinguishes local from global calibration |
| Generator and fitted-model definitions | Makes the calibration claim interpretable |
| Code revision, configuration, seed policy | Supports reproducibility |

Include all prespecified scenarios, including failures and negative or inconclusive outcomes. Never interpret successful calibration under one toy generator as proof of robustness to arbitrary backgrounds or detector effects.
