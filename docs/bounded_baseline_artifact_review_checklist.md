# Bounded CMS baseline workflow: artifact review checklist

**Status:** review checklist; no bounded Run2012B/C spectrum result is claimed by this document.
**Purpose:** prevent a successful workflow launch, a schema report, or a partial scan from being mistaken for a validated physics reproduction.

## 1. Confirm the exact run

Before interpreting any output, record:
- workflow run URL, conclusion, branch, and head commit SHA;
- whether the run used the current `research-level-schema-audit.yml` workflow, not an older schema-only version;
- artifact name, creation time, expiry, and downloaded archive SHA-256;
- official CERN record ID, exact file name, byte size, and input SHA-256 for each period.

A prior artifact from an older workflow version is not evidence that newer steps ran. The workflow is manual-only; absence of a recent run means the new bounded spectrum/reference comparison has not been executed.

## 2. Review each Run2012B/C output separately

For each record, check the artifact contains:
- `schema_<record>.json` and a manifest row;
- candidate spectrum CSV and metadata;
- independent ROOT/RDataFrame reference histogram CSV and metadata;
- `comparison_<record>.json`, comparison stdout, and exit-status file.

Do not pool Run2012B and Run2012C counts or treat one file per period as a full-period exposure sample.

## 3. Interpret comparison outcomes

- **Exit status 0:** the comparator reports exact bin-edge and integer-count parity for the two bounded outputs. This is a strong implementation check for that exact input prefix and selection; it is not full-data reproduction or physics validation.
- **Exit status 2:** histogram edges match but at least one bin count differs. Inspect every reported differing bin and compare total counts, cut flow, mass calculations, selection and ROOT histogram semantics. Do not loosen the exact-parity criterion merely to obtain a green workflow.
- **Other nonzero status / missing comparison JSON:** the comparison did not complete successfully. Inspect logs and preserve the failure; do not describe it as a physics discrepancy until tool/runtime failure is excluded.
- **Exact parity on the first 100,000 entries:** remains a bounded smoke test. Full-data parity requires processing all entries of the same reference input and satisfying the metadata audit's full-scan conditions.

## 4. Checks before any trigger-related claim

The current comparison is a dimuon-spectrum baseline, not a trigger-efficiency analysis. Before discussing trigger efficiencies, prescales, or trigger-induced acceptance, independently establish:
- certified run/lumisection selection and its authoritative source;
- the relevant HLT path versions and period-specific meanings;
- prescale and data-taking conditions;
- a valid independent denominator and numerator definition;
- treatment of overlap, matching, and event selection;
- uncertainties and validation against appropriate CMS documentation.

A branch's presence in the file is not evidence that these conditions are satisfied.

## 5. Decision rule

Proceed to a full reference reproduction only after the bounded run is reproducible and any discrepancies are understood. Proceed to the confirmatory statistical study only after (a) the baseline and estimand are frozen, (b) a focused literature comparison identifies a specific unresolved question, and (c) scenario distributions, comparators, thresholds, random-seed policy, Monte Carlo precision targets, and failure handling are committed before confirmatory runs.

**Non-claims:** this checklist does not establish a new resonance, a detector defect, trigger efficiency, discovery significance, novelty, peer review, or admissions impact.
