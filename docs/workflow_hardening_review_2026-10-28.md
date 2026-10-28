# Workflow hardening review — 2026-10-28

## Changes proposed in this branch

This branch makes four narrowly scoped changes to the bounded CMS data-validation workflow:

1. **Input hash in both exporter metadata files.** The manual workflow passes `--sha256-input` to both the Uproot candidate and ROOT reference exporter. Each metadata output should therefore record the SHA-256 of the same local ROOT input; the workflow also retains the download manifest and checksum verification.
2. **Per-record failure isolation.** The manual workflow records download, schema, candidate, reference, histogram-comparison, and metadata-comparison exit statuses. A failed download for Run2012B should not prevent an attempt at Run2012C. If either exporter fails, comparison is marked as not run (status 125), not passed. Logs are retained in the artifact.
3. **Enforce input provenance in metadata comparison.** The candidate and ROOT reference metadata must each contain a valid 64-character hexadecimal SHA-256 and a positive integer input byte count. The checksums and byte counts must match; absent, malformed, or mismatched provenance fails the comparison with a machine-readable report and nonzero exit status. Tests cover matching and failure cases.
4. **Pin the PyPI ROOT distribution used by current CI.** Both workflows pin `ROOT==0.1a12` rather than resolving an unspecified latest version.

## Validation of this review branch

- Latest test-suite run for the provenance-validation changes, [40618697275](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40618697275), completed successfully. The Python 3.10, 3.11, and 3.12 jobs passed tests, compilation, and Ruff checks.
- Latest ROOT-reference integration run, [40618697262](https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40618697262), completed successfully, including the synthetic-data ROOT exporter test.
- These latest runs validate the PR's automated tests—including the new provenance regression cases—and synthetic integration only. They do **not** establish parity on CERN's real data.
- The manual workflow has **not** been dispatched by this branch, and no multi-gigabyte ROOT files were downloaded by these runs.
- The real-data comparison for records 31123 and 31129 remains **NOT ESTABLISHED** until the manual workflow is explicitly dispatched, completes, and its actual artifacts are independently inspected.

## Important limitation of the ROOT environment

The successful integration log warns that the PyPI ROOT distribution is alpha-stage and should not be relied on for production purposes. Pinning improves repeatability but does not remove that limitation. Before relying on ROOT output as a scientific reference, assess whether a supported, versioned ROOT container/environment is feasible and document the environment.

## Scope boundaries

The workflow is a bounded software-parity check on the first 100,000 events of one file from each record. It is not a full-record physics analysis, trigger-efficiency study, resonance discovery, or proof of novelty. Do not begin confirmatory pseudoexperiments solely because this workflow passes.
