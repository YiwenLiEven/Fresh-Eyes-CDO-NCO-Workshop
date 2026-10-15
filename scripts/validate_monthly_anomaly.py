#!/usr/bin/env python3
"""Validate the CDO/NCO reproduction of the shared monthly-anomaly example."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import xarray as xr


def read_values(path: Path) -> np.ndarray:
    with xr.open_dataset(path, decode_times=False) as dataset:
        return np.asarray(dataset["tas_anom"].squeeze(drop=True).values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdo-nco", default="outputs/demo/monthly/cdo_nco")
    parser.add_argument("--python", default="outputs/demo/monthly/python")
    parser.add_argument("--report", default="outputs/demo/monthly_validation.json")
    args = parser.parse_args()

    comparisons = {
        "monthly_anomaly_1979_2014": "tas_monthly_anomaly_1979_2014.nc",
        "mean_monthly_anomaly_map_1979_2014": "tas_mean_monthly_anomaly_1979_2014.nc",
        "arctic_monthly_unweighted_1979_2014": "tas_arctic_monthly_anomaly_1979_2014.nc",
        "arctic_annual_unweighted_1979_2014": "tas_arctic_annual_anomaly_1979_2014.nc",
    }
    tolerance = 3.0e-4
    report: dict[str, dict[str, float | bool]] = {}

    for name, filename in comparisons.items():
        left = read_values(Path(args.cdo_nco) / filename)
        right = read_values(Path(args.python) / filename)
        if left.shape != right.shape:
            raise SystemExit(f"Shape mismatch for {name}: {left.shape} != {right.shape}")
        if not np.array_equal(np.isfinite(left), np.isfinite(right)):
            raise SystemExit(f"Missing-value mask mismatch for {name}")
        if not np.isfinite(left).any():
            raise SystemExit(f"No finite values for {name}")
        difference = float(np.nanmax(np.abs(left - right)))
        report[name] = {
            "max_absolute_difference": difference,
            "tolerance": tolerance,
            "passed": difference <= tolerance,
        }

    # Check scientific semantics independently of positional array comparison.
    for directory in (Path(args.cdo_nco), Path(args.python)):
        with xr.open_dataset(directory / "tas_monthly_anomaly_1979_2014.nc") as ds:
            assert ds.sizes["time"] == 432, "Expected 36 complete years (432 months)"
            assert int(ds.time.dt.year.min()) == 1979
            assert int(ds.time.dt.year.max()) == 2014
            residual = ds.tas_anom.sel(time=slice("1981", "2010")).groupby("time.month").mean("time")
            assert float(abs(residual).max()) < tolerance, "Monthly baseline must average to zero"
        with xr.open_dataset(directory / "tas_arctic_annual_anomaly_1979_2014.nc", decode_times=False) as ds:
            assert ds.tas_anom.squeeze().size == 36, "Expected one stripe per year"

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

    failed = [name for name, result in report.items() if not result["passed"]]
    if failed:
        raise SystemExit("Monthly-anomaly equivalence failed: " + ", ".join(failed))
    print("All shared-example results agree within tolerance.")


if __name__ == "__main__":
    main()
