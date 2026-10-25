# Research question and scope

**Status:** provisional research design; no analysis results claimed.  
**Last updated:** 2026-10-25

## Working title
**Calibrating Dimuon Resonance-Search Statistics under Prespecified Background and Selection Misspecification**

## Primary question
In a documented CMS Open Data dimuon-spectrum analysis, how does the empirical false-positive behaviour of a specified local resonance-search procedure change under prespecified, controlled departures from its background-shape and analysis-window assumptions, and how well can a diagnostic fixed before evaluation identify configurations in which nominal calibration fails?

This is a candidate question, not a verified research gap. The literature review must establish whether a materially equivalent experiment has already been reported.

## Scope guardrails
- The project audits statistical calibration; it does not claim to discover a particle.
- Real CMS collision data, model-generated background-only pseudoexperiments, and deliberately misspecified stress tests must be labelled separately.
- Any diagnostic is a research object to evaluate, not a guaranteed correction.
- Global significance will be included only if a defensible scan procedure and its null distribution can be implemented and validated. Otherwise, the first version will focus on a prespecified local test and explicitly defer global claims.
- No claim of a 3-sigma or 5-sigma false-positive rate will be made unless simulation volume and tail-estimation method support it. Small pilot experiments cannot empirically validate a 5-sigma tail.
- The first milestone is a reproducible reference analysis and a documented literature-based decision, not a large simulation campaign.

## Candidate hypotheses (to be prespecified only after baseline choices are justified)
1. Under correctly specified background-only generation and fitting, the test procedure's empirical type-I error is compatible with its nominal level within Monte Carlo uncertainty.
2. Certain prespecified background-shape or fit-window departures may produce measurable miscalibration, bias, or interval undercoverage.
3. A prespecified diagnostic may distinguish some, but not necessarily all, misspecified configurations from adequately calibrated ones.

These are hypotheses, not expected findings. Null or negative results are scientifically reportable.

## Primary estimand
For a prespecified nominal local test size alpha and a defined stress-test scenario, estimate the probability of rejecting the background-only hypothesis when data are generated under that scenario. Report the number of valid pseudoexperiments, the observed rejection fraction, and a binomial confidence interval. The selected alpha values must match feasible simulation counts and the intended claim.

## Secondary outcomes
- Signal-yield bias under injected-signal validation scenarios, if implemented.
- Coverage of intervals for the signal yield or another explicitly defined parameter.
- Fit failures and boundary/pathology rates.
- Diagnostic sensitivity, specificity, and uncertainty, using a predeclared scenario-level definition of miscalibration.
- Local/global significance comparisons only after a valid scan-calibration design is specified.

## What would count as useful
A transparent, reproducible map of how defined modelling departures affect a specific procedure, with uncertainty quantified and held-out stress scenarios, could be useful even if the proposed diagnostic performs poorly. A collection of background fits without a validated statistical question would not establish a contribution.

## Decision gate before implementation
Proceed beyond a small pilot only after:
1. the exact CMS dataset and trigger/event selection are identified;
2. relevant prior literature and existing code are reviewed;
3. a baseline likelihood and fitting window are justified;
4. the null-generating process and misspecification scenarios are specified independently of evaluation outcomes;
5. simulation counts are justified by target error rates and Monte Carlo precision.
