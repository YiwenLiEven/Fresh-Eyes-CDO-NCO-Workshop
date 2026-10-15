# Fresh Eyes CDO/NCO Workshop

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop?quickstart=1)
[![Launch YL seminar in Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

A CDO/NCO reproduction of [EG's shared monthly-anomaly notebook](https://github.com/egalytska/Fresh_eyes/blob/393cfcf876fa47c6c231c3be70dbd9f8552fe3a3/stripes_EG.ipynb), based on the [Fresh Eyes Python Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop). Use Binder for YL's 20-minute online demonstration and participant hands-on work, or Codespaces for development.

> **Use CDO/NCO to prepare the data.**  
> **Use Python to understand the data.**

## The teaching claim

This project does **not** argue that CDO/NCO is better than Python.

For standard climate-data preprocessing and analysis, CDO/NCO can often achieve the same scientific result with much shorter commands. Python remains especially powerful for visualization, customized analysis, statistics, and machine learning.

The workshop demonstrates the same task twice:

```text
Python/xarray solution
        |
        v
CDO/NCO solution
        |
        v
Compare code and outputs
        |
        v
Validate numerical agreement
```

## Current seminar case: monthly anomalies and Arctic stripes

The Binder entry notebook follows EG's agreed cross-language example:

```text
Monthly global near-surface air temperature
        |
        v
CDO: 1981-2010 monthly climatology -> 1979-2014 monthly anomalies
        |
        v
NCO: select 65-90N -> arithmetic Arctic mean; CDO: annual mean
        |
        v
NCL: Robinson map, Arctic monthly line and 36 annual stripes
```

Python independently reproduces the calculation and validates all four numerical products. The shared Arctic mean is deliberately **unweighted**; using CDO `fldmean` would change the definition. NCL matches the shared map limits (-0.2/+0.4 degC), and the stripes use blue-white-red with symmetric data-derived scaling. See the [cell-by-cell mapping](docs/EG_SHARED_NOTEBOOK_MAPPING.md).

## Participant quick start with Binder

1. Select **Launch YL seminar in Binder** above.
2. Wait for JupyterLab to open directly on `00_yl_20_minute_binder_demo.ipynb`.
3. Run the notebook from top to bottom, or follow the time-stamped presenter prompts.
4. Download any changed notebook or output before closing the session; Binder sessions are temporary.

The Binder configuration uses conda-forge for Python, CDO, NCO and NCL. Its build script creates teaching data, runs both scientific workflows, renders the figures, validates equivalence and executes the presenter and hands-on notebooks. A completed build writes `outputs/verification.json`. Build and test the exact Git revision before distributing its launch URL.

## Instructor quick start with Codespaces

1. Select **Code → Codespaces → Create codespace on main**, or use the badge above.
2. Wait for the setup message: `Workshop environment is ready.`
3. Open `notebooks/00_yl_20_minute_binder_demo.ipynb`.
4. Select the displayed Python kernel and run all cells.

The container automatically installs CDO, NCO, NCL, netCDF utilities, xarray, matplotlib, Jupyter, and the test dependencies. It also generates a deterministic offline teaching dataset and runs the complete validation workflow.

## Local quick start

On Linux or WSL with CDO, NCO, NCL, Python 3.11+, and netCDF installed:

```bash
python -m pip install -e .
make all
```

## Workshop notebooks

| Notebook | Purpose |
|---|---|
| `00_yl_20_minute_binder_demo.ipynb` | Main YL seminar: EG's monthly anomalies, Arctic series, four validations and all three NCL figures |
| `00_opening_demo.ipynb` | Seminar opener: Python versus CDO/NCO annual global anomaly and stripes |
| `01_processing_side_by_side.ipynb` | Time maximum and seasonal climatology, reproduced and validated |
| `02_climate_stripes.ipynb` | Full stripes workflow, baseline correction, comparison, and plotting |
| `03_hands_on_exercises.ipynb` | Earlier global-anomaly exercises and extensions |
| `04_monthly_anomaly_hands_on.ipynb` | Current hands-on: monthly baseline, Arctic weighting and stripe colours |

The exact 20-minute delivery plan, online interaction prompts, setup checklist, and fallback path are in [YL_20_MINUTE_SEMINAR.md](YL_20_MINUTE_SEMINAR.md).

## What was found in the original workshop

The source repository contains three notebooks:

- `getcmip6data.ipynb`: Google Cloud, ESGF website, ESGF API/OPeNDAP, and Intake-ESM access to CMIP6 data;
- `process.ipynb`: maximum temperature, unit conversion, Robinson map, and seasonal climatology;
- `stripes.ipynb`: cosine-latitude global mean, annual mean, 1981–2010 anomaly, and climate stripes.

The exact dataset is CMIP6 ACCESS-CM2 historical monthly `tas`, member `r1i1p1f1`, table `Amon`, grid `gn`, spanning 1850–2014 globally.

The detailed, operation-by-operation audit is in [docs/ORIGINAL_WORKSHOP_MAPPING.md](docs/ORIGINAL_WORKSHOP_MAPPING.md).

## Reproduction map

| Scientific operation | Python/xarray | CDO/NCO reproduction |
|---|---|---|
| Variable selection | `ds["tas"]` | `ncks -v tas` or `cdo selname,tas` |
| Time selection | `.sel(time=slice(...))` | `cdo selyear,1981/2010` |
| Kelvin to Celsius | `tas - 273.15` | `cdo subc,273.15` |
| Time maximum | `.max("time")` | `cdo timmax` |
| Seasonal climatology | `.groupby("time.season").mean()` | `cdo yseasmean` |
| Annual mean | `.groupby("time.year").mean()` | `cdo yearmean` |
| Weighted global mean | `.weighted(cos(lat)).mean()` | `cdo fldmean` |
| Baseline anomaly | selection, mean, subtraction | `selyear`, `timmean`, `subc` |
| Metadata cleanup | xarray attributes | `ncrename`, `ncatted` |
| Climate stripes | matplotlib | NCL primary implementation; Python alternative |
| Customized visualization | matplotlib/cartopy | Keep in Python when it is the clearer tool |

## Data choices

Binder and Codespaces start with a deterministic **synthetic** CF-style dataset covering 1850–2014. Its latitude-dependent trend makes the averaging choices visible. It demonstrates method agreement and must not be presented as ACCESS-CM2 output. To compare actual values with other presenters, supply exactly the same full-grid NetCDF file.

To retrieve a lightweight sample of the actual ACCESS-CM2 file used by the source workshop:

```bash
make real-data
```

The script uses NCO over OPeNDAP, retains all 1,980 months, and samples the spatial grid. A strided sample will not reproduce full-grid Arctic means exactly. See [data/README.md](data/README.md). The saved-data hyperlink mentioned in the email was not present in the supplied message.

## Reproducible validation

Run everything:

```bash
make all
```

The workflow writes Python and CDO results independently, then compares:

- maximum temperature;
- seasonal climatology;
- global annual temperature anomaly.

The current EG example additionally compares the 432 monthly anomaly fields, the mean anomaly map, the unweighted Arctic monthly series and its 36 annual values. It checks finite-value masks, shapes, selected periods and near-zero baseline residuals. These results are in `outputs/demo/monthly_validation.json`.

The earlier global-case report is `outputs/demo/validation.json`. Tests fail if any maximum absolute difference exceeds the documented tolerance.

## Seminar materials

- [YL_20_MINUTE_SEMINAR.md](YL_20_MINUTE_SEMINAR.md): current timed Binder talk;
- [docs/EG_SHARED_NOTEBOOK_MAPPING.md](docs/EG_SHARED_NOTEBOOK_MAPPING.md): primary shared-example audit;

- [SEMINAR_DEMO.md](SEMINAR_DEMO.md): minute-by-minute live-demo sequence and recovery plan;
- [docs/INSTRUCTOR_NOTES.md](docs/INSTRUCTOR_NOTES.md): caveats and discussion prompts;
- [docs/ORIGINAL_WORKSHOP_MAPPING.md](docs/ORIGINAL_WORKSHOP_MAPPING.md): complete source audit and operator mapping.

## Attribution

The current Binder demonstration follows [Evgenia Galytska's compressed seminar example](https://github.com/egalytska/Fresh_eyes). These implementations were written independently; the reference notebook is linked rather than copied.

The scientific examples are based on the public repository [abhnil/Fresh_Eyes_on_CMIP_Data_Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop). This repository is an independent teaching reproduction, not a fork and not an official continuation of the source project.

- Cases reproduced from the source: CMIP6 `tas` access, time maximum, seasonal climatology, weighted global annual mean, baseline anomaly, and climate stripes.
- Extensions in this repository: NCL climate stripes, side-by-side validation, offline teaching data, automated tests, Codespaces configuration, instructor notes, and participant exercises.
- Tasks intentionally retained in Python: numerical validation, interpretation, customized visualization, and exploratory analysis.

The code in this repository is released under the MIT License. CMIP6 data retain their original licenses and citation requirements.
