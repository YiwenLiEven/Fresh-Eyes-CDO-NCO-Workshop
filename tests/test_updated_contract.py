"""Failures that would silently invalidate a historical/scenario comparison."""
import sys
import tempfile
import unittest
from pathlib import Path
import xarray as xr

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from generate_updated_fixture import generate
from check_updated_inputs import validate


class UpdatedContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.tmp.name)
        generate(cls.root)
        cls.hist=cls.root/'historical.nc'
        cls.future=cls.root/'ssp585.nc'

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def changed_future(self,name,change):
        with xr.open_dataset(self.future) as original:
            ds=original.load()
        ds=change(ds)
        path=self.root/(name+'.nc');ds.to_netcdf(path)
        return path

    def test_valid_2024_and_2100(self):
        self.assertEqual(validate(self.hist,self.future)['months'],552)
        self.assertEqual(validate(self.hist,self.future,2100)['years'],122)

    def test_missing_month_rejected(self):
        path=self.changed_future('missing_month',lambda ds: ds.isel(time=[i for i in range(ds.sizes['time']) if i!=13]))
        with self.assertRaisesRegex(ValueError,'Missing, duplicated'):
            validate(self.hist,path)

    def test_wrong_member_rejected(self):
        def change(ds):
            ds.attrs['variant_label']='r2i1p1f1';return ds
        path=self.changed_future('wrong_member',change)
        with self.assertRaisesRegex(ValueError,'variant_label'):
            validate(self.hist,path)

    def test_partial_month_bounds_rejected(self):
        def change(ds):
            import numpy as np
            ds.time_bnds.values[0,0]+=np.timedelta64(1,'D');return ds
        path=self.changed_future('wrong_bounds',change)
        with self.assertRaisesRegex(ValueError,'Bounds must start'):
            validate(self.hist,path)

    def test_mismatched_grid_rejected(self):
        path=self.changed_future('wrong_grid',lambda ds: ds.assign_coords(lon=ds.lon+0.25))
        with self.assertRaisesRegex(ValueError,'Incompatible lon'):
            validate(self.hist,path)

    def test_mismatched_calendar_rejected(self):
        def change(ds):
            ds.time.encoding['calendar']='noleap'
            ds.time_bnds.encoding['calendar']='noleap'
            return ds
        path=self.changed_future('wrong_calendar',change)
        with self.assertRaisesRegex(ValueError,'calendar must match'):
            validate(self.hist,path)


if __name__=='__main__':
    unittest.main()
