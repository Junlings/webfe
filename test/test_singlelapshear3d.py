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
from core.utility.table.stress_strain import add_mat_by_stressstrain
from command import commandparser

def test_procedure_interfaceshear():
    c1 = commandparser()    
    #c1.parser('*procedure_pole_imposedent,-1543.5,1102.5,70,56,294,44,31,450,True,True,-441,441')
    c1.parser('*procedure_interface3d,single,40,40,0,80,20,10,2,2')
    c1.parser('*save_project,temp.pydat')
    c1.parser('*export_marc_dat,default,dd.proc')

if __name__ == '__main__':
    
    test_procedure_interfaceshear()
    #post_single('model1','model1_job1.t19',resfile='model1_job1.pyres')
