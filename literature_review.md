# Initial literature map

**Status:** expanded starter review, not an exhaustive systematic review.  
**Last updated:** 2026-10-25

The proposed research gap remains **unproven**. A meaningful close predecessor exists for background-model selection and coverage in bump hunting, so the current model-selection-calibration idea may need to be narrowed or abandoned after full comparison.

## Data and analysis records

### 1. Wunsch (2019), CMS Open Data analysis example
“Analysis of the di-muon spectrum using data from the CMS detector taken in 2012.” DOI: 10.7483/OPENDATA.CMS.AAR1.4NZQ. Official record: https://opendata.cern.ch/record/cms-12342

This example reconstructs opposite-charge dimuon invariant mass using the 2012 Run B/C DoubleMuParked sample and explicitly warns that a feature near 30 GeV is caused by trigger/data-taking conditions, not a resonance. The analysis record itself lists two small files totalling 123.7 KiB; this is not the full event dataset.

### 2. Wunsch (2019), reduced muon event dataset
“DoubleMuParked dataset from 2012 in NanoAOD format reduced on muons.” DOI: 10.7483/OPENDATA.CMS.LVG5.QT81. Official record: https://opendata.cern.ch/record/12341

CERN describes one 2.1 GiB file with 61,540,413 events and branches for muon multiplicity, transverse momentum, pseudorapidity, azimuth, mass and charge. The record says the output was derived from validated runs but had no further validation. This is a candidate for baseline reproduction, not automatic evidence that all trigger variables or detector-level requirements are available.

### 3. CERN CMS Open Data research guidance
Official documentation: https://opendata.cern.ch/docs/cms-guide-for-research and https://opendata.cern.ch/docs/about-cms

The exact dataset, format, event selections, trigger information, data-quality requirements, compatible software, and citation terms must be verified before analysis.

## Closest resonance-search predecessor

### 4. Cesarotti et al. (2019), CMS Open Data dimuon search
“Searching in CMS open data for dimuon resonances with substantial transverse momentum,” *Physical Review D* 100, 015021. DOI: 10.1103/PhysRevD.100.015021. Publisher: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.100.015021

The paper reports a search using 2.11 fb^-1 of 7 TeV CMS Open Data, targeting dimuon masses of 14–66 GeV with transverse-momentum-enhanced selections. It is directly relevant prior work. The complete methods and supplementary details must be read before deciding whether a proposed calibration study overlaps.

## Statistical methods that constrain novelty and design

### 5. Williams (2017), background-model selection and bump hunting
“A novel approach to the bias-variance problem in bump hunting,” *Journal of Instrumentation* 12, P09034. DOI: 10.1088/1748-0221/12/09/P09034. Publisher: https://doi.org/10.1088/1748-0221/12/09/P09034

This is an especially important predecessor: it examines data-driven background-model selection, signal-strength bias, variance, and interval coverage in bump hunts. Because our candidate question also concerns model selection and calibration, we must compare the exact procedure and validation design. The proposed work must not be called novel until this comparison is complete.

### 6. Gross and Vitells (2010), look-elsewhere effect
“Trial factors for the look elsewhere effect in high energy physics,” *European Physical Journal C* 70, 525–530. DOI: 10.1140/epjc/s10052-010-1470-8. Publisher: https://doi.org/10.1140/epjc/s10052-010-1470-8

This paper explains why a local excess at a fixed mass and a search over many possible masses have different false-positive interpretations. Any global-significance claim requires a defined scan and a justified calibration method.

### 7. Cowan et al. (2011), likelihood-based tests
“Asymptotic formulae for likelihood-based tests of new physics,” *European Physical Journal C* 71, 1554. DOI: 10.1140/epjc/s10052-011-1554-0. Publisher: https://doi.org/10.1140/epjc/s10052-011-1554-0

This is a foundational reference on likelihood-ratio test statistics, nuisance parameters, systematic uncertainties, and asymptotic distributions. Our implementation must check whether the assumptions behind any asymptotic p-value are appropriate for the chosen procedure.

### 8. Hallin et al. (2023), resonant anomaly detection
“Resonant anomaly detection without background sculpting,” *Physical Review D* 107, 114012. DOI: 10.1103/PhysRevD.107.114012. Publisher: https://doi.org/10.1103/PhysRevD.107.114012

This work addresses spurious mass-structure risks in enhanced bump hunts involving anomaly scores. It is adjacent rather than identical to the proposed statistical-calibration direction, but it illustrates that selection-induced sculpting is an established concern.

### 9. CMS Collaboration (2023), low-mass dimuon search
“Search for direct production of GeV-scale resonances decaying to a pair of muons in proton-proton collisions at sqrt(s) = 13 TeV,” *JHEP* 12 (2023) 070. arXiv:2309.16003. Primary preprint: https://arxiv.org/abs/2309.16003

Relevant experimental context for low-mass dimuon searches, with a different data-taking and detector context. Review the methods and triggers before comparing results.

## Current assessment of originality

The current idea—compare a fixed background model with a data-selected model and evaluate false-positive calibration under held-out generating distributions—**may already be substantially covered by Williams (2017) or other work**. This cannot be resolved by writing a more ambitious title. We must compare methods line by line, identify any unaddressed question, and only then freeze the project.

If no distinct contribution survives the review, pivot to a narrower reproducibility/validation study and describe it honestly as such. A high-quality replication is worthwhile but should not be represented as a new statistical method.

## Required next review tasks

1. Read the full methods, supplementary material and references of Williams (2017) and Cesarotti et al. (2019).
2. Compare their generating models, fitting procedures, model-selection rules, test statistics, uncertainty intervals, coverage tests, and failure handling with our candidate design.
3. Search the primary literature for post-selection calibration and bump-hunt background-model uncertainty; add sources only after verifying title, authors, DOI or arXiv identifier, and actual claims.
4. Inspect the official CMS analysis source and dataset schema; reproduce the baseline spectrum.
5. Write a concise novelty decision: proceed, narrow, or stop. Record the evidence for that decision.
6. Keep local significance separate from global significance and model-based toy calibration separate from detector-level evidence.
