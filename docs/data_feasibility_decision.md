# Data feasibility decision memo

**Date:** 2026-10-26  
**Decision status:** no trigger-aware inference is approved yet; inspect actual files before selecting a primary dataset.

## Why the dataset labels matter

Three similarly named public resources must not be conflated:

1. **The 2019 reduced muon-only outreach file** ([record 12341](https://opendata.cern.ch/record/12341)) contains 61,540,413 events in a 2.1 GiB file and lists muon kinematics and charge. Its record explicitly says the reduced output was not further validated. This is useful for developing pair-mass code, but its listed schema does not establish trigger, prescale, or event-quality availability.
2. **A separate 2021 Run2012C reduced outreach file** ([record 12366](https://opendata.cern.ch/record/12366)) contains 35,455,705 events in a 4.2 GiB file and lists run/luminosity-block/event identifiers plus muon quality and isolation variables. This richer listed schema still does not, by itself, establish that trigger decision bits or prescales are included.
3. **The Run2012B/Run2012C research-level NanoAOD-like records** ([Run2012B record](https://opendata.cern.ch/record/cms-31123), [Run2012C record](https://opendata.cern.ch/record/cms-31129)) are distinct derived datasets. The portal describes validated-run processing but warns that not all variables are available. Record-level documentation is not proof of the exact branches in the file we will use.

The official CMS trigger guide explains that trigger decisions, trigger-object information, and prescales are separate pieces of information; availability depends on the data format and era. A stored HLT decision bit is not a measurement of trigger efficiency and does not automatically supply prescale weights. See [CERN's CMS trigger guide](https://opendata.web.cern.ch/docs/cms-guide-trigger-system).

## Required file-level audit

For one exact file from each candidate we seriously consider:

- Record the official file URL, record identifier, size, and checksum if provided.
- Inspect all ROOT trees and exact branch names.
- Confirm event identifiers, muon kinematics, charge, quality/isolation, HLT decision bits, and any prescale/trigger-menu metadata.
- Cross-reference branch meanings and trigger paths with the era-specific CMS documentation.
- Check whether the original published analysis selection can be reconstructed from the released variables.
- Keep a table with status **present / absent / ambiguous / not checked**, and a citation for every semantic interpretation.

Do not infer that the research-level Run2012C file has a branch solely because a separate reduced Run2012C outreach record lists it.

## Scope decision rules

**Route A — full trigger-aware study:** proceed only if exact files, trigger definitions, data-quality information, and any necessary prescale/efficiency inputs are demonstrably sufficient and the original analysis selection is reproducible.

**Route B — selection-aware spectrum robustness without trigger-efficiency claims:** if the available data support muon selection and spectrum checks but not a defensible trigger model, restrict real-data analysis to validated spectrum reconstruction and test calibration using clearly labelled model-generated pseudoexperiments. State that the toys do not reproduce the detector trigger.

**Route C — reproducibility study:** if neither the selection nor the reference spectrum can be reconstructed, focus on independently reproducing the public example and documenting limitations; do not describe the result as a novel trigger-robustness method.

## Go/no-go

No full simulation campaign starts until the chosen route is documented, the closest literature is compared method-by-method, and a protocol fixes the primary estimand, test statistic, fit-failure handling, scenarios, and held-out evaluation plan. A no-go result is preferable to unsupported claims.
