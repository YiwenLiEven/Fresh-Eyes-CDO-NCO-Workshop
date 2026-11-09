"""Visible, standalone CDO teaching steps for the updated workshop notebooks.

The notebook supplies a bash cell wrapper and runs each step in $DEMO_OUT/cdo.
Its preparation cell creates work/ and two raw input symlinks in this directory.
"""

CDO_STEPS = [
    (
        "Select temperature and years",
        """Input: the historical and SSP585 files. Output: `work/historical.nc`
and `work/ssp585.nc`, containing only monthly near-surface air temperature
(`tas`) for 1979–2014 and 2015–2024. `DEMO_END` is 2024 for this exercise.
`selname` selects the variable; `selyear` selects the dates.

Each command reads its input file and writes its last file argument.
The usual form is `cdo operator input.nc output.nc`. Each run creates fresh
output files; start a new run before repeating the workflow.""",
        """cdo selname,tas historical_input.nc work/historical_tas.nc
cdo selyear,1979/2014 work/historical_tas.nc work/historical.nc
cdo selname,tas ssp585_input.nc work/ssp585_tas.nc
cdo selyear,2015/"$DEMO_END" work/ssp585_tas.nc work/ssp585.nc""",
    ),
    (
        "Join the two experiments",
        """Input: the two selected temperature files. Output: `work/merged.nc`.
`mergetime` joins and sorts their monthly records into the continuous
1979–2024 series: 552 months. Both experiments use the same ACCESS-CM2
member and grid. The single `-b F64` option stores the joined data in double
precision before calculations; later files inherit that precision.""",
        """cdo -b F64 mergetime work/historical.nc work/ssp585.nc work/merged.nc""",
    ),
    (
        "Convert Kelvin to Celsius",
        """Input: `work/merged.nc`, with temperature in Kelvin.
Output: `work/celsius.nc`, in degrees Celsius.
`subc,273.15` changes the values; `setunit,degC` updates the unit label.
Changing the label alone would leave the values in Kelvin.""",
        """cdo subc,273.15 work/merged.nc work/celsius_raw.nc
cdo setunit,degC work/celsius_raw.nc work/celsius.nc""",
    ),
    (
        "Select the reference period",
        """Input: `work/celsius.nc`. Output: `work/baseline.nc`.
Select 1981–2010, the fixed 30-year reference period, giving 360 months.
This reference period stays fixed when the analysis is extended.""",
        """cdo selyear,1981/2010 work/celsius.nc work/baseline.nc""",
    ),
    (
        "Calculate twelve monthly reference fields",
        """Input: `work/baseline.nc`. Output: `climatology.nc`, containing
twelve temperature fields. `ymonmean` averages the 30 Januaries together,
then the 30 Februaries, and so on. Each matching calendar month has equal
weight; January and July have different reference fields.""",
        """cdo ymonmean work/baseline.nc climatology.nc""",
    ),
    (
        "Subtract the matching monthly reference",
        """Inputs: the full Celsius series and the twelve reference fields.
Output: `anomaly.nc`, with 552 monthly anomaly fields.
`ymonsub` subtracts the matching calendar-month reference at every grid
point: January minus reference January, February minus reference February,
and so on. `chname` renames `tas` to `tas_anom`; an anomaly is measured in
degrees Celsius, with positive values warmer than that month's reference.""",
        """cdo ymonsub work/celsius.nc climatology.nc work/anomaly_raw.nc
cdo chname,tas,tas_anom work/anomaly_raw.nc anomaly.nc""",
    ),
    (
        "Average the map with month-length weights",
        """Input: `anomaly.nc`. Output: `map_mean.nc`, one mean anomaly map.
At each grid point, calculate **sum(anomaly × days in month) / sum(days in
month)**. This follows the upstream recipe's duration weighting.

`muldpm` multiplies by each month's number of days and `timsum` sums over
time. A field of ones gives the denominator using the same calendar,
including leap years. The input checks require complete monthly bounds
and valid data throughout, so this denominator covers the same samples.""",
        """cdo muldpm anomaly.nc work/weighted.nc
cdo timsum work/weighted.nc work/weighted_sum.nc
cdo expr,'tas_anom=1;' anomaly.nc work/ones.nc
cdo muldpm work/ones.nc work/days.nc
cdo timsum work/days.nc work/weight_sum.nc
cdo div work/weighted_sum.nc work/weight_sum.nc map_mean.nc""",
    ),
    (
        "Average the Arctic grid points",
        """Input: `anomaly.nc`. Output: `arctic_monthly.nc`, one anomaly per
month. `sellonlatbox` selects all longitudes and grid-point latitudes from
65°N to 90°N. `fldmean,weights=false` gives each selected grid point equal
weight. On this complete rectangular grid, that matches the recipe's
unweighted longitude mean followed by its unweighted latitude mean.
This is an unweighted regional mean, not an area-weighted mean.""",
        """cdo sellonlatbox,0,360,65,90 anomaly.nc work/arctic.nc
cdo fldmean,weights=false work/arctic.nc arctic_monthly.nc""",
    ),
    (
        "Average the twelve months in each year",
        """Input: `arctic_monthly.nc`. Output: `arctic_annual.nc`, one Arctic
anomaly for each of the 46 years. `yearmean` gives the twelve monthly
samples equal weight, matching the upstream annual-statistics definition.
The annual series therefore uses equal month weights, while the map above
uses month-length weights.""",
        """cdo yearmean arctic_monthly.nc arctic_annual.nc""",
    ),
]
