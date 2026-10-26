# Focused literature-search update: dimuon bump-hunt calibration

**Checked:** 2026-10-26  
**Status:** targeted search update, not a systematic review.  
**Decision:** the proposed broad novelty claim remains **not established**. Do not start a large simulation campaign or describe this as a new method on the basis of this search alone.

## What this search adds

### 1. The 2012 CMS Open Data reference already documents the trigger-related structure

The CERN Open Data analysis record for the 2012 dimuon spectrum explicitly warns that the feature near 30 GeV is caused by data-taking/trigger effects, not a resonance. Its linked analysis uses the reduced muon-only sample and is useful for reproducibility, but the record does not itself establish the trigger efficiency or provide a validated trigger-response model.

- CERN Open Data analysis record: https://opendata.cern.ch/record/12342
- ROOT tutorial implementing the same selection: https://root.cern.ch/doc/PR/df102__NanoAODDimuonAnalysis_8py_source.html

**Implication:** re-plotting this structure or labelling it trigger-induced is not a novelty claim. The baseline is a software/reproducibility gate, not the scientific contribution.

### 2. The closest CMS Open Data resonance-search paper already treats local background fitting, ringing, and trigger turn-on limitations

Cesarotti et al. (2019), *Searching in CMS open data for dimuon resonances with substantial transverse momentum*, discusses local polynomial fits, fit-window and polynomial-order choices, the ringing effect, discrete profiling over background models, and a trigger-turn-on region where the method is unreliable without a precise trigger-shape model.

- Journal paper: https://doi.org/10.1103/PhysRevD.100.015021
- Searchable preprint: https://arxiv.org/abs/1902.07227

**Implication:** polynomial-order/window comparisons, a generic warning about trigger turn-on, and simple false-positive counts under alternative smooth spectra are insufficient by themselves. Any extension must specify exactly what is not already answered by this paper and why the distinction matters.

### 3. Background-model selection and coverage are already central in the bump-hunting literature

Williams (2017), *A novel approach to the bias-variance problem in bump hunting*, studies data-driven background-model selection, bias/variance, uncertainty and coverage, and false significance in toy ensembles.

- Preprint: https://arxiv.org/abs/1705.03578
- Journal version: https://doi.org/10.1088/1748-0221/12/09/P09034

**Implication:** comparing a fixed background with a selected background and evaluating coverage/false positives substantially overlaps with established work. More pseudoexperiments or a different plot do not establish novelty.

### 4. Later CMS dimuon searches show why trigger and selection details are analysis-specific

The CMS Collaboration's 2023 low-mass dimuon-resonance search uses a dedicated high-rate trigger stream and defines a specific mass-search range and selection. It is not a direct substitute for the 2012 dataset, but it reinforces that trigger stream, event content, selection, and mass range are part of the analysis definition—not generic nuisance labels.

- CMS result page: https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-21-005/index.html
- Paper: https://doi.org/10.1007/JHEP12(2023)070
- Preprint: https://arxiv.org/abs/2309.16003

**Implication:** do not import a later-era trigger model into the 2012 sample without a documented mapping and the required data/metadata. This source is context, not evidence that the present repository can model trigger efficiency.

## Revised novelty decision

The most defensible possible methodological question remains:

> For a fully specified local bump-hunt pipeline, how do prespecified, smooth acceptance/turn-on distortions—treated explicitly as synthetic stress tests rather than as a CMS trigger simulation—affect empirical null rejection rates, and can a diagnostic detect failures on held-out distortion shapes?

This is a **candidate for investigation only**, not a demonstrated gap. The targeted search above does not establish that no equivalent study exists.

Before any main simulation:
1. Search further for acceptance sculpting, trigger-induced mass-spectrum structures, spurious-signal tests, and null-calibration studies across collider experiments.
2. Compare complete procedures and estimands, not only paper titles.
3. Define the test statistic, fixed-mass versus scan interpretation, background generators, distortion family, nominal size, fit-failure handling, and held-out scenarios before running the main experiment.
4. Test calibration on analytically tractable cases and against an independent implementation.
5. Inspect exact official ROOT files and establish what trigger and event-quality information they actually contain.
6. If no clear non-duplicative question survives, choose the reproducibility/validation route and state that honestly.

## Immediate project status

- **Code/CI:** synthetic ROOT tests and CI validate only the tested pipeline behaviour.
- **Official-data baseline:** not yet run against an official ROOT file; no numerical reproduction claimed.
- **Trigger-aware inference:** not approved; exact file-level branch semantics and trigger/prescale inputs remain unresolved.
- **Novelty:** not passed.
- **Publication suitability:** cannot be predicted from the current scaffold.

A negative novelty or feasibility decision is useful progress: it prevents spending substantial time on an experiment whose interpretation the available evidence cannot support.
