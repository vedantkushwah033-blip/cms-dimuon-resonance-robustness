# Literature overlap decision checkpoint: classical dimuon bump hunts

**Date:** 2026-10-27  
**Status:** focused primary-source comparison; not systematic; novelty unproven  
**Branch:** `research-plan/initial-protocol`

## Executive finding

The candidate idea of evaluating global false-positive calibration for a scan-based dimuon bump hunt under background-model misspecification faces substantial prior-art overlap. The closest sources do more than generally discuss bump hunting:

- Williams (2017) explicitly studies data-driven background-model selection and uncertainty from model choice, including confidence-interval coverage.
- Cesarotti et al. (2019) describes a CMS Open Data dimuon resonance search that scans mass hypotheses, performs local background fits, compares polynomial orders/window choices, discusses correlated subsidiary p-value spikes (“ringing”), and relates these to global p-values.
- BumpNet (2025) studies automated resonance searches across histogram configurations and discusses the look-elsewhere effect.
- CMS's later direct low-mass dimuon resonance result demonstrates that a real experimental search requires detailed trigger-stream, event selection, background and detector treatment; a simple educational spectrum is not a substitute.

Accordingly, “we scan masses and study background-model choice” is not a sufficient research gap. The present project should remain a reproducibility and statistical-methodology study until a narrower, demonstrably distinct question is identified.

## Primary-source anchors

1. **Williams (2017)** — Michael Williams, “A novel approach to the bias-variance problem in bump hunting,” *Journal of Instrumentation* 12 (2017) P09034, DOI 10.1088/1748-0221/12/09/P09034. The primary abstract describes data-driven background-model selection, model-choice uncertainty, bias/variance, and confidence-interval coverage.  
   Primary record: https://dspace.mit.edu/entities/publication/59ee701d-ffd2-480e-88e2-1cc5f012fc7

2. **Cesarotti et al. (2019)** — “Searching in CMS Open Data for Dimuon Resonances with Substantial Transverse Momentum,” *Physical Review D* 100 (2019) 015021, DOI 10.1103/PhysRevD.100.015021. The paper describes a local mass-window search using a profiled likelihood, a fifth-order polynomial background with cubic cross-checks, variation of window sizes, discrete profiling across polynomial models, and discussion of ringing and global p-values. This is especially close to the project's dimuon context.  
   Primary publisher record: https://doi.org/10.1103/PhysRevD.100.015021

3. **BumpNet (2025)** — Arguin et al., “Automatizing the search for mass resonances using BumpNet,” *Journal of High Energy Physics* (2025), article 122, DOI 10.1007/JHEP02(2025)122. It studies machine-learning-assisted bump hunting across histogram configurations and includes validation against likelihood-ratio tests and look-elsewhere considerations.  
   Primary publisher record: https://link.springer.com/article/10.1007/JHEP02%282025%29122

4. **CMS direct low-mass dimuon search (2023)** — CMS Collaboration, CMS-EXO-21-005, JHEP 12 (2023) 070. It searches Run 2 data using a dedicated high-rate trigger stream and reports model-independent limits. This establishes an experimental reference point but is not the same dataset or analysis as the current educational Run 2012 baseline.  
   Official CMS result: https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-21-005/index.html

## What is not yet established

The source-level review above is a focused audit, not a systematic literature review. It does **not** establish that the candidate question is novel or that every relevant paper has been checked. Before choosing a research contribution, the project still needs section-by-section extraction of the methods and supplementary material, especially:

- the exact null-generating families and which fitting/model-selection steps are repeated for every pseudoexperiment;
- the exact local/global test statistic and calibration target;
- the role of discrete profiling, model choice, and mass-window selection;
- treatment of fit failures, boundaries, and invalid test statistics;
- comparator fairness, uncertainty on calibration estimates, and held-out validation.

Absence of a detail from an abstract is not evidence that a paper omits it.

## Recommended project positioning for now

A defensible short-term objective is **reproducible implementation and independent validation of a documented CMS Open Data dimuon baseline**, with explicit boundaries between the educational spectrum, the published 2019 search, and any later simulation study.

A later statistical-methods contribution should proceed only if the detailed comparison reveals a concrete unanswered question. Possible dimensions to investigate—not claims of novelty—include a sharply defined end-to-end failure-accounting rule or a prespecified stress test of a specific pipeline component. These would still need literature verification, analytic controls, fair comparators, and empirical evidence.

## Gate before confirmatory Monte Carlo

**NO-GO for confirmatory simulation remains in force.** The next actions are methods extraction and numerical baseline reproduction. Do not run a large toy campaign simply to accumulate a high run count; that cannot fix a weak estimand, a mismatched comparator, or an unproven novelty claim.

## Next concrete work items

1. Extract and cite the relevant sections/supplements from Williams (2017) and Cesarotti et al. (2019) in the comparison matrix.
2. Separate “reproduce the public educational example” from “reproduce a published resonance search” in project language and outputs.
3. Obtain a valid official ROOT input and compare event counts, selected pairs, invariant masses, and histogram bins against the public reference on identical events.
4. Reassess the candidate question only after steps 1–3; document a no-go/redirection decision if no meaningful gap survives.
