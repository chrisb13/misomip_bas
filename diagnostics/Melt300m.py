import numpy as np
from netCDF4 import Dataset
import collections
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MultipleLocator
import os
import xarray as xr
import glob

#mesh_file='/work/n02/shared/robin/MISOMIP/NEMO_TYP/mesh_mask_expt1_TYP_CALVE.nc'
mesh_file='/fs2/n02/shared/chbull/nemo_ISOMIP_oceanTYP_01c/mesh_mask.nc'
#out_file='/work/n02/shared/robin/MISOMIP/NEMO_TYP/Ocean0_TYP_1m_00010101_00021230_grid_T.nc'
out_file='/fs2/n02/shared/chbull/nemo_ISOMIP_oceanTYP_01c/ISOMIP-0_TYP_1m_00010101_00030110_grid_T.nc'

out_file='/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_01b/ISOMIP-0_1m_00010101_00030110_grid_T.nc'
mesh_file='/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_01c/mesh_mask.nc'

#####################
#  COM experiments  #
#####################

plot_dict=collections.OrderedDict()
plot_dict['COM_ISOMIP_ocean0']=['/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_01c/ISOMIP-0_1m_00010101_00030110_grid_T.nc','/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_01c/mesh_mask.nc']
plot_dict['COM_ISOMIP_ocean0_OLD']=['/home/chris/VBoxSHARED/NEMO_COM/ISOMIP-0_1m_00010101_00021230_grid_T.nc','/home/chris/VBoxSHARED/NEMO_COM/mesh_mask_ISOMIP_COM1.nc']

plot_dict['COM_ISOMIP_ocean1']=['/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_02c/ISOMIP-1_1m_00010101_00210410_grid_T.nc','/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_02c/mesh_mask.nc']
plot_dict['COM_ISOMIP_ocean1_OLD']=['/home/chris/VBoxSHARED/NEMO_COM/ISOMIP-1_1m_00010101_00201230_grid_T.nc','/home/chris/VBoxSHARED/NEMO_COM/mesh_mask_ISOMIP_COM1.nc']

plot_dict['COM_ISOMIP_ocean2']=['/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_03c/ISOMIP-2_1m_00010101_00210410_grid_T.nc','/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_03c/mesh_mask.nc']
plot_dict['COM_ISOMIP_ocean2_OLD']=['/home/chris/VBoxSHARED/NEMO_COM/ISOMIP-2_1m_00010101_00201230_grid_T.nc','/home/chris/VBoxSHARED/NEMO_COM/mesh_mask_ISOMIP_COM2.nc']

#####################
#  TYP experiments  #
#####################

# plot_dict=collections.OrderedDict()
# plot_dict['TYP_ISOMIP_ocean0']=['/home/chris/VBoxSHARED/nemo_ISOMIP_oceanTYP_01c/ISOMIP-0_TYP_1m_00010101_00030110_grid_T.nc','/home/chris/VBoxSHARED/nemo_ISOMIP_oceanTYP_01c/mesh_mask.nc']
# plot_dict['TYP_ISOMIP_ocean0_OLD']=['/home/chris/VBoxSHARED/NEMO_TYP/Ocean0_TYP_1m_00010101_00021230_grid_T.nc','/home/chris/VBoxSHARED/NEMO_TYP/mesh_mask_expt1_TYP_CALVE.nc']

# plot_dict['TYP_ISOMIP_ocean1']=['/home/chris/VBoxSHARED/nemo_ISOMIP_oceanTYP_02c/ISOMIP-1_TYP_1m_00010101_00210410_grid_T.nc','/home/chris/VBoxSHARED/nemo_ISOMIP_oceanTYP_02c/mesh_mask.nc']
# plot_dict['TYP_ISOMIP_ocean1_OLD']=['/home/chris/VBoxSHARED/NEMO_TYP/Ocean1_TYP_1m_00010101_00201230_grid_T.nc','/home/chris/VBoxSHARED/NEMO_TYP/mesh_mask_expt1_TYP_CALVE.nc']

# plot_dict['TYP_ISOMIP_ocean2']=['/home/chris/VBoxSHARED/nemo_ISOMIP_oceanTYP_03c/ISOMIP-2_TYP_1m_00010101_00210410_grid_T.nc','/home/chris/VBoxSHARED/nemo_ISOMIP_oceanTYP_03c/mesh_mask.nc']
# plot_dict['TYP_ISOMIP_ocean2_OLD']=['/home/chris/VBoxSHARED/NEMO_TYP/Ocean2_TYP_1m_00010101_00201230_grid_T.nc','/home/chris/VBoxSHARED/NEMO_TYP/mesh_mask_expt2_TYP_CALVE.nc']

#############################
#  comparing the mesh_mask  #
#############################


# mesh1='/home/chris/VBoxSHARED/NEMO_COM/mesh_mask_ISOMIP_COM1.nc'
# mesh2='/home/chris/VBoxSHARED/NEMO_COM/mesh_mask_ISOMIP_COM2.nc'

mesh1='/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_01c/mesh_mask.nc'
mesh2='/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_02c/mesh_mask.nc'
# mesh2='/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_03c/mesh_mask.nc'

# tmask1=Dataset(mesh1,'r').variables['tmask']
# tmask2=Dataset(mesh2,'r').variables['tmask']

# for depth in np.arange(np.shape(tmask1)[1]):
    # plt.close('all')
    # fig=plt.figure()
    # ax=fig.add_subplot(1, 3,1)
    # cs1=ax.contourf(tmask1[0,depth,:,:])
    # plt.colorbar(cs1,cax=make_axes_locatable(ax).append_axes("bottom", size="5%", pad=0.25),orientation='horizontal')
    # ax.set_title('Com1 '+str(depth))
    # ax=fig.add_subplot(1, 3,2)
    # cs1=ax.contourf(tmask2[0,depth,:,:])
    # plt.colorbar(cs1,cax=make_axes_locatable(ax).append_axes("bottom", size="5%", pad=0.25),orientation='horizontal')
    # ax.set_title('Com2 '+str(depth))
    # ax=fig.add_subplot(1, 3,3)
    # cs1=ax.contourf(tmask2[0,depth,:,:]-tmask1[0,depth,:,:])
    # plt.colorbar(cs1,cax=make_axes_locatable(ax).append_axes("bottom", size="5%", pad=0.25),orientation='horizontal')
    # ax.set_title('Com2-Com1')
    # plt.show()

# __import__('pdb').set_trace()

##################################################
#  plotting time series of melt rate comparison  #
##################################################


# plt.close('all')
# #width then height
# fig=plt.figure(figsize=(9.0,12.0))
# for idx,exp in enumerate(plot_dict.keys()):
    # if idx in [0,1]:
        # ax=fig.add_subplot(3, 1,1)
        # ax1=ax
        # # plt.setp(ax.get_xticklabels(), visible=False)
    # if idx in [2,3]:
        # ax=fig.add_subplot(3, 1,2)
        # # plt.setp(ax.get_xticklabels(), visible=False)
    # if idx in [4,5]:
        # ax=fig.add_subplot(3, 1,3)

    # out_file=plot_dict[exp][0]
    # mesh_file=plot_dict[exp][1]
    # print out_file
    # print mesh_file


    # melt=Dataset(out_file,'r').variables['meltRate'][:]
    # print np.sum(melt)
    # e1t=Dataset(mesh_file,'r').variables['e1t'][0]
    # e2t=Dataset(mesh_file,'r').variables['e2t'][0]
    # tmask=Dataset(mesh_file,'r').variables['tmask'][0,0]
    # tmaskutil=Dataset(mesh_file,'r').variables['tmaskutil'][0]
    # isfdraft=Dataset(mesh_file,'r').variables['isfdraft'][0]
    # meltyear=melt*365*24*60*60/918.0
    # melt300=np.where(isfdraft<300,0.0,meltyear)
    # area=e1t*e2t
    # area300=np.where(isfdraft<300,0.0,area)

    # pme=[]
    # for i in range(melt.shape[0]):
       # # print i,np.sum(melt300[i]*area300*(tmaskutil)*(1-tmask))/np.sum(area300*(tmaskutil)*(1-tmask))
       # pme.append(np.sum(melt300[i]*area300*(tmaskutil)*(1-tmask))/np.sum(area300*(tmaskutil)*(1-tmask)))

    # ax.set_ylabel('Melt rate (m/yr)')
    # ax.plot(pme,label=exp)
    # ax.grid(True)
    # ax.legend(loc='lower-left')
    # if idx==5:
        # ax.set_xlabel('Months')
# plt.show()
# fig.savefig('./isomiptimeseries.png',dpi=300,bbox_inches='tight')

########################################################################################
#  looking at Robin's interpolated files...  (well, and some of the CNRS NEMO results) #
########################################################################################

plt.close('all')

fig=plt.figure(figsize=(9.0,12.0))
for ocean_num in np.arange(3):
    ax=fig.add_subplot(3, 1,ocean_num+1)

    ifiles=sorted(glob.glob('/home/chris/VBoxSHARED/Ocean'+str(ocean_num)+'*.nc' ))
    assert(ifiles!=[]),"glob didn't find anything!"

    for f in ifiles:
        print f
        ifile=xr.open_dataset(f)
        ax.plot(ifile['totalMeltFlux'].values.tolist(),label=os.path.basename(f),lw=2,alpha=0.7)
        ax.set_ylabel('totalMeltFlux (kg/s)')
        ax.set_xlabel('Months')
        ax.grid(True)

    ax.legend(loc='upper left')
plt.show()
