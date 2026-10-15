#!/usr/bin/env bash
set -euo pipefail

input=${1:-data/demo/tas_demo.nc}
output_dir=${2:-outputs/demo/monthly/cdo_nco}

mkdir -p "${output_dir}"

# NCO keeps only the shared seminar variable before CDO starts processing.
ncks -O -v tas "${input}" "${output_dir}/tas_selected.nc"

# Exact reproduction of the shared Python example:
# Kelvin -> Celsius; 1981-2010 monthly climatology; monthly anomalies;
# then retain 1979-2014.
cdo -L -f nc4c -z zip_4 subc,273.15 \
  "${output_dir}/tas_selected.nc" \
  "${output_dir}/tas_degC.nc"

cdo -L -f nc4c -z zip_4 ymonmean \
  -selyear,1981/2010 \
  "${output_dir}/tas_degC.nc" \
  "${output_dir}/tas_monthly_climatology_1981_2010.nc"

cdo -L -f nc4c -z zip_4 ymonsub \
  "${output_dir}/tas_degC.nc" \
  "${output_dir}/tas_monthly_climatology_1981_2010.nc" \
  "${output_dir}/tas_monthly_anomaly_full.nc"

cdo -L -f nc4c -z zip_4 seldate,1979-01-01,2014-12-31 \
  "${output_dir}/tas_monthly_anomaly_full.nc" \
  "${output_dir}/tas_monthly_anomaly_1979_2014.nc"

cdo -L -f nc4c -z zip_4 timmean \
  "${output_dir}/tas_monthly_anomaly_1979_2014.nc" \
  "${output_dir}/tas_mean_monthly_anomaly_1979_2014.nc"

# Match EG's arithmetic grid-point mean exactly. CDO fldmean would instead
# apply cell-area weights and would change the definition of this example.
ncks -O -d lat,65.0,90.0 \
  "${output_dir}/tas_monthly_anomaly_1979_2014.nc" \
  "${output_dir}/tas_arctic_field_1979_2014.nc"
ncwa -O -a lat,lon \
  "${output_dir}/tas_arctic_field_1979_2014.nc" \
  "${output_dir}/tas_arctic_monthly_anomaly_1979_2014.nc"
cdo -L -f nc4c -z zip_4 yearmean \
  "${output_dir}/tas_arctic_monthly_anomaly_1979_2014.nc" \
  "${output_dir}/tas_arctic_annual_anomaly_1979_2014.nc"

for file in \
  "${output_dir}/tas_monthly_anomaly_full.nc" \
  "${output_dir}/tas_monthly_anomaly_1979_2014.nc" \
  "${output_dir}/tas_mean_monthly_anomaly_1979_2014.nc" \
  "${output_dir}/tas_arctic_field_1979_2014.nc" \
  "${output_dir}/tas_arctic_monthly_anomaly_1979_2014.nc" \
  "${output_dir}/tas_arctic_annual_anomaly_1979_2014.nc"
do
  ncrename -O -v tas,tas_anom "${file}"
  ncatted -O \
    -a units,tas_anom,o,c,'degC' \
    -a long_name,tas_anom,o,c,'Near-Surface Air Temperature Monthly Anomaly' \
    -a anomaly_reference_period,tas_anom,o,c,'1981-2010' \
    "${file}"
done

echo "CDO/NCO monthly-anomaly workflow complete: ${output_dir}"
