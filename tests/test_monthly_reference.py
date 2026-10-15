"""Independent scientific checks of the shared example's Python reference."""

import subprocess
import sys

import numpy as np
import xarray as xr

from scripts.generate_demo_data import build_dataset


def test_monthly_reference_matches_calendar_and_arctic_definition(tmp_path):
    data = build_dataset()
    input_file = tmp_path / "input.nc"
    data.to_netcdf(input_file)
    output_dir = tmp_path / "reference"
    subprocess.run(
        [sys.executable, "scripts/run_python_monthly_anomaly.py", str(input_file), str(output_dir)],
        check=True,
    )
    with xr.open_dataset(output_dir / "tas_monthly_anomaly_1979_2014.nc") as ds:
        anomaly = ds.tas_anom.load()
    assert anomaly.sizes["time"] == 432
    np.testing.assert_array_equal(np.unique(anomaly.time.dt.year), np.arange(1979, 2015))
    baseline = anomaly.sel(time=slice("1981", "2010"))
    residual = baseline.groupby("time.month").mean("time")
    assert float(abs(residual).max()) < 3e-4

    # Independently subtract the baseline January mean at one grid point.
    raw = data.tas.sel(time=slice("1979", "2014"))
    raw_january = data.tas.sel(time=slice("1981", "2010")).isel(time=slice(0, None, 12))
    np.testing.assert_allclose(
        anomaly.isel(time=0, lat=0, lon=0),
        raw.isel(time=0, lat=0, lon=0) - raw_january.isel(lat=0, lon=0).mean("time"),
        atol=3e-4,
    )
    arctic_field = anomaly.where(anomaly.lat >= 65, drop=True)
    arithmetic = arctic_field.values.mean(axis=(1, 2))
    with xr.open_dataset(output_dir / "tas_arctic_monthly_anomaly_1979_2014.nc") as ds:
        np.testing.assert_allclose(ds.tas_anom, arithmetic, atol=1e-6)
    with xr.open_dataset(output_dir / "tas_arctic_annual_anomaly_1979_2014.nc") as ds:
        assert ds.tas_anom.size == 36
        np.testing.assert_allclose(ds.tas_anom, arithmetic.reshape(36, 12).mean(axis=1), atol=1e-6)
    weighted = arctic_field.weighted(np.cos(np.deg2rad(arctic_field.lat))).mean(("lat", "lon"))
    assert float(abs(weighted-arithmetic).max()) > 1e-4, "Fixture must distinguish averaging definitions"
