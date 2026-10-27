# Methods extraction worksheet: Williams (2017) and Cesarotti et al. (2019)

**Date:** 2026-10-27  
**Status:** preliminary extraction from accessible primary-source records/text; not a complete supplementary-material audit  
**Branch:** `research-plan/initial-protocol`

## Purpose

This worksheet converts the closest prior-art sources into concrete comparison questions. It is deliberately conservative: where a detail has not been verified from the complete methods and supplementary material, it is marked unresolved rather than assumed absent.

## Williams (2017): bias-variance and background-model choice

**Source:** Michael Williams, “A novel approach to the bias-variance problem in bump hunting,” *Journal of Instrumentation* 12 (2017) P09034, DOI 10.1088/1748-0221/12/09/P09034.

### Verified at abstract/record level
- The work explores data-driven background-model selection.
- It considers uncertainty in a signal-strength estimator arising from the choice of background model.
- It evaluates methods on realistic example problems.
- It discusses bias, sensitivity, and confidence-interval coverage.

### Consequence for this repository
The project cannot claim a new contribution merely for comparing background families, quantifying model-choice uncertainty, measuring bias/variance, or reporting coverage.

### Must inspect in full paper before claiming a gap
- Exact candidate model families and selection rule.
- Which selection decisions are repeated within each pseudoexperiment.
- Primary estimand and coverage construction.
- Treatment of scans over mass or analysis choices.
- Generator assumptions, finite-sample design, and uncertainty in reported calibration.
- Fit-failure and boundary handling.
- Which components are intended for direct comparison to a classical CMS dimuon pipeline.

**Status:** unresolved; abstract-level evidence only is not enough to infer a missing method.

## Cesarotti et al. (2019): CMS Open Data dimuon search

**Source:** Cari Cesarotti, Yotam Soreq, Matthew J. Strassler, Jesse Thaler, and Wei Xue, “Searching in CMS Open Data for Dimuon Resonances with Substantial Transverse Momentum,” *Physical Review D* 100 (2019) 015021, DOI 10.1103/PhysRevD.100.015021.

### Verified from accessible primary text
- Uses CMS Open Data from 7 TeV collisions and describes a search for narrow dimuon resonances.
- Uses separate isolated-muon and prompt-muon samples and dimuon transverse-momentum selections.
- Scans mass hypotheses with local windows and a profiled-likelihood approach.
- Uses a fifth-order polynomial background and checks a cubic alternative and different window choices.
- Discusses correlated subsidiary p-value spikes (“ringing”) and the relationship to global p-values.
- Describes discrete profiling across polynomial models as a cross-check/alternative.

### Consequence for this repository
A proposal to study polynomial background choice, window size, local scan behavior, model profiling, or global p-value effects is already close to this work. Any new study must identify a sharply delimited unresolved question rather than repeat these dimensions under a new title.

The repository's planned public-example spectrum comparison is **not** a reproduction of this published resonance search. A basic opposite-charge pair spectrum does not reproduce the paper's triggers, event selection, kinematic categories, signal model, likelihood, systematic uncertainties, or limits.

### Must inspect in full paper and supplement before claiming a gap
- Exact local p-value and global-statistic procedures.
- Which scan/window choices are fixed and which are optimized from data.
- The extent and design of any pseudoexperiment calibration.
- Exact calibration generators and the handling of model misspecification.
- How discrete profiling and model-selection uncertainty enter inference.
- Numerical precision and fit-failure accounting.
- Which of these details overlap with the candidate study's intended estimand.

**Status:** substantial overlap established; remaining technical details unresolved.

## Comparison questions that must be answered before any confirmatory run

| Question | Williams (2017) | Cesarotti et al. (2019) | Current repository |
|---|---|---|---|
| Background-model choice | Present at high level; exact rules to extract | Polynomial alternatives/discrete profiling discussed | No validated bump-hunt implementation established |
| Mass/window scan | Exact handling to extract | Local mass-window scan described | Not implemented/validated as a complete search pipeline |
| Global calibration | Exact procedure to extract | Global p-value/ringing discussed; exact details to extract | Not established |
| Misspecification stress tests | Exact generators to extract | Exact generators/calibration to extract | Candidate only; no confirmatory simulation |
| Fit failures | Unresolved | Unresolved from current extraction | Must define and test before simulation |
| Reproduction status | Not attempted | Not reproduced; distinct from public educational example | Public-example numerical parity pending |

## Stop/go decision

**NO-GO for confirmatory Monte Carlo remains.** The next task is full methods extraction plus the real-data baseline parity test. If the extracted procedures already answer the proposed question, the project should pivot to a transparent reproduction/validation artifact or formulate a genuinely different question with a defensible motivation. A replication can be valuable when executed rigorously, but it must be described as a replication or educational validation, not as a novel statistical method.

## Evidence references

- Williams (2017) primary repository record: https://dspace.mit.edu/entities/publication/59ee701d-ffd2-480e-88e2-1cc5f012fc7
- Cesarotti et al. (2019) primary publisher/DOI record: https://doi.org/10.1103/PhysRevD.100.015021
- BumpNet (2025) primary publisher record for broader context: https://link.springer.com/article/10.1007/JHEP02%282025%29122
