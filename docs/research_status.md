# Research status ledger

**Last updated:** 2026-10-26

## Confirmed completed in this repository
- Added a staged real-data baseline execution guide covering official input identification, schema inventory, a limited smoke test, provenance capture, full-run conditions, reference-comparison requirements, and interpretation limits.
- Refined run metadata to call the upper-edge count `pairs_at_or_above_mass_max`, avoiding the ambiguous label `pairs_above_mass_range` for the half-open histogram interval.
- Updated the spectrum integration test to verify the renamed accounting field and explicit histogram interval metadata.
- Added `docs/real_data_baseline_execution_guide.md` with source-record distinctions, a staged smoke/full-run procedure, provenance requirements, and bounded interpretation; the guide explicitly does not claim a real-data run has occurred.
- Added the ROOT schema inventory invocation and JSON output path to the run guide so the schema is actually inspected rather than merely showing the CLI help.
- Added a shared mass-histogram helper with explicit half-open `[mass_min, mass_max)` semantics, separate non-finite accounting, and a count-conservation invariant.
- Added unit tests for empty inputs, invalid configurations, non-finite values, and the upper-edge overflow case; corrected a test's expected bin counts after checking the exact bin edges.
- Updated the baseline spectrum script to use the helper and record the histogram interval convention in run metadata.
- Documented the ROOT-versus-NumPy upper-edge discrepancy and its correction in `docs/reference_baseline_comparison.md`.
- Added `docs/scenario_matrix_template.csv` to distinguish development, pilot, held-out null-misspecification, and optional signal-injection scenarios; unresolved design choices remain explicitly marked for definition.
- Added `docs/next_experiment_decision.md` with stop/go gates and criteria for narrowing claims when provenance, reference agreement, novelty, or validation fails.
- Added `docs/monte_carlo_precision_planning.md` with illustrative binomial precision calculations and explicit limits on what 10,000 null trials can establish.
- Initial research question and scope guardrails documented.
- Starter bibliography identifies a close prior CMS Open Data dimuon resonance analysis.
- Provisional data source and provenance checklist documented.
- Monte Carlo planning template added.
- Exact Clopper-Pearson interval utility and unit tests added.
- Vectorized invariant-mass utility, Awkward-array pair-mass helper, and chunked baseline reconstruction script added.
- Unit tests for analytic kinematic cases and synthetic jagged muon arrays added; one incorrect analytic test expectation was corrected during development.
- Python packaging and GitHub Actions test workflow added.
- Novelty gate, literature matrix, experiment-protocol template, data-source assessment, milestones, quality gates, and independent-review plan added.
- Added a ROOT schema inventory tool with candidate branch-group coverage and a synthetic-file integration test.
- Compared the public reference implementation and aligned the baseline script's default selection, binning, mass range, and log axes; numerical reproduction remains pending.
- Added a method-by-method novelty comparison against Williams (2017), Cesarotti et al. (2019), and foundational look-elsewhere/likelihood references.
- Added an end-to-end smoke test for the spectrum CLI, verifying `--max-events`, pair counts, metadata, CSV output, and plot creation on synthetic ROOT data.
- Added optional local-input SHA-256 and provenance metadata (file size, tree entry count, selected branch types, Python/package versions).
- Improved numerical stability handling: only tiny round-off-scale negative invariant-mass-squared values are clamped; non-finite kinematics remain non-finite and are counted instead of silently becoming zero-mass pairs. The end-to-end CLI test now verifies this behavior using a synthetic ROOT event.
- Web-checked official Run2012B/Run2012C research-level records and identified documented HLT decision bits in the Run2012C variable list; actual file-level branch and prescale checks remain pending.
- Added a dataset feasibility memo distinguishing the 2019 muon-only outreach file, the separate 2021 Run2012C reduced outreach file, and the research-level derived records.
- The schema inspector now reports presence/absence for muon kinematics, charge, event identifiers, and candidate quality/isolation fields, while retaining a heuristic list of trigger-related names.

## Workflow status checked 2026-10-26
- GitHub Actions run for commit `3ed0f9e` (decision gates): completed successfully.
- GitHub Actions run for commit `40b819d` (scenario matrix): completed successfully.
- GitHub Actions run for commit `1a40e06` (Monte Carlo precision planning): was still in progress at the last check; do not report it as passing until completed.

## Latest workflow status for histogram changes
- Follow-up commits `f0916b1`, `68fa674`, and `3b149d1` update overflow metadata, its integration test, and shell line continuations in the baseline guide. Their CI results have not yet been checked here.
- The initial test commit `cc02702` failed because the test's expected bin counts were incorrect for its declared bin edges; the expectation was corrected in `370bf7e`.
- The corrected test commit `370bf7e`, histogram script integration `3e474db`, metadata update `3e685ae`, and histogram audit documentation `ca67b79` have successful GitHub Actions runs.
- The most recent guide commits were queued/in progress at the last status check; their workflows are not yet verified.

## Not yet completed
- Exhaustive or systematic literature review.
- Confirmation that the candidate research contribution is novel.
- Direct file-level inspection of the Run2012B/Run2012C research-level ntuples and verification of HLT/prescale branches.
- Download/inspection of the full 2.1 GiB outreach reduced event dataset (not a priority for physics claims).
- Execution of the baseline script against the official ROOT file and comparison with the reference spectrum.
- Baseline reproduction against the official reference plot.
- Schema validation and event-level invariant-mass cross-check.
- Selection/trigger feasibility analysis.
- Implementation of a resonance likelihood or bump-hunt test statistic.
- Main pseudoexperiments, held-out stress tests, or empirical results.
- Independent external technical review.
- Manuscript submission or publication.

## Evidence policy
A planned task is not a result. A passing CI run validates the current automated software checks, not the scientific hypothesis. The baseline script has only been exercised on a tiny synthetic ROOT file; it has not yet been run against the official CMS event file. The schema inspector and independent four-vector test passed in the confirmed CI run recorded in `docs/validation_log.md`. A passing CI workflow would validate only the checks that actually ran. A repository commit is not evidence of novelty, peer review, or admissions impact.
