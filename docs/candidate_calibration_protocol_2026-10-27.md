# Candidate calibration protocol and decision gates

**Date:** 2026-10-27  
**Status:** design proposal only — not preregistered, not a validated analysis, and not evidence of novelty.

## Purpose

This document turns the literature-gap checkpoint into an auditable set of decisions. It is intended to prevent a large pseudoexperiment campaign from producing attractive but scientifically ambiguous plots. It does not authorize confirmatory simulation or establish that the proposed question is novel.

## Candidate scientific question

For a fully specified local dimuon bump-hunt procedure, how does the empirical null rejection probability change when the background-generating process differs from the model family used for fitting, after accounting for every prespecified model-selection and fit-failure decision?

This is a candidate estimand, not yet a novelty claim. Williams (2017) already studies model choice, bias/variance, and uncertainty in bump hunting. Before this question is frozen, the literature review must establish exactly what is and is not covered by prior procedures.

## Primary estimand (candidate)

For each prespecified null-generating mechanism g, estimate

    alpha_hat_g = (1/N) sum_i I(pipeline rejects the null on toy i).

The primary calibration error is the signed difference alpha_hat_g - alpha_0, where alpha_0 is the declared nominal local test size. A nominal 5% size is a candidate convention only; it must be aligned with the reproduced baseline and the final research question before simulation.

Report the binomial Monte Carlo standard error and a confidence interval for every estimate. Do not report a rejection fraction without its denominator, uncertainty, generator, and failure accounting.

### Local versus global claims

- A local-window rejection probability is not a global look-elsewhere-corrected discovery probability.
- If the procedure scans multiple windows or masses, either calibrate the maximum scan statistic under the null and report global error separately, or explicitly restrict claims to a single predeclared local window.
- Do not use “discovery significance” as a synonym for an uncalibrated local p-value.

## Candidate comparator arms

The final comparator set must be justified from the papers and the reproduced CMS baseline, not selected after viewing favorable results.

1. **Fixed-family reference:** one background family and fit/selection rule fixed before generating toys.
2. **Selection-enabled pipeline:** the same underlying analysis except for the prespecified model-selection step.
3. **Failure-accounting audit:** diagnostic reporting that separates numerical-fit failures, selection failures, invalid test-statistic outcomes, and valid non-rejections. It must not silently discard failed toys.
4. **Held-out misspecification checks:** generators not used to tune the fitting procedure, including only physically/statistically defensible smooth alternatives agreed before the confirmatory run.

A comparator is not automatically a meaningful scientific baseline just because it is easy to implement. Each arm must answer a stated decision question and be linked to an existing method or documented baseline.

## Generator design and leakage prevention

Before confirmatory simulation, write down for every generator:

- its mathematical definition and parameter range;
- why it represents a defensible null background scenario;
- which choices were used for development and which are held out;
- event-count / exposure model and whether finite-sample fluctuations are Poisson or conditional;
- fit range, bin edges, and any excluded regions;
- random-number generator and reproducible seed derivation;
- which quantities are estimated from the toy and which are fixed externally.

Do not tune the method against a generator and then call performance on that same generator an independent validation. Label development, validation, and held-out generators separately.

## Failure policy (must be frozen before the run)

- A fit failure is an outcome to report, not a toy to silently remove.
- The primary pipeline's treatment of failed fits must be specified before running: fail-closed/non-rejection, a prespecified retry sequence, or another defensible policy. Report sensitivity to this policy separately.
- Record all attempts, retry counts, optimizer status, boundary hits, invalid likelihoods, and non-finite test statistics.
- Never let a failed fit become a rejection or non-rejection by accident through default values, NaN comparisons, or exception swallowing.
- The denominator for the end-to-end empirical rejection rate is all generated null toys. If a conditional-on-success diagnostic is shown, label it secondary and show the failure fraction beside it.

## Monte Carlo precision

Choose N from a declared precision target, not from a desire for a large run count. For a binomial proportion near 0.05, the approximate standard error is

    SE(alpha_hat) approximately sqrt(0.05 * 0.95 / N).

For orientation, this is about 0.0069 at N=1,000 and 0.0022 at N=10,000. These are approximate standard errors, not guarantees about interval coverage or bias. Use an exact or Wilson binomial interval in reported tables. Account for multiple generator scenarios and planned comparisons when interpreting uncertainty.

## Required validation before confirmatory runs

1. **Literature comparison:** extract the actual estimands, calibration procedure, model-choice rules, and failure handling in Williams (2017), Cesarotti et al. (2019), BumpNet, NPLM, and LaCATHODE. State the remaining gap in one falsifiable sentence.
2. **Analytic controls:** validate the test statistic and p-value/rejection implementation on cases with known or independently computable answers.
3. **Null calibration control:** verify the full pipeline on a generator where its assumptions hold; quantify Monte Carlo uncertainty.
4. **Adversarial software tests:** exercise fit failure, boundary solutions, invalid likelihoods, empty bins, zero counts, and non-finite outputs. Assert that every toy has exactly one terminal status.
5. **Reference reproduction:** reproduce the relevant documented CMS baseline quantitatively before using data to motivate the pseudoexperiment choices. Code/source review alone is not numerical reproduction.
6. **Freeze:** version-control the protocol, configuration, test statistic, binning, fit range, generator definitions, failure policy, seed scheme, and stopping rule before the confirmatory campaign.

## Data-use boundary

CMS Open Data can anchor a reproducibility case study, but a visible excess in a public histogram is not itself evidence of a resonance. The reduced outreach sample has limited branches and does not support a trigger-aware analysis. Do not infer trigger efficiency, muon quality/isolation effects, or detector performance from fields absent from the sample. Treat the known feature near 30 GeV as a documented trigger/data-taking caveat, not a signal candidate.

The current local ROOT download previously inspected in the user's Downloads folder was a roughly 10 KB HTML response, not a ROOT file. Consequently, this protocol does not claim a completed data run or verified real-data baseline.

## Go/no-go rule

**No-go** for confirmatory simulations while any of the following remains unresolved:
- the literature gap is only “compare models under misspecification”;
- the primary estimand or local/global interpretation is ambiguous;
- generator choices are not independently justified;
- fit failures can be silently dropped or inconsistently counted;
- analytic and software controls are not passing;
- the reference analysis has not been quantitatively reproduced where the project claims reproduction.

**Go** only after the above items are documented, independently reviewed where possible, and frozen. A go decision authorizes a controlled simulation study; it does not imply publication suitability or scientific novelty.

## Source anchors

- Williams, *A novel approach to the bias-variance problem in bump hunting*, JINST 12 (2017) P09034. DOI: 10.1088/1748-0221/12/09/P09034.
- Cesarotti et al., *Searching in CMS open data for dimuon resonances with substantial transverse momentum*, Phys. Rev. D 100 (2019) 015021. DOI: 10.1103/PhysRevD.100.015021.
- *Automatizing the search for mass resonances using BumpNet*, JHEP (2025). DOI: 10.1007/JHEP02(2025)122.
- *Robust resonant anomaly detection with NPLM*, Eur. Phys. J. C (2025). DOI: 10.1140/epjc/s10052-025-14759-w.
- Hallin et al., *Resonant anomaly detection without background sculpting*, Phys. Rev. D 107 (2023) 114012. DOI: 10.1103/PhysRevD.107.114012.
