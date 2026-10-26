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


## 6. Literature audit update — 2026-10-27

A targeted follow-up search reinforces that the current idea must be narrowed before it can be called novel.

### Closest methods to compare directly

1. **Williams (2017), “A novel approach to the bias-variance problem in bump hunting,” JINST 12 P09034.** This paper directly studies data-driven background-model selection and uncertainty from model choice, and evaluates bias and interval coverage. It is a central comparator, not merely background reading. DOI: https://doi.org/10.1088/1748-0221/12/09/P09034.
2. **Cesarotti et al. (2019), “Searching in CMS open data for dimuon resonances with substantial transverse momentum,” Phys. Rev. D 100, 015021.** The analysis uses local mass windows, polynomial backgrounds, and explicit choices of polynomial degree and window width; it also discusses ringing and trigger turn-on effects. DOI: https://doi.org/10.1103/PhysRevD.100.015021.
3. **Algeri (2020), “Detecting new signals under background mismodeling,” Phys. Rev. D 101, 015003.** This work directly treats inference under background mismatch and the risk that misspecification inflates false discoveries. DOI: https://doi.org/10.1103/PhysRevD.101.015003.
4. **Volkovich et al. (2022), “A data-directed paradigm for BSM searches: the bump-hunting example,” Eur. Phys. J. C.** The paper offers a different data-directed strategy for locating regions of interest; the proposed study should clarify whether it evaluates the same inferential target or a materially different one. DOI: https://doi.org/10.1140/epjc/s10052-022-10215-1.
5. **Hallin et al. (2023), “Resonant anomaly detection without background sculpting,” Phys. Rev. D 107, 114012.** This work addresses background sculpting in enhanced bump hunts. It is particularly relevant if any proposed diagnostic or selection depends on auxiliary variables or event selection. DOI: https://doi.org/10.1103/PhysRevD.107.114012.
6. **Recent Gaussian-process background modelling literature (2025).** A current GP-based background-estimation study evaluates background-only samples, goodness-of-fit and pseudoexperiment ensembles, while noting that global fit diagnostics can miss local biases. This further weakens any claim that “use pseudoexperiments to test background reliability” is novel by itself. DOI: https://doi.org/10.1140/epjc/s10052-025-14574-3.

### Narrower hypothesis worth testing

A potentially defensible question is not whether misspecification can hurt bump hunts; that is established. It is whether a **predeclared calibration audit of the complete model-selection-plus-scan pipeline** can provide useful, quantified guarantees or warning rates under a specified and independently held-out class of null generators, compared fairly with existing uncertainty-envelope, spurious-signal, goodness-of-fit and pseudoexperiment approaches.

This is still only a hypothesis. Before proceeding, build a row-by-row related-work table comparing each paper's:
- inferential target (local p-value, global type-I error, signal-strength bias/coverage, limit coverage, or diagnostic warning rate);
- treatment of model selection and nuisance refitting;
- scan/look-elsewhere calibration;
- background-misspecification families;
- use of independent held-out generators;
- failure-rate accounting and uncertainty on estimated operating characteristics;
- real-data validation requirements.

A gap must be stated as a precise difference on these dimensions and supported by the papers themselves. If the literature already contains an equivalent design, abandon this novelty claim and select a narrower question.

### Scope correction

The Run2012B/C schema audit and bounded spectrum workflow are engineering/validation tasks. They do not validate a detector-level acceptance model. Unless the project obtains authoritative run/lumisection certification, path-specific trigger semantics and prescales, and a valid efficiency denominator, all acceptance-like perturbations must remain explicitly synthetic and the primary conclusions must be framed as statistical-method results rather than claims about CMS trigger performance.

### Decision after this update

**Continue literature comparison and baseline validation. Do not launch confirmatory pseudoexperiments yet.** The precise gap, estimand, comparator implementations, null generators, and target Monte Carlo precision are not frozen.
