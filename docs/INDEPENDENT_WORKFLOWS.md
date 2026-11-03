# Independent processing routes for the current seminar

This revision replaces the combined monthly CDO/NCO pipeline in the active
seminar and hands-on notebooks. Original source audits describe older versions.

| Scientific step | Python | CDO only | NCO only |
|---|---|---|---|
| Select variable and period | indexing, sel | selname, seldate | ncks -v, -d |
| Kelvin to Celsius | subtract 273.15 | subc, setunit | ncap2, ncatted |
| 12 monthly reference means | groupby time.month | ymonmean | strided ncwa, ncecat |
| Subtract matching month | grouped subtraction | ymonsub | ncap2, t modulo 12 |
| Mean anomaly map | mean time | timmean | ncwa -a time |
| Arithmetic Arctic mean | mean lat/lon | fldmean,weights=false | ncwa -a lat,lon |
| Equal-month annual mean | groupby time.year | yearmean | ncra --mro, 12-record groups |
| Final comparison plots | matplotlib | Python reads CDO outputs | Python reads NCO outputs |

Important: bare CDO fldmean AND fldavg use area weights. Changing only the
operator name does not disable weighting. The current script explicitly passes
weights=false. NCO requires an unlimited record dimension for ncra; the script
uses ncks --mk_rec_dmn time after the ncwa spatial reduction.

The CDO and NCO scripts use no Python data transformation and never read the
other route's outputs. Bash provides process control and filenames. The shared
Python input check is read-only. Synthetic-fixture generation and independent
validation are outside the two processing implementations.

Four products from each command-line route are checked against Python using
calendar-month/year labels, exact spatial coordinates, finite masks and a
0.0003 degC absolute tolerance (zero relative tolerance). The monthly anomalies
must have a zero 1981-2010 monthly baseline. The analysis must contain 432 months
and the stripes exactly 36 consecutive years.

Default data are synthetic. The input contract intentionally rejects missing
values, incomplete months and unsupported grids. This is a controlled seminar
comparison, not a universal processing recipe for all CMIP datasets.

The Python comparison map uses ordinary latitude/longitude axes rather than a
Robinson projection. Scientific values match the shared task; this presentation
choice avoids network downloads of cartographic data in Binder.

The older combined script and NCL figures remain optional historical examples.
They are not executed by binder/postBuild or the current run_all.sh.

References:

- https://mpim-sw.gitlab-pages.dkrz.de/cdo/modules/man/Fldstat.html
- https://nco.sourceforge.net/nco.html#Subcycle
- https://github.com/egalytska/Fresh_eyes/blob/393cfcf876fa47c6c231c3be70dbd9f8552fe3a3/stripes_EG.ipynb
