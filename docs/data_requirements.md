# Data requirements and feasibility gates

**Status: requirements checklist; this repository has not yet processed a CMS dataset.**

## A. Choose the estimand before choosing the largest dataset
The provisional primary estimand is the null rejection probability of one explicitly specified local test under defined generating scenarios. This does not automatically require the largest collision dataset. The pseudoexperiment generator, fit procedure, trigger/selection definition, and calibration design determine feasibility.

## B. Dataset suitability gate
The 2019 education/outreach reduced dataset at https://opendata.cern.ch/record/12341 explicitly says no further validation was performed on the reduced output. Use it for software development unless independent checks establish suitability. First assess the research-level Run2012B and Run2012C DoubleMuParked ntuples (https://opendata.cern.ch/record/cms-31123 and https://opendata.cern.ch/record/cms-31129). These were processed using validated runs, but the portal notes that not all variables are available. Inspect the actual schema and producer documentation before selecting the primary input.

## B. Required observed-data inputs
Before analysis, record and verify:
- Official CERN Open Data record, DOI, exact file paths, checksums where available, and reuse/citation conditions.
- Data-taking period, run/luminosity-block certification, integrated luminosity and its source.
- Dataset/stream and trigger paths, thresholds, prescales, and turn-on region.
- Muon kinematics and quality variables, opposite-charge pairing, and four-vector components or enough information to reconstruct them.
- Branch names, units, missing-value conventions, duplicate-event checks, and schema/version.
- Selection, mass range, binning, fit windows, and reproducible comparison to the official reference output.
- Compatible software release and limitations of the old released data and simulation.

## C. Required pseudoexperiment metadata
For each scenario preserve:
- Null-generating model and parameter values; whether parameters are fixed or estimated per trial.
- Fitted null and signal-plus-background models, optimizer settings, convergence criteria, and boundary rules.
- Test statistic, nominal rejection threshold, and whether p-values are asymptotic or simulation-calibrated.
- Scenario-specific changes from baseline, with one change at a time initially.
- Random-seed strategy, attempted and valid trial counts, fit failures, and retry policy.
- Development scenarios and held-out evaluation scenarios separated before inspecting results.

## D. Data-volume strategy
1. Tiny example or a few hundred events: verify parsing, units, invariant mass, charge pairing, and selections. This is only a software smoke test.
2. Small representative file/subset: validate the pipeline and compare with a documented reference. Do not tune final conclusions on this subset.
3. Full selected public sample: process only after the subset matches the reference and trigger/data-quality requirements are understood. Report the actual selected event count; do not guess it in advance.
4. Pseudoexperiments: start with 20 per scenario for code checks, then a 500-run pilot, then consider 10,000 per scenario for ordinary 5% type-I-error precision. Use exact binomial intervals and a predeclared precision goal. Ten thousand runs do not empirically establish five-sigma tails.

## E. Stop conditions
Do not launch the main simulation if the baseline cannot be reproduced, required variables or trigger information are unavailable, a known trigger artifact is treated as a resonance without evidence, the novelty is only a repeat of published polynomial/window comparisons, or the test statistic and fit-failure policy remain outcome-driven.

## F. Provenance rule
Observed collision data, simulated detector events, model-generated pseudoexperiments, and artificial stress tests are different data classes and must be labelled separately. Never call a toy simulation CMS data.
