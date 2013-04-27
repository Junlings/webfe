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

#from command import commandparser
from core.utility.models.create_single_lap_shear import create_pullout

import numpy as np
import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from math import tan, floor, atan

import time


def procedure_interface3d(*args):
    model1 = model(settings)
    
    mtype = args[0]
    La = float(args[1])
    Ha = float(args[2])
    Za = float(args[3])
    Lb = float(args[4])
    Hb = float(args[5])  # mess with t2 as t3
    Zb = float(args[6])
    Lsize = float(args[7])
    Hsize = float(args[8])
    #offset = float(args[7])
    #bond_region = float(args[8])
    
    model1 = create_pullout(model1,La=La,Ha=Ha,Za=Za,Lb=Lb,Hb=Hb,Zb=Zb,Lsize=Lsize,Hsize=Hsize,offset=0,bond_region=None)
    
    return model1
    
    