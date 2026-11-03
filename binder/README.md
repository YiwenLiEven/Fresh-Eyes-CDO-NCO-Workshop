# Binder environment

The current seminar environment uses conda-forge for Python, CDO and NCO. NCL is optional legacy material and is not required by the current notebooks. NCO must be version 5.1.9 or later for the grouped annual-average operation.

## Build and checks

`environment.yml` installs the scientific tools and JupyterLab. `postBuild` installs this repository, generates the synthetic dataset, runs Python, CDO-only and NCO-only workflows, checks eight independent comparisons, creates the common Python comparison figure, and executes both seminar and hands-on notebooks.

A successful build writes `outputs/verification.json` containing tool/package versions, eight numerical comparisons and notebook execution status. Executed copies are in `outputs/executed/`. The result figure is `outputs/demo/monthly/three_way_comparison.png` and the detailed checks are in `outputs/demo/monthly/three_way_validation.json`.

The solver ranges are a compatible specification, not a complete lock file. Record the tested versions and freeze a Git revision before the seminar.

## Launch

[Launch YL's notebook](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

For a final seminar invitation, replace `main` with the successfully tested commit SHA. JupyterLab opens the notebook directly through `urlpath=lab/tree/...`.

Default data are synthetic and explicitly labelled. The actual full-grid ACCESS-CM2 file must be the same across languages for comparisons with the other presenters. See the [source mapping](../docs/EG_SHARED_NOTEBOOK_MAPPING.md).

Binder sessions are temporary. Download changed notebooks and results before leaving.

Official configuration references: [repo2docker](https://repo2docker.readthedocs.io/en/stable/configuration/) and [Binder JupyterLab links](https://mybinder.readthedocs.io/en/latest/howto/user_interface.html).
