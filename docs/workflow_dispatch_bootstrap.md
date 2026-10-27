# Manual workflow-dispatch bootstrap

GitHub requires a `workflow_dispatch` workflow file to exist on the default branch before it exposes the manual-run control. This change adds only a **dispatch bootstrap** to `main`; it does not merge the research implementation or start a data job.

## How it is intended to be used

1. After this small pull request is reviewed and explicitly approved for merging, open the Actions page.
2. Select **research-level CMS schema and bounded baseline audit**.
3. In the branch selector, choose `research-plan/initial-protocol`.
4. Confirm the displayed workflow run uses that branch before starting it.

The copy on `main` is intentionally a guard-only workflow and does not download data. The research branch contains the actual workflow definition and analysis scripts. If `main` is selected, the guard exits with an explanatory error.

## Scope and risk

- No automatic push or pull-request trigger is configured.
- The bootstrap has read-only repository permissions.
- It does not install dependencies, download ROOT files, run analysis, or upload artifacts.
- Selecting the research branch runs its workflow, which currently downloads one ROOT file from each of records 31123 and 31129 (each approximately 1.5 GB), then attempts a 100,000-event candidate/reference comparison for each.
- That data run may consume substantial network, disk, and runner time. It is a bounded software-parity check, not a trigger-efficiency analysis or a physics discovery.
- This pull request does **not** merge the larger draft research PR, alter analysis code on `main`, or dispatch any workflow.

No workflow is dispatched by this change. A maintainer must review and merge this bootstrap PR, and the research run must then be deliberately launched from the research branch.
