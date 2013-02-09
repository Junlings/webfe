
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

from command import commandparser


def test_plot():

    aa = tpfdb()
    
    aa.add('a',np.array([[1,2,3,4,5,6,7,8,9,0],[14,5,6,17,8,9,0,1,2,3]]).T,unitlist=['N/A','N/A'],labellist=['L1','L2'])
    aa.add('b',np.array([[11,12,13,14,15,16,17,18,19,0],[14,5,61,17,81,91,0,11,12,13]]).T,unitlist=['N/A','N/A'],labellist=['L1','L2'])
    aa.add_plotdata_command('plot1',['a:L1','a:L2'])
    aa.add_plotdata_command('plot1',['b:L1','b:L2'])
    aa.edit_pdb_legend('plot1',2,'other L2')
    aa.append_plotdata_mask('plot1','xy','pair_sortx')
    aa.add_figure('plot1','plot1','default','line-one axis')
    aa.figurerealize('plot1')
    aa.savefig('plot1','jpg','aa.jpg')

    
    
if __name__ == '__main__':
    test_plot()