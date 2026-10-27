# Execution Plan: From Repository Scaffold to Defensible CMS Dimuon Result

**Status date:** 2026-10-27  
**Branch:** `research-plan/initial-protocol`  
**Decision:** Continue bounded validation; do not start confirmatory simulations.

## Executive decision

The project has a useful, tested software scaffold and a successful 10,000-entry smoke test on the official CMS outreach file. That is evidence that a bounded input-processing path works, not evidence of a physics result. One file each from the Run2012B and Run2012C DoubleMuParked records has passed a schema audit. The required numerical, bin-by-bin comparison between the candidate implementation and an independent reference has **not** been established.

The current candidate research topic—false-positive calibration of a complete dimuon bump-hunt pipeline under background misspecification and model selection—has meaningful overlap with existing literature. Novelty is not established. No discovery, trigger-efficiency, or publication-readiness claim is justified.

## Work that can proceed without local access

1. Keep the methods-level literature comparison bounded and claim-focused. For each closest paper, extract the tested procedure, null/data-generating assumptions, test statistic, treatment of model choice, scan/look-elsewhere correction, evaluation metrics, and stated limitations from the paper itself. Mark unavailable details as unknown rather than infer them.
2. Keep the code and protocol separate from scientific conclusions. Existing synthetic tests validate specific software behaviors only.
3. Prepare the independent-reference acceptance checklist and artifact schema so the next data run has a deterministic pass/fail decision.
4. Do not change the default branch or merge the draft PR merely to make a manual workflow available. Review the PR and choose an execution path deliberately.

## Required gates, in order

### Gate 1 — Provenance and exact input
For each chosen file, preserve official record URL, exact filename, byte size, SHA-256, tree name, entry count, download command/tool version, and schema report. A filename or extension is not proof of ROOT format. The 10,096-byte local download described in the chat is not verified as a ROOT file and must not be used.

**Pass condition:** the downloaded file opens as ROOT, its checksum and provenance are recorded, and the expected branches/types are present.

### Gate 2 — Bounded real-data processing
Run a fixed, bounded number of entries from one checksum-verified Run2012B and one Run2012C DoubleMuParked file. Preserve logs and outputs. Confirm event cut flow, opposite-charge pair accounting, finite-mass handling, bin edges, and metadata.

**Pass condition:** run completes without hidden failures; all counts reconcile; the report states exactly which files and entries were processed.

### Gate 3 — Independent numerical parity
Use the independent ROOT/RDataFrame reference exporter and candidate implementation on the same entries, event selection, mass range, bin count, and boundary convention. Compare every bin count exactly and histogram edges within the predeclared tolerance; compare cut-flow and selection metadata independently. Preserve artifacts even on failure.

**Pass condition:** exact integer bin-count agreement, edge agreement within the declared tolerance, and metadata/cut-flow agreement. Any discrepancy blocks downstream statistical claims until diagnosed.

### Gate 4 — Scientific selection and estimand
Do not claim trigger efficiency from HLT branch presence alone. Establish run-dependent trigger path semantics, data-quality/lumisection treatment, prescale/luminosity handling, and a defensible denominator if trigger claims are retained. If those cannot be established, explicitly drop trigger-efficiency claims and narrow the study.

Choose one primary estimand before simulation. For a full scan, global type-I error must be defined through the maximum test statistic over the exact prespecified scan and model-selection procedure. Local fixed-window rejection, interval coverage, and diagnostic false-alarm rate are separate outcomes.

### Gate 5 — Novelty and fair comparator
Complete methods-level comparison against the closest prior work, especially Williams (2017) and Cesarotti et al. (2019), and relevant later bump-hunting/anomaly methods. State what is identical, what differs, and why the difference matters. If no specific gap remains after this comparison, pivot or stop rather than relabel a known method as novel.

### Gate 6 — Confirmatory simulation preregistration
Only after Gates 1–5 pass, freeze:
- primary estimand and test statistic;
- scan range, grid, candidate models and model-selection rule;
- null-generating families and development/calibration/held-out split;
- credible comparator and paired design where appropriate;
- failed-fit and invalid-toy accounting;
- replicate count justified by Monte Carlo uncertainty;
- stopping rule, software versions, random seeds and output artifacts.

Every pseudoexperiment must rerun the entire analysis pipeline, including selection/model choice and the scan, if the target is global calibration. Do not use the same scenarios to tune and claim held-out performance.

## Immediate blockers

- No verified local research-level ROOT file has been made available to the analysis environment in this session.
- The bounded outreach smoke test is not numerical reference parity.
- The revised manual research-level baseline workflow exists on the unmerged branch and has not been run; workflow-dispatch availability is constrained because it is not on the default branch.
- The research question, primary estimand, comparator, and held-out null population remain provisional.
- Latest-head CI must be checked on the exact commit; missing status entries are inconclusive, not passes.

## User input needed

**No immediate user action is needed for the repository-side literature and protocol work.** When the workflow reaches the real-data gate, one of these will be needed:
1. authorization to merge a reviewed, narrowly scoped workflow-enabling change to the default branch; or
2. the user runs the documented bounded procedure locally and provides its text/artifacts.

Do not ask the user to download more data until the execution route and exact target file are chosen. Never request passwords, access tokens, or account credentials.

## Publication and admissions boundaries

A polished repository, transparent limitations, reproducible code, an independently validated result, and external expert feedback can strengthen a research portfolio. They do not guarantee journal acceptance, transfer credit, or admission to any university. Do not describe this as a discovery or as publication-ready before the evidence supports that language.
