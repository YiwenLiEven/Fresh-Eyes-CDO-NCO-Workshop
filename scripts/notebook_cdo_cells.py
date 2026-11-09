"""One CDO calculation followed by one short inspection per teaching step.

Each entry is (title, explanation, command, inspection). The notebook adds its
own execution prefix. Run from a fresh demonstration directory containing
``data/historical.nc``, ``data/ssp585.nc``, and an empty ``cdo/`` directory.
"""

CDO_STEPS = [
    (
        "Select historical temperature",
        "Keep near-surface air temperature from the historical file. "
        "The inspection should show the variable name `tas`.",
        "cdo selname,tas data/historical.nc cdo/historical_tas.nc",
        "cdo showname cdo/historical_tas.nc",
    ),
    (
        "Select 1979–2014",
        "Keep the historical part of our analysis. "
        "The inspection should report 432 monthly records.",
        "cdo selyear,1979/2014 cdo/historical_tas.nc cdo/historical.nc",
        "cdo ntime cdo/historical.nc",
    ),
    (
        "Select SSP585 temperature",
        "Keep `tas` from the SSP5-8.5 scenario file, using the same model "
        "member and grid. Check that its variable is also `tas`.",
        "cdo selname,tas data/ssp585.nc cdo/ssp585_tas.nc",
        "cdo showname cdo/ssp585_tas.nc",
    ),
    (
        "Select 2015–2024",
        "Keep the scenario part needed for this analysis. "
        "The inspection should report 120 monthly records.",
        "cdo selyear,2015/2024 cdo/ssp585_tas.nc cdo/ssp585.nc",
        "cdo ntime cdo/ssp585.nc",
    ),
    (
        "Join the experiments",
        "Join the historical and scenario records in time order: 552 months "
        "from 1979 through 2024. The single `-b F64` option saves double "
        "precision before calculation; subsequent files inherit it.",
        "cdo -b F64 mergetime cdo/historical.nc cdo/ssp585.nc cdo/merged.nc",
        "cdo ntime cdo/merged.nc",
    ),
    (
        "Convert the temperature values",
        "Subtract 273.15 to convert Kelvin values to Celsius. The inspection "
        "summarizes the first month's minimum, mean, and maximum; "
        "`-seltimestep,1` restricts this check to one month.",
        "cdo subc,273.15 cdo/merged.nc cdo/celsius_raw.nc",
        "cdo infon -seltimestep,1 cdo/celsius_raw.nc",
    ),
    (
        "Update the unit label",
        "The values have been converted; now label them `degC`. "
        "Check the unit. Changing this label alone would not convert values.",
        "cdo setunit,degC cdo/celsius_raw.nc cdo/celsius.nc",
        "cdo showunit cdo/celsius.nc",
    ),
    (
        "Select the 1981–2010 reference period",
        "Keep the fixed 30-year reference period. "
        "Check that it contains 360 monthly records.",
        "cdo selyear,1981/2010 cdo/celsius.nc cdo/baseline.nc",
        "cdo ntime cdo/baseline.nc",
    ),
    (
        "Calculate twelve reference months",
        "Average the 30 Januaries, the 30 Februaries, and so on, giving "
        "each matching month equal weight. Check that the output contains "
        "calendar months 1 through 12.",
        "cdo ymonmean cdo/baseline.nc cdo/climatology.nc",
        "cdo showmon cdo/climatology.nc",
    ),
    (
        "Subtract the matching reference month",
        "Subtract reference January from each January, reference February "
        "from each February, and so on. Inspect the first month's anomaly "
        "range in degrees Celsius; positive values are warmer than its reference.",
        "cdo ymonsub cdo/celsius.nc cdo/climatology.nc cdo/anomaly_raw.nc",
        "cdo infon -seltimestep,1 cdo/anomaly_raw.nc",
    ),
    (
        "Name the anomaly variable",
        "Rename `tas` to `tas_anom` without changing the values. "
        "Check the new variable name in the monthly anomaly product.",
        "cdo chname,tas,tas_anom cdo/anomaly_raw.nc cdo/anomaly.nc",
        "cdo showname cdo/anomaly.nc",
    ),
    (
        "Multiply anomalies by month length",
        "The map uses duration weights: sum(anomaly × days) / sum(days). "
        "First multiply each anomaly by its month's number of days. "
        "The first-month summary is January's anomaly multiplied by 31.",
        "cdo muldpm cdo/anomaly.nc cdo/weighted.nc",
        "cdo infon -seltimestep,1 cdo/weighted.nc",
    ),
    (
        "Sum the weighted anomalies",
        "Sum over all months at each grid point to obtain the map's numerator. "
        "The inspection now summarizes one accumulated field.",
        "cdo timsum cdo/weighted.nc cdo/weighted_sum.nc",
        "cdo infon cdo/weighted_sum.nc",
    ),
    (
        "Create a field of ones",
        "Create one at every grid point and month for the denominator. "
        "The first-month minimum, mean, and maximum should all be 1. "
        "The input data have valid data throughout and complete monthly bounds.",
        "cdo expr,'tas_anom=1;' cdo/anomaly.nc cdo/ones.nc",
        "cdo infon -seltimestep,1 cdo/ones.nc",
    ),
    (
        "Count the days in each month",
        "Multiply the ones by month length using the file's calendar, "
        "including leap years. For January 1979, all three summary values "
        "should be 31.",
        "cdo muldpm cdo/ones.nc cdo/days.nc",
        "cdo infon -seltimestep,1 cdo/days.nc",
    ),
    (
        "Sum the calendar days",
        "Sum the month lengths to obtain the denominator. "
        "For 1979–2024, the summary should show 16,802 days everywhere.",
        "cdo timsum cdo/days.nc cdo/weight_sum.nc",
        "cdo infon cdo/weight_sum.nc",
    ),
    (
        "Calculate the duration-weighted map",
        "Divide the weighted anomaly sum by the day count. "
        "Inspect the minimum, mean, and maximum of the resulting anomaly map "
        "in degrees Celsius. This preserves the upstream duration weighting.",
        "cdo div cdo/weighted_sum.nc cdo/weight_sum.nc cdo/map_mean.nc",
        "cdo infon cdo/map_mean.nc",
    ),
    (
        "Select the Arctic",
        "Keep all longitudes and grid-point latitudes from 65°N to 90°N. "
        "The inspection reports how many grid points remain in this region.",
        "cdo sellonlatbox,0,360,65,90 cdo/anomaly.nc cdo/arctic.nc",
        "cdo ngridpoints cdo/arctic.nc",
    ),
    (
        "Calculate the monthly Arctic mean",
        "Give every selected grid point equal weight. On this complete "
        "rectangular grid, this matches the recipe's unweighted longitude "
        "mean followed by its unweighted latitude mean. Inspect the first "
        "month's single regional anomaly.",
        "cdo fldmean,weights=false cdo/arctic.nc cdo/arctic_monthly.nc",
        "cdo outputtab,date,value -seltimestep,1 cdo/arctic_monthly.nc",
    ),
    (
        "Calculate the annual Arctic mean",
        "Average each year's twelve monthly samples with equal weights, "
        "matching the upstream annual definition. Check that there are "
        "46 annual values. The map above uses month-length weights; "
        "this annual series uses equal month weights.",
        "cdo yearmean cdo/arctic_monthly.nc cdo/arctic_annual.nc",
        "cdo ntime cdo/arctic_annual.nc",
    ),
]
