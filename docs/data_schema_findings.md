# Data-schema findings and open checks

**Last checked:** 2026-10-26
**Implementation note:** the schema tool reports candidate branch groups, but group absence is not proof that an analysis is impossible; branch semantics and the exact intended selection must be checked against producer documentation.  
**Status:** public record documentation reviewed; no CMS ROOT file has yet been opened by this project. The schema inspector and spectrum reconstruction CLI are tested on synthetic ROOT files.

## Official record-level facts

### Run2012B DoubleMuParked research-level ntuple
- Record: https://opendata.cern.ch/record/31123
- The CERN Open Data record describes a research-level NanoAOD-like ntuple processed from AOD using validated runs, with 26,084,708 events across 57 files (75.6 MiB).
- CERN explicitly warns that not all variables are available.

### Run2012C DoubleMuParked research-level ntuple
- Record: https://opendata.cern.ch/record/cms-31129
- The CERN Open Data record describes a research-level NanoAOD-like ntuple processed from AOD using validated runs, with 35,455,705 events across 74 files (101.1 MiB).
- The linked official variable-list documentation includes HLT decision bits, including several dimuon trigger paths, as well as muon quality and isolation variables.

### Education/outreach reduced samples (distinct from the research-level records)
- Record: https://opendata.cern.ch/record/12341
- The 61,540,413-event file is reduced to muon kinematics and charge for an educational analysis. CERN states that no further validation was performed on the reduced output.
- Treat it as a development example unless a separate validation justifies a broader role.

## What these facts do and do not establish

The Run2012B/C variable-list documentation makes a trigger-aware study more plausible than the muon-only outreach sample. However, the record-level pages are not inspections of the actual files. We have not yet established:
- Exact branch names in a downloaded/streamed file for each period.
- Whether Run2012B has the same HLT fields as Run2012C.
- Whether prescale values, trigger menus, and run-dependent trigger definitions are available.
- Whether the selected stream and trigger path support the intended mass range and selection.
- Whether all required run/luminosity-block and event-quality metadata are present.
- Whether the original reference analysis can be reproduced using these reduced ntuples.

An HLT decision bit indicates a stored path decision; it does not by itself establish trigger efficiency, turn-on behavior, prescale treatment, or an unbiased sample.

## File-level audit protocol

1. Choose one file from Run2012B and one from Run2012C; record exact official file paths and checksums where possible.
2. Run `python scripts/inspect_root_schema.py --input <file> --output outputs/schema_run2012B.json` (and likewise for Run2012C).
3. Check tree names, event counts, identifiers, muon kinematics/quality/isolation fields, HLT branches, and any prescale/luminosity metadata.
4. Cross-reference the actual branches with the producer tool and the original 2012 dimuon analysis code.
5. Record a pass/fail/unknown for each required input. Unknown is not a pass.
6. Only then select the primary dataset and revise the research question to match what the data can genuinely support.

## Official variable-list cross-check — 2026-10-26

The CERN-published variable-list documentation linked from both research-level records was inspected directly:

- Run2012B: https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/derived-data/NanoAODRun1/31123/Run2012B_DoubleMuParked_doc.html
- Run2012C: https://opendata.cern.ch/eos/opendata/cms/dataset-semantics/derived-data/NanoAODRun1/31129/Run2012C_DoubleMuParked_doc.html

Both published variable lists document many event-level HLT decision branches, including examples such as `HLT_Mu13_Mu8` and `HLT_Mu17_Mu8`, alongside muon kinematics, charge, and several quality/isolation fields. Direct searches did not find `HLT_Dimuon0_Jpsi`, `HLT_DoubleMu11_Acoplanarity03`, or `HLT_DoubleMu5_IsoMu5` on those derived-schema pages. This supports a trigger-aware *schema investigation*, but not a claim that any specific desired path is available.

This is documentation-level evidence only: it does not replace opening the exact downloadable ROOT file and checking its tree, branch types, event-level values, run coverage, and missingness. The published variable lists do not document prescale values. An HLT boolean records a path decision; by itself it does not provide trigger efficiency, prescale correction, the full run-dependent trigger menu, or an unbiased denominator for an efficiency measurement.

Next file-level checks:
1. Inspect a representative ROOT file from each period and preserve the schema reports and checksums.
2. Confirm the exact dimuon HLT branches and any `GoodLumisection`/run/luminosity-block fields in those files.
3. Establish the path versions and run ranges from CMS trigger documentation; do not pool periods or path versions without a justified mapping.
4. Treat prescale availability as unresolved until a documented source is identified.

## Precision correction to the trigger-branch inventory — 2026-10-26

The published Run2012B and Run2012C variable-list pages were checked directly for the specific names previously listed above. They do document many HLT boolean branches, including `HLT_Mu13_Mu8` and `HLT_Mu17_Mu8`, and L1 double-muon decisions. However, searches of those variable-list pages did **not** find `HLT_Dimuon0_Jpsi`, `HLT_DoubleMu11_Acoplanarity03`, or `HLT_DoubleMu5_IsoMu5`. Those names must not be described as documented branches in these derived ntuples on the evidence currently checked. Some of these names appear in the original AOD record's list of possible HLT paths; that is not proof they are present in the derived ntuple.

This corrects the overly specific branch examples in the preceding subsection. The defensible conclusion is narrower: the published derived schemas contain many named HLT decisions, including some dimuon-related paths, but the exact target path needed for the proposed estimand must be checked in each actual file and against the run-dependent configuration. Trigger-efficiency feasibility remains unresolved.
