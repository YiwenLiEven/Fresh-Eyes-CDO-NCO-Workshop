#!/usr/bin/env python3
"""Optional numerical oracle using the real ESMValCore preprocessors.

Run this script in an environment with ESMValCore and Iris installed. These
large optional dependencies are deliberately absent from the Binder image.
The four main products share the CDO/NCO workshop's filenames and var_name.
This runs the preprocessors, not the full recipe/diagnostics command-line job.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("historical", help="Raw historical monthly tas in K")
    parser.add_argument("output_dir")
    parser.add_argument("--future", help="Raw SSP585 monthly tas in K")
    parser.add_argument("--start-year", type=int, default=1979)
    parser.add_argument("--end-year", type=int, default=2024)
    args = parser.parse_args()

    # Import after parsing so --help also works in the lightweight demo env.
    import esmvalcore
    import iris
    import numpy as np
    from esmvalcore.preprocessor import (
        anomalies,
        annual_statistics,
        climate_statistics,
        concatenate,
        convert_units,
        extract_region,
        extract_time,
        meridional_statistics,
        zonal_statistics,
    )

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    source_files = [args.historical] + ([args.future] if args.future else [])
    cubes = []
    first_year = min(args.start_year, 1981)
    last_year = max(args.end_year, 2010)
    for filename in source_files:
        cube = iris.load_cube(filename, iris.Constraint(cube_func=lambda c: c.var_name == "tas"))
        dates = cube.coord("time").units.num2date(cube.coord("time").points)
        selected = np.flatnonzero([(first_year <= d.year <= last_year) for d in dates])
        if not selected.size:
            continue
        cube = cube[int(selected[0]):int(selected[-1]) + 1]
        if cube.coord("time").bounds is None:
            raise ValueError("The ESMValCore oracle requires explicit CF time bounds")
        cubes.append(cube)
    if not cubes:
        raise ValueError("No input months fall within the requested periods")
    cube = concatenate(cubes)
    dates = cube.coord("time").units.num2date(cube.coord("time").points)
    month_ids = np.array([12 * d.year + d.month - 1 for d in dates])
    np.testing.assert_array_equal(month_ids, np.arange(12 * first_year, 12 * (last_year + 1)))
    # Preserve source precision: this is the actual ESMValCore computation,
    # including its float32 reductions, rather than a reimplementation.
    cube = convert_units(cube, "degC")
    reference = dict(start_year=1981, start_month=1, start_day=1,
                     end_year=2011, end_month=1, end_day=1)
    baseline = extract_time(cube.copy(), **reference)
    climatology = climate_statistics(baseline, operator="mean", period="month")
    anomaly = anomalies(cube, period="month", reference=reference)
    anomaly = extract_time(anomaly, args.start_year, 1, 1, args.end_year + 1, 1, 1)
    anomaly.var_name = "tas_anom"
    anomaly.long_name = "Near-Surface Air Temperature Monthly Anomaly"
    anomaly.attributes["anomaly_reference_period"] = "1981-2010"
    mean_map = climate_statistics(anomaly.copy(), operator="mean", period="full")
    arctic = extract_region(anomaly.copy(), 0.0, 360.0, 65.0, 90.0)
    arctic_monthly = meridional_statistics(zonal_statistics(arctic, "mean"), "mean")
    arctic_annual = annual_statistics(arctic_monthly.copy(), operator="mean")

    suffix = f"{args.start_year}_{args.end_year}.nc"
    products = {
        "tas_monthly_anomaly_" + suffix: anomaly,
        "tas_mean_monthly_anomaly_" + suffix: mean_map,
        "tas_arctic_monthly_anomaly_" + suffix: arctic_monthly,
        "tas_arctic_annual_anomaly_" + suffix: arctic_annual,
        "tas_monthly_climatology_1981_2010.nc": climatology,
    }
    for filename, product in products.items():
        iris.save(product, str(output / filename), zlib=True, complevel=3)
    report = {
        "esmvalcore_version": esmvalcore.__version__,
        "iris_version": iris.__version__,
        "source_files": [Path(f).name for f in source_files],
        "analysis_period": [args.start_year, args.end_year],
        "reference_period": [1981, 2010],
        "monthly_samples": int(anomaly.shape[0]),
        "annual_samples": int(arctic_annual.shape[0]),
        "monthly_climatology_weighting": "equal samples within calendar month",
        "mean_map_weighting": "CF time bound interval lengths",
        "arctic_weighting": "unweighted zonal then meridional mean; latitude centres 65-90 N",
        "annual_weighting": "equal monthly samples",
        "scope": "actual ESMValCore preprocessors; full recipe and diagnostics not invoked",
        "products": list(products),
    }
    (output / "esmvalcore_reference_provenance.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
