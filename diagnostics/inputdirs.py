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
    output_folder='/home/chris/VBoxSHARED/20180814_isomip analysis/analysis/'
    plot_outputs=output_folder+'plots/'

    nemo_fols=collections.OrderedDict()
    nemo_fols['nemo_ISOMIP_oceanCOM_01b']=['/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_01b/']
    nemo_fols['nemo_ISOMIP_oceanCOM_02b']=['/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_02b/']
    nemo_fols['nemo_ISOMIP_oceanCOM_03b']=['/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_03b/']

    nemo_fols['nemo_ISOMIP_ocean_robinCOM_01']=['/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_robinCOM_01/']
    nemo_fols['nemo_ISOMIP_ocean_robinCOM_02']=['/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_robinCOM_02/']
    nemo_fols['nemo_ISOMIP_ocean_robinCOM_03']=['/home/chris/VBoxSHARED/nemo_ISOMIP_ocean_robinCOM_03/']

if __name__ == "__main__":                                     #are we being run directly?
    pass
