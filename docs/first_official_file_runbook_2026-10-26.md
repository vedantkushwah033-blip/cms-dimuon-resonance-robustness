# First official-file runbook: CMS dimuon baseline

**Date:** 2026-10-26  
**Status:** executable plan; commands have not been run by this repository in this update.  
**Purpose:** move from synthetic-file tests to a real-file smoke test without confusing a software check with a physics result.

## Dataset choice: keep the stages separate

### Stage 1 — outreach example, software validation only

CERN's public dimuon analysis record identifies the derived file below and provides its official download command. The record says the reduced output was not further validated, so use it first to test file access and reproduce the public educational example—not as validated input for a trigger-efficiency or new-physics claim.

Official record: https://opendata.cern.ch/record/12341  
Reference analysis: https://opendata.cern.ch/record/12342

Known public XRootD path from the official analysis record:

```text
root://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root
```

This path is remote; it is not a local file and must not be passed to the script's local-only SHA-256 option.

### Stage 2 — research-level Run2012B/C files, scientific feasibility check

After Stage 1 works, inspect the exact file(s) from the separate research-level records:
- Run2012B: https://opendata.cern.ch/record/cms-31123
- Run2012C: https://opendata.cern.ch/record/cms-31129

Do not assume the research-level files share the outreach file's branches or selection semantics. Download one exact file from each record, preserve its official URL and checksum if provided, and inspect it independently. A schema containing HLT bits is not by itself a trigger-efficiency or prescale model.

## Reproducible commands

The repository includes `.github/workflows/official-data-smoke-test.yml`. On `research-plan/initial-protocol`, it now runs on scoped pushes affecting the workflow, dependency manifest, inspection/reconstruction scripts, or analysis source; this allows a bounded test before the PR is merged. It also supports manual dispatch after the workflow reaches the default branch. The job is bounded to 30 minutes, hard-capped at 10,000 events (not merely defaulted to that value), and uploads diagnostic outputs for 14 days. A workflow definition is not execution evidence: inspect the actual run and artifact before calling the smoke test successful.


Run from the repository root in an environment with dependencies installed using `python -m pip install -e ".[dev,remote]"`. The `remote` extra installs Uproot optional XRootD bindings; the ordinary test/development install does not include this remote-access dependency.

Set the public reference URL:

```bash
export CMS_DIMUON_OUTREACH_URL='root://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root'
```

1. **Inspect the actual remote file schema** (not just the web-page variable list):

```bash
python scripts/inspect_root_schema.py \
  --input "$CMS_DIMUON_OUTREACH_URL" \
  --output outputs/schema_outreach_2012.json
```

Check the report before running the spectrum script. Confirm the tree name, event count, required branches (`nMuon`, `Muon_pt`, `Muon_eta`, `Muon_phi`, `Muon_mass`, `Muon_charge`) and types. If a required branch is missing, stop and record the mismatch; do not silently adapt the script to another schema.

2. **Run a bounded smoke test** (only checks file access and pipeline execution):

```bash
python scripts/reproduce_dimuon_spectrum.py \
  --input "$CMS_DIMUON_OUTREACH_URL" \
  --max-events 10000 \
  --output-dir outputs/outreach_smoke
```

Inspect the JSON metadata, CSV histogram and plot. A successful smoke test is not full-data parity and does not validate trigger modelling.

3. **Run the complete outreach reference sample only after the smoke test passes**:

```bash
python scripts/reproduce_dimuon_spectrum.py \
  --input "$CMS_DIMUON_OUTREACH_URL" \
  --output-dir outputs/outreach_full
```

Do not use `--max-events` for the full-data result. Preserve the generated metadata and record the exact command, commit SHA, package versions, event counts and output checksums.

4. **Inspect research-level files separately** (replace each placeholder with a locally downloaded exact file path from the corresponding official record):

```bash
python scripts/inspect_root_schema.py \
  --input data/Run2012B_exact_file.root \
  --output outputs/schema_run2012B.json

python scripts/inspect_root_schema.py \
  --input data/Run2012C_exact_file.root \
  --output outputs/schema_run2012C.json
```

The placeholder paths are examples, not existing files. Keep data files and generated outputs out of version control unless the repository's data policy explicitly permits them.

## Acceptance gates

### Gate 1 — file opens and schema is understood
- The remote/local file opens reproducibly.
- The tree and required branches are present with expected types.
- Jagged muon collections are consistent with the scalar muon multiplicity.
- Event and pair accounting invariants hold.
- The output records source, tree entries, events read, selection mode and software/commit metadata.

### Gate 2 — baseline matches the published example
- Run the full relevant outreach sample.
- Match selection, mass range, binning and histogram edge conventions.
- Compare the candidate histogram to a reference output from the official analysis using explicit bin-by-bin metrics, not visual similarity alone.
- Explain and document any discrepancy before calling it a reproduction.

### Gate 3 — research-level scientific suitability
- Audit Run2012B and Run2012C independently.
- Establish exact branch meanings, run coverage, selection and trigger-path definitions.
- Verify whether prescales, event-quality requirements and other needed metadata exist or can be sourced with defensible provenance.
- Only then decide whether trigger-aware inference is possible.

## Stop conditions

Stop and report the blocker if network access fails, the expected file/tree/branches are absent, the script fails a validation gate, the official reference output cannot be obtained for comparison, or the source's selection cannot be reconstructed. Do not replace a failed check with a synthetic result and label it real-data validation.

## Reporting template

Record one of these statuses for every stage:
- **NOT RUN** — no execution evidence.
- **BLOCKED** — attempted but a documented dependency/access/data issue prevented completion.
- **PASS** — command completed and every stated acceptance check passed.
- **FAIL** — command completed but at least one check failed.

Report the exact command and commit for any PASS/FAIL. Do not report a task as passed merely because its instructions were written.
