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

FORCING_NAME='yyyy'
FORCING_NUM=kkkk
PROJ='pppp'
WORKDIR='wwww'+'/'
STOCKDIR='ssss'
CONFIG='cccc'
CASE='oooo'
DESC='zzzz'
RBUILD_NEMO='jjjj'
YEAR0=Y0Y0
YEAR_MAX=YMYM

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

        NDAYS=5
        # NDAYS=32
        NDAYS=365
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
            get_ISOMIP_timeslice(int(NRUN),WORKDIR)
            #always want a mesh_mask with the moving geometry experiments..
            nml_patch['namdom']={'nn_msh':1}

            if NRUN>1:
                nml_patch['namrun']['ln_iscpl']=True
                nml_patch['namsbc_iscpl']={'nn_drown':50} # this wasn't in the cfg but it seems to patch ok!

      
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
        subprocess.call('echo "-np '+str(XIOCORES) +' ./xios_server.exe" >> app.conf',shell=True)

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
