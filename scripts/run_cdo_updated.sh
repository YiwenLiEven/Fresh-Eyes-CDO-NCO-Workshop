#!/usr/bin/env bash
# All data processing in this route is CDO-only. Run the shared input check first.
set -euo pipefail
hist=${1:?historical input required}; future=${2:?ssp585 input required}; out=${3:?output required}; end=${4:-2024}
mkdir -p "$out/work"
# Some CDO builds reparse filename arguments internally. Stage symbolic links
# and work from the output directory so paths with spaces also work on macOS.
hist_absolute="$(cd "$(dirname "$hist")" && pwd)/$(basename "$hist")"
future_absolute="$(cd "$(dirname "$future")" && pwd)/$(basename "$future")"
ln -sf "$hist_absolute" "$out/work/raw_historical.nc"
ln -sf "$future_absolute" "$out/work/raw_ssp585.nc"
out_label=$out
cd "$out"
out=.
hist=work/raw_historical.nc
future=work/raw_ssp585.nc
# Classic NetCDF intermediates also avoid repeated HDF5 probe messages.
CDO=(cdo -O -L -s -b F64 -f nc)
"${CDO[@]}" selname,tas "$hist" "$out/work/historical_tas.nc"
"${CDO[@]}" selyear,1979/2014 "$out/work/historical_tas.nc" "$out/work/historical.nc"
"${CDO[@]}" selname,tas "$future" "$out/work/ssp585_tas.nc"
"${CDO[@]}" selyear,2015/"$end" "$out/work/ssp585_tas.nc" "$out/work/ssp585.nc"
"${CDO[@]}" mergetime "$out/work/historical.nc" "$out/work/ssp585.nc" "$out/work/merged.nc"
"${CDO[@]}" subc,273.15 "$out/work/merged.nc" "$out/work/celsius_raw.nc"
"${CDO[@]}" setunit,degC "$out/work/celsius_raw.nc" "$out/work/celsius.nc"
"${CDO[@]}" selyear,1981/2010 "$out/work/celsius.nc" "$out/work/baseline.nc"
"${CDO[@]}" ymonmean "$out/work/baseline.nc" "$out/climatology.nc"
"${CDO[@]}" ymonsub "$out/work/celsius.nc" "$out/climatology.nc" "$out/work/anomaly_raw.nc"
"${CDO[@]}" chname,tas,tas_anom "$out/work/anomaly_raw.nc" "$out/anomaly.nc"
# ESMValCore climate_statistics(period=full) weights by the interval duration.
# The checked input contract guarantees full calendar-month bounds.
"${CDO[@]}" muldpm "$out/anomaly.nc" "$out/work/weighted.nc"
"${CDO[@]}" timsum "$out/work/weighted.nc" "$out/work/weighted_sum.nc"
"${CDO[@]}" expr,'tas_anom=1;' "$out/anomaly.nc" "$out/work/ones.nc"
"${CDO[@]}" muldpm "$out/work/ones.nc" "$out/work/days.nc"
"${CDO[@]}" timsum "$out/work/days.nc" "$out/work/weight_sum.nc"
"${CDO[@]}" div "$out/work/weighted_sum.nc" "$out/work/weight_sum.nc" "$out/map_mean.nc"
# Match the recipe's unweighted zonal and meridional means on a complete grid.
"${CDO[@]}" sellonlatbox,0,360,65,90 "$out/anomaly.nc" "$out/work/arctic.nc"
"${CDO[@]}" fldmean,weights=false "$out/work/arctic.nc" "$out/arctic_monthly.nc"
# ESMValCore annual_statistics uses equal monthly samples, unlike the map.
"${CDO[@]}" yearmean "$out/arctic_monthly.nc" "$out/arctic_annual.nc"
echo "CDO complete: $out_label"
