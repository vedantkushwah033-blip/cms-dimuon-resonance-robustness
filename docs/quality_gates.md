# Quality gates for a credible research contribution

These gates are a checklist, not a guarantee of publication or admissions outcomes.

## Gate 1 — literature and novelty
- Build a comparison table of closest prior studies: question, dataset, selection, statistic, null generation, scenarios, metrics, and limitations.
- Read methods and supplements, not only abstracts.
- Identify the exact methodological difference and why it is not already answered.
- If no meaningful difference remains, stop or reframe before spending compute.

## Gate 2 — data validity
- Reproduce a public reference spectrum from a documented dataset.
- Explain triggers, data-quality certification, prescales/turn-on, object selection, units, and known artifacts.
- Verify event-level invariant mass independently and test edge cases.
- Do not infer detector-level realism from a simple parametric toy model.

## Gate 3 — statistical validity
- Freeze the primary estimand, alpha, test statistic, fit range, models, convergence policy, and exclusions before main runs.
- Validate the implementation on known cases and independent implementations where feasible.
- Use exact binomial confidence intervals for empirical rejection rates.
- Separate parameter-fitting uncertainty from Monte Carlo uncertainty.
- Keep development and held-out stress scenarios distinct.
- Report fit failures, boundary hits, coverage, and every prespecified scenario, including negative results.

## Gate 4 — independent reproducibility
- Clean-environment setup works from documented commands.
- Automated tests and continuous integration pass.
- An independent person can reproduce key tables and figures from scripts and configuration.
- Random seeds and run metadata are recorded; outputs are traceable to input and code versions.

## Gate 5 — communication and external review
- Paper distinguishes prior work, method, results, assumptions, limitations, and contribution.
- No claims exceed the design, especially global significance or five-sigma calibration.
- Seek technical critique from a knowledgeable researcher or statistician if available; do not imply endorsement without explicit permission.
- Choose a venue based on scope and quality, not prestige alone.

## Admissions framing
The work is compelling when the student can explain their own decisions, code, uncertainty calculations, failed approaches, and limitations. A paper label or repository activity alone is not proof of research depth. No numerical extracurricular rating predicts admission to a particular university.
