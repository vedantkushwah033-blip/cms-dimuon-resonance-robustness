# Decision log

Append material choices rather than silently rewriting past decisions.

## 2026-10-25 — Initial research-plan branch
- **Decision:** begin with research design and literature audit; do not start a large simulation campaign.
- **Reason:** prior CMS Open Data dimuon work already discusses resonance searches, local background fits, and fit-window/polynomial choices. A broad “test background models” claim would be insufficiently specific.
- **Evidence:** CMS dimuon spectrum record (Wunsch, 2019; DOI 10.7483/OPENDATA.CMS.AAR1.4NZQ); Cesarotti et al., Physical Review D 100, 015021 (2019); official CMS Open Data research guide.
- **Consequences:** question remains provisional; no novelty claim or empirical result is made.
- **Revisit when:** methods and supplementary materials of closest prior studies have been read and the exact available data and triggers are confirmed.

## 2026-10-25 — Calibration target
- **Decision:** use empirical type-I error under background-only pseudoexperiments as candidate primary outcome.
- **Reason:** it directly measures whether a specified test rejects the null at its stated rate under a defined generating scenario.
- **Caveat:** this evaluates only the chosen generator and analysis procedure. It does not prove calibration for real data or every plausible background.
- **Revisit when:** exact likelihood/test statistic and feasible nominal alpha values are specified.

## 2026-10-25 — Global significance is conditional
- **Decision:** do not promise global-significance results in the first implementation.
- **Reason:** global significance requires a clearly defined scan and a validated null distribution for the maximum statistic; it cannot be inferred from a single local fit.
- **Revisit when:** a complete scan protocol and sufficient computational plan are justified.

## 2026-10-25 — Avoid ungrounded discovery language
- **Decision:** no claim of a new particle, an anomalous CMS observation, or a universally effective diagnostic.
- **Reason:** the planned work concerns method calibration and controlled simulations.
- **Revisit when:** only if a later analysis supports a specific claim and appropriate validation and review have occurred.
