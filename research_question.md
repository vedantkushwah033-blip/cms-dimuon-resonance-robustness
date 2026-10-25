# Research question and scope

**Status:** provisional research design; no empirical results claimed.  
**Last updated:** 2026-10-25

## Working title
**Selection-Aware Calibration of Local Dimuon Bump Hunts: A Reproducible Statistical Audit**

This title describes a candidate direction, not a claim of novelty.

## Candidate primary question
For a fully specified local dimuon bump-hunt procedure, how does its empirical null rejection rate behave when the background-generating process differs from the fitted background model, and how does including any data-driven background-model selection affect calibration on prespecified held-out scenarios?

This candidate must pass a literature audit before it is frozen. Williams (2017) already studies data-driven background-model selection and uncertainty/coverage in bump hunting. If the proposed comparison is already answered by that or another study, we must narrow or stop the novelty claim.

## Primary estimand
For a prespecified nominal test size alpha and a precisely defined background-generating scenario, estimate the probability that the complete analysis procedure rejects the null. If the procedure selects a background model, the selection step must be repeated inside each pseudoexperiment exactly as it would be in the intended analysis. Report the rejection count, number of attempted and valid trials, empirical rate, exact binomial confidence interval, and failure rate.

The primary estimand concerns the defined simulation scenarios. It does not prove calibration for all possible backgrounds or establish detector-level realism.

## Candidate comparison
Subject to literature and feasibility gates, compare:
1. A fixed, prespecified background model and local test.
2. A model-selection procedure whose candidate models and selection rule are fixed in advance.
3. The same procedures under a baseline generating model and scientifically justified alternative smooth generators, with held-out scenarios kept untouched during development.

A comparison is not useful merely because it contains more models. It must answer a specific question not already answered in the literature.

## Scope guardrails
- No particle-discovery claim.
- Distinguish observed CMS collision data, detector simulation, model-generated pseudoexperiments and artificial stress tests.
- Use the reduced 2012 CMS sample first for baseline reconstruction; do not assume it contains all trigger/quality information needed for a trigger-level study.
- A model-generated mass spectrum does not represent full detector-level CMS data.
- Any diagnostic is evaluated, not presumed effective.
- Global significance is out of scope unless a defensible scan procedure and the null distribution of the maximum statistic are implemented and validated.
- Do not claim five-sigma tail validation from ordinary toy-simulation counts.
- Report negative and inconclusive results.

## Data feasibility
The candidate reduced event dataset is documented at https://opendata.cern.ch/record/12341 (DOI 10.7483/OPENDATA.CMS.LVG5.QT81). It contains listed muon kinematic and charge branches, but the available record alone does not establish that all trigger information needed for the original trigger-misspecification idea is available. The initial code therefore aims only to reconstruct the opposite-charge invariant-mass spectrum.

## Go/no-go conditions
Proceed to the main experiment only after:
1. The official baseline spectrum is reproduced and discrepancies explained.
2. The closest prior work, especially Williams (2017) and Cesarotti et al. (2019), is compared method-by-method.
3. The primary estimand, test statistic, model families, model-selection rule, fit-failure policy and held-out scenarios are frozen.
4. The required inputs are shown to support the intended inference.
5. A pilot demonstrates correct implementation and feasible runtime.

If a meaningful novelty gap does not survive these checks, re-scope the project as a high-quality reproducibility and validation study rather than claiming a new method.
