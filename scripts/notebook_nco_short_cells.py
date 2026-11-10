"""Direct NCO commands for the annual Arctic anomaly demonstration."""

NCO_SHORT_STEPS = [
    (
        'Select historical months',
        'Select tas for January 1979–December 2014. -v selects the variable; -d selects dates. Coordinates and linked time bounds are retained automatically. The metadata shows 432 monthly records.',
        'ncks -v tas -d time,1979-01-01,2014-12-31 data/historical.nc nco/historical.nc',
        'ncks -m -C -v tas nco/historical.nc',
    ),
    (
        'Select SSP5-8.5 months',
        'Select January 2015–December 2024 from the original SSP5-8.5 file. The result contains 120 monthly records on the same grid.',
        'ncks -v tas -d time,2015-01-01,2024-12-31 data/ssp585.nc nco/ssp585.nc',
        'ncks -m -C -v tas nco/ssp585.nc',
    ),
    (
        'Join historical and SSP5-8.5',
        'ncrcat joins the monthly records in the listed order. The output contains 552 consecutive months from 1979 through 2024.',
        'ncrcat nco/historical.nc nco/ssp585.nc nco/merged.nc',
        'ncks -m -C -v tas nco/merged.nc',
    ),
    (
        'Convert Kelvin to Celsius',
        'ncap2 -s evaluates an arithmetic expression. Subtract 273.15 and label the values degC. double(tas) keeps double precision for subsequent calculations. Inspect the first month at one grid point.',
        'ncap2 -s \'tas=double(tas)-273.15;tas@units="degC";\' nco/merged.nc nco/celsius.nc',
        'ncks -H -C -v tas -d time,0 -d lat,0 -d lon,0 nco/celsius.nc',
    ),
    (
        'Calculate the monthly Arctic temperature',
        'Select latitude centres from 65°N to 90°N. ncwa -a lat,lon averages both spatial dimensions, giving every selected grid point equal weight. Inspect the first twelve monthly temperatures.',
        'ncwa -a lat,lon -d lat,65.0,90.0 nco/celsius.nc nco/arctic_monthly.nc',
        'ncks -H -C -v tas -d time,0,11 nco/arctic_monthly.nc',
    ),
    (
        'Calculate the annual Arctic temperature',
        'ncra --mro produces one mean for each group of twelve monthly records. Every month has equal weight. -C -v tas,time retains the temperature and time coordinate without carrying monthly interval bounds into the annual output. Check that there are 46 annual values.',
        'ncra --mro -C -v tas,time -d time,,,12,12 nco/arctic_monthly.nc nco/annual_temperature.nc',
        'ncks -m -C -v tas nco/annual_temperature.nc',
    ),
    (
        'Calculate the 1981–2010 reference temperature',
        'Select the thirty annual values from 1981 through 2010 and average them over time. The result is one Arctic reference temperature. This baseline uses the same complete years and equal monthly weights as the shared calculation.',
        'ncwa -a time -d time,1981-01-01,2010-12-31 nco/annual_temperature.nc nco/reference.nc',
        'ncks -H -C -v tas nco/reference.nc',
    ),
    (
        'Subtract the reference temperature',
        'ncdiff subtracts the second file from the first. The single reference temperature is subtracted from every annual value. Positive anomalies indicate years warmer than the 1981–2010 reference. Inspect the first five annual anomalies.',
        'ncdiff nco/annual_temperature.nc nco/reference.nc nco/annual_anomaly.nc',
        'ncks -H -C -v tas -d time,0,4 nco/annual_anomaly.nc',
    ),
    (
        'Label the annual anomaly',
        'Label tas as an air-temperature anomaly. Remove links to the monthly bounds, auxiliary coordinates and external area variable that are absent from this annual series. The time coordinate identifies each year; this file does not claim interval bounds. The anomaly values remain unchanged.',
        'ncatted -a bounds,time,d,, -a coordinates,tas,d,, -a cell_measures,tas,d,, -a standard_name,tas,o,c,air_temperature_anomaly nco/annual_anomaly.nc',
        'ncks -m -C -v tas nco/annual_anomaly.nc',
    ),
]
