# Fresh Eyes: Python, CDO-only and NCO-only

**Updated seminar · published 9 November 2026 · Yiwen Li**

The updated demonstration follows [Evgenia Galytska's ESMValTool recipe](https://github.com/egalytska/Fresh_eyes/blob/040b9c7962355b1f8fa1312b7af867b458102b85/ESMValTool/recipe_temperature_anomalies.yml):
historical + SSP5-8.5 data, **1979–2024** anomalies against the **1981–2010** monthly
reference. CDO and NCO each process the original input files independently.
Python provides a third route, numerical checks and comparison graphics.

**The notebooks now default to real ACCESS-CM2 historical + SSP5-8.5 data.**
The Binder build caches the two organizer files; they are also staged on the
prepared Mac. Missing real files stop execution. Synthetic inputs are available
only through an explicit `WORKSHOP_MODE=synthetic` software-test mode.

## Start

- [20-minute seminar notebook](notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Participant hands-on notebook](notebooks/04_monthly_anomaly_hands_on.ipynb)
- [Local setup, real-data mode and scientific definitions](docs/UPDATED_DEMO.md)

Recommended Binder links, pinned to the tested code revision:

- [Open the 20-minute seminar in BIDS Binder](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Open participant practice in BIDS Binder](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b?urlpath=lab/tree/notebooks/04_monthly_anomaly_hands_on.ipynb)
- [Generic mybinder.org fallback](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

**The seminar notebook was rerun successfully in a live public BIDS Binder
session.** All 8 code cells and ten product comparisons passed using real
ACCESS-CM2 data. Participant practice also passed all 10 cells after restarting
its kernel and running all cells in the same public session. Both notebooks
reached Idle / 100%. Save your results
before closing a Binder session and keep the local setup as a fallback.

```bash
conda env create -f binder/environment.yml
conda activate fresh-eyes
python scripts/fetch_updated_data.py
jupyter lab notebooks/00_yl_20_minute_binder_demo.ipynb
```

On the prepared Mac, the project-level `Launch_Updated_Notebook.command` uses the
existing local CDO/NCO/Jupyter environment. No global shell changes are required.

## Common calculation

| Product | Shared definition |
|---|---|
| Monthly climatology | 1981–2010 mean for each calendar month |
| Monthly anomalies | 1979–2024, 552 fields |
| Mean anomaly map | **Month-duration weighted** mean |
| Arctic monthly series | 65–90°N, **equal grid-point weights** |
| Annual stripes | 46 years; **equal weight for each monthly sample** |

The map and annual series use different time weights, following the recipe.
Five CDO products and five NCO products are checked against Python with an
absolute tolerance of 0.0003°C, exact coordinate/calendar alignment and additional
baseline and annual-mean checks. Optional `END_YEAR=2100` is an extension.

```bash
python scripts/fetch_updated_data.py
bash scripts/run_updated_workflows.sh \
  data/access_cm2/tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc \
  data/access_cm2/tas_Amon_ACCESS-CM2_ssp585_r1i1p1f1_gn_201501-210012.nc \
  outputs/updated_real 2024
```

Results include route-specific NetCDF files, `updated_validation.json` and
`updated_comparison.png`.

## Validation

The real 1979–2024 ACCESS-CM2 workflow has passed all ten product comparisons,
including the annual time-bound checks. All **8 seminar code cells and 10
participant code cells** passed with their default real inputs; final cell stderr
streams were empty. The exact results and notebook hashes are in
[the verification record](docs/UPDATED_NOTEBOOK_CHECKS.json). These local checks
execute cells with IPython in-process; they are distinct from a live Jupyter or
Binder session test. The latest Mac test run passed **12 tests** in 8.73 seconds
with one NumPy compatibility warning. Synthetic software-test evidence is
retained separately.

A fresh Linux Codespace built the environment from `binder/environment.yml` and
completed the Binder build procedure: **8 tests passed**, the real 1979–2024
workflow passed all ten comparisons (maximum difference 1.50990331e-14°C), and
both notebooks executed successfully through `nbconvert`. The verification writer
checked the actual source hashes and the 8/10 code-cell counts. Output compaction
also completed. One NumPy compatibility warning remained in the test run.

Published Linux evidence: [build and notebook execution](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/blob/main/docs/updated_verification/linux_build.json)
and [output compaction](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/blob/main/docs/updated_verification/linux_compaction.json).

## Public Binder verification and publication

The live BIDS Binder seminar run used CDO **2.6.5**, NCO **5.4.2** and Python
**3.11.18**. It processed 552 monthly fields for 1979–2024 against the 1981–2010
monthly reference. All ten comparisons passed; the largest difference was
**1.509903313490213e-14°C**. The notebook reached Idle / 100%, and its real-data
comparison figure was inspected. The participant rerun also passed its 70°N
exercise (CDO/NCO maximum difference 3.019806626980426e-14°C) and its monthly
reference-residual check (5.968558980384842e-14°C). See the
[public launch record](docs/binder_launch_verification_20261109.json).

The recommended links pin
[fe1dc89f49a4cd32c72283056d2b5e1ce29d362b](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/commit/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b),
the code revision tested in that public session. A subsequent CI-verified code
revision is
[95b89e87aacacde7ec98aaf94f0188214a2d6dea](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/commit/95b89e87aacacde7ec98aaf94f0188214a2d6dea),
which adds data-download retries. [CI run 8, attempt 2](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42568209901) succeeded for that
revision: the `scientific-equivalence` job passed and produced one artifact. A
Node.js 20 deprecation warning was informational. The live public Binder record
still applies to the pinned `fe1dc89` code revision. Old pinned Binder links
continue to identify the earlier code. The downloaded
[GitHub Actions build receipt](docs/updated_verification/github_actions_build.json)
records the CI result. A later documentation-only commit does not change which
code revisions these execution records verify.

The numerical checks establish agreement among Python, CDO and NCO. A direct
comparison with Evgenia's saved ESMValTool outputs has not been completed.

## Attribution and earlier material

Original Python workshop: [Abhnil / Fresh_Eyes_on_CMIP_Data_Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop).
Updated shared reference: [Evgenia Galytska / Fresh_eyes](https://github.com/egalytska/Fresh_eyes).
Independent command-line implementations and teaching material: Yiwen Li's workshop.

Earlier 1979–2014 notebook sources are retained as `notebooks/legacy_*.ipynb`.
The existing combined CDO/NCO scripts, NCL material, old figures and saved execution
reports belong to earlier demonstrations. Their archived PASS records must not be
presented as validation of the new 1979–2024 calculation.
