# Independent review of the CMS dimuon research branch — 2026-10-28

Reviewer: AI assistant; not a human expert review.

## Scope and evidence

The review concerns the bounded Run2012B/C dimuon histogram comparison workflow and the proposed follow-up statistical study. It separates source-level inspection, synthetic numerical tests, real-data validation, and scientific claims.

Both candidate and reference are expected to process the same input file and exactly the first 100,000 events, apply the same exactly-two-muon and opposite-charge selection, and produce the same 30,000-bin dimuon mass histogram over [0.25, 300) GeV. Exact integer parity is a sensible acceptance criterion if event selection, mass calculation, flow-bin semantics, and bin edges are genuinely matched.

## Evidence limits

- NumPy-only tests do not validate the Uproot/Awkward execution path.
- Synthetic ROOT integration does not establish parity on the CERN files.
- A local checksum repeated by multiple programs proves consistency among those programs, not identity with a published checksum.
- No trigger-efficiency claim is supported by this workflow; prescale, luminosity, and efficiency-denominator information are outside the current scope.

## Findings register

| Priority | Finding | Status / required action |
|---|---|---|
| High | CSV summaries were not linked to metadata | **Addressed in PR #5:** compare bin count, exact integer total, SHA-256 digest, and range against each exporter's metadata. Digest binding detects post-export substitution but does not prove exporter scientific correctness. |
| High | Both outputs could be truncated identically | **Addressed in PR #5:** comparator can require exact event-prefix counts independently for both outputs. |
| High | Real-data parity is unestablished | **Open blocker:** no bounded comparison of the target CERN files has been run by PR #3–#6. Obtain explicit operator approval before any large-data dispatch. |
| Moderate | Reference ROOT distribution is alpha-stage | **Open environment risk:** PyPI `root==0.1a12` is explicitly marked pre-release. ROOT's official install guidance recommends package-manager or precompiled distributions; evaluate a versioned conda-forge or official ROOT container setup before treating it as the scientific reference. |
| Moderate | Dependencies and action versions are not all pinned | **Open audit item:** inventory workflow actions and runtime dependencies, pin what is operationally appropriate, and preserve environment versions in artifacts. |
| Moderate | Expected input hashes are not independently anchored | **Open provenance risk:** a digest computed locally by both exporters proves they read identical bytes, not that those bytes match a separately published expected digest. |
| Low | Stable mass formula and ROOT's direct four-vector calculation may differ at floating-point edges | **Partly characterized synthetically:** PR #6 adds a conditional denominator for the rule-of-three bound and clearer output naming. It remains a synthetic NumPy comparison, not a ROOT-vs-NumPy observation on CMS data. |
| Moderate | CSV bin edges could be contiguous and span the correct endpoints while being nonuniform | **Addressed in PR #6:** when metadata configuration is supplied, every CSV edge is checked against the configured uniform grid within `1e-12 GeV`; a regression test covers a nonuniform two-bin grid. |

## Follow-up engineering review — PR #5/#6

The latest inspected draft, PR #6, adds per-bin comparison against the configured uniform histogram grid and corrects the synthetic sensitivity audit's conditional denominator. The Python tests/compileall/Ruff workflow and synthetic ROOT reference-exporter integration both passed on commit `086d7e16a58dc0114ba51f91c9922e528ee2b7b2` (workflow runs `40646864601` and `40646864756`). These are software checks only; the integration uses a synthetic fixture and does not establish numerical parity on CERN data. PR #6 remains draft/open/unmerged.

The current CSV integrity checks bind file bytes to exporter metadata, but they do not independently authenticate the CSV's scientific correctness. Likewise, matching locally computed input checksums across exporters is not an external provenance anchor. The workflow should continue to fail closed on missing/malformed metadata and report each validation layer separately.

## Synthetic numerical sensitivity

The script estimate_bin_flip_sensitivity.py compares the cancellation-resistant mass formula with a direct Cartesian E²−|p|² evaluation on synthetic float32-like inputs. It reports bin disagreements and a rule-of-three upper bound only when zero disagreements are observed. This is a numerical stress test, not an observation about CMS data. Its generator assumptions and the fact that ROOT itself is not run by this script must remain explicit.

## Statistical protocol proposal

Primary estimand: global false-positive probability for a window-scan dimuon search under background-only truths not represented by the fitted function family. Prespecify three comparators: fixed-order polynomial, order selected by an F-test, and discrete profiling over declared families with a parameter penalty. Calibrate a global threshold on matched null simulations; in every pseudo-experiment repeat the entire scan and selection and use the maximum local statistic.

Use development, validation, and held-out generator sets. Fix seeds, number of pseudo-experiments, fit-failure handling, and stopping rules in advance. Do not drop failed fits; report them and predefine their primary and sensitivity treatment. A 10,000-replicate scenario gives an approximate 95% binomial half-width of 0.0043 at alpha=0.05; paired comparisons need their own uncertainty estimates. This is a protocol proposal, not a preregistered or executed result.

## Go/no-go

- Bounded engineering validation: conditional go, after safeguards and user approval.
- Real-data parity: not established.
- Confirmatory statistical experiment: no-go until protocol freeze and real-data workflow audit.
- Publication novelty: possible narrow question, not established by a limited literature review.
