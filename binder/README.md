# Binder environment

The shared seminar environment uses conda-forge for Python, CDO, NCO and NCL 6.6.2. Keeping those compiled tools in one environment avoids relying on a particular Ubuntu APT package version.

## Build and checks

`environment.yml` installs the scientific tools and JupyterLab. `postBuild` installs this repository, generates the synthetic dataset, runs both workflows, checks four shared-example outputs, creates all three NCL figures and executes the seminar and hands-on notebooks.

A successful build writes `outputs/verification.json` containing tool/package versions, numerical comparisons and notebook execution status. PNG signature/dimension checks catch cases where NCL exits without writing a figure. Executed notebook copies are available in `outputs/executed/`.

The solver ranges are a compatible specification, not a complete lock file. Record the tested versions and freeze a Git revision before the seminar.

## Launch

[Launch YL's notebook](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

For a final seminar invitation, replace `main` with the successfully tested commit SHA. JupyterLab opens the notebook directly through `urlpath=lab/tree/...`.

Default data are synthetic and explicitly labelled. The actual full-grid ACCESS-CM2 file must be the same across languages for comparisons with the other presenters. See the [source mapping](../docs/EG_SHARED_NOTEBOOK_MAPPING.md).

Binder sessions are temporary. Download changed notebooks and results before leaving.

Official configuration references: [repo2docker](https://repo2docker.readthedocs.io/en/stable/configuration/) and [Binder JupyterLab links](https://mybinder.readthedocs.io/en/latest/howto/user_interface.html).
