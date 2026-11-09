# Binder environment

The current seminar environment uses conda-forge for Python, CDO and NCO. NCL is optional legacy material and is not required by the current notebooks. NCO must be version 5.1.9 or later for the grouped annual-average operation.

## Build and checks

`environment.yml` installs the scientific tools and JupyterLab. `postBuild`
installs this repository and performs separate regression and demonstration checks:

1. Run the legacy 1979–2014 synthetic regression: eight comparisons, retained
   under `outputs/demo/monthly/`.
2. Run the updated synthetic software test and the pytest suite.
3. Download and hash-check both real ACCESS-CM2 historical and SSP585 inputs,
   then run independent Python, CDO and NCO routes for 1979–2024: ten product
   comparisons plus calendar, coordinate, baseline and annual-definition checks.
4. Execute both active notebooks with the real inputs and write the build report.

A successful build writes `outputs/verification.json` with tool/package versions,
the real-data 1979–2024 validation and notebook execution evidence. Legacy
synthetic evidence is recorded in a separate `legacy` section. The current
real-data report and figure are
`outputs/updated_real_build/updated_validation.json` and
`outputs/updated_real_build/updated_comparison.png`. Executed notebook copies are
in `outputs/executed/`; each notebook's own output directory is recorded in the
verification report. The default analysis has 552 monthly values and 46 annual
values, using the historical 1981–2010 monthly reference for both experiments.

The devcontainer bootstrap uses official micromamba under `.runtime/bin` to
create `.runtime/env` from this same manifest, then executes `binder/postBuild`
inside that environment. Its interpreter and terminal PATH select these tools;
the bootstrap does not install distribution CDO/NCO packages or modify system
package repositories. The first build needs network access and downloads the
real inputs. A failed download fails the build rather than changing data mode.

The solver ranges are a compatible specification, not a complete lock file. Record the tested versions and freeze a Git revision before the seminar.

## Launch

[Launch YL's notebook](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

For a final seminar invitation, replace `main` with the successfully tested commit SHA. JupyterLab opens the notebook directly through `urlpath=lab/tree/...`.

Default data are **real ACCESS-CM2 historical + SSP5-8.5**, cached in the image
under `data/access_cm2/`. Missing real inputs stop the notebook. Synthetic mode
requires the explicit setting `WORKSHOP_MODE=synthetic` and remains visibly
labeled as a software test. See the [updated demonstration guide](../docs/UPDATED_DEMO.md)
for input hashes, scientific definitions and the independent processing routes.

Binder sessions are temporary. Download changed notebooks and results before leaving.

Official configuration references: [repo2docker](https://repo2docker.readthedocs.io/en/stable/configuration/) and [Binder JupyterLab links](https://mybinder.readthedocs.io/en/latest/howto/user_interface.html).

## Keeping the Binder image compact

After the complete build and both real-data notebooks pass,
`scripts/compact_binder_outputs.py` reads `outputs/verification.json` to identify
only the two notebook runs verified in that build. It preserves their reports
and figures, and removes their generated NetCDF files. The executed notebook
copies are retained. Raw historical and SSP585 inputs remain cached.

For `outputs/updated_real_build`, all five final NetCDF products from each of
Python, CDO and NCO remain available; only the route `work/` directories are
removed. The corresponding `work/` directories in the explicitly named synthetic
build run, `outputs/updated_build`, are also removed. The cleanup does not scan
or remove historical output runs. It checks successful reports and path
boundaries, rejects symlink directories, and unlinks input-file symlinks without
following their targets. Its receipt is `outputs/binder_compaction.json`.

Interactive notebook execution creates a new output directory, so participants
can still inspect every newly generated intermediate during their own session.
