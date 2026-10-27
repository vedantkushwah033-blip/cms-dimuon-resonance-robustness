# Independent-baseline comparison tooling: static review

**Review date:** 2026-10-27  
**Branch:** `research-plan/initial-protocol`  
**Review type:** source inspection only; no code was executed in this review.  
**Decision:** tooling is promising, but scientific baseline remains **NOT VALIDATED** until a successful bounded real-data run produces inspectable artifacts.

## Scope reviewed

Static inspection covered:
- `scripts/compare_histograms.py`
- `scripts/compare_baseline_metadata.py`
- `scripts/export_reference_dimuon_histogram.py`
- `pyproject.toml`
- `.github/workflows/tests.yml`
- `.github/workflows/research-level-schema-audit.yml`

This review does not certify code correctness, run the workflows, or validate the scientific interpretation.

## Positive design choices observed

1. Histogram counts are parsed as exact integer strings rather than floats, avoiding loss of integer precision above (2^{53}).
2. Bin edges are checked for finite values, positive widths, ordering/contiguity, and candidate-reference agreement using an explicit absolute tolerance.
3. The comparison report preserves per-bin count differences and distinguishes edge compatibility from exact count parity.
4. Metadata comparison checks event cut flow, histogram configuration, mass-range accounting, and the candidate's non-finite-mass count.
5. The reference exporter uses ROOT/RDataFrame and ROOT four-vectors, while the candidate path uses the project's Uproot/NumPy/Awkward implementation. This is a useful cross-implementation check, though both still need to be shown to represent the intended reference procedure.
6. The research-level workflow preserves comparison reports and exit statuses even when parity checks fail, which supports diagnosis instead of hiding discrepancies.
7. The workflow is manual rather than downloading large research files on every documentation change.

## Important interpretation boundaries

- Exact histogram parity only establishes agreement for the same input files, event prefix, branches, selection, mass calculation, and histogram definition. It does not establish that the selection is appropriate for a physics question.
- The workflow's 100,000-event prefix is a bounded validation sample, not a full-period measurement and not a luminosity-representative sample by default.
- A schema inventory establishes branch names/types, not trigger activation, prescales, certified luminosity, stream-selection semantics, or an unbiased efficiency denominator.
- A passing synthetic test suite establishes only the behaviors exercised by those tests. It does not replace real-data parity.
- ROOT and NumPy can differ in how edge values and non-finite values are handled. The current metadata comparator appropriately blocks flow-bin interpretation when the candidate has non-finite masses, but this behavior must be exercised on actual data.
- A successful workflow can fail to establish scientific parity even if download and schema inspection succeeded. Inspect the comparison JSON and metadata comparison JSON; do not use the workflow's overall status as a substitute for reviewing those artifacts.

## Required acceptance criteria for the next bounded run

For each Run2012B/C sampled file:

1. Confirm the exact record, filename, size, SHA-256, tree, entry limit, and selected branch list are preserved in the artifact manifest.
2. Confirm candidate and reference process the same event prefix and the same required branches.
3. Require exact integer parity in every histogram bin and bin edges within the declared tolerance.
4. Require all cut-flow/configuration checks to pass, including zero candidate non-finite masses for the current flow-bin comparison.
5. Inspect any failure report before changing code; preserve the failing artifact and explain the root cause.
6. Record the precise code commit and dependency/runtime versions for both paths.
7. Keep trigger-efficiency and new-physics claims out of the report unless separate evidence supports them.

## Current gate decision

**Gate 3 (independent numerical parity): NOT YET PASSED based on the evidence available to this static review.** The repository contains the comparator and a workflow intended to generate the evidence, but this review did not verify a successful current run with parity artifacts. A prior schema-audit success is not a parity result.

**Next action:** retrieve and inspect the latest research-level audit workflow run and its artifacts, if available; otherwise run the bounded workflow through an explicitly authorized route. Do not start confirmatory pseudoexperiments until the data baseline, estimand, comparator, and novelty gates are resolved.
