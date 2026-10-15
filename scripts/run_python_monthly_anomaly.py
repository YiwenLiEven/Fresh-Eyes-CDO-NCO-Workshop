#!/usr/bin/env python3
"""Python/xarray reference for the shared 2026 monthly-anomaly example."""

from __future__ import annotations

import argparse
from pathlib import Path

import xarray as xr

from workshop import open_tas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="data/demo/tas_demo.nc")
    parser.add_argument("output_dir", nargs="?", default="outputs/demo/monthly/python")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tas = open_tas(args.input)
    reference = tas.sel(time=slice("1981-01-01", "2010-12-31"))
    if reference.sizes["time"] != 360:
        raise ValueError("The shared baseline requires all 360 months of 1981-2010")
    climatology = reference.groupby("time.month").mean("time")
    anomaly = tas.groupby("time.month") - climatology
    anomaly = anomaly.sel(time=slice("1979-01-01", "2014-12-31"))
    if anomaly.sizes["time"] != 432:
        raise ValueError("The shared analysis requires all 432 months of 1979-2014")
    anomaly.name = "tas_anom"
    anomaly.attrs.update(
        units="degC",
        long_name="Near-Surface Air Temperature Monthly Anomaly",
        anomaly_reference_period="1981-2010",
    )

    mean_field = anomaly.mean("time", keep_attrs=True)
    # Deliberately unweighted, following stripes_EG.ipynb exactly.
    arctic = anomaly.where((anomaly.lat >= 65) & (anomaly.lat <= 90), drop=True)
    arctic_monthly = arctic.mean(("lat", "lon"), keep_attrs=True)
    arctic_annual = arctic_monthly.groupby("time.year").mean("time", keep_attrs=True)

    encoding = {"tas_anom": {"zlib": True, "complevel": 3}}
    anomaly.to_dataset().to_netcdf(
        output_dir / "tas_monthly_anomaly_1979_2014.nc", encoding=encoding
    )
    mean_field.to_dataset().to_netcdf(
        output_dir / "tas_mean_monthly_anomaly_1979_2014.nc", encoding=encoding
    )
    climatology.rename("tas").to_dataset().to_netcdf(
        output_dir / "tas_monthly_climatology_1981_2010.nc",
        encoding={"tas": {"zlib": True, "complevel": 3}},
    )
    arctic_monthly.to_dataset().to_netcdf(
        output_dir / "tas_arctic_monthly_anomaly_1979_2014.nc", encoding=encoding
    )
    arctic_annual.to_dataset().to_netcdf(
        output_dir / "tas_arctic_annual_anomaly_1979_2014.nc", encoding=encoding
    )

    print(f"Python monthly-anomaly workflow complete: {output_dir}")


if __name__ == "__main__":
    main()
