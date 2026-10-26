# Analysis plan

**Status:** pre-implementation plan; numerical results intentionally absent.  
**Last updated:** 2026-10-26

## Stage 0 — literature and data feasibility
Deliverables: verified source table; precise data record and format; documented trigger and event selection; list of observables and required simulated samples; novelty decision with stop/re-scope criteria.

**Stop condition:** if the closest prior work already answers the same question with an equivalent experimental design, do not proceed under a novelty claim. Reframe only if a genuinely distinct question is supported by evidence.

## Stage 1 — reproducible baseline

A chunked starter script is available at `scripts/reproduce_dimuon_spectrum.py`. Begin by inspecting a specific selected file with `python scripts/inspect_root_schema.py --input /path/to/selected-file.root --output outputs/schema_report.json`, then use `python scripts/reproduce_dimuon_spectrum.py --input /path/to/selected-file.root --max-events 10000` only if its schema supports the baseline; this is a proposed smoke test and has not yet been run against the official file. The script applies only opposite-charge pairing and is not a trigger/quality-selection analysis. Compare its output to the official reference before proceeding. Do not assume that branch lists documented for one Run2012C-derived record apply to another record.

1. Reproduce a documented CMS dimuon mass spectrum using the official record and technical instructions.
2. Record file identifiers, dataset DOI, data-taking period, luminosity information where documented, software versions, event filters, trigger requirements, muon quality requirements, opposite-charge condition, mass range, and binning.
3. Validate the invariant-mass calculation independently on a small sample using four-vectors and a known implementation.
4. Compare the reconstructed distribution against the official reference plot or output where meaningful.
5. Explain known trigger-induced structures and avoid interpreting them as new resonances.
6. Save a configuration file and immutable run metadata; do not embed unrecorded choices in scripts.

The baseline is not complete until the analysis can be rerun from documented inputs and its key selection steps have tests.

## Stage 2 — define a testable procedure

The literature audit must explicitly compare the candidate design against Williams (2017), which already addresses data-driven background-model selection, bias/variance, and interval coverage in bump hunting. If the proposed comparison is materially equivalent, do not proceed under a novelty claim.

Before the main pseudoexperiment set, prespecify: target mass range and fixed-mass versus scan design; baseline background family and parameterization; fit range/window and binning; test statistic and p-value calculation; fit-failure and boundary handling; nuisance parameters and constraints; feasible nominal alpha levels; definition of calibration failure; diagnostic and decision threshold; and development versus held-out evaluation scenarios.

Do not choose these after looking at which option produces the strongest result.

## Stage 3 — null calibration and stress tests
A. **Well-specified null:** generate background-only pseudoexperiments from the same model used for fitting. This checks basic implementation and nominal calibration, not realism.

B. **Misspecified null:** generate from prespecified alternative shapes or controlled mixtures, then fit with the nominal procedure. The generating model must differ from the fitted model in a documented way.

C. **Selection stress tests:** test only selection or trigger effects that can be defined from available data and documentation. A changed selection cut changes the target population and is not automatically a misspecification unless the data-generating and assumed analysis selections are clearly distinguished.

D. **Injected-signal validation (secondary):** if useful, inject known signals into background-only samples to test signal-yield bias and interval coverage. Do not confuse this with false-positive calibration under the null.

Use a small pilot to catch implementation bugs and estimate computational cost. Do not begin a large campaign until the protocol is frozen.

## Stage 4 — outcomes and uncertainty
Primary metric for each scenario and nominal test size alpha: number of pseudoexperiments rejecting the null divided by the number of valid, prespecified trials.

Report the rejection count and denominator, rejection fraction, a binomial confidence interval (Wilson or exact method chosen in advance), invalid-fit rate and handling, Monte Carlo uncertainty, scenario definition, and random seeds.

For low nominal alpha, the expected number of false positives is N times alpha. A simulation with few expected exceedances cannot precisely estimate a tiny tail probability. Ordinary pseudoexperiment counts will not empirically certify a 5-sigma tail. Avoid extrapolation unless a validated tail method is separately justified and audited.

Secondary outcomes may include parameter bias, interval coverage, and diagnostic classification performance. Define denominators and failed-fit handling before evaluation.

## Stage 5 — diagnostic evaluation
Select one simple, scientifically motivated diagnostic only after the literature review. Candidate classes include goodness-of-fit measures or predictive checks, but exact form and threshold must be prespecified.

- Develop or tune on designated scenarios only.
- Freeze the diagnostic and threshold.
- Evaluate on held-out scenarios designed to differ in shape or severity from the development set.
- Report sensitivity, specificity, false alarm rate, and uncertainty.
- Include failure cases. A diagnostic that cannot detect a form of misspecification should be described as limited, not silently replaced after seeing evaluation results.

A goodness-of-fit test may have low power against some alternatives and cannot prove a model is correct. Passing a diagnostic does not guarantee valid p-values.

## Stage 6 — independent validation and reporting
- Recompute key summaries from raw trial-level outputs with a separate audit script.
- Add unit tests for invariant mass, likelihood components, p-value conversion, confidence intervals, and scenario labels.
- Run tests on a small deterministic fixture in continuous integration.
- Archive configuration, dependency versions, seeds, outputs, and a manifest.
- Report negative results and limitations alongside positive findings.

## Computational budget
Start with deterministic unit tests and a tiny pilot (for example, tens to a few hundred pseudoexperiments per scenario, only for software debugging). This pilot is not evidence of tail calibration. Set the final number of trials from target alpha, desired interval precision, number of scenarios, and measured runtime. Use a documented decision, not an arbitrary large run matrix.

## Prespecified decision gates
- **Gate A:** data and literature support a specific, non-duplicative question.
- **Gate B:** baseline is reproducible and cross-checked.
- **Gate C:** statistical procedure and scenarios are frozen.
- **Gate D:** independent validation passes.
- **Gate E:** conclusions are no broader than the tested assumptions.

No result, significance claim, or publication suitability is promised in advance.
