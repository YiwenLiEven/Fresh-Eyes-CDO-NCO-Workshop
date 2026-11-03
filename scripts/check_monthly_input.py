"""Read-only shared input contract. This does not produce processed data."""
import sys
import numpy as np
import xarray as xr

with xr.open_dataset(sys.argv[1]) as ds:
    a=ds.tas
    assert a.dims==('time','lat','lon'), 'Expected tas(time,lat,lon)'
    assert a.attrs.get('units')=='K', 'These scripts expect Kelvin input'
    months=ds.time.dt.year.values*12+ds.time.dt.month.values
    assert np.all(np.diff(months)==1), 'Missing or duplicate months'
    assert ds.time.dt.month.values[0]==1 and ds.time.dt.month.values[-1]==12
    for start,end,count in [('1979','2014',432),('1981','2010',360)]:
        assert ds.sel(time=slice(start,end)).sizes['time']==count
    assert (ds.lat.values[1:]>ds.lat.values[:-1]).all()
    assert ds.lat.where((ds.lat>=65)&(ds.lat<=90),drop=True).size>0
    assert np.allclose(np.diff(ds.lat),np.diff(ds.lat)[0])
    assert np.allclose(np.diff(ds.lon),np.diff(ds.lon)[0])
    assert float(ds.lon.min())>=0 and float(ds.lon.max())<=360
    assert bool(a.notnull().all()), 'Shared strict fixture contract: no missing tas values'
print('PASS: complete monthly Kelvin input, regular 0-360 grid, no missing values.')
