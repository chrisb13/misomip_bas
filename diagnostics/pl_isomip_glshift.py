#!/usr/bin/env python 
#   Author: Christopher Bull. 
#   Affiliation:  Department of Geography and Environmental Sciences, 
#                 Northumbria University, Newcastle upon Tyne, UK
#   Contact: christopher.bull@northumbria.ac.uk
#   Date created: Mon, 10 Aug 2020 10:11:53
#   Machine created on: SB2Vbox
#
"""
Quick script to look at Rupert's flagged spikes in MISOMIP experiments

See email thread:
    from:	Christopher Bull <christopher.bull@northumbria.ac.uk>
    to:	Robin Smith <robin.smith@ncas.ac.uk>
    cc:	Rupert Gladstone <rupertgladstone1972@gmail.com>,
    Stephen Cornford <stephen.l.cornford@gmail.com>
    date:	Aug 10, 2020, 8:15 PM
    subject:	Re: UKESM MISOMIP1
"""
from cb2logger import *
import os
import xarray as xr
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MultipleLocator
infile='/home/chris/VBoxSHARED/IceOcean1_COM_BISICLES_UKESMis-2D.nc'
assert(os.path.exists(infile)),"netCDF file does not exist!"
ifile=xr.open_dataset(infile)
import numpy as np
import collections

def detectgl(arr):
    plot_dict=collections.OrderedDict()
    #for time in np.arange(15):
    for time in np.arange(200):
        #print time
        curr=arr[time,:]

        for lat in np.arange(800):
            #print time,lat
            if curr[40,lat]==0.:
                gl_width=len(np.where(curr[:,lat]==0.)[0])
                plot_dict[time]=(lat,gl_width)
                break
        print time,plot_dict[time]
    return plot_dict

if __name__ == "__main__": 
    LogStart('',fout=False)

    plot_dict=detectgl(ifile['groundedMask'])

    #find retreats -- offset with np.diff? Bug?
    idxs=np.where(np.diff([plot_dict.values()[k][0] for k in range(len(plot_dict.values()))])!=0.)

    plt.close('all')
    fig=plt.figure()
    ax=fig.add_subplot(5, 1,1)
    ax.plot(np.sum(np.sum(ifile['basalMassBalance'],axis=1),axis=1),label='basalMassBalance')
    ax.scatter(idxs,np.sum(np.sum(ifile['basalMassBalance'],axis=1),axis=1)[idxs],color='r')
    ax.grid(True)
    ax.set_title('basalMassBalance')
    ax=fig.add_subplot(5, 1,2)
    ax.plot(plot_dict.keys(),[plot_dict.values()[k][0] for k in range(len(plot_dict.values()))],label='groundingline index')
    ax.grid(True)
    ax.legend()
    ax=fig.add_subplot(5, 1,3)
    ax.plot(plot_dict.keys(),[plot_dict.values()[k][1] for k in range(len(plot_dict.values()))],label='groundingline width')
    ax.grid(True)
    ax.legend()
    ax=fig.add_subplot(5, 1,4)
    ax.plot(np.sum(np.sum(ifile['groundedMask'],axis=1),axis=1),label='groundedMask')
    ax.set_title('groundedMask')
    ax.grid(True)
    ax=fig.add_subplot(5, 1,5)
    ax.plot(np.sum(np.sum(ifile['iceThickness'],axis=1),axis=1),label='iceThickness')
    ax.set_title('iceThickness')
    ax.grid(True)
    plt.show()
    import pdb;pdb.set_trace()

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
