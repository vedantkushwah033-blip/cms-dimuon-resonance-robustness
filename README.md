# CMS Dimuon Resonance Robustness

A reproducible statistical-calibration study of dimuon resonance-search procedures using CMS Open Data where feasible, alongside explicitly labelled model-generated pseudoexperiments and controlled stress tests.

> **Status (2026-10-25): early research design and baseline-code scaffold.** The repository now contains an initial ROOT/NanoAOD spectrum-reconstruction script and tested mathematical utilities, but the script has not yet been run against the official event file, the reference spectrum has not been reproduced, and no novel finding or publication is claimed.

## Research objective
The candidate objective is to evaluate the false-positive calibration of a clearly specified local dimuon bump-hunt procedure under prespecified background-generating scenarios, including any model-selection step only if the literature audit identifies a defensible gap. The question is provisional. Williams (2017) already studies background-model selection, bias/variance and coverage in bump hunting, so the exact method must be compared before claiming novelty.

## Data records — do not confuse these
- **Analysis example:** Wunsch (2019), DOI 10.7483/OPENDATA.CMS.AAR1.4NZQ, https://opendata.cern.ch/record/cms-12342. The record's two example files total 123.7 KiB; this is not the full event sample. It warns that the feature near 30 GeV is trigger/data-taking related.
- **Reduced event dataset:** Wunsch (2019), DOI 10.7483/OPENDATA.CMS.LVG5.QT81, https://opendata.cern.ch/record/12341. CERN describes a 2.1 GiB file with 61,540,413 events and reduced muon kinematic/charge branches. The record says no further validation was performed on the reduced output.

The reduced sample is a candidate for baseline reconstruction, not proof that all trigger information needed for trigger-misspecification studies is available.

## Repository map
- `research_question.md`, `analysis_plan.md` — provisional question and staged protocol.
- `literature_review.md`, `docs/literature_matrix.csv`, `docs/novelty_gate.md` — closest prior work and originality gate.
- `data_sources.md`, `docs/data_source_assessment.md`, `docs/data_requirements.md` — source provenance and feasibility constraints.
- `docs/experiment_protocol_template.md` — preregistration checklist for the main simulation.
- `docs/independent_review_plan.md`, `docs/quality_gates.md` — validation and external-review requirements.
- `src/cms_dimuon_robustness/invariant_mass.py` — vectorized kinematic calculation.
- `src/cms_dimuon_robustness/nanoaod.py` — Awkward-array opposite-charge pair-mass calculation.
- `scripts/reproduce_dimuon_spectrum.py` — chunked ROOT/NanoAOD baseline reconstruction.
- `src/cms_dimuon_robustness/monte_carlo.py` — exact binomial confidence intervals and a sample-size planning approximation.
- `tests/` — unit and synthetic-ROOT integration tests. GitHub Actions passed 17 tests plus Ruff checks on Python 3.10, 3.11 and 3.12 for commit `e6259abaaae0b9799b00ad125b20b521c00e40a3`.

## Setup
Python 3.10 or newer:

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
ruff check src tests
```

## First baseline run
Start with a limited event smoke test, not a full 61-million-event run:

```bash
python scripts/reproduce_dimuon_spectrum.py --max-events 10000
```

By default the script reads the official reduced NanoAOD ROOT file via XRootD and writes a histogram CSV, metadata JSON and PNG under `outputs/baseline/`. This command is a proposed first run; the repository has not yet confirmed that it succeeds in your environment. Inspect its metadata and compare the spectrum with the official reference before interpreting it. The script pairs all opposite-charge muons and applies no extra trigger or quality cuts, so it is not a complete physics selection.

After the smoke test, inspect the output, verify event-level masses against an independent four-vector calculation, then increase the sample size only after resolving any discrepancies.

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
