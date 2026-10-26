# CMS Dimuon Resonance Robustness

A reproducible statistical-calibration study of dimuon resonance-search procedures using CMS Open Data where feasible, alongside explicitly labelled model-generated pseudoexperiments and controlled stress tests.

> **Status (2026-10-26): early research design and baseline-code scaffold.** A bounded 10,000-entry smoke test has passed against the official CMS outreach ROOT file, including schema inspection and spectrum-output generation. The full 61.5-million-entry file has not been processed, and the official reference spectrum has not been reproduced quantitatively. No novel finding or publication is claimed. The outreach schema contains no trigger-related branch candidates or listed muon quality/isolation candidates, so it is not sufficient for the proposed trigger-aware scientific analysis.

## Research objective
The candidate objective is to evaluate the false-positive calibration of a clearly specified local dimuon bump-hunt procedure under prespecified background-generating scenarios, including any model-selection step only if the literature audit identifies a defensible gap. The question is provisional. Williams (2017) already studies background-model selection, bias/variance and coverage in bump hunting, so the exact method must be compared before claiming novelty.

## Data records — do not confuse these
- **Analysis example:** Wunsch (2019), DOI 10.7483/OPENDATA.CMS.AAR1.4NZQ, https://opendata.cern.ch/record/cms-12342. The record's two example files total 123.7 KiB; this is not the full event sample. It warns that the feature near 30 GeV is trigger/data-taking related.
- **Education/outreach reduced event dataset:** Wunsch (2019), DOI 10.7483/OPENDATA.CMS.LVG5.QT81, https://opendata.cern.ch/record/12341. CERN describes a 2.1 GiB file with 61,540,413 events and reduced muon kinematic/charge branches. The record explicitly says no further validation was performed on the reduced output. It must not be treated as validated physics-measurement input without additional checks.
- **Research-level Run-1 ntuples to assess next:** Run2012B DoubleMuParked, https://opendata.cern.ch/record/cms-31123, and Run2012C DoubleMuParked, https://opendata.cern.ch/record/cms-31129. CERN describes these as research-level NanoAOD-like ntuples processed from AOD using validated runs. Their exact branch schemas and suitability for trigger-aware work must still be inspected; do not assume trigger decisions or prescales are present.

The education/outreach sample remains useful for pipeline development only. The research-level ntuples are stronger candidates for the scientific baseline, subject to schema and selection validation. Official records report 26.1 million Run2012B events and 35.5 million Run2012C events. The Run2012C variable list documents HLT decision bits; exact file-level presence and prescale metadata remain unverified.

## Repository map
- `research_question.md`, `analysis_plan.md` — provisional question and staged protocol.
- `literature_review.md`, `docs/literature_matrix.csv`, `docs/novelty_gate.md` — closest prior work and originality gate.
- `data_sources.md`, `docs/data_source_assessment.md`, `docs/data_requirements.md` — source provenance and feasibility constraints.
- `docs/experiment_protocol_template.md` — preregistration checklist for the main simulation.
- `docs/independent_review_plan.md`, `docs/quality_gates.md` — validation and external-review requirements.
- `src/cms_dimuon_robustness/invariant_mass.py` — vectorized kinematic calculation.
- `src/cms_dimuon_robustness/nanoaod.py` — Awkward-array opposite-charge pair-mass calculation.
- `scripts/reproduce_dimuon_spectrum.py` — chunked ROOT/NanoAOD baseline reconstruction; requires an explicit input path to prevent accidental use of the unvalidated outreach dataset.
- `scripts/inspect_root_schema.py` — inventories trees, entries, branch names, trigger-related candidates, branch types, and presence/absence of candidate branch groups; semantics still require review.
- `tests/test_independent_four_vector.py` — compares vectorized mass calculations with an independently implemented four-vector reference on 250 fixed-seed random cases.
- `tests/test_spectrum_script.py` — runs the baseline command-line script on a synthetic ROOT file and checks event limits, counts, metadata, CSV and plot outputs.
- `tests/test_spectrum_selection_modes.py` — verifies that exactly-two-muon event selection and all-opposite-charge-pairs selection produce distinct, expected event/pair counts on a mixed-multiplicity sample.
- `tests/test_spectrum_input_validation.py` — checks that malformed muon counts, mismatched jagged-branch lengths, missing required branches, invalid charge values, and negative finite muon kinematics fail explicitly.
- `docs/selection_semantics.md` — defines event-level versus pair-level selection and explains the statistical consequences of multiple pairs per event.
- `docs/data_schema_findings.md`, `docs/data_feasibility_decision.md` — separate record-level facts from file-level checks and define trigger-aware, limited-scope, and reproducibility-only routes.
- `docs/reference_baseline_comparison.md` — maps the implementation to the official public example's event selection, binning, mass range, and axes.
- `docs/official_reference_code_audit_2026-10-26.md` — compares the official CMS Open Data v1.4 source code with this implementation; source-level selection and histogram configuration align, but no numerical reproduction is claimed.
- `docs/official_outreach_smoke_test_2026-10-26.md` — records the successful 10,000-entry official-data smoke test, branch-schema limitations, event/pair counts, earlier failed attempts, and next acceptance gate.
- `docs/research_level_schema_feasibility_audit_2026-10-26.md` — reviews official Run2012B/C variable documentation, separating record-level facts from file-level checks and rejecting trigger-efficiency claims until path decisions/prescales are verified.
- `docs/real_data_baseline_run_card.md` — documents provenance and bounded schema-audit commands for one file each from research-level DoubleMuParked and SingleMu records; the documented downloads have not yet been completed by this repository.
- `docs/run1_trigger_feasibility_gate.md` — records the requirements for a valid trigger estimand and why HLT bits alone are insufficient.
- `docs/literature_search_update_2026-10-26.md` — records a focused follow-up search; this is not a systematic review and novelty remains unproven.
- `docs/literature_scope_decision_2026-10-27.md` — records a critical source-screening memo, identifies close prior work, and puts large simulations/novelty claims on hold until a defensible gap and data feasibility are demonstrated.
- `docs/literature_scope_update_2026-10-27.md` — extends the focused literature screening to Bayesian background modelling, background sculpting, and the data-feasibility constraints.
- `docs/first_official_file_runbook_2026-10-26.md` — gives staged commands and acceptance gates for the outreach file and research-level Run2012B/C files.
- `.github/workflows/official-data-smoke-test.yml` — hard-capped 10,000-event remote access/pipeline smoke test with a 30-minute limit and artifact upload; the successful run is linked in the smoke-test report.
- `src/cms_dimuon_robustness/monte_carlo.py` — exact binomial confidence intervals and a sample-size planning approximation.

## Setup
Python 3.10 or newer:

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"  # local tests/development
# For optional CERN root:// remote-file access:
python -m pip install -e ".[dev,remote]"
pytest
ruff check src tests
```

## First baseline run
The official outreach-file smoke test has already succeeded for the first 10,000 entries. Do not treat that bounded pipeline check as a full reference reproduction or a physics validation. To inspect another specific file, first verify its exact source and schema:

```bash
python scripts/inspect_root_schema.py --input /path/to/official-file.root --output outputs/schema_report.json
python scripts/reproduce_dimuon_spectrum.py --input /path/to/selected-file.root --max-events 10000
```

The scripts require an explicit file path or supported ROOT URL. The spectrum script defaults to exactly two reconstructed muons with opposite charge, 30,000 bins over 0.25–300 GeV, and logarithmic x/y axes to align with the public example. The default mode selects events with exactly two muons and then requires opposite charge; an optional all-pairs mode includes multi-muon events and is not reference-parity compatible. Neither mode applies trigger or object-quality cuts, so neither is a complete physics selection. The education/outreach dataset is not considered validated physics input; evaluate the research-level Run-1 ntuples only after exact file provenance and schema have been verified.

After any new-file smoke test, inspect the output, verify event-level masses against an independent four-vector calculation, and compare with a reference before increasing sample size.

## Statistical precision and scientific guardrails
- Smoke tests, pilot runs and main simulations have different purposes; planning counts are not evidence.
- Report rejection counts, denominators, exact binomial intervals, failed fits and all prespecified scenarios.
- Separate observed collision data, detector simulation, model-generated pseudoexperiments and artificial stress tests.
- Do not claim global significance without a defined scan and validated maximum-statistic distribution.
- Do not claim a novel method until the closest methods—especially Williams (2017) and Cesarotti et al. (2019)—have been compared in detail.
- A unit-tested utility does not validate the complete analysis; a passing CI run validates only the checks actually executed.

## Important sources
- CERN Open Data analysis example: https://opendata.cern.ch/record/cms-12342
- CERN Open Data reduced event dataset: https://opendata.cern.ch/record/12341
- Williams (2017), bump-hunting model selection: https://doi.org/10.1088/1748-0221/12/09/P09034
- Cesarotti et al. (2019), CMS Open Data dimuon resonance search: https://doi.org/10.1103/PhysRevD.100.015021
- Gross & Vitells (2010), look-elsewhere effect: https://doi.org/10.1140/epjc/s10052-010-1470-8
