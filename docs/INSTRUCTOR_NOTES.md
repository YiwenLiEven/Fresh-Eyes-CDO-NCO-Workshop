# Instructor Notes

## Scientific caveats

- `data/demo/tas_demo.nc` is synthetic. It exists to guarantee reproducibility and must not be interpreted as a climate projection or observation.
- The optional ACCESS-CM2 teaching sample is spatially strided. It preserves the full monthly time axis but is not suitable for publication-quality area averages.
- CDO `fldmean` uses grid-cell area information where available and derives suitable weights for regular latitude–longitude grids. The workshop comparison uses a regular grid so its result can be checked against xarray cosine-latitude weighting.
- The original stripes notebook restricts the dataset to 1981–2010 before calculating anomalies. The revised workflow uses 1981–2010 only as a reference period and retains 1850–2014 for visualization.
- Small differences can arise from operator order, floating-point precision, time weighting, calendar handling, missing values, and grid-cell area definitions. Always state the comparison tolerance.

## Discussion prompts

1. Which workflow is easier to audit at a glance?
2. Which workflow is easier to customize for an unusual statistic?
3. Where should metadata validation occur?
4. What changes when the grid is curvilinear or unstructured?
5. What should remain in Python even when CDO/NCO performs preprocessing?

## Expected tool versions

The Codespaces container installs Debian Bookworm packages for CDO, NCO, and netCDF utilities. Exact patch versions may change when the base image is rebuilt. The automated tests verify scientific behavior rather than pinning distro package patch versions.

