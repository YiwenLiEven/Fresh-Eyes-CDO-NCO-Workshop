#!/usr/bin/env bash
# NCO-only processing. Bash controls filenames and loops, not data arithmetic.
set -euo pipefail
input=${1:-data/demo/tas_demo.nc}
out=${2:-outputs/demo/monthly/nco}
mkdir -p "$out/work"
ncks -O -v tas -d time,'1979-01-01','2014-12-31' "$input" "$out/work/selected.nc"
ncap2 -O -s 'tas=double(tas)-273.15;tas@units="degC";' "$out/work/selected.nc" "$out/work/celsius.nc"
# The shared input contract rejects missing values. A finite common sentinel
# also avoids NaN-vs-NaN metadata warnings in NCO arithmetic.
ncatted -O -a _FillValue,tas,o,d,1.0e20 "$out/work/celsius.nc"
ncks -O -d time,'1981-01-01','2010-12-31' "$out/work/celsius.nc" "$out/work/baseline.nc"
# Baseline has 360 consecutive months starting in January. Each stride selects
# one calendar month across all 30 years. ncwa removes the reduced time axis.
months=()
for m in {0..11}; do
  printf -v tag '%02d' "$m"
  ncwa -O -a time -d time,"$m",359,12 "$out/work/baseline.nc" "$out/work/clim_$tag.nc"
  months+=("$out/work/clim_$tag.nc")
done
ncecat -O -u month "${months[@]}" "$out/tas_monthly_climatology_1981_2010.nc"
ncrename -O -v tas,tas_clim "$out/tas_monthly_climatology_1981_2010.nc" "$out/work/clim_named.nc"
ncks -A -v tas_clim "$out/work/clim_named.nc" "$out/work/celsius.nc"
# The selected series starts in January, so zero-based t modulo 12 identifies
# its climatology month. All subtraction happens inside NCO ncap2.
ncap2 -O -s 'tas_anom=tas;for(t=0;t<$time.size;t++){tas_anom(t,:,:)=tas(t,:,:)-tas_clim(t%12,:,:);}tas_anom@units="degC";tas_anom@anomaly_reference_period="1981-2010";' \
  "$out/work/celsius.nc" "$out/work/anomaly.nc"
ncks -O -v tas_anom "$out/work/anomaly.nc" "$out/tas_monthly_anomaly_1979_2014.nc"
ncwa -O -a time "$out/tas_monthly_anomaly_1979_2014.nc" "$out/tas_mean_monthly_anomaly_1979_2014.nc"
ncwa -O -a lat,lon -d lat,65.0,90.0 "$out/tas_monthly_anomaly_1979_2014.nc" "$out/tas_arctic_monthly_anomaly_1979_2014.nc"
# ncwa can leave time fixed; ncra requires a record (unlimited) dimension.
ncks -O --mk_rec_dmn time "$out/tas_arctic_monthly_anomaly_1979_2014.nc" "$out/work/arctic_record.nc"
# Groups of 12 records, one output per group, no month-length weights.
ncra -O --mro -d time,,,12,12 "$out/work/arctic_record.nc" "$out/tas_arctic_annual_anomaly_1979_2014.nc"
echo "NCO-only processing complete: $out"
