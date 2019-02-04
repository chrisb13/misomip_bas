#   Author: Christopher Bull. 
#   Affiliation:  British Antarctic Survey
#                 Cambridge, UK
#   Contact: chbull@bas.ac.uk
#   Date created: Mon, 10 Dec 2018 13:44:52
#   Machine created on: SB2Vbox
#   NB: need to load the Anaconda environment 

from cb2logger import *
import f90nml
import os
import glob
import shutil 
import re
import sys
import numpy as np
import contextlib as ctx
from netCDF4 import Dataset

OCEANCORES=eeee
XIOCORES=ffff
NODES=gggg
RHOURS=hhhh

FORCING_NUM=kkkk
FORCING_TYPE='uuuu'
PROJ='pppp'
WORKDIR='wwww'+'/'
STOCKDIR='ssss'
CONFIG='cccc'
CASE='oooo'
DESC='zzzz'
RBUILD_NEMO='jjjj'
YEAR0=Y0Y0
YEAR_MAX=YMYM
BISICLES_CPL=xxxx

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

def rebuild_mesh_mask(handle):
    """function to rebuild the mesh_mask using the NEMO tool
    :handle: text file handle
    :returns: 
    """
    handle.write(''+'\n')
    handle.write('echo "Re-combining: '+'mesh_mask'+'"'+'\n')
    handle.write('aprun -b '+RBUILD_NEMO+' '+'mesh_mask'+' '+str(OCEANCORES)+'\n')
    handle.write(''+'\n')

    handle.write('if [ -f ' +'mesh_mask.nc'+' ]; then'+'\n')
    handle.write('   echo "File: '+'mesh_mask.nc'+' reassembled ok"'+'\n')
    handle.write('   rm '+'mesh_mask_*.nc'+'\n')
    handle.write('else'+'\n')
    handle.write('   echo "!@#$% PROBLEM WITH RE-ASSEMBLY OF FILE'+' mesh_mask"'+'\n')
    handle.write('   echo ">>>>>>>>>> STOP !"'+'\n')
    handle.write('   exit 1'+'\n')
    handle.write('fi'+'\n')
    return



def get_ISOMIP_timeslice(slice,wkdir):
    """robin's code for feeding nemo the right bathy / isf_draft

    Creates:
       -bathy_meter.nc
       -isf_draft_meter.nc
    :slice: integer time slice (starts at 1)
    :wkdir: WORKDIR 
    :returns: 
    """
    lg.info("Creating bathy_meter.nc and isf_draft_meter.nc for Ocean3-4 timestep: "+str(slice))

    ncin=wkdir+'bathy_meter_all.nc'
    assert(os.path.exists(ncin)),"can't find bathy_meter_all.nc, was it correctly linked by production_nemo_ARCHER.sh?"
    ncfile_in = Dataset(ncin)
    isf=ncfile_in.variables['isf_draft'][:].squeeze()
    bathy=ncfile_in.variables['Bathymetry_isf'][:].squeeze()

    ncfile_out = Dataset('bathy_meter.nc','w',format='NETCDF3_CLASSIC')
    ncfile_out.createDimension('x',isf.shape[2])
    ncfile_out.createDimension('y',isf.shape[1])
    bathy_nc=ncfile_out.createVariable('Bathymetry_isf',np.dtype('float64').char,('y','x'))
    bathy_nc[:]=bathy[slice-1,:,:]
    ncfile_out.close()

    ncfile_out = Dataset('isf_draft_meter.nc','w',format='NETCDF3_CLASSIC')
    ncfile_out.createDimension('x',isf.shape[2])
    ncfile_out.createDimension('y',isf.shape[1])
    isf_nc=ncfile_out.createVariable('isf_draft',np.dtype('float64').char,('y','x'))
    isf_nc[:]=isf[slice-1,:,:]
    ncfile_out.close()
    return

if __name__ == "__main__": 

    ##########
    #  init  #
    ##########

    nmlpath="namelist_cfg"
    # nmlpath_ice="namelist_ice_ref"

    os.chdir(WORKDIR)

    ##########
    #  init  #
    ##########

    LogStart('',fout=False)

    lg.info("******************************************")
    lg.info("*   project "+PROJ  +"                       ")
    lg.info("*   config  "+CONFIG+"                       ")
    lg.info("*   case    "+CASE  +"                       ")
    lg.info("*   Desc    "+DESC  +"                       ")
    lg.info("*   OceanCores    "+str(OCEANCORES)+"                      ")
    lg.info("*   XiosCores     "+str(XIOCORES)  +"                      ")
    lg.info("******************************************")

    YEAR=YEAR0

    # while [  $YEAR -lt $YEAR_MAX ]; do
    while int(YEAR) <= int(YEAR_MAX):
        # lg.info("Currently working on year: " + str(YEAR))

        # NDAYS=5
        # NDAYS=32
        # NDAYS=365

        #because 'nn_leapy':30 our years are 360 days!
        NDAYS=360
        lg.info("We are running with NDAYS: "+ str(NDAYS))

        # ##-- calculate corresponding number of time steps for NEMO:
        # NIT000=`echo "$NITENDM1 + 1" | bc`
        # NITEND=`echo "$NITENDM1 + ${NDAYS} * 86400 / ${RN_DT}" | bc`

        # RN_DT=`grep "rn_rdt " namelist_nemo_GENERIC_${CONFIG} |cut -d '=' -f2 | cut -d '!' -f1 | sed -e "s/ //g"`
        nml = f90nml.read(nmlpath)
        RN_DT=nml['namdom']['rn_rdt']

        nml_patch={}
        if not os.path.exists(WORKDIR+'prod_nemo.db'):
            lg.info("First NEMO run, creating ./prod_nemo.db. Starting: "+"1 "+str(YEAR0)+" 0")

            NITENDM1=0
            NIT000=str(int(NITENDM1) + 1)
            NITEND=str(int(NITENDM1) + int(NDAYS) * 86400 / int(RN_DT))

            fileHandle = open (WORKDIR+ 'prod_nemo.db',"w" )
            fileHandle.write("0001 "+str(YEAR0)+" 0 \n")
            fileHandle.close()

            YEAR=YEAR0
            MONTH=01
            DAY=01

            NRUN=1

            # warning: can't do integer with leading zeros...
            # nml_patch['namrun']={'ln_rstart':False,'cn_exp':CONFIG+'_'+CASE,'nn_date0':00010101,'nn_rstctl':0,'nn_it000':int(NIT000),'nn_itend':int(NITEND),'nn_leapy':30}
            nml_patch['namrun']={'ln_rstart':False,'cn_exp':CONFIG+'_'+CASE,'nn_rstctl':0,'nn_it000':int(NIT000),'nn_itend':int(NITEND),'nn_leapy':30}
            nml_patch['namdom']={'nn_msh':1}

        else:
            # ncj's..
            # read NRUN YEAR MONTH DAY NITENDM1 << EOF
            # `tail -1 prod_nemo.db`
            fileHandle = open (WORKDIR+ 'prod_nemo.db',"r" )
            lineList = fileHandle.readlines()
            lineList=[r.rstrip() for r in lineList]

            #remove empty elements
            lineList = filter(None, lineList)
            fileHandle.close()

            NRUN,YEAR,NITENDM1=lineList[-1].split(' ')
            lg.info("./prod_nemo.db says, run to do is: " + str(lineList[-1]))

            NIT000=str(int(NITENDM1) + 1)
            NITEND=str(int(NITENDM1) + int(NDAYS) * 86400 / int(RN_DT))
            dummy,YEAR0,dummy2=lineList[0].split(' ')
            dummy,dummy2=None,None
            nml_patch['namrun']={'ln_rstart':True,'cn_exp':CONFIG+'_'+CASE,'nn_rstctl':2,'nn_it000':int(NIT000),'nn_itend':int(NITEND),'cn_ocerst_indir':WORKDIR+'OUTNEMO_'+str(int(NRUN)-1).zfill(4)+'/restarts/','nn_leapy':30,'cn_ocerst_in':CONFIG+'_'+CASE+'_'+str(NITENDM1)+'_restart_oce'}

            #check here to see if the restart files exist
            rfiles=sorted(glob.glob(WORKDIR+'OUTNEMO_'+str(int(NRUN)-1).zfill(4)+'/restarts/'+CONFIG+'_'+CASE+'_*_restart*.nc'))


            assert(rfiles!=[]),"E R R O R: Didn't find any NEMO restart files,STOP!"
	    lg.info("Found "+str(len(rfiles)) + " restart files, e.g. "+os.path.basename(rfiles[0]))
            rfiles=None

            if int(YEAR)>int(YEAR_MAX):
                lg.warning("We are stopping (as there's nothing to do, we've already done the required years)!")
                sys.exit()

            lg.info("Running from restart files: "+WORKDIR+'OUTNEMO_'+str(int(NRUN)-1).zfill(4)+'/restarts/'+CONFIG+'_'+CASE+'_'+str(NITENDM1)+'_restart*.nc')

        # print NIT000,NITEND 

        if FORCING_NUM==3 or FORCING_NUM==4:
            if not BISICLES_CPL:
                get_ISOMIP_timeslice(int(NRUN),WORKDIR)
            else:
                biscdir=WORKDIR+'OUTNEMO_'+str(NRUN).zfill(4)+'/'+'bisc/'
                mkdir(biscdir)
                if int(YEAR)==1:
                    get_ISOMIP_timeslice(int(NRUN),WORKDIR)
                else:
                    if os.path.exists(WORKDIR+'bathy_meter.nc'):
                        os.remove(WORKDIR+'bathy_meter.nc')
                        lg.warning("File: "+WORKDIR+'bathy_meter.nc' + ' removed.')

                    if os.path.exists(WORKDIR+'isf_draft_meter.nc'):
                        os.remove(WORKDIR+'isf_draft_meter.nc')
                        lg.warning("File: "+WORKDIR+'isf_draft_meter.nc' + ' removed.')

                    biscdir_prev=WORKDIR+'OUTNEMO_'+str(int(NRUN)-1).zfill(4)+'/'+'bisc/'

                    if FORCING_TYPE=='TYP':
                        shutil.copyfile(biscdir_prev+'bathy_isf_meter_TYP.nc',WORKDIR+'bathy_meter.nc')
                        shutil.copyfile(biscdir_prev+'bathy_isf_meter_TYP.nc',WORKDIR+'isf_draft_meter.nc')
                    elif FORCING_TYPE=='COM':
                        shutil.copyfile(biscdir_prev+'bathy_isfdraft_242.nc',WORKDIR+'bathy_meter.nc')
                        shutil.copyfile(biscdir_prev+'bathy_isfdraft_242.nc',WORKDIR+'isf_draft_meter.nc')
                    bisicles_restart=sorted(glob.glob(biscdir_prev+'chk.MMP.*.2d.hdf5'  ))
                    assert(bisicles_restart!=[]),"glob didn't find a bisicles_restart file!"
                    os.symlink(bisicles_restart[0], WORKDIR+'bisicles/chk.last')
                    lg.info("Using bisicles restart file: "+bisicles_restart[0])

            #always want a mesh_mask with the moving geometry experiments..
            nml_patch['namdom']={'nn_msh':1}

            if NRUN>1:
                nml_patch['namrun']['ln_iscpl']=True
                nml_patch['namsbc_iscpl']={'nn_drown':50} # this wasn't in the cfg but it seems to patch ok!

            if OCEANCORES==20:
                lg.info("Hard-wiring the proc-decomp for square workloads on 20 procs (normally used for TYP)") 
                nml_patch['nammpp']={}
                nml_patch['nammpp']['jpni']=2
                nml_patch['nammpp']['jpnj']=10
                nml_patch['nammpp']['jpnij']=20
            elif OCEANCORES==12:
                lg.info("Hard-wiring the proc-decomp for Antony's test-case of 12 cores") 
                #this ran on COM! But is slower than 24 cores on one node
                nml_patch['nammpp']={}
                nml_patch['nammpp']['jpni']=0
                nml_patch['nammpp']['jpnj']=0
                nml_patch['nammpp']['jpnij']=0

            elif OCEANCORES==24:
                lg.info("Hard-wiring the proc-decomp for square workloads on 24 procs (normally used for COM)") 
                nml_patch['nammpp']={}
                nml_patch['nammpp']['jpni']=12
                nml_patch['nammpp']['jpnj']=2
                nml_patch['nammpp']['jpnij']=24
            elif OCEANCORES==48:
                lg.info("Hard-wiring the proc-decomp for square workloads on 48 procs (normally used for COM)") 
                nml_patch['nammpp']={}
                # nml_patch['nammpp']['jpni']=24
                # nml_patch['nammpp']['jpnj']=2
                # nml_patch['nammpp']['jpnij']=48
                nml_patch['nammpp']['jpni']=0
                nml_patch['nammpp']['jpnj']=0
                nml_patch['nammpp']['jpnij']=0
                #this didn't work
            elif OCEANCORES==96:
                lg.info("Hard-wiring the proc-decomp for square workloads on 48 procs (normally used for COM)") 
                nml_patch['nammpp']={}
                # nml_patch['nammpp']['jpni']=24
                # nml_patch['nammpp']['jpnj']=4
                # nml_patch['nammpp']['jpnij']=96
                nml_patch['nammpp']['jpni']=0
                nml_patch['nammpp']['jpnj']=0
                nml_patch['nammpp']['jpnij']=0
                #this didn't work

        lg.info("")
        lg.info("Resulting patch for namelist_ref: "+str(nml_patch['namrun']))
        f90nml.patch(nmlpath, nml_patch, out_path=nmlpath+'_new')
        shutil.move(nmlpath+'_new', nmlpath)

        ###########################################################
        ###-- run
        
        lg.info("")
        lg.info("LAUNCHING the simulation for YEAR "+str(YEAR))

        # ln -s namelist namelist_ref

        subprocess.call('echo "-np '+str(OCEANCORES)+' ./nemo.exe" > app.conf',shell=True)
        subprocess.call('echo "-np '+str(XIOCORES) + ' ./xios_server.exe" >> app.conf',shell=True)

        #think Goggomobil!
        rnemo=WORKDIR+'GoGGoNEMO_'+str(NRUN).zfill(4)+'.sh'
        with ctx.closing(open(rnemo,'w')) as handle:
            handle.write('#!/bin/bash '+'\n')
            # handle.write('set -x'+'\n')
            handle.write('export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)'+'\n')
            handle.write('export OMP_NUM_THREADS=1'+'\n')
            handle.write('cd '+WORKDIR+'\n')
            handle.write('ulimit -c unlimited'+'\n')
            handle.write('ulimit -s unlimited'+'\n')
            # handle.write('pwd'+'\n')

            #normal nemo run
            # handle.write('aprun -b -n '+str(XIOCORES)+' -N '+str(XIOCORES)+' ./xios_server.exe : -n '+ str(OCEANCORES)+ ' -N 24 ./nemo.exe'+'\n')
            if OCEANCORES>=24:
                handle.write('aprun -n '+ str(OCEANCORES)+ ' -N ' +str(24)+ ' ./nemo.exe'+'\n')
            else:
                handle.write('aprun -n '+ str(OCEANCORES)+ ' -N ' +str(OCEANCORES)+ ' ./nemo.exe'+'\n')

            handle.write(''+'\n')
            handle.write('echo "NEMO run finished, will now try and re-assemble restart and mesh_mask files..."'+'\n')
            handle.write(''+'\n')

            if str(NRUN)=='1':
                rebuild_mesh_mask(handle)
            elif FORCING_NUM==3 or FORCING_NUM==4:
                rebuild_mesh_mask(handle)

            rone=CONFIG+'_'+CASE+'_'+NITEND.zfill(8)+'_'+'restart_oce.nc'
            # rone_ice=CONFIG+'_'+CASE+'_'+NITEND.zfill(8)+'_'+'restart_ice.nc'
            # initone='output.init.nc'

            rone_star=CONFIG+'_'+CASE+'_'+NITEND.zfill(8)+'_'+'restart_oce_????.nc'
            # rone_ice_star=CONFIG+'_'+CASE+'_'+NITEND.zfill(8)+'_'+'restart_ice_????.nc'
            # initone_star='output.init_????.nc'

            for f,f_star in zip([rone],[rone_star]):
                handle.write(''+'\n')
                handle.write('echo "Re-combining: '+f+'"'+'\n')
                handle.write('mkdir tempo '+'\n')
                handle.write('mv '+f_star +' tempo/'+'\n')
                handle.write('cd tempo '+'\n')

                #the -b makes aprun, run the executable from where it is 'locally'
                #not sure why but I never got a symlink to work for this
                handle.write('aprun -b '+RBUILD_NEMO+' '+f[:-3]+' '+str(OCEANCORES)+'\n')

                handle.write('if [ -f ' +f+' ]; then'+'\n')
                handle.write('   echo "File: '+f+' reassembled ok"'+'\n')
                handle.write('   mv '+f+' ..'+'\n')
                handle.write('   rm '+f_star+'\n')
                handle.write('else'+'\n')
                handle.write('   echo "!@#$% PROBLEM WITH RE-ASSEMBLY OF FILE '+f+'"\n')
                handle.write('   echo ">>>>>>>>>> STOP !"'+'\n')
                handle.write('   exit 1'+'\n')
                handle.write('fi'+'\n')

                handle.write('cd ..'+'\n')
                handle.write('rm -r tempo/'+'\n')

            if BISICLES_CPL:
                handle.write(''+'\n')
                handle.write('echo "NEMO stuff finished, will now try and do the BISICLES stuff"'+'\n')

                handle.write(''+'\n')
                handle.write('# make a netcdf file containing the annual average NEMO shelf melt variables in the units BISICLES wants'+'\n')
                handle.write('module load cdo'+'\n')
                handle.write('module load python-compute'+'\n')
                handle.write('export PYTHONPATH=.:$PYTHONPATH'+'\n')
                handle.write('module unload cray-netcdf-hdf5parallel/4.4.1.1;module unload cray-hdf5-parallel/1.10.0.1;module load nco'+'\n')
                handle.write('module load pc-netcdf4-python'+'\n')
                handle.write('module load pc-scipy'+'\n')
                handle.write('cd bisicles'+'\n')
                handle.write('######################################################'+'\n')
                handle.write('#  convert NEMO output into BISICLES readable input  #'+'\n')
                handle.write('######################################################'+'\n')
                handle.write('#namely: nemoout4bisicles.hdf5'+'\n')
                handle.write('echo "Looking for last grid_T NEMO output file"'+'\n')
                handle.write('LAST_GRID_T_FILE=`ls '+WORKDIR+CONFIG+'_'+CASE+'_1m'+'*_grid_T.nc| tail -1`'+'\n')
                handle.write('echo "Found: ${LAST_GRID_T_FILE}"'+'\n')
                handle.write('chmod u+rwx ${LAST_GRID_T_FILE}'  +'\n')
                handle.write(''+'\n')

                if int(YEAR)==1:
                    # handle.write('LAST_BISICLES_RESTART='+WORKDIR+'bisicles/chk.init'+'\n')
                    handle.write('LAST_BISICLES_RESTART='+'chk.init'+'\n')
                else:
                    handle.write('LAST_BISICLES_RESTART='+'chk.last'+'\n')

                handle.write('#get melt rate/sub-shelf latent heating'+'\n')
                handle.write('ncks -Ov meltRate,sohflisf $LAST_GRID_T_FILE tmp2.nc'+'\n')
                handle.write("#average all the time-entries to get 'annual' (we hope!) average"+'\n')
                handle.write('ncra -O tmp2.nc tmp.nc'+'\n')
                handle.write('#change variable names/units into what bisicles wants'+'\n')
                handle.write('NDAYS='+str(NDAYS)+'\n')
                handle.write('YEAR='+str(YEAR)+'\n')
                handle.write('ncap2 -Os "sowflisf=double(meltRate)*60*60*24*${NDAYS}/1e3" tmp.nc tmp2.nc'+'\n')
                handle.write('ncap2 -Os "sohflisf=double(sohflisf)*60*60*24*${NDAYS}" tmp2.nc nple3.nc'+'\n')

                if FORCING_TYPE=='TYP':
                    # robin email (Fri, Jan 25, 2:49 PM)
                    # after NEMO runs:
                    # a) nco: add some netCDF masking to nple3.nc so the regridding only
                    # touches the active NEMO domain

                    # b) python: zero out melt fluxes where the ice is very thin (prevents
                    # burning holes through the ice. This wasn't a problem in COM, it seems)

                    # c) cdo: remap NEMO melt onto the BISICLES grid

                    # after BISICLES runs, there was also

                    # d) cdo: remap BISICLES geometry onto NEMO grid

                    # e) python: rather than use (Xylar's) bisiclesToSTDGeom.py and (my)
                    # expand_geom_2d.py, for TYP I had a different script to change the
                    # variable names and things so NEMO could read it.

                    handle.write('ncap2 -Os "sohflisf=double(sohflisf)*60*60*24*${NDAYS}" tmp2.nc nple3.nc'+'\n')
                    handle.write('#############COULD DO WITH FORMALLY MASKING nple3.nc TO AVOID BIASSING IN edge 0s######'+'\n')
                    handle.write('ncatted -a _FillValue,sowflisf,m,f,0 nple3.nc'+'\n')
                    handle.write('ncatted -a missing_value,sowflisf,m,f,0 nple3.nc'+'\n')
                    handle.write('ncatted -a missing_value,sohflisf,m,f,0 nple3.nc'+'\n')
                    handle.write('ncatted -a _FillValue,sohflisf,m,f,0 nple3.nc'+'\n')
                    handle.write('########################################################################################'+'\n')
                    handle.write('#tries to enforce 0 melt in places the BISICLES isf_draft (rather than'+'\n')
                    handle.write('#the mesh_mask) says are verging on the too-thin'+'\n')
                    handle.write('#NB zero_thin_melt assumes you have the isf_draft_meter.nc available in the current directory'+'\n')
                    handle.write('module load pc-matplotlib '+'\n')
                    handle.write('python zero_thin_melt.py'+'\n')
                    handle.write('#remap onto the BISICLES grid'+'\n')
                    handle.write('ln -s $input_MISOMIP/gridfile_NEMO_MISOMIP_TYP.txt .'+'\n')
                    handle.write('ln -s $input_MISOMIP/gridfile_BISICLES_MISOMIP1km.txt .'+'\n')
                    handle.write('cdo remapcon,gridfile_BISICLES_MISOMIP1km.txt -setgrid,gridfile_NEMO_MISOMIP_TYP.txt nple3.nc nemo_melt_1km.nc'+'\n')


                    # TODO
                    # ?_bike*dump files
                    handle.write('python goxy_toBIKE-TYP.py'+'\n')
                elif FORCING_TYPE=='COM':

                    handle.write('##chop off the border and change the axes to BISICLES cartesian'+'\n')
                    handle.write('python goxy_toBIKE-COM.py'+'\n')


                # BISICLES runs the same regardless of COM/TYP
                handle.write('##convert it to BISICLES hdf5 format'+'\n')
                handle.write('nctoamr2d.Linux.64.CC.ftn.OPT.INTEL.ex nemoout4bisicles.nc nemoout4bisicles.hdf5 MELT_REGRID HEAT_REGRID'+'\n')
                handle.write('##clean up'+'\n')
                handle.write('rm nple3.nc tmp2.nc tmp.nc'+'\n')
                handle.write('#inputs.MMP needs to have the correct path to the restart file and the main.maxTime where main.maxTime is the number of years'+'\n')
                handle.write('sed -e "s/EENNDDDDAATTEE/${YEAR}/g ; s/RREESSTTAARRTTFFIILLEE/${LAST_BISICLES_RESTART}/g" inputs.MMP_template > inputs.MMP'+'\n')
                handle.write('#bisicles outputs, .X is the proc number'+'\n')
                handle.write('rm pout.MPP.*'+'\n')
                handle.write('aprun -n 1 bisicles.exe inputs.MMP'+'\n')
                handle.write('##find last BISICLES plot file'+'\n')
                handle.write('LAST_BISICLES_PLOT=`ls -rt plot* | tail -1`'+'\n')
                handle.write("BISI_SUCESS=`grep 'AmrIce::run finished' pout.MMP.0`"+'\n')
                handle.write('if [ -z "$BISI_SUCESS" ]'+'\n')
                handle.write('then'+'\n')
                handle.write('    echo "E R R O R"'+'\n')
                handle.write('    echo "\$BISI_SUCESS is empty"'+'\n')
                handle.write('    touch killnemo'+'\n')
                handle.write('    exit 1'+'\n')
                handle.write('else'+'\n')
                handle.write('    echo "\$BISI_SUCESS is NOT empty, BISICLES run finished successfully"'+'\n')
                handle.write('    #echo ${BISI_SUCESS}'+'\n')
                handle.write('fi'+'\n')
                handle.write('echo "running flatten2d thing"'+'\n')
                handle.write('#makes blex'+'\n')
                handle.write('flatten2d.Linux.64.CC.ftn.OPT.INTEL.ex $LAST_BISICLES_PLOT bplex.nc 2'+'\n')

                if FORCING_TYPE=='TYP':

                    handle.write('cdo remapcon,gridfile_NEMO_MISOMIP_TYP.txt -setgrid,gridfile_BISICLES_MISOMIP1km.txt bplex.nc bike_geom_TYP.nc'+'\n')
                    handle.write('python $input_MISOMIP/process_mismipgeom.py'+'\n')
                    # handle.write('cp bathy_isf_meter_TYP.nc <wherever the next nemo will need it>'+'\n')
                    handle.write('#should have created bathy_isf_meter_TYP.nc'+'\n')
                    handle.write('#rm intermediate files'+'\n')
                    handle.write('rm nemoout4bisicles.nc chk.init bplex.nc inputs.MMP nemoout4bisicles.hdf5 chk.last'+'\n')
                    
                elif FORCING_TYPE=='COM':
                    handle.write('echo "bisiclesToSTDGeom.py"'+'\n')
                    handle.write('#Xylars BISICLES output --> isf_draft'+'\n')
                    handle.write('python bisiclesToSTDGeom.py'+'\n')
                    handle.write('echo "expand_geom_2d.py"'+'\n')
                    handle.write('#pads around the outside back into NEMO'+'\n')
                    handle.write('python expand_geom_2d.py'+'\n')
                    handle.write('#should have created bathy_isfdraft_242.nc and bathy_isfdraft.nc'+'\n')
                    handle.write('#rm intermediate files'+'\n')
                    handle.write('rm nemoout4bisicles.nc chk.init bplex.nc inputs.MMP nemoout4bisicles.hdf5 chk.last'+'\n')

        subprocess.call('chmod u+x '+rnemo,shell=True)

        lg.info("Launching NEMO with the following script: ")
        lg.info(rnemo)
        lg.info("")
        subprocess.call(rnemo,shell=True)

        #making up some fake outputs...
        #subprocess.call("touch WED025_CORE_13_1m_19760101_19850830_grid_T.nc", shell=True)
        #if NRUN==1:
        #    subprocess.call("touch WED025_CORE_13_"+NITEND.zfill(8)+"_restart_oce_0127.nc", shell=True)
        #    subprocess.call("touch ocean.output", shell=True)
        #else:
        #    subprocess.call("touch WED025_CORE_13_"+(str(int(NITEND)+int(NITENDM1))).zfill(8)+"_restart_oce_0127.nc", shell=True)
        #    subprocess.call("touch ocean.output", shell=True)

        # ##-- compress output files:
        
        odir=WORKDIR+'OUTNEMO_'+str(NRUN).zfill(4)+'/'
        rdir=odir + 'restarts/'
        initdir=odir + 'inits/'
        if not os.path.exists(odir):
            mkdir(odir)
        if not os.path.exists(rdir):
            mkdir(rdir)

        #bisicles error trap / move bisicles output files
        if BISICLES_CPL:
            if os.path.exists(WORKDIR+'bisicles/killnemo'):
                lg.warning("We are stopping (as we think something went wrong with bisicles...")
                sys.exit()

            #move everything important to OUTNEMO
            if FORCING_TYPE=='TYP':
                shutil.move(WORKDIR+'bisicles/bathy_isf_meter_TYP.nc', biscdir)
            elif FORCING_TYPE=='COM':
                shutil.move(WORKDIR+'bisicles/bathy_isfdraft_242.nc', biscdir)
                shutil.move(WORKDIR+'bisicles/bathy_isfdraft.nc', biscdir)
            shutil.move(WORKDIR+'bisicles/pout.MMP.0', biscdir)

            bisicles_restart=sorted(glob.glob(WORKDIR+'bisicles/chk.MMP.*.2d.hdf5'  ))
            shutil.move(bisicles_restart[0], biscdir)
            bisicles_output=sorted(glob.glob(WORKDIR+'bisicles/plot.MMP.*.2d.hdf5'  ))
            shutil.move(bisicles_output[0], biscdir)

        ofiles=sorted(glob.glob(WORKDIR+CONFIG+'_'+CASE+'_[1-5][dhm]_*nc'))
        rfiles=sorted(glob.glob(WORKDIR+CONFIG+'_'+CASE+'_*_restart*.nc'))

        #something bad maybe happened let's see if there's a NEMO error..
        if ofiles==[] or rfiles==[]:
            lg.error("")
            lg.error("No output or restart files, looking for a NEMO error...")
            p = subprocess.Popen("grep -A 4 '\''E R R'\'' ocean.output", stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            lg.info(output)


        assert(ofiles!=[]),"E R R O R: Didn't find any NEMO output files, STOP!"
        assert(rfiles!=[]),"E R R O R: Didn't find any NEMO restart files,STOP!"

        #move the output/restart and initfiles (if they existed)
        for f in ofiles:
            shutil.move(f, odir+os.path.basename(f))

        for f in rfiles:
            shutil.move(f, rdir+os.path.basename(f))

        #for evolving cavity cases keep mesh_mask and bathy/isf
        if FORCING_NUM==3 or FORCING_NUM==4:
            shutil.move(WORKDIR+'isf_draft_meter.nc', odir+'isf_draft_meter'+'_'+str(YEAR).zfill(4)+'.nc')
            shutil.move(WORKDIR+'bathy_meter.nc', odir+'bathy_meter'+'_'+str(YEAR).zfill(4)+'.nc')
            shutil.move(WORKDIR+'mesh_mask.nc', odir+'mesh_mask'+'_'+str(YEAR).zfill(4)+'.nc')

        # initfiles=sorted(glob.glob(WORKDIR+'output.init*.nc'))
        # if initfiles==[]: lg.warning("Didn't find any NEMO init files.")
        # if initfiles!=[]:
            # if not os.path.exists(initdir):
                # mkdir(initdir)

            # for f in initfiles:
                # shutil.move(f, initdir+os.path.basename(f))

        ##########################################################
        ##-- prepare next run if every little thing went all right (if not, we should have crashed by now via the globs)
        m = re.search(WORKDIR+CONFIG+'_'+CASE+"_(.*)_restart",rfiles[0])

        if m:
            LAST_RESTART_NIT=m.groups()[0]
        else:
            lg.error("Couldn't work out (regexfail) last restart tstep..")

        # YEARf=`expr $YEAR + 1`
        YEARf=str(int(YEAR)+1)
        MONTHf=1
        DAYf=1


        lg.info("Last restart created at ocean time step "+LAST_RESTART_NIT)
        lg.info("  ---> writting this date in prod_nemo.db")
        lg.info(" ")
        subprocess.call("echo "+LAST_RESTART_NIT+" > restart_nit.txt", shell=True)

        fileHandle = open (WORKDIR+ 'prod_nemo.db',"r" )
        lineList = fileHandle.readlines()
        lineList=[r.rstrip() for r in lineList]
        lineList = filter(None, lineList)

        lineList[-1]=' '.join(lineList[-1].split(' ')[:-1])+' '+LAST_RESTART_NIT+'\n'

        #specify the starting point for the next run (because the last one finished okay)
        NexRUN=str(int(NRUN)+1).zfill(4)
        next_run=str(NexRUN)+' '+str(YEARf)+' '+LAST_RESTART_NIT
        lineList.append(next_run)

        fileHandle_two = open (WORKDIR+ 'prod_nemo_two.db',"w" )
        for line in lineList:
            if '\n' not in line:
                line=line+'\n'
            fileHandle_two.write(line) 

        fileHandle.close()
        fileHandle_two.close()
        shutil.move(WORKDIR+'prod_nemo_two.db',WORKDIR+'prod_nemo.db')

        # ##########################################################
        # ##-- send outputs and restarts to storage disk
        
        # shutil.move('namelist','namelist.'+NRUN)
        shutil.copyfile(nmlpath, odir+'namelist.'+str(NRUN).zfill(4) ) #we need it for the next year..
        # shutil.copyfile(nmlpath_ice, odir+'namelist_ice_ref.'+str(NRUN).zfill(4) ) #we need it for the next year..
        shutil.move('ocean.output',odir+'ocean.output.'+str(NRUN).zfill(4))
        shutil.move(rnemo,odir+'GoGGoNEMO_'+str(NRUN).zfill(4)+'.sh')

        # update location of ofiles / rfiles/ initfiles
	ofiles=[odir+os.path.basename(f) for f in ofiles]
	rfiles=[rdir+os.path.basename(f) for f in rfiles]
        # if initfiles!=[]:
            # initfiles=[odir+os.path.basename(f) for f in initfiles]

        # #qsub compress_nemo_${NRUN}.sh
        with ctx.closing(open(WORKDIR+'cnemo_'+str(NRUN).zfill(4)+'.sh','w')) as handle:
            handle.write('#!/bin/bash --login'+'\n')
            handle.write('#PBS -l select=serial=true:ncpus=1'+'\n')
            handle.write('#PBS -l walltime=01:00:00'+'\n')
            handle.write('#PBS -A n02-FISSA'+'\n')
            handle.write('# Make sure any symbolic links are resolved to absolute path'+'\n')
            handle.write('export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)'+'\n')
            handle.write('#load modules'+'\n')
            handle.write('module load cray-netcdf-hdf5parallel/4.4.1.1 '+'\n')
            handle.write('module load cray-hdf5-parallel/1.10.0.1'+'\n')
            handle.write('module swap PrgEnv-cray PrgEnv-intel'+'\n')

            handle.write(''+'\n')
            handle.write('cd '+WORKDIR+'\n')

            #compression step ..
	    handle.write('#compress ofiles'+ '\n')
            for f in ofiles:
                handle.write(''+ '\n')
		handle.write('#Doing file: '+os.path.basename(f)+ '\n')
		tmpf=' '+os.path.dirname(f)+'/tmp.nc'
                handle.write('nccopy -d 5 '+f+ tmpf +' \n')

                handle.write('if [ -f ' +tmpf+' ]; then'+'\n')
                handle.write('   mv -f '+tmpf+' '+f+'\n')
                handle.write('else'+'\n')
                handle.write('   echo "!@#$% PROBLEM WITH COMPRESSION OF FILE '+f+'"\n')
                handle.write('   echo ">>>>>>>>>> STOP !"'+'\n')
                handle.write('   exit'+'\n')
                handle.write('fi'+'\n')

	    # handle.write('# ------ '+ '\n')
	    # handle.write('#compress rfiles'+ '\n')
            # for f in rfiles:
                # handle.write(''+ '\n')
		# handle.write('#Doing file: '+os.path.basename(f)+ '\n')
		# tmpf=' '+os.path.dirname(f)+'/tmp.nc'
                # handle.write('nccopy -d 5 '+f+ tmpf +' \n')

                # handle.write('if [ -f ' +tmpf+' ]; then'+'\n')
                # handle.write('   mv -f '+tmpf+' '+f+'\n')
                # handle.write('else'+'\n')
                # handle.write('   echo "!@#$% PROBLEM WITH COMPRESSION OF FILE"'+f+'\n')
                # handle.write('   echo ">>>>>>>>>> STOP !"'+'\n')
                # handle.write('   exit'+'\n')
                # handle.write('fi'+'\n')

	    handle.write(''+ '\n')
	    handle.write('# ------ '+ '\n')
            #write to RDF
	    handle.write('echo "Finished compressing, WRITE to RDF"'+ '\n')

            handle.write('mkdir -p '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/'+'\n')
            handle.write('mv -v '+ odir + '*.nc '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/'+'\n')
            handle.write('mv -v '+ odir + 'namelist* '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/'+'\n')
            handle.write('mv -v '+ odir + 'ocean* '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/'+'\n')
            handle.write('mv -v '+ odir+'GoGGoNEMO_'+str(NRUN).zfill(4)+'.sh '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/'+'\n')

            if str(NRUN)=='1':
                handle.write('mv -v '+ WORKDIR + 'mesh_mask.nc '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+'\n')

            #bisicles copy/move outputs
            if BISICLES_CPL:
                handle.write('mv -v '+ biscdir + 'plot.MMP* '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/'+'\n')
                handle.write('cp -v '+ biscdir + 'chk.MMP* '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/'+'\n')
                handle.write('mv -v '+ biscdir + 'pout.MMP.0 '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/'+'\n')
                if FORCING_TYPE=='TYP':
                    handle.write('cp -v '+ biscdir + 'bathy_isf_meter_TYP.nc '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/bathy_isfdraft_242_bisicles.nc'+'\n')
                elif FORCING_TYPE=='COM':
                    handle.write('cp -v '+ biscdir + 'bathy_isfdraft_242.nc '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/bathy_isfdraft_242_bisicles.nc'+'\n')
                    handle.write('mv -v '+ biscdir + 'bathy_isfdraft.nc '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/bathy_isfdraft_bisicles.nc'+'\n')


            #r'sync the run to the shared folder after every year it goes... (so Antony/Robin can see it..)
            handle.write('rsync -avz --progress /nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+' ' + '/nerc/n02/shared/chbull/MISOMIP'+'\n')
            handle.write('chmod a+rwx '+'/nerc/n02/shared/chbull/MISOMIP/'+CONFIG+'_'+CASE+'/ '+'\n')
            handle.write('chmod a+rwx '+'/nerc/n02/shared/chbull/MISOMIP/'+CONFIG+'_'+CASE+'/* '+'\n')
            handle.write('chmod a+rwx '+'/nerc/n02/shared/chbull/MISOMIP/'+CONFIG+'_'+CASE+'/*/* '+'\n')
            
        subprocess.call('chmod u+x '+WORKDIR+'cnemo_'+str(NRUN).zfill(4)+'.sh',shell=True)
        subprocess.call('qsub '+WORKDIR+'cnemo_'+str(NRUN).zfill(4)+'.sh',shell=True)

	# we will keep the restarts in the run dir until we're happy with all the outputs..
	if not os.path.exists(WORKDIR+'mv_restarts_rdf.sh'):
	    append_write = 'w' # make a new file if not
	    frestart= open(WORKDIR+'mv_restarts_rdf.sh',append_write)
            frestart.write('#!/bin/bash'+'\n')
            frestart.write('#this is a manual step to be done later'+'\n')
	    frestart.write(''+'\n')
	    
	else:
	    append_write = 'a' # append if already exists
	    frestart= open(WORKDIR+'mv_restarts_rdf.sh',append_write)

	frestart.write(''+'\n')
        frestart.write('mkdir -p '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/restarts/'+'\n')
	frestart.write('mv -v '+rdir+'*.nc '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/restarts/'+'\n')
	frestart.write('#mv -v '+'/nerc/n02/n02/chbull/RawData/NEMO/'+CONFIG+'_'+CASE+'/'+str(YEAR).zfill(4)+'/restarts/ '+rdir+' # to undo \n')
	frestart.write(''+'\n')
        subprocess.call('chmod u+x '+WORKDIR+'mv_restarts_rdf.sh',shell=True)
	frestart.close()

        #kick on for another year.
        YEAR=str(int(YEAR)+1)

    lg.info('')
    lg.info('All done! Consider moving your restarts to the RDF, see: '+WORKDIR+'mv_restarts_rdf.sh')
    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
