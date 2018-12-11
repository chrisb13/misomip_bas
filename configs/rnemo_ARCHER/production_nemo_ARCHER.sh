#!/bin/bash
#   Author: Christopher Bull. 
#   Affiliation:  British Antarctic Survey
#                 Cambridge, UK
#   Contact: chbull@bas.ac.uk
#   Date created: Mon, 10 Dec 2018 13:44:52
#   Machine created on: SB2Vbox
#

##############################################
# This is the script to execute NEMO runs    #
##############################################

##-- User's choices START

CONFIG='nemo_ISOMIP_oceanCOM_10'
CASE='z'
RDIR="/fs2/n02/n02/chbull/nemo/run"
WORKDIR=${RDIR}/nemo_${CONFIG}_${CASE}

DEBUGJOB=FALSE
#DEBUGJOB=TRUE
if [ $DEBUGJOB = TRUE ]
    then
    echo "Running a SHORT debug job"
    NODES=1
    OCEANCORES=10
    XIOCORES=4
    RHOURS=0
  else
    #echo "normal job"
    #NODES=14
    #OCEANCORES=300
    #XIOCORES=4
    NODES=1
    OCEANCORES=10
    XIOCORES=5
    RHOURS=5
fi

PROJ='n02-FISSA'  

#avoid weird char'
DESC='Messing around trying to get ISOMIP Ocean3-4 experiments to go (third go looping on 10 days...)' 
YEAR0=1
YEAR_MAX=5
#DDMM

STOCKDIR="/nerc/n02/n02/chbull/RawData/NEMO"  #- restart and output directory on rdf

WCONFIG=/fs2/n02/n02/chbull/nemo/bld_configs/input_MISOMIP

#change the case name too!
FORCING_TYPE=COM
#FORCING_TYPE=TYP

FORCING_NUM=0

FORCING=/work/n01/shared/core2

NEMOdir="/fs2/n02/n02/chbull/nemo/models/MergedCode_9321_flx9855_remap9853_divgcorr9845_shlat9864"

#make sure you've compiled this!
RBUILD_NEMO=${NEMOdir}/TOOLS/REBUILD_NEMO/rebuild_nemo

DATE=`date '+%Y-%m-%d %H:%M:%S'`

##-- User's choices END

##############################################
##-- initializations

echo "****************************************************"
echo "*          NEMO SIMULATION                          "
echo "*   project $PROJ                                   "
echo "*   config  $CONFIG                                 "
echo "*   wconfig $WCONFIG                                "
echo "*   case    $CASE                                   "
echo "*   desc    $DESC                                   "
echo "****************************************************"

############################################################
##-- prepare run dir

#some hacks (from nico) to make the sed subs work..
STOCKDIR2=`echo $STOCKDIR |sed -e "s/\//\\\\\\\\\//g"`
WORKDIR2=`echo $WORKDIR  |sed -e  "s/\//\\\\\\\\\//g"`
RBUILD_NEMO2=`echo $RBUILD_NEMO  |sed -e  "s/\//\\\\\\\\\//g"`

echo ""
echo "We are using wconfig: ${WCONFIG}"
echo ""

#create run folder
if [ -d "$WORKDIR" ]; then
    echo $WORKDIR " already exists, so we will try and re-start.."

  else
    echo $WORKDIR " does not exist, so we will create it.."
    # create run files for first run...
    mkdir -p ${WORKDIR}
    #mkdir -p ${WORKDIR}/inputs

    cd ${WORKDIR}

    cat << EOF > ./README
    *****************************************************
    *          NEMO SIMULATION                          *
    *   project   $PROJ                                 *
    *   config    $CONFIG                               *
    *   case      $CASE                                 *
    *   Desc      $DESC                                 *
    *   Date      $DATE                                 *
    *                                                   *
    *   User's choices:                                 *
    *   PROJ      $PROJ                                 *
    *   CONFIG    $CONFIG                               *
    *   CASE      $CASE                                 *
    *   YEAR0     $YEAR0                                *
    *   YEAR_MAX  $YEAR_MAX                             *
    *   RDIR      $RDIR                                 *
    *   WORKDIR   $WORKDIR                              *
    *   STOCKDIR  $STOCKDIR                             *
    *   INPUTDIR  $INPUTDIR                             *
    *   WCONFIG   $WCONFIG                              *
    *   FORCING   $FORCING                              *
    *   FORCING_TYPE   $FORCING_TYPE                              *
    *   NEMOdir   $NEMOdir                              *
    *****************************************************
EOF

    cat << EOF > ./env_rec
    date=$(date)
    echo $date

    #record of current env:

    ENV=$(env)
    echo $ENV
EOF

    #nemo and xios
    #ln -s ${NEMOdir}/CONFIG/${CONFIG}/BLD/bin/nemo.exe nemo.exe
    ln -s /fs2/n02/n02/chbull/nemo/models/MergedCode_9321_flx9855_remap9853_divgcorr9845_shlat9864/NEMOGCM/CONFIG/ISOMIP/BLD/bin/nemo.exe nemo.exe

    #ln -s /fs2/n02/n02/chbull/nemo/models/XIOS/bin/xios_server.exe xios_server.exe
    ln -s /fs2/n02/n02/chbull/nemo/models/XIOSv1/bin/xios_server.exe xios_server.exe
    
    ##cp template: namelists, *.xml etc
    cp --preserve=links /nerc/n02/n02/chbull/repos/misomip_bas/configs/rnemo_ARCHER/* ${WORKDIR}

    echo "We are using config type: ${FORCING_TYPE}"
    echo "We are doing ocean number: ${FORCING_NUM}"
    if [ ${FORCING_TYPE} = "COM" ]; then
        OCEANCORES=24
        if [ ${FORCING_NUM} -eq 0 ]; then
            ln -s ${WCONFIG}/NEMO_COM/isomip+_NEMO_expt1_242_geom.nc isf_draft_meter.nc
            ln -s ${WCONFIG}/NEMO_COM/isomip+_NEMO_expt1_242_geom.nc bathy_meter.nc

            ln -s ${WCONFIG}/NEMO_COM/nemo_base_WARM-NEWFIX.nc TS_init.nc
            ln -s ${WCONFIG}/NEMO_COM/nemo_base_WARM-NEWFIX.nc resto.nc

            ln -s namelist_ref_COM_0 namelist_ref
            ln -s namelist_cfg_COM_0 namelist_cfg
        elif [ ${FORCING_NUM} -eq 1 ]; then
            ln -s ${WCONFIG}/NEMO_COM/isomip+_NEMO_expt1_242_geom.nc isf_draft_meter.nc
            ln -s ${WCONFIG}/NEMO_COM/isomip+_NEMO_expt1_242_geom.nc bathy_meter.nc

            ln -s ${WCONFIG}/NEMO_COM/nemo_base_COLD-NEWFIX.nc TS_init.nc
            ln -s ${WCONFIG}/NEMO_COM/nemo_base_WARM-NEWFIX.nc resto.nc

            ln -s namelist_ref_COM_1 namelist_ref
            ln -s namelist_cfg_COM_1 namelist_cfg
        elif [ ${FORCING_NUM} -eq 2 ]; then
            ln -s ${WCONFIG}/NEMO_COM/isomip+_NEMO_expt2_242_geom_recalve.nc isf_draft_meter.nc
            ln -s ${WCONFIG}/NEMO_COM/isomip+_NEMO_expt2_242_geom_recalve.nc bathy_meter.nc

            ln -s ${WCONFIG}/NEMO_COM/nemo_base_WARM-NEWFIX.nc TS_init.nc
            ln -s ${WCONFIG}/NEMO_COM/nemo_base_COLD-NEWFIX.nc resto.nc

            ln -s namelist_ref_COM_2 namelist_ref
            ln -s namelist_cfg_COM_2 namelist_cfg
        fi 
    elif [ ${FORCING_TYPE} = "TYP" ]; then
        OCEANCORES=10
        if [ ${FORCING_NUM} -eq 0 ]; then
            ln -s ${WCONFIG}/NEMO_TYP/bathy_isf_meter_expt1_TYP_CALVE.nc isf_draft_meter.nc
            ln -s ${WCONFIG}/NEMO_TYP/bathy_isf_meter_expt1_TYP_CALVE.nc bathy_meter.nc

            ln -s ${WCONFIG}/NEMO_TYP/nemo_base_WARM-NEWFIX.nc TS_init.nc
            ln -s ${WCONFIG}/NEMO_TYP/nemo_base_WARM-NEWFIX.nc  resto.nc

            ln -s namelist_ref_TYP_0 namelist_ref
            ln -s namelist_cfg_TYP_0 namelist_cfg

        elif [ ${FORCING_NUM} -eq 1 ]; then
            ln -s ${WCONFIG}/NEMO_TYP/bathy_isf_meter_expt1_TYP_CALVE.nc isf_draft_meter.nc
            ln -s ${WCONFIG}/NEMO_TYP/bathy_isf_meter_expt1_TYP_CALVE.nc bathy_meter.nc

            ln -s ${WCONFIG}/NEMO_TYP/nemo_base_COLD-NEWFIX.nc TS_init.nc
            ln -s ${WCONFIG}/NEMO_TYP/nemo_base_WARM-NEWFIX.nc  resto.nc

            ln -s namelist_ref_TYP_1 namelist_ref
            ln -s namelist_cfg_TYP_1 namelist_cfg

        elif [ ${FORCING_NUM} -eq 2 ]; then
            ln -s ${WCONFIG}/NEMO_TYP/bathy_isf_meter_expt2_TYP_CALVE.nc isf_draft_meter.nc
            ln -s ${WCONFIG}/NEMO_TYP/bathy_isf_meter_expt2_TYP_CALVE.nc bathy_meter.nc

            ln -s ${WCONFIG}/NEMO_TYP/nemo_base_WARM-NEWFIX.nc TS_init.nc
            ln -s ${WCONFIG}/NEMO_TYP/nemo_base_COLD-NEWFIX.nc  resto.nc

            ln -s namelist_ref_TYP_2 namelist_ref
            ln -s namelist_cfg_TYP_2 namelist_cfg
        fi 

        #rm ${WORKDIR}/namelist_ref_*

    else
        echo "We are using forcing: ${FORCING_TYPE}"
        echo "E R R O R: I don't know what to do with this forcing type."
        exit
    fi 

fi

sed -e "s/pppp/${PROJ}/g ; s/ssss/${STOCKDIR2}/g ; s/wwww/${WORKDIR2}/g ; s/cccc/${CONFIG}/g ; s/oooo/${CASE}/g ; s/zzzz/${DESC}/g ; s/Y0Y0/${YEAR0}/g ; s/YMYM/${YEAR_MAX}/g ; s/eeee/${OCEANCORES}/g ; s/ffff/${XIOCORES}/g ; s/gggg/${NODES}/g ; s/hhhh/${RHOURS}/g; s/jjjj/${RBUILD_NEMO2}/g ; s/yyyy/${FORCING_TYPE}/g " ${WORKDIR}/run_nemo_GENERIC.py > ${WORKDIR}/GoGoNEMO.py

chmod +x ${WORKDIR}/GoGoNEMO.py 
#export PYTHONPATH=/work/n02/n02/chbull/anaconda2/pkgs;export PATH=/work/n02/n02/chbull/anaconda2/bin:$PATH;source activate root

if [ $DEBUGJOB = TRUE ]
    then
cat << 'EOF' > ${WORKDIR}/GoNEMO.sh
#!/bin/bash 
#!
#PBS -A pppp
#PBS -N WED025-log
#PBS -l select=gggg
#PBS -l walltime=00:20:00
#PBS -q short
export PYTHONPATH=/work/n02/n02/chbull/anaconda2/pkgs;export PATH=/work/n02/n02/chbull/anaconda2/bin:$PATH;source activate root
python wwww/GoGoNEMO.py
EOF
  else
cat << 'EOF' > ${WORKDIR}/GoNEMO.sh
#!/bin/bash 
#!
#PBS -A pppp
#PBS -N WED025-log
##PBS -j oe wwww/
#PBS -l select=gggg
#PBS -l walltime=hhhh:00:00
##PBS -l walltime=48:00:00
##PBS -q long
#PBS -mb -M chbull@bas.ac.uk

#FYI
OCEANCORES=eeee
XIOCORES=ffff
NODES=gggg

#quick script so the following has it's own, correct python environment
#nb: DO NOT exchange PATH for the login nodes' PATH it breaks the aprun command (see ARCHER email to Mark)
export PYTHONPATH=/work/n02/n02/chbull/anaconda2/pkgs;export PATH=/work/n02/n02/chbull/anaconda2/bin:$PATH;source activate root

python wwww/GoGoNEMO.py
EOF
fi

#bash run file
sed -e "s/pppp/${PROJ}/g ;s/wwww/${WORKDIR2}/g ; s/cccc/${CONFIG}/g ; s/oooo/${CASE}/g ; s/eeee/${OCEANCORES}/g ; s/ffff/${XIOCORES}/g ; s/gggg/${NODES}/g ; s/hhhh/${RHOURS}/g" ${WORKDIR}/GoNEMO.sh > ${WORKDIR}/GoNEMO_tmp.sh
mv -v ${WORKDIR}/GoNEMO_tmp.sh ${WORKDIR}/GoNEMO.sh

##go NEMO !
chmod +x ${WORKDIR}/GoNEMO.sh
qsub ${WORKDIR}/GoNEMO.sh
