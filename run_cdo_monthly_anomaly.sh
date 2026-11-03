#!/usr/bin/env bash
# CDO-only processing. No NCO executable or Python calculation is used.
set -euo pipefail
input=${1:-data/demo/tas_demo.nc}
out=${2:-outputs/demo/monthly/cdo}
mkdir -p "$out"
# Contract: monthly Kelvin tas(time,lat,lon), complete calendar years, regular grid.
cdo -L -b F64 -f nc4 setunit,degC -subc,273.15 -selname,tas "$input" "$out/tas_degC.nc"
cdo -L -b F64 ymonmean -selyear,1981/2010 "$out/tas_degC.nc" "$out/tas_monthly_climatology_1981_2010.nc"
cdo -L -b F64 chname,tas,tas_anom -seldate,1979-01-01,2014-12-31 -ymonsub \
  "$out/tas_degC.nc" "$out/tas_monthly_climatology_1981_2010.nc" "$out/tas_monthly_anomaly_1979_2014.nc"
cdo -L -b F64 timmean "$out/tas_monthly_anomaly_1979_2014.nc" "$out/tas_mean_monthly_anomaly_1979_2014.nc"
# Disable area weights explicitly to match EG's arithmetic grid-point mean.
cdo -L -b F64 fldmean,weights=false -sellonlatbox,0,360,65,90 \
  "$out/tas_monthly_anomaly_1979_2014.nc" "$out/tas_arctic_monthly_anomaly_1979_2014.nc"
cdo -L -b F64 yearmean "$out/tas_arctic_monthly_anomaly_1979_2014.nc" "$out/tas_arctic_annual_anomaly_1979_2014.nc"
echo "CDO-only processing complete: $out"
