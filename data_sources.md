# Data sources and provenance

**Status:** candidate sources; dataset selection not yet finalized.  
**Last updated:** 2026-10-25

## Candidate 1 — CMS dimuon spectrum from 2012
- Official CERN Open Data record: https://opendata.cern.ch/record/cms-12342
- Title: “Analysis of the di-muon spectrum using data from the CMS detector taken in 2012”
- Author listed on record: Stefan Wunsch
- DOI: 10.7483/OPENDATA.CMS.AAR1.4NZQ
- Description: opposite-charge dimuon invariant-mass spectrum from CMS Run B and C 2012 data.
- Important caveat: the official record describes a feature near 30 GeV as a trigger/data-taking effect, not a resonance. Any reproduction must preserve this warning and document trigger requirements.

**Feasibility status:** candidate only. Inspect the linked technical description, input files, code, triggers, data-quality requirements, and citation instructions before deciding it supports the proposed calibration study.

## Candidate 2 — CMS Open Data research documentation
- Official research guide: https://opendata.cern.ch/docs/cms-guide-for-research
- Official overview of CMS data: https://opendata.cern.ch/docs/about-cms

The portal distinguishes primary collision datasets from simulated samples and explains that object selections, data-quality requirements, and software compatibility matter. Do not assume every desired simulation sample or detector variable is available for every released data-taking period.

## Candidate 3 — prior CMS Open Data resonance analysis
- Cesarotti et al. (2019), Physical Review D 100, 015021
- DOI: 10.1103/PhysRevD.100.015021
- Publisher page: https://journals.aps.org/prd/abstract/10.1103/PhysRevD.100.015021

This is a methodological reference, not the project's dataset by default. It discusses local dimuon mass fits and background-model/window choices and must be studied carefully to avoid duplicating its analysis.

## Required provenance record before data processing
Record at minimum: portal record and DOI; exact dataset file names and checksums if available; collision period and data-taking conditions; luminosity and certification source; trigger paths, prescale/turn-on considerations, and event selection; object definitions and quality criteria; whether each input is real collision data, simulated collision data, or generated stress-test data; software environment and compatibility constraints; citation and reuse conditions.

## Three categories that must never be conflated
1. **Observed CMS collision data:** public measured sample, subject to its trigger, detector, and data-quality conditions.
2. **Background-only pseudoexperiments:** synthetic samples drawn from an explicitly specified null-generating model.
3. **Artificial stress-test samples:** samples generated from deliberately altered assumptions to test robustness.

Only the first category is real collision data. The other two are simulations used to assess statistical behaviour.

## Data minimization
Do not download large files until the chosen analysis, required branches/variables, software stack, and baseline validation steps are clear. Start with the smallest sample or portal-provided example that can establish feasibility.
