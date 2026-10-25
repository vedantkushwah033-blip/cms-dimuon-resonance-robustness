# CMS Dimuon Resonance Robustness

A reproducible statistical-calibration study of dimuon resonance-search procedures using CMS Open Data where feasible, alongside explicitly labelled model-generated pseudoexperiments and controlled stress tests.

> **Status (2026-10-25): research design and software scaffold only.** This repository has not yet processed a CMS collision dataset, reproduced an official spectrum, run the proposed pseudoexperiment study, or established a novel finding. No scientific result or publication claim is made.

## Research objective
The provisional objective is to estimate how a specified local resonance-search test's false-positive rate behaves under well-defined background-only and prespecified misspecification scenarios, with uncertainty quantified and evaluation scenarios held out from development. This is not a particle-discovery claim.

## Why the question needs care
Prior CMS Open Data work already studies dimuon resonance searches, local background fitting, fit-window choices, and spurious correlated structures. A simple comparison of polynomial orders or windows is not sufficient by itself to establish novelty. See `literature_review.md` before treating the question as a research gap.

## Repository map
- `research_question.md` — provisional question, estimand, and scope guardrails.
- `literature_review.md` — starter bibliography and known limitations.
- `analysis_plan.md` — staged study protocol and reporting requirements.
- `data_sources.md` — candidate official sources and provenance rules.
- `docs/data_requirements.md` — data, trigger, simulation, and stop-condition checklist.
- `docs/milestones.md` — effort-based roadmap and acceptance gates.
- `configs/monte_carlo_plan.yaml` — explicitly provisional simulation-count plan.
- `src/cms_dimuon_robustness/monte_carlo.py` — exact binomial intervals and run-planning utility; not a resonance fitter.
- `tests/` — automated tests.

## Setup

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
ruff check src tests
```

## Data policy
Do not download large samples until the exact dataset, schema, trigger, selection, and reference analysis are verified. The candidate 2012 dimuon spectrum is documented by CERN Open Data at https://opendata.cern.ch/record/cms-12342 (DOI: 10.7483/OPENDATA.CMS.AAR1.4NZQ). Its record explicitly notes that a structure near 30 GeV is trigger-related, not a resonance. The candidate is not yet finalized.

## Monte Carlo precision
The configuration starts with 20 pseudoexperiments per scenario for smoke tests, 500 for a runtime/fit-failure pilot, and a possible 10,000-run main study. These are planning counts only; freeze the protocol after the pilot and justify final counts by the desired interval width. A 10,000-run study cannot empirically validate a five-sigma tail.

## Reproducibility commitments
- Record input record IDs/DOIs, file names and checksums where possible, software versions, selections, seeds, and run metadata.
- Separate observed collision data, simulated detector data, model-generated pseudoexperiments, and artificial stress tests.
- Report attempted/valid trials, failures, uncertainty intervals, and negative findings.
- Do not claim global significance without a defined scan and validated distribution of the maximum test statistic.
- Do not report a discovery, calibrated result, or publication until the corresponding analysis and independent checks are actually complete.

## Important sources
- CERN Open Data dimuon spectrum: https://opendata.cern.ch/record/cms-12342
- CMS Open Data research guide: https://opendata.cern.ch/docs/cms-guide-for-research
- Cesarotti et al., *Phys. Rev. D* 100, 015021 (2019): https://doi.org/10.1103/PhysRevD.100.015021
