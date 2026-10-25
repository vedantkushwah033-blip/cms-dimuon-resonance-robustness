# Initial literature map

**Status:** starter bibliography, not an exhaustive systematic review.  
**Last updated:** 2026-10-25

Related work clearly exists; novelty of the proposed combination is not established. This file separates verified starting points from open review tasks.

## Primary sources and official records

### 1. CMS Open Data dimuon spectrum record
Stefan Wunsch, “Analysis of the di-muon spectrum using data from the CMS detector taken in 2012” (CERN Open Data Portal, 2019), DOI: 10.7483/OPENDATA.CMS.AAR1.4NZQ. Official record: https://opendata.cern.ch/record/cms-12342

The record describes an opposite-charge dimuon invariant-mass spectrum over a wide mass range and explicitly notes a structure near 30 GeV caused by the trigger used in data-taking rather than a resonance. Trigger and selection documentation is therefore essential. This is a starting point for learning/reproduction, not automatically the correct dataset for a new calibration study.

### 2. Research use of CMS Open Data
CERN Open Data Portal, “CMS Guide to research use of CMS Open Data.” Official documentation: https://opendata.cern.ch/docs/cms-guide-for-research

The guide explains available research datasets and example analyses. Released data require domain-specific selection and software knowledge, and the released samples/software have limitations. The exact data format, trigger, run period, luminosity, certification, and compatible simulation must be checked for the chosen analysis.

### 3. Published CMS Open Data dimuon resonance search
Cesarotti et al., “Searching in CMS open data for dimuon resonances with substantial transverse momentum,” Physical Review D 100, 015021 (2019), DOI: 10.1103/PhysRevD.100.015021. Official APS page: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.100.015021

This work uses CMS Open Data to search for narrow dimuon resonances and discusses local background fitting, polynomial choices, fit windows, and correlated spurious structures (“ringing”). Simply comparing polynomial orders or changing a fit window is not by itself a defensible novelty claim. The full methods and references must be read before finalizing the exact test.

### 4. CMS low-mass dimuon resonance search
CMS Collaboration, “Search for direct production of GeV-scale resonances decaying to a pair of muons in proton-proton collisions at sqrt(s) = 13 TeV,” JHEP 12 (2023) 070. Official result page: https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-21-005/index.html ; arXiv: https://arxiv.org/abs/2309.16003

This is relevant scientific context for low-mass dimuon searches and trigger streams, but it uses a different data-taking context and is not a direct recipe for the older public dataset. Review the selection and background treatment before drawing comparisons.

## Limitations of this initial review
- The research question remains provisional. These sources establish close prior work, not a research gap.
- This is not yet a comprehensive review of statistical literature on likelihood-ratio tests under misspecification, spurious-signal tests, goodness-of-fit diagnostics, trials factors/look-elsewhere corrections, or coverage calibration.
- Claims in the supplied project brief about a 2025 anomaly-detection paper and conformal-calibration work have not been accepted as evidence here until exact title, authors, publication status, DOI/arXiv ID, and primary source are verified. Do not cite uncertain metadata.
- Do not claim that the proposed diagnostic is new. First identify the exact diagnostic and compare it against established methods.
- Do not assume the CMS record provides all required variables or simulations. Inspect the record's associated dataset and technical documentation.

## Required next literature-review tasks
1. Read the complete methods and supplementary material of the 2019 CMS Open Data resonance paper.
2. Identify prior studies that explicitly run background-only pseudoexperiments and assess type-I error or p-value calibration under alternative background models.
3. Review established look-elsewhere-effect methods and distinguish local from global significance.
4. Review spurious-signal and bias tests used in resonance searches, including whether the proposed diagnostic duplicates a known method.
5. Verify every citation against its publisher, collaboration, CERN record, or arXiv primary page.
6. Record what each prior study does and does not test in a comparison table before calling any gap unresolved.
