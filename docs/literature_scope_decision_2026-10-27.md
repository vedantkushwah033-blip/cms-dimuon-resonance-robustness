# Literature scope decision and novelty risk — 2026-10-27

**Status:** focused source-screening memo, not a systematic review. **Novelty is not established.** No new statistical experiment is authorized by this memo.

## Decision in one paragraph

The broad idea “test local dimuon bump hunts under background-model misspecification and compare fixed versus selected background models” is not yet a defensible novelty claim. Closely related work already studies background-model selection, bias/variance, and interval coverage in bump hunting; a CMS Open Data dimuon-resonance analysis already uses local polynomial fits, discusses fit-window choice and spurious ringing, compares cubic and quintic models, and masks a trigger-turn-on region in one sample. Newer work also studies data-directed bump hunting and background-sculpting-resistant anomaly searches. The project must identify a narrower, decision-relevant gap—or deliberately become a transparent reproducibility/benchmark study—before large simulation runs or any novelty language.

## Primary-source screening completed

### 1. Williams (2017): background-model choice is already a central bump-hunt topic

- Michael Williams, “A novel approach to the bias-variance problem in bump hunting,” *Journal of Instrumentation* 12 (2017) P09034, DOI: [10.1088/1748-0221/12/09/P09034](https://doi.org/10.1088/1748-0221/12/09/P09034); [arXiv:1705.03578](https://arxiv.org/abs/1705.03578).
- The published abstract explicitly studies data-driven background-model selection and uncertainty from model choice, evaluates several methods on realistic examples, and discusses confidence-interval coverage.
- Consequence: comparing “fixed model versus selected model” and reporting coverage is not, by itself, an original contribution. Any proposed difference must be established against the paper's actual methods, scenarios, and results—not inferred from the abstract alone.

### 2. Cesarotti et al. (2019): direct overlap with CMS Open Data dimuon searches

- Cari Cesarotti, Yotam Soreq, Matthew J. Strassler, Jesse Thaler, and Wei Xue, “Searching in CMS Open Data for Dimuon Resonances with Substantial Transverse Momentum,” *Physical Review D* 100, 015021 (2019), DOI: [10.1103/PhysRevD.100.015021](https://doi.org/10.1103/PhysRevD.100.015021); [arXiv:1902.04222](https://arxiv.org/abs/1902.04222).
- The published methods describe local fits around each test mass, a fifth-order polynomial with six free parameters, fit-window choices, a cubic/quintic cross-check, and the risk of correlated spurious “ringing” features. The analysis also discusses a trigger-turn-on region.
- Consequence: a project framed simply as “test polynomial background choice and local bump-hunt robustness on CMS dimuon data” risks substantial overlap. A distinct estimand and method comparison are required.

### 3. Data-directed bump hunting (2022)

- “A data-directed paradigm for BSM searches: the bump-hunting example,” *European Physical Journal C* (2022), [journal article](https://link.springer.com/article/10.1140/epjc/s10052-022-10215-1).
- This is another nearby line of work on data-directed methods for bump hunting. Its full methods and relation to the proposed experiment still need a detailed comparison.
- Consequence: do not present data-directed selection or a generic diagnostic as new without checking this literature.

### 4. Resonant anomaly detection and background sculpting (2023)

- “Resonant anomaly detection without background sculpting,” *Physical Review D* 107, 114012 (2023), [journal article](https://doi.org/10.1103/PhysRevD.107.114012).
- The work proposes latent CATHODE for enhanced bump hunts and evaluates stability and performance in toy and LHC Olympics R&D examples.
- Consequence: if the project introduces a data-driven diagnostic, anomaly score, or selection step, the background-sculpting literature is relevant; a generic “robustness diagnostic” is not automatically a gap.

### 5. Newer inference/model-checking directions (2025)

- “Finding excesses in model parameter space,” *European Physical Journal C* (2025), [journal article](https://link.springer.com/article/10.1140/epjc/s10052-025-13795-w), discusses simulation-based inference and the challenge of unknown or difficult-to-simulate backgrounds.
- Consequence: the broader field is active. This source is contextual rather than a demonstrated direct duplicate of the current proposal; its exact relevance needs a methods-level read.

## Data-side constraint that affects the scientific claim

The public CMS outreach dimuon example documents a feature near 30 GeV as a trigger/data-taking effect, not a new resonance. Its reduced dataset contains only muon kinematics and charge, and the portal states that the reduced output was not further validated. The successful 10,000-entry repository smoke test is therefore software evidence only. It does not validate a trigger model, establish a physics-quality selection, reproduce the full reference histogram, or support a new-physics claim.

The separate Run2012B/C research-level derived records are better candidates for exact-file inspection. Their published variable lists include path-named HLT decisions, but exact file contents, path/run semantics, valid denominator, certified-lumisection handling, and prescale/luminosity treatment still require verification. Do not describe the analysis as trigger-efficiency measurement until those inputs and the estimand are validated.

Official source records:
- [CMS Open Data dimuon example, record 12342](https://opendata.cern.ch/record/cms-12342)
- [Reduced outreach dataset, record 12341](https://opendata.cern.ch/record/12341)
- [Run2012B DoubleMuParked research-level ntuple, record 31123](https://opendata.cern.ch/record/cms-31123)
- [Run2012C DoubleMuParked research-level ntuple, record 31129](https://opendata.cern.ch/record/cms-31129)

## Candidate routes, ranked by evidence required (not by prestige)

### Route A — reproducibility and numerical-validation paper (lowest novelty burden)

Reproduce the public baseline from the exact official source; compare event cut-flow, histogram bin contents and boundaries against an independently executed reference; explain floating-point differences; publish a reproducible audit with versioned data manifest and tests. This can be valuable if the discrepancy analysis or validation method reveals a meaningful, generalizable lesson. A correct reproduction alone may be educational rather than a high-impact research contribution.

### Route B — a narrow statistical-calibration benchmark (possible, but novelty gate remains open)

Define one concrete analysis decision that prior work has not already answered. Freeze the complete procedure, including every model-selection/diagnostic step, and estimate its null rejection rate on a small set of scientifically justified, predeclared and held-out generating scenarios. Validate known cases, refit nuisance parameters per pseudoexperiment, record failures, and use exact binomial intervals. Compare the design method-by-method against Williams (2017), Cesarotti et al. (2019), and the data-directed/anomaly-detection literature before running a large simulation.

A benchmark is not novel merely because it uses more scenarios, a different random seed, or another plot. The contribution must change a methodological conclusion or a practical analysis decision.

### Route C — trigger-aware study (highest data and physics burden)

Proceed only after actual research-level files have been inspected and the trigger estimand is justified. Require exact file provenance, branch types and values, run-dependent path definitions, event selection, certified luminosity sections, valid denominator, and prescale/luminosity treatment. If any essential item is unavailable, narrow the claim instead of imputing it.

## Stop/go checklist before any main experiment

- [ ] Read the methods and relevant supplements of the closest papers, not only their abstracts.
- [ ] Complete a paper-by-paper matrix: data, selection, statistic, fitted/generating models, selection rule, nuisance refitting, calibration metric, held-out scenarios, and limitations.
- [ ] State the one-sentence methodological difference and the specific decision a result would change.
- [ ] Demonstrate that the public data pipeline is quantitatively reproduced or explicitly limit the project to software validation.
- [ ] Freeze a primary estimand, alpha, test statistic, fit window, candidate models, selection rule, fit-failure policy, random-seed policy, and held-out scenarios.
- [ ] Validate the implementation on known statistical cases before using CMS-motivated stress tests.
- [ ] Obtain an independent technical review if possible; report its actual scope and do not imply endorsement.

**Current decision: HOLD the large Monte Carlo experiment and all novelty claims.** Continue with exact-file data feasibility and the methods-level literature comparison first. If no meaningful gap survives, publish the work honestly as a reproducibility/validation study or stop; neither outcome should be disguised as a discovery.
