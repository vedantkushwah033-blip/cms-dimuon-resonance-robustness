# Dimuon event-selection and pair-counting contract

**Status:** software contract documented; no real CMS file has yet been validated by this repository.

## Why this distinction matters

There are two different operations:

1. **Select events:** decide which collision events enter the sample.
2. **Select pairs:** within each selected event, form opposite-charge muon pairs and calculate each pair's invariant mass.

They are not interchangeable. If an event contains three muons with charges (+1, -1, +1), it contains two opposite-charge pairs. Counting both pairs changes the statistical unit and can introduce correlated entries from the same event. Treating each pair as independent in a later statistical model would then be unjustified unless that dependence is handled explicitly.

## Implemented modes

### `exactly-two-opposite-charge` (default)

- Event selection: `nMuon == 2`.
- Pair selection: the two muons must have opposite charge.
- A selected event contributes either zero or one pair.
- This mode is intended to align with the public CMS outreach example's exactly-two-muon event selection.
- It is the only current mode suitable for a direct cut-flow comparison with that reference.

### `all-opposite-charge-pairs`

- Event selection: all events in the input tree.
- Pair selection: all opposite-charge pairs in each event.
- A multi-muon event can contribute more than one histogram entry.
- This is an exploratory spectrum definition, not a parity reproduction of the outreach example.

Run the mode explicitly and preserve the generated `run_metadata.json`:

```bash
python scripts/reproduce_dimuon_spectrum.py --input /path/to/sample.root --selection exactly-two-opposite-charge
python scripts/reproduce_dimuon_spectrum.py --input /path/to/sample.root --selection all-opposite-charge-pairs --output-dir outputs/all_pairs
```

## Invariants checked by integration tests

A synthetic three-event sample contains:
- one two-muon opposite-sign event;
- one three-muon event with two opposite-sign pairs;
- one two-muon same-sign event.

The expected outcomes are:

| Quantity | Exactly-two mode | All-pairs mode |
| --- | ---: | ---: |
| Events read | 3 | 3 |
| Events selected before charge requirement | 2 | 3 |
| Events containing at least one opposite-charge pair | 1 | 2 |
| Opposite-charge pairs | 1 | 3 |

The run metadata records both `events_selected` (the event-multiplicity selection) and `events_with_opposite_charge_pair` (an event-level count after pair construction). These are intentionally distinct from `opposite_charge_pairs_total`, which counts pair-level entries. These are software-contract tests, not measurements from CMS data.

## Statistical consequences

Before fitting a background or calibrating a test statistic, the analysis protocol must identify its unit of sampling and inference. If the intended observation is an event-level count, pair-level entries from multi-muon events are clustered and cannot automatically be treated as independent. A primary analysis must therefore freeze the event selection, pair construction, fit range, histogram binning, background family, test statistic, and pseudoexperiment generation before inspecting final calibration outcomes.

## Limitations

- This script reconstructs a kinematic spectrum; it does not implement the trigger, certified-lumisection, object-quality, isolation, or full physics selections required for a detector-level search.
- The educational muon-only dataset is documented as not further validated after reduction. Use it for reference reproduction only with that limitation stated.
- The research-level Run2012B/C files need file-level schema and selection audits before use.
- Matching the reference selection is necessary but not sufficient for reproduction; actual histogram/cut-flow parity remains unverified.
