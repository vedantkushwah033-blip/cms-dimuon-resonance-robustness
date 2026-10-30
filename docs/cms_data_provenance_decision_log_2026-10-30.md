# CMS data provenance and trigger-semantics decision log

**Updated:** 2026-10-30  
**Purpose:** prevent dataset/format confusion and unsupported trigger claims.

## Officially verified records

| Record | DOI / record | What CERN states | Permitted role at present |
|---|---|---|---|
| Run2012B DoubleMuParked AOD | 10.7483/OPENDATA.CMS.YLIC.86ZZ; record 6004 | 29,308,627 events, 2,279 files, 7.9 TiB; run range 193833–196531; lists possible HLT paths | Research-grade AOD source; requires CMSSW/ROOT workflow and exact file/run certification |
| Run2012C DoubleMuParked AOD | 10.7483/OPENDATA.CMS.M5AD.Y3V3; record 6030 | 36,820,243 events, 2,920 files, 9.8 TiB; run range 198022–203742; lists possible HLT paths | Research-grade AOD source; requires CMSSW/ROOT workflow and exact file/run certification |
| Reduced Run2012B+C muon NanoAOD-like file | 10.7483/OPENDATA.CMS.LVG5.QT81; record 12341 | 61,540,413 events, one 2.1 GiB file; muon kinematics/charge; no further validation of reduced output | Pipeline development and cautious descriptive cross-check only |
| Public dimuon analysis example | 10.7483/OPENDATA.CMS.AAR1.4NZQ; record cms-12342 | Analysis example using 2012 DoubleMuParked data; warns of a feature near 30 GeV associated with trigger/data-taking | Reference-method and known-artifact context; not the full event sample |

## Important distinctions

1. The AOD datasets (Run2012B and Run2012C) are not the same object as the reduced 2.1 GiB outreach file.
2. The 2.1 GiB record has a useful Events tree with muon kinematics and charge, but it does not provide the trigger and muon-quality information needed to claim a trigger-aware analysis.
3. A schema-only inspection of one research-level file per period is not a full dataset validation.
4. A list of possible HLT paths does not tell us which path fired for a particular event, whether it was active in a given run, its prescale, or the event-level efficiency.
5. A trigger decision bit is not an efficiency denominator. Efficiency studies require an independently selected reference sample and a documented prescale/luminosity treatment.
6. Good-run certification must be applied consistently with the exact data-taking period and reprocessing. The AOD records point to the 2012 certification JSON.
7. The known feature near 30 GeV in the public analysis example must not be interpreted as a new resonance.

## Confirmed vs pending

### Confirmed from official records
- Run2012B and Run2012C AOD records are separate and have the stated event/file scales.
- Both records describe the DoubleMuParked primary dataset and list possible HLT paths.
- The reduced muon record has 61,540,413 events, one 2.1 GiB file, and the five muon kinematic/charge branches plus multiplicity.
- CERN explicitly says no further validation was done on the reduced output.
- The public analysis example flags the 30 GeV feature as trigger/data-taking related.

### Pending
- Verify exact file checksums and provenance for every research-level NanoAOD-like file used.
- Inspect the full branch schema for each exact selected file, including types and event counts.
- Establish HLT path version/run-range activation and any prescale information.
- Verify the event-selection and good-run certification applied to each derived file.
- Determine whether an unbiased reference sample exists for a trigger-efficiency measurement.
- Reproduce the official dimuon reference spectrum quantitatively from the same event-selection definition.
- Obtain and review the source code/configuration used to create the reduced research-level ntuples.

## Decision

Do not use the phrase "trigger-efficiency measurement" unless an appropriate reference sample, trigger decisions, run-dependent path configuration, prescale/luminosity treatment, and efficiency denominator are established. Until then, the defensible target is statistical robustness to modeled acceptance distortions, with CMS data providing descriptive context and a reproducible spectrum baseline.
