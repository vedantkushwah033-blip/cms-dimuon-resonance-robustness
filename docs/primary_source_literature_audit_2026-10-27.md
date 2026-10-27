# Focused primary-source literature audit: what the closest papers imply

**Date:** 2026-10-27  
**Status:** targeted primary-source review; not systematic; novelty remains unproven  
**Branch:** `research-plan/initial-protocol`

## Executive decision

The current candidate—global false-positive calibration for a model-selection-enabled bump hunt under held-out background misspecification—must remain provisional. Primary-source abstracts and accessible full-text sections confirm substantial overlap in the broad problem area:

- Williams (2017) explicitly studies data-driven background-model selection and uncertainty due to model choice, including confidence-interval coverage.
- Cesarotti et al. (2019) is a substantive CMS Open Data dimuon search, not merely a spectrum plot; it uses event selections, detector/QCD background treatment, and model-independent limits.
- BumpNet (2025) is a machine-learning extension of the data-directed paradigm and reports validation against idealized likelihood-ratio tests, with explicit attention to the look-elsewhere effect.
- Grosso et al. (2025) study NPLM-based resonant anomaly detection, including a hyper-test over selection thresholds and hyperparameter-induced variance.

Therefore, generic claims about model selection, background misspecification, automation, or scan calibration are not a defensible novelty statement. The potential contribution, if any, must be a narrowly defined end-to-end calibration evaluation that differs materially from these methods and uses a fair, credible comparator. That difference has not yet been demonstrated.

## Source-by-source findings

### 1. Williams (2017)

**Verified from primary-source record:** Michael Williams, “A novel approach to the bias-variance problem in bump hunting,” *Journal of Instrumentation* 12 (2017) P09034, DOI 10.1088/1748-0221/12/09/P09034. The MIT repository's abstract states that the paper explores data-driven background-model selection and assigns uncertainty on a signal-strength estimator arising from background-model choice; it evaluates methods on realistic examples and discusses bias, sensitivity, and confidence-interval coverage.

**Implication:** The project cannot claim novelty for simply studying background-model choice, uncertainty from functional-form selection, or coverage.

**Still to extract from the full PDF:** precise model-choice rules; whether and how the entire selection step is repeated in pseudoexperiments; the primary calibration target; scan/look-elsewhere treatment; failure handling; and the exact scenario families. Do not infer omissions from the abstract.

### 2. Cesarotti et al. (2019)

**Verified from the primary arXiv record:** Cari Cesarotti, Yotam Soreq, Matthew J. Strassler, Jesse Thaler, and Wei Xue, “Searching in CMS Open Data for Dimuon Resonances with Substantial Transverse Momentum,” *Physical Review D* 100 (2019) 015021, DOI 10.1103/PhysRevD.100.015021. The abstract describes a search in 2.11 fb⁻¹ of 7 TeV pp collisions, with dimuon transverse-momentum selections and isolated/prompt-muon samples; the latter requires detector-effect and QCD-background information obtained from CMS Open Data.

**Implication:** The repository's simple educational dimuon spectrum is not a reproduction of this published search. Different data format, object/trigger requirements, selections, background model, and estimand must be acknowledged. A 30,000-bin spectrum comparison to the outreach example only validates implementation parity with that example, not the published 2019 search.

**Still to extract:** the paper's exact fit/test procedure and model-independent-limit construction, including any calibration details relevant to a proposed comparison.

### 3. BumpNet (2025)

**Verified from the publisher's open-access record:** Arguin et al., “Automatizing the search for mass resonances using BumpNet,” *Journal of High Energy Physics* (2025), article 122, DOI 10.1007/JHEP02(2025)122; published 19 February 2025. The abstract describes a neural approach extending the Data-Directed Paradigm, trained on smoothly falling analytical functions and realistic simulated data. It predicts statistical-significance distributions across histogram configurations and is validated against idealized likelihood-ratio tests, with attention to the look-elsewhere effect.

**Implication:** “Automating a bump hunt,” “evaluating many histogram configurations,” and “accounting for the look-elsewhere effect” are already active research directions.

**Still to extract:** exact training/test split, null-generating families, significance calibration, uncertainty, and whether the paper evaluates the same end-to-end estimand proposed here.

### 4. Grosso et al. (2025), NPLM

**Verified from the full open-access article:** Grosso, Sengupta, Golling et al., “Robust resonant anomaly detection with NPLM,” *European Physical Journal C* 85, 1074 (2025), DOI 10.1140/epjc/s10052-025-14759-w; published 28 September 2025. The article studies NPLM as an alternative to CWoLa/BDT-based anomaly selection. It discusses end-to-end NPLM testing, the effect of selection-threshold hyperparameters, and a hyper-test across thresholds. It explicitly discusses the need to account for the look-elsewhere effect in sliding-window resonant searches.

**Implication:** A project about threshold/model-selection variance and scan calibration must distinguish itself from this work. The paper's task uses anomaly-selection approaches and benchmark datasets, so it is not automatically the same estimand as a classical polynomial-background fit—but that difference alone does not establish novelty.

**Still to extract:** precise null calibration and failure handling for the exact NPLM test, and a comparison of its assumptions with the candidate classical pipeline.

## Updated candidate research question (not approved/frozen)

If primary-text extraction supports a genuine gap, consider:

> Under which prespecified background-only generator shifts does a fully specified classical dimuon bump-hunt pipeline—with every data-driven model-selection and mass-scan step repeated in null calibration—exceed its target global type-I error, relative to a literature-justified comparator, when all fit failures remain in the end-to-end accounting?

This wording is falsifiable but may still overlap existing work. It must not be presented as novel until the closest papers and supplements are compared line by line.

## Non-negotiable methodological distinctions

- **Local vs global:** a local p-value at one mass is not a global discovery probability after scanning masses.
- **Calibration vs robustness:** nominal calibration under the assumed model and behavior under held-out misspecification are different questions.
- **Selection vs fixed model:** if model selection is data-dependent, the null calibration must reproduce that selection procedure; otherwise the calibration does not describe the deployed pipeline.
- **Failure rate vs conditional performance:** dropping failed fits can bias the apparent rejection rate. The denominator and terminal status of every toy must be recorded.
- **Software parity vs physics validation:** passing tests and reproducing an outreach spectrum do not validate trigger efficiencies, a published search, or a new-physics claim.

## Required next literature pass

For each paper, extract section/page/equation references for:
1. test statistic and null hypothesis;
2. model-selection or threshold-selection rule;
3. whether the full selection/scan is repeated under the null;
4. local/global significance construction;
5. generator families and held-out validation;
6. fit-failure and numerical-boundary treatment;
7. reported Monte Carlo uncertainty and replicate counts;
8. available code/data and reproducibility.

Then write one exact sentence stating what prior work does not answer. If this cannot be supported by specific method-level evidence, reject the candidate gap and pivot.

## Decision and status

- Confirmatory Monte Carlo: **NO-GO**.
- Full real-data baseline parity: **pending**.
- Trigger semantics/denominator feasibility: **pending**.
- Candidate novelty: **not established**.
- Publication or admissions impact: **not predictable from current evidence**.
- Next practical gate: finish source extraction and execute the documented bounded baseline run on checksum-verified files; no need to download multi-gigabyte data merely to advance the literature review.

## Primary-source anchors

- Williams, MIT repository record and author manuscript: DOI 10.1088/1748-0221/12/09/P09034.
- Cesarotti et al., arXiv:1902.04222 and PRD DOI 10.1103/PhysRevD.100.015021.
- Arguin et al., JHEP DOI 10.1007/JHEP02(2025)122.
- Grosso et al., EPJC DOI 10.1140/epjc/s10052-025-14759-w.

The metadata and claims above were checked against publisher/repository primary-source records on 2026-10-27. This is still a focused review, not a systematic review.
