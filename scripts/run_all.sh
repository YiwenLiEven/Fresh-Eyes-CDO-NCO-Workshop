#!/usr/bin/env bash
set -euo pipefail

input=${1:-data/demo/tas_demo.nc}
root=${2:-outputs/demo}

command -v cdo >/dev/null
command -v ncks >/dev/null
command -v ncl >/dev/null

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
STRIPES_INPUT="${root}/cdo/tas_global_annual_anomaly.nc" \
STRIPES_OUTPUT_BASE="${root}/climate_stripes_ncl" \
  ncl scripts/make_stripes.ncl > "${root}/ncl_stripes.log"

bash scripts/run_cdo_nco_monthly_anomaly.sh \
  "${input}" "${root}/monthly/cdo_nco"
python scripts/run_python_monthly_anomaly.py \
  "${input}" "${root}/monthly/python"
python scripts/validate_monthly_anomaly.py \
  --cdo-nco "${root}/monthly/cdo_nco" \
  --python "${root}/monthly/python" \
  --report "${root}/monthly_validation.json"

ncl "input_dir=\"${root}/monthly/cdo_nco\"" "output_dir=\"${root}/monthly\"" \
  scripts/make_eg_figures.ncl > "${root}/ncl_eg_figures.log"
python scripts/check_ncl_outputs.py "${root}/monthly"

echo "Complete workflow finished successfully."
