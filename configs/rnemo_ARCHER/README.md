# README 

### What is this repository for? 
Run files for ARCHER for MISOMIP

### Notes
Files needed inside: /fs2/n02/n02/chbull/nemo/bld_configs/input_MISOMIP are:

/fs2/n02/n02/chbull/nemo/bld_configs/input_MISOMIP/BISICLES:
chk.isomip24.spin.ssa.l3.Chombo.A2e-17.constfriction.a0.3.098006.2d.hdf5  flatten2d.Linux.64.CC.ftn.OPT.INTEL.ex
driver2d.Linux.64.CC.ftn.OPT.MPI.GNU.DY.ex                                nctoamr2d.Linux.64.CC.ftn.OPT.INTEL.ex

/fs2/n02/n02/chbull/nemo/bld_configs/input_MISOMIP/NEMO_COM:
isomip+_NEMO_expt1_242_geom.nc          isomip+_NEMO_expt3_242_geom_recalve.nc  nemo_base_COLD-NEWFIX.nc
isomip+_NEMO_expt2_242_geom_recalve.nc  isomip+_NEMO_expt4_242_geom_recalve.nc  nemo_base_WARM-NEWFIX.nc

/fs2/n02/n02/chbull/nemo/bld_configs/input_MISOMIP/NEMO_TYP:
bathy_isf_meter_expt1_TYP_CALVE.nc  bathy_isf_meter_expt3_TYP_CALVE.nc  nemo_base_COLD-NEWFIX.nc
bathy_isf_meter_expt2_TYP_CALVE.nc  bathy_isf_meter_expt4_TYP_CALVE.nc  nemo_base_WARM-NEWFIX.nc

### Instructions to run an experiment
-edit production_nemo_ARCHER.sh:

    change RDIR="/fs2/n02/n02/chbull/nemo/run" to where you want the run to go from.
    Fix links to /fs2/n02/shared/chbull/Ocean3TEMP/TESTCASE_misomip/rebuild_nemo
    Fix line 152 to the place you cloned the git repo too (this path: /nerc/n02/n02/chbull/repos/misomip_bas/configs/rnemo_ARCHER/ )
    Change WCONFIG=/fs2/n02/n02/chbull/nemo/bld_configs/input_MISOMIP to your input dir
    edit NEMO executable path 
    edit XIOS executable path 
    Change STOCKDIR to a place you want the output to be archieved
    Change PROJ='n02-bas' to the relevant ARCHER group.

    Change for the run your doing:
        FORCING_TYPE=
        FORCING_NUM=
        YEAR_MAX=
        CONFIG=''
        CASE=''


If you want the script to loop on something faster than a year change NDAYS in run_nemo_GENERIC.py

Once you've done the above, run production_nemo_ARCHER.sh on a log-in node and cross your fingers...
