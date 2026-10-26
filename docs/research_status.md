# Research status ledger

**Last updated:** 2026-10-27

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
- Web-checked official Run2012B/Run2012C research-level records and identified documented HLT decision bits. A later exact-file schema audit confirmed branch presence/types in one sampled DoubleMuParked ROOT file per period; event-level path semantics, denominator, prescales, and luminosity checks remain pending.
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
- Full-file processing and quantitative comparison with the official reference spectrum. A bounded first-10,000-entry prefix of the official outreach ROOT file has passed a software smoke test; research-level Run2012B/C files have not yet been inspected at file level.
- Baseline reproduction against the official reference plot.
- Schema validation and event-level invariant-mass cross-check.
- Selection/trigger feasibility analysis.
- Implementation of a resonance likelihood or bump-hunt test statistic.
- Main pseudoexperiments, held-out stress tests, or empirical results.
- Independent external technical review.
- Manuscript submission or publication.

## Evidence policy
A planned task is not a result. A passing CI run validates the current automated software checks, not the scientific hypothesis. The baseline script has been exercised on synthetic ROOT fixtures and on the first 10,000 entries of the official outreach ROOT file. This establishes bounded software execution only; full-file processing and quantitative reference-spectrum reproduction remain unestablished. The schema inspector and independent four-vector test passed in the confirmed CI run recorded in `docs/validation_log.md`. A passing CI workflow would validate only the checks that actually ran. A repository commit is not evidence of novelty, peer review, or admissions impact.

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

## Latest baseline-selection integrity update — 2026-10-26

- The baseline script now uses the same scalar `nMuon == 2` selection as the official CMS outreach reference, instead of deriving the event selection only from `len(Muon_pt)`. Before selection, it checks `nMuon` against the `Muon_pt` collection length and verifies that `Muon_eta`, `Muon_phi`, `Muon_mass`, and `Muon_charge` have the same per-event multiplicity. A mismatch fails with the first global event index and the observed counts.
- Added synthetic ROOT regression coverage for a scalar `nMuon`/collection disagreement and for malformed muon-branch lengths in an event that would otherwise be excluded by the exactly-two-muon selection. Updated smoke fixtures to include the required scalar `nMuon` branch.
- Verified GitHub Actions run [40255415397](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40255415397) for commit `9e2409b016cedad73db650caf92411ca088e3327`: all three Python jobs (3.10, 3.11, 3.12) completed `pytest` and `ruff check src tests` successfully. The preceding code change also passed all three jobs in [run 40255405965](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40255405965).
- During the change, an intermediate commit's CI failed because older synthetic ROOT fixtures did not yet contain the newly required `nMuon` branch. The fixtures were updated, regression coverage was added, and the later runs above passed. This is a test-fixture correction, not evidence of a real-data failure.
- Scope remains limited: this validates software behavior on synthetic fixtures and supported Python versions. The official CMS ROOT file has still not been processed here; checksum capture, schema inspection on that file, full-spectrum reproduction, and quantitative parity comparison remain outstanding.

## Preregistered quantitative comparison protocol — 2026-10-26

- Added [`docs/preregistered_baseline_comparison_protocol.md`](preregistered_baseline_comparison_protocol.md) before running the real-data comparison. It freezes the reference selection and binning, requires exact input provenance and machine-readable reference outputs, specifies cut-flow and per-bin comparison metrics, and defines how discrepancies must be diagnosed.
- The protocol's target is exact integer equality in every histogram bin, but it does not grant a pass from visual similarity. Any observed differences must be localized and explained; any numerical tolerance must be justified from measured mass differences and bin widths before it is used for acceptance.
- The official reference source was inspected directly. Its mass helper returns a C++ `float`, while the candidate Python path can retain greater precision. Therefore exact bin parity is a target to test, not something to assume. The protocol explicitly requires checking bin-edge migration rather than relaxing the criteria after seeing results.
- The protocol is a planning artifact, not evidence that a real-data run has occurred. The official CMS ROOT input, local checksum, full reference histogram export, candidate full-run histogram, and quantitative comparison are still outstanding.\n\n## Executable histogram parity comparison — 2026-10-26\n\n- Added `scripts/compare_histograms.py`, a machine-readable comparator for reference and candidate CSV histograms. It validates required columns, finite and ordered contiguous bin edges, nonnegative integer counts, equal bin counts and exact bin-edge equality; reports total counts, number of differing bins, total absolute count difference, maximum absolute bin difference and each differing interval. It exits 0 only for exact integer parity and exits 2 when valid histograms have differing bin counts.\n- Added `tests/test_histogram_comparison.py` covering exact parity, a known two-bin discrepancy, fail-closed behavior for differing edges, and rejection of invalid counts. GitHub Actions runs for the new comparator, tests, output-precision change and protocol update were still in progress at the time of this status edit; results must be checked before describing these changes as CI-validated.\n- Updated the candidate histogram CSV writer to preserve low/high bin edges at 17 significant digits, avoiding unnecessary precision loss from the prior eight-significant-digit serialization. Updated the preregistered protocol to require the comparator and explain the output precision.\n- This improves the tooling needed for the future numerical comparison; it is not itself a comparison result. The official ROOT file and reference histogram have not yet been run through this tool.\n

## Exact-count comparison hardening — 2026-10-26

- Histogram comparison now parses CSV pair counts directly as base-10 integers rather than converting through binary floating point. This avoids loss of exact count information above the floating-point integer precision boundary (2^53).
- Per-bin differences, total counts, and absolute-difference metrics use Python integer arithmetic, avoiding fixed-width integer overflow in the comparator's arithmetic.
- Added a regression test that compares adjacent counts above 2^53 and confirms the one-count discrepancy is detected exactly; malformed fractional/non-integer count strings are rejected.
- Commits: comparator `53c0ee6463d4366f6f27edda9d6edcbd6016294a`; tests `dafce3bbed28e18fe6c6ac9f61ed732805f9605c`. The CI result for these commits must be checked before describing the change as validated.
- This improves the comparison tool only. It is not evidence that the real CMS file has been processed or that candidate/reference parity has been achieved.


## Histogram comparator validation closure — 2026-10-26

- The corrective test commit `4e8fd45c14e865713790e8f9ad47d3f81033dac1` passed all three configured Python jobs in GitHub Actions run [40256388844](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40256388844). The following ledger/documentation commit `ee2265993c9236f4b286874883e378f336f4ae82` passed run [40256407530](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40256407530).
- The earlier failed comparator workflow remains documented in `docs/validation_log.md`; its cause was stale invalid-count error-message assertions after exact-integer parsing was introduced. Those assertions were updated and the corrected workflow is green.
- Current validated scope: synthetic histogram fixtures and automated tests/lint across Python 3.10, 3.11, and 3.12. Still not validated: the official ROOT input, its checksum/schema, the candidate full-data spectrum, the official reference export, and numerical histogram parity. Do not describe the analysis as reproduced until those steps are executed and archived.


## Comparator robustness update — 2026-10-26
- Added strict histogram CSV structural validation: duplicate column names and rows with extra/missing fields are rejected rather than silently interpreted.
- Histogram counts are parsed as decimal integer strings, not through floating-point conversion; malformed forms are rejected and large counts remain exact.
- Regression tests cover malformed files and exact integer behavior. The initial malformed-fixture test run failed due to incorrect newline escaping in the test data; the fixture was corrected, and CI run [40257190269](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40257190269) passed pytest and Ruff on Python 3.10, 3.11, and 3.12.
- Evidence boundary unchanged: automated CI validates the tested software paths, not real-data correctness. Official ROOT-file execution, provenance capture from the actual input, reference histogram export, and bin-by-bin parity remain uncompleted.


## Independent numerical reference exporter — 2026-10-26
- Added `scripts/export_reference_dimuon_histogram.py`, a PyROOT/RDataFrame path that follows the official selection and mass calculation, exports ROOT regular-bin counts to CSV, and writes ROOT version, selection cut-flow, and underflow/overflow metadata.
- Updated the real-data guide with the command, artifact requirements, and warning that the script has not yet been executed against the CMS ROOT file. The generated reference artifact must be checked against the exact input checksum and official source before use.
- CI now compiles project scripts and lints the new exporter in addition to existing tests. The workflow result for this change is pending; no passing status is claimed yet.
- This closes an implementation gap, not the empirical gap: no real CMS spectrum or bin-by-bin parity result has been produced.


## ROOT exporter CI follow-up — 2026-10-26
- CI run [40257810613](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40257810613) passed on Python 3.10, 3.11, and 3.12 after adding file-size/optional SHA-256 metadata to the reference exporter. The workflow now compiles Python files and lints the exporter in addition to running tests.
- The exporter records the official source commit `19a4a64fd58ef66a6ee3cf4f2a469fba61c60a09` and source URL. The final source-pin commit's CI status remains separate and must be checked before being called validated.
- This is syntax/lint/software-suite evidence only; the CMS file has not been processed with PyROOT, and no reference/candidate histogram comparison has been run.


## Metadata-audit acceptance hardening — 2026-10-26
- The metadata audit now validates strict JSON types for booleans, counts, bin counts, mass ranges, tree names, SHA-256 digests, and input file sizes.
- Full-data acceptance requires the candidate to read the complete reference event count, match `events_read` to `events_processed`, and avoid a partial `max_events` limit.
- Pair accounting is conserved across in-range, below-range, overflow, and non-finite categories. Event and pair count bounds reject impossible cut-flow metadata.
- Reference ROOT histogram entries including flow are checked against the opposite-sign event count. New regression tests cover partial runs, inconsistent pair totals, malformed types, impossible count relationships, and reference cut-flow mismatch.
- Corrected fixtures after earlier CI failures exposed missing new metadata and a non-conserving synthetic count example. Latest code/test commit `475c0eb8dc5d7354442a515436a16c749ed90b54` passed the ordinary Python 3.10/3.11/3.12 tests, compilation, and Ruff workflow [40275514023](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40275514023) and ROOT synthetic integration workflow [40275522182](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40275522182).
- A later documentation-only commit `c21d98e8537d70d92ef4eb2f33647c8527b3fecf` records these changes; its own CI was still running when this status entry was added.
- None of these checks substitutes for processing the official CMS file. Actual data checksum/schema capture, full candidate run, independent reference CSV, and exact 30,000-bin comparison remain uncompleted.

## Reference histogram flow-count conservation — 2026-10-26
- Added a strict invariant requiring regular-bin counts + underflow + overflow to equal the reference histogram's recorded fill-entry count.
- Added regression tests for a non-conserving flow-count sum and a boolean masquerading as an integer count.
- Code, tests, and validation-log updates are committed. Check CI on the current head before treating this latest addition as validated.
- Empirical boundary unchanged: no full official CMS input processing, reference export, or 30,000-bin parity claim has been completed.


## Comparator-report internal consistency — 2026-10-26
- The metadata audit now requires the comparator's discrepancy summary to agree with exact parity: zero differing bins, zero total absolute count difference, and zero maximum absolute count difference, all strict nonnegative integer fields.
- Added a regression test for a contradictory report claiming parity while reporting nonzero discrepancies.
- Latest code and test commits are committed; check their GitHub Actions results before describing this addition as validated.
- The actual official CMS dataset has not been processed, and no full-data 30,000-bin parity result is claimed.


## Comparator discrepancy-list consistency — 2026-10-26
- Added an audit invariant requiring the `differing_bins` list length to match `differing_bin_count` and each entry to be an object.
- Updated exact-parity fixtures and added a regression test for a zero count paired with a nonempty mismatch list.
- Latest code/test CI remains the acceptance gate; full CMS data processing and 30,000-bin parity remain outstanding.


- Hardened audit JSON parsing against duplicate object keys, which standard `json.loads` behavior would otherwise silently resolve by keeping the last occurrence. Regression tests cover all three audit inputs (reference metadata, candidate metadata, and histogram report). The code and tests passed GitHub Actions on Python 3.10, 3.11, and 3.12; see `docs/validation_log.md`. This is input-integrity hardening, not real-data validation.


- The audit CLI now writes a structured `FAIL` JSON artifact and exits with status 2 when any input metadata file is malformed or contains duplicate keys. A regression test verifies this behavior; Python 3.10/3.11/3.12 automated checks and the synthetic ROOT integration workflow passed. This is defensive tooling work, not evidence of a successful CMS-data reproduction.


- Strict JSON parsing now rejects non-standard `NaN`/infinity tokens in all three audit inputs, with regression coverage for each token and input position. The updated test suite passed across Python 3.10–3.12 and the synthetic ROOT integration workflow passed. See `docs/validation_log.md`; this is metadata validation, not a real-data result.


- Added a numerical-stability guard for float32 NanoAOD branches: kinematic fields are promoted to float64 before invariant-mass arithmetic. A regression test targets nearly collinear high-pT muons, where float32 intermediate rounding can erase a nonzero invariant mass. The pinned reference returns a C++ `float`, so exact histogram parity remains an empirical question; this fix is not a parity claim. See `docs/validation_log.md`.


- Both histogram CLIs now reject non-finite mass bounds before touching the ROOT input. Candidate and reference run metadata also record the checked-out project commit, separately from the pinned upstream reference-source revision. Regression tests were added for invalid bounds and project-commit metadata; the corrected tests passed on Python 3.10–3.12 and the ROOT integration workflow passed on commit `33f703fcad9f4609b730f928277ba19c0a5a8dee`. See `docs/validation_log.md` for run links and the note about correcting the negative-infinity argparse fixture.


## Numerical-stability follow-up — 2026-10-26

- The vectorized and NanoAOD mass paths now use a cancellation-resistant invariant-mass expression based on transverse masses, rapidities, and half-angle identities rather than direct subtraction of large squared four-vector components.
- Regression coverage includes two nearly collinear muons at pT=1e8 GeV with float32 NanoAOD inputs; the physical nonzero mass is retained. The latest code/test commit passed the Python 3.10–3.12 test, compilation, and Ruff matrix and the ROOT synthetic integration workflow (runs 40282993593 and 40282993559).
- This is a numerical robustness result, not a real-data validation result. Exact 30,000-bin parity against the pinned reference remains unmeasured on the official CMS input.


## Bounded reference-export smoke tests — 2026-10-26

- The PyROOT reference exporter supports `--max-events N`, using single-threaded `RDataFrame.Range` to limit processing during a smoke test. Full runs retain implicit multithreading; metadata identifies the event cap so a partial sample is not confused with a full-data run.
- Synthetic integration confirms the one-event capped reference run and full-fixture candidate/reference parity. The Python 3.10–3.12 matrix and ROOT integration passed on code/test commit `cde7b263ee404bdbebe0659518c837dbef080858` (runs 40283199640 and 40283199631).
- No bounded or full export has yet been executed on the official CMS file. The next scientific acceptance milestone remains checksum/schema capture, full-data reference and candidate exports, and an exact 30,000-bin comparison.


## Candidate/reference input-integrity parity — 2026-10-26

- Both implementations now reject malformed muon charge values and finite negative transverse momenta or masses before filling histograms. Non-finite candidate kinematics remain separately accounted for rather than being silently converted to a physical mass.
- Regression tests cover invalid charges and negative finite kinematics. The full Python test/compile/Ruff matrix and ROOT synthetic integration passed on commit `23c17d919a02a452a391741b38434c867e95b21a` (runs 40283709403 and 40283709344).
- Full official CMS input processing, checksum/schema capture, and exact 30,000-bin reference comparison are still outstanding.


## Selection-aligned reference preflight — 2026-10-26

- The ROOT reference exporter validates collection lengths for all events, while charge and finite-negative kinematic validation is limited to the selected `nMuon == 2` events. A regression test verifies that an unselected one-muon event with an invalid charge is not rejected.
- Commit `206678e4fcb444de7c7e89bca4d2f3c157ca79b9` passed the Python 3.10–3.12 matrix and ROOT integration (runs 40283968358 and 40283968367; 8 ROOT integration tests passed).
- The remaining scientific blocker is still the actual CMS file: no real-data reference export, candidate export, or exact 30,000-bin parity comparison has been performed.


## Trigger feasibility gate and latest CI audit — 2026-10-26

- Added `docs/run1_trigger_feasibility_gate.md` to distinguish the six-branch muon-only outreach sample from the richer Run2012B/Run2012C derived records, and to define evidence required before any trigger-efficiency claim. It explicitly separates schema documentation from file-level evidence and records no real-data trigger audit as completed.
- Updated `docs/data_schema_findings.md` and `docs/data_source_assessment.md` with official CERN variable-list evidence and the limitations of HLT decision bits. The CERN trigger guide explains that path configurations vary by run and that stored decisions alone do not establish efficiency or prescale correction.
- Latest confirmed Python test matrix and ROOT synthetic integration runs for commit `55728e154ee0c26ac9a0ff7cf8f3f48999194b5f` both have successful runs (`40287725284` and `40287725431`). A separate overlapping Python workflow (`40287731148`) failed in all three environments on an assertion expecting exactly four branches in `tests/test_schema_inspection.py`; its log does not match the test file present at that commit, where the corresponding test uses `>= 4` in `tests/test_schema_inspector.py`. The failed run's jobs were requested for rerun; do not call that rerun successful until checked.
- No official CMS ROOT file has been inspected or processed by this repository. Actual file checksum/schema capture, run-dependent HLT interpretation, validated-lumisection application, candidate/reference full-data outputs, and exact 30,000-bin parity remain outstanding.


## Latest schema and trigger-feasibility work — 2026-10-26

- Corrected the exact HLT-branch inventory after checking CERN's published variable lists: the derived schemas document paths such as `HLT_Mu13_Mu8` and `HLT_Mu17_Mu8`, but the checked pages do not document the earlier-listed `HLT_Dimuon0_Jpsi`, `HLT_DoubleMu11_Acoplanarity03`, or `HLT_DoubleMu5_IsoMu5` branches. Original AOD possible-path lists are not proof of derived-branch presence.
- Added the official `HLT_Mu13_Mu8` version/run-interval record and 2012 luminosity record to the source audit. The path changes across Run2012B/C; the applicable version and run range must be resolved per event.
- Added Run2012B/C SingleMu datasets as *candidate* denominator-study inputs, not as a ready-made unbiased denominator. Their published schemas say trigger objects are only partially filled and that `GoodLumisection` is not available in every dataset.
- Enhanced `scripts/inspect_root_schema.py` to include ROOT branch type strings in its JSON output, and added regression coverage. A separate compatibility test now avoids assuming that jagged/split ROOT branches produce exactly four branch names.
- Added an opt-in bounded real-data schema-audit workflow for one file each from Run2012B/C DoubleMuParked and SingleMu. The workflow's initial Actions runs failed before creating any jobs (zero jobs returned), so no real-data schema audit has run yet. This needs workflow-level diagnosis; do not report the data audit as complete.
- Existing synthetic ROOT integration passed on commit `9931de407e6d5e53d3f9c0f1136cbd8eb8f7c8f2` (run `40299849754`). The full Python test workflow after the branch-type change and compatibility test is still pending/ambiguous; earlier overlapping runs reported a failure in a test path that was not present in the reported commit tree. Verify the latest commit's checks before treating the code change as accepted.
- The scientific blocker remains actual ROOT-file provenance/schema and event-level inspection. Trigger efficiency, a novel method, and full-data 30,000-bin parity remain unestablished.


## Real-data execution path correction — 2026-10-26

- The initial GitHub Actions workflow intended to download and inspect one ROOT file per CERN record repeatedly failed before creating any jobs. To avoid leaving a broken workflow in the research branch, I removed it and documented a bounded manual procedure in `docs/real_data_baseline_run_card.md` using the official `cernopendata-client`, checksum verification, `scripts/inspect_root_schema.py`, and a provenance manifest.
- No actual CMS ROOT file has been downloaded or inspected in this environment; outbound DNS/network access from the local execution container is unavailable, and the repository connector does not expose a workflow-dispatch action. The next data step therefore requires running the documented commands in an environment with CERN Open Data access, or fixing/enabling a validated remote execution path.
- The PR remains open and in draft. Latest Python and ROOT integration runs on the newest commit are queued, so the schema type enhancement and regression test must not be described as fully CI-validated yet.


## Latest status correction — 2026-10-26 (after outreach smoke test)

- The bounded outreach ROOT smoke test is confirmed successful: GitHub Actions run [40372505488](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40372505488), code commit `8ead6521c726442f8766433554e709186ed2426a`. It read the first 10,000 entries in file order, found 5,750 exactly-two-muon events and 4,504 opposite-charge pairs, and reconciled 24 below-range + 4,478 in-range + 2 at/above-range + 0 non-finite = 4,504 pairs.
- This does **not** supersede the outstanding research-level schema audit: no exact file from records 31123, 31129, 31127, or 31133 has been verified by a schema report in this repository. The documented CERN-client run card remains unexecuted.
- The README was corrected in commit `2f0e50789803ca394f7d63a146a485f9ee9847ac` so it no longer contradicts the successful bounded outreach smoke test. No successful CI result has yet been observed for that newest documentation commit; the GitHub combined-status connector returned no status entries, which is inconclusive rather than a pass.
- Current scientific decision: do not claim trigger efficiency or trigger-aware robustness from the outreach file. The next acceptance gate is exact-file schema/provenance for research-level data, followed by an explicit trigger-denominator/prescale feasibility decision. If that cannot be established, narrow the data claim to spectrum reconstruction and clearly labelled pseudoexperiment stress tests.


## Execution-path correction — 2026-10-27

- The attempted research-level ROOT schema-audit workflows were removed in commits `67482e77c6896b800eabf48c5863a8b80145ef84` and `1d2c28ff368edfa6e88b2631691ca41bc4b8bd87`. This reverses an unverified workflow addition: the existing project history records that similar workflow attempts failed before creating jobs, and this session's GitHub connector can inspect some PR-triggered runs but cannot dispatch a workflow or reliably enumerate push-triggered runs.
- The new workflow file was inspected before removal: it installed the project and CERN Open Data client, attempted to download one ROOT file from records 31123 and 31129, and would have uploaded schema JSON and a checksum manifest. Its command sequence was not executed in this session; its intended behavior is not evidence of a successful download.
- The canonical next step remains the bounded manual procedure in `docs/real_data_baseline_run_card.md`, which also includes candidate Run2012B/C SingleMu records 31127 and 31133. A successful file-level audit must preserve exact file identity, checksum, schema JSON, tree entries, and branch types. Do not claim that research-level ROOT files have been inspected until those outputs exist.
- No CMS collision ROOT file was opened by this session. Trigger path availability, run-dependent path semantics, valid denominator, prescales/luminosity handling, and quantitative reference-spectrum reproduction remain unverified. This workflow cleanup does not change the scientific status.


## Literature-scope decision — 2026-10-27

- Added `docs/literature_scope_decision_2026-10-27.md` after screening primary-source records for Williams (2017), Cesarotti et al. (2019), data-directed bump hunting (2022), resonant anomaly detection/background sculpting (2023), and a newer model-parameter-space paper (2025). This is a focused source-screening memo, not a systematic review or a claim that every paper's methods have been fully audited.
- The current broad question—background misspecification plus fixed-versus-selected model comparison—has substantial overlap risk. The memo places large Monte Carlo runs and novelty claims on hold until the closest methods are compared and a distinct estimand/decision is justified.
- The next priority remains the exact-file feasibility gate for Run2012B/C research-level ROOT data. The successful outreach smoke test is only a bounded software check; it does not establish trigger semantics, valid denominator/prescale handling, full reference parity, or a physics result.
- README now links the scope memo. Latest documentation commit: `febb4e9cf1d4e0ef3177ef09eb7be30196285a46`. The available status/run lookup returned no entries for this commit; latest-head CI is **unverified**, not a pass.


## Latest verified status — 2026-10-27

- **Research-level schema audit completed:** workflow run [40403830670](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40403830670) succeeded for one checksum-verified file from Run2012B DoubleMuParked record 31123 and one from Run2012C DoubleMuParked record 31129. It uploaded JSON schema reports and a file manifest. The report `docs/exact_file_schema_audit_run2012b_c_2026-10-27.md` records exact filenames, byte sizes, SHA-256 digests, tree entry counts, branch types, and limitations.
- The sampled `Events` trees contain `Muon_pt/eta/phi/mass/charge`, run/lumisection/event identifiers, candidate quality/isolation fields, `GoodLumisection`, and many HLT/L1-named branches. `HLT_Mu13_Mu8` and `HLT_Mu17_Mu8` are Boolean branches in both samples. This confirms schema-level availability only—not event-level trigger semantics, active path versions, prescale corrections, an unbiased denominator, or trigger efficiency.
- The earlier section “Execution-path correction — 2026-10-27” records an intermediate point in the work when no successful audit was yet available. It is superseded by the later successful run and report above. The workflow is manual-only to avoid repeated multi-gigabyte downloads. It currently exists only on the unmerged research branch, so manual dispatch is not available until the workflow file is present on the default branch.
- Focused literature screening now covers close work on dimuon bump hunts, model selection, data-directed searches, background sculpting, and Bayesian marginal-likelihood methods. The review is not systematic and no novelty claim is justified yet.
- CI for the code/tests and ROOT exporter on commit `88efc10e2c48a8662c2d17aa2669b4f36f3daad5` passed on Python 3.10, 3.11, and 3.12, and the ROOT exporter integration passed. CI for later documentation commits is being checked; do not generalize earlier passes to every latest commit.
- **Next acceptance gate:** run the baseline spectrum pipeline on a bounded event subset from the research-level files and compare against a suitable public reference, then inspect event-level run/trigger values. Do not launch the main simulation campaign until baseline validity and the exact research gap are established.


## CI confirmation after workflow/documentation updates — 2026-10-27

- The project test workflow and ROOT reference-exporter integration both completed successfully for commit `54cdcc1629e9ecf628d8068376a05b0c8dbb068a`: [tests run 40411406132](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40411406132) and [ROOT integration run 40411405993](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40411405993).
- These checks validate the repository's automated test suite and reference-exporter integration at that commit. They do **not** execute the manually dispatched research-level download/baseline workflow, validate the workflow's external data downloads, or constitute real-data spectrum reproduction.
- The current research-level workflow includes a bounded 100,000-entry spectrum smoke test per sampled DoubleMuParked file. It still requires manual dispatch in GitHub Actions. Until its artifact exists and is inspected, the spectrum results remain pending.


## Manual baseline workflow execution gate — 2026-10-27

The revised bounded baseline/parity workflow has not run. A dispatch-path audit found that the workflow exists only on the unmerged research branch, while GitHub requires a `workflow_dispatch` workflow file to exist on the default branch before the manual dispatch control/event is available. The run card, README, and validation log now state this prerequisite. I have not merged the draft PR or changed the default branch merely to expose the workflow. The next gate is an intentional review/merge decision or execution of the documented bounded run in a controlled environment with CERN Open Data access. Until then, candidate/reference numerical parity is unknown.
