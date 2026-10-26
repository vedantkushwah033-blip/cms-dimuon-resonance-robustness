# Research-level Run2012B/C schema feasibility audit — 2026-10-26

**Evidence level:** official record-level variable documentation reviewed; exact ROOT files have not yet been opened by this repository. This is not a file-level schema validation.

## Official records

- Run2012B DoubleMuParked research-level NanoAOD-like ntuples: https://opendata.cern.ch/record/cms-31123
- Run2012C DoubleMuParked research-level NanoAOD-like ntuples: https://opendata.cern.ch/record/cms-31129
- Run2012B documented variable list: https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/derived-data/NanoAODRun1/31123/Run2012B_DoubleMuParked_doc.html
- Run2012C documented variable list: https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/derived-data/NanoAODRun1/31129/Run2012C_DoubleMuParked_doc.html
- CERN CMS trigger guide: https://opendata.cern.ch/docs/cms-guide-trigger-system

CERN describes these as research-level NanoAOD-like ntuples derived directly from AOD with validated runs. The records report 26,084,708 Run2012B events across 57 files (75.6 MiB) and 35,455,705 Run2012C events across 74 files (101.1 MiB). The records say the files are available over XRootD or by direct download.

## Promising documented fields

The published variable lists include:
- Event identity: `run`, `luminosityBlock`, `event`.
- Muon kinematics and charge: `Muon_pt`, `Muon_eta`, `Muon_phi`, `Muon_mass`, `Muon_charge`.
- Candidate muon quality/selection fields such as `Muon_isGlobal`, `Muon_isTracker`, `Muon_isGood`, `Muon_tightId`, `Muon_mediumId`, `Muon_softId`, and `Muon_pfRelIso03_all` / `Muon_pfRelIso04_all`.
- A `GoodLumisection` field is documented as available for some, but not all, datasets; its presence and semantics must be verified for the exact files.
- Trigger-related items include `HLT_Activity_Ecal_SC7`, `HLTriggerFirstPath`, `HLTriggerFinalPath`, a generic `Trig` flag described as suitable for Minimum Bias analysis, and `TrigObj` described as only partially filled so far.

These fields suggest that the research-level files may support a better documented baseline than the muon-only outreach file. However, the published variable list does **not** by itself establish that the specific DoubleMuParked HLT path decisions, path configuration history, or prescales needed for a trigger-aware analysis are present. In particular, generic trigger-related fields are not a substitute for a documented per-path decision and prescale model.

## Feasibility judgement

| Proposed use | Current judgement | Why |
|---|---|---|
| Reconstruct a dimuon mass spectrum with documented muon-quality selections | Plausible, pending exact file inspection | Kinematics, charge, and multiple quality/isolation candidates are documented |
| Compare selected and unselected spectra as a robustness study | Potentially feasible, pending prespecified selections and validation | Event identity and candidate object-quality fields are documented, but exact branch semantics and consistency need inspection |
| Claim trigger efficiency or emulate the DoubleMuParked trigger | **Not established / no-go for now** | Per-path trigger decisions and prescale metadata have not been confirmed; generic `Trig` and partially filled `TrigObj` are insufficient evidence |
| Make a discovery or claim a new resonance | **No-go** | No research question, statistical calibration, systematic model, or full-data reproduction has passed the relevant gates |

## Next exact-file check

Before changing the analysis plan, run `scripts/inspect_root_schema.py` on one actual Run2012B file and one actual Run2012C file identified from the official record file lists. Save the exact file URL, checksum if available, schema JSON, tree entry count, and branch types. Confirm the actual presence and types of event identity, muon-quality, trigger-related, and luminosity-block fields. Do not infer that a record-level variable list guarantees a branch is present in every file.

If the files do not contain the needed path-specific trigger decisions and prescale inputs, narrow the project to a transparently selected-spectrum/background-modelling robustness study with a documented trigger limitation—or choose a data source whose trigger metadata can be validated. Do not label it a trigger-efficiency analysis.



## Follow-up: what the published schema actually says about triggers

A closer reading of the detailed variable-list tables changes one part of the initial interpretation: the top-level collection summary names HLT_Activity_Ecal_SC7, but the detailed Run2012B and Run2012C variable lists also enumerate many individual Boolean HLT branches, including HLT_Mu13_Mu8 and HLT_Mu17_Mu8. Therefore it would be incorrect to conclude from the top-level summary alone that no path-specific HLT decision branches are documented.

What the public documentation does and does not establish:

- It documents path-named Boolean branches such as HLT_Mu13_Mu8 and HLT_Mu17_Mu8 in both Run2012B and Run2012C semantics tables.
- It also documents HLTriggerFirstPath and HLTriggerFinalPath, but these generic fields should not be substituted for a target path decision.
- Trig is described as a generic flag suitable for Minimum Bias analysis, and TrigObj is described as only partially filled.
- Dataset_DoubleMu is a dataset-membership flag, not itself a trigger-efficiency denominator.
- The published schema documentation does not by itself establish the exact branch presence and values in the specific downloaded files, the precise run-dependent meaning/version of each path bit, the correct denominator for an efficiency measurement, or the prescale/luminosity treatment.

This means path-specific HLT branches are a **plausible file-inspection lead**, not an automatic no-go. Trigger-efficiency or trigger-emulation claims remain blocked until the exact ROOT files, run-dependent path definitions, denominator, data-quality selection, and prescale/luminosity requirements are validated. The original AOD path lists must not be treated as a substitute for derived-file schema evidence.

## Exact-file access status

The official records identify the merged filenames Run2012B_DoubleMuParked_merged.root and Run2012C_DoubleMuParked_merged.root and state that the collections can be accessed through XRootD or direct download. In this session, the record pages expose descriptive metadata and semantics links but not a directly verifiable file URL in the parsed page. No guessed EOS path is recorded and no file-level schema result is claimed.

Official references:
- https://opendata.cern.ch/record/31123
- https://opendata.cern.ch/record/cms-31129
- https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/derived-data/NanoAODRun1/31123/Run2012B_DoubleMuParked_doc.html
- https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/derived-data/NanoAODRun1/31129/Run2012C_DoubleMuParked_doc.html
