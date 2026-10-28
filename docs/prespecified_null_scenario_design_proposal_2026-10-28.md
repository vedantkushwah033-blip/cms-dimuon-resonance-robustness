# Prespecified null-scenario design for the refitted-background prototype

**Status:** design proposal; not preregistered; not run; not CMS-validated. This document defines a candidate stress-test grid, not results. An independent reviewer should approve the scientific rationale and freeze the grid before any confirmatory simulation.

## Aim and estimand

Estimate the held-out rejection fraction of the *implemented* empirical upper-tail rank procedure at nominal level 0.05 for each explicitly defined toy-generating spectrum. The fit family and scan procedure are fixed within a scenario. Results describe these toy distributions only; they do not establish uniform type-I error control for CMS data or all possible backgrounds.

## Shared conventions to freeze

- Use a fixed number of bins and a declared half-open mass range; publish every bin edge.
- Map bin centers linearly to (x\in[-1,1]).
- Define the mean vector before simulation, with all means strictly positive.
- Generate independent Poisson counts per bin unless a separate non-Poisson experiment is explicitly specified.
- Fit the same fixed-order log-polynomial model in every pseudoexperiment; use the same declared scan-window widths.
- Compute the observed-data statistic (if later used) with the identical binning, fit, scan and failure policy. Do not tune the scan after viewing an observed excess.
- Use distinct, recorded random seeds for development, pilot, calibration and evaluation. Record software versions and commit SHA.
- Treat any fit failure as a recorded procedure outcome. Never silently discard failures or change the rule after seeing the results.
- Report calibration/evaluation sizes, rejection count, rejection fraction, Wilson interval, empirical p-value resolution, fit failures and the complete scenario definition.

The precise bin count, mass range, scan widths, background order and simulation sizes must be chosen and justified before a confirmatory run. Do not infer them from a visually interesting feature.

## Candidate scenario grid

Let (x_i\) be the normalized bin center and let (\mu_i\) be the Poisson mean. The following are *candidate mathematical stress tests*, not assertions about the physical shape of CMS data. Choose numerical parameters and ranges in a pilot, then freeze them before evaluating held-out scenarios.

| ID | Generator mean | Fitted family | What it probes | Status |
|---|---|---|---|---|
| S0: matched log-linear | (\mu_i=\exp(a+b x_i)\) | log-linear | Baseline implementation check when the model family is correctly specified | Required baseline |
| S1: smooth curvature | (\mu_i=\exp(a+b x_i+c x_i^2)\), with nonzero (c\) | log-linear | Smooth shape misspecification | Candidate held-out |
| S2: higher-order smooth shape | (\mu_i=\exp(a+b x_i+c x_i^2+d x_i^3)\) | log-linear | More flexible smooth misspecification | Candidate held-out |
| S3: broad localized shoulder | (\mu_i=\exp(a+b x_i)+A\exp[-(x_i-m)^2/(2s^2)]\), constrained to positive means | log-linear | A broad local deviation that may be absorbed imperfectly by the fit | Candidate held-out |
| S4: fit-order sensitivity | Use the same generator as S2 | Compare predeclared log-linear and log-quadratic fits as separate procedures | Whether the conclusion depends on a fixed model order | Secondary, separate procedure |
| S5: count-model stress test | A separately specified overdispersed generator, if implemented and independently checked | Declared Poisson fit | Sensitivity to violation of the independent-Poisson assumption | **Not supported by current generator; do not run yet** |

For S1–S3, parameter values and ranges are deliberately not filled in here: they require a reasoned choice of binning, expected event scale and physically/statistically defensible shape perturbations. Do not choose them by searching for scenarios that produce the most dramatic false-positive rate. If no defensible rationale is available, report a generic mathematical stress test rather than a CMS-motivated model.

## Separation of samples and roles

1. **Development:** tiny deterministic fixtures to test the code path and edge cases. Never report these as calibration evidence.
2. **Pilot:** estimate runtime, numerical stability and fit-failure rates only. Pilot outcomes may guide a written design revision, but the final scenario grid must be frozen afterward.
3. **Calibration:** generate a fixed independent sample of scan maxima for each frozen scenario/procedure.
4. **Held-out evaluation:** use a separate seed/sample. For each evaluation statistic (T), calculate (p=(1+\#\{T_{cal}\ge T\})/(M+1)); ties count in the upper tail. Reject if (p\le\alpha).
5. **Reporting:** publish all prespecified scenarios, including failures and unfavorable results. Do not select a subset based on whether the observed rejection fraction is close to 0.05.

A shared calibration sample means the evaluation p-values are not mutually independent conditional on that calibration sample. Report the per-scenario rejection fraction and its Wilson interval as a Monte Carlo summary; do not treat these summaries as proof of simultaneous or uniform calibration across scenarios.

## Interpretation rules

- A rejection fraction near 0.05 in S0 only supports behavior under that matched toy design, within Monte Carlo uncertainty.
- A deviation in S1–S3 is evidence of sensitivity for that specific misspecification, not a universal failure rate for CMS.
- A Wilson interval quantifies binomial Monte Carlo uncertainty in the held-out rejection fraction; it does not cover uncertainty about whether the scenario is scientifically realistic.
- A non-rejection is not proof that the background model is adequate.
- This procedure does not include detector/trigger response, event-selection uncertainty, event-level dependence, official CMS background-model selection, or independent data/reference parity.
- Do not quote a discovery p-value or physics claim from this scenario grid.

## Go/no-go gates before confirmatory runs

- [ ] Independent review approves the estimand, binning, scan windows and fit-failure policy.
- [ ] Each generator is fully specified with frozen numerical parameters and a documented rationale.
- [ ] The calibration sample is large enough that (1/(M+1)\le\alpha\); choose a stricter precision target if needed.
- [ ] Pilot failure rates and convergence behavior are documented before freezing the design.
- [ ] Tests and lint pass on supported Python versions for the exact commit to be evaluated.
- [ ] The full prespecified scenario list and reporting table are frozen in version control.
- [ ] If any CMS-data claim is contemplated, separate provenance, selection, reference-spectrum parity and trigger/luminosity checks are completed first.

**Current decision: NO-GO for confirmatory simulation.** This proposal still has unfilled numerical design choices and no independent review. It is safe to continue software validation and protocol review; do not label the study preregistered or CMS-validated.
