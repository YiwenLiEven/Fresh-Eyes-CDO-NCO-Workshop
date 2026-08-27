from __future__ import annotations

import json
from pathlib import Path
import subprocess


def test_all_workshop_comparisons_pass() -> None:
    data = Path("data/demo/tas_demo.nc")
    if not data.exists():
        subprocess.run(
            ["python", "scripts/generate_demo_data.py", "--output", str(data)],
            check=True,
        )
    subprocess.run(["bash", "scripts/run_all.sh", str(data), "outputs/test"], check=True)
    report = json.loads(Path("outputs/test/validation.json").read_text())
    assert report
    assert all(result["passed"] for result in report.values())

