# Fresh Eyes: climate analysis with CDO and NCO

**Yiwen Li · Fresh Eyes on CMIP**

Calculate temperature anomalies, Arctic time series and climate stripes from
real **ACCESS-CM2 historical + SSP5-8.5** monthly data. CDO and NCO each process
the original files independently. The calculation follows
[Evgenia Galytska's ESMValTool recipe](https://github.com/egalytska/Fresh_eyes/blob/040b9c7962355b1f8fa1312b7af867b458102b85/ESMValTool/recipe_temperature_anomalies.yml).

## Open a notebook

- [Main notebook in BIDS Binder](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Practice notebook in BIDS Binder](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/04_monthly_anomaly_hands_on.ipynb)
- [Generic mybinder.org fallback](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Notebook files](notebooks/) · [Data, methods and local setup](docs/UPDATED_DEMO.md)

Use the latest `main` links above for the current command-by-command notebooks.
An older commit-pinned link opens that earlier revision. Binder sessions are
temporary; download your edited notebook and results before leaving.

## Run the cells in order

1. Start at the first cell and use **Shift+Enter** to run each cell, including
   collapsed cells. Their output remains visible.
2. Work through **nine CDO steps** and **ten NCO steps**. Both notebooks show
   the actual commands in their `%%bash -e` cells: `cdo`, `ncks`, `ncap2`, `ncwa`
   and the other operators. Each step explains its input, output and options.
3. Compare the results and view the maps, Arctic series and annual stripes.
   An independent Python calculation supplies the numerical reference; its
   support cells are collapsed by default.
4. Use the practice notebook to explore the reference period and Arctic region.
   To repeat the calculation, restart the kernel and run from the first cell.
   Each full run creates a new output folder and keeps the previous results.

Commands retain the options needed for the calculation. CDO uses `-b F64` once
when joining the experiments, so temperatures are stored in double precision
before arithmetic. NCO selects classic NetCDF once in its first historical
extraction; subsequent products inherit that format.

## Common calculation

| Product | Definition |
| --- | --- |
| Monthly reference | 1981–2010 mean for each calendar month |
| Monthly anomalies | 1979–2024: 552 monthly fields |
| Mean anomaly map | Month-duration weighted mean |
| Arctic monthly series | Latitude centres 65–90°N, equal grid-point weights |
| Annual stripes | 46 annual values, equal weight for the 12 monthly samples |

The map and annual series use different time weights. Five products from each
command-line route are compared with the independent reference at an absolute
tolerance of 0.0003°C, with coordinate, calendar, baseline and annual-mean checks.
Set `WORKSHOP_END_YEAR=2100` before launching Jupyter for the optional extension.

## Run locally

```bash
conda env create -f binder/environment.yml
conda activate fresh-eyes
python scripts/fetch_updated_data.py
jupyter lab notebooks/00_yl_20_minute_binder_demo.ipynb
```

On Yiwen's configured Mac, the project-level `Launch_Updated_Notebook.command`
uses the existing CDO/NCO/Jupyter environment. Both real input files are already
available there. Local use can continue offline once the environment and data
are installed. See the [Mac setup guide](docs/LOCAL_MAC_SETUP.md) and
[Binder/devcontainer configuration](binder/README.md).

Real ACCESS-CM2 is the default. The Binder build caches both hash-checked inputs;
missing real files stop execution. `WORKSHOP_MODE=synthetic` is an explicit
software-test option, with synthetic labels on its output.

## Verification by revision

The current revision simplifies the command options while preserving the
scientific definitions and the 24-cell main / 30-cell practice structure.
Local real-data checks completed **24/24 main cells and 30/30 practice cells**
using IPython in-process, including the actual Bash command cells. All ten
product comparisons passed, with maximum absolute difference
**3.552713678800501e-15°C**, together with the coordinate, calendar and method
checks. See the [simplified-command verification record](docs/simple_commands_verification_20261109.json).
This verifies local cell execution; a live Jupyter/Binder run of this new
revision remains to be recorded.

The [earlier inline-command record](docs/inline_commands_verification_20261109.json)
applies to revision `88d9fc0...`, before this option simplification. That version
also passed its [Linux CI run](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42585557534).
Those results do not establish execution or live-browser verification of the
current simplified commands.

The [earlier public Binder record](docs/binder_launch_verification_20261109.json)
verifies revision `fe1dc89...`, whose main and practice notebooks had **8 and 10
code cells**. The [earlier Linux CI receipt](docs/updated_verification/github_actions_build.json)
records the corresponding build on `95b89e8...`. Those reports remain evidence
for their recorded revisions.
Comparison with Evgenia's saved ESMValTool products remains a separate check.

## Attribution

Original workshop: [Abhnil / Fresh_Eyes_on_CMIP_Data_Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop).
Shared scientific reference: [Evgenia Galytska / Fresh_eyes](https://github.com/egalytska/Fresh_eyes).
CDO/NCO adaptations and learning material: Yiwen Li's workshop.
Earlier notebook sources remain under `notebooks/legacy_*.ipynb`.
