# Mapping the Original Fresh Eyes Python Workshop to CDO and NCO

## Source reviewed

Original repository: [abhnil/Fresh_Eyes_on_CMIP_Data_Workshop](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop)

The review covers all three notebooks in the source repository as available in August 2026.

## Notebook inventory

### `getcmip6data.ipynb`

- **Scientific purpose:** discover, access, open, and inspect CMIP6 monthly near-surface air temperature.
- **Dataset:** CMIP6, `ACCESS-CM2`, `historical`, `r1i1p1f1`, `Amon`, `tas`, native grid `gn`, version `v20191108`.
- **Institution:** `CSIRO-ARCCSS`.
- **Time coverage:** 1850-01 through 2014-12, 1,980 monthly steps.
- **Spatial coverage:** global, 144 latitude × 192 longitude.
- **Access routes demonstrated:** Google Cloud Zarr catalog, ESGF website/wget, ESGF Search API with OPeNDAP, and Intake-ESM.
- **Python packages:** pandas, xarray, zarr, fsspec, pyesgf, intake, warnings.
- **Operations:** catalog filtering, opening remote data, inspecting a dataset, and plotting the first time slice.

### `process.ipynb`

- **Scientific purpose:** post-process the same ACCESS-CM2 `tas` dataset.
- **Python packages:** intake, xarray through Intake-ESM, matplotlib, cartopy, warnings.
- **Operations:** maximum over time, conversion from K to °C, Robinson-projection map, seasonal grouping and mean, four-panel seasonal plot.

### `stripes.ipynb`

- **Scientific purpose:** create climate stripes from ACCESS-CM2 `tas`.
- **Python packages:** pyesgf, xarray, numpy, matplotlib.
- **Operations:** ESGF API search, OPeNDAP opening, cosine-latitude weighted global mean, 1981–2010 temporal selection, annual means, anomaly relative to the selected-period mean, line plot, and stripe plot.
- **Important teaching observation:** the source code selects 1981–2010 before annualizing and calculating anomalies. It therefore produces only 30 stripes. This workshop preserves the 1981–2010 reference period but applies the reference to the complete 1850–2014 annual series.

## Operation mapping

| Original Python task | Python/xarray method | CDO | NCO | Can reproduce? | Workshop decision |
|---|---|---|---|---|---|
| Open local NetCDF | `xr.open_dataset()` | `cdo sinfo` / any operator input | `ncks` | Yes | Show all three roles |
| Open remote OPeNDAP | `xr.open_dataset(url)` | Build-dependent remote input | `ncks URL output.nc` | Yes | Use NCO for explicit retrieval |
| Select `tas` | `ds["tas"]` | `selname,tas` | `ncks -v tas` | Yes | Show NCO and CDO syntax |
| Select 1981–2010 | `.sel(time=slice(...))` | `selyear,1981/2010` | `ncks -d time,start,end` | Yes | Prefer CDO date-aware selection; show NCO index selection |
| Convert K to °C | `tas - 273.15` | `subc,273.15` | `ncap2 -s 'tas=tas-273.15'` | Yes | Use CDO; mention NCO alternative |
| Maximum over time | `.max("time")` | `timmax` | `ncra -y max` | Yes | Use CDO in the main workflow |
| Seasonal climatology | `.groupby("time.season").mean()` | `yseasmean` | Possible but awkward | Yes | Use CDO |
| Annual mean | `.groupby("time.year").mean()` | `yearmean` | `ncra` with carefully grouped files | Yes | Use CDO |
| Cosine-latitude global mean | `.weighted(cos(lat)).mean()` | `fldmean` | `ncwa -w ...` with prepared weights | Yes | Use CDO; validate against xarray |
| Baseline mean | `.sel(...).mean()` | `timmean -selyear,...` | `ncra` after selection | Yes | Use CDO |
| Subtract baseline | `annual - baseline` | `subc` | `ncap2` | Yes | Use CDO and NCO metadata cleanup |
| Edit names/attributes | xarray attributes | `setattribute` | `ncrename`, `ncatted` | Yes | Use NCO |
| Robinson map | cartopy | Not a processing task | Not a processing task | No direct replacement intended | Keep Python visualization |
| Climate stripes | matplotlib | Not a processing task | Not a processing task | No direct replacement intended | CDO/NCO prepare; Python plots |

## Tasks not present in the source notebooks

The reviewed notebooks do **not** perform the following tasks:

- spatial subsetting;
- trend estimation;
- multi-file merging;
- ensemble statistics;
- regridding;
- advanced statistical inference;
- machine learning.

These topics should not be presented as reproductions of the source workshop. If introduced during discussion, label them clearly as possible extensions.

## Resulting teaching architecture

```text
Original or teaching NetCDF
          |
          v
CDO/NCO: selection, reduction, climatology, anomalies, metadata
          |
          v
Small analysis-ready NetCDF
          |
          v
Python: validation, interpretation, visualization
```

The intended message is complementarity, not competition:

> Use CDO/NCO to prepare the data.  
> Use Python to understand the data.

