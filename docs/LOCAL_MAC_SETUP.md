# Local Mac demonstration setup

Verified on 9 November 2026. The existing environment in the adjacent
`YL_CDO_NCO_Seminar/.runtime` directory supplies the required tools. No system
installation, shell-profile changes or replacement of that environment was needed.

| Component | Verified version or status |
| --- | --- |
| CDO | 2.5.0 |
| NCO | 5.3.9, including `ncra --mro` |
| Python | 3.12.14 |
| JupyterLab | 4.6.3 |
| Scientific libraries | xarray, NumPy, netCDF4, cftime, matplotlib and cartopy import successfully |
| Test runner | pytest 8.1.1 from the existing local package cache; isolated under `.local-tools/test-packages` |
| Architecture | x86_64 environment running successfully through Rosetta on the Apple Silicon Mac |

## Open and run

The following launchers are in the parent project directory, alongside this
repository and the previous seminar folder.

- Double-click `Launch_Updated_Notebook.command` to open
  `notebooks/00_yl_20_minute_binder_demo.ipynb` in local JupyterLab, using real
  ACCESS-CM2 historical and SSP585 data by default.
- Double-click `Run_Updated_Demo.command` to execute all three updated routes and
  their comparison with real ACCESS-CM2 historical and SSP585 data by default.
- In Bash or zsh, run `source ./activate_fresh_eyes.sh` from the parent project
  directory to activate the tools and change into this repository.

For the real organizer inputs, run these commands from the parent directory:

```bash
bash Run_Updated_Demo.command
bash Launch_Updated_Notebook.command
```

The first command downloads/checks the historical and SSP585 files and runs the
updated workflows. The second chooses real-data mode in Jupyter. Its notebook
preparation cell requires both files to be present and stops with a clear error
if either is missing; it does not download them automatically. Run
`python scripts/fetch_updated_data.py` from the repository first when needed.
A failed real download stops the run; neither entry point silently substitutes
synthetic input. For a longer scenario
analysis, the command-line runner also accepts `--end-year 2100`. Both launchers
continue to accept `--real` explicitly.

Synthetic input is an explicit software-test option:

```bash
bash Run_Updated_Demo.command --synthetic
bash Launch_Updated_Notebook.command --synthetic
```

These commands display the synthetic label and never represent their values as
ACCESS-CM2 results. An explicit `WORKSHOP_MODE=synthetic` environment setting also
selects synthetic mode; command-line mode options override that setting.

The activation helper detects its location and supports a `FRESH_EYES_ENV`
override for a different prepared environment. All application caches stay inside
the project. To check versions without opening Jupyter, run
`bash Launch_Updated_Notebook.command --check` or
`bash Run_Updated_Demo.command --check`. Neither check downloads data, starts a
server or runs the scientific calculations. Both support `--help`.

## Execution evidence

The original 1979–2014 historical task was executed against the existing real
ACCESS-CM2 historical file, with 1,980 monthly records on its 144 × 192 grid.
Python and CDO completed; the first NCO run exposed a NetCDF3 record-dimension
limitation. Its initial selection now explicitly writes NetCDF4, allowing the
time and climatology-month axes. NCO and the complete comparison were then rerun
successfully. The original raw file was not changed.

- `outputs/local_historical/three_way_validation.json`: all eight comparisons
  pass at absolute tolerance 0.0003 °C; largest difference is
  0.0000259399414091 °C.
- `outputs/local_historical/three_way_comparison.png`: real historical results.
- `outputs/local_historical/run.log`: initial execution, including the original
  NCO format failure and CDO/HDF5 file-probe messages.
- `outputs/local_historical/nco_retry.log` and `comparison.log`: successful
  processing after the format fix and all eight numerical checks.
- `outputs/local_updated_synthetic_20261109_122525_60219/updated_validation.json`:
  actual execution through the new root launcher; all ten updated product
  comparisons pass, together with the monthly baseline and annual-definition
  checks. These are synthetic software test results.

The real historical check above verifies the previous historical scientific
definition. Separate saved real-data reports verify the updated historical-plus-
SSP585 definition, with both input files now staged in `data/access_cm2`:

- `outputs/real_2024/updated_validation.json`: all ten comparisons pass for
  1979–2024, 552 months and 46 annual values; maximum difference is
  3.5527136788e-15 °C.
- `outputs/real_2100/updated_validation.json`: all ten comparisons pass for
  1979–2100, 1,464 months and 122 annual values; maximum difference is
  2.4868995752e-14 °C.

Both reports explicitly identify ACCESS-CM2 and `synthetic: false`. Their
invariants also pass. These establish agreement among the three local processing
routes, not a comparison against Evgenia's saved ESMValTool products.

## Practical details

CDO 2.5.0 rejects data/output paths containing spaces even when the shell quotes
them. The launchers change into the repository and use relative paths to avoid
this issue. Keep those relative paths when running examples manually.

The command-line environment and both processing demonstrations have been tested.
Jupyter's packages and version check work. Notebook kernel execution from the
restricted automation shell could not bind a localhost port, so that check does
not establish an interactive Jupyter session. Launch the notebook from a normal
Terminal or Finder session. The launcher preserves Jupyter authentication and
binds the server to the local machine only.

The local pytest 8.1.1 differs from the Binder manifest's version range. The local
environment is therefore a working demonstration environment, not a byte-for-byte
copy of the Binder image. Do not copy its `.runtime` directory to another Mac;
create an environment from the repository manifest instead.
