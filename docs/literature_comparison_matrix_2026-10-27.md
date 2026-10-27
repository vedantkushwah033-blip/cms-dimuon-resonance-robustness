# Literature comparison matrix: full-pipeline bump-hunt calibration

**Date:** 2026-10-27  
**Status:** focused desk-review matrix; not a systematic review; no novelty claim  
**Branch:** `research-plan/initial-protocol`

## Why this matrix exists

The project should not proceed from “background-model choice can affect bump hunts” to a large simulation campaign: that broad concern is already represented in the literature. The useful question is whether a precisely defined end-to-end estimand, comparator, and held-out evaluation remain unanswered by the closest methods.

The entries below are intentionally conservative. “Not established from current review” means the relevant full text/method supplement still needs to be checked; it does **not** mean the paper omits the feature.

## Method-by-method comparison

| Work | Main target / contribution (high-level) | Connection to this project | Must verify from primary text before claiming a gap |
|---|---|---|---|
| Williams (2017), *A novel approach to the bias-variance problem in bump hunting*, JINST 12 P09034 | Data-driven background-function choice and bias/variance trade-offs in bump hunting | Direct overlap with model selection and uncertainty effects | Exact test statistic, model-selection rule, calibration target, treatment of scan/look-elsewhere effects, and whether complete selection is repeated inside null toys |
| Cesarotti et al. (2019), *Searching in CMS open data for dimuon resonances with substantial transverse momentum*, PRD 100 015021 | A CMS Open Data dimuon resonance search with specified selections and background treatment | Direct reference for data provenance, spectrum reconstruction, and baseline analysis choices | Exact event selection, fit/window choices, test statistic, local/global significance treatment, and what numerical outputs can be reproduced from available public artifacts |
| Algeri and related look-elsewhere-effect literature | Statistical calibration when searching across a parameter space / many candidate locations | Essential for distinguishing local-window false-positive rate from global discovery probability | Which approximation or toy calibration applies to the proposed scan; assumptions and limitations |
| Volkovich et al. (2022), data-directed bump hunting | Methods that use data to guide the search or optimize aspects of a bump hunt | Potential overlap with selection effects induced by looking across analysis choices | Exact optimization/search procedure and how its null distribution is calibrated |
| Hallin et al. (2023), *Resonant anomaly detection without background sculpting*, PRD 107 114012 | Anomaly-detection approach designed to avoid background sculpting | Alternative approach; relevant if the proposed pipeline uses learned or data-driven selection | Whether it addresses the same estimand and event-level setup; do not imply equivalence merely because both are resonance searches |
| BumpNet (2025), JHEP 02 (2025) 122 | Automated resonance-search/significance approach across histogram configurations | Recent automated-search comparator; broad “automation improves bump hunting” claim is not novel by itself | Exact calibration target, training/validation split, model dependence, coverage or false-positive guarantees, and applicability to this classical pipeline |
| Robust resonant anomaly detection with NPLM (2025), EPJC | NPLM-based resonant anomaly detection and practical robustness considerations | Recent alternative anomaly-detection family | Exact null calibration, scan procedure, nuisance treatment, and whether comparisons include full-pipeline selection |
| Other profile-likelihood / discrete profiling / spurious-signal methods | Established ways to account for background functional-form uncertainty in resonance searches | Could be a closer comparator than an ad hoc fixed polynomial | Identify the closest method for the intended estimand; define fair matching before choosing the final baseline |

## Required extraction fields

For each closest paper, record the following from the paper and supplement, with page/section/equation references:

1. **Scientific setting:** collision/data context, observable, mass range, and event selection.
2. **Target estimand:** local p-value, global p-value, false-positive rate, bias, coverage, power, or another quantity.
3. **Background treatment:** fixed model, discrete profiling, data-directed selection, ensemble, learned model, or other.
4. **Selection inside calibration:** whether every data-dependent selection/tuning step is repeated in null pseudoexperiments.
5. **Scan correction:** single window, local result, asymptotic look-elsewhere correction, or global calibration of the maximum statistic.
6. **Failure accounting:** treatment of fit failures, invalid covariance, boundaries, and non-finite statistics.
7. **Validation design:** same-family validation, held-out generator family, real-data closure, or other.
8. **Uncertainty reporting:** Monte Carlo uncertainty, interval method, and replicate count where applicable.
9. **Reproducibility:** available code/data/configuration and whether a result can be independently reproduced.
10. **Unanswered decision:** the exact methodological decision this work does not settle, supported by evidence rather than absence of a keyword.

## Candidate gap test

A defensible gap statement must be narrower than “background misspecification affects bump hunts.” It should identify:

- one fully specified pipeline;
- one primary end-to-end estimand (candidate: scenario-specific global type-I error);
- one credible, literature-linked comparator;
- a held-out set of null-generating scenarios that was not used for tuning;
- explicit fit-failure and Monte Carlo uncertainty handling; and
- a practical decision that would change if the comparison found poor calibration.

If the closest paper already performs this comparison under materially equivalent assumptions, **reject this candidate gap** and revise the project. A different dataset, more pseudoexperiments, or more plots alone do not establish methodological novelty.

## Evidence status

- The project has a focused source-screening memo and related methods notes, but this matrix is not a systematic review.
- Exact methods extraction for every row is **incomplete**.
- No claim is made that no prior paper addresses the candidate estimand.
- The project remains **NO-GO for confirmatory Monte Carlo** pending exact-file baseline validation, completed primary-text comparison, comparator choice, and protocol freeze.
- No new-physics, resonance, trigger-efficiency, publication-readiness, or admissions-impact claim follows from this document.

## Source anchors

- Williams (2017), DOI: 10.1088/1748-0221/12/09/P09034.
- Cesarotti et al. (2019), DOI: 10.1103/PhysRevD.100.015021.
- BumpNet (2025), DOI: 10.1007/JHEP02(2025)122.
- NPLM resonant anomaly detection (2025), DOI: 10.1140/epjc/s10052-025-14759-w.
- Hallin et al. (2023), DOI: 10.1103/PhysRevD.107.114012.

Verify full bibliographic metadata and cite exact pages/equations before manuscript use.
