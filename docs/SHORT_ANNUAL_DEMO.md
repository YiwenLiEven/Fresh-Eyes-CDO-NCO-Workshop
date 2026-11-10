# Annual Arctic anomalies: short lesson

**[Open the short annual-stripes lesson in Binder](https://mybinder.org/v2/gh/YiwenLiEven/Fresh-Eyes-CDO-NCO-Workshop/main?urlpath=lab/tree/notebooks/05_annual_stripes_short_demo.ipynb)**
for the recommended 20-minute demonstration. The
[notebook file](../notebooks/05_annual_stripes_short_demo.ipynb) is also available for local use.
It contains **11 CDO and 9 NCO processing commands**, each immediately followed
by a result query. There are 45 executable cells including five collapsed
support cells. Every processing command is visible and executable directly.

This is an additional lesson. The existing full seminar and practice notebooks
retain their complete five-product calculations. Local verification has passed;
online CI and a live Binder check are pending for this release. The `main` link
selects the latest published source; older commit-pinned links retain their
previous versions.

## Scope and equivalence

The short route starts from both raw ACCESS-CM2 files. It selects 1979–2024,
converts temperature to Celsius, averages the 65–90°N grid points equally,
averages each complete year equally over its twelve months, and subtracts
the 1981–2010 mean annual temperature.

For complete years, fixed spatial weights and equal month weights:

`mean_months(temperature - monthly_reference)`
equals `mean_months(temperature) - mean_months(monthly_reference)`.

The second term equals the mean of the 30 annual temperatures in 1981–2010.
Thus the final annual anomalies agree with the complete monthly-anomaly route.
The existing input validation checks contiguous complete years and finite
temperature values. Do not assume this rearrangement applies unchanged to
missing months, changing spatial masks or month-length-weighted annual means.

This short lesson does **not** calculate the twelve monthly climatology maps,
monthly anomaly fields, or the duration-weighted anomaly map. Those remain
available in [the full practice notebook](../notebooks/04_monthly_anomaly_hands_on.ipynb).

## Presentation timing

These are target allocations, not measured rehearsal times.

| Topic | Target |
|---|---:|
| Data and annual-anomaly definition | 2 minutes |
| CDO calculation and result queries | 6 minutes |
| NCO calculation and result queries | 6 minutes |
| Compare annual series and stripes | 3 minutes |
| Questions and buffer | 3 minutes |

Explain each new operation, then point to the record count or a sample value
in its query output. The second date selection repeats the first pattern.
Use the final NCO metadata command to distinguish changing numbers from changing
their description; the numerical calculation is complete after subtraction.
Detailed questions about monthly reference fields can use the full notebook.

## Verified execution

The exact short notebook passed all **45/45 cells** with both real ACCESS-CM2
and the explicitly labelled synthetic fixture. All 20 queries produced output
and all captured stderr streams were empty. The real-data notebook took about
**12.35 seconds** to execute locally in this run; that is computation time,
not presentation time or a guarantee of Binder performance.

All 46 annual values agree with the full independent monthly-anomaly reference.
Maximum real-data differences: CDO **6.39488462e-14°C**;
NCO **2.61124455e-13°C**. Checks also cover the annual temperature series,
reference temperature, subtraction, baseline residual, year labels and output
metadata. The NCO annual output contains `tas` and `time` with no invalid links
to monthly bounds or omitted coordinates; its time labels identify years and
it does not claim interval bounds. CDO's full-year bounds are checked separately.

See [short_annual_verification_20261110.json](short_annual_verification_20261110.json)
for notebook hashes, exact checks and the distinction between local execution
and live Binder verification. The comparison figure was visually inspected.

Rebuild the additional notebook with:

```bash
python scripts/build_short_annual_notebook.py
```

The builder reuses the established input/reference support cells from the full
notebook, adds `ncdiff` to the plain-command registration, and leaves the full
notebooks unchanged. Run the Data cell to create a fresh output directory when
repeating the lesson.
