# Real-Data Baseline Run Card

**Status:** Operational checklist; no real-data reproduction is claimed by this document.

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
