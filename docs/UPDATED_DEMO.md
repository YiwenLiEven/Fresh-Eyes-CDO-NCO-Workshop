# CDO/NCO notebooks: run a command and inspect its result

- [Main notebook](../notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Practice notebook](../notebooks/04_monthly_anomaly_hands_on.ipynb)

## Follow each result

Run the Data cell first, then continue with **Shift+Enter**, including collapsed
cells. Each processing cell contains **one direct command** beginning with
`cdo`, `ncks` or another NCO tool. The next cell contains a short CDO/NCO query
that displays the result immediately. Read its output before proceeding to the
next transformation. If a command reports an error or the query differs from
the expected result, inspect that step before continuing.

The Data cell creates a fresh run directory and makes it the notebook's working
directory. Inputs have the names `data/historical.nc` and `data/ssp585.nc`.
CDO products go into `cdo/`, and NCO products into `nco/`. These same literal
paths appear in the commands. Collapsed cells handle data checks, the independent
reference and figures; no Python editing is needed to follow the calculations.

Run the commands exactly as shown. To use a command in a terminal, first enter
the run directory printed in the Data output, then copy the same command text.
To repeat the whole calculation, start again from the
first cell; a new run directory keeps the previous files intact.

The short queries make each transformation observable:

| After processing | Inspect the result |
| --- | --- |
| Variable selection | Variable names and dimensions |
| Date selection and joining | Record counts and time coverage |
| Unit conversion | Unit attribute and sample values |
| Monthly reference | Twelve calendar-month reference fields |
| Monthly anomalies | Field dimensions and sample anomaly values |
| Arctic means | One value per month |
| Annual reduction | 46 annual values and calendar-year coverage |

CDO uses `-b F64` once when joining the experiments, before the Kelvin-to-Celsius
arithmetic. Later outputs inherit double precision. NCO chooses classic NetCDF
once in the first historical extraction; its derived files inherit that format.

## Source and scientific definitions

The calculation follows Evgenia Galytska's
[updated ESMValTool recipe](https://github.com/egalytska/Fresh_eyes/blob/040b9c7962355b1f8fa1312b7af867b458102b85/ESMValTool/recipe_temperature_anomalies.yml)
at revision `040b9c7962355b1f8fa1312b7af867b458102b85`. The general processing
examples originate in [Abhnil's Python workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop).
CDO and NCO independently process the same inputs; Python provides a third
calculation, numerical comparisons and figures.

| Scientific choice | Teaching calculation |
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

Every route uses the historical 1981–2010 reference for both experiments. Input
checks require matching grids, calendars and model/member metadata, consecutive
months, finite values and complete monthly time bounds. The mean map is a
period-mean anomaly, not a trend; the inputs are model output, not observations.

## Real input files

**Real ACCESS-CM2 is the default.** The repository stores the full organizer
files under `data/access_cm2/`. The Data cell exposes them to each new run using
the shorter names shown in the lesson commands:

| Name inside the run directory | Organizer file |
| --- | --- |
| `data/historical.nc` | `tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc` |
| `data/ssp585.nc` | `tas_Amon_ACCESS-CM2_ssp585_r1i1p1f1_gn_201501-210012.nc` |

The historical file comes from the organizer's shared archive; Evgenia's
repository supplies the future scenario file. The fetch helper uses the pinned
source revision and checks both hashes:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Historical, 1850–2014 | 148190686 | `3e106e8430f04cd2b260a7230b1e461ccebdda338d09e3f07e8497678c5c6f0f` |
| SSP5-8.5, 2015–2100 | 77137066 | `8f0d0cee4c370c0c30acc31ef6bf03a2592ee3dfd827a13e37716cd7484909b1` |

Both files are cached by the Binder build and are present on the configured Mac.
The notebook requires them to exist and does not download replacements. If a
file is missing, execution stops. When downloading is unavailable, copy the
matching organizer files into the repository's `data/access_cm2/` directory.
Synthetic software-test data remain explicitly labeled and do not represent
ACCESS-CM2 results.

## Run locally or in Binder

On the configured Mac, open `Launch_Updated_Notebook.command` in the parent
project folder or use `activate_fresh_eyes.sh`. The existing environment has
CDO 2.5.0, NCO 5.3.9, Python 3.12.14 and JupyterLab 4.6.3, running through Rosetta
on the Apple Silicon Mac. See [LOCAL_MAC_SETUP.md](LOCAL_MAC_SETUP.md) for setup.

On another compatible machine, run these installation commands from the
repository folder:

```bash
conda env create -f binder/environment.yml
conda activate fresh-eyes
python scripts/fetch_updated_data.py
jupyter lab notebooks/00_yl_20_minute_binder_demo.ipynb
```

Once the environment and inputs are installed, the notebooks can run offline.
The [Binder environment guide](../binder/README.md) also describes the Linux
devcontainer. Recreate an installed Conda environment on another machine rather
than copying its directory. NCO 5.1.9 or later is needed for `ncra --mro`.

Open the latest published notebooks online:

- [Main notebook in Binder](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Practice notebook in Binder](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/04_monthly_anomaly_hands_on.ipynb)
- [BIDS Binder alternative](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

Older commit-pinned links select their earlier notebook revisions. Binder
sessions are temporary; save your edited notebook and results before leaving.
The local installation is available when public Binder is unavailable.

## Results and batch extension

Each run contains independent `python/`, `cdo/` and `nco/` products,
`updated_validation.json` and `updated_comparison.png`. Five products from each
command-line route are compared with the reference: monthly climatology,
monthly anomalies, duration-weighted map, Arctic monthly series and annual
series. Tolerance is 0.0003°C absolute with zero relative tolerance. Coordinates,
calendar labels and masks must agree; the reference-period monthly residual
must approach zero and each annual value must equal its 12-month mean.

**The teaching notebooks are fixed to 1979–2024.** Their date selections and
record indices are written for 552 months. Changing a single year or index does
not update the other dependent commands. Use the separate batch launcher for
the 2100 extension, from the parent project folder containing the launcher:

```bash
bash Run_Updated_Demo.command --real --end-year 2100
```

The batch workflow supports 1979–2100 and produces 122 annual values while
keeping the 1981–2010 reference fixed. It is separate from the fixed-date lesson
notebooks. Changing the analysis period also changes the period-mean map and
stripe color scale.

## Verification by revision

The current one-command/one-query format with bare command names passed complete local, in-process
IPython execution using real ACCESS-CM2 data for 1979–2024: 552 monthly fields
and 46 annual values. Every code cell completed successfully, every query cell
produced output, and all standard error streams were empty.

| Notebook | Processing commands | Result queries | Support cells | Completed code cells |
| --- | ---: | ---: | ---: | ---: |
| Main | 57: 20 CDO + 37 NCO | 57 | 5 | 119/119 |
| Practice | 63: the main lesson + six exercise pairs | 63 | 8 | 134/134 |

All ten product comparisons passed in each notebook. The largest absolute
difference from the independent reference was **3.552713678800501e-15°C**;
method and coordinate checks also passed. The
[plain-command verification record](plain_commands_verification_20261109.json)
records notebook hashes, cell counts, numerical results and the execution
method. This is local in-process evidence. Online CI and a live Binder check
of this revision are pending at publication. Literal-routing checks also verify
all 126 command strings and arguments, including NCO brace expressions, and
confirm that a failed external command raises an error.

Earlier evidence keeps its original scope:

| Evidence | Revision and scope |
| --- | --- |
| [Command-and-result checks](command_observe_verification_20261109.json) and [Linux CI](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42593420426) | `fcc5539...`: all 119/134 cells executed; focused live Binder CDO/NCO command/query checks also passed, before the change to bare command names |
| [Simplified-command checks](simple_commands_verification_20261109.json) | `4228f76...`: the earlier 24/30-cell notebooks, before processing and result queries were split into individual cells |
| [Simplified-command Linux CI](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42589034931) | `4228f76...`: successful build and 24/30-cell kernel execution |
| [Earlier inline-command checks](inline_commands_verification_20261109.json) | `88d9fc0...`: earlier 24/30-cell local execution |
| [Public Binder receipt](binder_launch_verification_20261109.json) | `fe1dc89...`: earlier 8/10-cell notebooks executed in the public Jupyter UI |

For `4228f76...`, the main Binder page opened and selected command sections were
visually checked. No additional browser Run All was performed; both notebooks'
actual kernel execution was verified by CI and the Binder build. Those results
do not verify the current command-and-result revision.

Direct numerical comparison with Evgenia's saved ESMValTool products and an
interactive local Mac Jupyter browser session remain separate checks. Earlier
1979–2014 sources are retained under `notebooks/legacy_*.ipynb`.
