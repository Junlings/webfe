
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

def post_dowel(filename):
    
    c1 = commandparser()
    
    c1.parser('*add_current_settings,filename,%s' % filename )
    c1.parser('*macro_load,C:\\Users\\junlings\\Desktop\\dowel action\\codes Finite length\\plots\\popsrprocessf.mac')
    
def post_all():
    post_dowel('11')
    post_dowel('12')
    post_dowel('21')
    post_dowel('22')
    post_dowel('23')
    post_dowel('31')
    post_dowel('32')
    post_dowel('33')
    post_dowel('34')
    post_dowel('41')
    post_dowel('51')
    post_dowel('52')
    post_dowel('53')
    post_dowel('54')

if __name__ == '__main__':
    '''
    test_baseline()
    test_group2()
    test_group3()
    test_group4()
    test_group5()
    '''
    #test_procedure_dowelaction()
    post_all()
    print 1
