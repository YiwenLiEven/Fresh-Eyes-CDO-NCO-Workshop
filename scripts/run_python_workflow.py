#!/usr/bin/env python3
"""Run the xarray reference workflow and write comparable NetCDF outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import xarray as xr

from workshop import annual_global_anomaly, maximum_temperature, open_tas, seasonal_climatology


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("outdir")
    args = parser.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    tas = open_tas(args.input)
    maximum_temperature(tas).to_netcdf(outdir / "tas_max_degC.nc")
    seasonal_climatology(tas).to_netcdf(outdir / "tas_seasonal_climatology_degC.nc")

    anomaly = annual_global_anomaly(tas)
    dates = xr.DataArray(
        [f"{int(year)}-07-01" for year in anomaly.year.values], dims="time"
    ).astype("datetime64[ns]")
    anomaly = anomaly.rename(year="time").assign_coords(time=dates)
    anomaly.to_netcdf(outdir / "tas_global_annual_anomaly.nc")
    print(f"Python outputs written to {outdir}")


if __name__ == "__main__":
    main()

