"""Build the English seminar and participant notebooks for the updated recipe."""
from pathlib import Path
import shutil
import nbformat as nbf
from notebook_cdo_cells import CDO_STEPS
from notebook_nco_cells import NCO_STEPS

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

setup = '''# Select the data and create this run
from pathlib import Path
import os, sys, subprocess, json, uuid
from datetime import datetime, timezone
from IPython.display import display, Image

ROOT = Path.cwd().resolve()
if not (ROOT / "scripts/run_python_updated.py").exists():
    ROOT = ROOT.parent
assert (ROOT / "scripts/run_python_updated.py").exists(), "Open this notebook from the workshop repository."
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
for route in ("cdo", "nco"):
    directory = RUN / route
    (directory / "work").mkdir(parents=True)
    (directory / "historical_input.nc").symlink_to(HIST.resolve())
    (directory / "ssp585_input.nc").symlink_to(FUTURE.resolve())
os.environ.update(DEMO_HIST=os.path.relpath(HIST, ROOT), DEMO_FUTURE=os.path.relpath(FUTURE, ROOT), DEMO_OUT=os.path.relpath(RUN, ROOT), DEMO_END=str(END_YEAR))
print("DATA MODE:", "SYNTHETIC SOFTWARE TEST — NOT ACCESS-CM2" if DATA_MODE == "synthetic" else "REAL ACCESS-CM2: historical + SSP5-8.5")
print("Analysis:", f"1979–{END_YEAR}", "| Monthly reference: 1981–2010")
print("Outputs:", RUN.relative_to(ROOT))
'''
check = '''# Check data coverage and tool versions
_ = subprocess.run([sys.executable, "scripts/check_updated_inputs.py", str(HIST), str(FUTURE), "--end-year", str(END_YEAR)], check=True)
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

The map weights each monthly field by its duration. The annual series gives
each month equal weight. Keeping these definitions the same across tools makes
the numerical comparison meaningful.
'''
validate='''# Compare the three results
subprocess.run([sys.executable, "scripts/compare_updated_workflows.py", str(RUN)], check=True)
report = json.loads((RUN / "updated_validation.json").read_text())
assert report["passed"]
print("Maximum absolute difference (°C):", max(row["max_absolute_difference_degC"] for row in report["comparisons"].values()))
print("Ten product comparisons passed; inspect the report for coordinate, baseline and annual checks.")'''
figure='''# Show the comparison figure
display(Image(filename=str(RUN / "updated_comparison.png")))'''


python_reference = '''# Calculate the independent reference
_ = subprocess.run([sys.executable, "scripts/run_python_updated.py", str(HIST), str(FUTURE), str(RUN / "python"), "--end-year", str(END_YEAR)], check=True, capture_output=True, text=True)
print(f"Reference ready: five products for 1979–{END_YEAR}.")
'''

def command_cells(route, steps, section):
    cells = []
    for number, (title, explanation, commands) in enumerate(steps, 1):
        cells.append(md(f"### {section}.{number:02d} · {title}\n\n{explanation}"))
        cells.append(code(f'%%bash -e\ncd "$DEMO_OUT/{route}"\n\n{commands.strip()}'))
    return cells

shell_intro = '''Each cell below contains the commands it executes. Use **Shift+Enter** to run
one cell and inspect its result before continuing.

- `%%bash -e` runs shell commands and stops the cell if a command fails.
- `cd "$DEMO_OUT/cdo"` or `cd "$DEMO_OUT/nco"` enters that route's result folder.
- `historical_input.nc` and `ssp585_input.nc` are short names for the two original files.
- `$DEMO_END` is 2024; it can be changed for the optional extension.

To repeat the calculation, run from the first cell again to create a new results
folder. The commands write new files without overwrite options.
'''

seminar=[
md('''# Climate-data processing with CDO and NCO
### Yiwen Li · Fresh Eyes on CMIP

Compute temperature anomalies, an Arctic time series and climate stripes from
**ACCESS-CM2 historical + SSP5-8.5 monthly temperature**. Follow the CDO and NCO
commands step by step, then compare their results with an independent Python calculation.

The shared scientific definitions follow
[Evgenia Galytska's ESMValTool recipe](https://github.com/egalytska/Fresh_eyes/blob/040b9c7962355b1f8fa1312b7af867b458102b85/ESMValTool/recipe_temperature_anomalies.yml).
The [original Python workshop by Abhnil](https://github.com/abhnil/Fresh_Eyes_on_CMIP_Data_Workshop)
provides the broader workshop context.

Run the cells in order with **Shift+Enter**, including the collapsed cells.
'''),
md('''## 01 · Data

| Item | Dataset |
|---|---|
| Model variable | ACCESS-CM2 monthly near-surface air temperature (`tas`, Kelvin) |
| Historical file | 1850–2014 |
| Future file | SSP5-8.5, 2015–2100 |
| Analysis period | 1979–2024: 552 months |
| Monthly reference | 1981–2010 |

Run the next cell to select the data and create a new results folder.
'''),code(setup, backstage=True),md(contract),code(check, backstage=True),
md('''## 03 · Reference calculation

The Python reference uses the same raw inputs and definitions. CDO and NCO
will each process the original files independently. At the end, we will compare
five products from each route.
'''),code(python_reference, backstage=True),
md('''## 04 · CDO: from monthly temperature to annual stripes

CDO operators describe the operation applied to a NetCDF file. Most steps below
write one new file, which becomes the input to the next step:
`cdo operation input.nc output.nc`.
'''),md(shell_intro),
*command_cells('cdo', CDO_STEPS, '04'),
md('''## 05 · NCO: the same calculation from the original data

NCO uses separate commands for selecting, concatenating, calculating and
averaging. Follow the filenames from one step to the next. This route reads the
two original files and does not use the CDO results.
'''),
*command_cells('nco', NCO_STEPS, '05'),
md('''## 06 · Compare the results

Check **five products** from each command-line route against Python: monthly
climatology, monthly anomaly fields, mean anomaly map, Arctic monthly series and
annual series. These ten comparisons also check coordinates, the reference-period
residual and the annual definition.
'''),code(validate, backstage=True),
md('''## 07 · Read the figures

Read each row across Python, CDO and NCO. The maps and stripes use shared color
limits. The first row is a period-mean anomaly, not a trend. The inputs are one
model realization under historical forcing followed by SSP5-8.5, not observations.

These checks compare the three implementations. A direct comparison with
Evgenia's saved ESMValTool outputs is a separate check.
'''),code(figure, backstage=True),
md('''## 08 · Try a different region or period

Open [04_monthly_anomaly_hands_on.ipynb](04_monthly_anomaly_hands_on.ipynb).
Change the Arctic boundary, annual time weights or scenario end year, one at a time.

Each run folder contains NetCDF outputs, `updated_validation.json` and
`updated_comparison.png`. Download your results and edited notebook before
closing a Binder session.
''')]
save('00_yl_20_minute_binder_demo.ipynb',seminar)

practice=[md('''# Hands-on: temperature anomalies with CDO and NCO
**Yiwen Li · Fresh Eyes on CMIP**

Use real ACCESS-CM2 historical + SSP5-8.5 data to reproduce the 1979–2024 result,
then change one scientific choice at a time. This notebook runs independently.

Run every cell in order with **Shift+Enter**, including collapsed cells. All CDO
and NCO processing commands are shown below their explanations.
'''),md(contract),code(setup, backstage=True),code(check, backstage=True),
md('''## 1 · Reproduce the common result

Keep the baseline, region and time weights fixed for the first calculation.
The independent reference and both command-line routes start from the raw data.
'''),code(python_reference, backstage=True),md(shell_intro),
md('## 1A · CDO'),*command_cells('cdo', CDO_STEPS, '1A'),
md('## 1B · NCO'),*command_cells('nco', NCO_STEPS, '1B'),
md('## 1C · Compare the three routes'),code(validate, backstage=True),code(figure, backstage=True),
md('''## 2 · Move the Arctic boundary to 70°N

Prediction: should narrowing the region change the annual anomaly? The answer
depends on the spatial structure of the data. These commands use each route's
own anomaly file. They retain equal grid-point weights and equal monthly weights.
Only the latitude threshold changes.
'''),code('''%%bash -e
mkdir -p "$DEMO_OUT/exercises"
cdo sellonlatbox,0,360,70,90 \
  "$DEMO_OUT/cdo/anomaly.nc" "$DEMO_OUT/exercises/cdo_arctic_70N.nc"
cdo fldmean,weights=false \
  "$DEMO_OUT/exercises/cdo_arctic_70N.nc" "$DEMO_OUT/exercises/cdo_monthly_70N.nc"
ncwa -a lat,lon -d lat,70.0,90.0 \
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
'''),code('''%%bash -e
cdo yearmonmean "$DEMO_OUT/cdo/arctic_monthly.nc" \
  "$DEMO_OUT/exercises/cdo_annual_monthlength.nc"'''),code('''with xr.open_dataset(RUN / "exercises/cdo_annual_monthlength.nc") as weighted, xr.open_dataset(RUN / "cdo/arctic_annual.nc") as equal:
    difference = weighted.tas_anom.values.squeeze() - equal.tas_anom.values.squeeze()
    print("Annual month-length weighting minus equal-month weighting:")
    print("Maximum absolute change:", float(abs(difference).max()), "°C")
print("The shared recipe's annual result remains the original equal-month product.")''', backstage=True),
md('''## 4 · Check the reference period residual

For each grid point and calendar month, the average anomaly over 1981–2010
should be close to zero. This checks the month matching, not whether all
1979–2024 anomalies average to zero.
'''),code('''%%bash -e
cdo selyear,1981/2010 "$DEMO_OUT/cdo/anomaly.nc" \
  "$DEMO_OUT/exercises/baseline_anomaly.nc"
cdo ymonmean "$DEMO_OUT/exercises/baseline_anomaly.nc" \
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
print('Wrote two notebooks with inline CDO/NCO commands.')
