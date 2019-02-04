from netCDF4 import Dataset
import numpy as np

ncfile_in = Dataset('nple3.nc','r')
heat242 = ncfile_in.variables['sohflisf'][:].squeeze()
melt242 = ncfile_in.variables['sowflisf'][:].squeeze()

heat240 = heat242[1:-1,1:-1]
melt240 = melt242[1:-1,1:-1]

heat400=np.zeros([40,400])
melt400=np.zeros([40,400])

heat400[:,160:]=heat240
melt400[:,160:]=melt240

x_bike=np.load("x_bike400.dump")
y_bike=np.load("y_bike400.dump")

#add Steph's 640km calving-edge-enforced-by-melt criterion
melt400[:,np.where(x_bike >= 640e3)]=-1.0e+4

ncfile_out = Dataset('nemoout4bisicles.nc','w',format='NETCDF3_CLASSIC')
ncfile_out.createDimension('x',x_bike.shape[0])
ncfile_out.createDimension('y',y_bike.shape[0])

x_nc=ncfile_out.createVariable('x',np.dtype('float64').char,('x'))
y_nc=ncfile_out.createVariable('y',np.dtype('float64').char,('y'))

x_nc[:]=x_bike
y_nc[:]=y_bike

heat_nc=ncfile_out.createVariable('HEAT_REGRID',np.dtype('float64').char,('y','x'))
melt_nc=ncfile_out.createVariable('MELT_REGRID',np.dtype('float64').char,('y','x'))

melt_nc[:]=melt400
heat_nc[:]=heat400

ncfile_out.close()
