# Run-1 dimuon trigger-feasibility gate

**Status:** Documentation-level feasibility only; no ROOT file-level trigger audit has been completed by this repository as of 2026-10-26.

## Purpose

Decide whether the available Run2012B and Run2012C derived datasets support the specific trigger-related estimand before implementing an efficiency or trigger-correction analysis. This is an input-validity gate, not a claim of trigger calibration.

## Official source distinction

1. The 2019 muon-only outreach dataset contains 61,540,413 events in one 2.1 GiB file. Its documented schema lists only `nMuon`, `Muon_pt`, `Muon_eta`, `Muon_phi`, `Muon_mass`, and `Muon_charge`. It is suitable for reconstructing the example dimuon spectrum, but that listed schema is insufficient for a trigger-aware study. See the [CERN record](https://opendata.cern/record/12341).
2. The separate Run2012B and Run2012C derived records publish richer variable lists, including event identity, muon quality/isolation fields, and HLT decision candidates. Those documents motivate file-level investigation but do not prove the exact downloadable files contain every needed field or that the fields are suitable for an efficiency denominator.
3. The original Run2012B and Run2012C AOD records describe the primary datasets, run ranges, validated-run JSON, and possible HLT paths. AOD trigger semantics and derived-column names must not be treated as interchangeable without checking provenance and conversion code. See the [Run2012B AOD record](https://opendata.web.cern.ch/record/6004) and [Run2012C AOD record](https://opendata.web.cern.ch/record/6030).
4. The [CMS Open Data trigger guide](https://opendata.web.cern.ch/docs/cms-guide-trigger-system) explains that trigger paths/configurations can change between runs, that the configuration should be interpreted from the relevant data-taking configuration, and that a decision bit alone is not a complete trigger-efficiency measurement.

## Required audit table

For each Run2012B and Run2012C input, record one of **PASS**, **FAIL**, or **UNKNOWN** for every row. A branch-name match alone can never count as PASS for semantic requirements.

| Requirement | Evidence required | Why it matters |
|---|---|---|
| File provenance | Official record ID, exact file name/URI, byte size, SHA-256 | Makes the result traceable |
| Tree and event coverage | Tree name, entry count, run range, duplicate/event-overlap check if combining files | Prevents accidental sample mixing |
| Branch schema | Actual branch names and ROOT types from the exact file | Detects missing or incompatible fields |
| Event identity | Run, luminosity block, event number where available | Supports duplicate and run-period checks |
| Muon collection integrity | Multiplicity matches across pt, eta, phi, mass, charge, and all used quality fields | Prevents malformed events from silently entering selection |
| HLT decision semantics | Exact path names, path versions, and proof of what a stored boolean represents | Prevents treating similarly named paths as equivalent |
| Run-dependent menu | Official configuration and valid run range for every used path | Path thresholds and filters can change over time |
| Trigger denominator | A justified event/object sample not already conditioned on the trigger being measured, or a documented alternative design | Avoids biased efficiency estimates |
| Prescales and luminosity | Authoritative prescale/luminosity treatment or proof they are not required for the chosen estimand | HLT bits alone do not encode prescale correction |
| Data-quality certification | Validated-run/good-lumisection selection and recorded source | Avoids including uncertified periods |
| Object selection | Explicit offline muon selection with documented variables and thresholds | Needed for a reproducible efficiency definition |
| Independent validation | Spot-check actual event values and compare selection/cutflow with a trusted reference | Branch presence does not validate content |

## Decision rules

- **GO for spectrum reconstruction:** the six muon kinematic/charge branches are present with consistent collection lengths, and the selection/reference convention is specified.
- **GO for a trigger-efficiency study:** only after the trigger decision semantics, run-dependent menu, appropriate denominator, data-quality selection, and required prescale/luminosity treatment are all supported by actual input and authoritative documentation.
- **NO-GO for trigger-efficiency claims:** if the only available evidence is a list of HLT booleans or the sample is already selected by the trigger under study and no valid denominator is available.
- **NARROW the question:** if the file can support mass-spectrum reconstruction and stress tests but cannot support a detector-level trigger measurement. A simulation using an assumed trigger turn-on can study that assumed model; it must be labelled a toy-model stress test, not a CMS trigger measurement.

## Recommended next execution

1. Download or access one small, representative file from each chosen derived record.
2. Run `scripts/inspect_root_schema.py` and preserve the JSON output plus file checksum and official source.
3. Fill this table with evidence, marking unsupported requirements UNKNOWN rather than guessing.
4. Inspect the actual event values and run ranges for all candidate HLT fields.
5. Decide whether to continue with a trigger-efficiency estimand or limit the work to reproducible spectrum reconstruction and clearly labelled simulation studies.

## Non-claims

This document does not claim that any research-level ROOT file has been downloaded, that file-level schema inspection has succeeded, that trigger efficiency has been measured, or that a novel method has been established.


## Exact-path caveat — 2026-10-26

The published derived variable lists document many HLT decision branches, with examples including `HLT_Mu13_Mu8` and `HLT_Mu17_Mu8`. Direct searches did not find `HLT_Dimuon0_Jpsi`, `HLT_DoubleMu11_Acoplanarity03`, or `HLT_DoubleMu5_IsoMu5` on those derived-schema pages. The original AOD record's list of possible paths must not be treated as evidence that the same-named branch exists in the derived files. Select a target path only after checking its exact branch in each file and validating its run-dependent meaning.
