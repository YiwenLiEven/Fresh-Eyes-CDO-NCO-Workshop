"""Validate labelled scientific products, then plot with Python only."""
import argparse, json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

PRODUCTS={
 'monthly':'tas_monthly_anomaly_1979_2014.nc',
 'map':'tas_mean_monthly_anomaly_1979_2014.nc',
 'arctic_monthly':'tas_arctic_monthly_anomaly_1979_2014.nc',
 'arctic_annual':'tas_arctic_annual_anomaly_1979_2014.nc',
}
def read(root,route,product):
    with xr.open_dataset(root/route/PRODUCTS[product]) as ds:
        a=ds.tas_anom.squeeze(drop=True).load()
        if 'time' in a.dims:
            if product=='arctic_annual':
                a=a.assign_coords(year=('time',a.time.dt.year.values)).swap_dims({'time':'year'}).drop_vars('time')
            else:
                a=a.assign_coords(time=a.time.dt.year.values*12+a.time.dt.month.values)
        if product=='map': a=a.transpose('lat','lon')
        if product=='monthly': a=a.transpose('time','lat','lon')
        return a

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',default='outputs/demo/monthly');args=p.parse_args()
    root=Path(args.root); tol=3e-4; report={}; arrays={}
    for product in PRODUCTS:
        reference=read(root,'python',product); arrays[product]={'python':reference}
        for route in ['cdo','nco']:
            actual=read(root,route,product)
            reference,actual=xr.align(reference,actual,join='exact')
            assert reference.dims==actual.dims and reference.shape==actual.shape
            np.testing.assert_array_equal(np.isfinite(reference),np.isfinite(actual))
            error=float(abs(actual-reference).max())
            print(f'{route}/{product}: maximum absolute error {error:.12g} degC',flush=True)
            np.testing.assert_allclose(actual,reference,rtol=0,atol=tol,equal_nan=True)
            report[f'{route}_vs_python/{product}']={'max_absolute_difference_degC':error,'absolute_tolerance_degC':tol,'passed':True}
            arrays[product][route]=actual
    for route in ['python','cdo','nco']:
        monthly=arrays['monthly'][route]
        assert monthly.sizes['time']==432
        assert int(monthly.time[0])==1979*12+1 and int(monthly.time[-1])==2014*12+12
        # Monthly baseline must average to zero for each calendar month and cell.
        base=monthly.sel(time=slice(1981*12+1,2010*12+12))
        assert float(abs(base.values.reshape(30,12,*base.shape[1:]).mean(axis=0)).max())<tol
        np.testing.assert_array_equal(arrays['arctic_annual'][route].year,np.arange(1979,2015))
    (root/'three_way_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    fig,axes=plt.subplots(3,3,figsize=(14,8),layout='constrained')
    limit=max(float(abs(arrays['arctic_annual'][r]).max()) for r in ['python','cdo','nco'])
    for col,route in enumerate(['python','cdo','nco']):
        field=arrays['map'][route]
        im=axes[0,col].pcolormesh(field.lon,field.lat,field,vmin=-.2,vmax=.4,cmap='RdBu_r',shading='auto')
        axes[0,col].set(title=f'{route.upper()}: mean anomaly',xlabel='Longitude',ylabel='Latitude')
        # Plain lat/lon axes avoid extra Cartopy downloads in an ephemeral session.
        series=arrays['arctic_monthly'][route]
        axes[1,col].plot(1979+np.arange(432)/12,series,lw=.8)
        axes[1,col].set(title='Arctic monthly anomaly',ylabel='degC',xlabel='Year')
        annual=arrays['arctic_annual'][route]
        axes[2,col].imshow(annual.values[None,:],extent=[1978.5,2014.5,0,1],aspect='auto',cmap='RdBu_r',vmin=-limit,vmax=limit)
        axes[2,col].set(title='Arctic annual stripes',yticks=[],xlabel='Year')
    fig.colorbar(im,ax=axes[0,:],label='degC',shrink=.7)
    fig.suptitle('Same input and definitions; three independent processing routes\nSynthetic teaching data, not observed climate change')
    fig.savefig(root/'three_way_comparison.png',dpi=160);plt.close(fig)
    print(json.dumps(report,indent=2));print('PASS: all eight comparisons, aligned coordinates, masks and baseline checks.')
if __name__=='__main__':main()
