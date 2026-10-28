# Literature matrix for the adaptive dimuon bump-hunt calibration question

**Audit date:** 2026-10-28  
**Status:** expanded preliminary map; not a systematic review, not exhaustive, and not a novelty certification.

## Question being screened

For a prespecified mass range and candidate background families, what is the empirical null rejection probability of the *entire adaptive search procedure* when the analyst chooses/fits the background and scans mass using the same spectrum? How does calibration change when the null-generating process is outside the fitted candidate family?

This is a methodological simulation question. It is not, by itself, a claim about a new resonance, a validated CMS detector effect, or a new statistical method.

## Literature matrix

| Work | What it already addresses | Consequence for this project | Remaining distinction to investigate |
|---|---|---|---|
| Williams (2017), “A Novel Approach to the Bias-Variance Problem in Bump Hunting,” JINST 12 P09034, DOI [10.1088/1748-0221/12/09/P09034](https://doi.org/10.1088/1748-0221/12/09/P09034) | Data-driven background-model selection, uncertainty from model choice, bias/variance, and interval coverage in bump hunts. | Background-model choice, bias, or coverage alone cannot be presented as the new contribution. | Does a held-out, generator-misspecified assessment of the global type-I error of a fully specified adaptive scan add a clearly distinct estimand, or is it covered by existing studies? |
| Gross & Vitells (2010), “Trial factors for the look elsewhere effect in high energy physics,” EPJC 70, 525–530, DOI [10.1140/epjc/s10052-010-1470-8](https://doi.org/10.1140/epjc/s10052-010-1470-8) | The look-elsewhere effect and trial-factor approximations for searches over an unknown parameter such as resonance mass. | A scan over mass already creates a known multiplicity/calibration problem. A proposal must compare with established look-elsewhere treatments, not describe the mass scan itself as novel. | How does additional data-adaptive background selection affect calibration relative to a correctly implemented scan-level null calibration? |
| Vaslin et al. (2022), “Fitting the BumpHunter test statistic distribution and global p-value estimation,” arXiv:2211.07446 | Estimation of global BumpHunter p-values from pseudo-experiments, including a fitted tail approximation to reduce computational burden. | Global bump-hunt calibration and computationally efficient estimation of global p-values are established topics. | The proposed project must specify whether it evaluates a different failure mode (e.g. generator misspecification) rather than merely reimplementing global p-values. |
| Cesarotti et al. (2019), “Searching in CMS Open Data for dimuon resonances with substantial transverse momentum,” PRD 100, 015021, DOI [10.1103/PhysRevD.100.015021](https://doi.org/10.1103/PhysRevD.100.015021) | A research-level CMS Open Data dimuon resonance search, with event selections, background treatment, a profiled-likelihood strategy, and model-independent limits. | “Use CMS Open Data to search for dimuon resonances” is not a novelty claim. This repo currently does not reproduce this paper’s selection or result. | The current work should remain a software/reference validation and a controlled statistical-method study unless it can document a well-defined connection to this analysis. |
| “A data-directed paradigm for BSM searches: the bump-hunting example” (EPJC, 2022), DOI [10.1140/epjc/s10052-022-10215-1](https://doi.org/10.1140/epjc/s10052-022-10215-1) | A data-directed strategy for identifying regions of interest and then following them with conventional analysis. | The broader issue of exploratory searches and post-selection inference is already actively studied. | Clarify whether the proposed estimand is a null false-positive rate for a fixed algorithm, not the general merits of exploratory/data-directed search. |
| “Gaussian process regression as a sustainable data-driven background estimate method at the (HL)-LHC” (EPJC, 2025), DOI [10.1140/epjc/s10052-025-14574-3](https://doi.org/10.1140/epjc/s10052-025-14574-3) | Gaussian-process background estimation in collider bump hunting and pseudo-experiment-based false-positive assessment with BumpHunter. | Gaussian-process backgrounds and pseudo-experiment false-positive studies are not new in isolation. | If a GP is included, it should be a prespecified comparator or one candidate model, not the claimed contribution. The evaluation must account for the complete fitting and scanning procedure. |
| “Resonant anomaly detection without background sculpting,” PRD 107, 114012 (2023), DOI [10.1103/PhysRevD.107.114012](https://doi.org/10.1103/PhysRevD.107.114012) | How anomaly-score selection can sculpt a resonant observable and create downstream bump-hunt complications. | Selection-induced structures and background sculpting are a distinct, related source of spurious features; a trigger-only or smooth-function misspecification simulation would not automatically cover it. | Decide whether sculpting is out of scope or a separate scenario. Do not conflate it with a detector-trigger feature without a model and evidence. |
| Wunsch (2019), “Analysis of the di-muon spectrum using data from the CMS detector taken in 2012,” CERN Open Data record 12342, DOI [10.7483/OPENDATA.CMS.AAR1.4NZQ](https://doi.org/10.7483/OPENDATA.CMS.AAR1.4NZQ) | An educational Run2012B/C dimuon spectrum and its event-processing context; explicitly warns that the feature near 30 GeV is caused by data-taking/trigger effects, not a resonance. | The educational histogram is not a valid basis for a discovery claim. Matching its bins would validate only a defined reproduction target, not trigger efficiency or physics interpretation. | Establish exact-file numerical parity and separately document trigger semantics before making any detector-related claim. |

## Statistical design implications

1. **Name the estimand before choosing the simulation.** For example, at nominal level alpha, estimate the probability that the complete frozen background-fit + model-selection + mass-scan procedure rejects under each named null generator. Do not interchange this with local p-value calibration, confidence-interval coverage, or power.
2. **Make the algorithm complete.** Freeze the mass range, binning, candidate signal widths, background families, fit ranges, optimization criteria, nuisance treatment, scan statistic, and every data-dependent choice. If any of these are selected using the pseudo-data, repeat that choice inside every pseudo-experiment.
3. **Separate development, calibration, and evaluation.** Use independent random streams and distinct generator scenarios. A held-out scenario should not be used to tune thresholds or repair the method after seeing its results.
4. **Include standard comparators.** At minimum, distinguish a correctly calibrated scan-level baseline (e.g. a BumpHunter-style maximum statistic) from the adaptive background-selection procedure. Compare like-for-like estimands and compute Monte Carlo uncertainty.
5. **Account for failure modes.** Predefine failed-fit handling, non-convergence, boundary estimates, empty/low-count bins, and the number of valid replicates. Report failure rates rather than silently dropping difficult pseudo-experiments.
6. **Separate null calibration from power.** Evaluate false-positive control using background-only pseudo-data. Assess signal-injection power separately, over prespecified signal masses and yields.
7. **Do not overstate scope.** Synthetic background families are not automatically realistic CMS spectra. Real-data histogram parity does not establish a valid trigger model, and neither establishes discovery significance.

## Focused comparison: the closest calibration overlap

The 2025 Barr & Liu paper is especially important to the proposed direction. Its published methods describe background-only pseudo-experiments, BumpHunter p-value distributions, false-positive assessment, residual background-modelling biases, and separate signal-injection tests. It also studies a Gaussian-process background estimator on a CMS-derived dijet spectrum and projects performance to an HL-LHC scenario. Therefore:

- A project that merely compares background estimators with pseudo-experiments, checks BumpHunter false positives, or adds a Gaussian-process comparator would substantially overlap with established work.
- The current project should not claim that false-positive calibration under background modelling, pseudo-experiments, or GPR-based bump hunting is new.
- A possible narrower distinction is the *evaluation design*: freeze the entire adaptive procedure, then test its global type-I error on independently held-out generating processes deliberately outside the fitted candidate family. This is a hypothesis about a possible gap, not a verified gap.
- The distinction is only meaningful if the proposed procedure actually includes adaptive model selection and the same-data scan, and if its estimand and comparator differ materially from existing BumpHunter/GPR studies. A simple change of dataset or larger replicate count is not enough.

This comparison was checked against the publisher's article page: Barr & Liu, *European Physical Journal C* 85, 846 (2025), DOI 10.1140/epjc/s10052-025-14574-3. The publisher describes background-only pseudo-experiments and BumpHunter-based false-positive testing in the methods. See https://link.springer.com/article/10.1140/epjc/s10052-025-14574-3. The arXiv preprint is https://arxiv.org/abs/2503.07289.

## Current decision

**GO for literature-informed protocol development; NO-GO for confirmatory simulation or novelty claims.**

Before unblocking confirmatory runs:
- expand the search to original BumpHunter/Hypertest references, trial-factor and random-field methods, discrete profiling/model uncertainty, and post-selection inference;
- inspect the methods and appendices of the listed papers, not only abstracts;
- write a one-page estimand-and-comparator table and have a statistician/HEP analyst review it;
- establish the exact-file baseline parity gate independently;
- freeze protocol fields and preserve the validator's evidence gates.

This matrix records a research triage, not proof that the search is complete. The project should be described as a reproducible methodological benchmark/replication until a defensible gap is supported by the wider literature and results.
