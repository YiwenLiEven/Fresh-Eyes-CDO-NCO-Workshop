# Fresh Eyes: Python vs CDO-only vs NCO-only

[Launch the seminar in Binder](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/ea6af63d118797569d8068baab669281aaa2d137?urlpath=lab/tree/notebooks/00_yl_20_minute_binder_demo.ipynb)

[Open the participant hands-on notebook](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/ea6af63d118797569d8068baab669281aaa2d137?urlpath=lab/tree/notebooks/04_monthly_anomaly_hands_on.ipynb) · [Download the presentation](slides/CDO_NCO_Hands_On_Comparison_YL_2026_Final.pptx)

**Verified on 3 November 2026:** the pinned revision `ea6af63` built successfully on public Binder, opened JupyterLab, and passed all eight CDO/Python and NCO/Python comparisons. Both seminar notebooks executed without errors; both tests passed during the build. The largest numerical difference was 8.14e-06 degC (tolerance 0.0003 degC). See [Binder verification](docs/binder_launch_verification.json) and [the successful GitHub Actions run](https://github.com/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/actions/runs/41609810743). The launch links above use that tested commit.

## Current seminar workflow

Three independent implementations start from the same raw Kelvin NetCDF:

| Route | Complete processing implementation | Final visualization |
|---|---|---|
| Python reference | xarray | Python/matplotlib |
| CDO-only | CDO, no NCO commands | Python/matplotlib |
| NCO-only | NCO, no CDO commands | Python/matplotlib |

All routes reproduce EG's monthly climatology (1981-2010), monthly anomalies (1979-2014), mean anomaly map, arithmetic Arctic mean (65-90N), and equal-month annual stripes. Each has its own output directory. Python validates eight comparisons: four CDO products against Python, and four NCO products against Python. CDO explicitly uses fldmean,weights=false. Bare fldmean and fldavg use area weights and would change the shared definition.

### Start

Open notebooks/00_yl_20_minute_binder_demo.ipynb and run all cells. For practice open notebooks/04_monthly_anomaly_hands_on.ipynb.

The default input is deterministic **synthetic** teaching data, not ACCESS-CM2 output. Supply WORKSHOP_INPUT to use a real shared file that satisfies the documented input contract. Scripts require complete monthly Kelvin tas(time,lat,lon), a regular 0-360 longitude grid, no missing values, all of 1979-2014, and all of 1981-2010. The read-only input checker rejects unsupported inputs instead of silently treating them as equivalent.

Run locally in the prepared Linux environment:

    python -m pip install -e .
    python scripts/generate_demo_data.py
    bash scripts/run_independent_workflows.sh

Outputs: outputs/demo/monthly/{python,cdo,nco}, three_way_validation.json and three_way_comparison.png.

Numerical agreement means absolute error <= 0.0003 degC (rtol=0), exact calendar/spatial alignment and matching masks. It does not mean byte-identical NetCDF files. Metadata and mid-month timestamps may differ while calendar-month labels agree.

### Legacy material

The previous combined CDO/NCO script, global annual examples, NCL figures and notebooks 00_opening_demo through 03_hands_on_exercises remain historical/optional examples. They are not the current three-route seminar. The old executed notebooks and verification report describe the old revision, not evidence for the new one. Use the pinned revision and current Binder verification linked above for the independent-workflow seminar.

### Attribution

Original Python workshop: [abhnil/Fresh_Eyes_on_CMIP_Data_Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop).
Shared compressed reference: [egalytska/Fresh_eyes, stripes_EG.ipynb](https://github.com/egalytska/Fresh_eyes/blob/393cfcf876fa47c6c231c3be70dbd9f8552fe3a3/stripes_EG.ipynb).
The independent command-line implementations, input contract, equivalence checks and shared Python comparison figure are workshop extensions. Original source audits remain in docs/ORIGINAL_WORKSHOP_MAPPING.md and docs/EG_SHARED_NOTEBOOK_MAPPING.md; their old combined-route descriptions are historical.
