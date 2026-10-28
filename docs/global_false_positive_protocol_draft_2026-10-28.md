# Global false-positive calibration protocol — draft for review

**Status:** protocol proposal only; not preregistered, not executed, and not evidence of a physics result.  
**Project:** Statistical Reliability of Dimuon Resonance Searches under Trigger and Background-Model Misspecification.  
**Branch:** audit/histogram-edge-and-sensitivity-fixes-2026-10-28  
**Date drafted:** 2026-10-28

## 1. Research question

Under background-only dimuon spectra, how does the global false-positive probability of a prespecified bump-hunt procedure change when (a) the background-generating process is outside the fitted model family and (b) the analyst selects a background model from the same spectrum being scanned?

This study concerns statistical calibration under specified simulations. It does not establish trigger efficiency, detector performance, the presence of a resonance, or a new particle.

## 2. Primary estimand

For each prespecified background-generating scenario and analysis procedure, estimate

\[
p_{\mathrm{global}}=P_{H_0}(T_{\max}\ge c),
\]

where each pseudo-experiment repeats the complete fitting, background-model selection, mass-window scan, and maximum-statistic calculation. The threshold \(c\) must be determined using a separate calibration sample and then frozen before evaluation on held-out generators.

Report the empirical rate, a two-sided 95% Wilson interval, number of generated pseudo-experiments, number and fraction of failed fits, and the exact rule used to handle failures. Never silently drop failures.

## 3. Analysis procedures to compare

Compare only after implementing and unit-testing the exact algorithms:

1. **Fixed model:** one prespecified background functional form and order.
2. **Data-selected order:** a prespecified order-selection rule, including all thresholds and tie handling.
3. **Declared-family profiling/selection:** a finite, prespecified family with a fully specified penalty or profiling statistic.

These are candidate procedures, not a claim that any is superior. The precise functional forms, parameter bounds, fit ranges, likelihood, and model-selection rule are unresolved protocol fields and must be fixed before confirmatory generation.

## 4. Null-generating scenarios and leakage prevention

Create a declared set of background-only generators, with parameters and normalization ranges specified before simulation. Partition generator families into:

- **Development:** used for implementation and debugging only.
- **Calibration:** used to choose the global threshold for each declared procedure.
- **Held-out evaluation:** used once for the confirmatory false-positive estimate; no retuning after results are viewed.

At least one held-out family should be deliberately outside the fitted candidate family. Do not use held-out evaluation results to change models, thresholds, ranges, or failure rules. If changes are necessary, label the resulting analysis exploratory and create a new untouched evaluation design.

Do not call a generator “realistic” without external justification. Initially this is a controlled statistical experiment whose conclusions are conditional on the declared generator suite.

## 5. Scan and test statistic

Before generating confirmatory pseudo-experiments, specify:

- mass range and binning;
- allowed window widths and positions, including endpoint rules;
- minimum expected background or event-count requirements;
- likelihood and nuisance-parameter treatment;
- local statistic and its sign/one-sidedness;
- optimization failure criteria;
- definition of the global statistic, preferably the maximum of the declared local statistic over every eligible scan position and model-selection step.

The entire selection and scan must be repeated inside each replicate. A collection of local p-values is not a global calibration result.

## 6. Calibration and evaluation

Use independent random streams and recorded seeds for development, calibration, and evaluation. Determine the critical threshold from the calibration distribution of the global statistic using a quantile convention specified in advance. Freeze that threshold before evaluating held-out pseudo-experiments.

For a target global false-positive rate of 0.05, 10,000 independent held-out replicates yield an approximate standard error of 0.00218 and a rough 95% normal margin of 0.0043 when the true rate is near 0.05. Use Wilson intervals for reporting; this planning approximation does not account for multiplicity across scenarios or paired contrasts.

The primary unit is a complete pseudo-experiment, not a mass bin or scan window. Do not treat windows from the same spectrum as independent observations.

## 7. Fit failures and diagnostics

Prespecify:
- what constitutes a failed or non-converged fit;
- whether the primary conservative analysis counts any unusable replicate as a false positive, as a failure, or under another justified rule;
- sensitivity analyses under alternative defensible failure handling;
- reporting of convergence status, boundary hits, invalid likelihoods, and scan coverage.

Always publish the generated-replicate denominator, completed-fit denominator, and failure rate separately. A procedure must not appear better because it fails more often.

## 8. Comparisons and uncertainty

Primary comparison: difference in held-out global false-positive rates between each adaptive procedure and the fixed-model comparator within the same generator scenario. Use common pseudo-experiment seeds where pairing is meaningful, and compute uncertainty for paired differences using a method fixed before evaluation. Report scenario-specific results rather than pooling away failures in difficult generators.

Control or explicitly label multiplicity for the family of procedures and generator scenarios. Do not select only favorable scenarios for the headline result.

## 9. Reproducibility artifacts

Retain:
- protocol version and source commit;
- environment/package lock and platform details;
- all configuration files and seeds;
- per-replicate generator, parameters, fit status, selected model, scan statistic, and failure reason;
- calibration thresholds and their derivation;
- summary tables and interval calculations;
- deterministic reconstruction checks and hashes for generated artifacts.

Use small deterministic tests to verify the statistic, scan boundaries, quantile convention, Wilson interval implementation, and failure accounting before large runs.

## 10. Go/no-go gates

**Gate A — software:** unit tests and small deterministic examples pass; failure paths are exercised.

**Gate B — protocol:** all unresolved choices in Sections 3–8 are fixed in a versioned configuration reviewed before confirmatory generation.

**Gate C — provenance:** the selected input/simulation configuration, dependency environment, seeds, and output manifest are recorded.

**Gate D — real-data baseline:** bounded candidate/reference histogram parity is established on the intended CERN file and event prefix, with identical selection and binning. This gate validates the reconstruction only; it does not validate trigger efficiency or scientific novelty.

**Gate E — confirmatory simulation:** run only after Gates A–C and the declared analysis review; preserve the held-out evaluation set.

No large or costly workflow should be dispatched until its exact input, resource bounds, outputs, and approval are explicit.

## 11. Current blockers

- Real CERN candidate/reference parity has not been established.
- The supported ROOT environment has not yet been substituted and tested against the synthetic fixture.
- The precise generator families, fit functions, scan range/windows, test statistic, calibration quantile, and failure policy are not yet frozen.
- A literature review has not established that this exact question is novel.

## 12. Interpretation boundaries

A calibrated simulation result would support a statement about the tested procedures under the tested generators. It would not, by itself, prove the true background of CMS data belongs to those generators, establish trigger validity, claim a resonance, or establish publication novelty. Any publication-level claim requires expert review and a documented comparison with prior bump-hunting literature.

## Pre-run checklist

- [ ] Specify and justify each background generator and parameter range.
- [ ] Freeze all fitted models, parameter bounds, and selection rules.
- [ ] Freeze mass scan and global statistic.
- [ ] Freeze threshold calibration and quantile convention.
- [ ] Freeze fit-failure handling and sensitivity analyses.
- [ ] Freeze replicate counts, seeds, and stopping rule.
- [ ] Validate code on hand-checkable toy examples.
- [ ] Complete bounded real-data parity and environment audit.
- [ ] Obtain review before confirmatory execution.
