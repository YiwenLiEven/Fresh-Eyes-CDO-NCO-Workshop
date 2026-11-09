#!/usr/bin/env bash
# All data processing in this route is NCO-only. Run the shared input check first.
set -euo pipefail
hist=${1:?historical input required}; future=${2:?ssp585 input required}; out=${3:?output required}; end=${4:-2024}
mkdir -p "$out/work"
ncks -O -3 --mk_rec_dmn time -v tas,time_bnds -d time,'1979-01-01','2014-12-31' "$hist" "$out/work/historical.nc"
ncks -O -3 --mk_rec_dmn time -v tas,time_bnds -d time,'2015-01-01',"$end-12-31" "$future" "$out/work/ssp585.nc"
ncrcat -O "$out/work/historical.nc" "$out/work/ssp585.nc" "$out/work/merged.nc"
ncap2 -O -s 'tas=double(tas)-273.15;tas@units="degC";' "$out/work/merged.nc" "$out/work/celsius.nc"
ncatted -O -a _FillValue,tas,o,d,1.0e20 -a missing_value,tas,o,d,1.0e20 -a _FillValue,time_bnds,d,, -a cell_measures,tas,d,, "$out/work/celsius.nc"
ncks -O -d time,'1981-01-01','2010-12-31' "$out/work/celsius.nc" "$out/work/baseline.nc"
months=()
for m in {0..11}; do
  printf -v tag '%02d' "$m"
  ncwa -O -a time -d time,"$m",359,12 "$out/work/baseline.nc" "$out/work/clim_$tag.nc"
  months+=("$out/work/clim_$tag.nc")
done
ncecat -O -u month "${months[@]}" "$out/climatology.nc"
ncap2 -O -s 'month[month]=array(1,1,$month);month@long_name="calendar month";' "$out/climatology.nc" "$out/climatology.nc"
ncrename -O -v tas,tas_clim "$out/climatology.nc" "$out/work/clim_named.nc"
ncks -O --fix_rec_dmn month "$out/work/clim_named.nc" "$out/work/clim_fixed.nc"
ncks -A -v tas_clim "$out/work/clim_fixed.nc" "$out/work/celsius.nc"
ncap2 -O -s 'tas_anom=tas;for(t=0;t<$time.size;t++){tas_anom(t,:,:)=tas(t,:,:)-tas_clim(t%12,:,:);}tas_anom@units="degC";tas_anom@anomaly_reference_period="1981-2010";' "$out/work/celsius.nc" "$out/work/anomaly_all.nc"
ncks -O -v tas_anom,time_bnds "$out/work/anomaly_all.nc" "$out/anomaly.nc"
# Duration in the CF time units. Normalization cancels days versus hours.
ncap2 -O -s 'duration[time]=double(time_bnds(:,1)-time_bnds(:,0));' "$out/anomaly.nc" "$out/work/weighted.nc"
ncwa -O -a time -w duration -v tas_anom "$out/work/weighted.nc" "$out/map_mean.nc"
ncwa -O -a lon -d lat,65.0,90.0 "$out/anomaly.nc" "$out/work/arctic_zonal.nc"
ncwa -O -a lat "$out/work/arctic_zonal.nc" "$out/arctic_monthly.nc"
ncks -O --mk_rec_dmn time "$out/arctic_monthly.nc" "$out/work/arctic_record.nc"
ncra -O --mro -d time,,,12,12 "$out/work/arctic_record.nc" "$out/arctic_annual.nc"
# ncra averages bounds as ordinary variables; replace them with each full year.
ncks -O -v time_bnds -d time,0,,12 "$out/work/arctic_record.nc" "$out/work/year_starts.nc"
ncks -O -v time_bnds -d time,11,,12 "$out/work/arctic_record.nc" "$out/work/year_ends.nc"
ncap2 -O -s 'year_end[time]=time_bnds(:,1);' "$out/work/year_ends.nc" "$out/work/year_ends_named.nc"
ncks -A -C -v year_end "$out/work/year_ends_named.nc" "$out/work/year_starts.nc"
ncap2 -O -s 'time_bnds(:,1)=year_end;' "$out/work/year_starts.nc" "$out/work/year_bounds.nc"
ncks -A -C -v time_bnds "$out/work/year_bounds.nc" "$out/arctic_annual.nc"
echo "NCO complete: $out"
