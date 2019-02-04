from netCDF4 import Dataset
import numpy as np

def expand_out(array240):
  array242=np.zeros([nj,ni])

  array242[1:-1,1:-1]=array240

  array242[0   ,1:-1] =array240[0 ,: ]
  array242[-1  ,1:-1] =array240[-1,: ]
  array242[1:-1,0   ] =array240[: ,0 ]
  array242[1:-1,-1  ] =array240[: ,-1]

  array242[0 ,0 ] =array240[0 ,0 ]
  array242[-1,0 ] =array240[-1,0 ]
  array242[0 ,-1] =array240[0 ,-1]
  array242[-1,-1] =array240[-1,-1]

  return array242

def remove_single(array242):
  ni=array242.shape[1]
  nj=array242.shape[0]

  copy242=np.copy(array242)
  for j in np.arange(nj):
    for i in np.arange(ni-1)+1:
      if     (array242[j,i-1] == 0) \
         and (array242[j,i] > 0) \
         and (array242[j,i+1] == 0) : 
           print j,i,array242[j,i-1],array242[j,i],array242[j,i+1]
           copy242[j,i]=0.

  return copy242

def backfill(array242):
  open=np.where(array242[:,0:159] < 1)
  array242[open]=75

  return array242


ni=242
nj=42

filename_in="bathy_isfdraft.nc"
filename_out="bathy_isfdraft_242.nc"
ncfile_in = Dataset(filename_in,'r')
bathy240=ncfile_in.variables['Z_base'][:].squeeze()*-1
isf240=ncfile_in.variables['Z_bottom'][:].squeeze()*-1

bathy242=expand_out(bathy240)
isf242=expand_out(isf240)
#isf242=remove_single(isf242)
#isf242=backfill(isf242)

ncfile_out = Dataset(filename_out,'w',format='NETCDF3_CLASSIC')
ncfile_out.createDimension('x',ni)
ncfile_out.createDimension('y',nj)
bathy_nc=ncfile_out.createVariable('Bathymetry_isf',np.dtype('float64').char,('y','x'))
isf_nc=ncfile_out.createVariable('isf_draft',np.dtype('float64').char,('y','x'))
bathy_nc[:]=bathy242
isf_nc[:]=isf242
ncfile_out.close()
