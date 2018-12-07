#!/usr/bin/env python 
#   Author: Christopher Bull. 
#   Affiliation:  British Antarctic Survey
#                 Cambridge, UK
#   Contact: chbull@bas.ac.uk
#   Date created: Fri, 02 Nov 2018 13:22:52
#   Machine created on: SB2Vbox
#
"""
Quick script to understand what went wrong with Robin's T/S init and resto files...

See email thread:
    from:	Robin Smith <robin.smith@ncas.ac.uk> via nercacuk.onmicrosoft.com
    to:	"Bull, Christopher Y.S." <chbull@bas.ac.uk>
    cc:	"Siahaan, Antony" <antsia@bas.ac.uk>
    date:	Oct 30, 2018, 1:02 PM
    subject:	Re: NEMO output files of the old Ocean0-2 run
"""
import sys,os
from cb2logger import *
import glob
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MultipleLocator

def TSinit_check(coldfiles,warmfiles,ename):
    """function to plot vertical profiles of T/S init with the spatial mean taken at each level
    
    :coldfiles: collection of nemo_base_COLD files
    :warmfiles: collection of nemo_base_WARM files
    :ename: output name of plot
    :returns: 
    """

    plt.close('all')
    #width then height
    fig=plt.figure(figsize=(13.0,5.0))
    ax=fig.add_subplot(1, 2,1)
    ax2=fig.add_subplot(1, 2,2)

    for f in coldfiles+warmfiles:
        ifile=xr.open_dataset(f)
        pme=np.mean(np.mean(ifile['Tinit'],axis=1),axis=1)
        pme2=np.mean(np.mean(ifile['Sinit'],axis=1),axis=1)
        ax.plot(pme,range(len(pme)),label=os.path.basename(f),alpha=0.6,lw=5)
        ax.set_title('Tinit')
        ax.grid(True)

        ax.set_xlabel('Temperature (spatial level mean)')
        ax.set_ylabel('Depth level')

        # plt.gca().invert_yaxis()
        ax2.plot(pme2,range(len(pme2)),label=os.path.basename(f),alpha=0.6,lw=5)
        ax2.set_title('Sinit')
        ax2.grid(True)

        ax2.set_xlabel('Salinity (spatial level mean)')
        ax2.set_ylabel('Depth level')
        # plt.gca().invert_yaxis()
    ax.legend(loc='lower right')
    ax2.legend(loc='lower right')
    fig.savefig(ename,dpi=300,bbox_inches='tight')

    pass

def resto_check(coldfiles,warmfiles):
    """function to check the resto variable by comparing each level and showing a spatial plot as needed
    
    :coldfiles: collection of nemo_base_COLD files
    :warmfiles: collection of nemo_base_WARM files
    :ename: output name of plot
    :returns: 
    """
    plt.close('all')
    fig=plt.figure(figsize=(20.0,5.0))
    axes=[fig.add_subplot(1, 4,1),fig.add_subplot(1, 4,2),fig.add_subplot(1, 4,3),fig.add_subplot(1, 4,4)]
    pmes=[]
    for idx,f in enumerate(coldfiles+warmfiles):
        ax=axes[idx]
        ifile=xr.open_dataset(f)

        #check that the resto is the same at every level
        zlev=ifile['resto'].shape[0]
        for a,b in zip(np.arange(zlev),np.arange(1,zlev)):
            # print a,b
            if not np.array_equal(ifile['resto'][a,:],ifile['resto'][b,:]):
                lg.error("resto was not the same at every level!")
                sys.exit()

        cs1=ax.contourf(ifile['resto'][0,:],30)
        ax.set_title(os.path.basename(f))
        pmes.append(ifile['resto'][0,:])
        plt.colorbar(cs1,cax=make_axes_locatable(ax).append_axes("bottom", size="5%", pad=0.25),orientation='horizontal')


    zlev=4
    for a,b in zip(np.arange(zlev),np.arange(1,zlev)):
        # print a,b
        if not np.array_equal(pmes[a],pmes[b]):
            lg.warning("resto was not the same across the experiments!")
    # plt.show()

    lg.info("resto was the same!")

    return

if __name__ == "__main__": 
    LogStart('',fout=False)
    typf='/fs2/n02/shared/robin/MISOMIP/NEMO_TYP/'
    # typf='/home/chris/VBoxSHARED/isomip/NEMO_TYP/'

    comf='/fs2/n02/shared/robin/MISOMIP/NEMO_COM/'
    # comf='/home/chris/VBoxSHARED/isomip/NEMO_COM/'
    
    coldtyp=sorted(glob.glob(typf + 'nemo_base_COLD*' ))
    assert(coldtyp!=[]),"glob didn't find anything!"

    warmtyp=sorted(glob.glob(typf + 'nemo_base_WARM*' ))
    assert(warmtyp!=[]),"glob didn't find anything!"

    coldcom=sorted(glob.glob(comf + 'nemo_base_COLD*' ))
    assert(coldcom!=[]),"glob didn't find anything!"

    warmcom=sorted(glob.glob(comf + 'nemo_base_WARM*' ))
    assert(warmcom!=[]),"glob didn't find anything!"

    ####################
    #  check T/S init  #
    ####################

    TSinit_check(coldtyp,warmtyp,'./typcomparison.png')
    TSinit_check(coldcom,warmcom,'./comcomparison.png')

    #######################################
    #  check resto files for differences  #
    #######################################

    resto_check(coldtyp,warmtyp)
    resto_check(coldcom,warmcom)



    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
