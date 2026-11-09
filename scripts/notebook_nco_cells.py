"""Literal NCO commands and explanations used by the notebook builder."""

NCO_STEPS = [
    (
        'Select the historical and scenario months',
        '''`ncks` extracts `tas` and its time bounds from each raw input. The
historical selection contains **432 months, 1979–2014**. For an end year of
2024, the SSP5-8.5 selection contains **120 months, 2015–2024**.

`-v` selects variables; `-d time,start,end` selects dates. `--mk_rec_dmn time`
makes time the record dimension needed by `ncrcat`. The first `-3` selects
classic NetCDF; the merged file and later outputs inherit that format. The
outputs are `work/historical.nc` and `work/ssp585.nc`.''',
        r'''ncks -3 --mk_rec_dmn time -v tas,time_bnds \
  -d time,'1979-01-01','2014-12-31' \
  historical_input.nc work/historical.nc

ncks --mk_rec_dmn time -v tas,time_bnds \
  -d time,'2015-01-01',"$DEMO_END-12-31" \
  ssp585_input.nc work/ssp585.nc''',
    ),
    (
        'Join the two experiments',
        '''`ncrcat` concatenates records in the supplied order: historical
first, then SSP5-8.5. `work/merged.nc` contains **552 consecutive monthly fields
for 1979–2024**. No averaging occurs in this step.''',
        r'''ncrcat work/historical.nc work/ssp585.nc work/merged.nc''',
    ),
    (
        'Convert Kelvin to Celsius',
        '''`ncap2 -s` evaluates the visible arithmetic expression. `double(tas)`
requests double precision, and subtracting **273.15** converts Kelvin to Celsius.
The result is `work/celsius.nc` with the same monthly fields.

`ncatted -a` edits attributes. The two missing-value attributes use the same
double-precision value. The time bounds are complete, so their unused fill
attribute is removed. The original `cell_measures` link refers to an external
area file; it is removed because these spatial means use equal grid-point
weights. These attribute edits do not change the valid temperature values.''',
        r'''ncap2 -s '
  tas=double(tas)-273.15;
  tas@units="degC";
' work/merged.nc work/celsius.nc

ncatted \
  -a _FillValue,tas,o,d,1.0e20 \
  -a missing_value,tas,o,d,1.0e20 \
  -a _FillValue,time_bnds,d,, \
  -a cell_measures,tas,d,, \
  work/celsius.nc''',
    ),
    (
        'Select the 1981–2010 reference period',
        '''The reference is taken from the historical years in
`work/celsius.nc`. `work/baseline.nc` contains **360 consecutive months**,
starting in January 1981 and ending in December 2010.''',
        r'''ncks -d time,'1981-01-01','2010-12-31' \
  work/celsius.nc work/baseline.nc''',
    ),
    (
        'Calculate twelve monthly reference fields',
        '''NCO indices start at **zero**. For January, `m=0` and
`-d time,0,359,12` selects indices **0, 12, 24, …, 348**: the 30 Januaries.
February starts at index 1; the loop continues through December at index 11.

`ncwa -a time` takes an arithmetic mean and removes the time dimension.
`ncecat -u month` joins the twelve fields in January-to-December order.
`ncap2` adds month labels **1–12** and writes the final `climatology.nc`.
`month_files` holds only the twelve filenames.''',
        r'''month_files=()
for m in {0..11}; do
  printf -v tag '%02d' "$m"
  ncwa -a time -d time,"$m",359,12 \
    work/baseline.nc "work/clim_$tag.nc"
  month_files+=("work/clim_$tag.nc")
done

ncecat -u month "${month_files[@]}" work/climatology_unlabelled.nc

ncap2 -s '
  month[month]=array(1,1,$month);
  month@long_name="calendar month";
' work/climatology_unlabelled.nc climatology.nc''',
    ),
    (
        'Subtract the matching calendar-month reference',
        '''Rename the reference temperature to `tas_clim`, fix its month
dimension, and append it to the temperature file. A fixed month dimension
allows the time dimension to remain the single record dimension in classic
NetCDF.

The input starts in January and contains consecutive complete months. Therefore
`t%12` identifies the corresponding zero-based reference month for every time
index `t`. `ncap2` subtracts that reference at every latitude and longitude.
`anomaly.nc` retains **552 monthly anomaly fields** and their time bounds.''',
        r'''ncrename -v tas,tas_clim climatology.nc work/clim_named.nc
ncks --fix_rec_dmn month work/clim_named.nc work/clim_fixed.nc
ncks -A -v tas_clim work/clim_fixed.nc work/celsius.nc

ncap2 -s '
  tas_anom=tas;
  for(t=0;t<$time.size;t++){
    tas_anom(t,:,:)=tas(t,:,:)-tas_clim(t%12,:,:);
  }
  tas_anom@units="degC";
  tas_anom@anomaly_reference_period="1981-2010";
' work/celsius.nc work/anomaly_all.nc

ncks -v tas_anom,time_bnds work/anomaly_all.nc anomaly.nc''',
    ),
    (
        'Calculate the duration-weighted mean anomaly map',
        '''`time_bnds(:,1)-time_bnds(:,0)` gives each monthly interval's
duration in the file's time units. `ncwa -a time -w duration` computes
**Σ(anomaly × duration) / Σ(duration)** at each grid point.

`map_mean.nc` contains one latitude–longitude field. The map follows the
recipe's duration weighting and is a period-mean anomaly, not a trend.''',
        r'''ncap2 -s '
  duration[time]=double(time_bnds(:,1)-time_bnds(:,0));
' anomaly.nc work/weighted.nc

ncwa -a time -w duration -v tas_anom \
  work/weighted.nc map_mean.nc''',
    ),
    (
        'Average the Arctic grid points',
        '''`-d lat,65.0,90.0` selects latitude centres from 65°N to 90°N.
`ncwa -a lon` first takes the zonal mean; `ncwa -a lat` then takes the
meridional mean. No area weights are supplied, matching the recipe's arithmetic
spatial means.

`arctic_monthly.nc` contains **552 monthly Arctic anomalies**.''',
        r'''ncwa -a lon -d lat,65.0,90.0 \
  anomaly.nc work/arctic_zonal.nc

ncwa -a lat work/arctic_zonal.nc arctic_monthly.nc''',
    ),
    (
        'Calculate annual Arctic anomalies',
        '''`ncks --mk_rec_dmn time` prepares the monthly time series for
record averaging. With `ncra --mro -d time,,,12,12`, the stride and averaging
group both contain twelve records: January–December of each year.

`arctic_annual.nc` contains **46 annual values, 1979–2024**. Each monthly sample
has equal weight. This annual definition deliberately differs from the
duration-weighted map.''',
        r'''ncks --mk_rec_dmn time \
  arctic_monthly.nc work/arctic_record.nc

ncra --mro -d time,,,12,12 \
  work/arctic_record.nc arctic_annual.nc''',
    ),
    (
        'Set the annual time bounds',
        '''`ncra` also averages the monthly bounds as ordinary variables.
Replace those bounds with the start of January and the end of December for
each year, leaving the annual anomaly values unchanged.

The first selection takes records **0, 12, 24, …**; the second takes records
**11, 23, 35, …**. `-C -v` copies only the named variable, so the annual time
coordinate is preserved. The final file has **46 complete calendar-year
intervals**.''',
        r'''ncks -v time_bnds -d time,0,,12 \
  work/arctic_record.nc work/year_starts.nc
ncks -v time_bnds -d time,11,,12 \
  work/arctic_record.nc work/year_ends.nc

ncap2 -s 'year_end[time]=time_bnds(:,1);' \
  work/year_ends.nc work/year_ends_named.nc
ncks -A -C -v year_end work/year_ends_named.nc work/year_starts.nc

ncap2 -s 'time_bnds(:,1)=year_end;' \
  work/year_starts.nc work/year_bounds.nc
ncks -A -C -v time_bnds work/year_bounds.nc arctic_annual.nc''',
    ),
]
