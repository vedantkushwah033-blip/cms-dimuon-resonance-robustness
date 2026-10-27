# Independent audit of the 27 October research-level workflow artifact

**Audit date:** 2026-10-27  
**Repository:** `vedantkushwah033-blip/cms-dimuon-resonance-robustness`  
**Workflow run:** [40403830670](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40403830670)  
**Artifact:** `research-level-schema-audit`, ID `12691464206`  
**Run head:** `5ba056432af970485be6cc6b21ba9dfc15453a2b`

## What I independently inspected

I downloaded the artifact ZIP from GitHub Actions and inspected its actual contents rather than inferring them from the green workflow status.

The ZIP contains exactly three files:

- `manifest.tsv`
- `schema_31123.json`
- `schema_31129.json`

It contains **no** candidate spectrum CSV, ROOT reference spectrum CSV, histogram comparison JSON, metadata comparison JSON, or per-comparison exit-status file.

The manifest records:

| CERN record | File | Bytes | SHA-256 |
|---|---|---:|---|
| 31123 (Run2012B DoubleMuParked) | `03C5684F-8BAF-4312-8235-2B0039F2FB93.root` | 1,454,534,615 | `293a9aa2a61f734ad19670925da3220eb4338b931576b115c75892307e8796d7` |
| 31129 (Run2012C DoubleMuParked) | `06C1145E-99D4-4DAC-859D-F634CC8714AF.root` | 1,542,887,879 | `6e2fe573bb00f0f612e71ab04c82a845d9bf52b1ba9a5a0898afaab97b733b7d` |

The schema JSON reports 481,872 `Events` entries and 907 branch names for the sampled Run2012B file, and 515,439 entries and 894 branch names for the sampled Run2012C file. The branch inventories include muon kinematics/charge, event identifiers, `GoodLumisection`, and trigger-named branches. This is evidence of file-level schema inspection only.

## Why the green run does not establish numerical parity

I retrieved the workflow definition at the run's actual head commit. At that commit, `.github/workflows/research-level-schema-audit.yml` was a **schema-only push-triggered workflow**: it downloaded one ROOT file from each record, ran `scripts/inspect_root_schema.py`, and uploaded the schema JSON plus manifest. It did not run the spectrum reconstruction, ROOT reference exporter, or either comparator.

The current research branch subsequently gained a revised manual workflow that includes a 100,000-entry candidate/reference comparison. That later workflow must not be retroactively attributed to run 40403830670. The current branch's manual workflow also remains unavailable for dispatch until a `workflow_dispatch` workflow is present on the default branch, or an equivalent controlled execution path is used.

## Decision

- **Exact-file provenance and schema for one file per Run2012B/C DoubleMuParked record:** PASS for the bounded files listed above.
- **Candidate/reference histogram parity:** NOT RUN / NOT ESTABLISHED by this artifact.
- **Candidate/reference cut-flow agreement:** NOT RUN / NOT ESTABLISHED by this artifact.
- **Event-level trigger semantics, run-dependent path interpretation, valid efficiency denominator, prescales/luminosity, full-record coverage:** NOT ESTABLISHED.
- **Confirmatory Monte Carlo, discovery, novelty, publication readiness:** remain on hold.

This correction is deliberately narrow: it does not invalidate the successful schema audit. It prevents a schema-only workflow success from being mistaken for a spectrum-comparison result.
