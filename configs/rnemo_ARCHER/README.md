# README 

### What is this repository for? 
Run files for ARCHER for MISOPMIP

### Notes
Files needed inside: /fs2/n02/n02/chbull/nemo/bld_configs/input_MISOMIP are:

NEMO_COM:
isomip+_NEMO_expt1_242_geom.nc
isomip+_NEMO_expt2_242_geom_recalve.nc
nemo_base_COLD-NEWFIX.nc
nemo_base_WARM-NEWFIX.nc

NEMO_TYP:
bathy_isf_meter_expt1_TYP_CALVE.nc
bathy_isf_meter_expt2_TYP_CALVE.nc
nemo_base_COLD-NEWFIX.nc
nemo_base_WARM-NEWFIX.nc

### Instructions to run an experiment
- edit header variables in: production_nemo_ARCHER.sh then run on log-in node
