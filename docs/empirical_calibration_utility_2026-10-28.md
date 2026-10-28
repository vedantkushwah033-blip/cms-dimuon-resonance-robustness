# Empirical calibration utility — implementation note

**Status:** mathematical helper only; not an end-to-end calibration pipeline. Date: 2026-10-28.

The new `src/cms_dimuon_robustness/calibration.py` function computes a Monte Carlo upper-tail rank p-value from supplied null statistics:

`p = (1 + number of null statistics >= observed statistic) / (M + 1)`

Ties are counted in the upper tail. The smallest representable value is `1/(M+1)`. The function returns the p-value, exceedance count, calibration sample size, and resolution.

## Scientific assumptions

This calculation is interpretable only if the calibration statistics come from a defensible null-generating mechanism and rerun the same frozen analysis pipeline as the observed statistic, including any background fit, adaptive model choice, scan, and failure handling. Calibration and held-out evaluation data must remain separate. Tail precision requires enough replicates; a small calibration ensemble cannot support very small p-values. Failed fits need a prespecified policy.

The function does not generate pseudoexperiments, verify exchangeability, fit backgrounds, or establish type-I error. It must not be used to report a CMS discovery p-value. Unit tests have been added but must pass CI before the helper is considered software-verified.
