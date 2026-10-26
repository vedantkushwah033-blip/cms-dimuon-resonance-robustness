# Literature scope update: acceptance sculpting and bump-hunt calibration

**Checked:** 2026-10-27  
**Purpose:** focused extension to the initial literature screen; not a systematic review.  
**Decision:** keep the main simulation campaign on hold. A potentially defensible contribution has not yet been isolated.

## Sources checked

1. **Cesarotti et al. (2019), “Searching in CMS open data for dimuon resonances with substantial transverse momentum.”** The analysis discusses background fitting, polynomial order and fit-window sensitivity, ringing, discrete profiling, and the trigger turn-on limitation. This directly overlaps with a generic claim that trigger/acceptance structures can complicate dimuon bump hunts.
   - Journal: https://doi.org/10.1103/PhysRevD.100.015021
   - Preprint: https://arxiv.org/abs/1902.07227

2. **Williams (2017), “A novel approach to the bias-variance problem in bump hunting.”** This work evaluates data-driven background-model selection and uncertainty/coverage in toy ensembles. Generic background misspecification, coverage, or false-positive comparisons therefore cannot be claimed as new without a more precise distinction.
   - Journal: https://doi.org/10.1088/1748-0221/12/09/P09034
   - Preprint: https://arxiv.org/abs/1705.03578

3. **Volkovich, De Vito Halevy and Bressler (2022), “A data-directed paradigm for BSM searches: the bump-hunting example.”** This proposes an algorithmic/data-directed approach to finding deviations from smoothly falling mass spectra. It reinforces that a new diagnostic or decision procedure needs direct comparison with existing algorithms, not only a new toy setup.
   - Journal: https://doi.org/10.1140/epjc/s10052-022-10215-1

4. **Hallin et al. (2023), “Resonant anomaly detection without background sculpting.”** LaCATHODE explicitly studies and addresses background sculpting in enhanced bump hunts. Any proposed diagnostic framed broadly as detecting or preventing mass-spectrum sculpting risks substantial overlap unless its estimand and operating conditions are clearly different.
   - Journal: https://doi.org/10.1103/PhysRevD.107.114012

5. **Yallup and Handley (2023), “Hunting for bumps in the margins.”** This develops a Bayesian marginal-likelihood approach to background modelling and signal extraction, adding another close methodological comparison for any proposal involving Bayesian background selection.
   - Journal: https://doi.org/10.1088/1748-0221/18/05/P05014
   - Preprint: https://arxiv.org/abs/2211.10391

6. **CMS Collaboration (2023), “Search for direct production of GeV-scale resonances decaying to a pair of muons in proton-proton collisions at √s = 13 TeV.”** This is a different run period and search, not a substitute dataset; it illustrates that trigger stream, selection, mass range, and event content must be treated as analysis-specific.
   - CMS result: https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-21-005/index.html
   - Journal: https://doi.org/10.1007/JHEP12(2023)070
   - Preprint: https://arxiv.org/abs/2309.16003

7. **CERN Open Data Run2012B and Run2012C research-level NanoAOD-like records.** Both official semantics tables document path-named Boolean fields including `HLT_Mu13_Mu8` and `HLT_Mu17_Mu8`, plus event identity, muon kinematics, quality/isolation candidates, and a `GoodLumisection` flag described as not present in all datasets. This is stronger evidence than the collection-summary page alone, but it remains record-level documentation, not proof that the branches exist and are correctly interpreted in the specific files we download.
   - Run2012B: https://opendata.cern.ch/record/31123
   - Run2012B semantics: https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/derived-data/NanoAODRun1/31123/Run2012B_DoubleMuParked_doc.html
   - Run2012C: https://opendata.cern.ch/record/cms-31129
   - Run2012C semantics: https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/derived-data/NanoAODRun1/31129/Run2012C_DoubleMuParked_doc.html

## Research decision

### Not defensible yet
Do not claim novelty for:
- rediscovering the known structure near 30 GeV in the outreach spectrum;
- showing that trigger/acceptance distortions can alter a mass spectrum;
- comparing a few polynomial orders or fit windows;
- reporting coverage or false-positive rates for generic misspecified backgrounds;
- adding a Bayesian label without a genuinely different inferential target and comparison.

### Candidate question to test, not yet approved
For a fully specified, fixed bump-hunt procedure, can a prespecified diagnostic trained only on development distortion families detect calibration failures on genuinely held-out, smooth acceptance-like distortions, while maintaining the nominal false-positive rate on held-out null backgrounds?

This candidate is worthwhile only if:
1. The complete procedure and diagnostic are compared against credible baselines from the cited literature.
2. The distortion family is clearly defined as a **synthetic stress test**, not a CMS trigger simulation.
3. The held-out split is defined before confirmatory results are inspected.
4. The target estimand, scan/global-test interpretation, fit failures, Monte Carlo uncertainty, and success/failure criteria are frozen in advance.
5. A focused broader literature review establishes that the precise diagnostic/estimand is not already answered.

### Immediate priority
The current next step remains exact-file inspection for the official Run2012B/C research-level records. Until the schema and selection are verified, there is no basis to claim a trigger-efficiency analysis. A defensible paper may ultimately be a narrower reproducibility and statistical-validation study; that is preferable to overstating an unproven novelty claim.
