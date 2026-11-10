"""Record the new real-data build and retain clearly separated legacy evidence."""

import hashlib
import importlib.metadata
import json
import platform
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REFERENCE_COMMIT = '040b9c7962355b1f8fa1312b7af867b458102b85'
SHORT_NOTEBOOK = '05_annual_stripes_short_demo'


def checked_real_validation(path, annual_only=False):
    evidence = json.loads(path.read_text())
    assert evidence['passed'], f'Validation failed: {path}'
    assert evidence['input']['source_id'] == 'ACCESS-CM2'
    assert evidence['input']['synthetic'] is False
    assert evidence['input']['period'] == '1979-2024'
    assert evidence['input']['months'] == 552 and evidence['input']['years'] == 46
    if annual_only:
        assert set(evidence['comparisons']) == {'cdo', 'nco'}
        assert all(item['years'] == 46 and item['annual_temperature_and_subtraction_checked']
                   for item in evidence['comparisons'].values())
        assert evidence['cdo_annual_bounds_full_year'] is True
        assert evidence['nco_output_metadata']
        assert evidence['conditions']['complete_months_and_finite_grid'] is True
        assert evidence['conditions']['equal_month_annual_weights'] is True
        assert evidence['conditions']['equal_grid_weights_65_to_90N'] is True
        assert evidence['conditions']['baseline'] == '1981-2010'
    else:
        assert len(evidence['comparisons']) == 10
    assert all(item['passed'] for item in evidence['comparisons'].values())
    return evidence


def checked_notebook(name):
    source_path = Path('notebooks') / f'{name}.ipynb'
    executed_path = Path('outputs/executed') / f'{name}.ipynb'
    source = json.loads(source_path.read_text())
    executed = json.loads(executed_path.read_text())
    expected_cells = [c for c in source['cells'] if c['cell_type'] == 'code']
    code_cells = [c for c in executed['cells'] if c['cell_type'] == 'code']
    assert len(code_cells) == len(expected_cells) > 0
    assert [''.join(c['source']) for c in code_cells] == [''.join(c['source']) for c in expected_cells]
    counts = [c.get('execution_count') for c in code_cells]
    assert counts == list(range(1, len(code_cells)+1)), f'Unexecuted or out-of-order cells: {name}'
    assert not any(o.get('output_type') == 'error' for c in code_cells for o in c.get('outputs', []))
    streams = '\n'.join(''.join(o.get('text', [])) for c in code_cells
                        for o in c.get('outputs', []) if o.get('output_type') == 'stream')
    assert 'DATA MODE: REAL ACCESS-CM2: historical + SSP5-8.5' in streams
    assert 'Analysis: 1979–2024 | Monthly reference: 1981–2010' in streams
    match = re.search(r'^Outputs:\s*(.+)$', streams, flags=re.MULTILINE)
    assert match, f'No run directory printed by {name}'
    run = Path(match.group(1).strip())
    assert run.resolve().is_relative_to(Path('outputs').resolve())
    annual_only = name == SHORT_NOTEBOOK
    validation_path = run / ('short_validation.json' if annual_only else 'updated_validation.json')
    validation = checked_real_validation(validation_path, annual_only=annual_only)
    return {
        'data_mode': 'real', 'analysis_period': validation['input']['period'],
        'code_cell_count': len(code_cells), 'execution_counts': counts,
        'all_code_cells_executed': True, 'error_outputs': 0,
        'source_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'executed_sha256': hashlib.sha256(executed_path.read_bytes()).hexdigest(),
        'run_validation_file': validation_path.as_posix(),
        'run_validation_passed': True,
        'validation_scope': 'annual_arctic_series' if annual_only else 'five_products',
        'run_validation': validation,
    }


def main():
    main_path = Path('outputs/updated_real_build/updated_validation.json')
    report = {
        'completed_utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(),
        'packages': {p: importlib.metadata.version(p) for p in ('xarray', 'numpy', 'netCDF4', 'nbconvert')},
        'tools': {}, 'shared_reference_commit': REFERENCE_COMMIT,
        'data_mode': 'real', 'analysis_period': '1979-2024',
        'main_evidence_file': main_path.as_posix(),
        'independent_workflow_validation': checked_real_validation(main_path),
        'comparison_scope': 'Three independent Python/CDO/NCO routes; not an upstream ESMValTool rerun.',
        'legacy': {
            'analysis_period': '1979-2014', 'data_mode': 'synthetic',
            'shared_reference_commit': '393cfcf876fa47c6c231c3be70dbd9f8552fe3a3',
            'independent_workflow_validation': json.loads(Path('outputs/demo/monthly/three_way_validation.json').read_text()),
        },
    }
    for tool, args in {'cdo': ['-V'], 'ncks': ['--version']}.items():
        result = subprocess.run([tool, *args], check=True, text=True, capture_output=True)
        report['tools'][tool] = (result.stdout + result.stderr).strip()
    report['notebooks'] = {name: checked_notebook(name) for name in
                           ('00_yl_20_minute_binder_demo', '04_monthly_anomaly_hands_on', SHORT_NOTEBOOK)}
    report['notebooks_executed'] = True
    Path('outputs/verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: outputs/verification.json records real 1979–2024 data, full five-product checks, short annual-series checks and every code cell in all three notebooks.')


if __name__ == '__main__':
    main()
