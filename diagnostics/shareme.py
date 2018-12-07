#!/usr/bin/env python 
#   Author: Christopher Bull. 
#   Affiliation:  British Antarctic Survey
#                 Cambridge, UK
#   Contact: chbull@bas.ac.uk
#   Date created: Tue, 14 Aug 2018 13:59:14
#   Machine created on: SB2Vbox
#

"""
This module is for commonly used variables and functions for the isomip work

"""

from _smlogger import _LogStart
_lg=_LogStart().setup()

import itertools
from matplotlib import gridspec
import matplotlib.pyplot as plt
import os
import numpy as np
import subprocess

import inputdirs as indi
#for inset axes
#hacked from:
#http://matplotlib.org/examples/axes_grid/inset_locator_demo.html
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

#for multiple plots
#from:http://stackoverflow.com/questions/18266642/multiple-imshow-subplots-each-with-colorbar 
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MultipleLocator

import glob
import math
import copy
from matplotlib import colors
import matplotlib
import re

def mkdir(p):
    """make directory of path that is passed"""
    try:
       os.makedirs(p)
       _lg.info("output folder: "+p+ " does not exist, we will make one.")
    except OSError as exc: # Python >2.5
       import errno
       if exc.errno == errno.EEXIST and os.path.isdir(p):
          pass
       else: raise

def inset_title_box(ax,title,bwidth="20%",location=1):
    """
    Function that puts title of subplot in a box
    
    :ax:    Name of matplotlib axis to add inset title text box too
    :title: 'string to put inside text box'
    :returns: @todo
    """

    axins = inset_axes(ax,
                       width=bwidth, # width = 30% of parent_bbox
                       height=.30, # height : 1 inch
                       loc=location)

    plt.setp(axins.get_xticklabels(), visible=False)
    plt.setp(axins.get_yticklabels(), visible=False)
    axins.set_xticks([])
    axins.set_yticks([])

    axins.text(0.5,0.3,title,
            horizontalalignment='center',
            transform=axins.transAxes,size=10)

if __name__ == "__main__": 
    pass

