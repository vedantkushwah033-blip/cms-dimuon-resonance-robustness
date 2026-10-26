# Reference-baseline comparison: public CMS dimuon example

**Status:** code comparison completed; numerical reproduction not yet completed.

## Primary reference

The public CMS Open Data analysis repository is:
https://github.com/cms-opendata-analyses/DimuonSpectrumNanoAODOutreachAnalysis

Its Python implementation (`dimuonSpectrum.py`) constructs an `Events` RDataFrame from the 2012 reduced muon-only outreach file and applies these steps:

1. Select events with exactly two muons (`nMuon == 2`).
2. Select opposite-charge pairs.
3. Compute the dimuon invariant mass using ROOT's `PtEtaPhiMVector`.
4. Fill a 30,000-bin histogram from 0.25 to 300 GeV.
5. Plot logarithmic x and y axes.
6. Print the selection cut-flow report.

The published analysis record warns that the structure near 30 GeV is a trigger/data-taking effect, not a resonance:
https://opendata.cern.ch/record/cms-12342

The outreach dataset record lists only muon multiplicity, kinematics, and charge and explicitly says the reduced output was not further validated:
https://opendata.cern.ch/record/12341

## Implementation alignment

The repository's baseline script now defaults to the reference's exactly-two-muon opposite-charge selection using scalar `nMuon == 2`, checks `nMuon` against the `Muon_pt` collection length and all other muon-branch collection lengths per event, and uses 30,000 bins, a 0.25–300 GeV mass range, and logarithmic axes. It retains a separately labelled `all-opposite-charge-pairs` option for exploratory work. It writes CSV counts and run metadata as well as a PNG plot.

The Python implementation uses Uproot/Awkward and NumPy rather than ROOT RDataFrame. This is an independent software implementation, but it is not a reproduction until the actual input data are processed and the histogram is compared quantitatively with the reference.

## Histogram edge-semantics audit

The baseline now explicitly uses the half-open interval `[mass_min, mass_max)`: values exactly at the configured upper edge are overflow, consistent with ROOT histogram convention. A shared helper counts non-finite masses separately and enforces the accounting invariant `total = nonfinite + below + in-range + at-or-above-upper-edge`. The upper-edge case is covered by `tests/test_histogram.py`. This fixes an implementation risk where NumPy's default final-bin behavior can otherwise include a value equal to the final edge, unlike ROOT. This software-level correction is necessary but does not establish numerical agreement with the official spectrum.

## Remaining reproduction checks

- Inspect the exact input file's schema and record its official dataset identifier.
- Run the script with the default reference-aligned selection and all required events.
- Compare histogram binning, event counts, low-mass threshold, log axes, and cut flow against the public example.
- Investigate differences in pair-mass computation and floating-point precision.
- Explain the known trigger-related feature without treating it as a resonance.
- Preserve run metadata, package versions, input checksum/URL, and comparison metrics.
- Do not claim the 11.6 fb^-1 figure from the reference plot is the integrated luminosity of a sample unless the data record and selection support that interpretation.

## Important limitation

The reference uses an educational muon-only derived file. This is suitable for reproducing that example, but the record says no further validation was performed on the reduced output. It does not establish trigger-efficiency or prescale modelling. A separate research-level data record requires a separate file-level audit.


## Machine-readable parity audit hardening

The end-to-end metadata audit (`scripts/audit_baseline_metadata.py`) supplements bin-by-bin histogram comparison with explicit checks that the candidate used the reference-aligned `exactly-two-opposite-charge` selection and that the reference opposite-sign event count equals the candidate opposite-charge-pair total. Under the exactly-two-muon selection, each opposite-sign event contributes one pair, including pairs whose mass is later classified as non-finite or outside the histogram range. The audit also validates checksum syntax, positive integer input sizes, and integer types for event/pair counts so malformed metadata cannot pass merely because Python considers values such as `40.0` equal to `40`.

Regression tests cover the wrong selection mode, opposite-sign cut-flow disagreement, malformed matching checksums, nonpositive file size, and float-encoded counts. These tests validate the audit's software contract only. The audit must be run on actual reference and candidate outputs before any parity claim; synthetic fixtures are not evidence of real-data reproduction.

The histogram-report flags `bin_edges_exactly_equal` and `exact_bin_by_bin_parity` are now validated as actual JSON booleans. This avoids Python's permissive equality (`1 == True`) allowing malformed numeric values to pass a parity gate. Regression tests cover integer, float, string, null, list, and mismatched boolean values.

The audit also requires the reference, candidate, and histogram-report bin counts to be positive JSON integers. Matching string values such as `"30000"` are rejected instead of passing equality checks without satisfying the metadata schema. An integration test checks both a valid minimal audit and the malformed matching-string case.

Mass-range metadata is schema-checked as well: bounds must be finite JSON numbers, and both reference and candidate ranges must satisfy `0 < minimum < maximum`. Matching string-encoded bounds are rejected. This prevents equality alone from treating malformed metadata as a valid reproducibility record.

The audit also validates that both metadata tree identifiers are non-empty strings; identical malformed values such as numeric tree identifiers cannot pass solely because they compare equal. The integration tests cover this case alongside the count and mass-range schema checks.

## Full-data and pair-accounting acceptance gates

The metadata audit now refuses to accept a partial event scan as a full-data reproduction: `events_read` must equal the reference tree's total entry count, `events_processed` must equal `events_read`, and `max_events` must be absent or at least the full reference event count. This prevents a smoke-test run from being accidentally presented as a full-data parity run.

The candidate pair-accounting audit also verifies conservation across in-range, below-range, overflow, and non-finite mass categories. Their sum must equal `opposite_charge_pairs_total`, and all inputs must be nonnegative JSON integers. Malformed values are reported as failed checks instead of causing arithmetic exceptions. Regression tests cover a partial run, a deliberately inconsistent accounting total, and a malformed string count.
Additional physical-count invariants are checked: exactly-two-muon events cannot exceed all events; opposite-sign events cannot exceed exactly-two-muon events; selected events cannot exceed events read; and, under the exactly-two selection, opposite-charge pairs cannot exceed selected events. These guards catch internally impossible but mutually matching metadata before a parity report is accepted.

The reference-side audit also checks that ROOT's recorded histogram entry count (including flow entries) matches the opposite-sign event cut-flow count. Under the exactly-two-muon selection, each opposite-sign event contributes one histogram fill; disagreement therefore flags a cut-flow or metadata inconsistency before candidate parity is accepted.


## Independent reference implementation precision

The optional ROOT-based exporter now returns the reference four-vector invariant mass as a C++ `double`, rather than narrowing it to `float` after the calculation. Input NanoAOD branches may be stored as float32, but retaining double precision for the computed mass avoids an unnecessary second quantization before narrow-bin histogramming. This is a numerical hygiene improvement, not evidence of parity; the PyROOT reference and Uproot candidate still need to be run on the same actual input file and compared.
