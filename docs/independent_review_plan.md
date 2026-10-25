# Independent technical review plan

**Status: planned; no independent review has occurred yet.**

The goal is to make the work falsifiable and inspectable, not to imply endorsement.

## Review package
Provide a reviewer with:
- The frozen protocol and a concise methods note.
- Related-work matrix with primary-source citations.
- Reproducible environment and exact commands.
- A small, versioned example input and expected outputs.
- Tests and continuous-integration status.
- Simulation configuration, seed policy, fit-failure accounting and generated summaries.
- Main claims paired with the exact table/figure and uncertainty estimate supporting each claim.

## Review questions
1. Does the stated research gap differ materially from the closest prior work?
2. Does the data selection support the claimed inference?
3. Are generating and fitted models defined correctly and transparently?
4. Is nuisance-parameter refitting handled consistently in each pseudoexperiment?
5. Are nominal rejection rates calibrated under the well-specified null within expected Monte Carlo uncertainty?
6. Are stress-test departures scientifically justified and kept separate from held-out validation?
7. Are failed fits, boundary hits, exclusions and all prespecified scenarios reported?
8. Are confidence intervals and multiplicity/global-significance statements appropriate?
9. Can the reviewer reproduce at least one baseline figure and one primary result from a clean environment?
10. Do the conclusions remain within the scope of the experiment?

## Recording feedback
For each comment, record: reviewer question, code/data/protocol version, severity, response, changes made, and whether the comment remains unresolved. Do not identify a reviewer publicly or claim endorsement without their explicit permission.

## Independence standard
A self-review or an automated test is not independent technical scrutiny. Ideally, ask a researcher/statistician with relevant expertise to inspect a defined subset of the work. If no external reviewer is available, label the limitation honestly and use independent implementations, known-case tests, and reproducibility checks as partial safeguards—not as equivalent substitutes.
