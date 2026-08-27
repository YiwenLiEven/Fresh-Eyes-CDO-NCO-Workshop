#!/usr/bin/env python3
"""Plot climate stripes from a preprocessed one-dimensional NetCDF series."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, TwoSlopeNorm
import numpy as np
import xarray as xr


COLORS = [
    "#08306b", "#08519c", "#2171b5", "#4292c6",
    "#6baed6", "#9ecae1", "#c6dbef", "#deebf7",
    "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a",
    "#ef3b2c", "#cb181d", "#a50f15", "#67000d",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="outputs/demo/cdo/tas_global_annual_anomaly.nc")
    parser.add_argument("output", nargs="?", default="outputs/demo/climate_stripes.png")
    args = parser.parse_args()

    anomaly = xr.open_dataset(args.input, use_cftime=True)["tas_anom"].squeeze(drop=True)
    values = np.asarray(anomaly.values, dtype=float)
    limit = float(np.nanmax(np.abs(values)))
    stripe = np.vstack([values, values])

    fig, ax = plt.subplots(figsize=(12, 3.2), constrained_layout=True)
    ax.imshow(
        stripe,
        aspect="auto",
        cmap=ListedColormap(COLORS),
        norm=TwoSlopeNorm(vmin=-limit, vcenter=0.0, vmax=limit),
        interpolation="nearest",
    )
    ax.set_axis_off()
    ax.set_title("Global temperature stripes, 1850–2014\n1981–2010 baseline", pad=14)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180, bbox_inches="tight")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()

