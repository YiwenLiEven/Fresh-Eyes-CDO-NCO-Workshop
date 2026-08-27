# Seminar Demonstration Runbook

This runbook supports a 45–60 minute seminar plus a 20–30 minute hands-on session.

## Before the seminar

1. Open the repository in Codespaces at least once so the container image is cached.
2. Confirm that `.devcontainer/post-create.sh` finishes successfully.
3. Open `notebooks/00_opening_demo.ipynb` and select the Python kernel.
4. Run all cells once.
5. Keep `outputs/demo/climate_stripes.png` open in a second editor tab.
6. Optionally run `make real-data` before the session if the venue network is reliable.

## Core message

Do not frame the session as “CDO/NCO is better than Python.” Use this wording:

> For standard climate-data preprocessing and analysis, CDO/NCO can often achieve the same scientific result with much shorter commands. Python remains especially powerful for visualization, customized analysis, statistics, and machine learning.

Then reveal:

> Use CDO/NCO to prepare the data.  
> Use Python to understand the data.

## Live sequence

### 0–5 minutes: scientific question

Ask: “How did global near-surface air temperature change relative to 1981–2010?”

Show the final stripes first. Avoid beginning with software installation or operator lists.

### 5–15 minutes: Python workflow

In `00_opening_demo.ipynb`, show the xarray sequence:

1. open the monthly field;
2. convert K to °C;
3. calculate cosine-latitude weights;
4. calculate a global mean;
5. group by year;
6. calculate the baseline;
7. subtract the baseline.

Emphasize that the code is readable, explicit, and easy to customize.

### 15–25 minutes: CDO/NCO workflow

Reveal the processing chain:

```bash
cdo -yearmean -fldmean -subc,273.15 input.nc annual_global.nc
cdo -timmean -selyear,1981/2010 annual_global.nc baseline.nc
cdo subc,$BASELINE annual_global.nc anomaly.nc
ncrename -v tas,tas_anom anomaly.nc
```

Explain right-to-left evaluation in chained CDO commands. Explain that NCO is especially convenient for extraction and metadata surgery.

### 25–35 minutes: numerical equivalence

Run:

```bash
python scripts/validate_results.py
```

Show `outputs/demo/validation.json`. The important result is not identical byte layout; it is agreement within an explicit numerical tolerance.

### 35–45 minutes: Python visualization

Run:

```bash
python scripts/make_stripes.py
```

Make the division of labor visible:

```text
CDO/NCO -> small analysis-ready NetCDF -> Python -> explanation and visualization
```

## Hands-on segment

Participants should complete these tasks in order:

1. Run `make all` and inspect the validation report.
2. Open `01_processing_side_by_side.ipynb` and reproduce maximum temperature and seasonal climatology.
3. Open `02_climate_stripes.ipynb`, change the baseline to 1961–1990 in both workflows, and verify agreement again.
4. Optional extension: run `make real-data`, substitute the ACCESS-CM2 teaching sample, and repeat the comparison.

## Recovery plan

- If ESGF/OPeNDAP is unavailable, use `data/demo/tas_demo.nc`; the seminar remains fully functional.
- If notebook execution is slow, run `bash scripts/run_all.sh` in the terminal and use the notebooks only for explanation.
- If a participant changes a notebook irreversibly, use GitHub’s source-control panel to discard only that notebook’s changes.
- Never depend on a live 219 MB download for the opening demo.

