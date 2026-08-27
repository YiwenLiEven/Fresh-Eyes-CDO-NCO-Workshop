#!/usr/bin/env bash
set -euo pipefail

input=${1:-data/demo/tas_demo.nc}
outdir=${2:-outputs/demo/nco}
mkdir -p "${outdir}"

echo "Demonstrating NCO selection and metadata operations on ${input}"

ncks -O -4 -L 4 -v tas -d time,1572,1931 \
  "${input}" "${outdir}/tas_1981_2010.nc"

ncatted -O \
  -a workshop_operation,global,o,c,'NCO variable and temporal selection' \
  -a workshop_period,global,o,c,'1981-2010' \
  "${outdir}/tas_1981_2010.nc"

test "$(cdo -s ntime "${outdir}/tas_1981_2010.nc")" -eq 360
echo "NCO selected tas and 360 monthly time steps."
ncks -m -v tas "${outdir}/tas_1981_2010.nc" | head -n 25

