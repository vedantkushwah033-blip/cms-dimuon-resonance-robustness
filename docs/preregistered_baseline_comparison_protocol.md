# Preregistered baseline comparison protocol

**Status:** defined before the real-data comparison. No observed CMS comparison result is claimed.

## Purpose

Determine whether the repository's Uproot/Awkward implementation reproduces the public CMS 2012 dimuon outreach example. This is a software/reference-parity check, not a discovery test or trigger-efficiency measurement.

Primary reference:
- Official source: https://github.com/cms-opendata-analyses/DimuonSpectrumNanoAODOutreachAnalysis/blob/master/dimuonSpectrum.py
- Analysis record: https://opendata.cern.ch/record/12342
- Dataset record: https://opendata.cern.ch/record/12341

## Frozen reference definition

The official script reads the `Events` tree from `Run2012BC_DoubleMuParked_Muons.root`, selects `nMuon == 2`, selects `Muon_charge[0] != Muon_charge[1]`, computes mass using ROOT `PtEtaPhiMVector`, and fills 30,000 bins over [0.25, 300.0] GeV. Its helper returns a C++ `float`; the ROOT histogram uses ROOT's underflow/overflow semantics and its RDataFrame reports cut flow.

The candidate uses Uproot/Awkward and a Python mass calculation. Before selection, it checks that `nMuon` agrees with the `Muon_pt` collection length and that all other required muon collections have matching per-event lengths. These are data-integrity checks, not additional physics selections.

## Comparison procedure

1. **Freeze provenance.** Record official record IDs, exact input URL, local byte size and SHA-256, tree name and entry count, repository commit, command line, Python and package versions.
2. **Smoke test.** Process the first 10,000 events; verify outputs and accounting identities; record whether any integrity guard fires. This is not the full reproduction.
3. **Export reference outputs.** Run the official script on the exact same input and make only the output-plumbing changes needed to export histogram bin edges, integer bin counts, and cut-flow counts. Preserve the original selections, mass helper, binning and ROOT histogram. Archive the minimal patch/diff. A plot alone is insufficient.
4. **Run full candidate analysis.** Use the same file, full event range, tree, selection, mass range and bin count. Preserve metadata.
5. **Compare cut flow and accounting.** Compare total tree entries, events processed, exactly-two-muon count, opposite-charge selected-event count, opposite-charge pairs, in-range counts, underflow, overflow and non-finite handling where available. Align each count with the reference's exact filter stage.
6. **Compare every bin.** Verify all bin edges; report number of differing bins, total absolute bin-count difference, maximum absolute bin difference, and the intervals of every differing bin. Do not compare only plots or normalized shapes.
7. **Diagnose all differences.** Investigate selection/count differences first; then compare masses for identical events and inspect numerical precision and bin-edge migration. The reference returns a C++ `float`, while the candidate may retain higher precision, so exact bin parity cannot be assumed before measurement. Do not silently widen tolerances or omit inconvenient bins.
8. **Record disposition.** Classify as exact parity, explained numerical differences, unresolved discrepancy, or failed reproduction. Preserve comparison tables and scripts.

## Acceptance criteria

- **Required:** exact input provenance and same tree/file; integrity checks pass; event-selection and opposite-charge counts agree; bin edges and ROOT-compatible range semantics align; accounting closes without unexplained loss.
- **Target:** exact integer equality in every histogram bin.
- **If target fails:** no pass based on visual similarity. Localize discrepancies to events/bins and explain them reproducibly. Any tolerance must be justified from measured mass differences and bin widths and documented before it is used to decide pass/fail; it must not conceal selection errors.
- Visual resemblance, qualitative resonance patterns, or a p-value treating the reference plot as independent data are not acceptance criteria.

## Reporting checklist

Report input URL and record IDs, byte size, SHA-256, tree entries, processed events, commit and environment; reference and candidate cut-flow counts; total opposite-charge pairs and range/overflow/non-finite accounting; number of differing bins and difference metrics; numerical precision effects; final disposition and unresolved limitations.

## Limitations

The CMS record describes an educational muon-only derived output that was not further validated. Agreement establishes parity with that example, not trigger/prescale modelling, event-quality certification, or a novel physics result. The public record warns that the feature near 30 GeV is a trigger/data-taking effect, not a resonance.
