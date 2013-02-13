
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


def add_property(model1):
    ''' add material to the model'''

    
    model1.property('concrete','hex8',{'type':7})
    model1.property('interface','quad4',{'type':186})
    model1.property('rebar','line2',{'type':98})

    
    model1.material('mat_rebar','uniaxial_elastic_plastic',{'E':4000,'mu':0.3,'mass':0.0,'sigma_y':100,'tabletag':None}) #'uniaxial_elastic',{'E':35000.0,'mu':0.3,'mass':0.0})  
    model1.material('mat_concrete','lowtension_marc_builtin',{'E':8000.0,'mu':0.3,'mass':0.0,'ft':1.1,'Es':50,'epsilon':0.003,'shear':0.1})
    model1.material('mat_interface','interface_marc_builtin',{'mattype':'linear','Gc':1,'vc':0.03,'vm':0.1,'s_n':1,'s_n_c':1,'stiff_c':1})
    
    model1.link_mat_prop('mat_concrete','concrete')
    model1.link_mat_prop('mat_interface','interface')
    model1.link_mat_prop('mat_rebar','rebar')    
    return model1


def test_test():
    dow_width = 2
    dow_height = 4
    dow_rebarcenter = 3
    dow_holewidth = 1
    dow_holedepth = 1
    dow_length = 16
    dow_length_incr = 1
    dow_sep_incr = 2
    
    test_procedure_dowelaction(dow_width,dow_height,dow_rebarcenter,dow_holewidth,dow_holedepth,dow_length,dow_length_incr,dow_sep_incr)

def test_baseline():
    dow_width = 1.5
    dow_height = 4.25
    dow_rebarcenter = dow_height-1.188
    dow_holewidth = 0.375
    dow_holedepth = 0.375
    dow_length = 14/2.0
    dow_length_incr = 0.5
    dow_sep_incr = 2
    dow_sep_h = 2.45
    dia=0.375
    test_procedure_dowelaction('dowel_base',dia,dow_width,dow_height,dow_rebarcenter,dow_holewidth,dow_holedepth,dow_length,dow_length_incr,dow_sep_incr,dow_sep_h)
    
def test_group2():
    dow_width = 1.5
    dow_height = 4.25
    dow_rebarcenter = dow_height-1.188
    dow_holewidth = 0.375
    dow_holedepth = 0.375
    dow_length = 18/2.0
    dow_length_incr = 0.5
    dow_sep_incr = 2
    dow_sep_h = 2.45
    dia=0.375
    test_procedure_dowelaction('dowel_g2',dia,dow_width,dow_height,dow_rebarcenter,dow_holewidth,dow_holedepth,dow_length,dow_length_incr,dow_sep_incr,dow_sep_h)
    
def test_group3():
    dow_width = 1.5
    dow_height = 4.0
    dow_rebarcenter = dow_height-0.938
    dow_holewidth = 0.375
    dow_holedepth = 0.375
    dow_length = 14/2.0
    dow_length_incr = 0.5
    dow_sep_incr = 2
    dow_sep_h = 2.45-0.25
    dia=0.375
    test_procedure_dowelaction('dowel_g3',dia,dow_width,dow_height,dow_rebarcenter,dow_holewidth,dow_holedepth,dow_length,dow_length_incr,dow_sep_incr,dow_sep_h)
    

def test_group4():
    dow_width = 1.125
    dow_height = 4.25
    dow_rebarcenter = dow_height-1.188
    dow_holewidth = 0.375
    dow_holedepth = 0.375
    dow_length = 14/2.0
    dow_length_incr = 0.5
    dow_sep_incr = 2
    dow_sep_h = 2.45
    dia=0.375
    test_procedure_dowelaction('dowel_g4',dia,dow_width,dow_height,dow_rebarcenter,dow_holewidth,dow_holedepth,dow_length,dow_length_incr,dow_sep_incr,dow_sep_h)
   
def test_group5():
    dow_width = 1.75
    dow_height = 4.5
    dow_rebarcenter = dow_height-1.25
    dow_holewidth = 0.5
    dow_holedepth = 0.5
    dow_length = 14/2.0
    dow_length_incr = 0.5
    dow_sep_incr = 2
    dow_sep_h = 2.45
    dia = 0.5
    test_procedure_dowelaction('dowel_g5',dia,dow_width,dow_height,dow_rebarcenter,dow_holewidth,dow_holedepth,dow_length,dow_length_incr,dow_sep_incr,dow_sep_h)
   
   
def test_procedure_dowelaction(name,dia,dow_width,dow_height,dow_rebarcenter,dow_holewidth,dow_holedepth,dow_length,dow_length_incr,dow_sep_incr,dow_sep_h):
    model1 = model(settings)
    
    #dow_width = 2
    #dow_height = 4
    #dow_rebarcenter = 3
    #dow_holewidth = 1
    #dow_holedepth = 1
    #dow_length = 16
    #dow_length_incr = 1
    #dow_sep_incr = 2
    
    # create nodes and elements
    model1 = rec_planeconfig(model1,'rec1',dow_width,dow_height,dow_rebarcenter,dow_holewidth,dow_holedepth,dow_length,dow_length_incr,dow_sep_incr)
    

    # add and assign property
    model1 = add_property(model1)
    
    #
    model1.section('rec1','SolidCircular3D',{'mattag':'mat_rebar',
                                             'para':{'diameter':dia},})
    model1.section('interface','interface2d',{})  # default thickness as unit

    
    model1.link_sec_prop('rec1','rebar') 
    model1.link_sec_prop('interface','interface')
    
    model1.link_prop_conn('interface',setnamelist=['interface_top','interface_bot'])
    model1.link_prop_conn('concrete',setnamelist=['element_sec',])
    model1.link_prop_conn('rebar',setnamelist=['rebar',])
    
    # rotate
    model1.nodelist.transform(ry=3.1415926/2.0)
    
    # define top interface and bottom interface

    rebar_nodes = model1.nodelist.select_node_coord(ry=[dow_height-dow_rebarcenter-0.01,dow_height-dow_rebarcenter+0.01],
                                                    rz=[-0.01,0.01])
    model1.nodeset('rebar_nodes',{'nodelist':rebar_nodes})     
    
    # select top surface node for supports
    topnodes = model1.nodelist.select_node_coord(ry=[dow_height,dow_height])
    model1.nodeset('topnodes',{'nodelist':topnodes})        
    model1.bond('topbond',{'xyz':[1,1,1,0,0,0],'DOF':6,'setnamelist':['topnodes']})    
    
    
    # select center of rebar for applying the cententrated load
    middlenodes = model1.nodelist.select_node_coord(rx=[0,0],rz=[0,0],ry=[dow_height-dow_rebarcenter,dow_height-dow_rebarcenter])
    model1.nodeset('middlenodes',{'nodelist':middlenodes})
    model1.table('loadtable',1,['time'],[[0,0],[1,1]])
    model1.load('centerload',{'xyz':[0,1,0,0,0,0],'DOF':6,'scalar':-4,'setnamelist':['middlenodes'],'tabletag':'loadtable'})
    
    
    # restrain due to symmetric
    xybondnodes = model1.nodelist.select_node_coord(rz=[-0.01,0.01])
    model1.nodeset('xybondnodes',{'nodelist':xybondnodes})
    model1.bond('xybond',{'xyz':[0,0,1,1,0,0],'DOF':6,'setnamelist':['xybondnodes']})

    # restrain due to symmetric
    yzbondnodes = model1.nodelist.select_node_coord(rx=[-0.01,0.01])
    model1.nodeset('yzbondnodes',{'nodelist':yzbondnodes})
    model1.bond('xzbond',{'xyz':[1,0,1,1,1,1],'DOF':6,'setnamelist':['yzbondnodes']})
    
    model1.loadcase('loadcase1','static_arclength',{'boundarylist':['topbond','centerload','xybond','xzbond'],'para':{'nstep':50}})
    
    model1.job('job1','static_job',{'loadcaselist':['loadcase1'],'submit':False,'reqresultslist':['stress','total_strain','crack_strain','plastic_strain']})    

    
    # delete the portion
    sepnodes = model1.nodelist.select_node_coord(rx=[0,dow_length_incr*dow_sep_incr],ry=[0,dow_sep_h])
    #model1.nodeset('middlenodes',{'nodelist':middlenodes})
    sepelem = model1.select_elements_nodelist(sepnodes)
    rebarelem = model1.setlist['rebar'].elemlist
    
    sepelem = list(set(sepelem) - set(rebarelem))
    model1.delete_elements(sepelem)
    
    model1.sweep()
    exp1 = exporter(model1,name+'.proc','ex_Marc_dat')
    exp1.export(name)
    model1.modelsavetofile(name+'.pydat')
    print 1


def post_dowel():
    c1 = commandparser()    
    c1.parser('*macro_load,M:\\github\\webfe\\test\\dowel\\posyprocess.mac')

if __name__ == '__main__':
    
    test_baseline()
    test_group2()
    test_group3()
    test_group4()
    test_group5()
    #test_procedure_dowelaction()
    #post_dowel()
