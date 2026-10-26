# Novelty gate: what must be new, and how we will test it

**Status: candidate research direction only. Originality is not established.**

## 1. Why the initial question is not yet enough

A broad study of polynomial order, fit-window choice, or spurious bumps would overlap substantially with existing dimuon-resonance-search literature. The 2019 CMS Open Data study by Cesarotti et al. explicitly describes local fits to dimuon spectra, polynomial background models, and choices of fit-window size. That work must be treated as a close predecessor, not a footnote.

The 2012 public spectrum record by Wunsch is primarily an outreach analysis and documents a known trigger-related structure near 30 GeV. Its record reports two files totalling 123.7 KiB and points to a reduced muon NanoAOD sample. It is a useful baseline/reproduction candidate, but it must not be assumed to be sufficient for a novel research-grade statistical study until the actual data schema and analysis scope are checked.

## 2. Candidate contribution to investigate—not claim

Investigate **selection-aware calibration of a local dimuon bump-hunt procedure when background-model selection is itself part of the analysis**. The key issue would not be “which polynomial fits best?” in isolation. It would be whether the *entire prespecified procedure*, including any allowed model-selection or diagnostic step, controls its null rejection rate on held-out generating scenarios.

A candidate design, subject to literature review and data feasibility:

1. Define a baseline local test and a small, scientifically justified set of candidate background families.
2. Compare a fixed-model procedure with a procedure that selects among those families using a predeclared rule.
3. Generate null samples under a baseline family and distinct smooth alternatives; include only physically/empirically justified scenarios.
4. Refit nuisance/background parameters in every pseudoexperiment using the actual planned fitting workflow.
5. Evaluate empirical type-I error at feasible nominal levels, interval coverage where meaningful, fit failures, and sensitivity to prespecified deviations.
6. Develop any diagnostic on development scenarios, then evaluate it unchanged on held-out scenarios.
7. Use the observed CMS spectrum to validate the data pipeline and contextualize limitations; do not treat a toy model as a detector-level truth model.

This is only a possible contribution. The literature audit may show that equivalent work already exists, or that the public data cannot support a credible connection to the real detector. If so, revise or stop the project rather than overstate novelty.

## 3. Falsifiable novelty questions

Before the main experiment, document answers with citations:

- Have prior studies already evaluated false-positive calibration after background-model selection in local bump hunts?
- Have they compared fixed and selected models under held-out smooth null generators with per-toy nuisance refitting?
- Are comparable studies already available for high-energy resonance searches, including toy Monte Carlo, bootstrap calibration, goodness-of-fit, spurious-signal studies, and look-elsewhere corrections?
- What precise decision or scientific inference would change because of our results?
- Can the proposed experiment be validated against known statistical cases independently of CMS data?

A novelty claim must cite the closest methods, explain the difference precisely, and state what the study does *not* establish.

## 4. Go/no-go gate

**Go** only if the literature review identifies a meaningful gap, the required data/method are feasible, and a protocol can be frozen before outcomes are inspected.

**Re-scope** if the gap is narrower than expected but a defensible methodological question remains.

**Stop** if the main experiment is already answered by equivalent published work, if necessary inputs are unavailable, or if the design relies on unsupported assumptions.

## 5. Evidence needed for a strong claim

- A related-work matrix with primary-source citations and explicit comparison dimensions.
- A frozen protocol, including primary estimand, alpha, test statistic, model-selection rule, failure handling, and held-out scenarios.
- Validated software with automated tests and independent cross-checks.
- Results with uncertainty intervals, all prespecified scenarios, failed-fit accounting, sensitivity analysis, and negative findings.
- Reproduction by a person other than the primary author if feasible; record what they actually checked.
- A clear distinction between model-based calibration evidence and claims about real CMS data.

**Do not describe this project as original, novel, peer-reviewed, or externally validated until the corresponding evidence exists.**
