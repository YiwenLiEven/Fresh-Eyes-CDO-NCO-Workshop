"""Compact only this successful Binder build's explicitly verified outputs.

Run after write_verification_report.py. Raw inputs and historical output folders
are outside the deletion plan. Symlink files are unlinked, never followed.
"""
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ('python', 'cdo', 'nco')
PRODUCTS = ('climatology', 'anomaly', 'map_mean', 'arctic_monthly', 'arctic_annual')
SHORT_NOTEBOOK = '05_annual_stripes_short_demo'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bounded_path(relative):
    """Accept repo-relative outputs paths with no symlink ancestors."""
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and '..' not in pure.parts,
            f'Unsafe output path: {relative}')
    require(len(pure.parts) >= 2 and pure.parts[0] == 'outputs',
            f'Path is outside outputs: {relative}')
    current = ROOT
    for part in pure.parts:
        current = current / part
        require(not current.is_symlink(), f'Symlink ancestor is not permitted: {relative}')
    require(current.resolve().is_relative_to((ROOT / 'outputs').resolve()),
            f'Path escaped outputs: {relative}')
    return current


def read_validation(relative, synthetic, annual_only=False):
    path = bounded_path(relative)
    data = json.loads(path.read_text())
    require(data.get('passed') is True, f'Unverified run: {relative}')
    require(data['input']['synthetic'] is synthetic, f'Unexpected data mode: {relative}')
    require(data['input']['period'] == '1979-2024', f'Unexpected period: {relative}')
    expected_comparisons = 2 if annual_only else 10
    require(len(data['comparisons']) == expected_comparisons and
            all(item.get('passed') is True for item in data['comparisons'].values()),
            f'Incomplete comparisons: {relative}')
    if annual_only:
        require(set(data['comparisons']) == {'cdo', 'nco'} and
                all(item.get('years') == 46 for item in data['comparisons'].values()),
                f'Incomplete annual-series comparisons: {relative}')
    return path.parent


def walk_files(directory):
    """List files without traversing symlink directories; reject such directories."""
    for base, directories, files in os.walk(directory, followlinks=False):
        base = Path(base)
        for name in directories:
            require(not (base / name).is_symlink(),
                    f'Symlink directory found inside generated output: {base / name}')
        for name in files:
            path = base / name
            kind = path.lstat().st_mode
            require(stat.S_ISREG(kind) or stat.S_ISLNK(kind),
                    f'Unexpected special file: {path}')
            yield path


def main():
    verification = json.loads(bounded_path('outputs/verification.json').read_text())
    require(verification.get('data_mode') == 'real' and
            verification.get('analysis_period') == '1979-2024' and
            verification.get('notebooks_executed') is True,
            'A completed real-data verification report is required')
    require(verification.get('main_evidence_file') ==
            'outputs/updated_real_build/updated_validation.json',
            'Unexpected main build evidence location')
    main_run = read_validation(verification['main_evidence_file'], synthetic=False)
    synthetic_run = read_validation('outputs/updated_build/updated_validation.json', synthetic=True)
    expected_notebooks = {'00_yl_20_minute_binder_demo', '04_monthly_anomaly_hands_on', SHORT_NOTEBOOK}
    require(set(verification['notebooks']) == expected_notebooks,
            'Expected both full notebooks and the verified short annual notebook')

    # Validate the entire plan before deleting anything.
    notebook_runs = set()
    for name, evidence in verification['notebooks'].items():
        require(evidence.get('run_validation_passed') is True and
                evidence.get('all_code_cells_executed') is True and
                evidence.get('error_outputs') == 0 and evidence.get('data_mode') == 'real',
                f'Notebook is not fully verified: {name}')
        relative = evidence['run_validation_file']
        annual_only = name == SHORT_NOTEBOOK
        pattern = (r'outputs/short_annual_real_\d{8}T\d{6}_[0-9a-f]{6}/short_validation\.json'
                   if annual_only else
                   r'outputs/updated_real_\d{8}T\d{6}_[0-9a-f]{6}/updated_validation\.json')
        require(re.fullmatch(pattern, relative),
                f'Unexpected notebook output location: {relative}')
        run = read_validation(relative, synthetic=False, annual_only=annual_only)
        figure = run / ('short_comparison.png' if annual_only else 'updated_comparison.png')
        require(figure.is_file() and not figure.is_symlink(),
                f'Missing comparison figure: {relative}')
        notebook_runs.add(run)

    notebook_files = []
    for run in sorted(notebook_runs):
        notebook_files.extend(p for p in walk_files(run) if p.suffix == '.nc')

    keep = [main_run / route / f'{product}.nc' for route in ROUTES for product in PRODUCTS]
    for path in keep:
        checked = bounded_path(path.relative_to(ROOT).as_posix())
        require(checked.is_file(), f'Missing final main-run product: {checked}')

    work_directories = []
    for run in (main_run, synthetic_run):
        for route in ROUTES:
            work = bounded_path((run / route / 'work').relative_to(ROOT).as_posix())
            if work.exists():
                require(work.is_dir(), f'Expected generated work directory: {work}')
                list(walk_files(work))  # Validate symlinks and file types now.
                work_directories.append(work)
    require(shutil.rmtree.avoids_symlink_attacks,
            'This cleanup requires Python symlink-safe rmtree support')

    removed_bytes = sum(p.lstat().st_size for p in notebook_files)
    for directory in work_directories:
        removed_bytes += sum(p.lstat().st_size for p in walk_files(directory))
    for path in notebook_files:
        path.unlink()  # Includes raw-input symlinks, never their targets.
    for directory in work_directories:
        shutil.rmtree(directory)

    require(all(p.is_file() for p in keep), 'A retained main product is missing')
    receipt = {
        'notebook_runs_compacted': [p.relative_to(ROOT).as_posix() for p in sorted(notebook_runs)],
        'notebook_netcdf_files_removed': len(notebook_files),
        'work_directories_removed': [p.relative_to(ROOT).as_posix() for p in work_directories],
        'bytes_removed_including_symlink_entries': removed_bytes,
        'main_final_netcdf_files_retained': [p.relative_to(ROOT).as_posix() for p in keep],
        'raw_inputs_preserved': True,
        'reports_figures_and_executed_notebooks_preserved': True,
    }
    (ROOT / 'outputs/binder_compaction.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Binder compaction complete: {removed_bytes / 1024**3:.2f} GiB of generated intermediates removed.')


if __name__ == '__main__':
    main()
