# Real-data baseline execution guide

**Status:** reproducible run instructions; execution against CMS data is not yet claimed.

## 1. Choose the baseline's purpose

The first baseline is a reproduction of the public 2019 outreach example, not a trigger-efficiency measurement and not the final physics dataset for a trigger-aware study.

- Analysis record: https://opendata.cern.ch/record/12342
- Dataset record: https://opendata.cern.ch/record/12341
- Input filename: `Run2012BC_DoubleMuParked_Muons.root`
- Published file location in the official analysis source:
  `root://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root`
- Dataset record reports 61,540,413 events and one 2.1 GiB file.

The portal warns that this reduced muon-only output was not further validated. Its listed branches do not establish trigger decisions, prescales, or the full event-quality information needed for trigger-efficiency claims.

## 2. Download once and preserve provenance

From an environment with the CMS Open Data XRootD client installed, run:

```bash
xrdcp root://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root ./Run2012BC_DoubleMuParked_Muons.root
sha256sum ./Run2012BC_DoubleMuParked_Muons.root
```

Save the exact output of `sha256sum` with the run artifacts. A checksum identifies the bytes processed; it does not by itself prove provenance, so retain the official record and source URL as well.

## 3. Run a smoke test first

From the repository root, after installing the project and its declared dependencies:

```bash
python -m pip install -e '.[dev]'
python scripts/inspect_root_schema.py \
  --input ./Run2012BC_DoubleMuParked_Muons.root \
  --output outputs/outreach-smoke/schema.json
python scripts/reproduce_dimuon_spectrum.py \
  --input ./Run2012BC_DoubleMuParked_Muons.root \
  --max-events 10000 \
  --sha256-input \
  --output-dir outputs/outreach-smoke
```

The schema inventory is heuristic: branch-name matches are leads, not proof of variable semantics. Inspect the JSON and cite the authoritative record/documentation for each branch interpretation. The spectrum script requires `nMuon` plus the five muon branches documented in its source. Before selection, it checks `nMuon` against the per-event `Muon_pt` collection length and verifies that `Muon_eta`, `Muon_phi`, `Muon_mass`, and `Muon_charge` have matching per-event collection lengths.

Inspect the metadata JSON, histogram CSV, and PNG. Confirm that:
- The input checksum and byte size are present.
- The schema JSON lists the `Events` tree and all required branches, including `nMuon`; each event's `nMuon` value agrees with the `Muon_pt` collection length.
- The event count equals the requested limit, unless a documented input issue prevented it.
- The selected event count matches the selection definition.
- The pair accounting identity holds.
- The histogram interval is recorded as `[mass_min, mass_max)`.
- The outputs are nonempty and readable.

## 4. Run the full baseline only after the smoke test passes

```bash
python scripts/reproduce_dimuon_spectrum.py \
  --input ./Run2012BC_DoubleMuParked_Muons.root \
  --sha256-input \
  --output-dir outputs/outreach-full
```

The checksum option performs an additional full file read. If time is limited, compute the checksum once separately and document that choice, rather than repeatedly hashing a large input.

## 5. Compare like with like

The official outreach Python implementation applies `nMuon == 2`, then opposite charge, then computes the pair mass, using 30,000 bins over 0.25–300 GeV and logarithmic axes. Compare selection definitions, bin edges, under/overflow treatment, and counts—not only the visual appearance of the plot.

Do not compare against cut-flow numbers from a different Run-1 NanoAOD example unless the exact input and selections are shown to be the same. Different records or formats can have different event counts and branch content.

## 6. Keep the conclusion bounded

The official analysis record explicitly warns that the feature near 30 GeV is a trigger/data-taking effect, not a new resonance. Reproducing that feature is not a discovery, nor does a muon-only derived file establish the trigger mechanism quantitatively.

The full run is a software/reference-reproduction milestone only. Trigger-aware inference requires a separate audit of a suitable research-level file, exact trigger semantics, data-quality requirements, and any needed prescale information.


## 7. Produce and compare a numerical reference artifact

The official reference currently documents a plotted histogram and a cut-flow report; a PNG alone is not a valid input to the exact comparator. Before claiming numerical parity, create a reference CSV from the official ROOT implementation (or a separately reviewed ROOT-based exporter) with exactly these columns:

```text
mass_low_GeV,mass_high_GeV,pair_count
```

The repository now includes `scripts/export_reference_dimuon_histogram.py`, which uses PyROOT/RDataFrame, ROOT's `PtEtaPhiMVector`, and `TH1D` to independently export regular-bin counts plus reference metadata. It is deliberately separate from the Uproot/NumPy candidate implementation. The source is pinned to official commit `19a4a64fd58ef66a6ee3cf4f2a469fba61c60a09` (the `dimuonSpectrum.py` revision), and that commit is written into the reference metadata. Run it in a ROOT-enabled environment on the *same local input file*:

```bash
python scripts/export_reference_dimuon_histogram.py \
  --input ./Run2012BC_DoubleMuParked_Muons.root \
  --sha256-input \
  --output-dir outputs/reference
```

The exporter writes `dimuon_mass_histogram.csv` and `reference_metadata.json`; with `--sha256-input`, the metadata includes the input's byte size and SHA-256. Hashing adds one full input-file read. Before indexing muon vectors, it performs a preflight pass to reject any event where `nMuon` disagrees with the `Muon_pt` collection or the muon branches have inconsistent collection lengths; this adds a full event scan but avoids unsafe indexing on malformed data. It records the ROOT version, cut-flow counts, and histogram underflow/overflow. Do not digitize the reference PNG or infer counts from its pixels. The script has been added to the repository but has **not yet been executed** against the CMS file, and the generated CSV must still be independently inspected before it is accepted as the reference artifact.

Once both numerical CSVs exist, run:

```bash
python scripts/compare_histograms.py \
  --reference outputs/reference/dimuon_mass_histogram.csv \
  --candidate outputs/outreach-full/dimuon_mass_histogram.csv \
  --output outputs/comparison/histogram_comparison.json
```

The comparator returns exit code 0 only for exact bin-by-bin count parity, exit code 2 for valid histograms with differing counts, and raises an error for malformed CSVs, invalid counts, or incompatible bin edges. Preserve the JSON report even when parity fails; discrepancies are evidence to investigate, not a reason to silently relax the criterion. This comparator checks regular-bin edges and counts. It does not by itself compare underflow/overflow, event cut-flow, mass values, or trigger semantics, so those must be recorded and assessed separately.


After the histogram comparison, run the metadata/provenance audit:

```bash
python scripts/audit_baseline_metadata.py \
  --reference-metadata outputs/reference/reference_metadata.json \
  --candidate-metadata outputs/outreach-full/run_metadata.json \
  --histogram-report outputs/comparison/histogram_comparison.json \
  --output outputs/comparison/baseline_audit.json
```

This audit requires the reference and candidate metadata to identify the same input by matching SHA-256 and byte size, and checks tree entries, exactly-two-muon event count, binning, regular-bin totals, underflow/overflow, and the comparator's exact-parity result. It exits 0 only when every required check passes; otherwise it exits 2 and preserves a machine-readable list of failed checks. Both scripts must use the same local file and `--sha256-input`; a matching filename is not evidence of matching bytes. A passing audit establishes software-level reproduction evidence only, not trigger or detector validation.

## 8. Reproduction acceptance checklist

Do not mark the baseline reproduced until all of the following are attached to one run record:

- Input URL/record, file byte size, SHA-256, tree name, entry count, and software versions.
- Schema inventory and evidence that the required branches have the expected semantics.
- Candidate metadata, CSV, and plot from the full run.
- Reference CSV produced by a documented ROOT-based method, plus ROOT version and source revision.
- Reference and candidate cut-flow counts and explicit underflow/overflow accounting.
- Machine-readable comparison JSON and an explanation for every discrepancy; exact parity is the preregistered target.

If any item is unavailable, report the reproduction as incomplete and state which evidence is missing. A successful unit-test or synthetic-ROOT CI run is not a substitute for this checklist.
