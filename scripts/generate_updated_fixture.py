"""Small deterministic historical/SSP585-shaped SOFTWARE TEST, not climate data."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr


def generate(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    for experiment,first,last in [('historical','1979-01-01','2014-12-01'),('ssp585','2015-01-01','2100-12-01')]:
        starts=pd.date_range(first,last,freq='MS'); ends=starts+pd.offsets.MonthBegin(1)
        time=starts+(ends-starts)/2
        lat=np.arange(-87.5,90,5.);lon=np.arange(2.5,360,10.)
        t=(time.year.to_numpy()-1979)+(time.month.to_numpy()-.5)/12
        m=time.month.to_numpy()
        # Month-dependent trend makes a mistaken equal-month MAP detectably wrong.
        pattern=1+0.6*np.sin(np.deg2rad(lat))[None,:,None]+0.2*np.cos(np.deg2rad(lon))[None,None,:]
        v=273.15+12-30*np.sin(np.deg2rad(lat))[None,:,None]**2+np.cos(np.deg2rad(lon))[None,None,:]+(0.03*t+0.03*t*np.sin(m))[...,None,None]*pattern+6*np.sin(m/12*2*np.pi)[...,None,None]
        ds=xr.Dataset({'tas':(('time','lat','lon'),v.astype('float32')),
                       'time_bnds':(('time','bnds'),np.stack([starts.values,ends.values],axis=1))},
                      coords={'time':time,'lat':lat,'lon':lon},
                      attrs={'Conventions':'CF-1.8','title':'SYNTHETIC SOFTWARE TEST: not ACCESS-CM2',
                             'source_id':'WORKSHOP-DEMO','experiment_id':experiment,'variant_label':'r1i1p1f1','grid_label':'gn','table_id':'Amon'})
        ds.tas.attrs.update(units='K',standard_name='air_temperature')
        ds.time.attrs.update(standard_name='time',axis='T',bounds='time_bnds')
        ds.lat.attrs.update(units='degrees_north',standard_name='latitude',axis='Y')
        ds.lon.attrs.update(units='degrees_east',standard_name='longitude',axis='X')
        for name in ['time','time_bnds']:
            ds[name].encoding.update(units='days since 1850-01-01',calendar='proleptic_gregorian',dtype='float64',_FillValue=None)
        ds.to_netcdf(out/(experiment+'.nc'),format='NETCDF3_64BIT',unlimited_dims=['time'])
    print(f'Synthetic software fixture: {out}')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');generate(p.parse_args().output)
