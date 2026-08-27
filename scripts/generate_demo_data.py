#!/usr/bin/env python3
"""Generate a compact deterministic CF-style temperature dataset for teaching."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr


def build_dataset() -> xr.Dataset:
    time = pd.date_range("1850-01-01", "2014-12-01", freq="MS") + pd.Timedelta(days=14)
    lat = np.arange(-87.5, 90.0, 5.0, dtype=np.float32)
    lon = np.arange(2.5, 360.0, 5.0, dtype=np.float32)

    year_fraction = (time.year.to_numpy() - 1850) + (time.month.to_numpy() - 0.5) / 12.0
    trend = 0.0065 * year_fraction
    multidecadal = 0.15 * np.sin(2.0 * np.pi * year_fraction / 55.0)
    seasonal = np.sin(2.0 * np.pi * (time.month.to_numpy() - 1) / 12.0)

    lat_r = np.deg2rad(lat)
    lon_r = np.deg2rad(lon)
    base = 288.0 - 42.0 * np.sin(lat_r) ** 2
    seasonal_pattern = 8.0 * np.sin(lat_r)
    spatial_pattern = 0.8 * np.cos(2.0 * lon_r)[None, :] * np.cos(lat_r)[:, None]

    tas = (
        base[None, :, None]
        + spatial_pattern[None, :, :]
        + seasonal[:, None, None] * seasonal_pattern[None, :, None]
        + trend[:, None, None]
        + multidecadal[:, None, None]
    ).astype(np.float32)

    ds = xr.Dataset(
        data_vars={"tas": (("time", "lat", "lon"), tas)},
        coords={"time": time, "lat": lat, "lon": lon},
        attrs={
            "title": "Deterministic CMIP-style teaching dataset",
            "summary": "Synthetic data for CDO/NCO/Python software comparison; not for scientific conclusions.",
            "Conventions": "CF-1.8",
            "source_id": "WORKSHOP-DEMO",
            "experiment_id": "historical-style",
            "variant_label": "r1i1p1f1",
            "table_id": "Amon",
        },
    )
    ds["tas"].attrs.update(
        standard_name="air_temperature",
        long_name="Near-Surface Air Temperature",
        units="K",
        cell_methods="area: time: mean",
    )
    ds["lat"].attrs.update(standard_name="latitude", units="degrees_north", axis="Y")
    ds["lon"].attrs.update(standard_name="longitude", units="degrees_east", axis="X")
    ds["time"].attrs.update(standard_name="time", axis="T")
    return ds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/demo/tas_demo.nc")
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    if output.exists():
        print(f"Dataset already exists: {output}")
        return

    ds = build_dataset()
    encoding = {"tas": {"zlib": True, "complevel": 3, "dtype": "float32"}}
    ds.to_netcdf(output, format="NETCDF4", encoding=encoding)
    print(f"Wrote {output} ({output.stat().st_size / 1_048_576:.1f} MiB)")


if __name__ == "__main__":
    main()

