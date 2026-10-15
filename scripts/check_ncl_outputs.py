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

import numpy as np
from PIL import Image
rgb = np.asarray(Image.open(directory / "01_mean_anomaly_map.png").convert("RGB"))
map_region = rgb[int(.30*rgb.shape[0]):int(.60*rgb.shape[0]), int(.20*rgb.shape[1]):int(.80*rgb.shape[1])].astype(int)
assert (np.ptp(map_region, axis=2)>20).mean() > .20, "Map has insufficient contour fill"
rgb = np.asarray(Image.open(directory / "03_arctic_annual_stripes.png").convert("RGB"))
h,w=rgb.shape[:2]
xs=((.05+.90*(np.arange(36)+.5)/36)*w).astype(int)
rows=rgb[(np.array([.36,.46,.56,.64])*h).astype(int)][:,xs].astype(int)
assert np.max(np.ptp(rows,axis=0))<=3, "Stripes vary vertically"
assert np.ptp(rows[0],axis=0).max()>20, "Stripes have no color variation"
print("PASS: map contour coverage and vertical stripes rendering")
