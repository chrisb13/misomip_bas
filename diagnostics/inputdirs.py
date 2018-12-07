#!/usr/bin/env python 
#   Author: Christopher Bull. 
#   Affiliation:  British Antarctic Survey
#                 Cambridge, UK
#   Contact: chbull@bas.ac.uk
#   Date created: Tue, 14 Aug 2018 13:49:28
#   Machine created on: SB2Vbox
#
"""
This module is for adjusting the input dirs and experiments.

"""

import collections
from _indlogger import _LogStart

_lg=_LogStart().setup()

paper_case='20180814_isomip analysis'

years=[\
('1981-01-01','2009-12-31')\
]

if paper_case=='20180814_isomip analysis':
    basefol='/home/chris/VBoxSHARED/'
    basefol='/home/chris/VBoxSHARED/ISOMIP/'
    output_folder=basefol+'20180814_isomip analysis/analysis/'
    # output_folder='/home/chris/VBoxSHARED/20180814_isomip analysis/analysis/'
    plot_outputs=output_folder+'plots/'

    nemo_fols=collections.OrderedDict()
    # nemo_fols['nemo_ISOMIP_oceanCOM_01b']=[basefol+'nemo_ISOMIP_ocean_01b/']
    # nemo_fols['nemo_ISOMIP_oceanCOM_02b']=[basefol+'nemo_ISOMIP_ocean_02b/']
    # nemo_fols['nemo_ISOMIP_oceanCOM_03b']=[basefol+'nemo_ISOMIP_ocean_03b/']

    # nemo_fols['nemo_ISOMIP_ocean_robinCOM_01']=[basefol+'nemo_ISOMIP_ocean_robinCOM_01/']
    # nemo_fols['nemo_ISOMIP_ocean_robinCOM_02']=[basefol+'nemo_ISOMIP_ocean_robinCOM_02/']
    # nemo_fols['nemo_ISOMIP_ocean_robinCOM_03']=[basefol+'nemo_ISOMIP_ocean_robinCOM_03/']

    # nemo_fols['Ocean1_COM_COCO']=[basefol+'Ocean1_COM_COCO/']
    # nemo_fols['Ocean1_COM_MITgcm_BAS']=[basefol+'Ocean1_COM_MITgcm_BAS/']
    # nemo_fols['Ocean2_COM_COCO']=[basefol+'Ocean2_COM_COCO/']
    # nemo_fols['Ocean2_COM_MITgcm_BAS']=[basefol+'Ocean2_COM_MITgcm_BAS/']

    nemo_fols['Ocean0_COM_NEMO-UKESM1is-f']=[basefol+'Ocean0_COM_NEMO-UKESM1is-f/']
    nemo_fols['Ocean0_TYP_NEMO-UKESM1is-f']=[basefol+'Ocean0_TYP_NEMO-UKESM1is-f/']
    nemo_fols['Ocean0_COM_NEMO-UKMOGO7-E']=[basefol+'Ocean0_COM_NEMO-UKMOGO7-E/']
    nemo_fols['Ocean0_TYP_NEMO-UKMOGO7-E']=[basefol+'Ocean0_TYP_NEMO-UKMOGO7-E/']
    nemo_fols['Ocean0_TYP_NEMO-UKMOGO7-C']=[basefol+'Ocean0_TYP_NEMO-UKMOGO7-C/']
    nemo_fols['Ocean0_COM_NEMO-UKMOGO7-C']=[basefol+'Ocean0_COM_NEMO-UKMOGO7-C/']

    # nemo_fols['Ocean1_COM_NEMO-UKESM1is-f']=[basefol+'Ocean1_COM_NEMO-UKESM1is-f/']
    # nemo_fols['Ocean1_COM_NEMO-UKMOGO7-C']=[basefol+'Ocean1_COM_NEMO-UKMOGO7-C/']
    # nemo_fols['Ocean1_COM_NEMO-UKMOGO7-E']=[basefol+'Ocean1_COM_NEMO-UKMOGO7-E/']

    # nemo_fols['Ocean1_TYP_NEMO-UKESM1is-f']=[basefol+'Ocean1_TYP_NEMO-UKESM1is-f/']
    # nemo_fols['Ocean1_TYP_NEMO-UKMOGO7-C']=[basefol+'Ocean1_TYP_NEMO-UKMOGO7-C/']
    # nemo_fols['Ocean1_TYP_NEMO-UKMOGO7-E']=[basefol+'Ocean1_TYP_NEMO-UKMOGO7-E/']

    # nemo_fols['Ocean2_COM_NEMO-UKESM1is-f']=[basefol+'Ocean2_COM_NEMO-UKESM1is-f/']
    # nemo_fols['Ocean2_COM_NEMO-UKMOGO7-C']=[basefol+'Ocean2_COM_NEMO-UKMOGO7-C/']
    # nemo_fols['Ocean2_COM_NEMO-UKMOGO7-E']=[basefol+'Ocean2_COM_NEMO-UKMOGO7-E/']

    # nemo_fols['Ocean2_TYP_NEMO-UKESM1is-f']=[basefol+'Ocean2_TYP_NEMO-UKESM1is-f/']
    # nemo_fols['Ocean2_TYP_NEMO-UKMOGO7-C']=[basefol+'Ocean2_TYP_NEMO-UKMOGO7-C/']
    # nemo_fols['Ocean2_TYP_NEMO-UKMOGO7-E']=[basefol+'Ocean2_TYP_NEMO-UKMOGO7-E/']



if __name__ == "__main__":                                     #are we being run directly?
    pass
