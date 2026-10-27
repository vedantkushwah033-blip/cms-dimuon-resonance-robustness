# Literature-gap checkpoint: local dimuon bump-hunt calibration

**Date:** 2026-10-27  
**Status:** desk-review checkpoint only; no data result, novelty claim, or publication claim.

## Decision

**Do not launch the confirmatory Monte Carlo campaign yet.** The current candidate question—whether a data-driven background-model selection step changes the null rejection rate under smooth-background misspecification—is statistically sensible, but its broad form is not demonstrably novel. The closest existing work directly covers background-model choice and uncertainty in bump hunting, and newer resonance-search methods make a generic “compare models under stress” study even less distinctive.

The next defensible step is to finish a claim-by-claim literature matrix and only then freeze a narrower estimand. A different implementation, more toys, or use of CMS Open Data alone does not establish originality.

## Closest work and consequences for our design

| Work | Relevant established scope | Consequence for this project |
|---|---|---|
| Williams, *A novel approach to the bias-variance problem in bump hunting*, JINST 12 (2017) P09034, DOI [10.1088/1748-0221/12/09/P09034](https://doi.org/10.1088/1748-0221/12/09/P09034) | Studies data-driven background-model selection, bias/variance, uncertainty assignment, and interval coverage in bump hunting. | A basic fixed-model versus selected-model comparison, or a generic coverage study, is not enough. Identify a specific unaddressed procedure, estimand, or failure mode before proceeding. |
| Cesarotti et al., *Searching in CMS open data for dimuon resonances with substantial transverse momentum*, Phys. Rev. D 100 (2019) 015021, DOI [10.1103/PhysRevD.100.015021](https://doi.org/10.1103/PhysRevD.100.015021) | Applies local dimuon bump hunting to CMS Open Data, using polynomial background fits, local windows, and cross-checks of model/window choices; discusses ringing and trigger-turn-on limitations. | Rebuilding a dimuon mass plot or varying polynomial order/window is primarily a reproduction/teaching exercise unless a new statistical question is independently justified. Do not claim the public sample establishes trigger performance. |
| *Automatizing the search for mass resonances using BumpNet*, JHEP (2025), DOI [10.1007/JHEP02(2025)122](https://doi.org/10.1007/JHEP02(2025)122) | Uses a learned approach to predict bump-hunt significance distributions across histogram configurations and evaluates against idealized likelihood-ratio tests. | A broad “automate model choice / improve bump-hunt calibration” framing risks overlap with contemporary algorithmic approaches. A proposed method must be compared on matched tasks and metrics, not just mentioned. |
| *Robust resonant anomaly detection with NPLM*, EPJC (2025), [journal article](https://link.springer.com/article/10.1140/epjc/s10052-025-14759-w) | Studies NPLM-based approaches for resonant anomaly detection, including integration with sliding-window bump hunts and hyperparameter/threshold sensitivity. | Hyperparameter selection and variance of anomaly-search procedures are active topics. Do not frame threshold sensitivity as novel without checking the exact method and baselines. |
| Hallin et al., *Resonant anomaly detection without background sculpting*, Phys. Rev. D 107 (2023) 114012, DOI [10.1103/PhysRevD.107.114012](https://doi.org/10.1103/PhysRevD.107.114012) | Introduces LaCATHODE for enhanced bump hunts and evaluates background sculpting behavior. | If the project expands beyond one-dimensional mass fits into auxiliary-feature/anomaly selection, background sculpting and selection-induced distortions become mandatory related work. |

## What is—and is not—supported today

Supported:
- A reproducible, carefully tested implementation of a dimuon spectrum pipeline is a useful software/research foundation.
- Synthetic pseudoexperiments can answer a precisely defined statistical question about the specified generating and fitting procedures.
- The observed CMS spectrum can serve as a pipeline/reference check only after exact inputs, selections, and numerical comparison are documented.

Not supported:
- That the project has found a new resonance or any new physics.
- That a 30 GeV feature is a resonance; the outreach material identifies a known trigger/data-taking effect.
- That synthetic smooth-background experiments reproduce detector-level CMS behavior.
- That a new contribution exists merely because the code is independent or the simulation count is large.
- That a trigger-efficiency study is feasible without verified event-level trigger semantics, run-dependent path behavior, prescale/luminosity treatment, data-quality selection, and a defensible denominator.

## Candidate route to a defensible contribution

Before choosing a main experiment, complete a literature matrix with one row per closest paper and these fields:

1. Exact inferential target: local p-value calibration, global/scan calibration, signal-strength bias, interval coverage, or discovery power.
2. Whether model selection, fit-window selection, or diagnostic selection is included inside each pseudoexperiment.
3. Null-generating distributions and whether held-out generators are used.
4. Whether nuisance parameters are refit for every toy.
5. Treatment of failed fits, boundary solutions, and invalid uncertainty estimates.
6. Validation method, uncertainty on estimated rejection rates, and benchmark code/data availability.
7. The precise difference that remains after matching the prior paper's procedure and metrics.

A possible methodological question is whether *a predeclared, fail-closed analysis pipeline* maintains nominal rejection rates when fit failures and model-selection decisions are included in the full repeated procedure, evaluated on held-out generators. This is **only a hypothesis for literature review**, not a novelty claim; it may already be covered by prior work.

If the matrix shows that this is already answered, narrow the scope to a transparent reproducibility/benchmarking report or stop the research claim. If no defensible held-out generator can be motivated from data or literature, do not present arbitrary mathematical distortions as physically realistic CMS backgrounds.

## Gate before confirmatory simulation

Do not start a large confirmatory run until all boxes are checked:

- [ ] Read and summarize the full Williams (2017) method and its exact calibration/coverage claims.
- [ ] Extract the exact statistical procedure and selection variants from Cesarotti et al. (2019).
- [ ] Compare the proposed estimand to BumpNet, NPLM, LaCATHODE, and other directly relevant resonance-search calibration papers.
- [ ] State one primary estimand and one decision the result would change.
- [ ] Define scientifically justified generating scenarios and keep a held-out subset untouched during development.
- [ ] Validate the fitting/test implementation on known analytic or independently computed cases.
- [ ] Reproduce a documented CMS baseline numerically before connecting toy results to the data.
- [ ] Freeze test statistic, fit range, binning, model-selection rule, fit-failure policy, RNG scheme, and precision target before confirmatory runs.

## References

- Williams, M. (2017). *A novel approach to the bias-variance problem in bump hunting*. JINST 12, P09034. https://doi.org/10.1088/1748-0221/12/09/P09034
- Cesarotti, C., Soreq, Y., Strassler, M. J., Thaler, J., & Xue, W. (2019). *Searching in CMS open data for dimuon resonances with substantial transverse momentum*. Phys. Rev. D 100, 015021. https://doi.org/10.1103/PhysRevD.100.015021
- *Automatizing the search for mass resonances using BumpNet* (2025). JHEP 02, 122. https://doi.org/10.1007/JHEP02(2025)122
- *Robust resonant anomaly detection with NPLM* (2025). European Physical Journal C. https://link.springer.com/article/10.1140/epjc/s10052-025-14759-w
- Hallin, A. et al. (2023). *Resonant anomaly detection without background sculpting*. Phys. Rev. D 107, 114012. https://doi.org/10.1103/PhysRevD.107.114012
