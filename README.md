# Fresh Eyes CDO/NCO Workshop

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop?quickstart=1)

A seminar-ready CDO/NCO reproduction and extension of the [Fresh Eyes on CMIP Data Python Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop), designed for live demonstration and participant hands-on work in GitHub Codespaces.

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

## Seminar opening demo: global temperature stripes

The opening case reproduces the source workshop’s climate-stripes analysis while separating preprocessing from visualization:

```text
Monthly global near-surface air temperature
        |
        v
CDO/NCO: select, convert units, annualize, area-average, calculate anomaly
        |
        v
Small one-dimensional NetCDF time series
        |
        v
Python: validate and plot climate stripes
```

The source notebook uses Python for data access, processing, statistics, and plotting. This workshop demonstrates a complementary architecture: CDO/NCO prepares an analysis-ready result, and Python explains and visualizes it.

## Quick start with Codespaces

1. Select **Code → Codespaces → Create codespace on main**, or use the badge above.
2. Wait for the setup message: `Workshop environment is ready.`
3. Open `notebooks/00_opening_demo.ipynb`.
4. Select the displayed Python kernel and run all cells.

The container automatically installs CDO, NCO, netCDF utilities, xarray, matplotlib, Jupyter, and the test dependencies. It also generates a deterministic offline teaching dataset and runs the complete validation workflow.

## Local quick start

On Linux or WSL with CDO, NCO, Python 3.11+, and netCDF installed:

```bash
python -m pip install -e .
make all
```

## Workshop notebooks

| Notebook | Purpose |
|---|---|
| `00_opening_demo.ipynb` | Seminar opener: Python versus CDO/NCO annual global anomaly and stripes |
| `01_processing_side_by_side.ipynb` | Time maximum and seasonal climatology, reproduced and validated |
| `02_climate_stripes.ipynb` | Full stripes workflow, baseline correction, comparison, and plotting |
| `03_hands_on_exercises.ipynb` | Participant tasks and clearly labeled extensions |

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
| Visualization | matplotlib/cartopy | Keep in Python |

## Data choices

Codespaces starts with a deterministic CF-style demo dataset covering 1850–2014. This ensures that the seminar never depends on a live remote-data service. It is synthetic and clearly labeled.

To retrieve a lightweight sample of the actual ACCESS-CM2 file used by the source workshop:

```bash
make real-data
```

The script uses NCO over OPeNDAP, retains all 1,980 months, and samples the spatial grid to keep the download practical. See [data/README.md](data/README.md).

## Reproducible validation

Run everything:

```bash
make all
```

The workflow writes Python and CDO results independently, then compares:

- maximum temperature;
- seasonal climatology;
- global annual temperature anomaly.

The machine-readable report is `outputs/demo/validation.json`. Tests fail if any maximum absolute difference exceeds the documented tolerance.

## Seminar materials

- [SEMINAR_DEMO.md](SEMINAR_DEMO.md): minute-by-minute live-demo sequence and recovery plan;
- [docs/INSTRUCTOR_NOTES.md](docs/INSTRUCTOR_NOTES.md): caveats and discussion prompts;
- [docs/ORIGINAL_WORKSHOP_MAPPING.md](docs/ORIGINAL_WORKSHOP_MAPPING.md): complete source audit and operator mapping.

## Attribution

The scientific examples are based on the public repository [abhnil/Fresh_Eyes_on_CMIP_Data_Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop). This repository is an independent teaching reproduction, not a fork and not an official continuation of the source project.

- Cases reproduced from the source: CMIP6 `tas` access, time maximum, seasonal climatology, weighted global annual mean, baseline anomaly, and climate stripes.
- Extensions in this repository: side-by-side validation, offline teaching data, automated tests, Codespaces configuration, instructor notes, and participant exercises.
- Tasks intentionally retained in Python: visualization, interpretation, and customized exploratory analysis.

The code in this repository is released under the MIT License. CMIP6 data retain their original licenses and citation requirements.

