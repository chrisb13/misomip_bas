#!/usr/bin/env python 
#   Author: Christopher Bull. 
#   Affiliation:  British Antarctic Survey
#                 Cambridge, UK
#   Contact: chbull@bas.ac.uk
#   www:     christopherbull.com.au
#   Date created: Tue, 16 Oct 2018 15:34:43
#   Machine created on: SB2Vbox
#
"""
Quick script to compare the mesh mask isf_draft between the old and new isomip+ experiments for Ocean 0/1 and Ocean2
"""
from cb2logger import *
import os
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import copy
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MultipleLocator

def mkdir(p):
    """make directory of path that is passed"""
    try:
       os.makedirs(p)
       lg.info("output folder: "+p+ " does not exist, we will make one.")
    except OSError as exc: # Python >2.5
       import errno
       if exc.errno == errno.EEXIST and os.path.isdir(p):
          pass
       else: raise

if __name__ == "__main__": 
    LogStart('',fout=False)

    ##########
    #  init  #
    ##########

    mkdir('./plots/')

    case='ocean2'
    case='oceanNewVsOld'
    if case=='ocean1':
        #ocean0/1
        robin='/home/chris/VBoxSHARED/isomip_robin/mesh_mask_ISOMIP_COM1.nc'
        cb='/home/chris/VBoxSHARED/isomip_robin/mesh_mask_cb1.nc'
        # cb='/home/chris/VBoxSHARED/isomip_robin/mesh_mask_cb1_NEW.nc'
        pres='/home/chris/VBoxSHARED/isomip_robin/isomip+_NEMO_expt1_242_geom.nc'
    elif case=='ocean2':
        # ocean2
        robin='/home/chris/VBoxSHARED/isomip_robin/mesh_mask_ISOMIP_COM2.nc'
        cb='/home/chris/VBoxSHARED/isomip_robin/mesh_mask_cb2.nc'
        pres='/home/chris/VBoxSHARED/isomip_robin/isomip+_NEMO_expt2_242_geom_recalve.nc'
    elif case=='oceanNewVsOld':
        robin='/home/chris/VBoxSHARED/isomip_robin/mesh_maskOcean0_OLD.nc'
        robin='/home/chris/VBoxSHARED/isomip_robin/mesh_mask_ISOMIP_COM1.nc'

        cb='/home/chris/VBoxSHARED/isomip_robin/mesh_maskOcean0_NEW.nc'
        pres='/home/chris/VBoxSHARED/isomip_robin/isomip+_NEMO_expt1_242_geom.nc'
    else:
        lg.error("Don't know what to do here....")
        __import__('pdb').set_trace()
    assert(os.path.exists(robin)),"netCDF file does not exist!"
    assert(os.path.exists(cb)),"netCDF file does not exist!"
    assert(os.path.exists(pres)),"netCDF file does not exist!"
    cbf=xr.open_dataset(cb)
    robinf=xr.open_dataset(robin)
    presf=xr.open_dataset(pres)

    ######################################################################################################
    #  plan view but now with fairer comparison where we mask out grounded ice from the prescribed file  #
    ######################################################################################################

    plt.close('all')
    # fig=plt.figure()
    fig=plt.figure(figsize=(20.0,9.0))
    ax=fig.add_subplot(1, 5,1)

    #this cut-off in finding 'grounded' is important b/c it changes the 'analytic' metric

    #in the new runs it was: rn_glhw_min      = 1.e-3
    # from doc: minimum water column thickness to define the grounding line
    # source:
    # /fs4/n01/shared/antsia/MergedCode_9321_flx9855_remap9853_divgcorr9845_shlat9864/NEMOGCM/CONFIG/SHARED/namelist_ref

    # In the old code, this was a bit less explicit, there was one global value...
    # rn_hmin     =   -3.     !  min depth of the ocean (>0) or min number of ocean level (<0)
    # source:
    # /fs2/n02/shared/robin/MISOMIP/NEMO_COM/namelist_cfg

    grounded=np.where((presf['Bathymetry_isf']-presf['isf_draft'])<1.0)
    #need to do this otherwise when we changes the values it writes back to the array
    analytic=copy.copy(presf['isf_draft'].values)
    analytic[grounded]=0.0
    cs1=ax.contourf(analytic,levels=np.linspace(0,600,25))
    # cs1=ax.contourf(presf['isf_draft']-presf['Bathymetry_isf'])#,levels=np.linspace(0,600,25))
    plt.colorbar(cs1,cax=make_axes_locatable(ax).append_axes("bottom", size="5%", pad=0.25),orientation='horizontal')
    ax.set_title('prescribed')

    ax=fig.add_subplot(1, 5,2)
    cs1=ax.contourf(robinf['isfdraft'][0,:],levels=np.linspace(0,600,25))
    plt.colorbar(cs1,cax=make_axes_locatable(ax).append_axes("bottom", size="5%", pad=0.25),orientation='horizontal')
    ax.set_title('robin (old)')

    ax=fig.add_subplot(1, 5,3)
    cs1=ax.contourf(cbf['isfdraft'][0,:],levels=np.linspace(0,600,25))
    plt.colorbar(cs1,cax=make_axes_locatable(ax).append_axes("bottom", size="5%", pad=0.25),orientation='horizontal')
    ax.set_title('new')

    ax=fig.add_subplot(1, 5,4)
    cs1=ax.contourf(robinf['isfdraft'][0,:]-analytic,levels=np.linspace(-400,400,26),cmap='seismic',extend='both')
    plt.colorbar(cs1,cax=make_axes_locatable(ax).append_axes("bottom", size="5%", pad=0.25),orientation='horizontal')
    ax.set_title('robin - analytic')

    ax=fig.add_subplot(1, 5,5)
    cs1=ax.contourf(cbf['isfdraft'][0,:]-analytic,levels=np.linspace(-400,400,26),cmap='seismic',extend='both')
    plt.colorbar(cs1,cax=make_axes_locatable(ax).append_axes("bottom", size="5%", pad=0.25),orientation='horizontal')
    ax.set_title('new - analytic')
    efile='./plots/'+case+'mesh_mask_comp'+'_'+case+'.png'
    # fig.savefig(efile,dpi=300,bbox_inches='tight')
    # print(efile)
    plt.show()

    ######################
    #  meriodonal slice  #
    ######################
    
    yidx=20
    for yidx in np.arange(cbf['isfdraft'].shape[1]):
        plt.close('all')
        fig=plt.figure()
        ax=fig.add_subplot(1, 1,1)
        cs1=ax.plot(presf['isf_draft'][yidx,:],label='prescribed, yidx: '+str(yidx),alpha=0.5,lw=4)#,linestyle=':')
        cs1=ax.plot(presf['Bathymetry_isf'][yidx,:],label='prescribed_bathy, yidx: '+str(yidx),alpha=0.5,lw=4,linestyle='--')#,linestyle=':')
        cs1=ax.plot(robinf['isfdraft'][0,yidx,:],label='robin, yidx: '+str(yidx),alpha=0.5,lw=4)#,linestyle='-.')
        cs1=ax.plot(cbf['isfdraft'][0,yidx,:],label='new, yidx: '+str(yidx),alpha=0.5,lw=4,linestyle='--')
        ax.legend(loc='lower right')
        ax.set_ylabel('depth')
        ax.set_xlabel('x')
        ax.set_title('Meridional Slice of isfdraft, where yidx is: ' + str(yidx) )
        plt.gca().invert_yaxis()
        efile='./plots/'+case+'_mesh_mask_comp_meri_slice'+'_'+case+'_'+str(yidx).zfill(2)+'.png'
        fig.savefig(efile,dpi=300,bbox_inches='tight')
        print efile
        # fig.savefig('./.pdf',format='pdf',bbox_inches='tight')
        # plt.show()

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
