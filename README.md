# Fresh Eyes: climate analysis with CDO and NCO

**Yiwen Li · Fresh Eyes on CMIP**

Calculate temperature anomalies, Arctic time series and climate stripes from
real **ACCESS-CM2 historical + SSP5-8.5** monthly data. CDO and NCO process the
original files independently, following
[Evgenia Galytska's ESMValTool recipe](https://github.com/egalytska/Fresh_eyes/blob/040b9c7962355b1f8fa1312b7af867b458102b85/ESMValTool/recipe_temperature_anomalies.yml).

## Open a notebook

- **[Short annual-stripes lesson in Binder — recommended for 20 minutes](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/05_annual_stripes_short_demo.ipynb)**:
  11 CDO + 9 NCO commands, each followed by a result query. Compare final annual
  Arctic anomalies and stripes. See the [scope and timing guide](docs/SHORT_ANNUAL_DEMO.md).
- [Complete five-product workflow in Binder](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Practice notebook in Binder](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/04_monthly_anomaly_hands_on.ipynb)
- [BIDS Binder alternative for the short lesson](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/05_annual_stripes_short_demo.ipynb)
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
4. View the annual-series comparison and stripes. The complete notebooks also
   include monthly fields and maps. An independent Python calculation supplies
   the reference; its support code remains collapsed.

Run the commands exactly as shown. In a terminal, use the same command text
and work in the run directory printed by the Data cell. To repeat the whole
calculation, return to the first cell and start a new run; earlier files remain
in their previous output directory.

## Common calculation

The short lesson calculates annual Arctic temperature, subtracts the 1981–2010
annual reference, and compares the resulting 46 annual anomalies with the
complete monthly-anomaly reference. Equal month weights, complete calendar
years and fixed spatial weights make the annual results equivalent. It does
not calculate the intermediate monthly fields or the weighted map.

The complete workflow and practice notebook calculate all five products:

| Product | Definition |
| --- | --- |
| Monthly reference | 1981–2010 mean for each calendar month |
| Monthly anomalies | 1979–2024: 552 monthly fields |
| Mean anomaly map | Month-duration weighted mean |
| Arctic monthly series | Latitude centres 65–90°N, equal grid-point weights |
| Annual stripes | 46 annual values, equal weight for the 12 monthly samples |

In the complete notebooks, five products from each route are compared with the independent reference at
an absolute tolerance of 0.0003°C, with coordinate, calendar, baseline and
annual-mean checks. The teaching commands use fixed dates and record counts for
1979–2024. The optional 2100 analysis uses the separate batch launcher described
in the [local guide](docs/UPDATED_DEMO.md#results-and-batch-extension).

## Run locally

```bash
conda env create -f binder/environment.yml
conda activate fresh-eyes
python scripts/fetch_updated_data.py
jupyter lab notebooks/05_annual_stripes_short_demo.ipynb
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

The **10 November revision** adds the short annual lesson and simplifies the
complete NCO selections and record-dimension handling. All three notebooks
passed complete local, in-process IPython execution with real ACCESS-CM2 data:

| Notebook | Processing commands | Code cells passed | Comparison scope |
| --- | ---: | ---: | --- |
| Short annual lesson | 11 CDO + 9 NCO | 45/45 | 46 annual anomalies per route |
| Complete workflow | 20 CDO + 36 NCO | 117/117 | Five products per route |
| Practice | Complete workflow + six exercise pairs | 132/132 | Five products and exercises |

All result queries produced output and all captured stderr streams were empty.
The short lesson also passed its synthetic-data execution. Its largest real
annual difference from the complete monthly-anomaly reference was
**2.61124455e-13°C**. See the
[short-lesson verification record](docs/short_annual_verification_20261110.json).
The complete notebooks passed all ten product comparisons, with maximum error
**3.552713678800501e-15°C**, and their five NCO products exactly matched the
previous local version. See
[nco_options_verification_20261110.json](docs/nco_options_verification_20261110.json).
These JSON files record the local checks before publication. **Online CI and a
live Binder check are pending for this release.**

Earlier evidence remains specific to its source revision:

- `b71a1fd...` (9 November): the
  [bare-command verification record](docs/plain_commands_verification_20261109.json)
  and [Linux CI run 42596677410](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42596677410)
  cover the previous 119/134-cell notebooks. A focused live Binder check also
  ran CDO and NCO selection/query pairs. Literal-routing checks preserved all
  126 practice command strings, including NCO arrays, and checked error propagation.
- `fcc5539...`: [Linux CI run 42593420426](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42593420426)
  executed all 119/134 cells; a focused live Binder check covered selection/query
  pairs before the change to bare command names.
- `4228f76...`: the [earlier simplified-command record](docs/simple_commands_verification_20261109.json)
  and [Linux CI run 42589034931](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42589034931)
  cover the earlier 24/30-cell notebooks. Their main page and command layout were
  checked in Binder without an additional browser Run All.

These earlier checks do not verify the 10 November release. Comparison with
Evgenia's saved ESMValTool products is a separate check.

## Attribution

Original workshop: [Abhnil / Fresh_Eyes_on_CMIP_Data_Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop).
Shared reference: [Evgenia Galytska / Fresh_eyes](https://github.com/egalytska/Fresh_eyes).
CDO/NCO adaptations and learning material: Yiwen Li's workshop.
Earlier notebook sources remain under `notebooks/legacy_*.ipynb`.
