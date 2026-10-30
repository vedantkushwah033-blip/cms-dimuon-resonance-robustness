# Research status ledger

**Last updated:** 2026-10-28

## Confirmed completed in this repository
- Added `empirical_rank_test_resolution` to make the plus-one empirical-rank p-value's discrete rejection grid explicit: minimum p-value, maximum exceedance count compatible with rejection, and unconditional rejection probability under iid continuous null statistics. Added unit tests for grid-aligned and non-grid-aligned alpha values and invalid inputs, and documented the distinction between unconditional rank size and conditional behavior for a fixed calibration sample. Restored the legacy `calibration_minimum_resolvable_pvalue` output key in both fixed-background and refitted-background evaluation results for compatibility. Replaced binary-float threshold multiplication with decimal-string arithmetic in the rank-grid helper and added a regression test for the alpha=0.29, M=99 boundary. Latest source/test commit `c54c85f8dce8558f7fa79008c141fe0d2a53d0c7` passed GitHub Actions tests on Python 3.10, 3.11, and 3.12, and the synthetic ROOT exporter integration workflow passed. These results verify software behavior only; they do not validate the null model or CMS data.

- Added `docs/independent_statistical_design_audit_2026-10-28.md`, a methodological review memo clarifying the estimand, calibration resolution versus precision, conditional interpretation of Wilson intervals, scan freezing, scenario specification, fit-failure policy, misspecification limits, and the separate CMS-data validation gate. It is explicitly not an external review or preregistration.
- The audit document's commit `789ceafc59c1bdd8e462c05869e5cede83880d44` passed GitHub Actions tests on Python 3.10, 3.11, and 3.12, including compilation and Ruff lint, and the independent ROOT exporter integration workflow passed on synthetic data. These are software checks only, not CMS-data validation.
- Confirmatory simulations remain on hold pending fixed numerical scenario choices and independent scientific review.
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

- Added explicit background-fit coefficient-boundary diagnostics in `fit_log_polynomial_background`: the fit result now records the coefficient bound, absolute boundary tolerance, indices of coefficients at either bound, a boolean flag, and a warning string when a bound is active. This deliberately does not redefine optimizer success as scientific adequacy or automatically discard boundary fits. Added a deterministic monkeypatched regression test for a nominally successful boundary solution and a test for an interior solution. Source commit: `a124deb49412ccdd8e416edc76a62e4620fe1900`; test commit: `65f20057786d1427828fee7559a15e0548566e2a`. CI for these revisions is queued/in progress and must be checked before calling this change verified. The diagnostics expose a potential instability; they do not yet define or validate a confirmatory fit-failure policy.

- Extended the refitted-background toy runner to count coefficient-boundary-active fits and report their replicate indices and rate. The held-out evaluator now reports calibration-sample and evaluation-sample boundary-fit counts/rates separately, preventing the new fitter diagnostic from being silently lost during calibration. Added reproducibility/evaluation assertions for these fields. Implementation commit: `81c66fd10cf2b9dd053f5099591da84877aa3420`; test commit: `a47aa4723ad7638100e884ef822f0e0ec0c6823c`. This is diagnostic reporting only: boundary fits are still retained under the existing fixed procedure, and no confirmatory failure policy has been selected. CI remains to be checked.


## Fit-stability audit plan — 2026-10-28
- Added `docs/exploratory_fit_stability_audit_plan_2026-10-28.md`, specifying per-attempt accounting, primary diagnostic estimands, scenario and seed requirements, interpretation of coefficient-boundary activity, stop conditions, and decision gates before any confirmatory run.
- The plan explicitly requires failures to be counted and attributed rather than silently dropped, separates boundary activity from fit failure, and limits interpretation to declared synthetic null scenarios. It is a proposed exploratory plan, not preregistered, not externally reviewed, and not run.
- Commit `cfe744cbd62ab436e2e7344776df42a04f708344` adds the plan. CI has not yet been checked for this documentation-only commit. Confirmatory simulations remain NO-GO; no real-CMS validation or physics conclusion is claimed.



## Refit-failure attribution — 2026-10-29
- Updated `simulate_refitted_background_null` to preserve its fail-closed behavior while wrapping a background-fit exception with the zero-based pseudoexperiment index, master RNG seed, and RNG-stream description. The original exception is retained as `__cause__` for diagnosis.
- No retry or silent omission is introduced: execution stops at the first fit failure and no scan statistic is recorded for that failed draw. The master seed plus index identifies the draw in the deterministic NumPy `default_rng` stream; it is not represented as an independently assigned per-toy seed.
- Added a regression test that injects a failure on the third fit, checks index/seed attribution, verifies exception chaining, and confirms the routine does not retry.
- Implementation commit: `6f33ddcaa1f998456019a9a81922f582f167c310`; test commit: `fd9c826366686dc3f0c158b9dfae20ba3dcaa1a0`.
- This is a traceability improvement, not a new statistical result. CI runs for implementation commit `6f33ddcaa1` were queued at the time of the status check and must pass before the change is considered validated. Confirmatory simulation remains NO-GO pending a frozen and reviewed design; no real-CMS validation is claimed.


## Constrained-gradient diagnostic — 2026-10-29
- Code review found that the reported `gradient_infinity_norm` is the raw objective gradient. At a coefficient bound, a nonzero raw gradient can be consistent with a constrained optimum, so interpreting it alone as optimizer non-convergence would be misleading.
- Added `projected_gradient_infinity_norm`, using the box constraints and existing boundary tolerance to zero gradient components that point outward from an active bound. The original raw-gradient field remains unchanged for transparency. This is a local KKT-style diagnostic, not proof of global optimality or model adequacy.
- Added deterministic tests for an active upper-bound fixture with outward-pointing gradient and for an interior fit where projected and raw gradients coincide.
- Code commit: `c8bc11ba2328f15fbd163beb369690f21402bca3`; test commit: `1db56417308ebd7358d05d745a820e68bac10523`. CI is pending for these exact changes and must be checked before considering the diagnostic validated.
- No simulations were run. The confirmatory study remains **NO-GO** pending independent review and frozen design; no CMS-data validation or resonance claim is supported.

- Follow-up test hardening: the first CI run exposed a too-strict exact-zero assertion in the projected-gradient test; the remaining slope component had a floating-point residual of approximately (1.9\times10^{-6}). Replaced exact equality with a tight numerical tolerance and added direction-sensitive fixtures for upper/lower bounds, checking that outward-pointing gradients are projected while inward-pointing gradients remain visible. Test-fix commit: `c5c1b5c9c562dd6c8df98d524cf51ebc18e5419c`; bound-direction tests: `0f3aa81d59b3219b7c9cd5543998870e2a3238d3`. CI for the latest commit must pass before verification is claimed.



## Focused acceptance-distortion supplement and plug-in bootstrap wrapper — 2026-10-30
- Added a provenance decision log that distinguishes the official Run2012B/C AOD records, the 2019 reduced outreach NanoAOD-like file, and the public dimuon analysis example. The log explicitly prohibits trigger-efficiency claims without event-level path semantics, run-dependent configuration, prescales/luminosity treatment, and a defensible denominator.
- Added a focused acceptance-distortion supplement. It is explicitly subordinate to the existing confirmatory draft and does not change the current NO-GO decision or resolve the outstanding literature, baseline-parity, comparator, scenario-freeze, and external-review gates.
- Added `parametric_bootstrap_scan_test`, which fits the observed binned spectrum with the existing fixed-order log-polynomial null, generates calibration pseudoexperiments from the fitted means, refits each pseudoexperiment, repeats the same scan, and reports a plus-one empirical-rank p-value. The function is explicitly labelled an exploratory plug-in parametric bootstrap; it does not claim uniform composite-null calibration, model-selection handling, detector effects, or CMS validation.
- Added deterministic reproducibility and invalid-input tests. The exact new branch commit has not yet been validated by CI or local execution; do not describe the new function/tests as passing until a workflow run completes.
- Confirmatory simulation remains **NO-GO**. No new CMS-data spectrum, trigger-efficiency estimate, resonance claim, or numerical scientific result was produced in this step.
