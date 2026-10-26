# Research status ledger

**Last updated:** 2026-10-26

## Confirmed completed in this repository
- Audited the official CMS outreach Python source and documented a component-by-component parity checklist in `docs/reference_implementation_audit.md`.
- Tightened opposite-sign selection semantics: the NanoAOD pair function now rejects charge values outside {-1,+1}, because `q1*q2 < 0` matches the reference's charge-inequality test only under that domain assumption.
- Added a test that malformed charge values raise an explicit error.
- The cross-implementation test comparing the Awkward and vectorized four-vector implementations completed successfully across configured Python versions.
- Added cross-implementation validation comparing the Awkward-array pair-mass path against the standalone vectorized four-vector function on 100 deterministic random two-muon events.
- Verified via GitHub Actions that the numerical-stability fix, pair-accounting invariant, and analytic/invalid-input tests completed successfully across the configured Python versions.
- Added a runtime invariant to the baseline spectrum script that raises an error if below-range, in-range, upper-edge/overflow, and non-finite pair counts do not sum to the total opposite-charge pair count.
- Removed a duplicate JSON metadata key for `pairs_at_or_above_mass_max`.
- Updated the standalone vectorized invariant-mass helper to clamp only round-off-scale negative mass-squared values; substantially negative results now remain invalid (`NaN`) rather than silently becoming zero.
- Refined the spectrum metadata field to `pairs_at_or_above_mass_max`, accurately describing the upper-edge overflow convention.
- Expanded the end-to-end spectrum smoke test so a synthetic two-muon event has a mass exactly at the configured upper edge; the test checks that it is excluded from the in-range histogram and included in the overflow accounting.
- Corrected the schema/run guide's shell line continuations and retained the actual schema inventory invocation.
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

- Follow-up numerical audit: both invariant-mass implementations now require the mass-squared value and its scale to be finite before treating a negative result as round-off. This prevents an infinite tolerance from making a non-finite negative result eligible for clamping. Commits: `b0472a4` (Awkward/NanoAOD path) and `05de35b` (standalone vectorized path). These source changes have been committed; their new CI status has not yet been verified.

- Added a defensive schema-integrity check in `opposite_charge_pair_masses`: required muon fields must exist and per-event multiplicities must match across kinematic and charge branches. Added a regression test with deliberately inconsistent jagged lengths. Commits: `3047bb4` and `8a58ba6`; their CI results are not yet verified.
- Follow-up audit of recent numerical-fix commits found no combined status checks exposed by the connector at the time checked; treat CI for `b0472a4` and `05de35b` as unverified, not passed.

## Workflow status checked 2026-10-26
- GitHub Actions run for commit `3ed0f9e` (decision gates): completed successfully.
- GitHub Actions run for commit `40b819d` (scenario matrix): completed successfully.
- GitHub Actions run for commit `1a40e06` (Monte Carlo precision planning): was still in progress at the last check; do not report it as passing until completed.

## Latest workflow status for histogram changes
- Cross-implementation test commit `1b5c488` completed successfully.
- Charge-domain validation (`2531a59`), malformed-charge test (`ffd7081`), assertion cleanup (`355158f`), and reference audit note (`9337e58`) had pending/queued CI at the last check; do not treat these latest changes as validated yet.
- The latest completed runs for commits `5d3ac5a`, `462e2af`, `208e264`, and `2085ec4` all succeeded.
- Cross-implementation test commit `1b5c488` was queued on Python 3.10, 3.11, and 3.12 at the last check; its result is pending.
- The end-to-end upper-edge fixture commit `0921ce3` and status-ledger commit `60d8237` both completed successfully in GitHub Actions.
- The pair-accounting invariant/metadata cleanup commit `5d3ac5a` was still running on Python 3.10 and 3.12, with Python 3.11 queued, at the last check.
- The direct invariant-mass stability change `462e2af` has just been committed; its CI result has not yet been verified.
- Run `f0916b1` failed because the spectrum integration test still expected the old metadata field name after the rename. The test was updated in `68fa674`, whose workflow completed successfully.
- Run `fdc98d6` added the first end-to-end upper-edge fixture; its workflow status was still in progress at the last check. Commit `0921ce3` corrected the fixture's eta values so the generated pair is exactly at the mass upper edge; its workflow is also still in progress at the last check.
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

## Latest validation update — 2026-10-26

- The schema-integrity guard and its malformed-event regression test are included in commit `8a58ba6b5bcb0ef6efd06a6d2c1f36f283bc0cd7`; the research-status ledger update is commit `63f840b6d3dabdcc5dabd3ac937e8a6e41f9c8fb`.
- GitHub Actions run [40254596371](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40254596371), triggered by the status-ledger commit, completed successfully. The Python 3.10, 3.11, and 3.12 jobs each passed dependency installation, `pytest`, and `ruff check src tests`. This validates the committed software/test suite on those runtimes; it does **not** validate a real CMS input file or establish physics-level correctness.
- **Still pending:** execute the documented workflow on the exact official ROOT file; preserve its official record, file URL, SHA-256, size, tree entry count, and branch inventory; inspect schema/units; compare the full baseline quantitatively against the public reference; and report discrepancies before proceeding to confirmatory statistical experiments.
- Interpretation guardrail remains unchanged: the muon-only outreach record is suitable for an educational baseline reproduction, not by itself for quantitative trigger-efficiency or prescale claims.

## Latest validation update — 2026-10-26 (verified against GitHub Actions)

- The schema-integrity change and its regression test are now validated by completed CI runs, not merely pending: run [40254583966](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40254583966) for commit `3047bb4` and run [40254587555](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40254587555) for commit `8a58ba6` both completed successfully.
- The follow-up diagnostic improvement reports the first mismatching event index and the observed multiplicities. Its CI run [40254895982](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40254895982) completed successfully for commit `301c460`; the dedicated regression test verifies the event index and counts.
- The latest branch-head run [40254903962](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40254903962), for commit `9eb16ab6e546e9acf60fbf1b06351a01f6c2eab3`, completed successfully on Python 3.10, 3.11, and 3.12. Each job completed dependency installation, `pytest`, and `ruff check src tests`.
- The research-status documentation commit `453aed4` also passed its workflow: [run 40254776537](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40254776537).
- These results validate the software test/lint suite for the tested commits. They do **not** validate the real CMS ROOT input, prove full parity with the official analysis, establish trigger semantics, or constitute evidence for a resonance claim. The real-data smoke test/full run and quantitative reference comparison remain outstanding.
