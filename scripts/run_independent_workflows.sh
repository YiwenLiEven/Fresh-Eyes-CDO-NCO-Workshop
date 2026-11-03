#!/usr/bin/env bash
set -euo pipefail
input=${1:-data/demo/tas_demo.nc}
out=${2:-outputs/demo/monthly}
python scripts/check_monthly_input.py "$input"
python scripts/run_python_monthly_anomaly.py "$input" "$out/python"
bash scripts/run_cdo_monthly_anomaly.sh "$input" "$out/cdo"
bash scripts/run_nco_monthly_anomaly.sh "$input" "$out/nco"
python scripts/compare_three_workflows.py --root "$out"
