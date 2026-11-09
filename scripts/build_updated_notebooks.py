"""Build the English seminar and participant notebooks for the updated recipe."""
from pathlib import Path
import shutil
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
N = ROOT / 'notebooks'

def md(s): return nbf.v4.new_markdown_cell(s.strip())
def code(s, backstage=False):
    cell = nbf.v4.new_code_cell(s.strip())
    if backstage:
        cell.metadata['jupyter'] = {'source_hidden': True}
        cell.metadata['tags'] = ['infrastructure']
    return cell

def save(name, cells):
    path = N / name
    archive = N / ('legacy_' + name)
    if path.exists() and not archive.exists(): shutil.copy2(path, archive)
    nb = nbf.v4.new_notebook(cells=cells, metadata={
        'kernelspec': {'display_name':'Python 3 (ipykernel)','language':'python','name':'python3'},
        'language_info': {'name':'python','version':'3.11'},
    })
    if path.exists():
        previous = nbf.read(path, as_version=4)
        if len(previous.cells) == len(nb.cells):
            for old, new in zip(previous.cells, nb.cells):
                if old.cell_type == new.cell_type:
                    new['id'] = old.get('id', new['id'])
    nbf.write(nb, path)

setup = '''from pathlib import Path
import os, sys, subprocess, json, uuid
from datetime import datetime, timezone
from IPython.display import display, Image

ROOT = Path.cwd().resolve()
if not (ROOT / "scripts/run_updated_workflows.sh").exists():
    ROOT = ROOT.parent
assert (ROOT / "scripts/run_updated_workflows.sh").exists(), "Open this notebook from the workshop repository."
os.chdir(ROOT)

# The seminar uses real ACCESS-CM2. Synthetic mode is an explicit software-test option.
DATA_MODE = os.environ.get("WORKSHOP_MODE", "real")  # "real" or "synthetic"
END_YEAR = int(os.environ.get("WORKSHOP_END_YEAR", "2024"))
assert DATA_MODE in {"synthetic", "real"}
assert END_YEAR >= 2024
os.environ["OMP_NUM_THREADS"] = "1"
if DATA_MODE == "synthetic":
    fixture = ROOT / "data/updated_fixture"
    subprocess.run([sys.executable, "scripts/generate_updated_fixture.py", str(fixture)], check=True)
    HIST, FUTURE = fixture / "historical.nc", fixture / "ssp585.nc"
else:
    directory = ROOT / "data/access_cm2"
    HIST = Path(os.environ.get("WORKSHOP_HISTORICAL", str(directory / "tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc")))
    FUTURE = Path(os.environ.get("WORKSHOP_FUTURE", str(directory / "tas_Amon_ACCESS-CM2_ssp585_r1i1p1f1_gn_201501-210012.nc")))
    missing = [str(p) for p in (HIST, FUTURE) if not p.is_file()]
    if missing:
        raise FileNotFoundError("Real-data mode requires both raw files. No synthetic substitution is allowed. Missing: " + "; ".join(missing) + ". See docs/UPDATED_DEMO.md.")

RUN = ROOT / "outputs" / ("updated_" + DATA_MODE + "_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + uuid.uuid4().hex[:6])
RUN.mkdir(parents=True)
os.environ.update(DEMO_HIST=os.path.relpath(HIST, ROOT), DEMO_FUTURE=os.path.relpath(FUTURE, ROOT), DEMO_OUT=os.path.relpath(RUN, ROOT), DEMO_END=str(END_YEAR))
print("DATA MODE:", "SYNTHETIC SOFTWARE TEST — NOT ACCESS-CM2" if DATA_MODE == "synthetic" else "REAL ACCESS-CM2: historical + SSP5-8.5")
print("Analysis:", f"1979–{END_YEAR}", "| Monthly reference: 1981–2010")
print("Outputs:", RUN.relative_to(ROOT))
'''
check = '''subprocess.run([sys.executable, "scripts/check_updated_inputs.py", str(HIST), str(FUTURE), "--end-year", str(END_YEAR)], check=True)
for command in (["cdo", "-V"], ["ncks", "--version"]):
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    print((result.stdout + result.stderr).splitlines()[0])
print("Python", sys.version.split()[0])'''
contract = '''## 02 · The calculation we are comparing

| Step | Definition used by every route |
|---|---|
| Input | ACCESS-CM2 monthly `tas` in Kelvin, historical + SSP5-8.5; or explicitly labeled synthetic test data |
| Main period | January 1979–December 2024: **552 months, 46 annual values** |
| Reference | January 1981–December 2010: 30 values for each calendar month |
| Monthly anomaly | Temperature minus the matching calendar-month reference field |
| Mean anomaly map | **Month-duration weighted** mean over the analysis period |
| Arctic mean | Latitude centres 65–90°N, all longitudes, **equal grid-point weights** |
| Annual stripes | **Equal weight for the 12 monthly samples** in each year |
| Comparison | Maximum absolute difference ≤ 0.0003°C, relative tolerance 0; coordinates and calendar labels agree |

The map and annual series deliberately use different time weights. This follows
`climate_statistics(period: full)` and `annual_statistics` in the updated
ESMValTool recipe. Replacing both with the same averaging operator changes the task.
The shared input check verifies matching grid, calendar and model/member metadata,
complete months, full calendar-month time bounds and finite input values.
'''
validate='''subprocess.run([sys.executable, "scripts/compare_updated_workflows.py", str(RUN)], check=True)
report = json.loads((RUN / "updated_validation.json").read_text())
assert report["passed"]
print("Maximum absolute difference (°C):", max(row["max_absolute_difference_degC"] for row in report["comparisons"].values()))
print("Ten product comparisons passed; inspect the report for coordinate, baseline and annual checks.")'''
figure='''display(Image(filename=str(RUN / "updated_comparison.png")))'''

seminar=[
md('''# Climate-data processing with CDO and NCO
### Two independent command-line routes — Yiwen Li / Fresh Eyes on CMIP

**20-minute prepared demonstration · updated 9 November 2026**

Updated reference: [Evgenia Galytska's ESMValTool recipe](https://github.com/egalytska/Fresh_eyes/blob/040b9c7962355b1f8fa1312b7af867b458102b85/ESMValTool/recipe_temperature_anomalies.yml).
The [original Python workshop by Abhnil](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop)
provides the broader climate-data processing context.

**Default: real ACCESS-CM2 historical + SSP5-8.5 output.** Both source files are
cached during the Binder build and are already staged on the prepared Mac.
The data mode is printed below and on the final figure. Missing real files
stop execution; the notebook never substitutes synthetic data.

For an offline software test, explicitly choose `WORKSHOP_MODE=synthetic`.

**No Python knowledge is needed for this lesson.** Follow the visible CDO/NCO
commands and their results. Setup, the independent Python reference, checks and
plotting code are folded to keep the lesson focused; their outputs remain visible.

Run every cell from top to bottom with **Shift+Enter**, including folded cells,
or use **Run All**. Do not delete the folded cells. Click their ellipsis to reveal
the code if you want to inspect it. Keep each `%%bash` header.
'''),
md('''## 01 · Our data — already prepared (0:00–1:00)

| Our data | What we use |
|---|---|
| Model variable | ACCESS-CM2 monthly near-surface air temperature |
| Historical file | 1850–2014 |
| Future file | SSP5-8.5, 2015–2100 |
| Today's analysis | 1979–2024: 552 months |
| Monthly reference | 1981–2010 |

**Presenter:** run the folded setup once before the talk. It selects the prepared
files and creates a fresh results folder. Participants can simply run the cell;
no Python editing is needed. The output confirms the data and analysis period.
The full scenario to 2100 is an optional later exercise.
'''),code(setup, backstage=True),md(contract),code(check, backstage=True),
md('''## 03 · Reference result (prepared before the talk)

An independent Python calculation provides the reference for our numerical
checks. Its code runs backstage from the same raw files, using the definitions
above. CDO and NCO each process those raw files themselves. Run this folded cell
and check the completion message; we will focus on the command-line routes next.
'''),code('''subprocess.run([sys.executable, "scripts/run_python_updated.py", str(HIST), str(FUTURE), str(RUN / "python"), "--end-year", str(END_YEAR)], check=True)''', backstage=True),
md('''## 04 · CDO-only route (2:00–8:00)

| Command | Meaning |
|---|---|
| `selyear` → `mergetime` | Select the two experiment segments and join their months |
| `subc,273.15` | Convert Kelvin to Celsius |
| `selyear,1981/2010` → `ymonmean` | Create the 12 monthly reference fields |
| `ymonsub` | Subtract the field for the corresponding calendar month |
| `timsum -muldpm` divided by summed month lengths | Compute the duration-weighted mean map |
| `sellonlatbox,0,360,65,90` → `fldmean,weights=false` | Select the Arctic and average grid points equally |
| `yearmean` | Average the 12 monthly Arctic anomalies equally |

Read chained CDO operators from right to left. `-O` replaces generated outputs;
`-b F64` requests double precision. Each run has its own output folder.
'''),code('''%%bash
set -euo pipefail
bash scripts/run_cdo_updated.sh "$DEMO_HIST" "$DEMO_FUTURE" "$DEMO_OUT/cdo" "$DEMO_END"'''),
md('''### Inspect one CDO step

The climatology has 12 fields, one per month; it is not a single reference mean.
The command below inspects the CDO result and changes no data.
'''),code('''%%bash
set -euo pipefail
cdo -s ntime "$DEMO_OUT/cdo/climatology.nc"
cdo -s showyear "$DEMO_OUT/cdo/arctic_annual.nc"'''),
md('''## 05 · NCO-only route (8:00–14:00)

| Command | Meaning |
|---|---|
| `ncks` → `ncrcat` | Select historical/future records and concatenate them |
| `ncap2` | Convert units and subtract the matching monthly reference |
| `ncwa -d time,m,359,12` | Average one reference month across 30 years |
| `ncecat` | Assemble the 12 separate reference fields |
| `ncwa` with `time_bnds` duration weights | Create the weighted mean map |
| `ncwa -a lat,lon -d lat,65.0,90.0` | Compute an unweighted Arctic monthly series |
| `ncra --mro -d time,,,12,12` | Average consecutive groups of 12 months |

NCO time indices are zero based. January uses 0, 12, …, 348; February starts at
1. This bookkeeping requires January starts and complete consecutive years.
Bash controls loops and filenames; the numerical operations remain in NCO.
No CDO output is read by this route.
'''),code('''%%bash
set -euo pipefail
bash scripts/run_nco_updated.sh "$DEMO_HIST" "$DEMO_FUTURE" "$DEMO_OUT/nco" "$DEMO_END"'''),
md('''## 06 · Numerical comparison (14:00–16:00)

Compare **five products** from each command-line route against Python:
monthly climatology, monthly anomaly fields, mean anomaly map, Arctic monthly
series and annual series. This gives ten product comparisons. The checks also
verify the baseline residual, time coverage, coordinates and equal-month annual
means. Similar-looking figures alone would not establish numerical agreement.
'''),code(validate, backstage=True),
md('''## 07 · Interpret the outputs (16:00–18:30)

Read each row across Python, CDO and NCO. Color limits are shared within the map
row and within the stripe row. The first row is a period-mean anomaly, not a
trend. Real mode is one model realization under historical forcing followed by
SSP5-8.5, not observations. Synthetic mode tests the software only.

These checks establish agreement among the three implementations. A comparison
with Evgenia's saved ESMValTool outputs is a separate verification step.
'''),code(figure, backstage=True),
md('''## 08 · Hands-on practice and saving results (18:30–20:00)

Open [04_monthly_anomaly_hands_on.ipynb](04_monthly_anomaly_hands_on.ipynb).
Change one scientific choice at a time: Arctic boundary, monthly time weights,
or the scenario end year. State which calculation changed before comparing plots.

Your run folder contains each route's NetCDF outputs, `updated_validation.json`
and `updated_comparison.png`. In Binder, download results and your edited notebook
before leaving; the session is temporary. The older 1979–2014 notebooks are
retained with the `legacy_` prefix for provenance.
''')]
save('00_yl_20_minute_binder_demo.ipynb',seminar)

practice=[md('''# Hands-on: choose one definition, predict the effect, then test it
**Yiwen Li · Fresh Eyes on CMIP · updated 9 November 2026**

This notebook runs independently from the seminar notebook. It uses the updated
1979–2024 ESMValTool calculation and starts each route from the same raw data.
**Default inputs are real ACCESS-CM2 historical + SSP5-8.5 output.**
Both source files must be available. The Binder build caches them; the prepared
Mac already has them. For an explicit software test only, choose
`WORKSHOP_MODE=synthetic`. There is no automatic fallback.

No Python knowledge is required. The setup, checks and plotting helpers are
folded; the CDO/NCO command cells and all outputs stay visible. Run folded cells
with **Shift+Enter** or **Run All**, and do not delete them. Click an ellipsis only
if you want to inspect the helper code.
'''),md(contract),code(setup, backstage=True),code(check, backstage=True),
md('''## 1 · Establish the reference result

Run all three independent implementations once. Keep their common baseline,
region and time weights fixed before exploring alternatives.
'''),code('''%%bash
set -euo pipefail
bash scripts/run_updated_workflows.sh "$DEMO_HIST" "$DEMO_FUTURE" "$DEMO_OUT" "$DEMO_END"'''),code(figure, backstage=True),
md('''## 2 · Move the Arctic boundary to 70°N

Prediction: should narrowing the region change the annual anomaly? The answer
depends on the spatial structure of the data. These commands use each route's
own anomaly file. They retain equal grid-point weights and equal monthly weights.
Only the latitude threshold changes.
'''),code('''%%bash
set -euo pipefail
mkdir -p "$DEMO_OUT/exercises"
cdo -O -L -s -b F64 -f nc sellonlatbox,0,360,70,90 \
  "$DEMO_OUT/cdo/anomaly.nc" "$DEMO_OUT/exercises/cdo_arctic_70N.nc"
cdo -O -L -s -b F64 -f nc fldmean,weights=false \
  "$DEMO_OUT/exercises/cdo_arctic_70N.nc" "$DEMO_OUT/exercises/cdo_monthly_70N.nc"
ncwa -O -a lat,lon -d lat,70.0,90.0 \
  "$DEMO_OUT/nco/anomaly.nc" "$DEMO_OUT/exercises/nco_monthly_70N.nc"'''),code('''import numpy as np
import xarray as xr
with xr.open_dataset(RUN / "exercises/cdo_monthly_70N.nc") as a, xr.open_dataset(RUN / "exercises/nco_monthly_70N.nc") as b:
    cdo70 = a.tas_anom.values.squeeze()
    nco70 = b.tas_anom.values.squeeze()
    np.testing.assert_allclose(cdo70, nco70, atol=0.0003, rtol=0)
    print("70°N CDO/NCO maximum difference:", float(abs(cdo70 - nco70).max()), "°C")
with xr.open_dataset(RUN / "cdo/arctic_monthly.nc") as original:
    print("70°N versus 65°N maximum difference:", float(abs(cdo70 - original.tas_anom.values.squeeze()).max()), "°C")''', backstage=True),
md('''## 3 · Change the annual time weights only

`yearmean` gives equal weight to each monthly sample. `yearmonmean` weights
monthly values by the number of days in each month. The latter is a valid
alternative question, but it changes the annual definition in the shared recipe.
Keep the Arctic boundary at 65°N while testing this difference.
'''),code('''%%bash
set -euo pipefail
cdo -O -s -b F64 -f nc yearmonmean "$DEMO_OUT/cdo/arctic_monthly.nc" \
  "$DEMO_OUT/exercises/cdo_annual_monthlength.nc"'''),code('''with xr.open_dataset(RUN / "exercises/cdo_annual_monthlength.nc") as weighted, xr.open_dataset(RUN / "cdo/arctic_annual.nc") as equal:
    difference = weighted.tas_anom.values.squeeze() - equal.tas_anom.values.squeeze()
    print("Annual month-length weighting minus equal-month weighting:")
    print("Maximum absolute change:", float(abs(difference).max()), "°C")
print("The shared recipe's annual result remains the original equal-month product.")''', backstage=True),
md('''## 4 · Check the reference period residual

For each grid point and calendar month, the average anomaly over 1981–2010
should be close to zero. This checks the month matching, not whether all
1979–2024 anomalies average to zero.
'''),code('''%%bash
set -euo pipefail
cdo -O -s -b F64 -f nc selyear,1981/2010 "$DEMO_OUT/cdo/anomaly.nc" \
  "$DEMO_OUT/exercises/baseline_anomaly.nc"
cdo -O -s -b F64 -f nc ymonmean "$DEMO_OUT/exercises/baseline_anomaly.nc" \
  "$DEMO_OUT/exercises/baseline_residual.nc"'''),code('''with xr.open_dataset(RUN / "exercises/baseline_residual.nc") as residual:
    maximum = float(abs(residual.tas_anom).max())
    assert maximum <= 0.0003
    print("PASS: maximum reference-period monthly residual =", maximum, "°C")''', backstage=True),
md('''## Optional extension · Continue the scenario to 2100

Change `WORKSHOP_END_YEAR` (or `END_YEAR` in the setup cell) to `2100`, restart,
and run all cells. Use the same historical 1981–2010 reference, and retain
explicit historical/SSP5-8.5 labeling. This produces 122 annual values, 1979–2100.
It is an extension of the seminar calculation; do not compare its period-mean
map directly with the 1979–2024 reference map as if the definitions were equal.

Save your edited notebook, NetCDF outputs, validation report and figures before
closing a Binder session. All outputs from this run are under the printed path.
''')]
save('04_monthly_anomaly_hands_on.ipynb',practice)
print('Wrote two updated notebooks; earlier notebooks retained as legacy copies.')
