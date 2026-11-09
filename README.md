# Fresh Eyes: Python, CDO-only and NCO-only

**Updated local seminar · 9 November 2026 · Yiwen Li**

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

## Local validation

The real 1979–2024 ACCESS-CM2 workflow has passed all ten product comparisons,
including the annual time-bound checks. All **8 seminar code cells and 10
participant code cells** passed with their default real inputs; final cell stderr
streams were empty. The exact results and notebook hashes are in
[the verification record](docs/UPDATED_NOTEBOOK_CHECKS.json). These local checks
execute cells with IPython in-process; they are distinct from a live Jupyter or
Binder session test. Synthetic software-test evidence is retained separately.

## Publication status

Target: [YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop).
This folder contains the local update. GitHub publication and a new Binder image
must be verified separately; the previous successful Binder run does not verify
this revision. Keep existing pinned links labeled as the earlier version until a
new tested commit is available.

## Attribution and earlier material

Original Python workshop: [Abhnil / Fresh_Eyes_on_CMIP_Data_Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop).
Updated shared reference: [Evgenia Galytska / Fresh_eyes](https://github.com/egalytska/Fresh_eyes).
Independent command-line implementations and teaching material: Yiwen Li's workshop.

Earlier 1979–2014 notebook sources are retained as `notebooks/legacy_*.ipynb`.
The existing combined CDO/NCO scripts, NCL material, old figures and saved execution
reports belong to earlier demonstrations. Their archived PASS records must not be
presented as validation of the new 1979–2024 calculation.
