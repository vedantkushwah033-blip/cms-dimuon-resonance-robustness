# Data-source assessment and go/no-go decision

**Assessment date:** 2026-10-25  
**Status:** source inspected; full data processing not yet performed.

## 1. Separate the analysis example from the event dataset

The CERN Open Data analysis record for Wunsch's 2012 dimuon spectrum is DOI **10.7483/OPENDATA.CMS.AAR1.4NZQ** and is available at https://opendata.cern.ch/record/cms-12342. The record says its example uses the 2012 Run B/C DoubleMuParked dataset, reconstructs opposite-charge dimuon invariant masses, and warns that a feature near 30 GeV is trigger/data-taking related rather than a resonance.

That analysis record itself contains two small files totalling 123.7 KiB. **Those are not the full event dataset.** The linked reduced NanoAOD event dataset is a separate record: DOI **10.7483/OPENDATA.CMS.LVG5.QT81**, https://opendata.cern.ch/record/12341. CERN describes it as one file, 2.1 GiB, with 61,540,413 events and muon branches for multiplicity, transverse momentum, pseudorapidity, azimuth, mass, and charge.

This correction matters for storage, compute planning and provenance. Do not report the 123.7 KiB analysis example as the size of the event sample.

## 2. What the available variables support

The reduced event dataset has enough listed muon kinematics and charges to reconstruct opposite-charge dimuon masses. It does not, from the listed schema alone, provide a complete detector-level trigger model, all event-level trigger decisions, all isolation variables, or all information needed to reproduce a modern analysis selection. The portal says no further validation was done on the reduced output beyond using validated runs for the source data.

Therefore:
- It is a plausible **baseline reproduction and pipeline-validation** sample.
- It is not automatically suitable for every proposed trigger-misspecification experiment.
- A toy generator based on fitted mass shapes would test statistical behaviour under that toy model, not detector-level CMS realism.
- We must inspect the original analysis source and data schema before claiming any selection or trigger variable is available.

## 3. Candidate research-grade alternatives

The 2019 Cesarotti et al. paper reports an analysis of 2.11 fb^-1 of 7 TeV CMS Open Data in a pT-enhanced dimuon search, using dimuon masses from 14 to 66 GeV and discussing background modelling. This is close prior work and must be reviewed in full before a novelty claim.

A research-grade reanalysis might require an accessible primary CMS dataset with the needed trigger/selection branches and a defensible luminosity/data-quality description. The repository must not assume those inputs are available merely because an outreach-derived sample exists. A data feasibility check is a gate, not a formality.

## 4. Go/no-go decision at this stage

**GO for:** downloading/inspecting the documented reduced NanoAOD sample; reproducing the reference mass spectrum; verifying the schema; checking the trigger feature and invariant-mass calculation.

**NOT YET APPROVED for:** claiming trigger-aware calibration on real CMS events, claiming a novel bump-hunt method, or launching a large main simulation.

**Next evidence required:**
1. Exact event schema and source code reviewed.
2. Reference spectrum reproduced and discrepancy report recorded.
3. Full closest-prior-work comparison completed.
4. A clearly defined estimand and generating/fitting model frozen.
5. A reasoned explanation of what the reduced dataset can and cannot validate.

## 5. Source records

- Wunsch, 2019 analysis record: DOI 10.7483/OPENDATA.CMS.AAR1.4NZQ; https://opendata.cern.ch/record/cms-12342
- Wunsch, 2019 reduced event dataset: DOI 10.7483/OPENDATA.CMS.LVG5.QT81; https://opendata.cern.ch/record/12341
- Cesarotti et al., Phys. Rev. D 100, 015021 (2019), DOI 10.1103/PhysRevD.100.015021; https://doi.org/10.1103/PhysRevD.100.015021
