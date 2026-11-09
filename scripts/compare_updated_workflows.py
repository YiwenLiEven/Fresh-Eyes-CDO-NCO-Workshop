"""Compare independent products and plot them; never supplies route intermediates."""
import argparse
import json
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', str(Path(__file__).resolve().parents[1]/'.cache/matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

PRODUCTS=['climatology','anomaly','map_mean','arctic_monthly','arctic_annual']


def read(root,route,product):
    with xr.open_dataset(root/route/(product+'.nc')) as ds:
        a=ds['tas' if product=='climatology' else 'tas_anom'].squeeze(drop=True).load()
        if product=='climatology':
            dim='month' if 'month' in a.dims else 'time'
            if dim=='time':
                np.testing.assert_array_equal(a.time.dt.month,np.arange(1,13))
                a=a.rename(time='month')
            else:
                np.testing.assert_array_equal(a.month,np.arange(1,13))
            a=a.assign_coords(month=np.arange(1,13)).transpose('month','lat','lon')
        elif 'time' in a.dims:
            if product=='arctic_annual':
                a=a.assign_coords(year=('time',a.time.dt.year.values)).swap_dims({'time':'year'}).drop_vars('time')
            else:
                a=a.assign_coords(time=a.time.dt.year.values*12+a.time.dt.month.values)
        if product=='anomaly': a=a.transpose('time','lat','lon')
        if product=='map_mean': a=a.transpose('lat','lon')
        return a


def compare(root):
    root=Path(root); tolerance=3e-4
    info=json.loads((root/'python/input_contract.json').read_text())
    arrays={p:{r:read(root,r,p) for r in ['python','cdo','nco']} for p in PRODUCTS}
    report={'input':info,'absolute_tolerance_degC':tolerance,'comparisons':{},'invariants':{}}
    for product in PRODUCTS:
        for route in ['cdo','nco']:
            ref,actual=xr.align(arrays[product]['python'],arrays[product][route],join='exact')
            assert ref.dims==actual.dims and ref.shape==actual.shape
            np.testing.assert_array_equal(np.isfinite(ref),np.isfinite(actual))
            error=float(abs(ref-actual).max())
            np.testing.assert_allclose(actual,ref,atol=tolerance,rtol=0)
            report['comparisons'][route+'/'+product]={'max_absolute_difference_degC':error,'passed':True}
            print(f'PASS {route}/{product}: {error:.9g} degC')
    for route in ['python','cdo','nco']:
        monthly=arrays['anomaly'][route]
        assert monthly.sizes['time']==info['months']
        assert int(monthly.time[0])==1979*12+1
        baseline=monthly.sel(time=slice(1981*12+1,2010*12+12)).values.reshape(30,12,*monthly.shape[1:])
        residual=float(abs(baseline.mean(axis=0)).max())
        assert residual<tolerance
        annual=arrays['arctic_annual'][route]
        np.testing.assert_array_equal(annual.year,np.arange(1979,1979+info['years']))
        np.testing.assert_allclose(annual.values,arrays['arctic_monthly'][route].values.reshape(-1,12).mean(axis=1),rtol=0,atol=tolerance)
        report['invariants'][route]={'baseline_residual_degC':residual,'annual_equal_months':True,'time_coverage':True}
        if route!='python':
            with xr.open_dataset(root/route/'arctic_annual.nc',decode_times=xr.coders.CFDatetimeCoder(use_cftime=True)) as ds:
                for year,(lo,hi) in zip(annual.year.values,ds.time_bnds.values):
                    assert (lo.year,lo.month,lo.day)==(int(year),1,1)
                    assert (hi.year,hi.month,hi.day)==(int(year)+1,1,1)
            report['invariants'][route]['annual_bounds_full_year']=True
        weighted_difference=float(abs(arrays['map_mean'][route]-monthly.mean('time')).max())
        report['invariants'][route]['weighted_vs_arithmetic_map_difference_degC']=weighted_difference
        if info['synthetic']:
            assert weighted_difference>tolerance, 'Fixture must distinguish the duration-weighted map from an arithmetic map'
    report['passed']=True
    (root/'updated_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    fig,axes=plt.subplots(3,3,figsize=(14,8),layout='constrained')
    map_limit=max(float(abs(arrays['map_mean'][r]).max()) for r in ['python','cdo','nco'])
    stripe_limit=max(float(abs(arrays['arctic_annual'][r]).max()) for r in ['python','cdo','nco'])
    for col,route in enumerate(['python','cdo','nco']):
        field=arrays['map_mean'][route]
        im=axes[0,col].pcolormesh(field.lon,field.lat,field,cmap='bwr',vmin=-map_limit,vmax=map_limit,shading='auto')
        axes[0,col].set(title=route.upper()+': duration-weighted map',xlabel='Longitude',ylabel='Latitude')
        series=arrays['arctic_monthly'][route]
        axes[1,col].plot(1979+np.arange(info['months'])/12,series,lw=.8)
        axes[1,col].set(title='Arctic monthly anomaly (65–90°N)',xlabel='Year',ylabel='°C')
        annual=arrays['arctic_annual'][route]
        si=axes[2,col].imshow(annual.values[None,:],extent=[1978.5,1978.5+info['years'],0,1],aspect='auto',cmap='bwr',vmin=-stripe_limit,vmax=stripe_limit)
        axes[2,col].set(title='Annual stripes: equal monthly samples',xlabel='Year',yticks=[])
    fig.colorbar(im,ax=axes[0,:],label='°C',shrink=.65)
    fig.colorbar(si,ax=axes[2,:],label='°C',shrink=.65)
    label='SYNTHETIC SOFTWARE TEST — not ACCESS-CM2 results' if info['synthetic'] else 'ACCESS-CM2 historical + SSP5-8.5 — model output'
    fig.suptitle(f"{label}\n{info['period']}; monthly reference 1981–2010; three independent routes")
    fig.savefig(root/'updated_comparison.png',dpi=150);plt.close(fig)
    print('PASS: ten product comparisons, monthly baseline, coordinates and annual definitions.')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root');compare(p.parse_args().root)
