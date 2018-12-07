#!/usr/bin/env python 
#   Author: Christopher Bull. 
#   Affiliation:  British Antarctic Survey
#                 Cambridge, UK
#   Contact: chbull@bas.ac.uk
#   Date created: Thu, 04 Oct 2018 16:31:48
#   Machine created on: SB2Vbox
#

"""
Quick script to plot the gammat0 melt rates for Ocean0 (just for the metadata doc).

These numbers came from:
    /fs2/n02/n02/chbull/nemo/run/isomip_Ocean0_gammattests/nemo_ISOMIP_ocean_01c_01
    /fs2/n02/n02/chbull/nemo/run/isomip_Ocean0_gammattests/nemo_ISOMIP_ocean_01c_02
    /fs2/n02/n02/chbull/nemo/run/isomip_Ocean0_gammattests/nemo_ISOMIP_ocean_01c_03
    /fs2/n02/n02/chbull/nemo/run/isomip_Ocean0_gammattests/nemo_ISOMIP_ocean_01c_04
    /fs2/n02/n02/chbull/nemo/run/nemo_ISOMIP_ocean_01c
    /fs2/n02/n02/chbull/nemo/run/isomip_Ocean0_gammattests/nemo_ISOMIP_ocean_01c_05

22.11.2018
These TYP numbers came from /fs2/n02/n02/chbull/nemo/run/isomip_redux/isomip_Ocean0_gammat_TYP_tests/

from:	Siahaan, Antony <antsia@bas.ac.uk>
to:	"Bull, Christopher Y.S." <chbull@bas.ac.uk>
date:	Nov 20, 2018, 6:33 PM
subject:	Re: NEMO output files of the old Ocean0-2 run

pme[0.02]=[15.43,15.30,15.17,15.05,14.94,14.85]
pme[0.05]=[28.30,28.19,28.07,27.95,27.83,27.74]
pme[0.07]=[32.89,32.72,32.56,32.43,32.31,32.25]
pme[0.10]=[37.43,37.26 ,37.13,37.04,37.0 ,36.97]
pme[0.12]=[39.79,39.65,39.49,39.37,39.30,39.22]
pme[0.14]=[41.54,41.42,41.32,41.23,41.16.41.07]

from:	Siahaan, Antony <antsia@bas.ac.uk>
to:	"Bull, Christopher Y.S." <chbull@bas.ac.uk>
date:	Nov 21, 2018, 4:54 PM
subject:	Re: NEMO output files of the old Ocean0-2 run

Melt[0.055] = [29.69,29.54,29.41,29.27,29.14,29.03]
Melt[0.060] = [30.88,30.72,30.54,30.36,30.26,30.18]
Melt[0.065] = [31.95,31.73,31.58,31.46,31.35,31.27]

"""
import sys,os
sys.path.insert(1,os.path.expanduser('~/hdrive/repos/cms_analysis/'))
from cb2logger import *
import matplotlib.pyplot as plt
import collections
import numpy as np


if __name__ == "__main__": 
    LogStart('',fout=False)
    #put useful code here!

    #########
    #  COM  #
    #########

    pme=collections.OrderedDict()
    pme['1.0e-2']=[11.47,11.21,11.00,11.04,10.70,11.38 ]
    pme['2.0e-2']=[20.99,20.87,21.33,21.49,20.85,20.57 ]
    pme['3.0e-2']=[27.03,28.10,26.98,26.32,25.47,25.65 ]
    pme['4.0e-2']=[30.68,29.61,30.23,29.80,29.09,28.27 ]
    pme['4.5e-2']=[30.88,32.60,32.10,32.44,30.90,30.33 ]
    pme['5.0e-2']=[36.16,36.93,35.68,36.84,37.51,37.27 ]
    pme['target']=[30]*6

    # plt.close('all')
    # fig=plt.figure()
    # ax=fig.add_subplot(1, 1,1)
    # for exp in pme.keys():
        # if exp!='target':
            # ax.plot(pme[exp],label=exp)
        # else:
            # ax.plot(pme[exp],label=exp,color='k',linestyle='--')
    # ax.legend(loc='lower left')
    # plt.show()

    plt.close('all')
    fig=plt.figure()
    ax=fig.add_subplot(1, 1,1)
    ax.grid(True)
    pme2=[]
    idxs=[]

    for exp in pme.keys():
        if exp!='target':
            # ax.plot(pme[exp],label=exp)
            ax.scatter(float(exp),np.mean(pme[exp]),color='k')
            pme2.append(np.mean(pme[exp]))
            idxs.append(float(exp))
            # __import__('pdb').set_trace()
        else:
            pass
        ax.plot(idxs,pme2,color='k')
    # ax.legend(loc='lower left')
    ax.set_ylabel('Melt Rate (m/year)')
    ax.set_xlabel('GammaT')
    ax.set_title('COM Gammat tuning')
    ax.set_ylim([0,40])
    ax.set_xlim([0,0.06])
    # fig.savefig('./gammatVSmeltCOM.png',dpi=300,bbox_inches='tight')
    plt.show()
    print('./gammatVSmeltCOM.png')

    #########
    #  TYP  #
    #########

    pme=collections.OrderedDict()
    pme['0.02']  = [15.43,15.30,15.17,15.05,14.94,14.85]
    pme['0.05']  = [28.30,28.19,28.07,27.95,27.83,27.74]
    pme['0.055'] = [29.69,29.54,29.41,29.27,29.14,29.03]
    pme['0.060'] = [30.88,30.72,30.54,30.36,30.26,30.18]
    pme['0.065'] = [31.95,31.73,31.58,31.46,31.35,31.27]
    pme['0.07']  = [32.89,32.72,32.56,32.43,32.31,32.25]
    pme['0.10']  = [37.43,37.26,37.13,37.04,37.0 ,36.97]
    pme['0.12']  = [39.79,39.65,39.49,39.37,39.30,39.22]
    pme['0.14']  = [41.54,41.42,41.32,41.23,41.16,41.07]
    pme['target']=[30]*6

    plt.close('all')
    fig=plt.figure()
    ax=fig.add_subplot(1, 1,1)
    ax.grid(True)
    pme2=[]
    idxs=[]

    for exp in pme.keys():
        if exp!='target':
            # ax.plot(pme[exp],label=exp)
            ax.scatter(float(exp),np.mean(pme[exp]),color='k')
            pme2.append(np.mean(pme[exp]))
            idxs.append(float(exp))
            # __import__('pdb').set_trace()
        else:
            pass
        ax.plot(idxs,pme2,color='k')
    # ax.legend(loc='lower left')
    ax.set_ylabel('Melt Rate (m/year)')
    ax.set_xlabel('GammaT')
    ax.set_title('TYP Gammat tuning')
    ax.set_ylim([0,50])
    # ax.set_xlim([0,0.06])
    # fig.savefig('./gammatVSmelt_TYP.png',dpi=300,bbox_inches='tight')
    plt.show()
    print('./gammatVSmelt_TYP.png')

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
