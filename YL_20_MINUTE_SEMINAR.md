# YL 20-Minute Online Seminar: EG Shared Example

**Presenter:** Yiwen Li (YL)

**Title:** Monthly Temperature Anomalies with CDO/NCO and NCL

**Format:** 20-minute live Binder demonstration, followed by the shared hands-on session

## Scientific target

Reproduce [EG's shared notebook](https://github.com/egalytska/Fresh_eyes/blob/393cfcf876fa47c6c231c3be70dbd9f8552fe3a3/stripes_EG.ipynb), including its latest fixed map range:

1. ACCESS-CM2 monthly near-surface air temperature in Kelvin.
2. Convert to Celsius.
3. Compute the 1981–2010 climatology separately for each calendar month.
4. Subtract the matching climatological month at every grid cell.
5. Analyse January 1979 through December 2014.
6. Plot the time-mean anomaly on a Robinson map (coolwarm, −0.2 to +0.4 °C).
7. Calculate the **unweighted** 65–90°N grid-point mean and plot 432 monthly anomalies.
8. Average monthly Arctic anomalies into 36 annual values and draw blue–white–red stripes with symmetric ±max(|annual anomaly|) scaling.

CDO handles the climatology, anomalies and time means. NCO handles variable selection, Arctic selection, the arithmetic grid-point mean and metadata. NCL draws all three figures. Python provides the independently computed reference and validation.

## Minute-by-minute delivery

| Time | What appears on screen | What YL says or does |
|---|---|---|
| 0:00–2:00 | Preview Arctic stripes and the shared scientific question | “What is a January anomaly compared with?” Explain the common cross-language target and the data label. |
| 2:00–4:00 | Dataset and CDO summary | Identify tas, Kelvin, monthly sampling, the 1981–2010 baseline and the 1979–2014 analysis window. |
| 4:00–6:30 | Compact xarray reference | Explain grouping by calendar month and why the source Arctic mean is unweighted. |
| 6:30–11:00 | Operator mapping and prepared CDO/NCO script | Run ymonmean, ymonsub, time selection, timmean, Arctic selection, ncwa and yearmean. |
| 11:00–13:00 | Four numerical comparisons | Show 432 months, 36 years, baseline residual checks and maximum absolute differences. |
| 13:00–17:00 | NCL Robinson map, monthly line and annual stripes | Connect each graphic to a processed NetCDF; explain map range and symmetric stripe normalization. |
| 17:00–19:00 | Short prediction questions | Ask how a different baseline or area-weighted Arctic mean would affect the result. Defer full edits to hands-on. |
| 19:00–20:00 | Tool-choice takeaway and hands-on link | Repeat the complementary workflow and hand over. |

## Binder entry point

Open `notebooks/00_yl_20_minute_binder_demo.ipynb`:

[Launch in Binder](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

Binder builds the environment from `binder/environment.yml`. The build creates synthetic data, executes both implementations, checks numerical equivalence, renders all three NCL figures, and executes both seminar notebooks. A completed build writes `outputs/verification.json`.

For the seminar, replace `main` in the launch URL with the tested Git commit SHA. Open the exact link before distributing it and keep a working presenter session open.

## Data agreement with the other presenters

The default Binder dataset is **synthetic**, with spatially varying trends so that the Arctic and global calculations differ visibly. It demonstrates software equivalence on one shared input. It does not reproduce actual ACCESS-CM2 values.

For direct comparison with AP/EG/DK, use the **same original NetCDF file and full spatial grid** in every language. The email's “saved data here” text did not include a resolvable data link, so that file is not silently substituted. Once the file is available locally, set `WORKSHOP_INPUT` before starting Jupyter or change the notebook's `DATA` path. The optional NCO download in this repository uses spatial striding; it is a teaching sample and cannot be compared numerically to the full-grid reference.

## Presenter rehearsal

- Build and launch the exact Binder revision before the seminar.
- Run the notebook in a fresh session and check all four PASS results.
- Keep `01_mean_anomaly_map.png`, `02_arctic_monthly_anomaly.png`, and `03_arctic_annual_stripes.png` as offline backups.
- Keep the NCL driver and CDO/NCO script in adjacent tabs.
- Share a browser window with readable code; avoid scrolling through build logs during the talk.
- If Binder is unavailable, show the executed notebook and saved figures.
- If time is short, reduce metadata discussion and audience predictions; retain validation and the three figure results.

## Hands-on handoff

Use `notebooks/04_monthly_anomaly_hands_on.ipynb`. Participants inspect the outputs, compare a second baseline, and examine arithmetic versus area-weighted Arctic means. Download changed notebooks and results before closing a temporary Binder session.

## Two caveats to explain accurately

**Spatial weights:** EG uses an arithmetic mean across Arctic grid points. `ncwa -a lat,lon` reproduces it. Using CDO `fldmean` would intentionally change the quantity to an area-weighted mean.

**Temporal weights:** EG gives each monthly value equal weight. CDO `yearmean` matches that choice here. A day-weighted annual mean would be a separate scientific choice.

## Closing words

“CDO expresses routine climate operations concisely. NCO lets us match the exact variable, region and averaging definition. Python verifies and explains the calculation, and NCL renders the result. Use CDO/NCO to prepare the data. Use Python to understand the data.”
