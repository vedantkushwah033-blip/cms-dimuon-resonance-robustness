# Real-Data Baseline Run Card

**Status (2026-10-27):** Operational checklist; no real-data spectrum reproduction is claimed. The schema-only audit of one official Run2012B and one Run2012C DoubleMuParked ROOT file is complete; the event-limited mass-spectrum analysis and quantitative reference comparison remain pending.

## Purpose

Record one reproducible attempt to run the baseline spectrum pipeline on a specifically identified CMS ROOT file. A successful command is not, by itself, evidence that the physics selection matches a published analysis.

## Before running

- [ ] Cite the exact CERN Open Data record and the exact downloadable file.
- [ ] Record the record's data-taking period, dataset type, processing format, and documented limitations.
- [ ] Confirm permission/access and download the file from the official record.
- [ ] Record local filename, byte size, and SHA-256.
- [ ] Inspect the ROOT tree name and branch types using the schema-inspection script.
- [ ] Confirm that required branches have the expected meanings and units.
- [ ] Confirm the reference analysis' exact event selection, object selection, trigger requirements, mass range, and histogram convention. Do not infer undocumented requirements.
- [ ] Pin the Python environment and package versions.
- [ ] Start with a small event-limited smoke test.

## Example commands

Run from the repository root in an environment where the project and dependencies are installed.

```bash
python scripts/inspect_root_schema.py --help
python scripts/reproduce_dimuon_spectrum.py --help
```

After reading each script's actual CLI help, run the schema inspector against the downloaded local file. Then run a small baseline test with the explicit tree name and an event limit. Do not copy a guessed URL or tree name into a final analysis.

For a full run, remove the event limit only after the smoke test succeeds. Add `--sha256-input` to record the input checksum. Preserve the complete stdout, metadata JSON, histogram CSV, plot, exact command, environment lock/export, and commit SHA.

## Required run record

| Field | Value to record |
|---|---|
| CERN record DOI/ID | |
| Exact file name and official download reference | |
| File size in bytes | |
| SHA-256 | |
| ROOT tree and entry count | |
| Schema inspection report | |
| Git commit SHA | |
| Python version and dependency versions | |
| Exact command line | |
| Selection definition and source | |
| Number of events read | |
| Number of events selected | |
| Opposite-charge pairs | |
| Non-finite masses | |
| Below-range / in-range / above-range counts | |
| Histogram binning and range | |
| Runtime and exit status | |
| Output artifact checksums | |
| Deviations from reference analysis | |

## Numerical and selection checks

1. Confirm event and pair counts are internally consistent. The current script's pair accounting should reconcile as below-range + in-range + above-range + non-finite = total opposite-charge pairs.
2. Inspect the first few events independently and manually calculate pair invariant masses from their four-vectors.
3. Check that the event-level multiplicity selection is exactly the intended reference selection; distinguish selected events from events that actually contain an opposite-charge pair.
4. Verify histogram edge conventions and the binning convention against the reference implementation. A log-scaled plot axis does not imply logarithmically spaced bins.
5. Compare the same mass range and the same selection to a reference output. If only a plot is available, treat visual comparison as preliminary and document digitization/normalization uncertainty.
6. Investigate discrepancies before changing the selection. Log each change and rerun all relevant checks.
7. Do not interpret any peak or localized structure as new physics without a separately specified statistical procedure and appropriate calibration.

## Pass criteria

The baseline is considered reproduced only when:
- The exact input and environment are identifiable;
- The event selection and histogram convention match the reference or every difference is explicitly justified;
- Counts and numerical spot checks pass;
- A quantitative comparison is documented;
- An independent reviewer can rerun the procedure from the recorded instructions.

## Failure criteria

Mark the attempt **inconclusive**, not successful, if the required branches or metadata are absent, the reference selection cannot be reconstructed, unexplained discrepancies remain, or the output cannot be reproduced. Do not silently substitute a different data record.

## Scientific boundary

This run card concerns spectrum reconstruction. It does not establish trigger efficiency, trigger prescale correction, signal significance, a discovery, or novelty of the proposed statistical method. Those require separate methods and evidence.


## Bounded official-file schema smoke test

The following uses the official CERN Open Data client to download **one ROOT file per record**, verify the portal checksum when available, and create a schema report. It is not a full-data run and does not establish trigger efficiency.

Install the client:

```bash
python -m pip install cernopendata-client
```

Run from the repository root in Bash:

```bash
set -euo pipefail
mkdir -p outputs/real_data_schema
printf "record_id\tfilename\tbytes\tsha256\n" > outputs/real_data_schema/manifest.tsv

for record_id in 31123 31129 31127 31133; do
  cernopendata-client download-files \
    --recid "$record_id" \
    --filter-regexp '\.root$' \
    --filter-range 1-1 \
    --server https://opendata.cern.ch \
    --verify

  input_file="$(find "$record_id" -type f -name '*.root' -print -quit)"
  test -n "$input_file"
  python scripts/inspect_root_schema.py \
    --input "$input_file" \
    --output "outputs/real_data_schema/schema_${record_id}.json"

  bytes="$(stat -c '%s' "$input_file")"
  sha256="$(sha256sum "$input_file" | awk '{print $1}')"
  printf "%s\t%s\t%s\t%s\n" "$record_id" "$input_file" "$bytes" "$sha256" \
    >> outputs/real_data_schema/manifest.tsv
done
```

Record mapping: 31123 = Run2012B DoubleMuParked; 31129 = Run2012C DoubleMuParked; 31127 = Run2012B SingleMu; 31133 = Run2012C SingleMu. The SingleMu records are optional candidates for denominator feasibility, not automatically unbiased samples. Keep the reports and manifest with the exact Git commit and environment version.

If download or checksum verification fails, preserve the complete error output and mark the audit **inconclusive**; do not silently switch records or use a different file.


## Audit status update — 2026-10-27

The workflow `research-level CMS ROOT schema audit` completed successfully for record 31123 (Run2012B DoubleMuParked) and record 31129 (Run2012C DoubleMuParked). Exact filenames, byte sizes, SHA-256 hashes, `Events` tree entry counts, relevant branch types, and limitations are recorded in `docs/exact_file_schema_audit_run2012b_c_2026-10-27.md`; the machine-readable JSON reports and manifest are attached to [workflow run 40403830670](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40403830670). This audit did **not** run the dimuon spectrum script on these research-level files. The optional SingleMu records 31127 and 31133 have not been downloaded by this workflow.


## Revised bounded parity workflow — 2026-10-27

The manual workflow `.github/workflows/research-level-schema-audit.yml` has since been extended beyond the successful schema-only run described above. When manually dispatched, it will download one checksum-verified file from each record (31123 and 31129), run both the candidate Uproot/NumPy implementation and the independent ROOT/RDataFrame implementation on the same first 100,000 entries, and compare all 30,000 histogram bins using `scripts/compare_histograms.py`. The workflow retains per-period comparison reports and uploads artifacts even if a parity check fails.

**This revised workflow has not been executed as of this entry.** Run 40403830670 is evidence for the earlier schema audit only; it is not evidence for the new baseline or parity steps. Do not state that numerical parity passed until the revised workflow has run and its output CSVs, metadata, comparison JSON, and logs have been inspected. The workflow file is currently on the research branch and is not yet available for manual dispatch from the Actions UI because it has not been added to the default branch.


## Important dispatch prerequisite (2026-10-27)

The revised workflow is currently present on the research branch, while PR #1 remains a draft and unmerged. GitHub's official documentation states that a `workflow_dispatch` workflow must exist on the default branch before it can be manually triggered from the Actions UI. Therefore, do not assume that opening Actions while viewing this branch will expose a working “Run workflow” button. The workflow must first be deliberately made available on the default branch, then dispatched against the reviewed research branch, or the bounded commands must be run in a separate environment with CERN Open Data access. See [GitHub's manual workflow guidance](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).

No research-level spectrum or parity output is available yet. The successful run 40403830670 covers the earlier schema-only workflow and must not be presented as evidence that this revised workflow executed.
