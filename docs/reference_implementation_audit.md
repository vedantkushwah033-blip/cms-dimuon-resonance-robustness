# Audit of the official dimuon outreach reference implementation

**Status:** source-code audit only. No CMS ROOT input has been processed in this project as part of this audit, and no numerical agreement is claimed.

## Audited reference

The official CMS Open Data outreach repository is:
https://github.com/cms-opendata-analyses/DimuonSpectrumNanoAODOutreachAnalysis

The inspected Python script is:
https://github.com/cms-opendata-analyses/DimuonSpectrumNanoAODOutreachAnalysis/blob/master/dimuonSpectrum.py

It opens the reduced Run2012BC muon-only ROOT file, filters events with exactly two muons, filters the two muons by charge inequality, computes the mass using ROOT's `PtEtaPhiMVector`, and fills a 30,000-bin histogram over 0.25–300 GeV.

## Equivalence checklist

| Component | Reference | Project implementation | Audit conclusion |
|---|---|---|---|
| Tree | `Events` | configurable tree, default `Events` | Same default; must verify actual file |
| Exactly two muons | `nMuon == 2` | `nMuon == 2`, after checking it equals `len(Muon_pt)` event-by-event | Directly follows reference scalar selection and fails on multiplicity disagreement |
| Opposite sign | `Muon_charge[0] != Muon_charge[1]` | product of charges < 0 | Equivalent only when charges are exactly +1 or -1; input-domain validation now enforces this |
| Four-vector mass | ROOT `PtEtaPhiMVector` | explicit cylindrical-coordinate four-vector | Independent cross-implementation test passes on synthetic events; not yet compared on real events |
| Histogram | 30,000 bins, 0.25–300 GeV | same defaults | Same configured range/bin count |
| Display | logarithmic x and y | logarithmic x and y | Similar intent; styling is not a numerical validation |
| Cut-flow report | ROOT report for both filters | metadata event counts | Project metadata should be compared against actual reference cut-flow output |

## Charge-selection caveat

A generic predicate `q1 * q2 < 0` is not identical to `q1 != q2` for arbitrary malformed charge values. For example, a charge of zero differs from +1 but is not opposite-sign. Physical reconstructed muon charges should be -1 or +1. The project now fails explicitly if other values occur, rather than silently changing the reference's meaning.

The baseline runner now checks the scalar `nMuon` branch against the jagged `Muon_pt` count and checks all four other muon collections against `Muon_pt` for every event before selection. It reports the first global event index and observed counts on disagreement. The guard does not prove the source file is valid; it makes an assumption visible and testable.

## Required real-data parity run

Once the official ROOT file is available locally, run both implementations with the same input and compare:
1. Total entries read.
2. Number of events with exactly two muons.
3. Number of opposite-charge events after the second filter.
4. Underflow, every regular histogram bin, and overflow.
5. Mass values for a fixed sample of events, including values near bin boundaries.
6. The output from the reference cut-flow report and the project's metadata.

A plot that looks similar is insufficient. The comparison should report exact count differences and a checksum of the input. Any discrepancy must be explained before claiming reproduction.

## Scope limits

The reduced muon-only outreach dataset is appropriate for reconstructing the documented spectrum, subject to the dataset's stated limitations. This audit does not establish trigger efficiency, data-quality selection, integrated-luminosity normalization, or a new-physics result. Such claims require suitable inputs and separate validation.
