# Software-validation gap audit: baseline dimuon reconstruction

**Date:** 2026-10-27  
**Status:** source-code review only; not a successful real-data validation  
**Branch:** `research-plan/initial-protocol`

## Scope and evidence

Reviewed the current `scripts/reproduce_dimuon_spectrum.py`, `src/cms_dimuon_robustness/nanoaod.py`, and `tests/test_nanoaod.py` on this branch. This is a static review of the visible source and tests. It does not mean the current branch was executed, that CI passed on the latest commit, or that an official ROOT file was successfully processed.

## What the current code already handles

- Requires the declared tree and branches `nMuon`, `Muon_pt`, `Muon_eta`, `Muon_phi`, `Muon_mass`, and `Muon_charge`.
- Checks agreement between `nMuon` and the per-event `Muon_pt` collection length.
- Checks per-event lengths for the kinematic and charge collections before calculating masses.
- Rejects charge values outside {-1, +1}; checks finite negative transverse momenta and masses.
- Promotes common float32 NanoAOD kinematics to float64 and uses a cancellation-resistant invariant-mass expression.
- Separates event counts from pair counts and asserts a pair-accounting invariant across below-range, in-range, overflow, and non-finite values.
- Writes histogram CSV and metadata with input, software versions, selection mode, counts, and commit when discoverable.
- Has synthetic tests for charge selection, low multiplicity, non-finite kinematics, cross-implementation agreement, invalid charges, mismatched branches, and float32 precision.

These are useful safeguards, but synthetic unit tests are not numerical reproduction of a reference analysis.

## Highest-priority validation gaps

### P0 — numerical reference parity

1. Run the official reference and project code on the **same small, checksum-identified ROOT file**, same tree, same event order, and same exact selection.
2. Compare selected-event counts, opposite-charge pair counts, mass values for a fixed sample of events, and histogram bins. A visual plot match is insufficient.
3. Explicitly document whether the public example's reference mass calculation uses the same muon mass, charge predicate, and four-vector convention. Resolve differences rather than fitting around them.
4. Test histogram boundary semantics: just below minimum, exactly minimum, just below maximum, exactly maximum, above maximum, NaN, and ±infinity.
5. Check the chunked result is invariant to chunk size and event limit. Compare a single-chunk run with multiple chunk sizes.

### P0 — selection and data-schema contracts

1. Add synthetic tests where `nMuon` disagrees with `Muon_pt`, and where `Muon_eta`, `Muon_phi`, `Muon_mass`, or `Muon_charge` has a different per-event length.
2. Test an event with exactly two same-sign muons: the event passes the multiplicity cut but contributes zero opposite-charge pairs. Ensure the cut-flow wording and counts remain unambiguous.
3. Verify the selected tree and branch names/types against each official file actually used. A NanoAOD-like format is not necessarily identical to every CMS ROOT record.
4. Test missing tree, each missing required branch, empty tree, zero-entry file, and unreadable/corrupt input; errors should be actionable and should not leave a misleading success metadata file.

### P1 — numerical stability and physical-domain edge cases

1. Add reference checks for extreme but valid eta, high-pT nearly collinear muons, back-to-back muons, zero pT, zero mass, and wrapped azimuth differences.
2. Define policy for non-finite eta/phi and infinite values; currently non-finite mass is visible to histogram accounting, but the code should not be interpreted as validating all malformed input semantics.
3. Add randomized property tests comparing the invariant-mass implementation with an independently implemented four-vector reference over a declared physical range.
4. Check that numerical tolerances are justified and report worst absolute/relative discrepancy, not only a pass/fail assertion.

### P1 — reproducibility and output integrity

1. Record the exact CERN record and file identifier, download/portal checksum, local SHA-256, exact command, environment lock/export, and Git commit in the run artifact.
2. Add a run identifier and ensure output files cannot silently overwrite an earlier run without an explicit decision.
3. Test output metadata serialization and histogram-count dtype/range for large samples.
4. Preserve the full command output and exit status. A metadata JSON file alone cannot prove that every run stage completed as intended.

## Scientific boundary

The current script reconstructs a simple opposite-charge dimuon spectrum. It does **not** establish trigger efficiency, prescale correction, certified luminosity, object-quality selection, background-model validity, a resonance excess, local/global significance, or publication novelty. Those are separate questions requiring documented sources and dedicated validation.

## Recommended next action

Do not add a bump-hunt or run a large pseudoexperiment campaign yet. First obtain a valid small official ROOT file, run the schema check and bounded spectrum script, then compare numerical output to the exact reference example. If the file cannot be downloaded or is not a real ROOT file, record the error and stop; do not substitute a guessed input. No new file is required from the user unless the official download fails again and we need the exact error text or a verified local file path.