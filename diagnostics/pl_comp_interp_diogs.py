#!/usr/bin/env python 
#   Author: Christopher Bull. 
#   Affiliation:  British Antarctic Survey
#                 Cambridge, UK
#   Contact: chbull@bas.ac.uk
#   Date created: Fri, 07 Dec 2018 16:16:15
#   Machine created on: SB2Vbox
#
"""
Script to plot diogs for comparisons of ISOMIP+ experiments post-interpolation

Heavily inspired (read stolen) from: Xylar's plotMISOMIPOceanData.py
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
import collections
import glob
import matplotlib.pyplot as plt

def get_climits(experiment,var):
    """get Xylar's limits for the various variables/experiments
    
    :experiment: full experiment path
    :var: plotting variable
    :returns: reutrns colourbar limits
    """
    ename=os.path.basename(experiment)

    warmexps=['Ocean0', 'Ocean1', 'Ocean3', 'IceOcean1', 'IceOcean2']
    for warme in warmexps:
        if warme in ename:
            # TLimits = [-2.5,1.1]
            # SLimits = [33.6,34.8]
            clim={}

            clim['bottomTemperature'] = [-2.5,1.1]
            clim['bottomSalinity']    = [33.6,34.8]
            clim['vBoundaryLayer']    = [-0.5,0.5]
            clim['uBoundaryLayer']    = [-0.5,0.5]
            clim['meltRate'] = [-100.,100.]
            clim['thermalDriving'] = [-1., 1.]
            clim['halineDriving'] = [-10., 10.]
            clim['frictionVelocity'] = [0, 0.02]
            clim['barotropicStreamfunction'] = [-0.3, 0.3]
            clim['overturningStreamfunction'] = [-0.2, 0.2]
            clim['temperatureXZ']=clim['bottomTemperature']
            clim['salinityXZ']=clim['bottomSalinity']
            clim['temperatureYZ']=clim['bottomTemperature']
            clim['salinityYZ']=clim['bottomSalinity']


            return clim[var]

    # TLimits = [-2.5,-1.8]
    # SLimits = [33.6,34.8]
    clim={}
    clim['bottomTemperature'] = [-2.5,-1.8]
    clim['bottomSalinity']    = [33.6,34.8]
    clim['vBoundaryLayer']    = [-0.5,0.5]
    clim['uBoundaryLayer']    = [-0.5,0.5]
    clim['meltRate'] = [-5.,5.]
    clim['thermalDriving'] = [-0.2, 0.2]
    clim['halineDriving'] = [-2.0, 2.0]
    clim['frictionVelocity'] = [0, 0.005]
    clim['barotropicStreamfunction'] = [-0.05, 0.05]
    clim['overturningStreamfunction'] = [-0.01,0.01]
    clim['temperatureXZ']=clim['bottomTemperature']
    clim['salinityXZ']=clim['bottomSalinity']
    clim['temperatureYZ']=clim['bottomTemperature']
    clim['salinityYZ']=clim['bottomSalinity']
    return clim[var]

if __name__ == "__main__": 
    LogStart('',fout=False)
    lg.warning("We are doing case: " + ind.paper_case)
    output_folder=ind.output_folder
    plot_folder=ind.plot_outputs
    nemo_fols=ind.nemo_fols
    plotoutputs=ind.plot_outputs
    sm.mkdir(output_folder)
    sm.mkdir(plot_folder)

    if ind.paper_case=='20180814_isomip analysis':

        figtits={}
        figtits['meltRate']= 'melt rate (m/a water equiv.)'
        figtits['thermalDriving']= 'thermal driving (C)'
        figtits['halineDriving']= 'haline driving (PSU)'
        figtits['frictionVelocity']= 'friction velocity (m/s)'
        figtits['barotropicStreamfunction']= 'barotropic streamfunction (Sv)'
        figtits['overturningStreamfunction']= 'overturning streamfunction (Sv)'

        figtits['bottomTemperature']= 'sea-floor temperature (C)'
        figtits['bottomSalinity']= 'sea-floor salinity (PSU)'
        figtits['uBoundaryLayer']= 'x-velocity (m/s) in the sub-shelf boundary layer'
        figtits['vBoundaryLayer']= 'y-velocity (m/s) in the sub-shelf boundary layer'
        figtits['temperatureXZ']= 'temperature (C) sliced through y=40 km'
        figtits['salinityXZ']= 'salinity (PSU) sliced through y=40 km'
        figtits['temperatureYZ']= 'temperature (C) sliced through x=540 km'
        figtits['salinityYZ']= 'salinity (PSU) sliced through x=540 km'

        vars=['meltRate', 'thermalDriving', 'halineDriving', 'frictionVelocity', 'barotropicStreamfunction', 'overturningStreamfunction','bottomTemperature','bottomSalinity','uBoundaryLayer','vBoundaryLayer','temperatureXZ','salinityXZ','temperatureYZ','salinityYZ']

        # vars=[ 'thermalDriving', 'halineDriving', 'frictionVelocity', 'barotropicStreamfunction', 'overturningStreamfunction']

        for varname in vars:
            #The following three ordered dictionaries are ordered by each subplot where they contain:
            #plotdict is the fields to contourf
            plotdict=collections.OrderedDict()
            #(optional) dimlab is the labels for the x/y axis
            dimlab=collections.OrderedDict()
            colorbars=collections.OrderedDict()

            for exp in nemo_fols.keys():
                lg.info("We are working experiment :" + exp)
                ifiles=sorted(glob.glob(nemo_fols[exp][0]+'*.nc'))
                assert(ifiles!=[]),"glob didn't find anything!"
                assert(os.path.exists(ifiles[0])),"netCDF file does not exist!"
                ifile=xr.open_dataset(ifiles[0])

                # ivar=ifile[varname]

                if varname=='meltRate':
                    # meltRate needs to be scaled to m/a (as we are used to seeing)
                    scale=365.*24.*60.*60.
                elif varname=='overturningStreamfunction' or varname=='barotropicStreamfunction':
                    scale=1e-6
                else:
                    scale=None

                # ename=os.path.basename(exp).split('_')[0]
                dimlab[exp]=('','')

                field=ifile[varname][-1,:].values

                #Xylar's missing value stuff
                # missingValue = 9.9692099683868690e36
                # if(np.ma.amax(field) == missingValue):
                    # # the array didnt' get masked properly, so do it manually
                    # field = np.ma.masked_array(field, mask=(field == missingValue), dtype=float)
                # else:
                    # # convert from float32 to float64 to avoid overflow/underflow problems
                    # if hasattr(field, 'mask'):
                      # field = np.ma.masked_array(field, mask=field.mask, dtype=float)
                    # else:
                      # field = np.array(field, dtype=float)

                #would also be good to include the xylar flipping stuff..

                plotdict[exp]=field

                # scale the variable if a scale is given
                if scale is not None:
                    plotdict[exp] *= scale

                # climits=clim[varname]
                climits=get_climits(ifiles[0],varname)

            plotback=sm.Grid(plotdict,(3,2),dimlabels=dimlab,globalcbar='jet',clevels=20,sharex=True,sharey=True,outputpath=plotoutputs+'comp_interpd/'+varname+'.png',globalclimits=climits,figtit=figtits[varname],titloc=3)
            print plotoutputs+'comp_interpd/'+varname+'.png'
            # __import__('pdb').set_trace()

    else:
        lg.error("I don't know what to do here!"+ ind.paper_case)
        sys.exit()

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
