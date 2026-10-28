# Gate review — bounded real-data parity workflow (2026-10-28)

**Review type:** static repository review only; no ROOT analysis was executed.  
**Decision:** numerical baseline remains NOT VALIDATED. Keep confirmatory simulations and scientific claims on hold.

## Reviewed
The current research-branch workflow, Uproot/Awkward candidate reconstruction, ROOT/RDataFrame reference exporter, histogram comparator, metadata comparator, and package configuration.

The workflow intends to download one checksum-verified ROOT file from each of records 31123 and 31129 and compare the first 100,000 events using 30,000 histogram bins. The earlier successful run 40403830670 was schema-only and is not evidence that this revised comparison ran.

## Static positives
- Both implementations require the same core muon branches and use an exactly-two-muon, opposite-charge selection.
- Candidate collection lengths and nMuon consistency are checked.
- Candidate pair counts are explicitly reconciled across mass-range categories.
- Histogram counts are compared as exact integers; bin edges use an explicit tolerance.
- Metadata checks cover cut flow, range, bin count, event limit, and candidate non-finite masses.
- The workflow is manual and uses read-only repository permissions.

## Blockers and cautions
1. **ROOT is not version-pinned.** Metadata records the installed version but does not guarantee a repeatable installation. Do not guess a pin; test one before freezing it.
2. **Exact bin parity is numerically sensitive.** The candidate and reference use distinct invariant-mass implementations. With 30,000 uniform bins over 0.25–300 GeV, bin widths are about 0.01 GeV; tiny floating-point differences near internal edges can shift counts. Preserve discrepancies, inspect event-level residuals, and do not relax tolerances after seeing results without a documented, predeclared rationale.
3. **100,000 events are an engineering prefix, not a representative or luminosity-normalized physics result.**
4. **Trigger claims remain unsupported.** Branch presence alone does not establish trigger semantics, prescales, certified luminosity, or an unbiased efficiency denominator.
5. **A green workflow status is insufficient.** Inspect artifacts for both records: file manifest and checksums, candidate/reference CSVs, comparison JSON and exit codes, metadata, software versions, logs, and warnings.

## Acceptance gate
- Acquisition: exact record/file identity and checksum verified.
- Schema: expected tree, branches, and event limit confirmed.
- Numerical parity: actual comparison outputs exist for both files; discrepancies are explained against predeclared criteria.
- Interpretation: explicitly state the bounded prefix and selection; make no trigger-efficiency, discovery, or novelty claim from parity alone.

Until actual candidate/reference artifacts are inspected, numerical parity is NOT RUN / NOT ESTABLISHED. Even a parity pass would not independently justify confirmatory pseudoexperiments; literature gap, estimand, comparator, analytic controls, and fit-failure policy remain separate gates.

Keep PR #2 and PR #1 unmerged during this review. No multi-gigabyte run has been dispatched by this review.
