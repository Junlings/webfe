import sys
import os
import datetime
sys.path.append('../../webfe/')
import numpy as np
from core.model.registry import model
from core.export.export import exporter
from core.settings import settings
from core.procedures.t_section import tsec_planeconfig
from core.procedures.rec_section import rec_planeconfig
from core.imports.marc.import_marc_dat import importfile_marc_dat
from core.post.import_marc_t16 import post_t16
from core.plots.plots import tpfdb
from core.model.section import layer_line

from command import commandparser
from core.utility.fem.create_arcplane import create_cylinderSurface
from core.utility.fem.create_3d_patch import create_3d_patch
from core.utility.fem.create_2d_patch import create_2d_patch
from core.utility.fem.create_single_line_nodelist import create_single_line_nodecoord
from core.utility.fem.create_prism_by_stretch import sktretch_2dmesh
from core.utility.fem.create_interface import create_interface
from core.utility.fem.create_single_line_setname import create_single_line_setname
from numpy import exp,sin,cos,arctan,abs,sqrt

import numpy as np
import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from math import tan, floor, atan

import time


def post_dowel():
    c1 = commandparser()    
    c1.parser('*macro_load,M:\\marcworking\\haider_beam\\postprocess new.mac')

if __name__ == '__main__':
    #
    #test_baseline()
    #test_group2()
    #test_group3()
    #test_group4()
    #test_group5()
    
    #test_procedure_dowelaction()
    post_dowel()
    
if __name__ == '__main__':
    
    BuildModel()
    
