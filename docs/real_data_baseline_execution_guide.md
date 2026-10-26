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
python scripts/inspect_root_schema.py --help
python scripts/reproduce_dimuon_spectrum.py \
  --input ./Run2012BC_DoubleMuParked_Muons.root \
  --max-events 10000 \
  --sha256-input \
  --output-dir outputs/outreach-smoke
```

If the schema-inspector CLI does not expose `--help` or uses different required arguments, consult `python scripts/inspect_root_schema.py --help` and record the actual command used; do not infer schema from a failed invocation. The spectrum script requires the five muon branches documented in its own source.

Inspect the metadata JSON, histogram CSV, and PNG. Confirm that:
- The input checksum and byte size are present.
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
