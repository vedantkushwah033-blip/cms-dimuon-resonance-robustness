# Official outreach ROOT smoke-test result — 2026-10-26

**Status: PASS for bounded data-access and pipeline smoke test only.**  
**Not a full-data reproduction, physics validation, trigger study, or novelty result.**

## Execution record

- GitHub Actions run: https://github.com/vedantkushwah033-blip/cms-dimuon-resonance-robustness/actions/runs/40372505488
- Code commit tested: `8ead6521c726442f8766433554e709186ed2426a`
- Trigger: scoped push to `research-plan/initial-protocol`
- Workflow: `.github/workflows/official-data-smoke-test.yml`
- Input: CERN CMS Open Data outreach ROOT file at the official `root://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root` path associated with https://opendata.cern.ch/record/12341
- Tree: `Events`
- Total tree entries reported by Uproot: 61,540,413
- Events read: first 10,000 entries in file order (not a random sample)
- Selection: exactly two reconstructed muons, then opposite-charge pair
- Event limit: 10,000, enforced by workflow
- Remote access: schema inspection and spectrum reconstruction both completed successfully using XRootD-backed Uproot access and numeric entry-count chunking.
- Artifact: `official-data-smoke-test` attached to the GitHub Actions run above.

## Observed schema facts

The schema inspector found the required muon kinematics and charge branches. Their reported types were `float[]` for `Muon_pt`, `Muon_eta`, `Muon_phi`, and `Muon_mass`; `int32_t[]` for `Muon_charge`; and `uint32_t` for `nMuon`.

The inspector found **no trigger-related branch-name candidates**, no event-identity branch group (`run`, `luminosityBlock`, `event`), and none of the listed muon quality/isolation candidate branches. This is direct file-level evidence that this reduced outreach file does not support the intended trigger-aware or quality-selection analysis as currently specified. The absence of candidate names is not a general statement about other CMS datasets.

## Bounded smoke-test accounting

| Quantity | Observed value |
|---|---:|
| Events read | 10,000 |
| Events with exactly two muons | 5,750 |
| Events with an opposite-charge pair | 4,504 |
| Opposite-charge pairs total | 4,504 |
| Pairs below 0.25 GeV | 24 |
| Pairs in the configured histogram range | 4,478 |
| Pairs at or above 300 GeV | 2 |
| Non-finite pair masses | 0 |

The accounting invariant holds: 24 + 4,478 + 2 + 0 = 4,504. Under the exactly-two-muon selection, each opposite-charge event contributes one pair. These values are a software smoke-test cut flow over the first 10,000 entries, not physics yields for the complete dataset.

## Failure-and-repair trail

The first attempts were useful diagnostics, not passes:
1. The first push-triggered run failed before data access because the manual-dispatch input was empty for a push event. The workflow now defaults the limit to 10,000 when no manual input exists.
2. The next run identified the missing `fsspec-xrootd` adapter. The `remote` optional dependency now includes it.
3. The following run successfully inspected the schema but failed during iteration because Uproot's memory-size chunk estimator reached an XRootD read that raised `TypeError: integer argument expected for offset`. The workflow now passes `--step-size 1000`; the CLI parser converts numeric values to integer entry counts. The subsequent run passed both schema inspection and the bounded reconstruction.

## What this result does and does not establish

Established:
- The official outreach ROOT file is reachable from GitHub Actions using the configured XRootD stack.
- The expected `Events` tree and required branches are present.
- The bounded 10,000-entry pipeline completes and produces schema, histogram, plot, and metadata artifacts.
- The implemented event/pair accounting is internally consistent for this smoke-test run.

Not established:
- Full 61.5-million-entry processing.
- Numerical bin-by-bin agreement with the official ROOT reference.
- Correctness of every reconstructed invariant mass relative to ROOT near histogram-bin boundaries.
- Trigger efficiency, trigger prescale modelling, muon quality selection, luminosity normalization, detector-level calibration, or suitability for a new-physics search.
- Research novelty or a publishable new result.

## Next gate

1. Preserve this run as the successful software smoke-test baseline.
2. Add a controlled numerical comparison against the official reference on the same event subset or a small local fixture, with an explicit tolerance and bin-boundary tests.
3. Before any full-file run, decide whether it is useful: the outreach sample lacks trigger and quality-selection candidates needed for the proposed trigger-aware scientific question.
4. Inspect the separate research-level Run2012B/C records and exact file schemas independently. Do not infer their schemas from this outreach result.
5. Keep the PR in draft until the latest test matrix, reference integration, and scope review are complete.

