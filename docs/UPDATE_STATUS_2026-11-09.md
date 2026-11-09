# Fresh Eyes update status — 9 November 2026

## Implemented and published

- Restored the handoff's `Fresh-Eyes-CDO-NCO-Workshop` source from the transferred
  updated archive and manual-upload overlay. Preserved the earlier seminar package.
- Read the updated public ESMValTool recipe at source commit
  `040b9c7962355b1f8fa1312b7af867b458102b85` in the browser.
- Implemented independent Python, CDO and NCO historical + SSP585 workflows,
  with 1979–2024 as the main period and 2100 as an optional extension.
- Staged both real ACCESS-CM2 raw files in `data/access_cm2/`, including the
  user-supplied SSP585 file, and checked their matching grids, model/member
  metadata, calendar, monthly coverage and time bounds. The input checksums and
  acquisition details are recorded in
  [real_input_receipt.json](updated_verification/real_input_receipt.json).
- Updated both teaching notebooks and the local launchers to use **real data by
  default**. Synthetic input remains an explicit software-test option; a missing
  real file stops the demonstration rather than substituting synthetic data.
- Updated the documentation, Binder build configuration and CI artifact paths.
  The former notebook sources remain under `legacy_` names.
- Reused the existing working Mac environment: CDO 2.5.0, NCO 5.3.9,
  Python 3.12.14 and JupyterLab. No new system installation or global shell
  changes were needed. The environment runs Intel binaries through Rosetta.
- Added project-root activation, notebook and batch-demo launchers.
- Launched the pinned revision on public BIDS Binder and reran the main seminar
  notebook in live Jupyter: 8 code cells, all ten real-data product comparisons
  and the final comparison figure completed successfully. The participant
  notebook then passed all 10 cells after restarting its kernel and running
  all cells in the same session; both notebooks reached Idle / 100%.
- Published the updated code on `main` at
  [fe1dc89f49a4cd32c72283056d2b5e1ce29d362b](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/commit/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b).
- Built a fresh Linux Codespace environment from `binder/environment.yml`, ran
  the Binder build procedure, executed both notebooks through `nbconvert`,
  verified the notebook source hashes and code-cell counts, and completed
  output compaction. The build and compaction records are published on GitHub.

## Execution evidence and limits

| Check | Result |
|---|---|
| Real ACCESS-CM2 1979–2024 workflow | 10 product comparisons pass; 552 months / 46 years; maximum difference 3.5527136788e-15°C |
| Real ACCESS-CM2 1979–2100 extension | 10 product comparisons pass; 1,464 months / 122 years; maximum difference 2.4868995752e-14°C |
| Main seminar notebook on Mac, real data | All 8 code cells pass; all 10 product comparisons pass; final cell stderr streams empty |
| Participant notebook on Mac, real data | All 10 code cells pass, including exercises; all 10 product comparisons pass; final cell stderr streams empty |
| Synthetic 1979–2024 software test | 10 product comparisons pass; maximum difference 8.88e-16°C |
| Synthetic 1979–2100 software extension | 10 product comparisons pass; maximum difference 3.55e-15°C |
| Legacy real ACCESS-CM2 historical workflow | 8 comparisons pass; maximum difference 2.594e-5°C |
| Repository test suite on Mac | Latest run: 12 tests passed in 8.73 seconds; one NumPy compatibility warning remained |
| Fresh Linux environment / Binder build procedure | Completed in Codespaces from `binder/environment.yml`; 8 tests pass with one NumPy compatibility warning |
| Real 1979–2024 workflow on Linux | 10 comparisons pass; maximum difference 1.50990331e-14°C |
| Both notebooks on Linux | Actual `nbconvert` execution passes; verification writer checks source hashes and 8/10 code-cell counts |
| Linux output compaction | Completed and recorded |
| Mac paths containing spaces | CDO staging fix tested successfully |
| Live local Jupyter browser session | Not verified: the automation environment could not bind a kernel port |
| Numerical comparison with Evgenia's saved outputs | Pending; recipe definitions and local ESMValCore source were audited |
| GitHub publication | Updated code published at `fe1dc89f49a4cd32c72283056d2b5e1ce29d362b` |
| Public BIDS Binder seminar | Live Jupyter rerun passes all 8 code cells and ten real-data comparisons; maximum difference 1.509903313490213e-14°C; Idle / 100% |
| Participant notebook in public browser | Restart Kernel and Run All passes all 10 cells; Idle / 100%; monthly reference residual 5.968558980384842e-14°C |
| CI-verified code revision | `95b89e87aacacde7ec98aaf94f0188214a2d6dea`; [run 8, attempt 2](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42568209901) succeeds, including `scientific-equivalence`, with one artifact |

The real-data checks establish agreement among the three independent local
implementations within the stated 0.0003°C absolute tolerance. They also check
calendar/grid alignment, reference-period residuals, equal-month annual means
and full-year annual time bounds. The anomaly map uses month-duration weights;
the Arctic annual series uses equal monthly weights, following the audited recipe.
These checks do not establish numerical agreement with Evgenia's saved products
or prove an end-to-end execution of her ESMValTool recipe.

[UPDATED_NOTEBOOK_CHECKS.json](UPDATED_NOTEBOOK_CHECKS.json) records the actual
notebook hashes, input hashes, software versions and real-data execution results.
These Mac notebook cells were run using IPython in-process, including their Bash
magics. The later Linux verification executed both notebooks through actual
Jupyter kernels using `nbconvert`. The subsequent public BIDS Binder seminar
rerun is recorded separately in
[binder_launch_verification_20261109.json](binder_launch_verification_20261109.json).
Earlier synthetic evidence remains in
[UPDATED_NOTEBOOK_CHECKS_SYNTHETIC.json](UPDATED_NOTEBOOK_CHECKS_SYNTHETIC.json).

The real workflow reports are `outputs/real_2024/updated_validation.json` and
`outputs/real_2100/updated_validation.json`. Full local execution records remain
under `outputs/` and are excluded from publication. Public summaries omit local
absolute paths. The SSP585 checksum identifies the user-supplied and tested file;
an independent upstream checksum was not supplied.

## GitHub and public Binder verification

The published repository is
[YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop).
The publication workspace was inspected clean at the handoff baseline
`5aec5b469d67cc20e4f5e874a489c297c1879fc0` before the update. The public BIDS Binder
run tested the published source commit
[fe1dc89f49a4cd32c72283056d2b5e1ce29d362b](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/commit/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b).
A subsequent CI-verified code revision,
[95b89e87aacacde7ec98aaf94f0188214a2d6dea](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/commit/95b89e87aacacde7ec98aaf94f0188214a2d6dea),
adds data-download retries. [CI run 8, attempt 2](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42568209901) was verified as
**Success** for that commit: total duration 3 minutes 17 seconds,
`scientific-equivalence` job duration 3 minutes 13 seconds, one artifact. A
Node.js 20 deprecation warning did not fail the run. The downloaded CI receipt
is [github_actions_build.json](updated_verification/github_actions_build.json).
These execution records identify code revisions; a later documentation-only
commit does not change the tested revision.

Recommended links pinned to the publicly tested code revision:

- [20-minute seminar — BIDS Binder](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Participant notebook — BIDS Binder](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b?urlpath=lab/tree/notebooks/04_monthly_anomaly_hands_on.ipynb)
- [Generic mybinder.org fallback](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

The main notebook completed all 8 code cells in the live BIDS Jupyter UI and
reached Idle / 100%. It used real historical and SSP5-8.5 data, 552 months for
1979–2024, with the 1981–2010 reference. All ten comparisons passed, with maximum
difference 1.509903313490213e-14°C. The displayed real-data figure was inspected:
Python, CDO and NCO columns showed corresponding maps, Arctic time series and
annual stripes. The participant notebook then completed Restart Kernel and
Run All through 10 code cells in the same session, also reaching Idle / 100%.
Its real-data setup and final baseline PASS were observed: monthly reference
residual 5.968558980384842e-14°C. The 70°N CDO/NCO exercise differed by at most
3.019806626980426e-14°C; the region change from 65°N to 70°N changed the monthly
values by up to 1.2266452280680342°C. The session reported CDO 2.6.5, NCO 5.4.2
and Python 3.11.18.

[The public launch record](binder_launch_verification_20261109.json) contains
these observations without temporary session addresses or tokens. The fresh
Linux environment, `nbconvert` executions and output compaction are recorded in
[linux_build.json](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/blob/main/docs/updated_verification/linux_build.json) and
[linux_compaction.json](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/blob/main/docs/updated_verification/linux_compaction.json).

Earlier attempts encountered a mybinder.org node `fsnotify: too many open files`
error and a GESIS TLS failure. The later BIDS launch succeeded. Public service
availability can vary; keep the validated local environment ready.

Remaining verification is limited to direct comparison with Evgenia's saved
ESMValTool outputs and an interactive local Mac Jupyter browser test. Both
public Binder notebooks and their full Linux build executions have passed.
Do not infer completion of these remaining checks from those successful runs.
