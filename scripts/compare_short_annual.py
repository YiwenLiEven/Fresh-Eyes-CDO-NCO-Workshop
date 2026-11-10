"""Compare three annual-anomaly files produced earlier in the lesson.

The curves and stripes read only the three files in PLOT_INPUTS below.
The other files check the annual temperatures and reference-period mean.
This script does not calculate or supply CDO/NCO processing intermediates.
"""
from pathlib import Path
import argparse
import json
import os

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".cache/matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


# Each row names one column in the comparison figure:
# (figure label, file relative to the current results folder, variable).
PLOT_INPUTS = (
    ("Python reference", "python/arctic_annual.nc", "tas_anom"),
    ("CDO", "cdo/annual_anomaly.nc", "tas"),
    ("NCO", "nco/annual_anomaly.nc", "tas"),
)


def annual_series(path, variable):
    with xr.open_dataset(path) as ds:
        series = ds[variable].squeeze(drop=True).load()
        if "time" in series.dims:
            years = series.time.dt.year.values
        else:
            years = series.year.values
        assert series.ndim == 1 and series.size == 46
        np.testing.assert_array_equal(years, np.arange(1979, 2025))
        assert np.isfinite(series.values).all()
        assert series.attrs["units"] == "degC"
        return np.asarray(series.values, dtype=float)


def compare(run):
    run = Path(run)
    tolerance = 3e-4
    info = json.loads((run / "python/input_contract.json").read_text())
    assert info["months"] == 552 and info["years"] == 46
    print("Files used for the curves and climate stripes:")
    for label, filename, variable in PLOT_INPUTS:
        print(f"  {label}: {filename} -> {variable}")
    print("  1979-2024: 46 annual Arctic anomalies (degC); reference 1981-2010.")
    print("  Arctic 65-90 N; equal grid-point and monthly weights.")
    print("Python reference: independent calculation, not saved ESMValTool output.")
    print("Additional checks: python/climatology.nc, cdo/annual_temperature.nc,")
    print("  nco/annual_temperature.nc, cdo/reference.nc, nco/reference.nc.")
    print("Data coverage: python/input_contract.json.\n")
    arrays = {
        label: annual_series(run / filename, variable)
        for label, filename, variable in PLOT_INPUTS
    }
    reference = arrays["Python reference"]
    with xr.open_dataset(run / "python/climatology.nc") as ds:
        baseline = float(ds.tas.sel(lat=slice(65, 90)).mean())
    report = {
        "scope": "Annual Arctic anomalies only; no claim of monthly-field/map equivalence from this short route",
        "input": info,
        "absolute_tolerance_degC": tolerance,
        "reference_method": "Full monthly-climatology and monthly-anomaly calculation",
        "plot_inputs": [
            {"label": label, "file": filename, "variable": variable}
            for label, filename, variable in PLOT_INPUTS
        ],
        "additional_check_inputs": [
            "python/climatology.nc", "cdo/annual_temperature.nc",
            "nco/annual_temperature.nc", "cdo/reference.nc", "nco/reference.nc",
        ],
        "conditions": {
            "complete_months_and_finite_grid": True,
            "equal_month_annual_weights": True,
            "equal_grid_weights_65_to_90N": True,
            "baseline": "1981-2010",
        },
        "comparisons": {},
    }
    for route in ("cdo", "nco"):
        values = arrays[route.upper()]
        temperatures = annual_series(run / route / "annual_temperature.nc", "tas")
        with xr.open_dataset(run / route / "reference.nc") as ds:
            actual_baseline = float(ds.tas.squeeze())
        np.testing.assert_allclose(values, reference, atol=tolerance, rtol=0)
        np.testing.assert_allclose(actual_baseline, baseline, atol=tolerance, rtol=0)
        np.testing.assert_allclose(temperatures, reference + baseline, atol=tolerance, rtol=0)
        np.testing.assert_allclose(values, temperatures - actual_baseline, atol=tolerance, rtol=0)
        residual = float(abs(values[2:32].mean()))
        assert residual < tolerance
        error = float(abs(values - reference).max())
        report["comparisons"][route] = {
            "years": 46, "passed": True,
            "max_absolute_difference_degC": error,
            "baseline_difference_degC": abs(actual_baseline - baseline),
            "baseline_anomaly_residual_degC": residual,
            "annual_temperature_and_subtraction_checked": True,
        }
        print(f"PASS {route}: 46 annual anomalies; maximum difference = {error:.9g} °C")
    with xr.open_dataset(run / "nco/annual_anomaly.nc") as ds:
        assert set(ds.variables) == {"tas", "time"}
        assert "bounds" not in ds.time.attrs
        assert "coordinates" not in ds.tas.attrs
        assert "coordinates" not in ds.tas.encoding
        assert "cell_measures" not in ds.tas.attrs
        assert ds.tas.attrs["standard_name"] == "air_temperature_anomaly"
    report["nco_output_metadata"] = "Year-labelled tas/time series; no interval-bound or unavailable-coordinate links"
    with xr.open_dataset(run / "cdo/annual_anomaly.nc",
                         decode_times=xr.coders.CFDatetimeCoder(use_cftime=True)) as ds:
        bounds_name = ds.time.attrs.get("bounds")
        assert bounds_name in ds
        for year, (lo, hi) in zip(range(1979, 2025), ds[bounds_name].values):
            assert (lo.year, lo.month, lo.day) == (year, 1, 1)
            assert (hi.year, hi.month, hi.day) == (year + 1, 1, 1)
    report["cdo_annual_bounds_full_year"] = True
    report["passed"] = True
    (run / "short_validation.json").write_text(json.dumps(report, indent=2) + "\n")
    years = np.arange(1979, 2025)
    limit = max(float(abs(a).max()) for a in arrays.values())
    fig, axes = plt.subplots(2, 3, figsize=(13, 5.3), layout="constrained",
                             gridspec_kw={"height_ratios": [2.4, 1]})
    for column, (label, filename, variable) in enumerate(PLOT_INPUTS):
        values = arrays[label]
        ax = axes[0, column]
        ax.plot(years, values, color="#235c7c", lw=1.6)
        ax.axhline(0, color="0.5", lw=.7)
        ax.set_title(f"{label}\n{filename} · {variable}", fontsize=10)
        ax.set(xlabel="Year", ylabel="Annual anomaly (°C)",
               xlim=(1978.5, 2024.5), ylim=(-limit * 1.12, limit * 1.12))
        stripe = axes[1, column].imshow(values[None, :], extent=[1978.5, 2024.5, 0, 1],
                    aspect="auto", cmap="bwr", vmin=-limit, vmax=limit)
        axes[1, column].set(xlabel="Year", yticks=[])
    fig.colorbar(stripe, ax=axes[1, :], label="Annual anomaly (°C)", shrink=.8)
    label = "SYNTHETIC SOFTWARE TEST" if info["synthetic"] else "ACCESS-CM2 historical + SSP5-8.5"
    fig.suptitle(f"{label}\nArctic 65–90°N · equal grid/month weights · reference 1981–2010")
    fig.savefig(run / "short_comparison.png", dpi=150)
    plt.close(fig)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("run")
    compare(parser.parse_args().run)
