
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

from core.utility.material import create_simpe_orie_UHPC as mat
    
def test_material():
    model1 = model(settings)
    
    model1 = mat.create_simpe_orie_UHPC(model1,'mat_UHPC_1',1.0,1.5,factor=1.0)
    model1 = mat.create_simpe_orie_UHPC(model1,'mat_UHPC_2',1.0,1.5,factor=1.2)
    
    
    print 1
    


if __name__ == '__main__':
    
    test_material()
    
