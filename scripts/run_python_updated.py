"""Independent xarray implementation of the updated ESMValTool definitions."""
import argparse
from pathlib import Path
import json
import xarray as xr
from check_updated_inputs import validate


def run(hist,future,out,end_year):
    info=validate(hist,future,end_year)
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    decoder=xr.coders.CFDatetimeCoder(use_cftime=True)
    with xr.open_dataset(hist,decode_times=decoder) as h, xr.open_dataset(future,decode_times=decoder) as f:
        # Select before loading: this seminar uses 1979–2024, not all of SSP585.
        tas=xr.concat([h.tas.sel(time=slice('1979','2014')),f.tas.sel(time=slice('2015',str(end_year)))],dim='time').astype('float64').load()-273.15
        climatology=tas.sel(time=slice('1981','2010')).groupby('time.month').mean('time')
        anomaly=tas.groupby('time.month')-climatology
        anomaly=anomaly.drop_vars('month')
        days=anomaly.time.dt.days_in_month.astype('float64')
        mean_map=anomaly.weighted(days).mean('time')
        arctic=anomaly.sel(lat=slice(65,90)).mean('lon').mean('lat')
        annual=arctic.groupby('time.year').mean('time')
        for name,field in [('climatology',climatology),('anomaly',anomaly),('map_mean',mean_map),('arctic_monthly',arctic),('arctic_annual',annual)]:
            field.name='tas_anom' if name!='climatology' else 'tas'
            field.attrs={'units':'degC','anomaly_reference_period':'1981-2010'}
            data=field.to_dataset(); data.attrs.update(source_id=info['source_id'],analysis_period=info['period'])
            data.to_netcdf(out/(name+'.nc'),format='NETCDF4',encoding={field.name:{'zlib':True,'complevel':2}})
    (out/'input_contract.json').write_text(json.dumps(info,indent=2)+'\n')
    print(f'Python complete: {out}')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('historical');p.add_argument('future');p.add_argument('output');p.add_argument('--end-year',type=int,default=2024)
    a=p.parse_args();run(a.historical,a.future,a.output,a.end_year)
