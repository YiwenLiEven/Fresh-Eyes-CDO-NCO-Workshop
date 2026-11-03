#!/usr/bin/env bash
set -euo pipefail

input=${1:-data/demo/tas_demo.nc}
root=${2:-outputs/demo}

command -v cdo >/dev/null
command -v ncks >/dev/null
command -v ncap2 >/dev/null

# Current seminar: three independent monthly workflows and Python graphics.
bash scripts/run_independent_workflows.sh "${input}" "${root}/monthly"
echo "Three independent workflows finished successfully."
