"""Read-only contract for the updated historical + SSP585 demonstration."""
import argparse
import json
from pathlib import Path
import numpy as np
import xarray as xr


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inspect(path, start, end):
    with xr.open_dataset(path, decode_times=xr.coders.CFDatetimeCoder(use_cftime=True)) as ds:
        require(ds.tas.dims == ('time', 'lat', 'lon'), 'Expected tas(time,lat,lon)')
        require(ds.tas.attrs.get('units') == 'K', 'Input tas must be Kelvin')
        months = ds.time.dt.year.values * 12 + ds.time.dt.month.values
        require(np.all(np.diff(months) == 1), 'Missing, duplicated or unordered months')
        require(ds.time.dt.month.values[0] == 1 and ds.time.dt.month.values[-1] == 12,
                'Each raw input must contain complete January–December years')
        selected = ds.sel(time=slice(str(start), str(end)))
        require(selected.sizes['time'] == (end-start+1)*12, f'Missing required {start}–{end} coverage')
        for name in ('lat', 'lon'):
            v = ds[name].values
            require(v.ndim == 1 and len(v) > 1 and np.all(np.diff(v)>0), f'{name} must increase')
            require(np.allclose(np.diff(v), np.diff(v)[0]), 'Regular grid required')
        require(float(ds.lon.min()) >= 0 and float(ds.lon.max()) < 360, 'Expected 0 <= lon < 360')
        require(bool(((ds.lat>=65)&(ds.lat<=90)).any()), 'No Arctic cells')
        require(bool(np.isfinite(selected.tas).all()), 'Missing/nonfinite tas is unsupported')
        bname = ds.time.attrs.get('bounds')
        require(bname in ds, 'Explicit monthly time bounds required')
        bounds = selected[bname].values
        require(bounds.shape == (selected.sizes['time'], 2), 'Expected time bounds (time,2)')
        for t, (lo, hi) in zip(selected.time.values, bounds):
            expected_hi = (t.year+1, 1) if t.month==12 else (t.year, t.month+1)
            require((lo.year,lo.month,lo.day,lo.hour,lo.minute,lo.second)==(t.year,t.month,1,0,0,0),
                    'Bounds must start at first day of each calendar month')
            require((hi.year,hi.month,hi.day,hi.hour,hi.minute,hi.second)==(*expected_hi,1,0,0,0),
                    'Bounds must end at first day of next calendar month')
        return dict(path=str(Path(path).resolve()), lat=ds.lat.values, lon=ds.lon.values,
                    calendar=ds.time.encoding.get('calendar','standard'),
                    time_units=ds.time.encoding.get('units'), bounds=bname,
                    first_month=int(months[0]), last_month=int(months[-1]),
                    attrs={k:ds.attrs.get(k) for k in ['source_id','variant_label','grid_label','table_id','experiment_id']})


def validate(hist, future, end_year=2024):
    require(2015<=end_year<=2100, 'End year must be between 2015 and 2100')
    h, f = inspect(hist,1979,2014), inspect(future,2015,end_year)
    require(h['last_month']==2014*12+12 and f['first_month']==2015*12+1,
            'Historical must end Dec 2014 and SSP585 start Jan 2015')
    for name in ['lat','lon']:
        require(np.array_equal(h[name],f[name]), f'Incompatible {name} grid; regridding is outside this example')
    for name in ['calendar','time_units','bounds']:
        require(h[name]==f[name], f'{name} must match across inputs for direct NCO concatenation')
    for key in ['source_id','variant_label','grid_label','table_id']:
        require(h['attrs'][key] is not None and h['attrs'][key]==f['attrs'][key], f'Missing/mismatched {key}')
    require(h['attrs']['source_id'] in ('ACCESS-CM2','WORKSHOP-DEMO'), 'Expected ACCESS-CM2 or explicitly labelled WORKSHOP-DEMO inputs')
    require(h['attrs']['experiment_id']=='historical' and f['attrs']['experiment_id']=='ssp585',
            'Expected historical and ssp585 experiment labels')
    require(h['bounds']=='time_bnds', 'This teaching NCO script expects the CF bounds variable time_bnds')
    return {'source_id':h['attrs']['source_id'],'variant_label':h['attrs']['variant_label'],
            'period':f'1979-{end_year}','baseline':'1981-2010','months':(end_year-1979+1)*12,
            'years':end_year-1979+1,'calendar':h['calendar'],'time_units':h['time_units'],
            'synthetic':h['attrs']['source_id']=='WORKSHOP-DEMO'}


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('historical'); p.add_argument('future'); p.add_argument('--end-year',type=int,default=2024)
    a=p.parse_args(); print(json.dumps(validate(a.historical,a.future,a.end_year),indent=2))
