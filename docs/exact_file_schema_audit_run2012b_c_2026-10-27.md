# Exact-file schema audit: Run2012B/C DoubleMuParked

**Audit date:** 2026-10-27  
**Workflow:** [research-level CMS ROOT schema audit](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40403830670)  
**Artifact:** `research-level-schema-audit` (workflow artifact; expires 2026-11-09)  
**Purpose:** establish what the sampled ROOT files contain before selecting a physics question. This is a schema inventory, not an event-selection validation or a trigger-efficiency measurement.

## Files inspected

The workflow used the CERN Open Data client to download one checksum-verified ROOT file from each official record and inspected its `Events` tree with `uproot`.

| Record | Local file in workflow artifact | Bytes | SHA-256 | Events tree entries | Branches |
|---|---|---:|---|---:|---:|
| [Run2012B DoubleMuParked, record 31123](https://opendata.cern.ch/record/31123) | `03C5684F-8BAF-4312-8235-2B0039F2FB93.root` | 1,454,534,615 | `293a9aa2a61f734ad19670925da3220eb4338b931576b115c75892307e8796d7` | 481,872 | 907 |
| [Run2012C DoubleMuParked, record 31129](https://opendata.cern.ch/record/cms-31129) | `06C1145E-99D4-4DAC-859D-F634CC8714AF.root` | 1,542,887,879 | `6e2fe573bb00f0f612e71ab04c82a845d9bf52b1ba9a5a0898afaab97b733b7d` | 515,439 | 894 |

These are two sampled files, not the complete records. The row counts are not dataset totals and should not be used as an exposure or luminosity estimate.

## Required branch inventory

Both sampled files contain the following branches with matching reported types:

| Branches | Type in both files |
|---|---|
| `Muon_pt`, `Muon_eta`, `Muon_phi`, `Muon_mass` | `float[]` |
| `Muon_charge` | `int32_t[]` |
| `Muon_tightId`, `Muon_mediumId` | `bool[]` |
| `Muon_pfRelIso03_all`, `Muon_pfRelIso04_all`, `Muon_dxy`, `Muon_dz` | `float[]` |
| `run`, `luminosityBlock`, `event` | `uint32_t`, `uint32_t`, `uint64_t` |
| `GoodLumisection` | `bool` |
| `HLT_Mu13_Mu8`, `HLT_Mu17_Mu8`, `HLT_Mu8`, `HLT_Mu17_TkMu8` | `bool` |

The Run2012B sample contains 438 branch names beginning `HLT_` and 128 beginning `L1_`; the Run2012C sample contains 427 `HLT_` and 126 `L1_` names. Trigger menus differ between the files: for example, `HLT_Mu17_Mu8_DZ` and `HLT_Mu17_TkMu8_DZ` were not present in either sampled file. This makes explicit per-period path selection essential; do not silently assume the same trigger menu across periods.

## What this establishes

1. The sampled research-level files have the event identity, muon four-vector ingredients, charge, several quality/isolation candidates, a good-lumisection flag, and many trigger-related branches needed to design an analysis.
2. The exact files can be identified reproducibly by record ID, filename, size, and SHA-256.
3. The `Events` tree has a substantial branch inventory; the analysis should read only needed branches rather than loading all branches at once.

## What this does **not** establish

- It does not validate the semantics or event-by-event correctness of each branch beyond its reported name and ROOT type.
- Branch presence does not establish whether a trigger path was unprescaled, active, or appropriate for a particular event/run; nor does it provide trigger efficiency.
- It does not establish the dataset's certified integrated luminosity, event deduplication, overlap between records, or a valid trigger-efficiency denominator.
- It does not show that the mass spectrum reproduces a published result, and it does not support a new-physics claim.
- The two-file sample is not a representative scan of all files or all run conditions.

## Required next checks before physics claims

1. Read the official record and semantics documentation for exact dataset provenance and branch meaning; retain the version/date of the documentation.
2. Check run/lumisection distributions and the meaning/application of `GoodLumisection`; do not assume it replaces an authoritative certified-lumisection JSON.
3. Verify the selected trigger paths against run-dependent menus and dataset stream logic. Do not estimate efficiency from a stream selected by the same trigger without a defensible independent denominator.
4. Inspect jagged-array lengths and non-finite values; verify muon-pair construction, charge selection, four-vector mass calculation, and event-level selection.
5. Reproduce a published control distribution or reference analysis before starting the proposed robustness study.
6. Freeze the estimand, selection, fit window, background alternatives, test statistic, scan/global significance treatment, and held-out synthetic stress-test families before looking at confirmatory results.

## Provenance

The machine-readable schema reports and manifest are attached to workflow run [40403830670](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40403830670). The workflow's successful status means download, checksum verification, inspection, and artifact upload completed; it is not a scientific validation result.


## Cross-file branch-set comparison

A reproducible comparison of the two schema JSON artifacts gives the following counts:

| Branch group | Run2012B | Run2012C | Present in both | B-only | C-only |
|---|---:|---:|---:|---:|---:|
| All branch names | 907 | 894 | 833 | 74 | 61 |
| Names beginning `HLT_` | 438 | 427 | 370 | 68 | 57 |
| Names beginning `L1_` | 128 | 126 | 122 | 6 | 4 |

**Interpretation:** the sampled files share most branch names but the HLT menus are not identical. In particular, the absence of a branch in one file must not be treated as a zero-valued trigger decision. The analysis should explicitly define a common-path set or period-specific mapping, validate path versions against run ranges, and report period-specific results before any combination. This comparison is between two files only and cannot establish the full menu evolution across all runs or files.
