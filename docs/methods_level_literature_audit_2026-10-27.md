# Methods-level literature audit: what the closest papers actually evaluate

**Date:** 2026-10-27  
**Status:** focused primary-source reading notes; not a systematic review, independent peer review, or novelty certification.  
**Purpose:** sharpen the comparator and estimand decisions before any confirmatory simulation.

## 1. Williams (2017): the overlap is deeper than “background selection”

**Source:** M. Williams, “A novel approach to the bias-variance problem in bump hunting,” *JINST* 12 (2017) P09034. [Author manuscript](https://arxiv.org/abs/1705.03578), [MIT repository record](https://dspace.mit.edu/entities/publication/59ee701d-ffd2-480e-88e2-1ccf5c012fc7).

### What the paper does
The methods section treats the signal-strength estimator and its confidence interval at each test mass as central quantities. It compares a wide background model, stepwise model selection, AIC-based choices, model averaging, regularization, and approaches to accounting for model-selection uncertainty. Its proposed construction maps a local fit interval to [-1, 1], includes odd background modes in candidate models, selects among even modes, and accounts for model-selection uncertainty using a discrete nuisance parameter in the profile likelihood. The paper reports that naive stepwise selection can bias estimates, undercover, and overstate significance in its studied examples; the more careful approaches depend on an adequate wide model.

The paper explicitly distinguishes local p-values from global p-values and says the look-elsewhere/global conversion is well covered elsewhere. That distinction matters: a project whose primary target is the global type-I error of an entire selected-model-plus-mass-scan procedure is not automatically identical to this paper’s main estimand, but neither is it automatically novel. The complete model-selection and scan steps still need to be represented in the calibration and comparator.

### Implication for this project
- **Not a sufficient contribution:** showing that selecting background models can change bias, coverage, or false positives.
- **Potential comparator:** the paper’s AIC-based model-selection approach with model-selection uncertainty, alongside a wide-model baseline, if it can be implemented faithfully and validated.
- **Unresolved:** whether its local fit construction and model choices transfer to the specific CMS data/fit range and to the proposed global calibration estimand.
- **Required check:** compare the exact primary estimand, fit region, signal template, background basis, model-selection rule, nuisance treatment, and calibration—not just headline outcomes.

## 2. Algeri (2020): a different kind of mismatch-aware procedure

**Source:** S. Algeri, “Detecting new signals under background mismodeling,” *Physical Review D* 101, 015003 (2020). [arXiv full text](https://arxiv.org/abs/1906.06615), [publisher page](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.101.015003). The author’s [LPBkg package documentation](https://salgeri.r-universe.dev/LPBkg) describes a software implementation.

### What the paper does
The paper represents a true density relative to a postulated density through a comparison density, then estimates deviations using an LP/Legendre-series approach. It defines an overall deviance test for whether the observed distribution differs from the postulated one anywhere over the chosen range, and confidence bands to characterize where departures occur. The workflow discusses using source-free samples or control regions where available, partial scientific knowledge about the background, and choices balancing approximation bias against variance. It also develops signal-search and characterization examples.

This is not merely another polynomial background fit. Its comparison-density representation and deviance/CD-plot workflow are a meaningful methodological alternative. At the same time, a goodness-of-fit departure is not automatically evidence for a narrow resonance, and a range-wide deviance test is not automatically calibrated for a pipeline that also scans candidate masses, chooses models, tunes thresholds, and reports the maximum excess.

### Implication for this project
- **Not a sufficient contribution:** inventing a generic mismatch flag or showing that the flag changes under a misspecified background.
- **Possible comparator or diagnostic:** LPBkg’s deviance/comparison-density approach, but only after checking assumptions, sample requirements, implementation, and whether its target matches the proposed estimand.
- **Critical question:** can a fair implementation use only information available to the candidate method, or does it rely on source-free/control-region information unavailable in the chosen CMS sample?
- **Calibration requirement:** if its diagnostic is used to make or alter a discovery decision, calibrate the entire predeclared decision pipeline on the relevant null scenarios; do not assume a per-range test automatically handles every later selection and scan.

## 3. Cesarotti et al. (2019): relevant physics precedent, different data/analysis

**Source:** C. Cesarotti et al., “Searching in CMS Open Data for Dimuon Resonances with Substantial Transverse Momentum,” *Physical Review D* 100, 015021 (2019). [Publisher article](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.100.015021).

The paper reports a resonance search using 2.11 fb^-1 of 7 TeV CMS Open Data from the 2011A DoubleMu sample, with a 14–66 GeV target range, dimuon transverse-momentum selections, isolated and prompt-muon samples, detector/QCD background treatment, and a profiled-likelihood search. It validates trigger-threshold choices using a prescaled trigger and discusses the relevant data/selection details.

The current repository’s schema audit samples Run2012B/C DoubleMuParked research-level files, while the educational outreach spectrum is a separate data product. These are not the same input or analysis. A successful reproduction of the simple opposite-charge spectrum would therefore not reproduce this published resonance search.

### Implication for this project
- Treat the paper as the closest physics-analysis precedent, not as evidence that the current project reproduces its results.
- Do not borrow its trigger assumptions or prescale/denominator logic without matching the dataset, run period, paths, selections, and metadata.
- Any future real-data claim needs its own provenance, selection, trigger, and baseline-validation record.

## 4. Comparison table

| Dimension | Williams (2017) | Algeri (2020) | Cesarotti et al. (2019) | Current project status |
|---|---|---|---|---|
| Main focus | Background-model selection; signal-strength bias/variance; intervals and local significance | Nonparametric mismatch assessment and signal inference using comparison densities | CMS Open Data dimuon resonance search | Not yet frozen |
| Core mechanism | Wide model, local fit, model selection, selection-uncertainty treatment | LP comparison density, deviance test, confidence bands, optional signal information | Physics-motivated event selection, trigger validation, profile likelihood | Baseline and candidate method still under development |
| Is mass-scan/global calibration the central evaluated target? | Global p-value noted as a separate established step; local inference/model selection is central | Overall distributional deviation test is developed; project-specific mass scan/selection calibration still needs separate scrutiny | Performs a defined physics search; its data and search scope differ from this repository | No global estimand frozen |
| Assumptions to examine | Adequate wide model, fit region, signal shape, candidate basis, nuisance treatment | Postulated distribution, LP truncation choice, calibration/control information, interpretation of departures | Data period, trigger paths, offline cuts, backgrounds, luminosity and efficiency treatment | Event-level trigger semantics and parity unverified |
| Possible role | Comparator for model-selection effects and inference | Comparator/diagnostic if its assumptions match | Physics/data precedent | None approved yet |
| Does this establish the proposed gap? | No | No | No | No novelty claim justified |

## 5. Consequences for the project decision

The narrow candidate question remains only a hypothesis:

> What is the global null rejection rate of a completely specified mass-scan pipeline, including its model selection and any diagnostic-based decision, on prespecified held-out null scenario families—and how does that operating characteristic compare with a fair, validated existing procedure?

The literature examined so far does not prove that this question is novel. It does, however, identify two materially different methodological routes that must not be collapsed into a generic “background robustness” label: model-selection-aware local resonance inference (Williams) and comparison-density-based mismatch assessment (Algeri).

### Required next actions
1. Decide whether the project’s primary outcome is global type-I error, a diagnostic false-alarm rate, coverage, or another estimand. Do not blend them into one headline metric.
2. Choose a comparator only after checking whether its assumptions and output genuinely match that estimand.
3. Inspect the official code/software for the chosen comparator and document any adaptation; do not implement a straw-man approximation and label it the published method.
4. Complete the CMS baseline provenance and candidate/reference parity gate.
5. If no distinct decision-relevant gap remains, reframe the work as a reproducible benchmark rather than claiming a new statistical method.

**Decision:** continue protocol/literature work; **no-go** for confirmatory simulation and no resonance/trigger-efficiency claim at this stage.
