#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  cdo \
  nco \
  netcdf-bin \
  make

python -m pip install --upgrade pip
python -m pip install -e .
python scripts/generate_demo_data.py --output data/demo/tas_demo.nc
bash scripts/run_all.sh data/demo/tas_demo.nc outputs/demo
pytest -q

echo
echo "Workshop environment is ready."
echo "Open notebooks/00_opening_demo.ipynb to begin."
