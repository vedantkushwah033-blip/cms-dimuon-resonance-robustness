# Workflow hardening review — 2026-10-28

## Changes proposed in this branch

This branch makes three narrowly scoped changes to the bounded CMS data-validation workflow:

1. **Input hash in both exporter metadata files.** The manual workflow now passes `--sha256-input` to both the Uproot candidate and ROOT reference exporter. This causes each exporter to record the SHA-256 of the local ROOT input, allowing the comparison evidence to identify the same exact file. The workflow separately retains the download manifest and checksum verification.
2. **Per-record failure isolation.** The manual workflow records download, schema, candidate, reference, histogram-comparison, and metadata-comparison exit statuses. A failed download or export for Run2012B no longer automatically prevents attempting Run2012C. If either exporter fails, comparison is explicitly marked as not run (status 125) rather than being mistaken for a pass. Logs are retained in the uploaded artifact.
3. **Pin the PyPI ROOT distribution used by current CI.** The latest successful integration run installed `ROOT==0.1a12`; both the manual workflow and integration workflow now pin that distribution instead of resolving an unspecified latest version.

## Important limitation of the pin

The successful integration log explicitly warns that this PyPI ROOT distribution is in alpha stage and should not be relied on for production purposes. Pinning makes the environment more repeatable, but it does not remove that upstream limitation. The workflow records the actual ROOT runtime version. Before making a scientific claim, review the warning and consider moving to a supported, versioned ROOT container/environment if practical.

## Validation state

- This change is on a review branch and has not been merged.
- The manual workflow has **not** been dispatched by this change.
- No large ROOT file was downloaded by this change.
- The latest earlier test-suite and synthetic ROOT integration runs passed on commit `1a03a01411a0e133820c0bf3341a8a27863539f0`. Those runs predate these workflow edits and therefore do not validate the revised workflow.
- Passing synthetic integration tests is not real-data numerical parity.
- The real-data comparison for records 31123 and 31129 remains NOT ESTABLISHED until the revised manual workflow is explicitly dispatched, completes, and its actual artifacts are independently inspected.

## Scope boundaries

The workflow is a bounded software-parity check on the first 100,000 events of one file from each record. It is not a full-record physics analysis, trigger-efficiency study, resonance discovery, or proof of novelty. Do not begin confirmatory pseudoexperiments solely because this workflow passes.
