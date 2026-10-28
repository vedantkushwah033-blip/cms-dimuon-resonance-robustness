# Exploratory scan-statistic implementation note

**Status:** exploratory software component, not a frozen analysis and not a physics result.  
**Date:** 2026-10-28

## What was implemented

`src/cms_dimuon_robustness/global_scan.py` computes a one-sided Poisson likelihood-ratio statistic for upward fluctuations over every contiguous window for a user-declared set of bin widths. For a window with observed count (n) and supplied expected background (b>0),

[
q_0 = \begin{cases}
2[n\log(n/b)-(n-b)], & n>b,\\
0, & n\le b.
\end{cases}
]

The scan returns the maximum (q_0), the selected window, its observed and expected counts, and the number of windows scanned. Tests cover the formula, an injected synthetic excess, downward-only fluctuations, invalid inputs, and duplicate widths.

## Important limits

- The expected background is an input. This code does **not** fit a background model or select a model.
- This is a scan-level test statistic, not a calibrated global p-value. The maximum over many windows has a nontrivial null distribution; a threshold must be calibrated on independent null pseudoexperiments using the exact frozen scan.
- The Poisson model treats bin counts as independent conditional on the supplied means. It does not model event-level selection, detector response, trigger efficiency, or correlations induced by background fitting.
- The statistic has not been validated against BumpHunter, ROOT/CMS data, or an established analysis package.
- Do not use this exploratory implementation to report discovery significance or to make a resonance claim.

## Next tests before scientific use

1. Cross-check the likelihood-ratio expression against an independent implementation.
2. Add property-based and boundary tests, and compare with a trusted scan-level implementation.
3. Specify whether the scan windows, background mean, and test statistic match the intended scientific estimand.
4. Add null pseudoexperiment calibration only after the baseline and algorithm specification are reviewed.
5. Keep calibration and held-out evaluation samples separate, and report every failed replicate.
