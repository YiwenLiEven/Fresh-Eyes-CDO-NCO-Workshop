#!/usr/bin/env python3
"""Download the organizer's real inputs; never substitute synthetic data.

The scenario uses GitHub's canonical raw-content URL at the pinned commit.
Transient HTTP/network failures receive at most four total attempts, separated
by 2, 4 and 8 seconds. Each attempt rewrites the partial file. Permanent HTTP
errors and NetCDF/hash validation failures stop immediately. Existing verified
inputs are reused, and partial downloads never replace them.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import time
import urllib.error
import urllib.request

COMMIT = '040b9c7962355b1f8fa1312b7af867b458102b85'
HIST = 'tas_Amon_ACCESS-CM2_historical_r1i1p1f1_gn_185001-201412.nc'
FUT = 'tas_Amon_ACCESS-CM2_ssp585_r1i1p1f1_gn_201501-210012.nc'
ASSETS = [
    (HIST, 'https://nc.uni-bremen.de/index.php/s/jRtQpitqdTD5fEc/download',
     '3e106e8430f04cd2b260a7230b1e461ccebdda338d09e3f07e8497678c5c6f0f'),
    (FUT, f'https://raw.githubusercontent.com/egalytska/Fresh_eyes/{COMMIT}/{FUT}',
     '8f0d0cee4c370c0c30acc31ef6bf03a2592ee3dfd827a13e37716cd7484909b1'),
]
HASH_PROVENANCE = {
    HIST: ('SHA-256 retained from the previously validated local workshop asset '
           'manifest; an independent publisher checksum was not supplied.'),
    FUT: ('SHA-256 measured from the user-downloaded source file on 2026-11-09; '
          'an independent publisher checksum was not supplied.'),
}
TRANSIENT_HTTP_STATUS = frozenset({408, 429, 500, 502, 503, 504})


def download(url, partial, *, opener=urllib.request.urlopen, sleep=time.sleep):
    """Transfer to a partial path; validation and final acceptance happen later."""
    partial = Path(partial)
    delays = (2, 4, 8)
    for attempt in range(4):
        try:
            with opener(url, timeout=60) as response, partial.open('wb') as stream:
                shutil.copyfileobj(response, stream)
            return
        except urllib.error.HTTPError as error:
            if error.code not in TRANSIENT_HTTP_STATUS or attempt == 3:
                raise
            reason = f'HTTP {error.code}'
        except (urllib.error.URLError, TimeoutError) as error:
            if attempt == 3:
                raise
            reason = type(error).__name__
        delay = delays[attempt]
        print(f'Transient {reason}; retry {attempt+2}/4 in {delay} seconds.', flush=True)
        sleep(delay)

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir', default='data/access_cm2')
    p.add_argument('--historical-file', type=Path, help='Reuse an existing raw historical file')
    args = p.parse_args()
    dest = Path(args.output_dir)
    dest.mkdir(parents=True, exist_ok=True)
    receipts = []
    for name, url, expected in ASSETS:
        target = dest / name
        if not target.exists():
            partial = target.with_suffix('.nc.part')
            if name == HIST and args.historical_file:
                shutil.copyfile(args.historical_file, partial)
            else:
                print(f'Downloading real ACCESS-CM2 data: {name}', flush=True)
                download(url, partial)
            # Reject HTML error pages and incomplete/non-NetCDF transfers before accepting.
            import netCDF4
            with netCDF4.Dataset(partial) as ds:
                if 'tas' not in ds.variables:
                    raise ValueError(f'No tas in {name}')
            if expected and digest(partial) != expected:
                raise ValueError(f'SHA-256 mismatch: {partial}')
            partial.replace(target)
        sha = digest(target)
        if expected and sha != expected:
            raise ValueError(f'SHA-256 mismatch: {target}')
        receipts.append(dict(file=name, source=url, sha256=sha, bytes=target.stat().st_size,
                             pinned_hash_verified=bool(expected),
                             independent_upstream_hash_verified=False,
                             hash_provenance=HASH_PROVENANCE[name]))
    (dest / 'download_receipt.json').write_text(json.dumps(dict(source_commit=COMMIT, assets=receipts), indent=2)+'\n')
    print('Real input files ready. Run the input-contract check before processing.')

if __name__ == '__main__':
    main()
