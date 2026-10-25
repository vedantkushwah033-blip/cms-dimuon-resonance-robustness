# Research status ledger

**Last updated:** 2026-10-25

## Confirmed completed in this repository
- Initial research question and scope guardrails documented.
- Starter bibliography identifies a close prior CMS Open Data dimuon resonance analysis.
- Provisional data source and provenance checklist documented.
- Monte Carlo planning template added.
- Exact Clopper-Pearson interval utility and unit tests added.
- Vectorized invariant-mass utility, Awkward-array pair-mass helper, and chunked baseline reconstruction script added.
- Unit tests for analytic kinematic cases and synthetic jagged muon arrays added; one incorrect analytic test expectation was corrected during development.
- Python packaging and GitHub Actions test workflow added.
- Novelty gate, literature matrix, experiment-protocol template, data-source assessment, milestones, quality gates, and independent-review plan added.

## Not yet completed
- Exhaustive or systematic literature review.
- Confirmation that the candidate research contribution is novel.
- Download/inspection of the full 2.1 GiB reduced event dataset.
- Execution of the baseline script against the official ROOT file and comparison with the reference spectrum.
- Baseline reproduction against the official reference plot.
- Schema validation and event-level invariant-mass cross-check.
- Selection/trigger feasibility analysis.
- Implementation of a resonance likelihood or bump-hunt test statistic.
- Main pseudoexperiments, held-out stress tests, or empirical results.
- Independent external technical review.
- Manuscript submission or publication.

## Evidence policy
A planned task is not a result. A passing CI run validates the current automated software checks, not the scientific hypothesis. The baseline script has only been exercised on a tiny synthetic ROOT file; it has not yet been run against the official CMS event file. A passing CI workflow would validate only the checks that actually ran. A repository commit is not evidence of novelty, peer review, or admissions impact.
