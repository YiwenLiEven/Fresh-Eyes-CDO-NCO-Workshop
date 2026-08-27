#!/usr/bin/env python3
"""Numerically compare the CDO and Python workshop outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import xarray as xr


def max_abs(a: xr.DataArray, b: xr.DataArray) -> float:
    left, right = xr.align(a.squeeze(drop=True), b.squeeze(drop=True), join="override")
    return float(np.nanmax(np.abs(left.values - right.values)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdo", default="outputs/demo/cdo")
    parser.add_argument("--python", default="outputs/demo/python")
    parser.add_argument("--report", default="outputs/demo/validation.json")
    args = parser.parse_args()

    cdo_dir = Path(args.cdo)
    py_dir = Path(args.python)
    comparisons = {
        "maximum_temperature_degC": (
            cdo_dir / "tas_max_degC.nc",
            py_dir / "tas_max_degC.nc",
            "tas",
            2.0e-4,
        ),
        "seasonal_climatology_degC": (
            cdo_dir / "tas_seasonal_climatology_degC.nc",
            py_dir / "tas_seasonal_climatology_degC.nc",
            "tas",
            2.0e-4,
        ),
        "global_annual_anomaly_degC": (
            cdo_dir / "tas_global_annual_anomaly.nc",
            py_dir / "tas_global_annual_anomaly.nc",
            "tas_anom",
            2.0e-4,
        ),
    }

    report: dict[str, dict[str, float | bool]] = {}
    for name, (cdo_file, py_file, variable, tolerance) in comparisons.items():
        cdo_data = xr.open_dataset(cdo_file, use_cftime=True)[variable]
        py_data = xr.open_dataset(py_file, use_cftime=True)[variable]
        difference = max_abs(cdo_data, py_data)
        report[name] = {
            "max_absolute_difference": difference,
            "tolerance": tolerance,
            "passed": difference <= tolerance,
        }

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

    failed = [name for name, result in report.items() if not result["passed"]]
    if failed:
        raise SystemExit(f"Scientific equivalence failed: {', '.join(failed)}")
    print("All CDO and Python results agree within tolerance.")


if __name__ == "__main__":
    main()

