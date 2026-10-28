# PR #3 adversarial review — 2026-10-28

## Verdict

**Conditionally proceed to bounded engineering validation only.** Real-data parity for CERN Open Data records 31123 and 31129 is not established. This is an AI review, not an independent human physics/software review.

## Changes in this review branch

- Bind each exported histogram CSV's row count and exact integer sum to the corresponding metadata.
- Require candidate and reference CSV arguments together.
- Require candidate max_events and events_read, and reference max_events and events_total, to equal the prespecified 100,000-event prefix in the manual workflow.
- Add regression tests for exact integer accumulation, malformed counts, stale CSV totals, wrong bin counts, matched truncation, and incomplete CLI argument pairs.
- Add a synthetic floating-point bin-flip sensitivity script. It is explicitly not a substitute for real-data parity.

## Residual limitations

1. **Summary binding is not cryptographic identity.** Equal row count and total do not prove the CSV is the exact file produced alongside a metadata JSON. A foreign CSV with the same number of rows and sum can pass. A follow-up should have each exporter record the output CSV SHA-256 in its metadata, then compare that digest against the actual CSV bytes.
2. The current summary parser checks count syntax and required column names, but does not yet validate every bin edge, monotonicity, contiguity, or the CSV's full edge sequence against metadata.
3. The manual workflow still uses the alpha-stage PyPI ROOT distribution ROOT==0.1a12. A supported, versioned conda-forge ROOT reference is preferable before scientific interpretation.
4. A locally computed SHA-256 compared among shell and exporters is useful for internal consistency, but not an independently published checksum. Record a verified expected digest after validating the downloaded file identity.
5. cernopendata-client, xrootd, and GitHub Actions tags are not all pinned.
6. Records 31123/31129 have not been fetched and compared in this review. The CERN Open Data site was not independently inspected here.
7. The synthetic mass-formula experiment tests numerical sensitivity only. It does not establish trigger efficiency, a resonance, or a physics result.

## Protocol gate

The next scientific question should be frozen before large simulation: for a prespecified dimuon mass scan and several background-function selection rules, what is the global false-positive probability under held-out background-only generators outside the fitted family? The full scan and model selection must be repeated inside each pseudo-experiment. Local-window rejection rates cannot support a global false-positive claim.

Use a fixed sample size and prespecified failure handling; retain every pseudo-experiment, including fit failures. The 10,000-replicate proposal gives an approximate 95% binomial half-width of 0.0043 at a true rate of 0.05, before considering paired differences or multiple scenarios. Freeze the denominator, threshold calibration, held-out generator split, seeds, and stopping rule before running confirmatory simulations.

## Publication status

Educational/research software baseline in development. No real-data parity, global false-positive result, trigger claim, or publication novelty has been established.
