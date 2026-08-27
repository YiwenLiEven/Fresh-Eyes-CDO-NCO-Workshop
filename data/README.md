# Workshop data

The repository supports two teaching datasets:

1. `data/demo/tas_demo.nc` is generated deterministically during Codespaces setup. It is CF-style, global, monthly, and spans 1850–2014. It guarantees that every participant can run the workshop even if a remote ESGF node is unavailable. It is synthetic and must not be used for scientific conclusions.
2. `data/raw/tas_ACCESS-CM2_teaching_sample.nc` is a lightweight, spatially strided sample of the exact ACCESS-CM2 historical `tas` file used by the original Fresh Eyes workshop. Run `make real-data` to retrieve it through OPeNDAP. It is suitable for teaching and software comparison, not publication-quality analysis.

The full source file is:

`tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc`

The real-data script preserves all 1,980 monthly time steps while sampling the latitude and longitude dimensions. The reduced grid keeps Codespaces downloads practical while retaining the full historical time axis required by the stripes demonstration.

