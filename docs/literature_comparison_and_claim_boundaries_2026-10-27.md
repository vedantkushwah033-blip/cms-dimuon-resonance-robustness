# Literature comparison: what the proposed CMS dimuon study can and cannot claim

**Date:** 2026-10-27  
**Status:** focused literature comparison; not a systematic review and not a novelty certification.  
**Decision:** no confirmatory simulation campaign until the proposed estimand is distinguished from prior methods and the CMS baseline is validated.

## 1. Purpose

The project should not treat a large number of pseudoexperiments, a new code implementation, or a different name for a diagnostic as a scientific contribution. This memo maps the current proposal against the closest papers that can be checked from primary sources and identifies the comparisons still required.

## 2. Closest prior work and implications

### Williams (2017): background-model selection and coverage

Michael Williams, “A novel approach to the bias-variance problem in bump hunting,” *Journal of Instrumentation* 12 (2017) P09034. DOI: https://doi.org/10.1088/1748-0221/12/09/P09034; author manuscript: https://arxiv.org/abs/1705.03578; MIT record: https://dspace.mit.edu/entities/publication/59ee701d-ffd2-480e-88e2-1ccf5c012fc7.

The abstract explicitly studies data-driven background-model selection, uncertainty due to model choice, realistic examples, bias, sensitivity and confidence-interval coverage. This makes “compare fixed and selected background models and report coverage” inadequate as a novelty claim on its own.

**Required follow-up:** read the methods and results in full, then tabulate the exact selection algorithms, data-generating models, test statistics, coverage definitions, and calibration procedures against the proposed study. Do not infer equivalence or novelty from an abstract alone.

### Cesarotti et al. (2019): direct CMS Open Data dimuon predecessor

Cari Cesarotti et al., “Searching in CMS Open Data for Dimuon Resonances with Substantial Transverse Momentum,” *Physical Review D* 100, 015021 (2019). DOI: https://doi.org/10.1103/PhysRevD.100.015021; article: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.100.015021; arXiv: https://arxiv.org/abs/1902.07227.

This is a direct dimuon/CMS Open Data precedent. It studies a physics search and model-independent limits, and the project’s existing focused audit records its local fitting, background choices, fit-window considerations, ringing risk, and trigger-turn-on discussion. The current repository’s outreach-spectrum reproduction uses a different, much narrower educational data product and must not be presented as reproducing the paper’s physics analysis.

**Required follow-up:** distinguish the outreach sample and research-level derived files from the dataset and selection used by the paper. Do not use its publication as evidence that the repository has reproduced the paper.

### Algeri (2020): inference under background mismodeling

Sara Algeri, “Detecting new signals under background mismodeling,” *Physical Review D* 101, 015003 (2020). DOI: https://doi.org/10.1103/PhysRevD.101.015003; article: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.101.015003; arXiv: https://arxiv.org/abs/1906.06615.

This paper directly addresses the risks that background over- or under-estimation can respectively reduce sensitivity or inflate false-discovery risk, and proposes a nonparametric strategy incorporating partial scientific knowledge. A generic “background mismatch can cause false positives” motivation is therefore established prior art.

**Required follow-up:** compare the proposed diagnostic’s estimand and operating characteristics with the actual Algeri procedure, including the information assumptions and null calibration.

### Volkovich, De Vito Halevy & Bressler (2022): data-directed bump hunting

“A data-directed paradigm for BSM searches: the bump-hunting example,” *European Physical Journal C* 82, 265 (2022). DOI: https://doi.org/10.1140/epjc/s10052-022-10215-1; article: https://link.springer.com/article/10.1140/epjc/s10052-022-10215-1.

The paper uses a neural network to estimate a significance distribution from mass histograms and compares predictions against profile-likelihood-based quantities. This is relevant if the proposed project adds a learned diagnostic or a data-directed scan.

**Required follow-up:** compare the actual output target, training/data-generation setup, calibration, and false-positive handling. Do not call a new neural network or diagnostic novel merely because its implementation differs.

### Background-sculpting-resistant anomaly methods (2023)

“Resonant anomaly detection without background sculpting,” *Physical Review D* 107, 114012 (2023). DOI: https://doi.org/10.1103/PhysRevD.107.114012.

This is relevant if a future diagnostic or event-selection step changes the background distribution. The method and assumptions need direct comparison before making any anomaly-detection novelty claim.

## 3. The only defensible candidate gap at present

A narrow candidate question is:

> For a fully specified local resonance-search pipeline, what is the empirical global type-I error and diagnostic false-alarm rate when the complete model-selection, fitting and mass-scan procedure is evaluated on independently generated, prespecified null scenarios not used to develop the diagnostic—and how does this compare with a fair, explicitly chosen existing calibration approach?

This wording is **not a novelty claim**. It may still be answered by prior work. The following must be shown before the question can proceed:

1. A methods-level comparison against Williams (2017), Algeri (2020), and the closest high-energy bump-hunt calibration approaches.
2. A precise operational definition of “held-out” scenario families, including why those scenarios are relevant and how they differ from development scenarios.
3. A fixed global test statistic and complete scan procedure, including all model-selection and diagnostic steps.
4. At least one credible existing comparator implemented with a fair tuning budget.
5. A prespecified primary estimand and Monte Carlo precision target.
6. A clear statement of what decision would change if the diagnostic succeeds or fails.

If these conditions do not reveal a genuine gap, the appropriate product is a carefully bounded reproducibility/benchmark study, not a claim of a new statistical method.

## 4. Evidence that must remain separate

- **Software correctness:** tests, deterministic fixtures, and independent implementation checks.
- **Data reproduction:** actual CMS inputs, verified provenance, documented selection, and quantitative reference parity.
- **Statistical validity:** correct generators, calibration, uncertainty intervals, failure accounting, and fair comparators.
- **Novelty:** a defensible comparison with the closest prior methods.
- **External validation:** independent technical review and a record of exactly what was checked.

Success in one category does not establish the others. In particular, schema branch presence is not trigger-efficiency validation; synthetic acceptance-like distortions are not detector simulations; and a green CI run is not a physics result.

## 5. Immediate go/no-go decision

**GO:** complete the bounded baseline run and artifact review, and expand the methods-level literature comparison.

**NO-GO:** do not start the confirmatory simulation campaign, claim a novel diagnostic, infer trigger efficiency, or report a resonance finding yet.

The workflow artifact review should capture the exact workflow run, commit, input checksums, output metadata, candidate/reference histogram comparison, and cut-flow comparison. A 100,000-entry prefix is a smoke test only; it cannot be described as full-data reproduction.

## 6. Reference links

- Williams (2017): https://doi.org/10.1088/1748-0221/12/09/P09034
- Cesarotti et al. (2019): https://doi.org/10.1103/PhysRevD.100.015021
- Algeri (2020): https://doi.org/10.1103/PhysRevD.101.015003
- Volkovich et al. (2022): https://doi.org/10.1140/epjc/s10052-022-10215-1
- CMS Open Data dimuon outreach analysis repository: https://github.com/cms-opendata-analyses/DimuonSpectrumNanoAODOutreachAnalysis

