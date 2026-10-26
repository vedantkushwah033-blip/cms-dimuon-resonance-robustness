# Next Experiment: Stop/Go Decision Record

**Status:** Proposed decision framework; no real-data run or statistical result is asserted here.

## Current decision

**GO:** inspect and validate a real-data baseline with a limited, explicitly identified CMS file.

**NO-GO:** launching the confirmatory Monte Carlo campaign or claiming a trigger-related finding before data provenance, selection semantics, and the novelty gap are resolved.

## Gate 1 — input and provenance

Proceed only when the exact official record and file are documented, the file checksum is recorded, the ROOT tree and required branches are inspected, and branch meanings/units are supported by authoritative documentation. If a required variable or trigger/prescale detail is absent, narrow the question or select another justified data source; do not infer it from names alone.

## Gate 2 — baseline agreement

Run a small sample first. Check event selection, pair construction, invariant-mass calculations, histogram edge conventions, and accounting identities. Then run the full intended sample if feasible. Compare against the published reference using the same selection, range, binning, and normalization wherever those are available.

A visual resemblance alone is not sufficient. If the reference only supplies a plot, record that limitation and do not claim exact numerical reproduction.

## Gate 3 — novelty

Compare the proposed estimand, generating distributions, fitted models, selection procedure, diagnostic, and validation design against the closest published studies. A different implementation or more simulations alone is not a novel contribution. If no clear gap remains, revise the question before confirmatory experiments.

## Gate 4 — method and pilot

Test the full fit-and-test procedure on known cases. Record convergence, boundary solutions, invalid covariance estimates, and failed fits. Use a pilot only to estimate runtime, tune implementation for correctness, and set a justified simulation budget. Do not report pilot outcomes as confirmatory evidence.

## Gate 5 — protocol freeze and confirmatory run

Before the main run, version the complete scenario matrix, test statistic, alpha, diagnostic threshold, model-selection rule, RNG/seed scheme, replicate count, failure policy, and held-out scenarios. Preserve per-replicate outputs and run metadata.

## Gate 6 — interpretation

Report all prespecified scenarios, including unfavorable results. Distinguish Monte Carlo uncertainty from model uncertainty. Synthetic acceptance-like distortions are not measurements of real trigger performance. No discovery or global-significance claim is permitted unless the relevant scan and look-elsewhere calibration are separately specified and validated.

## Stop conditions

Stop and investigate if:
- The reference baseline cannot be reconstructed from documented requirements;
- the results depend materially on undocumented selection assumptions;
- fit failures are frequent or scenario-dependent;
- held-out diagnostic performance is no better than a clearly defined baseline;
- the proposed novelty claim is already addressed by prior work;
- independent reviewers identify unresolved validity threats.

An inconclusive result is preferable to an unsupported positive conclusion.
