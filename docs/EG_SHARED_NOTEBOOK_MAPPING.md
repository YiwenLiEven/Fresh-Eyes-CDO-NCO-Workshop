# Shared seminar reference: exact reproduction map

Reviewed on 2026-10-15. Reference: [egalytska/Fresh_eyes, stripes_EG.ipynb](https://github.com/egalytska/Fresh_eyes/blob/393cfcf876fa47c6c231c3be70dbd9f8552fe3a3/stripes_EG.ipynb), commit `393cfcf876fa47c6c231c3be70dbd9f8552fe3a3` (2026-09-03, fixed map colour limits). This notebook is the primary target for YL's 20-minute Binder contribution. Abhnil's original notebooks remain the broader workshop reference.

## Contents actually inspected

The repository contains a short README and one notebook with 12 cells, including an empty final code cell. Imports: xarray, NumPy, matplotlib, matplotlib.colors.ListedColormap and cartopy.crs. ListedColormap is imported but not used. Data loading uses a local file, despite the introductory heading mentioning ESGF-API; the notebook does not itself download the data.

Dataset: CMIP6 / CMIP / CSIRO-ARCCSS / ACCESS-CM2 / historical / r1i1p1f1 / Amon / tas / gn / v20191108. File: `tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc`. Input period: 1850–2014. Baseline: 1981–2010. Analysis: 1979–2014. Map: global. Regional series: latitude centres from 65 to 90 degrees north, all longitudes.

| Source cell | Exact Python operation | CDO/NCO/NCL reproduction |
|---|---|---|
| 2 | Package imports | Python for reference and validation; CDO/NCO executables and NCL driver |
| 3 | `xr.open_dataset(local_file)` | `ncks -v tas`; inspect with `cdo sinfo` |
| 5 | `tas = ds.tas - 273.15` | `cdo subc,273.15` |
| 5 | Select baseline 1981–2010 | `cdo selyear,1981/2010` |
| 5 | Calendar-month climatology | `cdo ymonmean` |
| 5 | Subtract corresponding month at each grid cell | `cdo ymonsub data climatology anomaly` |
| 5 | Select 1979–2014 anomalies | `cdo seldate,1979-01-01,2014-12-31` |
| 6 | Mean over all selected monthly anomalies | `cdo timmean` |
| 6 | Robinson map, coolwarm, −0.2/+0.4 °C | NCL `gsn_csm_contour_map`, Robinson, `MPL_coolwarm`, same limits |
| 8 | Select 65–90N, arithmetic mean over lat/lon | `ncks -d lat,65.0,90.0` then `ncwa -a lat,lon` |
| 8 | Monthly Arctic line with zero reference | NCL `gsn_csm_xy`, 432 monthly points and a zero line |
| 10 | Arctic series grouped by calendar year | `cdo yearmean`, 36 values |
| 10 | Blue–white–red stripes, symmetric data-derived limit | NCL polygon colours using ±max(abs(annual)); 36 equal-width stripes |

## Fidelity decisions

- Preserve the source's **unweighted Arctic mean**. CDO `fldmean` is area-weighted and is reserved for a clearly labelled extension.
- Preserve equal weights for monthly samples, both in the baseline and annual average.
- Match map central longitude 0 and fixed colour range; graphic fonts and coastline resolution may differ across plotting libraries.
- Draw exactly one full rectangle per annual value. This avoids the half-width edge cells that can arise from passing sample centres to `pcolormesh`.
- Validate numerical fields before plotting. Compare four products, their shapes, finite-value masks, selected periods and baseline residuals.
- Default synthetic data are labelled explicitly. They validate implementation, not ACCESS-CM2 climate results. Full-grid numerical agreement across presenters requires the same original file.

## Extensions kept separate

The older notebooks retain global area-weighted annual anomalies, time maxima and seasonal climatology. These are useful follow-up material, but they are not substituted for EG's monthly-anomaly/Arctic example. The optional CMIP7 discussion is a transfer of method, not a claimed CMIP6–CMIP7 comparison result.

The saved-data hyperlink referred to in the email was not included in the supplied message. No substitute download is represented as that saved file.
