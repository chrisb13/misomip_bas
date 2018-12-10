#!/bin/bash
#quick bash script to move/rename robin's interpolated experiments.

#source: /fs2/n02/shared/robin/MISOMIP
#see: /home/chris/VBoxSHARED/repos/misomip_bas/configs/experiments.csv

#mkdir Ocean0_COM_NEMO-UKESM1is-f
#mkdir Ocean0_COM_NEMO-UKMOGO7-C
#mkdir Ocean0_COM_NEMO-UKMOGO7-E
#mkdir Ocean0_TYP_NEMO-UKESM1is-f
#mkdir Ocean0_TYP_NEMO-UKMOGO7-C
#mkdir Ocean0_TYP_NEMO-UKMOGO7-E
#mkdir Ocean1_COM_NEMO-UKESM1is-f
#mkdir Ocean1_COM_NEMO-UKMOGO7-C
#mkdir Ocean1_COM_NEMO-UKMOGO7-E
#mkdir Ocean1_TYP_NEMO-UKESM1is-f
#mkdir Ocean1_TYP_NEMO-UKMOGO7-C
#mkdir Ocean1_TYP_NEMO-UKMOGO7-E
#mkdir Ocean2_COM_NEMO-UKESM1is-f
#mkdir Ocean2_COM_NEMO-UKMOGO7-C
#mkdir Ocean2_COM_NEMO-UKMOGO7-E
#mkdir Ocean2_TYP_NEMO-UKESM1is-f
#mkdir Ocean2_TYP_NEMO-UKMOGO7-C
#mkdir Ocean2_TYP_NEMO-UKMOGO7-E


#mv  Ocean0_COM_NEMO-UKESM1is.nc-f  Ocean0_COM_NEMO-UKESM1is-f/Ocean0_COM_NEMO-UKESM1is-f.nc
#mv Ocean0_COM_NEMO-UKMOGO7.nc-C    Ocean0_COM_NEMO-UKMOGO7-C/Ocean0_COM_NEMO-UKMOGO7-C.nc
#mv Ocean0_COM_NEMO-UKMOGO7.nc-E    Ocean0_COM_NEMO-UKMOGO7-E/Ocean0_COM_NEMO-UKMOGO7-E.nc
#mv  Ocean0_TYP_NEMO-UKESM1is.nc-f  Ocean0_TYP_NEMO-UKESM1is-f/Ocean0_TYP_NEMO-UKESM1is-f.nc
#mv Ocean0_TYP_NEMO-UKMOGO7.nc-C    Ocean0_TYP_NEMO-UKMOGO7-C/Ocean0_TYP_NEMO-UKMOGO7-C.nc
#mv Ocean0_TYP_NEMO-UKMOGO7.nc-E    Ocean0_TYP_NEMO-UKMOGO7-E/Ocean0_TYP_NEMO-UKMOGO7-E.nc
#mv  Ocean1_COM_NEMO-UKESM1is.nc-f  Ocean1_COM_NEMO-UKESM1is-f/Ocean1_COM_NEMO-UKESM1is-f.nc
#mv Ocean1_COM_NEMO-UKMOGO7.nc-C    Ocean1_COM_NEMO-UKMOGO7-C/Ocean1_COM_NEMO-UKMOGO7-C.nc
#mv Ocean1_COM_NEMO-UKMOGO7.nc-E    Ocean1_COM_NEMO-UKMOGO7-E/Ocean1_COM_NEMO-UKMOGO7-E.nc
#mv  Ocean1_TYP_NEMO-UKESM1is.nc-f  Ocean1_TYP_NEMO-UKESM1is-f/Ocean1_TYP_NEMO-UKESM1is-f.nc
#mv Ocean1_TYP_NEMO-UKMOGO7.nc-C    Ocean1_TYP_NEMO-UKMOGO7-C/Ocean1_TYP_NEMO-UKMOGO7-C.nc
#mv Ocean1_TYP_NEMO-UKMOGO7.nc-E    Ocean1_TYP_NEMO-UKMOGO7-E/Ocean1_TYP_NEMO-UKMOGO7-E.nc
#mv  Ocean2_COM_NEMO-UKESM1is.nc-f  Ocean2_COM_NEMO-UKESM1is-f/Ocean2_COM_NEMO-UKESM1is-f.nc
#mv Ocean2_COM_NEMO-UKMOGO7.nc-C    Ocean2_COM_NEMO-UKMOGO7-C/Ocean2_COM_NEMO-UKMOGO7-C.nc
#mv Ocean2_COM_NEMO-UKMOGO7.nc-E    Ocean2_COM_NEMO-UKMOGO7-E/Ocean2_COM_NEMO-UKMOGO7-E.nc
#mv  Ocean2_TYP_NEMO-UKESM1is.nc-f  Ocean2_TYP_NEMO-UKESM1is-f/Ocean2_TYP_NEMO-UKESM1is-f.nc
#mv Ocean2_TYP_NEMO-UKMOGO7.nc-C    Ocean2_TYP_NEMO-UKMOGO7-C/Ocean2_TYP_NEMO-UKMOGO7-C.nc
#mv Ocean2_TYP_NEMO-UKMOGO7.nc-E    Ocean2_TYP_NEMO-UKMOGO7-E/Ocean2_TYP_NEMO-UKMOGO7-E.nc

####################################
#  moving robin's old experiments  #
####################################

mkdir Ocean0_COM_NEMO-UKMOGO6
mkdir Ocean0_TYP_NEMO-UKMOGO6
mkdir Ocean1_COM_NEMO-UKMOGO6
mkdir Ocean1_TYP_NEMO-UKMOGO6
mkdir Ocean2_COM_NEMO-UKMOGO6
mkdir Ocean2_TYP_NEMO-UKMOGO6
mkdir Ocean3_COM_NEMO-UKMOGO6
mkdir Ocean3_TYP_NEMO-UKMOGO6
mkdir Ocean4_COM_NEMO-UKMOGO6
mkdir Ocean4_TYP_NEMO-UKMOGO6

mv Ocean0_COM_NEMO-UKMOGO6.nc  Ocean0_COM_NEMO-UKMOGO6/Ocean0_COM_NEMO-UKMOGO6.nc
mv Ocean0_TYP_NEMO-UKMOGO6.nc  Ocean0_TYP_NEMO-UKMOGO6/Ocean0_TYP_NEMO-UKMOGO6.nc
mv Ocean1_COM_NEMO-UKMOGO6.nc  Ocean1_COM_NEMO-UKMOGO6/Ocean1_COM_NEMO-UKMOGO6.nc
mv Ocean1_TYP_NEMO-UKMOGO6.nc  Ocean1_TYP_NEMO-UKMOGO6/Ocean1_TYP_NEMO-UKMOGO6.nc
mv Ocean2_COM_NEMO-UKMOGO6.nc  Ocean2_COM_NEMO-UKMOGO6/Ocean2_COM_NEMO-UKMOGO6.nc
mv Ocean2_TYP_NEMO-UKMOGO6.nc  Ocean2_TYP_NEMO-UKMOGO6/Ocean2_TYP_NEMO-UKMOGO6.nc
mv Ocean3_COM_NEMO-UKMOGO6.nc  Ocean3_COM_NEMO-UKMOGO6/Ocean3_COM_NEMO-UKMOGO6.nc
mv Ocean3_TYP_NEMO-UKMOGO6.nc  Ocean3_TYP_NEMO-UKMOGO6/Ocean3_TYP_NEMO-UKMOGO6.nc
mv Ocean4_COM_NEMO-UKMOGO6.nc  Ocean4_COM_NEMO-UKMOGO6/Ocean4_COM_NEMO-UKMOGO6.nc
mv Ocean4_TYP_NEMO-UKMOGO6.nc  Ocean4_TYP_NEMO-UKMOGO6/Ocean4_TYP_NEMO-UKMOGO6.nc

