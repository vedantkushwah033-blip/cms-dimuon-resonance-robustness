# Method-by-method novelty comparison

**Last reviewed:** 2026-10-26  
**Decision:** the broad candidate question does **not** pass the novelty gate yet. This document is a comparison of known prior work, not a claim that a gap exists.

## Closest prior work

### Williams (2017), “A novel approach to the bias-variance problem in bump hunting”
Primary source: https://arxiv.org/abs/1705.03578

The paper explicitly studies data-driven background-model selection, bias and variance in the signal-strength estimator, uncertainty from model selection, interval coverage, and local p-values. It compares a true model, a wide model, stepwise selection, AIC selection, an AIC strategy that always includes odd modes, and frequentist model averaging. Its toy study uses 1,000 pseudo-datasets per background/signal setting and evaluates coverage and false significance. It also discusses real-world examples.

**Implication:** a proposal simply to compare a fixed background model with a selected model, generate smooth null alternatives, and measure bias/coverage/false positives would substantially overlap. Repeating the experiment with another spectrum is not automatically a scientific contribution.

### Cesarotti et al. (2019), “Searching in CMS open data for dimuon resonances with substantial transverse momentum”
Primary source: https://doi.org/10.1103/PhysRevD.100.015021

This is a direct CMS Open Data dimuon resonance-search predecessor. It uses local fits in a mass window, a fifth-order polynomial baseline, checks cubic versus quintic models and alternative window sizes, discusses a spurious “ringing” effect, and examines discrete profiling over background models. It also identifies a trigger-turn-on region where the spectrum changes rapidly and the method is unreliable without a precise trigger-shape model.

**Implication:** comparing polynomial order or window size, looking for ringing, or pointing out a trigger-induced feature is not sufficient novelty by itself. The known trigger feature near 30 GeV is already documented in the public CMS dimuon analysis record.

### Gross & Vitells (2010) and Cowan et al. (2011)
- Gross & Vitells: https://doi.org/10.1140/epjc/s10052-010-1470-8
- Cowan et al.: https://doi.org/10.1140/epjc/s10052-011-1554-0

These are foundational references for look-elsewhere effects and likelihood-based inference. A fixed-mass local test and a scan over many masses have different null distributions. Any global-significance claim would need a correctly defined scan and validated calibration.

## Candidate-method comparison

| Candidate idea | What prior work already covers | Remaining possible contribution (unproven) | Current decision |
|---|---|---|---|
| Compare polynomial orders and fit windows | Cesarotti et al. directly studies both, including ringing | Only if a precise, consequential, unaddressed calibration question is identified | Reject as standalone novelty |
| Compare fixed and data-selected background models | Williams studies stepwise/AIC selection, model averaging, uncertainty and coverage | A sharply defined estimand or scenario family not already treated, with a documented literature comparison | Not passed |
| Count false positives in background-only toys | Williams already evaluates false significance in ensembles | Need a substantively different and justified generator/procedure, not merely more toys | Not passed |
| Reproduce the 2012 dimuon spectrum and explain the known trigger feature | Public CMS example and paper already show the spectrum and known trigger/data-taking effect | A carefully documented independent reproducibility audit may be useful, but alone is likely a replication contribution rather than a new method | Feasible fallback |
| Evaluate calibration under synthetic trigger-turn-on distortions | Cesarotti identifies a problematic trigger-turn-on region; public outreach file is muon-only | Could test a *clearly defined abstract selection/turn-on distortion* if it answers a new question and is compared with relevant literature; it would not be a detector-level trigger model | Candidate for further review only |
| Claim real-data trigger-efficiency robustness using only the muon-only outreach file | The 2019 outreach record lists only muon kinematics and charge | No demonstrated availability of trigger bits, prescales, or enough metadata to support that inference | No-go with that file |

## Most defensible next question to investigate

Do not freeze the current title or claim novelty yet. Investigate this narrower methodological possibility:

> For a fully specified local bump-hunt pipeline, how much can an externally specified, smooth trigger-turn-on-like acceptance distortion change empirical null rejection rates when the analysis does not model that distortion, and can a prespecified diagnostic detect the failure on held-out distortion shapes?

This is **not yet a novel contribution**. The question must pass all of these checks before the main experiment:

1. Search for existing work on trigger turn-on effects, acceptance sculpting, selection-induced bumps, background misspecification, and empirical false-positive calibration.
2. Define the distortion mathematically and justify its shape/range from public documentation; do not tune it to create the strongest result.
3. Distinguish a generic synthetic acceptance function from actual CMS trigger efficiency. Without suitable trigger data, the inference is only about the synthetic model.
4. Specify the fixed-mass test or mass scan, background generator, fit model, statistic, nominal alpha, fit-failure policy, and held-out shapes in advance.
5. Test the null calibration on analytically known or independently implemented cases before the main study.
6. Compare the complete protocol to Williams (2017), Cesarotti et al. (2019), and literature on sculpting and trigger-induced structures.
7. If equivalent work already exists, or the available data cannot support the claimed interpretation, narrow the scope to a reproducibility and statistical-validation study.

## Go/no-go status

- [x] Identified close predecessor papers.
- [x] Rejected polynomial/window comparison as sufficient novelty.
- [x] Rejected trigger-efficiency claims from a muon-only schema without additional evidence.
- [ ] Complete literature search across trigger turn-on, selection sculpting, and null calibration.
- [ ] Establish a specific difference from all closest methods.
- [ ] Confirm actual input schema and reproduce a documented baseline.
- [ ] Freeze a reviewed protocol before main simulations.

**Bottom line:** scientific quality can be high even if the result is a careful replication or a negative finding. Novelty cannot be guaranteed by effort or by a publication label; it has to be demonstrated against prior work.
