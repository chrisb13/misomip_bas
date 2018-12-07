#!/bin/bash
set -x

#Quick bash script to set-up the re-run of the isomip experiments because of errors in the nemo_base_WARM/nemo_base_COLD files.

#   Author: Christopher Bull. 
#   Affiliation:  British Antarctic Survey
#                 Cambridge, UK
#   Contact: chbull@bas.ac.uk
#   Date created: Fri, 16 Nov 2018 11:51:45

cd /fs2/n02/n02/chbull/nemo/run/isomip_redux

#preserve symlinks
cp -avr nemo_ISOMIP_oceanCOM_01e nemo_ISOMIP_oceanCOM_01f
cp -avr nemo_ISOMIP_oceanCOM_02e nemo_ISOMIP_oceanCOM_02f
cp -avr nemo_ISOMIP_oceanCOM_03e nemo_ISOMIP_oceanCOM_03f
cp -avr nemo_ISOMIP_oceanTYP_01e nemo_ISOMIP_oceanTYP_01f
cp -avr nemo_ISOMIP_oceanTYP_02e nemo_ISOMIP_oceanTYP_02f
cp -avr nemo_ISOMIP_oceanTYP_03e nemo_ISOMIP_oceanTYP_03f

#fix the bad symlinks...
#this is what they used to look like...
#nemo_ISOMIP_oceanCOM_01e/TS_init.nc -> nemo_base_WARM.nc
#nemo_ISOMIP_oceanCOM_02e/TS_init.nc -> nemo_base_COLD.nc
#nemo_ISOMIP_oceanCOM_03e/TS_init.nc -> nemo_base_WARM.nc
#
#nemo_ISOMIP_oceanTYP_01e/TS_init.nc -> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM.nc
#nemo_ISOMIP_oceanTYP_02e/TS_init.nc -> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_COLD.nc
#nemo_ISOMIP_oceanTYP_03e/TS_init.nc -> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM.nc
#
#nemo_ISOMIP_oceanCOM_01e/resto.nc -> nemo_base_WARM.nc
#nemo_ISOMIP_oceanCOM_02e/resto.nc -> nemo_base_WARM.nc
#nemo_ISOMIP_oceanCOM_03e/resto.nc -> nemo_base_COLD.nc
#
#nemo_ISOMIP_oceanTYP_01e/resto.nc -> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM.nc
#nemo_ISOMIP_oceanTYP_02e/resto.nc -> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM.nc
#nemo_ISOMIP_oceanTYP_03e/resto.nc -> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_COLD.nc

#delete 'em
rm nemo_ISOMIP_oceanCOM_01f/TS_init.nc
rm nemo_ISOMIP_oceanCOM_02f/TS_init.nc
rm nemo_ISOMIP_oceanCOM_03f/TS_init.nc
rm nemo_ISOMIP_oceanTYP_01f/TS_init.nc
rm nemo_ISOMIP_oceanTYP_02f/TS_init.nc
rm nemo_ISOMIP_oceanTYP_03f/TS_init.nc

rm nemo_ISOMIP_oceanCOM_01f/resto.nc
rm nemo_ISOMIP_oceanCOM_02f/resto.nc 
rm nemo_ISOMIP_oceanCOM_03f/resto.nc 
rm nemo_ISOMIP_oceanTYP_01f/resto.nc 
rm nemo_ISOMIP_oceanTYP_02f/resto.nc 
rm nemo_ISOMIP_oceanTYP_03f/resto.nc 

#create new links to robin's fixed files

COM_COLD=/fs2/n02/shared/robin/MISOMIP/NEMO_COM/nemo_base_COLD-NEWFIX.nc
COM_WARM=/fs2/n02/shared/robin/MISOMIP/NEMO_COM/nemo_base_WARM-NEWFIX.nc

ln -s ${COM_WARM} nemo_ISOMIP_oceanCOM_01f/TS_init.nc #-> nemo_base_WARM.nc
ln -s ${COM_COLD} nemo_ISOMIP_oceanCOM_02f/TS_init.nc #-> nemo_base_COLD.nc
ln -s ${COM_WARM} nemo_ISOMIP_oceanCOM_03f/TS_init.nc #-> nemo_base_WARM.nc
                 
ln -s ${COM_WARM} nemo_ISOMIP_oceanCOM_01f/resto.nc   #-> nemo_base_WARM.nc
ln -s ${COM_WARM} nemo_ISOMIP_oceanCOM_02f/resto.nc   #-> nemo_base_WARM.nc
ln -s ${COM_COLD} nemo_ISOMIP_oceanCOM_03f/resto.nc   #-> nemo_base_COLD.nc

TYP_COLD=/fs2/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_COLD-NEWFIX.nc
TYP_WARM=/fs2/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM-NEWFIX.nc

ln -s ${TYP_WARM} nemo_ISOMIP_oceanTYP_01f/TS_init.nc #-> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM.nc
ln -s ${TYP_COLD} nemo_ISOMIP_oceanTYP_02f/TS_init.nc #-> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_COLD.nc
ln -s ${TYP_WARM} nemo_ISOMIP_oceanTYP_03f/TS_init.nc #-> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM.nc
                 
ln -s ${TYP_WARM} nemo_ISOMIP_oceanTYP_01f/resto.nc   #-> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM.nc
ln -s ${TYP_WARM} nemo_ISOMIP_oceanTYP_02f/resto.nc   #-> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM.nc
ln -s ${TYP_COLD} nemo_ISOMIP_oceanTYP_03f/resto.nc   #-> /work/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_COLD.nc

#cd nemo_ISOMIP_oceanCOM_01f
#qsub run_gyre2.pbs; cd ..
#cd nemo_ISOMIP_oceanCOM_02f
#qsub run_gyre2.pbs; cd ..
#cd nemo_ISOMIP_oceanCOM_03f
#qsub run_gyre2.pbs; cd ..
#cd nemo_ISOMIP_oceanTYP_01f
#qsub run_gyre2.pbs; cd ..
#cd nemo_ISOMIP_oceanTYP_02f
#qsub run_gyre2.pbs; cd ..
#cd nemo_ISOMIP_oceanTYP_03f
#qsub run_gyre2.pbs; cd ..

#the re-start switch....
#rm -r nemo_ISOMIP_oceanCOM_01f
#rm -r nemo_ISOMIP_oceanCOM_02f
#rm -r nemo_ISOMIP_oceanCOM_03f
#rm -r nemo_ISOMIP_oceanTYP_01f
#rm -r nemo_ISOMIP_oceanTYP_02f
#rm -r nemo_ISOMIP_oceanTYP_03f

###############################################
#Checking after we've run the script

#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanCOM_01f/TS_init.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_COM/nemo_base_WARM-NEWFIX.nc
#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanCOM_02f/TS_init.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_COM/nemo_base_COLD-NEWFIX.nc
#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanCOM_03f/TS_init.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_COM/nemo_base_WARM-NEWFIX.nc

#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanTYP_01f/TS_init.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM-NEWFIX.nc
#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanTYP_02f/TS_init.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_COLD-NEWFIX.nc
#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanTYP_03f/TS_init.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM-NEWFIX.nc

#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanCOM_01f/resto.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_COM/nemo_base_WARM-NEWFIX.nc
#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanCOM_02f/resto.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_COM/nemo_base_WARM-NEWFIX.nc
#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanCOM_03f/resto.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_COM/nemo_base_COLD-NEWFIX.nc

#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanTYP_01f/resto.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM-NEWFIX.nc
#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanTYP_02f/resto.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_WARM-NEWFIX.nc
#lrwxrwxrwx 1 chbull n02 63 Nov 16 11:26 nemo_ISOMIP_oceanTYP_03f/resto.nc -> /fs2/n02/shared/robin/MISOMIP/NEMO_TYP/nemo_base_COLD-NEWFIX.nc

# looks okay to me
