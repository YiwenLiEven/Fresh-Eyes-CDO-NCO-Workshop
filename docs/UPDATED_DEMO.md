# Updated CDO/NCO seminar: local use and Binder preparation

## Audience layout: prepare once, teach CDO/NCO

Step 01 is now a data card. The presenter runs the folded preparation and reference
cells before the talk. They find and check the same input files and create a fresh
output folder. Their Python source is available behind the ellipsis; participants
do not need to read or edit it. All CDO/NCO `%%bash` cells remain expanded.

The revision changes Markdown and visibility metadata only. Every executable
cell source is identical to the previously tested version, with 8 main-notebook
cells and 10 participant cells. Folded cells still run; do not delete or skip them
when starting a fresh kernel. Use the latest `main` Binder link in README for this
layout; an old commit-pinned URL will continue to display the old layout.


Prepared 9 November 2026 for Yiwen Li's Fresh Eyes on CMIP contribution.
All teaching material is in English. The two active notebooks are:

- `notebooks/00_yl_20_minute_binder_demo.ipynb`: the prepared 20-minute seminar.
- `notebooks/04_monthly_anomaly_hands_on.ipynb`: standalone participant practice.

## Source and scope

The scientific target is Evgenia Galytska's
[updated ESMValTool recipe](https://github.com/egalytska/Fresh_eyes/blob/040b9c7962355b1f8fa1312b7af867b458102b85/ESMValTool/recipe_temperature_anomalies.yml),
read from GitHub on 9 November 2026. The source repository marks its former
`stripes_EG` notebook as old. The general processing examples originated in
[Abhnil's Python workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop).
CDO and NCO remain independent full processing routes; Python provides a third
implementation, validation and final figures.

| Scientific choice | Updated seminar | Earlier seminar |
|---|---|---|
| Model experiments | Historical + SSP5-8.5 | Historical only |
| Analysis period | 1979–2024, 552 months / 46 years | 1979–2014, 432 months / 36 years |
| Monthly reference | 1981–2010, 30 values per calendar month | Same |
| Mean anomaly map | Time-bound duration weights | Equal monthly samples |
| Arctic monthly mean | 65–90°N grid centres, equal grid-point weights | Same |
| Arctic annual mean | Equal weight for each of the 12 months | Same |

The source recipe requests monthly `anomalies`, then `extract_time`. Its map uses
`climate_statistics(period: full, operator: mean)`, while the Arctic routes use
`extract_region`, `zonal_statistics(mean)`, `meridional_statistics(mean)` and, for
annual output, `annual_statistics(mean)`. The duration-weighted map and equal-month
annual interpretation were checked against the locally installed ESMValCore 2.10.0
source. This source-code audit is separate from executing Evgenia's recipe or
comparing her saved output files.

## Data modes

**The default is real ACCESS-CM2 historical + SSP5-8.5 output.** Both source
files are staged on the prepared Mac and cached during the Binder build. The
data mode appears at the start of each notebook and on each comparison figure.
If either real file is missing, execution stops; there is no automatic
substitution of synthetic input.

An optional software-test mode is available by setting `WORKSHOP_MODE=synthetic`.
Its figures and reports remain explicitly labeled as synthetic.

Real mode needs both files in `data/access_cm2/`:

```text
tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc
tas_Amon_ACCESS-CM2_ssp585_r1i1p1f1_gn_201501-210012.nc
```

The historical file comes from the organizer's shared archive; the future file
is supplied by the user and published by Evgenia in the updated repository.
The download helper is `python scripts/fetch_updated_data.py`. It uses the
pinned source revision and checks the input hashes before accepting the files.
The validated local input hashes are:

| Input | Bytes | SHA-256 |
|---|---:|---|
| Historical, 1850–2014 | 148190686 | `3e106e8430f04cd2b260a7230b1e461ccebdda338d09e3f07e8497678c5c6f0f` |
| SSP5-8.5, 2015–2100 | 77137066 | `8f0d0cee4c370c0c30acc31ef6bf03a2592ee3dfd827a13e37716cd7484909b1` |

The future hash identifies the supplied and tested file; a matching download
ensures that the same bytes are used. The notebook setup requires existing files
and does not start a download. If a download is unavailable, place the organizer's
original files in the directory above, or supply explicit paths:

```bash
export WORKSHOP_MODE=real
export WORKSHOP_HISTORICAL=/absolute/path/to/historical.nc
export WORKSHOP_FUTURE=/absolute/path/to/ssp585.nc
jupyter lab notebooks/00_yl_20_minute_binder_demo.ipynb
```

Every route applies the 1981–2010 historical reference to both experiment segments.
It does not recenter the future period against itself. The shared input checker
rejects mismatched grids, calendars and model/member metadata, missing months,
non-finite values and time bounds that do not describe complete calendar months.

## Run locally

On the prepared Mac, open the project-level `Launch_Updated_Notebook.command`,
or use the project-level activation script to put the tested environment on PATH.
The existing environment contains CDO 2.5.0, NCO 5.3.9, Python 3.12 and Jupyter.
It is an Intel Conda environment running through Rosetta on this Apple Silicon Mac.
Do not copy an installed Conda environment to another location; recreate it there.

On another compatible machine, create the environment from this repository:

```bash
conda env create -f binder/environment.yml
conda activate fresh-eyes
python scripts/fetch_updated_data.py
jupyter lab notebooks/00_yl_20_minute_binder_demo.ipynb
```

From the repository root, run the complete real comparison without Jupyter:

```bash
python scripts/fetch_updated_data.py
bash scripts/run_updated_workflows.sh \
  data/access_cm2/tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc \
  data/access_cm2/tas_Amon_ACCESS-CM2_ssp585_r1i1p1f1_gn_201501-210012.nc \
  outputs/updated_real 2024
```

The main analysis selects 1979–2024 before loading arrays, rather than loading
the full historical and future time series. For a small explicit software test,
run `python scripts/generate_updated_fixture.py data/updated_fixture` and supply
`data/updated_fixture/historical.nc` and `data/updated_fixture/ssp585.nc` to the
runner, with a separate synthetic output directory.
The output directory contains independent `python/`, `cdo/` and `nco/` products,
`updated_validation.json` and `updated_comparison.png`.

## Separate processing routes

```bash
python scripts/check_updated_inputs.py HISTORICAL.nc SSP585.nc --end-year 2024
python scripts/run_python_updated.py HISTORICAL.nc SSP585.nc outputs/run/python --end-year 2024
bash scripts/run_cdo_updated.sh HISTORICAL.nc SSP585.nc outputs/run/cdo 2024
bash scripts/run_nco_updated.sh HISTORICAL.nc SSP585.nc outputs/run/nco 2024
python scripts/compare_updated_workflows.py outputs/run
```

CDO alone performs its merge, conversion, climatology, anomalies and reductions.
NCO alone performs the corresponding operations from the same raw inputs. The
shared Python checker is read-only. The fixture generator supplies explicitly
synthetic test inputs; neither supplies intermediate scientific results to the
command-line routes.

The NCO annual step requires `ncra --mro` (NCO ≥ 5.1.9). Classic NetCDF intermediate
files avoid repeated HDF5 probing diagnostics. Each notebook creates a new run
folder; scripts use overwrite flags for reproducible reruns in a chosen folder.

## Numerical checks and interpretation

Five products from each command-line route are compared with Python: monthly
climatology, monthly anomaly fields, duration-weighted map, Arctic monthly series
and Arctic annual series. The tolerance is 0.0003°C absolute with relative tolerance
zero. Calendar labels and grid coordinates must align, masks must match, the
reference-period monthly residual must be close to zero, and the annual series
must equal the arithmetic mean of each year's 12 monthly values.

A synthetic PASS tests implementation consistency. It does not establish agreement
with ACCESS-CM2 or with Evgenia's saved ESMValTool outputs. Keep those claims
separate in presentation and publication records. A map is a period-mean anomaly,
not a trend; a real-data run is one simulation, not observations.

To extend the exercise to 2100, pass `2100` as the final shell argument, or set
`WORKSHOP_END_YEAR=2100` before launching Jupyter. This produces 122 annual values.
The main seminar remains 1979–2024; changing the end year also changes the
period-mean map and the common stripe color scale.

## Local notebook verification

All 8 seminar code cells and all 10 participant code cells passed using the
default real ACCESS-CM2 inputs. Both runs passed ten product comparisons,
including full-year annual bounds, with a maximum difference of
3.552713678800501e-15°C. The final cell stderr streams were empty.
[UPDATED_NOTEBOOK_CHECKS.json](UPDATED_NOTEBOOK_CHECKS.json) records the exact
notebook hashes, cell counts, software versions, numerical results, method and
limits. Earlier synthetic evidence is retained in
[UPDATED_NOTEBOOK_CHECKS_SYNTHETIC.json](UPDATED_NOTEBOOK_CHECKS_SYNTHETIC.json). A real-data PASS
establishes agreement among these Python/CDO/NCO implementations; comparison
with Evgenia's saved ESMValTool products is a separate check.

The execution sandbox prevented a normal Jupyter kernel from binding its local
socket. The checks therefore used IPython in-process, including the prepared
Bash cells, via `scripts/check_updated_notebook_cells.py`. They verify the cell
code but do not establish that a Jupyter browser session or Binder image launched.

## Public Binder and publication

The updated code is published in
[YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop).
Use the tested code revision `fe1dc89f49a4cd32c72283056d2b5e1ce29d362b` for seminar links:

- [20-minute seminar — recommended BIDS Binder](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)
- [Participant practice — BIDS Binder](https://bids.mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b?urlpath=lab/tree/notebooks/04_monthly_anomaly_hands_on.ipynb)
- [Generic mybinder.org fallback](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/fe1dc89f49a4cd32c72283056d2b5e1ce29d362b?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

The public BIDS Binder session launched successfully, and the main notebook was
rerun in live Jupyter through all 8 code cells. The UI reached Idle / 100%.
The run used real ACCESS-CM2 historical + SSP5-8.5 data: 552 months, 1979–2024,
with the 1981–2010 monthly reference. All ten product comparisons passed, with
a maximum difference of 1.509903313490213e-14°C. The final figure was inspected
for its real-data label and corresponding Python/CDO/NCO maps, Arctic series and
annual stripes. Recorded versions were CDO 2.6.5, NCO 5.4.2 and Python 3.11.18.
See [binder_launch_verification_20261109.json](binder_launch_verification_20261109.json).

The participant notebook also passed all 10 code cells after Restart Kernel
and Run All in the same public BIDS session, reaching Idle / 100%. Its setup
showed real 1979–2024 inputs; the final cell passed the monthly reference-residual
check at 5.968558980384842e-14°C. The 70°N exercise gave a CDO/NCO maximum
difference of 3.019806626980426e-14°C; changing the boundary from 65°N to 70°N
changed the monthly values by up to 1.2266452280680342°C. These are two different
comparisons: the first tests implementation agreement, the second changes the
scientific region. Both notebooks also passed the fresh Linux build through
`nbconvert`; the verification writer checked their source hashes and cell counts. Linux evidence is published in
[linux_build.json](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/blob/main/docs/updated_verification/linux_build.json) and
[linux_compaction.json](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/blob/main/docs/updated_verification/linux_compaction.json). The eight-test Linux suite passed with one
NumPy compatibility warning, and output compaction completed.

A subsequent CI-verified code revision is
[95b89e87aacacde7ec98aaf94f0188214a2d6dea](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/commit/95b89e87aacacde7ec98aaf94f0188214a2d6dea),
which adds downloader retries. [CI run 8, attempt 2](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/42568209901) passed for that
revision, including the `scientific-equivalence` job and one saved artifact. The
run took 3 minutes 17 seconds; its Node.js 20 deprecation warning was not a
failure. The downloaded [GitHub Actions build receipt](updated_verification/github_actions_build.json)
records that CI result. The public launch record applies to the pinned `fe1dc89f49a4cd32c72283056d2b5e1ce29d362b` revision, not to every
later commit. Direct numerical comparison with Evgenia's saved ESMValTool
products and an interactive local Mac Jupyter browser test remain unverified.

Binder sessions are temporary; save outputs and edited notebooks before leaving.
Keep the working local environment available for the seminar. The old seminar
and participant notebook sources are retained under the `legacy_` prefix, and
older pinned launch links still identify those earlier code revisions.
