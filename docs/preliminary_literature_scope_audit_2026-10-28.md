# Preliminary literature and scope audit — 2026-10-28

**Status:** preliminary desk review, not systematic and not a novelty certification. Search terms and papers should be expanded before manuscript submission.

## Research direction under review

Candidate question: how accurately does the *complete* dimuon bump-hunt procedure control its global false-positive rate when background-model selection and a mass scan are repeated on each spectrum, particularly when the background-generating process lies outside the fitted candidate family?

## Directly relevant prior work found

### 1. Williams (2017), *A Novel Approach to the Bias-Variance Problem in Bump Hunting*

Michael Williams, Journal of Instrumentation 12 (2017) P09034, DOI: 10.1088/1748-0221/12/09/P09034.

The paper studies data-driven background-model selection and uncertainty due to background-model choice, including estimator bias, variance, and confidence-interval coverage. Therefore, background-model selection and coverage alone cannot be presented as the novelty of this project. The proposed study would need a more specific distinction, such as a prespecified evaluation of *global false-positive calibration for the complete adaptive scan procedure* under clearly declared held-out generating families—and even that distinction must be checked against further literature.

### 2. Cesarotti et al. (2019), *Searching in CMS Open Data for Dimuon Resonances with Substantial Transverse Momentum*

Physical Review D 100, 015021 (2019), DOI: 10.1103/PhysRevD.100.015021.

This paper already performs a research-level dimuon resonance search using CMS Open Data, with selections, background considerations, a local bump-search strategy, and model-independent limits. Merely using CMS Open Data to search for dimuon resonances is not a novelty claim.

### 3. CERN Open Data educational dimuon spectrum

CERN Open Data records for the 2012 dimuon spectrum explicitly warn that the visible feature near 30 GeV is a trigger/data-taking effect, not a resonance. This reinforces that the current repository must not treat a feature in the educational spectrum as a discovery or use a histogram reproduction as evidence of trigger validity.

## Candidate contribution that remains unproven

A potentially defensible contribution could be a transparent, reproducible *calibration study* that:
1. defines the complete scan statistic and all data-dependent model-selection steps;
2. estimates a global critical threshold on an independent calibration sample;
3. evaluates false-positive rate on untouched background-generating scenarios, including at least one outside the fitted model family;
4. reports Monte Carlo uncertainty, failed-fit rates, and paired comparisons;
5. measures signal-injection power separately from null calibration; and
6. publishes a complete run manifest and per-replicate diagnostics.

These are proposed design features, not a demonstrated gap. The work must compare against established look-elsewhere corrections, bump-hunting methods, likelihood-ratio calibration, and model-selection approaches before claiming methodological novelty.

## Explicit exclusions

Do not claim:
- a new particle or resonance;
- a new false-positive correction method before one is defined and tested;
- trigger efficiency or detector-performance validation from histogram parity;
- novelty merely because many pseudo-experiments were run;
- superiority of a model-selection procedure before held-out results support it;
- publication readiness from passing software tests alone.

## Go/no-go recommendation

**Proceed with the calibration study as a hypothesis, not as an asserted novelty.** Before confirmatory simulation, expand the literature search and freeze the statistical protocol. If the literature already covers the precise proposed estimand and evaluation design, revise the question or treat the project as a rigorous replication/benchmark rather than manufacture a novelty claim.
