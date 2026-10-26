# Official CMS dimuon reference-code audit — 2026-10-26

**Audit type:** source-code comparison, not a numerical data reproduction.  
**Conclusion:** selection and histogram configuration align with the official outreach example at source level; numerical parity remains untested.

## Primary sources checked

- Official CMS Open Data analysis record: https://opendata.cern.ch/record/12342
- Official reference implementation, version tag `v1.4`: https://github.com/cms-opendata-analyses/DimuonSpectrumNanoAODOutreachAnalysis/blob/v1.4/dimuonSpectrum.py
- Official outreach dataset record: https://opendata.cern.ch/record/12341
- CERN CMS trigger guide: https://opendata.cern.ch/docs/cms-guide-trigger-system

The official Python reference opens the `Events` tree in the reduced 2012 Run B/C muon-only outreach file, selects `nMuon == 2`, then selects `Muon_charge[0] != Muon_charge[1]`, calculates mass from `Muon_pt`, `Muon_eta`, `Muon_phi`, and `Muon_mass` using ROOT `PtEtaPhiMVector`, fills 30,000 bins over 0.25–300 GeV, and draws both axes logarithmically. Its accompanying record explicitly warns that the feature near 30 GeV is a trigger/data-taking effect rather than a resonance.

## Source-level comparison

| Component | Official reference | Repository implementation | Assessment |
|---|---|---|---|
| Tree | `Events` | `Events` by default | Aligned by default |
| Event multiplicity | `nMuon == 2` | `exactly-two-opposite-charge` selection uses `nMuon == 2` | Aligned; implementation additionally checks `nMuon` against jagged collection length |
| Charge | Two charges differ | Physical opposite sign, after requiring charges to be exactly -1 or +1 | Equivalent for valid charge values; malformed values fail explicitly |
| Kinematics | ROOT `PtEtaPhiMVector` | Uproot/Awkward + a cancellation-resistant invariant-mass expression | Mathematically equivalent target; floating-point differences need measured comparison |
| Histogram | 30,000 linear bins from 0.25 to 300 GeV | Same default bin count and bounds | Aligned configuration |
| Edge semantics | ROOT histogram upper edge is overflow | Shared helper implements `[mass_min, mass_max)` and records overflow separately | Deliberately aligned |
| Axes | Log x and log y | Log x and log y | Aligned |
| Cut flow | ROOT RDataFrame report | JSON event/pair accounting | Comparable in principle, but must be checked on the same actual file |
| Plot annotations | CMS/luminosity and resonance labels | Generic baseline title and axis labels | Not identical; this repository does not claim exact visual reproduction |

## Findings and caveats

1. **This is not yet a reproduced result.** A source-code match cannot establish the event counts or bin contents. The exact file must be opened and the full event sample processed; the resulting histogram and cut flow must then be compared with the official reference output.
2. **A 10,000-event smoke test is not a full-data reproduction.** It can establish only that a bounded sample is readable and the software path runs.
3. **Do not use the outreach sample to claim trigger efficiency, prescale modelling, detector calibration, or a new resonance.** The source record describes it as a reduced muon-only example and warns about the trigger-related feature near 30 GeV. The trigger guide notes that path definitions are dataset- and run-dependent; the presence of a branch name alone is not validation of trigger semantics.
4. **The alternative all-pairs mode is not reference-equivalent.** It is available only as a separately named exploratory mode. Reference comparison must use `exactly-two-opposite-charge`.
5. **Mass calculation equivalence still needs empirical testing.** The implementation uses a numerically stable expression instead of ROOT's four-vector summation. A robust comparison should check pair masses near bin boundaries and report exact bin-by-bin parity, not merely visually similar plots.
6. **The reference's integrated-luminosity annotation should not be transferred to the reduced sample without a documented justification.** The code audit does not establish a luminosity normalization or a physics cross-section.

## Next acceptance gate

Once the bounded smoke test is executable, run it first and inspect schema, cut flow, accounting, and generated artifacts. A separate, explicitly reviewed full-file run is then required for numerical comparison. Keep the report marked **not reproduced** until that comparison passes. Only after data suitability and prior-work overlap are resolved should the project proceed to a larger statistical robustness study.

