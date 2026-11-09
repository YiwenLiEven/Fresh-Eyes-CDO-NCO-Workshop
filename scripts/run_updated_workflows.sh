#!/usr/bin/env bash
# Usage: bash scripts/run_updated_workflows.sh HIST FUTURE OUTPUT [END_YEAR]
set -euo pipefail
hist=${1:?historical input required}; future=${2:?ssp585 input required}; out=${3:?output required}; end=${4:-2024}
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-1}
python "$script_dir/check_updated_inputs.py" "$hist" "$future" --end-year "$end"
python "$script_dir/run_python_updated.py" "$hist" "$future" "$out/python" --end-year "$end"
bash "$script_dir/run_cdo_updated.sh" "$hist" "$future" "$out/cdo" "$end"
bash "$script_dir/run_nco_updated.sh" "$hist" "$future" "$out/nco" "$end"
python "$script_dir/compare_updated_workflows.py" "$out"
