# Bounded baseline workflow audit — 2026-10-28

**Status:** static source audit only. No CERN ROOT file was downloaded or processed during this audit. No real-data parity claim is made.

## Scope inspected

Branch: `audit/histogram-edge-and-sensitivity-fixes-2026-10-28`

Inspected:
- `scripts/reproduce_dimuon_spectrum.py`
- `scripts/export_reference_dimuon_histogram.py`
- `scripts/compare_baseline_metadata.py`
- `scripts/estimate_bin_flip_sensitivity.py`
- `docs/global_false_positive_protocol_draft_2026-10-28.md`

## Findings

### 1. The comparison is designed to bind outputs to the same input file

Both exporters record input byte count and optionally a SHA-256 digest. The comparator requires valid matching digests and positive matching byte counts, and can additionally compare both outputs to a manifest-provided digest and byte count. This is a strong provenance check when enabled. It does not establish that the event selection or calculation is scientifically correct.

### 2. The bounded prefix is an entry-order prefix, not a random sample

The candidate reads up to `--max-events` sequential entries in Uproot chunks. The ROOT exporter applies `RDataFrame.Range(max_events)` before its filters. The comparator checks the requested event limit and checks the processed counts. This is intended to compare the same first N entries, not a statistically representative subset. The input file/tree identity and the prefix length must remain identical.

A requested prefix longer than the tree should fail the expected-prefix check rather than silently being described as a full prefix.

### 3. Selection parity is narrower than general dimuon-spectrum parity

The current ROOT reference exporter selects `nMuon == 2`, then requires the two charges to differ. The candidate's default mode likewise selects events with exactly two reconstructed muons before forming opposite-charge pairs. In this mode, event and pair counts are expected to be one-to-one after selection.

The candidate also exposes `all-opposite-charge-pairs`, which allows events with more than two muons and can contribute multiple pairs per event. That mode is not semantically equivalent to the current reference selection and should not be used for a parity run. The comparator's count checks are expected to fail for incompatible selection semantics, but the run configuration should still explicitly record and enforce the intended mode.

Official CMS Open Data examples are not all identical: the CERN-published NanoAODRun1 examples describe a selection of two or more muons followed by opposite-charge selection. That is a different selection from exactly two muons. Therefore, the current pipeline must be described as a bounded comparison against its pinned reference implementation, not as universal equivalence to every CMS dimuon example.

### 4. Histogram accounting is explicit, but not detector or trigger validation

The candidate separately accounts for pairs below range, in regular bins, at/above the upper edge, and non-finite masses. The ROOT exporter writes regular-bin counts and metadata for underflow/overflow. The comparator checks corresponding totals and validates each CSV bin against the configured uniform grid.

These checks can detect implementation/configuration mismatches. They cannot establish trigger efficiency, validated-run selection, detector acceptance, or a physical interpretation of a feature in the spectrum.

### 5. Floating-point sensitivity is still a synthetic diagnostic

`scripts/estimate_bin_flip_sensitivity.py` compares two mass formulas on generated float32-like kinematics. It can inform numerical-risk analysis, but its results are not a ROOT-vs-Uproot comparison on actual CMS events and should not be presented as real-data parity evidence.

### 6. The ROOT runtime remains a reproducibility risk

The synthetic integration workflow has used the alpha-stage PyPI ROOT distribution `ROOT==0.1a12`. Pinning it improves repeatability of that CI environment but does not make the distribution production-stable. A supported ROOT installation/container should be tested against the same small synthetic fixtures before switching environments; the runtime change should be isolated from physics-method changes.

## Required gates before any real-data parity claim

1. Freeze the exact dataset record, file identity, tree name, branch schema, and input manifest.
2. Freeze the intended selection mode and verify it against the pinned reference source at the stated commit.
3. Use identical input bytes and the same entry-order prefix in both exporters.
4. Run a small bounded smoke test first; retain both metadata JSON files, CSVs, logs, and exit statuses.
5. Require the comparator to pass all provenance, cut-flow, histogram accounting, and bin-edge checks.
6. Investigate every mismatch; do not relax checks just to obtain a pass.
7. State clearly that a successful histogram parity test is a software/reconstruction validation only, not trigger-efficiency validation or a resonance result.

## Current conclusion

The repository has meaningful provenance and histogram-integrity safeguards, and the static comparison logic has a coherent intended contract. The key unresolved scientific gate is still an actual, bounded candidate/reference run on the declared CERN input, with the exact selection semantics and reference source independently confirmed. This audit did not execute that run and does not authorize or dispatch a larger workflow.
