# Implemented algorithm versus proposed estimand — code audit

**Audit date:** 2026-10-28  
**Scope:** source-level audit of the current research branch and its declared tests. No real-data execution, ROOT parity comparison, or new scientific simulation was performed in this audit.  
**Decision:** bounded exploratory implementation is in place; confirmatory calibration remains **NO-GO**.

## 1. The estimand we ultimately want

The proposed research estimand is the rejection probability of a **fully frozen, end-to-end bump-hunt** under a specified null-generating process. Every replicate must apply the same declared preprocessing, background fitting, candidate-model selection (if any), scan, maximization, and threshold rule as the analysis being evaluated. A scan statistic by itself cannot establish this operating characteristic.

## 2. What is implemented now

| Component | Current evidence | Status and limitation |
|---|---|---|
| Reconstruct opposite-charge dimuon mass spectrum from ROOT/NanoAOD-like data | `scripts/reproduce_dimuon_spectrum.py`, `src/cms_dimuon_robustness/nanoaod.py`, `src/cms_dimuon_robustness/histogram.py` | Baseline pipeline exists; numerical parity on the research-level Run2012B/C files is not established |
| Independent ROOT histogram export | `scripts/export_reference_dimuon_histogram.py` | Exporter exists; real-data bin-by-bin comparison remains pending |
| Invariant-mass and event/pair validation | `src/cms_dimuon_robustness/invariant_mass.py`, `nanoaod.py`, synthetic tests | Software checks only; not detector-level validation |
| One-sided Poisson excess statistic over contiguous windows | `src/cms_dimuon_robustness/global_scan.py` | Implemented for externally supplied expected counts; does not fit a background |
| Maximum scan statistic over declared widths | `scan_poisson_excess` | Implemented as exploratory statistic; global significance requires calibration under the same frozen scan |
| Plus-one empirical upper-tail rank p-value | `src/cms_dimuon_robustness/calibration.py` | Utility implemented; validity depends on exchangeable, correctly generated null statistics |
| Fixed-known-background Poisson null simulation | `simulate_fixed_background_null` | Implemented for independent Poisson bins with fixed means; omits fit uncertainty, model selection, detector effects and real-data validation |
| Held-out toy rejection-rate estimate | `evaluate_fixed_background_false_positive_rate` | Implemented with separate seeds and a Wilson score interval; evaluates only the fixed-known-background toy setup |
| Background likelihood fit and fitting-failure policy | No complete fit module in the audited path | Not implemented end-to-end |
| Prespecified background family/order selection | No complete selection module in the audited path | Not implemented |
| Full pipeline from a spectrum through fit, selection, scan, and global decision | No single end-to-end runner implementing the proposed estimand | Not implemented |
| Established-method comparator with documented matching choices | No completed, validated comparator in the audited path | Not implemented |
| Confirmatory experiment against misspecified null generators | Protocol draft only; required gates remain open | Not authorized; NO-GO |

## 3. Scan-statistic definition and boundaries

For a scanned window with observed total (n) and supplied expected background (b>0), the local upward-only Poisson likelihood-ratio statistic is

[
q_0 =
\begin{cases}
2\{n\log(n/b)-(n-b)\}, & n>b,\\
0, & n\le b.
\end{cases}
]

The scan returns the maximum (q_0) over every contiguous window of each declared width. Widths are measured in histogram bins; duplicate widths are removed while preserving their first appearance. Ties are resolved by the first maximum encountered in the declared width order and then by increasing start-bin position. The reported start bin is zero-based.

This statistic treats the expected background as supplied and known. It is not, by itself, a fitted-background bump hunt, a BumpHunter implementation, a local/global p-value, or evidence of a resonance. The scan maximum must be calibrated using the same scan and the relevant null-generation process.

## 4. Validation evidence and its meaning

Synthetic unit tests exercise input validation, constructed excesses, all-zero-statistic cases, duplicate widths, and a brute-force reference implementation that independently enumerates candidate windows. Calibration tests exercise empirical-tail conventions, deterministic seeded toys, Wilson interval endpoints, and held-out evaluation invariants.

CI status must be checked for the latest branch commit rather than inferred from older commits. Even a passing test matrix supports software behavior only; it does not establish physical realism, correct background modeling, type-I error control for an adaptive pipeline, or CMS data parity.

## 5. Remaining gates before confirmatory work

1. **Research-data provenance and baseline parity.** Pin the exact input file and checksum. Compare the analysis and independent ROOT export bin-by-bin, including selected-event counts, pair accounting, underflow/overflow and histogram boundaries. Declare acceptance tolerances before inspecting the comparison.
2. **Executable algorithm specification.** Freeze binning, fit range, candidate background functions, likelihood, parameter constraints, optimizer, model-selection rule, local statistic, scan windows, global statistic, and all fit-failure handling.
3. **Fit module with adversarial tests.** Test convergence failures, boundary estimates, sparse bins, numerical pathologies, and null spectra. Failures must be recorded, not silently dropped.
4. **Independent comparator.** Reproduce or implement a recognized scan-level method and document exactly which choices match and which differ. Do not claim equivalence by naming alone.
5. **Calibration design.** Keep development, threshold calibration, and held-out evaluation independent. Freeze seeds/streams, record every attempted replicate and failure, and ensure the simulated generator matches the scientific null claim.
6. **Traceability.** Bind protocol claims to concrete implementation entry points and tests. A structural validator can check that artifacts exist, but cannot certify that the implementation is scientifically correct.
7. **Novelty and independent review.** Complete the close-literature comparison and obtain review of the estimand, comparator, and scenario realism.
8. **Explicit authorization.** Do not start a large confirmatory campaign until the preceding gates pass and the project owner explicitly authorizes it.

## 6. Current decision

**NO-GO for confirmatory global-calibration simulations.** The limiting issue is the missing end-to-end fitted-background/model-selection pipeline, with research-level baseline parity, independent comparator validation, novelty review, and protocol review also unresolved.

**GO for bounded implementation and testing.** The current scan and fixed-background calibration helpers are useful exploratory building blocks. They must not be represented as the completed proposed analysis or as a CMS physics result.

## Repository artifacts

- `scripts/reproduce_dimuon_spectrum.py` — baseline reconstruction.
- `scripts/export_reference_dimuon_histogram.py` — independent ROOT export.
- `src/cms_dimuon_robustness/global_scan.py` — exploratory scan statistic.
- `src/cms_dimuon_robustness/calibration.py` — fixed-background calibration utilities.
- `configs/confirmatory_global_calibration_protocol.yaml` — unresolved draft protocol.
- `scripts/validate_confirmatory_protocol.py` — structural validator, not a scientific validator.
- `research_question.md` and `analysis_plan.md` — provisional question and staged plan.
