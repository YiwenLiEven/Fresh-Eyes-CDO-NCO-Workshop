#!/usr/bin/env bash
set -euo pipefail

input=${1:-data/demo/tas_demo.nc}
root=${2:-outputs/demo}

command -v cdo >/dev/null
command -v ncks >/dev/null

bash scripts/run_cdo_workflow.sh "${input}" "${root}/cdo"
bash scripts/run_nco_workflow.sh "${input}" "${root}/nco"
python scripts/run_python_workflow.py "${input}" "${root}/python"
python scripts/validate_results.py \
  --cdo "${root}/cdo" \
  --python "${root}/python" \
  --report "${root}/validation.json"
python scripts/make_stripes.py \
  "${root}/cdo/tas_global_annual_anomaly.nc" \
  "${root}/climate_stripes.png"

echo "Complete workflow finished successfully."

