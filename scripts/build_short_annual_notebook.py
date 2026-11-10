"""Build a standalone annual-stripes lesson; preserve the full notebooks."""
from copy import deepcopy
from pathlib import Path
import nbformat as nbf
from notebook_nco_short_cells import NCO_SHORT_STEPS

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


def md(text):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text, tag=None, support=False):
    cell = nbf.v4.new_code_cell(text.strip())
    if tag:
        cell.metadata["tags"] = [tag]
    if support:
        cell.metadata["jupyter"] = {"source_hidden": True}
        cell.metadata["tags"] = ["infrastructure"]
    return cell


def pairs(route, steps, section):
    cells = []
    for number, (title, explanation, command, query) in enumerate(steps, 1):
        assert "\n" not in command and "$" not in command
        assert "\n" not in query and "$" not in query
        cells.extend([
            md(f"### {section}.{number:02d} · {title}\n\n{explanation}"),
            code(command, f"{route}-processing"),
            md("**Inspect the result**"),
            code(query, f"{route}-inspection"),
        ])
    return cells


CDO_SHORT_STEPS = [
    ("Select historical months", "Keep 1979–2014: 432 monthly temperature fields.",
     "cdo selyear,1979/2014 data/historical.nc cdo/historical.nc",
     "cdo ntime cdo/historical.nc"),
    ("Select future months", "Keep 2015–2024 from SSP5-8.5: 120 monthly fields.",
     "cdo selyear,2015/2024 data/ssp585.nc cdo/ssp585.nc",
     "cdo ntime cdo/ssp585.nc"),
    ("Join the experiments", "Join the files in time order. -b F64 retains double precision for the following calculations.",
     "cdo -b F64 mergetime cdo/historical.nc cdo/ssp585.nc cdo/merged.nc",
     "cdo ntime cdo/merged.nc"),
    ("Convert Kelvin values to Celsius", "Subtract 273.15. The next step updates the unit label.",
     "cdo subc,273.15 cdo/merged.nc cdo/celsius_raw.nc",
     "cdo infon -seltimestep,1 cdo/celsius_raw.nc"),
    ("Label the converted values", "Set the unit to degC. The previous command changed the numbers; this command changes their label.",
     "cdo setunit,degC cdo/celsius_raw.nc cdo/celsius.nc",
     "cdo showunit cdo/celsius.nc"),
    ("Select the Arctic", "Select all longitudes and latitude centres from 65°N to 90°N.",
     "cdo sellonlatbox,0,360,65,90 cdo/celsius.nc cdo/arctic.nc",
     "cdo ngridpoints cdo/arctic.nc"),
    ("Average the Arctic grid points", "Give each selected grid point equal weight. The result contains one temperature per month.",
     "cdo fldmean,weights=false cdo/arctic.nc cdo/arctic_monthly.nc",
     "cdo outputtab,date,value -seltimestep,1/3 cdo/arctic_monthly.nc"),
    ("Average each complete year", "Give the twelve monthly samples equal weight. The result contains 46 annual temperatures.",
     "cdo yearmean cdo/arctic_monthly.nc cdo/annual_temperature.nc",
     "cdo ntime cdo/annual_temperature.nc"),
    ("Select the reference years", "The reference contains 30 annual temperatures from 1981 through 2010.",
     "cdo selyear,1981/2010 cdo/annual_temperature.nc cdo/baseline.nc",
     "cdo ntime cdo/baseline.nc"),
    ("Calculate the reference temperature", "Average those 30 years to obtain one reference temperature.",
     "cdo timmean cdo/baseline.nc cdo/reference.nc",
     "cdo output cdo/reference.nc"),
    ("Subtract the reference", "Annual anomaly = annual temperature minus the 1981–2010 reference. Positive values indicate warmer years.",
     "cdo sub cdo/annual_temperature.nc cdo/reference.nc cdo/annual_anomaly.nc",
     "cdo outputtab,date,value -seltimestep,1/5 cdo/annual_anomaly.nc"),
]


def build():
    # Reuse the established input, tool-registration and independent-reference
    # cells without modifying or executing the full notebook.
    full = nbf.read(NOTEBOOKS / "00_yl_20_minute_binder_demo.ipynb", as_version=4)
    support = [deepcopy(c) for c in full.cells if c.cell_type == "code"
               and "infrastructure" in c.metadata.get("tags", [])]
    setup, check, reference = support[:3]
    assert setup.source.startswith("# Select the data")
    assert check.source.startswith("# Check data coverage")
    assert reference.source.startswith("# Calculate the independent reference")
    setup.source = setup.source.replace('"ncrename", "ncwa"):', '"ncrename", "ncwa", "ncdiff"):')
    setup.source = setup.source.replace('"updated_" + DATA_MODE', '"short_annual_" + DATA_MODE')
    cells = [
        md('''# Annual climate stripes with CDO and NCO
### Yiwen Li · Fresh Eyes on CMIP

Start from **ACCESS-CM2 historical + SSP5-8.5** monthly temperature and calculate
the **annual Arctic temperature anomaly for 1979–2024**, relative to **1981–2010**.
Each processing command is followed by a short query that shows its result.

This lesson compares the final annual series and stripes. The
[complete workflow](00_yl_20_minute_binder_demo.ipynb) and
[hands-on notebook](04_monthly_anomaly_hands_on.ipynb) also calculate the twelve
monthly reference fields, monthly anomalies and the duration-weighted map.
The shared definitions follow
[Evgenia's recipe](https://github.com/egalytska/Fresh_eyes/blob/040b9c7962355b1f8fa1312b7af867b458102b85/ESMValTool/recipe_temperature_anomalies.yml).
'''),
        md('''## 01 · Data and calculation

| Item | Choice |
|---|---|
| Input | ACCESS-CM2 monthly near-surface temperature (`tas`, Kelvin) |
| Analysis | 1979–2024: 552 months, 46 complete years |
| Region | Latitude centres 65–90°N, all longitudes |
| Spatial mean | Equal weight for every selected grid point |
| Annual mean | Equal weight for each of the twelve monthly samples |
| Reference | Mean of the 30 annual temperatures in 1981–2010 |

**Annual anomaly = annual temperature − reference temperature.**

With complete calendar years and these fixed weights, this gives the same
annual result as calculating twelve monthly reference fields, subtracting the
matching reference from every month, and then averaging each year. It does not
produce the individual monthly anomaly fields or the weighted map.

Run the next cells with **Shift+Enter**, including collapsed cells. The data
cell creates a fresh results folder with `data/`, `cdo/` and `nco/` directories.
The same command text can be used in a terminal in that results folder.
'''), setup, check,
        md('''## 02 · Independent reference

The reference calculation uses the complete monthly-anomaly method. We will
check that the shorter annual calculation gives the same 46 annual values.
'''), reference,
        md('''## 03 · CDO

Read each command as an operation on an input file that writes an output file.
Run the next query to inspect the result before continuing.
'''),
        *pairs("cdo", CDO_SHORT_STEPS, "03"),
        md('''## 04 · NCO

NCO starts from the same original inputs. It selects variables and dates,
joins records, computes means and subtracts the reference temperature.
'''),
        *pairs("nco", NCO_SHORT_STEPS, "04"),
        md('''## 05 · Compare the annual series

Check all 46 annual anomalies against the independent monthly-anomaly reference.
The comparison also checks the annual temperatures, 1981–2010 reference and
near-zero mean anomaly during that reference period. This is an annual-result
comparison; the full notebooks contain the five-product comparison.
'''),
        code('''subprocess.run([sys.executable, str(ROOT / "scripts/compare_short_annual.py"), str(RUN)], check=True)
report = json.loads((RUN / "short_validation.json").read_text())
assert report["passed"]
print("Both annual series passed; 46 years per route.")''', support=True),
        md('''## 06 · Read the stripes

The same color scale is used for all three routes. Each stripe represents one
annual Arctic temperature anomaly. Positive values are warmer than 1981–2010.
These are results from one model realization, not observations.
'''),
        code('display(Image(filename=str(RUN / "short_comparison.png")))', support=True),
        md('''## Continue with monthly fields

Use the [complete hands-on workflow](04_monthly_anomaly_hands_on.ipynb) for
monthly reference fields, monthly anomalies, a duration-weighted map and
experiments with the Arctic boundary or annual weighting.

Download your edited notebook and results before closing a Binder session.
'''),
    ]
    output = NOTEBOOKS / "05_annual_stripes_short_demo.ipynb"
    nb = nbf.v4.new_notebook(cells=cells, metadata=deepcopy(full.metadata))
    if output.exists():
        old = nbf.read(output, as_version=4)
        if len(old.cells) == len(nb.cells):
            for before, after in zip(old.cells, nb.cells):
                if before.cell_type == after.cell_type:
                    after.id = before.id
    nbf.validate(nb)
    nbf.write(nb, output)
    print(f"Wrote {output.name}: {len(CDO_SHORT_STEPS)} CDO + {len(NCO_SHORT_STEPS)} NCO commands.")


if __name__ == "__main__":
    build()
