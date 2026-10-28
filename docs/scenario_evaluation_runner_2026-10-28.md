# Scenario-level evaluation runner

**Status:** orchestration utility; not a frozen confirmatory design and not CMS validation.

`evaluate_null_scenarios` accepts a mapping from scenario names to fully specified expected-count vectors, a common scan/calibration configuration, and a distinct calibration/evaluation seed pair per scenario. It calls the existing held-out refitted-background evaluator for each scenario and returns a machine-readable result structure containing the design, the expected means, and the per-scenario rejection fraction and Wilson interval.

The runner deliberately does not invent default parameter values or infer physical plausibility. It checks that means are finite and positive, all scenarios use the same number of bins, scenario keys match the seed map, and all seeds are unique across calibration/evaluation roles. Common binning is a comparability guard: changing the bin count changes the candidate-window set and the null distribution of the maximum scan statistic. The returned rows should be exported with the exact commit SHA, package versions, and the frozen protocol.

## Interpretation
- Each rejection fraction pertains only to its specified generating mean vector, fit order, scan widths, and sample sizes.
- Per-scenario Wilson intervals describe Monte Carlo uncertainty, not uncertainty about whether the scenario represents CMS data.
- Multiple scenarios do not establish uniform type-I error control. A good result for the matched scenario does not validate misspecified scenarios.
- Fit failure policy remains fail-fast in the underlying evaluator; failures must be investigated and documented rather than silently excluded.
- This function only defines a reusable execution path. It does not itself launch simulations or authorize confirmatory runs.
