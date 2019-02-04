from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

ncfile_in = Dataset('nemo_melt_1km.nc','r')
heat = ncfile_in.variables['sohflisf'][:].squeeze()
melt = ncfile_in.variables['sowflisf'][:].squeeze()

x_bike=np.load("x_bike.dump")
y_bike=np.load("y_bike.dump")

#add Steph's 640km calving-edge-enforced-by-melt criterion
melt[np.where(x_bike.swapaxes(0,1) >= 640e3)]=-1.0e+4

#remove mdi
#melt[np.where(melt > 1e30)]=0.
#heat[np.where(heat > 1e30)]=0.
np.ma.set_fill_value(melt,0.0)
np.ma.set_fill_value(heat,0.0)

ncfile_out = Dataset('nemoout4bisicles.nc','w',format='NETCDF3_CLASSIC')
ncfile_out.createDimension('x',x_bike.shape[0])
ncfile_out.createDimension('y',x_bike.shape[1])

x_nc=ncfile_out.createVariable('x',np.dtype('float64').char,('x'))
y_nc=ncfile_out.createVariable('y',np.dtype('float64').char,('y'))

x_nc[:]=x_bike[:,0]
y_nc[:]=y_bike[0,:]

heat_nc=ncfile_out.createVariable('HEAT_REGRID',np.dtype('float64').char,('y','x'))
melt_nc=ncfile_out.createVariable('MELT_REGRID',np.dtype('float64').char,('y','x'))

##cdo transform as stands has transposed X and Y axes. Want a rotation
##really - flip y(?)
melt_nc[:]=melt.data[::-1,:]
heat_nc[:]=heat.data[::-1,:]
#melt_nc[:]=melt
#heat_nc[:]=heat

ncfile_out.close()
