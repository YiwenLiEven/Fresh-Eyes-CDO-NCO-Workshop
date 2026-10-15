"""Record tested versions and validation evidence in the built environment."""

import importlib.metadata
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

report = {
    "completed_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "packages": {p: importlib.metadata.version(p) for p in ("xarray", "numpy", "netCDF4", "nbconvert")},
    "tools": {},
    "shared_reference_commit": "393cfcf876fa47c6c231c3be70dbd9f8552fe3a3",
}
for tool, args in {"cdo": ["-V"], "ncks": ["--version"], "ncl": ["-V"]}.items():
    result = subprocess.run([tool, *args], check=True, text=True, capture_output=True)
    report["tools"][tool] = (result.stdout + result.stderr).strip()
report["monthly_validation"] = json.loads(Path("outputs/demo/monthly_validation.json").read_text())
for name in ("00_yl_20_minute_binder_demo", "04_monthly_anomaly_hands_on"):
    notebook = json.loads(Path(f"outputs/executed/{name}.ipynb").read_text())
    assert not any(out.get("output_type") == "error" for cell in notebook["cells"] for out in cell.get("outputs", []))
report["notebooks_executed"] = True
Path("outputs/verification.json").write_text(json.dumps(report, indent=2) + "\n")
print("PASS: outputs/verification.json records completed scientific and notebook checks.")
