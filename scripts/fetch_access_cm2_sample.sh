#!/usr/bin/env bash
set -euo pipefail

url='https://dapds00.nci.org.au/thredds/dodsC/fs38/publications/CMIP6/CMIP/CSIRO-ARCCSS/ACCESS-CM2/historical/r1i1p1f1/Amon/tas/gn/v20191108/tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc'
output='data/raw/tas_ACCESS-CM2_teaching_sample.nc'
mkdir -p data/raw

if [[ -s "${output}" ]]; then
  echo "Real-data sample already exists: ${output}"
  exit 0
fi

echo "Retrieving a spatially strided sample of the original ACCESS-CM2 dataset..."
echo "All 1,980 monthly time steps are retained."
ncks -O -4 -L 3 -v tas -d lat,0,143,4 -d lon,0,191,3 "${url}" "${output}"

echo "Validating the downloaded sample..."
test "$(cdo -s ntime "${output}")" -eq 1980
ncks -m -v tas "${output}" | head -n 30
ls -lh "${output}"

