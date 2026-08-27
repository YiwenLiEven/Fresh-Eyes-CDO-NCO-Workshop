#!/usr/bin/env bash
set -euo pipefail

# The upstream devcontainer image may include a Yarn APT source whose signing
# key is periodically rotated. Yarn is unrelated to this workshop, so disable
# that optional source rather than allowing it to block the climate toolchain.
if [[ -f /etc/apt/sources.list.d/yarn.list ]]; then
  sudo mv /etc/apt/sources.list.d/yarn.list /etc/apt/sources.list.d/yarn.list.disabled
fi

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
