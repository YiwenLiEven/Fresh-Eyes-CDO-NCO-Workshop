"""Fail a build if NCL exits without creating all required PNGs."""

import struct
import sys
from pathlib import Path

directory = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("outputs/demo/monthly")
for name in ("01_mean_anomaly_map", "02_arctic_monthly_anomaly", "03_arctic_annual_stripes"):
    path = directory / f"{name}.png"
    with path.open("rb") as stream:
        header = stream.read(24)
    assert header[:8] == b"\x89PNG\r\n\x1a\n", f"Invalid PNG: {path}"
    width, height = struct.unpack(">II", header[16:24])
    assert width >= 200 and height >= 200, f"Unexpected image dimensions: {path}"
    print(f"PASS: {name}.png ({width} x {height})")
