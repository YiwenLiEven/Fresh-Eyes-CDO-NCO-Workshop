# Fresh Eyes: climate analysis with CDO and NCO

**Yiwen Li · Fresh Eyes on CMIP**

Calculate temperature anomalies, Arctic time series and climate stripes from
real **ACCESS-CM2 historical + SSP5-8.5** monthly data. CDO and NCO process the
original files independently, following
[Evgenia Galytska's ESMValTool recipe](https://github.com/egalytska/Fresh_eyes/blob/040b9c7962355b1f8fa1312b7af867b458102b85/ESMValTool/recipe_temperature_anomalies.yml).

## Open a notebook

- [Main notebook in Binder](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Practice notebook in Binder](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/04_monthly_anomaly_hands_on.ipynb)
- [BIDS Binder alternative](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Notebook files](notebooks/) · [Data, methods and local use](docs/UPDATED_DEMO.md)

The `main` links select the current published notebooks. An older commit-pinned
link opens that earlier revision. Save edited notebooks and results before
closing a temporary Binder session.

## Run one command, then inspect its result

1. Start with the Data cell and use **Shift+Enter** to run cells in order,
   including collapsed cells. Each new run gets its own output directory.
2. Run one direct processing command, such as `cdo` or `ncks`, in its own cell.
   The commands use the actual input names `data/historical.nc` and
   `data/ssp585.nc`, and write results under `cdo/` or `nco/`.
3. Immediately run the next cell: a short CDO/NCO query displays the new file's
   dimensions, dates, variables or sample values. Compare that output with the
   explanation before moving to the next processing command.
4. View the numerical comparison, maps, Arctic series and annual stripes.
   An independent Python calculation supplies the reference; its support code
   remains collapsed.

Run the commands exactly as shown. In a terminal, use the same command text
and work in the run directory printed by the Data cell. To repeat the whole
calculation, return to the first cell and start a new run; earlier files remain
in their previous output directory.

## Common calculation

| Product | Definition |
| --- | --- |
| Monthly reference | 1981–2010 mean for each calendar month |
| Monthly anomalies | 1979–2024: 552 monthly fields |
| Mean anomaly map | Month-duration weighted mean |
| Arctic monthly series | Latitude centres 65–90°N, equal grid-point weights |
| Annual stripes | 46 annual values, equal weight for the 12 monthly samples |

Five products from each route are compared with the independent reference at
an absolute tolerance of 0.0003°C, with coordinate, calendar, baseline and
annual-mean checks. The teaching commands use fixed dates and record counts for
1979–2024. The optional 2100 analysis uses the separate batch launcher described
in the [local guide](docs/UPDATED_DEMO.md#results-and-batch-extension).

## Run locally

```bash
conda env create -f binder/environment.yml
conda activate fresh-eyes
python scripts/fetch_updated_data.py
jupyter lab notebooks/00_yl_20_minute_binder_demo.ipynb
```

On Yiwen's configured Mac, `Launch_Updated_Notebook.command` uses the existing
CDO/NCO/Jupyter environment. Both real inputs are already available. Once the
environment and data are installed, the notebooks can run offline. See the
[Mac setup guide](docs/LOCAL_MAC_SETUP.md) and
[Binder/devcontainer configuration](binder/README.md).

Real ACCESS-CM2 is the default. The Binder build caches both hash-checked input
files. Missing real inputs stop execution; separately labeled synthetic data
remain available for software tests.

## Verification by revision

The current notebooks with bare command names passed complete local, in-process
IPython execution with real ACCESS-CM2 data: **119/119 code cells** in the main
notebook and **134/134** in the practice notebook. The main lesson contains
20 CDO and 37 NCO processing commands, each followed by a query cell; the practice
notebook adds six exercise pairs. Every query produced output, and no standard
error output was recorded.

All ten product comparisons passed in each notebook; the largest absolute
difference from the reference was **3.552713678800501e-15°C**. See the
[plain-command verification record](docs/plain_commands_verification_20261109.json)
for notebook hashes, cell counts and execution details. It also confirms that
all 126 command strings, including NCO array literals, reach the installed tools
unchanged and that failed commands raise an error. Online CI and a live Binder
check of this revision are pending at publication.

The preceding `fcc5539...` revision passed [Linux CI run 42593420426](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42593420426)
with all 119/134 cells executed. Its main page also passed a focused live Binder
check of CDO selection/query pairs and an NCO selection/query pair. That record
predates the current change to bare command names.

The [previous simplified-command record](docs/simple_commands_verification_20261109.json)
and successful [Linux CI run 42589034931](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42589034931)
apply to revision `4228f76...`, whose main and practice notebooks had 24 and 30
code cells. That version's main page opened and its commands were visually
checked in Binder; no additional browser Run All was performed. Those checks
remain evidence for the earlier revision. Comparison with Evgenia's saved
ESMValTool products is a separate check.

## Attribution

Original workshop: [Abhnil / Fresh_Eyes_on_CMIP_Data_Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop).
Shared reference: [Evgenia Galytska / Fresh_eyes](https://github.com/egalytska/Fresh_eyes).
CDO/NCO adaptations and learning material: Yiwen Li's workshop.
Earlier notebook sources remain under `notebooks/legacy_*.ipynb`.
