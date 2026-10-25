# Experiment protocol template

**Complete and review this document before the main simulation.**

## Identity and versions
- Protocol version:
- Date frozen:
- Code commit:
- Python/dependency environment:
- Data record, version and file checksums:
- Responsible author(s):
- Independent reviewer, if any:

## Scientific question
- Primary question:
- Primary estimand:
- Why this is not already answered by the closest prior work:
- Scope of inference and explicit exclusions:

## Observed data
- Dataset and DOI:
- Collision period, certification and luminosity source where applicable:
- Trigger paths and threshold/turn-on considerations:
- Object selection and mass range:
- Event-level variables available:
- Baseline reproduction target:
- Known artifacts and their interpretation:
- Data classes: observed data / detector simulation / model pseudoexperiment / stress test:

## Statistical procedure
- Fixed mass test or scan:
- Background-generating families and parameter values:
- Fitted null and signal-plus-background models:
- Nuisance-parameter treatment and refitting policy:
- Signal shape, if applicable:
- Test statistic and its direction:
- Nominal alpha values and why feasible:
- Binning or unbinned likelihood and justification:
- Optimizer, convergence checks and boundary handling:
- Fit failure definition and prespecified treatment:
- Multiplicity/global-significance procedure, if any:

## Scenarios and separation
- Baseline null scenario:
- Prespecified misspecification scenarios:
- Scientific justification for each scenario:
- Development scenarios:
- Held-out evaluation scenarios:
- Scenario labels and parameter ranges:
- Any scenario excluded before outcome inspection and reason:

## Monte Carlo plan
- Number of trials per scenario and precision justification:
- Random number generator and seed policy:
- Independent stream strategy:
- Stopping rule, if any, fixed in advance:
- Runtime pilot result and hardware/software:
- Exact interval method:
- Handling of invalid fits:
- Criteria for expanding simulation count:

## Outcomes
- Primary metric:
- Secondary metrics:
- Calibration-failure threshold:
- Diagnostic definition and threshold:
- Coverage or bias targets, if used:
- Multiplicity correction for secondary comparisons:
- Planned tables and figures:

## Validation
- Unit and property tests:
- Known-case calibration checks:
- Independent implementation/check:
- Sensitivity analyses:
- Clean-environment reproduction:
- Independent reviewer task and recorded outcome:

## Reporting commitments
- Report all prespecified scenarios and failed fits.
- Distinguish exploratory from confirmatory analysis.
- Report negative and inconclusive results.
- Do not change the primary estimand after inspecting results without explicitly labelling the change exploratory.
- Do not claim particle discovery, global significance, five-sigma calibration, originality, or external endorsement unless separately supported.
