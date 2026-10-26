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

The linked Run2012B variable documentation exposes a more specific distinction than broad field-family names alone suggest:

- The documented HLT collection is described as HLT_Activity_Ecal_SC7/O, not a documented family of DoubleMuParked path decisions.
- The documented L1 collection is L1_AlwaysTrue/O.
- HLTriggerFirstPath and HLTriggerFinalPath are documented as Boolean fields, but the published semantics page does not define them as per-path decisions for the DoubleMuParked muon triggers.
- Trig is explicitly a generic flag for triggers suitable for Minimum Bias analysis.
- TrigObj is described as only partially filled.
- The documentation includes Dataset_DoubleMu as a dataset-membership flag. Membership in a primary dataset is not equivalent to a per-event decision for a particular HLT path, and it does not provide prescale information.

These details strengthen the current no-go decision for a trigger-efficiency or trigger-emulation claim based solely on the documented fields. They do not prove that every possible trigger-related input is absent from every file; the exact ROOT schema and relevant trigger-condition metadata still require file-level inspection.

## Exact-file access status

The official records identify the merged filenames Run2012B_DoubleMuParked_merged.root and Run2012C_DoubleMuParked_merged.root, and state that the collections can be accessed through XRootD or direct download. In this session, the record pages expose the descriptive metadata and semantics links but not a directly verifiable file URL in the parsed page. Therefore no guessed EOS path is recorded and no file-level schema result is claimed.

Official references:
- https://opendata.cern.ch/record/31123
- https://opendata.cern.ch/record/cms-31129
- https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/derived-data/NanoAODRun1/31123/Run2012B_DoubleMuParked_doc.html
- https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/derived-data/NanoAODRun1/31129/Run2012C_DoubleMuParked_doc.html
