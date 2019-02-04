import numpy as np
from netCDF4 import Dataset

#rename and sort out axis sense for the regrided 1km BISICLES output

def flip_depth(array):
  array=array*-1
  array=np.maximum(array,0)
  return array

def calve(array,threshold):
  calved=np.where(array <= threshold)
  array[calved]=0.
  return array

def mindepth(array,thk,threshold):
  #should get thk mask, really
  min=np.where((abs(thk) > 1e-6) & (thk<threshold) & (thk.mask == False))
  print thk[min]
  print array[min]
  array[min]=threshold
  return array

ncin=Dataset("bike_geom_TYP.nc")
thk=ncin.variables["thickness"][:].squeeze()
isf=ncin.variables["Z_bottom"][:].squeeze()
bathy=ncin.variables["Z_base"][:].squeeze()

bathy=flip_depth(bathy)
isf=flip_depth(isf)

#isf=calve(isf,100.)
isf=mindepth(isf,thk,1.15)

ncout=Dataset("bathy_isf_meter_TYP.nc",'w',format='NETCDF3_CLASSIC')
ncout.createDimension('x',bathy.shape[1])
ncout.createDimension('y',bathy.shape[0])
bathy_nc = ncout.createVariable('Bathymetry_isf',np.dtype('float64').char,('y','x'))
isf_nc = ncout.createVariable('isf_draft',np.dtype('float64').char,('y','x'))
isf_nc[:]=isf
bathy_nc[:]=bathy
ncout.close()
