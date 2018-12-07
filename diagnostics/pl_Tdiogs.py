#!/usr/bin/env python 
#   Author: Christopher Bull. 
#   Affiliation:  British Antarctic Survey
#                 Cambridge, UK
#   Contact: chbull@bas.ac.uk
#   www:     christopherbull.com.au
#   Date created: Tue, 14 Aug 2018 13:50:14
#   Machine created on: SB2Vbox
#

"""
Quick script to plot diogs for ISOMIP experiments
"""
import logging as lg
import time
import os
import sys
pathfile = os.path.dirname(os.path.realpath(__file__)) 
sys.path.insert(1,os.path.dirname(pathfile)+'/')
from cb2logger import *
import inputdirs as ind
import shareme as sm
import os
import xarray as xr
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt
if __name__ == "__main__": 
    LogStart('',fout=False)
    lg.warning("We are doing case: " + ind.paper_case)
    output_folder=ind.output_folder
    plot_folder=ind.plot_outputs
    nemo_fols=ind.nemo_fols
    sm.mkdir(output_folder)
    sm.mkdir(plot_folder)
    if ind.paper_case=='20180814_isomip analysis':
        for exp in nemo_fols.keys():
            lg.info("We are working experiment :" + exp)
            import glob
            ifiles=sorted(glob.glob(nemo_fols[exp][0]+'ISOMIP-*_1m_*grid_T.nc'))
            assert(ifiles!=[]),"glob didn't find anything!"
            assert(os.path.exists(ifiles[0])),"netCDF file does not exist!"
            ifile=xr.open_dataset(ifiles[0])
            for var in ['sosstsst','sosaline','vosaline']:
                plt.close('all')
                fig=plt.figure()
                ax=fig.add_subplot(1, 1,1,axisbg='gray')
                # if var=='sosstsst':
                    # cs1=ax.contourf(np.mean(ifile[var][-12:],axis=0),np.linspace(-1.5,-0.1,30),extend='both')
                # elif var=='sosaline':
                    # cs1=ax.contourf(np.mean(ifile[var][-12:],axis=0),np.linspace(30,38,30),extend='both')

                #masking before taking mean is important!
                pnew=np.ma.masked_equal(ifile[var],0)
                if var=='sosstsst' or var=='sosaline':
                    pme=np.mean(pnew[-12:],axis=0)
                    ax.set_xlabel('x')
                    ax.set_ylabel('y')
                elif var=='vosaline':
                    pme=np.mean(np.mean(pnew[-12:],axis=0),axis=1)
                    ax.set_xlabel('x')
                    ax.set_ylabel('z')
                else:
                    pass

                # cs1=ax.contourf(np.ma.masked_equal(pme,0),30,extend='both')
                cs1=ax.contourf(pme,30,extend='both')

                if var=='vosaline':
                    plt.gca().invert_yaxis()

                plt.colorbar(cs1,cax=make_axes_locatable(ax).append_axes("bottom", size="5%", pad=0.25),orientation='horizontal')
                # plt.show()
                fig.savefig(plot_folder+exp+'_'+os.path.basename(ifiles[0])[:-3]+'_'+var+'.png',dpi=300,bbox_inches='tight')
                # fig.savefig('./.pdf',format='pdf',bbox_inches='tight')
                # plt.show()
            

    else:
        lg.error("I don't know what to do here!"+ ind.paper_case)
        sys.exit()

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
