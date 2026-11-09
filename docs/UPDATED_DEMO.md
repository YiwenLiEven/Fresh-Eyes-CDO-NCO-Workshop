# CDO/NCO notebooks: data, commands and local use

The two active notebooks are:

- [Main notebook](../notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Practice notebook](../notebooks/04_monthly_anomaly_hands_on.ipynb)

## Follow the commands

Run cells from top to bottom with **Shift+Enter**, including collapsed cells.
Each processing cell contains the CDO or NCO commands that it executes. Read the
input, output and option explanations above each cell, run it, then continue to
the next step. Both notebooks contain **nine CDO steps** and **ten NCO steps**.

`%%bash` runs shell commands inside the notebook. The cell changes into that
route's output directory, where `historical_input.nc` and `ssp585_input.nc`
refer to the original source files. `-O` permits replacing a step's previous
output when it is rerun. If a command fails, that cell stops. After a kernel
restart, run from the first cell so the data and output paths are established.

Collapsed cells handle data checks, an independent Python reference and result
display. They remain executable and their output is visible; no Python editing
is needed to follow the CDO/NCO calculations.

| Step | CDO | NCO |
| --- | --- | --- |
| 1 | Select `tas` and dates: `selname`, `selyear` | Select `tas`, time bounds and dates: `ncks` |
| 2 | Join experiments: `mergetime` | Join records: `ncrcat` |
| 3 | Convert Kelvin to Celsius: `subc`, `setunit` | Convert values and update attributes: `ncap2`, `ncatted` |
| 4 | Select 1981–2010: `selyear` | Select 1981–2010: `ncks` |
| 5 | Calculate 12 reference fields: `ymonmean` | Average each calendar month and assemble: `ncwa`, `ncecat`, `ncap2` |
| 6 | Subtract matching months: `ymonsub`, `chname` | Append reference and subtract: `ncrename`, `ncks`, `ncap2` |
| 7 | Duration-weighted mean map: `muldpm`, `timsum`, `div` | Duration-weighted mean map: `ncap2`, `ncwa -w` |
| 8 | Arctic selection and equal-grid mean: `sellonlatbox`, `fldmean,weights=false` | Arctic zonal and meridional means: `ncwa` |
| 9 | Equal-month annual mean: `yearmean` | Groups of 12 monthly records: `ncra --mro` |
| 10 | — | Set full calendar-year time bounds: `ncks`, `ncap2` |

## Source and scientific definitions

The calculation follows Evgenia Galytska's
[updated ESMValTool recipe](https://github.com/egalytska/Fresh_eyes/blob/040b9c7962355b1f8fa1312b7af867b458102b85/ESMValTool/recipe_temperature_anomalies.yml)
at revision `040b9c7962355b1f8fa1312b7af867b458102b85`. The general processing
examples originate in [Abhnil's Python workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop).
CDO and NCO each process the same raw files independently; Python provides a
third calculation, numerical comparisons and figures.

| Scientific choice | Current calculation |
| --- | --- |
| Model and experiments | ACCESS-CM2 historical + SSP5-8.5, member `r1i1p1f1`, grid `gn` |
| Analysis period | January 1979–December 2024: 552 months and 46 annual values |
| Monthly reference | 1981–2010: 30 samples for each calendar month |
| Mean anomaly map | Time-bound duration weighted mean |
| Arctic monthly mean | Latitude centres 65–90°N, equal grid-point weights |
| Arctic annual mean | Equal weight for the 12 monthly samples |

The recipe's map uses `climate_statistics(period: full, operator: mean)`. Its
Arctic series uses `extract_region`, `zonal_statistics(mean)` and
`meridional_statistics(mean)`, followed by `annual_statistics(mean)` for annual
output. The duration-weighted map and equal-month annual definitions were
checked against ESMValCore 2.10.0 source. This source audit is separate from
executing the upstream recipe or comparing its saved output files.

Every route applies the historical 1981–2010 reference to both experiment
segments. The future period is not recentered against itself. Input checks
require matching grids, calendars and model/member metadata, consecutive months,
finite values and complete monthly time bounds. The mean map is a period-mean
anomaly, not a trend; this is model output, not observations.

## Real input files

**Real ACCESS-CM2 is the default.** Both files are cached during the Binder build
and are present on the configured Mac. The notebook requires existing files and
does not download them. If either is missing, execution stops without replacing
it with synthetic data.

Expected files in `data/access_cm2/`:

```text
tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc
tas_Amon_ACCESS-CM2_ssp585_r1i1p1f1_gn_201501-210012.nc
```

The historical file comes from the organizer's shared archive; Evgenia's updated
repository supplies the future scenario file. The fetch helper uses the pinned
source revision and checks both hashes:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Historical, 1850–2014 | 148190686 | `3e106e8430f04cd2b260a7230b1e461ccebdda338d09e3f07e8497678c5c6f0f` |
| SSP5-8.5, 2015–2100 | 77137066 | `8f0d0cee4c370c0c30acc31ef6bf03a2592ee3dfd827a13e37716cd7484909b1` |

If downloading is unavailable, copy the matching organizer files into that
directory. Explicit file locations can also be selected before opening Jupyter:

```bash
export WORKSHOP_HISTORICAL=/absolute/path/to/historical.nc
export WORKSHOP_FUTURE=/absolute/path/to/ssp585.nc
jupyter lab notebooks/00_yl_20_minute_binder_demo.ipynb
```

`WORKSHOP_MODE=synthetic` selects an optional software-test dataset. Its figures
and reports stay labeled as synthetic; those results do not represent ACCESS-CM2.

## Run locally or in Binder

On the configured Mac, open the project-level `Launch_Updated_Notebook.command`
or source `activate_fresh_eyes.sh`. The existing environment has CDO 2.5.0,
NCO 5.3.9, Python 3.12.14 and JupyterLab 4.6.3. It runs through Rosetta on the
Apple Silicon Mac. See [LOCAL_MAC_SETUP.md](LOCAL_MAC_SETUP.md) for launch options.

On another compatible machine:

```bash
conda env create -f binder/environment.yml
conda activate fresh-eyes
python scripts/fetch_updated_data.py
jupyter lab notebooks/00_yl_20_minute_binder_demo.ipynb
```

After installation and data download, the local notebooks can run offline.
The [Binder environment guide](../binder/README.md) also describes the Linux
devcontainer configuration. Recreate the environment on another machine instead
of copying an installed Conda directory. NCO 5.1.9 or later is needed for
`ncra --mro`.

Open the latest notebooks online:

- [Main notebook in BIDS Binder](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Practice notebook in BIDS Binder](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/04_monthly_anomaly_hands_on.ipynb)
- [Generic mybinder.org fallback](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

The `main` links select the current published notebook. An older commit-pinned
link selects that earlier revision. Binder sessions are temporary; save edited
notebooks and results before leaving. Local use remains available when the
public Binder service is unavailable.

## Results and optional extension

Each run creates a new output directory with independent `python/`, `cdo/` and
`nco/` products, `updated_validation.json` and `updated_comparison.png`. Five
products from each command-line route are compared with the reference: monthly
climatology, monthly anomalies, duration-weighted map, Arctic monthly series and
Arctic annual series. Tolerance is 0.0003°C absolute and zero relative tolerance.
Coordinates, calendar labels and masks must agree; the reference-period monthly
residual must approach zero and each annual value must equal its 12-month mean.

For the optional extension, set `WORKSHOP_END_YEAR=2100` before launching Jupyter.
It produces 122 annual values for 1979–2100 while keeping the 1981–2010 monthly
reference fixed. Changing the end year also changes the period-mean map and
stripe color scale.

## Verification by revision

The current revision expands processing into visible command cells. Its
scientific definitions are unchanged, but its executable cell sources have
changed. Local checks executed all **24 main-notebook cells and 30 practice
cells** using the real ACCESS-CM2 historical and SSP5-8.5 files. Both notebooks
passed all ten product comparisons, with maximum absolute difference
**3.552713678800501e-15°C**, and their cell stderr streams were empty.

The checks used IPython in-process, including each actual Bash command cell.
They verify the current cell code without a separate Jupyter kernel or browser
session. The detailed evidence is
[inline_commands_verification_20261109.json](inline_commands_verification_20261109.json).
A live Jupyter/Binder check of this new revision remains to be recorded.

Earlier evidence remains available with its original scope:

| Evidence | Revision and scope |
| --- | --- |
| [Local notebook checks](UPDATED_NOTEBOOK_CHECKS.json) | Earlier notebooks with 8 main and 10 practice code cells, executed in-process on the Mac |
| [Public Binder receipt](binder_launch_verification_20261109.json) | `fe1dc89...`: earlier 8/10-cell notebooks completed in the public Jupyter UI with real data |
| [GitHub Actions build receipt](updated_verification/github_actions_build.json) | `95b89e8...`: full Linux build and earlier 8/10-cell notebook execution |
| [Linux build record](updated_verification/linux_build.json) | Earlier Binder environment and notebook execution |
| [Output compaction record](updated_verification/linux_compaction.json) | Earlier build's retained outputs and cleanup |

Those earlier records do not verify the current inline-command notebook revision.
Direct numerical agreement with Evgenia's saved ESMValTool products and an
interactive local Mac Jupyter browser session remain separate, unverified checks.
The earlier 1979–2014 notebook sources are retained under `notebooks/legacy_*.ipynb`.
