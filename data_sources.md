# Data sources and provenance

**Status:** candidate sources inspected at the record level; no event-level analysis has yet been run.  
**Last updated:** 2026-10-26

## Candidate A — CMS 2012 dimuon analysis example
- Official analysis record: https://opendata.cern.ch/record/cms-12342
- DOI: 10.7483/OPENDATA.CMS.AAR1.4NZQ
- Title: “Analysis of the di-muon spectrum using data from the CMS detector taken in 2012”
- It reconstructs opposite-charge dimuon invariant mass using the 2012 Run B/C DoubleMuParked sample.
- It explicitly warns that the bump near 30 GeV is a trigger/data-taking effect, not a resonance.
- **Important size distinction:** this analysis record lists two small files totalling 123.7 KiB. These are the analysis example files, not the full event dataset.

## Candidate B — education/outreach reduced CMS 2012 event dataset
- Official dataset record: https://opendata.cern.ch/record/12341
- DOI: 10.7483/OPENDATA.CMS.LVG5.QT81
- Title: “DoubleMuParked dataset from 2012 in NanoAOD format reduced on muons”
- CERN describes one 2.1 GiB file with 61,540,413 events. Listed branches include muon multiplicity, transverse momentum, pseudorapidity, azimuth, mass, and charge.
- The record says the reduced sample was derived from validated runs but that no further validation was performed on the output.

**Feasibility assessment:** suitable as a software-development example only until independently validated. The official record explicitly says no further validation was performed on the reduced output. The listed schema does not include trigger decisions or selection variables. Do not use this dataset alone to support physics-measurement claims or a trigger-misspecification study.

## Candidate C — research-level Run-1 DoubleMuParked ntuples (preferred for feasibility assessment)

- **Run2012B:** https://opendata.cern.ch/record/cms-31123
- **Run2012C:** https://opendata.cern.ch/record/cms-31129
- These are CMS Open Data group research-level NanoAOD-like ntuples processed from AOD. The portal states they were processed using validated runs; it also notes that not all variables are available. Run2012B is listed as 26,084,708 events across 57 files (75.6 MiB); Run2012C as 35,455,705 events across 74 files (101.1 MiB).
- They are stronger candidates for a research baseline than the education/outreach muon-only file, but that does not automatically validate a specific analysis.
- Before use, download or stream a small sample and run `scripts/inspect_root_schema.py`. Record exact file URLs, branch names, trigger-related fields, event identifiers, muon quality/isolation fields, and relevant selection information. Branch-name matches are only leads; inspect the original producer and analysis documentation. The official Run2012C variable-list page documents HLT decision branches (including several HLT_DoubleMu paths) and muon quality/isolation fields. This is encouraging for a trigger-aware feasibility study, but it is not a substitute for inspecting the exact merged file. The corresponding Run2012B branch list and any prescale/trigger-menu metadata still need direct confirmation.
- If the required trigger decisions, prescales, or event-quality information are absent, do not claim trigger-level robustness. Re-scope to what the available data genuinely support.

## Candidate D — prior CMS Open Data resonance analysis
- Cesarotti et al. (2019), *Physical Review D* 100, 015021
- DOI: 10.1103/PhysRevD.100.015021
- Publisher page: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.100.015021
- This is a close methodological predecessor. It uses 2.11 fb^-1 of 7 TeV CMS Open Data in a pT-enhanced dimuon search and discusses resonance-search methods. Read the full methods and references before claiming novelty.

## Candidate E — research documentation and additional methods
- CMS Open Data research guide: https://opendata.cern.ch/docs/cms-guide-for-research
- CMS Open Data overview: https://opendata.cern.ch/docs/about-cms
- Williams (2017), background-model selection and bump-hunting uncertainty: https://doi.org/10.1088/1748-0221/12/09/P09034

The Williams paper is particularly important because it studies data-driven background-model selection and coverage. Our candidate research question may overlap substantially and must be compared carefully.

## Required provenance record before full processing
Record: official record and DOI; exact file names and checksums where possible; dataset version; data-taking period; luminosity/certification source if used; trigger paths and turn-on/prescale caveats; object definitions; selections; branch names and units; software versions; citation/reuse conditions; and whether each input is observed collision data, simulated detector events, model-generated pseudoexperiments, or artificial stress-test data.

## Three categories that must never be conflated
1. **Observed CMS collision data:** measured events subject to the released sample's trigger, detector, and data-quality conditions.
2. **Background-only pseudoexperiments:** synthetic samples generated from an explicitly specified null model.
3. **Artificial stress-test samples:** samples generated from deliberately altered assumptions to evaluate robustness.

Only the first category is observed collision data. A parametric toy model does not become detector-level CMS data because it uses a spectrum inspired by CMS.

## Data minimization and stop conditions
Start with a small sample or documented example. Do not run a full 2.1 GiB data pass or a large simulation campaign until the baseline selection, data schema, software environment, and reference comparison are established. If the needed trigger information is unavailable, narrow the research question rather than claiming trigger-level calibration.
