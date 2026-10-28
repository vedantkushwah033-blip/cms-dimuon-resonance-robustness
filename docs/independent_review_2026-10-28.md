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

| Priority | Finding | Required action |
|---|---|---|
| High | CSV summaries were not linked to metadata | Add summary and exact CSV SHA-256 checks in exporter metadata |
| High | Both outputs could be truncated identically | Require exact event-prefix count in both metadata files |
| High | Real-data parity is unestablished | Run bounded workflow after validating dependency and provenance choices |
| Moderate | Reference ROOT distribution is alpha-stage | Prefer a supported, versioned conda-forge ROOT environment for reference validation |
| Moderate | Dependencies and action versions are not all pinned | Pin or record versions and preserve the runtime manifest |
| Moderate | Expected input hashes are not independently anchored | Verify file identity and store expected digest per record |
| Low | Stable mass formula and ROOT's direct four-vector calculation may differ at floating-point edges | Use synthetic sensitivity audit as context; investigate real-data differences rather than dismissing them |

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
