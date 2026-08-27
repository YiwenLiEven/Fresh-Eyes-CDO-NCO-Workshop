"""Shared Python reference calculations for the workshop notebooks and tests."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import xarray as xr


def open_tas(path: str | Path) -> xr.DataArray:
    """Open a NetCDF file and return near-surface air temperature in Celsius."""
    tas = xr.open_dataset(path, use_cftime=True)["tas"]
    if tas.attrs.get("units") == "K":
        tas = tas - 273.15
        tas.attrs.update(units="degC", long_name="Near-Surface Air Temperature")
    return tas


def weighted_global_mean(tas: xr.DataArray) -> xr.DataArray:
    """Return a cosine-latitude weighted global mean."""
    weights = np.cos(np.deg2rad(tas["lat"]))
    return tas.weighted(weights).mean(("lat", "lon"))


def annual_global_anomaly(
    tas: xr.DataArray, baseline: tuple[int, int] = (1981, 2010)
) -> xr.DataArray:
    """Calculate global annual anomalies relative to an inclusive baseline."""
    annual = weighted_global_mean(tas).groupby("time.year").mean("time")
    reference = annual.sel(year=slice(*baseline)).mean("year")
    anomaly = annual - reference
    anomaly.name = "tas_anom"
    anomaly.attrs.update(
        units="degC",
        long_name="Global Annual Near-Surface Air Temperature Anomaly",
        anomaly_reference_period=f"{baseline[0]}-{baseline[1]}",
    )
    return anomaly


def maximum_temperature(tas: xr.DataArray) -> xr.DataArray:
    """Maximum temperature at each grid cell over the full record."""
    out = tas.max("time")
    out.name = "tas"
    out.attrs.update(units="degC", long_name="Maximum Near-Surface Air Temperature")
    return out


def seasonal_climatology(tas: xr.DataArray) -> xr.DataArray:
    """Multi-year DJF/MAM/JJA/SON climatology."""
    out = tas.groupby("time.season").mean("time").sel(season=["DJF", "MAM", "JJA", "SON"])
    out.name = "tas"
    out.attrs.update(units="degC", long_name="Seasonal Near-Surface Air Temperature Climatology")
    return out

