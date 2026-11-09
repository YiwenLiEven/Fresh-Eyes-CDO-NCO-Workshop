# Fresh Eyes update status — 9 November 2026

## Completed locally

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

## Execution evidence and limits

| Check | Result |
|---|---|
| Real ACCESS-CM2 1979–2024 workflow | 10 product comparisons pass; 552 months / 46 years; maximum difference 3.5527136788e-15°C |
| Real ACCESS-CM2 1979–2100 extension | 10 product comparisons pass; 1,464 months / 122 years; maximum difference 2.4868995752e-14°C |
| Main seminar notebook, real data | All 8 code cells pass; all 10 product comparisons pass; final cell stderr streams empty |
| Participant notebook, real data | All 10 code cells pass, including exercises; all 10 product comparisons pass; final cell stderr streams empty |
| Synthetic 1979–2024 software test | 10 product comparisons pass; maximum difference 8.88e-16°C |
| Synthetic 1979–2100 software extension | 10 product comparisons pass; maximum difference 3.55e-15°C |
| Legacy real ACCESS-CM2 historical workflow | 8 comparisons pass; maximum difference 2.594e-5°C |
| Repository test suite | 8 tests passed; one NumPy binary-compatibility warning remained |
| Mac paths containing spaces | CDO staging fix tested successfully |
| Live local Jupyter browser session | Not verified: the automation environment could not bind a kernel port |
| Numerical comparison with Evgenia's saved outputs | Pending; recipe definitions and local ESMValCore source were audited |
| New GitHub update / fresh Binder image | Publication and Binder execution remain pending |

The real-data checks establish agreement among the three independent local
implementations within the stated 0.0003°C absolute tolerance. They also check
calendar/grid alignment, reference-period residuals, equal-month annual means
and full-year annual time bounds. The anomaly map uses month-duration weights;
the Arctic annual series uses equal monthly weights, following the audited recipe.
These checks do not establish numerical agreement with Evgenia's saved products
or prove an end-to-end execution of her ESMValTool recipe.

[UPDATED_NOTEBOOK_CHECKS.json](UPDATED_NOTEBOOK_CHECKS.json) records the actual
notebook hashes, input hashes, software versions and real-data execution results.
The notebook cells were run using IPython in-process, including their Bash
magics. This verifies their code without claiming a live Jupyter browser or
Binder session. Earlier synthetic evidence remains in
[UPDATED_NOTEBOOK_CHECKS_SYNTHETIC.json](UPDATED_NOTEBOOK_CHECKS_SYNTHETIC.json).

The real workflow reports are `outputs/real_2024/updated_validation.json` and
`outputs/real_2100/updated_validation.json`. Full local execution records remain
under `outputs/` and are excluded from publication. Public summaries omit local
absolute paths. The SSP585 checksum identifies the user-supplied and tested file;
an independent upstream checksum was not supplied.

## GitHub state and remaining online verification

The public target remains
[YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop).
The publication workspace was inspected at remote HEAD
`5aec5b469d67cc20e4f5e874a489c297c1879fc0`, matching the handoff's last verified
public revision, and was clean before applying this update. The updated local
source has not yet been confirmed as a new public commit.

Remaining steps:

1. Apply and review the prepared update against that inspected public baseline,
   preserving unrelated content and the repository directory structure.
2. Publish the reviewed changes and read back the resulting commit and files.
3. Build a fresh Binder image and execute both notebooks with the cached real
   historical and SSP585 inputs; record the results and tested commit.
4. Share a Binder link pinned to that newly verified commit.

Old pinned Binder links continue to identify the earlier code. Local scientific
and notebook checks do not imply that those online links have been updated.
