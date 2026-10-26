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

The repository's baseline script now defaults to the reference's exactly-two-muon opposite-charge selection using scalar `nMuon == 2`, checks `nMuon` against the `Muon_pt` collection length per event, and uses 30,000 bins, a 0.25–300 GeV mass range, and logarithmic axes. It retains a separately labelled `all-opposite-charge-pairs` option for exploratory work. It writes CSV counts and run metadata as well as a PNG plot.

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
