# PR #3 adversarial review — 2026-10-28

## Verdict

**Conditionally proceed to bounded engineering validation only.** Real-data parity for CERN Open Data records 31123 and 31129 is not established. This is an AI review, not an independent human physics/software review.

## Changes in this review branch

- Bind each exported histogram CSV's row count, exact integer sum, and SHA-256 to the corresponding metadata.
- Require candidate and reference CSV arguments together.
- Require candidate max_events and events_read, and reference max_events and events_total, to equal the prespecified 100,000-event prefix in the manual workflow.
- Add regression tests for exact integer accumulation, malformed counts, stale CSV totals, wrong bin counts, matched truncation, and incomplete CLI argument pairs.
- Add a synthetic floating-point bin-flip sensitivity script. It is explicitly not a substitute for real-data parity.

## Residual limitations

1. CSV SHA-256 binding is now included: both exporters record the exact output CSV digest, and the comparator verifies the actual CSV bytes against metadata. This protects against post-export substitution, though it cannot independently prove the exporter generated scientifically correct values.
2. **Updated by PR #6:** the summary parser validates required columns, integer count syntax, finite/increasing and contiguous edges, expected bin count, and every bin edge against the configured uniform grid. A regression test rejects a contiguous nonuniform grid with the correct endpoints.
3. The manual workflow still uses the pre-release PyPI ROOT distribution `ROOT==0.1a12`. PyPI explicitly labels it a pre-release, and the official ROOT installation guidance describes pip installation as alpha-mode; a supported, versioned conda-forge or official ROOT container environment should be evaluated before scientific interpretation.
4. A locally computed SHA-256 compared among shell and exporters is useful for internal consistency, but not an independently published checksum. Record a verified expected digest after validating the downloaded file identity.
5. cernopendata-client, xrootd, and GitHub Actions tags are not all pinned.
6. Records 31123/31129 have not been fetched and compared in this review. The CERN Open Data site was not independently inspected here.
7. The synthetic mass-formula experiment tests numerical sensitivity only. It does not establish trigger efficiency, a resonance, or a physics result.

## Follow-up adversarial fixes — 2026-10-28

A second pass found two concrete validation defects and patched them on the follow-up audit branch:

- **Histogram edge contract:** CSV validation previously checked finite/increasing edges, contiguity, total range, and bin count, but a contiguous nonuniform grid could still match the same endpoints and evade metadata validation if both exporters produced it. The parser now optionally checks every bin's low/high edge against the configured uniform grid and expected bin count, with the existing absolute tolerance. A regression test constructs a contiguous but nonuniform two-bin histogram and requires rejection.
- **Sensitivity bound denominator:** the synthetic bin-flip script counted bin disagreements only when both mass formulas placed a pair inside the histogram range, but used the stable-formula in-range count as the denominator for the rule-of-three bound. The denominator now explicitly counts pairs in range under both formulas, and the output label states that the bound is conditional on both formulas being in range. A regression test checks the denominator and the zero-observed-disagreement rule.
- **CSV snapshot integrity:** the comparator previously parsed a CSV through one file read and computed its SHA-256 through a second read. A concurrent replacement could therefore make the digest refer to bytes different from those summarized. It now reads bytes once, hashes that snapshot, and parses the same snapshot; a regression test simulates mutation at read time.
- **Output/input path collision:** the comparator already refused to overwrite either metadata JSON, but did not protect candidate/reference CSV inputs. Supplying a CSV path as `--output` could destroy an input artifact after parsing. The output-path guard now protects both metadata and optional CSV inputs, and a regression test asserts the original CSV bytes remain unchanged.

These code-level fixes are on the separate PR #6 branch, whose inspected head is `51faf4b9a5ee1dec286aa651f94b95f0116e3abc`. Latest-head Python tests, compileall, and Ruff passed on Python 3.10–3.12 in workflow run `40671389441`; the synthetic ROOT exporter integration, including the non-finite-kinematics rejection test, passed in run `40671389432`. These checks validate software behavior and synthetic fixtures only, not real-data parity. The sensitivity calculation remains a synthetic numerical stress test, not a direct ROOT-vs-NumPy comparison and not a CMS measurement.

## Protocol gate

The next scientific question should be frozen before large simulation: for a prespecified dimuon mass scan and several background-function selection rules, what is the global false-positive probability under held-out background-only generators outside the fitted family? The full scan and model selection must be repeated inside each pseudo-experiment. Local-window rejection rates cannot support a global false-positive claim.

Use a fixed sample size and prespecified failure handling; retain every pseudo-experiment, including fit failures. The 10,000-replicate proposal gives an approximate 95% binomial half-width of 0.0043 at a true rate of 0.05, before considering paired differences or multiple scenarios. Freeze the denominator, threshold calibration, held-out generator split, seeds, and stopping rule before running confirmatory simulations.

## Publication status

Educational/research software baseline in development. No real-data parity, global false-positive result, trigger claim, or publication novelty has been established.
