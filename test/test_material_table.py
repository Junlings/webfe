
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
from core.utility.table.stress_strain import add_mat_by_stressstrain,add_mat_by_file
from command import commandparser

if __name__ == '__main__':
    model1 = model(settings)
    
    model1 = add_mat_by_file(model1,'Aluminum','ss.csv',mode='Ratio|Total Strain',proplimit=29.44,propstrain=0.003511,straincinr=0.0005)
    #model1 = add_mat_by_stressstrain(model1,'mat_rebar',MMFX,0.0026)
    name = 'material'
    exp1 = exporter(model1,name+'.proc','ex_Marc_dat')
    exp1.export(name)
    model1.modelsavetofile(name+'.pydat')

    print 1