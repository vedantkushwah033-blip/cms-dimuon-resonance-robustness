# Implemented algorithm versus proposed estimand — code audit

**Audit date:** 2026-10-28  
**Scope:** source-level audit of the current research branch; no real-data execution or new statistical experiment was performed.  
**Conclusion:** the repository currently implements a dimuon-spectrum reconstruction and validation scaffold. It does **not** yet implement the proposed bump-hunt, adaptive background-model selection, scan-level test statistic, or global false-positive calibration. The protocol remains a design proposal, not an experiment that can currently be run end-to-end.

## 1. Claim-to-code map

| Research claim or component | Evidence in current code | Status |
|---|---|---|
| Reconstruct an opposite-charge dimuon mass spectrum from a ROOT/NanoAOD-like file | `scripts/reproduce_dimuon_spectrum.py`, `src/cms_dimuon_robustness/nanoaod.py`, and `src/cms_dimuon_robustness/histogram.py` | Implemented as a baseline pipeline; numerical parity on the research-level Run2012B/C files is not established |
| Independently calculate a reference histogram using ROOT | `scripts/export_reference_dimuon_histogram.py` | Implemented as an exporter; real-data comparison remains pending |
| Validate kinematic calculations and data integrity | `src/cms_dimuon_robustness/invariant_mass.py`, `nanoaod.py`, synthetic-data tests | Partially validated by unit/synthetic tests; this is software validation, not detector-level validation |
| Fit a smooth background likelihood to a mass spectrum | No fit/likelihood implementation identified in the audited analysis scripts | Not implemented |
| Define and compute a local excess/test statistic over mass windows | No bump-hunt or local-test-statistic implementation identified | Not implemented |
| Scan mass windows and compute a global statistic such as a maximum over the scan | No scan implementation identified | Not implemented |
| Select a background model/order from each observed spectrum | No candidate-family fitting or selection algorithm identified | Not implemented |
| Calibrate a global rejection threshold on separate pseudoexperiments | The YAML protocol describes intended fields, but there is no end-to-end calibration runner identified | Not implemented |
| Evaluate rejection frequency on disjoint held-out generators | Protocol template only; no generator/partition runner identified | Not implemented |
| Estimate false-positive rate with confidence intervals and explicit fit-failure accounting | An exact binomial interval utility exists, but no global bump-hunt calibration pipeline feeds it | Utility exists; proposed estimand workflow not implemented |
| Claim a novel statistical result from CMS data | Baseline parity and scientific gates are explicitly pending | Not supported |

## 2. What the existing software actually answers

The baseline scripts answer a narrower, useful engineering question: given a chosen ROOT file and a declared selection, can the code compute opposite-charge dimuon masses, account for histogram boundaries and invalid values, preserve provenance, and emit reproducible outputs? Synthetic tests can check the software's internal invariants.

They do **not** answer whether an adaptive bump-hunt has a calibrated global type-I error, whether background-model selection changes that error, or whether a candidate algorithm is robust to out-of-family background generation. Those require new analysis code and independent validation.

## 3. Why this distinction matters

The proposed estimand is the rejection probability of the **complete frozen algorithm** under a specified null generator. To estimate it, each replicate must execute the same end-to-end steps that would be used on an observed spectrum, including any fitting, model choice, mass-window scan, maximization, and threshold comparison. A histogram exporter plus a protocol YAML cannot establish that property.

The current protocol validator is deliberately structural: a completed-looking YAML can satisfy schema checks without proving that the described algorithm exists or matches the specification. Therefore, even a future structural-validator PASS must not be interpreted as implementation evidence or permission to run confirmatory simulations.

## 4. Required implementation gates before confirmatory work

1. **Baseline parity:** run both implementations on the same pinned, checksum-verified research-level ROOT input and compare bin-by-bin counts, underflow/overflow, selected-event counts, and pair accounting. Define acceptance tolerances before examining the result. Resolve any mismatch rather than normalizing it away.
2. **Executable algorithm specification:** write a minimal, deterministic bump-hunt implementation with explicit fit range, binning, candidate background forms, optimizer/constraints, local statistic, scan windows, global statistic, and failure behavior.
3. **Unit-level statistical checks:** test the statistic on analytically tractable or deliberately constructed spectra; test no-signal null cases, numerical failures, boundary conditions, and deterministic reproducibility.
4. **Reference comparator:** implement or independently reproduce an established scan-level comparator (for example, a BumpHunter-style procedure) and document exactly which choices are comparable. Do not imply equivalence from the name alone.
5. **Calibration runner:** implement separate development, threshold-calibration, and held-out evaluation partitions; preserve independent random streams; record every attempted replicate and every failure.
6. **Validator-to-code binding:** make the protocol identify concrete implementation entry points and tests, and add a gate that checks those declared artifacts exist. This is only a traceability check; a human/statistical review is still required to establish that code matches the scientific specification.
7. **Novelty and independent review:** finish the close-literature comparison and obtain review of the estimand, comparators, and scenario realism before confirmatory execution.
8. **Authorization:** leave confirmatory execution blocked until the preceding gates pass and the owner explicitly authorizes it.

## 5. Current go/no-go decision

**NO-GO for confirmatory global-calibration simulations.** The main reason is not computational scale: the end-to-end statistical procedure is not yet implemented. Research-level numerical baseline parity, complete literature novelty assessment, and independent protocol review are also unresolved.

**GO for bounded implementation work:** first build a small, testable scan/statistic module on synthetic spectra while keeping it clearly labelled exploratory. This can make progress without spending large compute budgets or implying a CMS physics result. Keep synthetic algorithm tests separate from real-data baseline acceptance.

## 6. Audit limitations

This is a bounded source-level audit of the named scripts and protocol artifacts, not a proof that no related code exists anywhere in every branch or commit. It does not assess physical realism, provide a systematic literature review, or certify novelty. Before changing the research claim, search the full repository and have the implemented algorithm independently reviewed.

## Sources in repository

- `scripts/reproduce_dimuon_spectrum.py` — baseline histogram reconstruction.
- `scripts/export_reference_dimuon_histogram.py` — independent ROOT histogram export.
- `src/cms_dimuon_robustness/invariant_mass.py` and `nanoaod.py` — kinematic and pair-selection helpers.
- `configs/confirmatory_global_calibration_protocol.yaml` — intentionally unresolved draft.
- `scripts/validate_confirmatory_protocol.py` — structural protocol validator, not a scientific or implementation validator.
- `research_question.md` and `analysis_plan.md` — provisional question and staged plan.

## Follow-up implementation status — 2026-10-28

This audit's original inventory above predates the exploratory scan and fixed-background calibration helpers added later on the same research branch. It must not be read as saying those components are still entirely absent. The current branch now includes:

- `src/cms_dimuon_robustness/global_scan.py`: a one-sided Poisson excess statistic scanned over a caller-supplied set of contiguous window widths, using externally supplied expected counts.
- `src/cms_dimuon_robustness/calibration.py`: plus-one empirical upper-tail p-values, fixed-known-background independent-Poisson null generation, a Wilson score interval, and a separate held-out toy false-positive evaluation helper.
- Synthetic unit tests for the scan and these utilities.

These are bounded exploratory building blocks. They do **not** complete the proposed end-to-end algorithm: there is still no fitted-background likelihood/uncertainty pipeline, no prespecified candidate-model selection implementation, no complete data-to-global-p-value runner, no matched established-method comparator, and no demonstrated real-data parity. The held-out helper evaluates only the fixed-background toy null, not the proposed misspecification estimand. Consequently, the NO-GO decision for confirmatory global-calibration simulations remains unchanged.

The Python test matrix subsequently passed on Python 3.10, 3.11, and 3.12 for commit `4e171a8a` (CI run `40707114657`). The dedicated PyROOT integration job for that commit was still running at the time of this update; it is not represented as passed here.
