#!/usr/bin/env bash
set -euo pipefail

input=${1:-data/demo/tas_demo.nc}
outdir=${2:-outputs/demo/cdo}
mkdir -p "${outdir}"

echo "Running the CDO reproduction on ${input}"

cdo -L -f nc4c -z zip_4 -timmax -subc,273.15 \
  "${input}" "${outdir}/tas_max_degC.nc"

cdo -L -f nc4c -z zip_4 -yseasmean -subc,273.15 \
  "${input}" "${outdir}/tas_seasonal_climatology_degC.nc"

cdo -L -f nc4c -z zip_4 -yearmean -fldmean -subc,273.15 \
  "${input}" "${outdir}/tas_global_annual_mean_degC.nc"

baseline=$(cdo -s output -timmean -selyear,1981/2010 \
  "${outdir}/tas_global_annual_mean_degC.nc" | xargs)

cdo -L -f nc4c -z zip_4 subc,"${baseline}" \
  "${outdir}/tas_global_annual_mean_degC.nc" \
  "${outdir}/tas_global_annual_anomaly.nc"

ncrename -O -v tas,tas_anom "${outdir}/tas_global_annual_anomaly.nc"
ncatted -O \
  -a units,tas_anom,o,c,'degC' \
  -a long_name,tas_anom,o,c,'Global Annual Near-Surface Air Temperature Anomaly' \
  -a anomaly_reference_period,tas_anom,o,c,'1981-2010' \
  "${outdir}/tas_global_annual_anomaly.nc"

echo "CDO baseline: ${baseline} degC"
echo "CDO outputs written to ${outdir}"

