# Research status ledger

**Last updated:** 2026-10-28

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
- Updated the baseline spectrum script to use the helper and record the histogram interval convention in run metadata.
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
- Web-checked official Run2012B/Run2012C research-level records and identified documented HLT decision bits. A later exact-file schema audit confirmed branch presence/types in one sampled DoubleMuParked ROOT file per period; event-level path semantics, denominator, prescales, and luminosity checks remain pending.
- Added a dataset feasibility memo distinguishing the 2019 muon-only outreach file, the separate 2021 Run2012C reduced outreach file, and the research-level derived records.
- The schema inspector now reports presence/absence for muon kinematics, charge, event identifiers, and candidate quality/isolation fields, while retaining a heuristic list of trigger-related names.

## Statistical calibration prototype status — 2026-10-28
- Implemented a fixed-order log-polynomial Poisson background fit, descriptive Pearson/deviance residual summaries, and a one-sided Poisson excess scan over declared contiguous windows. These are research prototypes, not an official CMS implementation.
- Implemented fixed-background and refitted-background toy generators, plus-one empirical upper-tail rank p-values, and a held-out rejection-fraction evaluator with Wilson score intervals and p-value-resolution reporting.
- Added deterministic tests for calibration, invalid inputs, scan behavior, background fitting, residual diagnostics, and component integration. Test workflow `40731730895` completed successfully for Python 3.10, 3.11 and 3.12, including pytest, compileall and Ruff; ROOT integration workflow `40731730860` also completed successfully, including the synthetic exporter test. These workflows predate the new null-generator module/tests and do not validate those latest changes.
- Important statistical distinction: a fixed supplied null-generating mean vector with per-toy refitting evaluates one specified toy design. It does not automatically give a valid composite-null parametric bootstrap, nuisance-uniform type-I control, or robustness to model misspecification.
- Added `docs/refitted_background_null_calibration_protocol_draft_2026-10-28.md` and `docs/prespecified_null_scenario_design_proposal_2026-10-28.md`. The latter proposes a matched baseline and smooth/local misspecification scenarios, separates development/pilot/calibration/evaluation roles, and documents stop/go gates. It is a proposal with unresolved numerical choices, not preregistered and not run.
- Current decision remains **NO-GO for confirmatory simulation** until numerical scenario parameters, binning, scan windows, fit-failure handling and precision targets are frozen and independently reviewed. No confirmatory simulation, real-data validation, CMS parity claim, discovery p-value or physics conclusion is asserted.
- PR #6 remains unmerged; no merge has been performed.


## Explicit synthetic null mean generators — 2026-10-28
- Added `src/cms_dimuon_robustness/null_scenarios.py` with two deterministic expected-mean builders: an exponential polynomial (matched-family baseline) and an additive Gaussian-shaped shoulder (deliberate local misspecification candidate). Coordinate convention matches the current fitter's `linspace(-1, 1, n_bins)` implementation.
- Added tests for the analytic definition, symmetry of a quadratic shape, shoulder amplitude/centering, zero-amplitude invariance, and invalid inputs including non-finite/overflow/underflow coefficients and invalid width/amplitude values.
- Added `docs/synthetic_null_generators_2026-10-28.md` describing their equations and emphasizing that they are mathematical toys, not CMS background models. These utilities do not run simulations or select confirmatory parameter values.
- Commits: `a586fb3ee0c52a4fc9067286ac1f8f98a211b7aa` (generator), `ff833fb83998043fb9bdf63be8374b7eaf22b97f` (initial tests), `1ecfd9058135ccfaaa0f52b3bd58825c14b726f3` (documentation), `ec88078f36ea7f1024c0dc8c034399c947363249` (expanded edge-case tests).
- **Latest code changes are not yet CI-verified.** Wait for the workflow triggered by the latest commit and inspect its final conclusions before claiming the new module passes. Confirmatory simulation remains NO-GO pending independent review and frozen scenario values.


## Scenario-level calibration orchestration — 2026-10-28
- Added `src/cms_dimuon_robustness/scenario_evaluation.py`, a reusable runner that accepts explicit scenario mean vectors and a common scan design, evaluates each with the held-out refitted-background evaluator, and returns per-scenario summaries plus the design metadata.
- Enforced explicit scenario names, positive finite means, exact scenario/seed-map agreement, distinct calibration/evaluation seeds, and seed uniqueness across all scenario roles. Added unit tests using a mocked evaluator for orchestration and validation failures.
- Added `docs/scenario_evaluation_runner_2026-10-28.md`. The runner does not choose parameters, launch any simulation now, or assert CMS validity. No confirmatory experiment was run.
- Commits: `21be811f400c350bccbbb8d48823cea712316664` (runner), `90c935ad5e0fc113d0756c8013fd99e23bef5cb0` (tests), `0e6f4459be1e96e4c3a60dcd71a4ba04b40ac0db` (documentation).
- Latest workflows for the prior null-generator commit were still in progress at last poll; new scenario-runner changes are also awaiting CI. Do not claim the latest code is verified until the exact latest workflow runs finish.


## CI follow-up — 2026-10-28
- Inspected scenario-runner workflow `40732582407`: pytest and compileall passed on Python 3.11, but Ruff failed because `tests/test_scenario_evaluation.py` imported unused NumPy; Python 3.10/3.12 jobs were cancelled after the matrix stopped on that failure. This is a lint issue, not a failing test assertion.
- Removed the unused import and strengthened orchestration assertions in commit `8fea8256d630bef7f53f866f784dd92c031732fa`. The workflow triggered by this repair must finish before declaring the scenario-runner change CI-green.
- ROOT integration workflow `40732582349` passed, including the synthetic ROOT exporter test. This checks the ROOT pipeline on synthetic data only, not the real CMS dataset or reference-spectrum parity.
- Confirmatory simulation remains **NO-GO**; PR #6 remains unmerged.


## Scenario runner preflight audit — 2026-10-28
- Code review identified that shared scan/sample settings were validated only when each per-scenario evaluator began. This could start some scenario work before a later scenario exposed a shared configuration problem; duplicate scan widths could also be reported in metadata even though the underlying scan deduplicates them.
- Updated `scenario_evaluation.py` to validate all shared settings (positive integer calibration/evaluation counts, finite `0 < alpha < 1`, non-negative integer fit order, fit-coefficient/bin compatibility, and valid scan widths) before invoking any scenario evaluator. It now normalizes duplicate widths consistently and records the actual normalized scan design.
- Added tests for duplicate-width normalization and for invalid shared configurations failing before any evaluator call. Added/updated the scenario-runner documentation.
- Commits: `ce5f0d9241a2676ed02a7d41fb95a2e1e9314a1b` (preflight implementation), `f0084162fbb3045498b2acedc03166fbac29f662` (tests), `33bf73d203c905f8905ad9b3238d7ec1f162d2fa` (documentation).
- The new commits triggered CI; at the time of this update, complete test-matrix and ROOT integration conclusions are not yet available. Do not describe this revision as CI-green until the runs for the exact latest commit finish.
- No Monte Carlo confirmatory study was run, PR #6 remains unmerged, and the scientific decision remains **NO-GO** pending independent review and frozen design choices.
