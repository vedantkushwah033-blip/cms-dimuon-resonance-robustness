# Kinematics validation note

## Purpose
The first executable scientific component is a vectorized invariant-mass calculation. It is a kinematic utility only; it is not a complete CMS analysis and does not establish trigger correctness, data quality, selection validity, or research novelty.

## Formula
For each muon, with transverse momentum $p_T$, pseudorapidity $\eta$, azimuth $\phi$, and mass $m$:

- $p_x=p_T\cos\phi$
- $p_y=p_T\sin\phi$
- $p_z=p_T\sinh\eta$
- $E=\sqrt{(p_T\cosh\eta)^2+m^2}$

For two muons, the pair invariant mass is

$$
m_{\mu\mu}=\sqrt{(E_1+E_2)^2-(p_{x,1}+p_{x,2})^2-(p_{y,1}+p_{y,2})^2-(p_{z,1}+p_{z,2})^2}.
$$

The implementation clips tiny negative mass-squared values to zero to avoid floating-point artefacts. Inputs must use consistent momentum units, normally GeV.

## Automated checks
The unit tests cover:
- A back-to-back massless pair with equal transverse momentum, whose invariant mass is analytically $2p_T$.
- A collinear massless pair, whose invariant mass is zero.
- Vectorized broadcasting.
- A zero-momentum pair with nonzero particle mass.
- Rejection of negative/non-finite inputs.

## Independent validation still required
Before using this function for CMS data:
1. Compare event-level results against an independently implemented four-vector calculation or a trusted ROOT/TLorentzVector-equivalent implementation.
2. Check branch names, units, array lengths, muon multiplicities, and charge values in the actual input files.
3. Test edge cases with real event records and compare the mass spectrum with the official reference output.
4. Document any binning or selection differences. Agreement in a toy unit test alone does not validate the full analysis.
