
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

def define_MMFX(model1):
    
    MMFX = [[0*0.000001,0*0.001],
        [2260*0.000001,60060*0.001],
        [3001*0.000001,77110*0.001],
        [4003*0.000001,95490*0.001],
        [5005*0.000001,109030*0.001],
        [6004*0.000001,118920*0.001],
        [7007*0.000001,126530*0.001],
        [8006*0.000001,132420*0.001],
        [9006*0.000001,137260*0.001],
        [10010*0.000001,141230*0.001],
        [11008*0.000001,144560*0.001],
        [12003*0.000001,147360*0.001],
        [13003*0.000001,149790*0.001],
        [14010*0.000001,151890*0.001],
        [15001*0.000001,153700*0.001],
        [16002*0.000001,155290*0.001],
        [17008*0.000001,156710*0.001],
        [18012*0.000001,157960*0.001],
        [18029*0.000001,157980*0.001],
        [18046*0.000001,158000*0.001],
        [18064*0.000001,158020*0.001],
        [18081*0.000001,158040*0.001],
        [18096*0.000001,158060*0.001],
        [18115*0.000001,158080*0.001],
        [18132*0.000001,158100*0.001],
        [18149*0.000001,158120*0.001],
        [18165*0.000001,158130*0.001],
        [18181*0.000001,158160*0.001],
        [18200*0.000001,158180*0.001],
        [18217*0.000001,158200*0.001],
        [18233*0.000001,158220*0.001],
        [18251*0.000001,158240*0.001],
        [18268*0.000001,158250*0.001],
        [18285*0.000001,158270*0.001],
        [18302*0.000001,158290*0.001],
        [18319*0.000001,158310*0.001],
        [18335*0.000001,158330*0.001],
        [18351*0.000001,158360*0.001],
        [18369*0.000001,158380*0.001],
        [18386*0.000001,158400*0.001],
        [18403*0.000001,158420*0.001],
        [18422*0.000001,158440*0.001],
        [18441*0.000001,158460*0.001],
        [18457*0.000001,158470*0.001],
        [18473*0.000001,158490*0.001],
        [18491*0.000001,158510*0.001],
        [18510*0.000001,158530*0.001],
        [18526*0.000001,158540*0.001],
        [18543*0.000001,158560*0.001],
        [18558*0.000001,158580*0.001],
        [18576*0.000001,158600*0.001],
        [18593*0.000001,158620*0.001],
        [18611*0.000001,158640*0.001],
        [18628*0.000001,158660*0.001],
        [18646*0.000001,158680*0.001],
        [18663*0.000001,158700*0.001],
        [18681*0.000001,158720*0.001],
        [18697*0.000001,158740*0.001],
        [18716*0.000001,158760*0.001],
        [18731*0.000001,158770*0.001],
        [18750*0.000001,158790*0.001],
        [18768*0.000001	,158810*0.001],
        [18786*0.000001,158830*0.001],
        [18802*0.000001,158850*0.001],
        [18821*0.000001,158870*0.001],
        [18838*0.000001,158890*0.001],
        [18855*0.000001,158900*0.001],
        [18871*0.000001,158920*0.001],
        [18889*0.000001,158930*0.001],
        [18905*0.000001,158950*0.001],
        [18921*0.000001,158970*0.001],
        [18939*0.000001,158990*0.001],
        [18957*0.000001,159010*0.001],
        [18976*0.000001,159030*0.001],
        [18994*0.000001,159050*0.001],
        [19010*0.000001,159070*0.001],
        [20006*0.000001,160060*0.001],
        [21009*0.000001,160950*0.001],
        [22002*0.000001,161760*0.001],
        [23001*0.000001,162470*0.001],
        [24007*0.000001,163120*0.001],
        [25003*0.000001,163710*0.001],
        [26019*0.000001,164230*0.001],
        [27019*0.000001,164720*0.001],
        [28011*0.000001,165140*0.001],
        [29019*0.000001,165520*0.001],
        [30015*0.000001,165880*0.001],
        [31000*0.000001,166180*0.001],
        [32000*0.000001,166460*0.001],
        [33000*0.000001,166710*0.001],
        [34007*0.000001,166920*0.001],
        [35015*0.000001,167100*0.001],
        [36314*0.000001,167150*0.001],
        [36835*0.000001,167150*0.001],
        [37681*0.000001,167150*0.001],
        [38475*0.000001,167170*0.001],
        [39181*0.000001,167170*0.001],
        [39877*0.000001,167170*0.001],
        [40000*0.000001,1000*0.001] ]
    model1 = add_mat_by_stressstrain(model1,'mat_rebar',MMFX,0.0026)
    return model1

def add_property(model1):
    ''' add material to the model'''

    
    model1.property('concrete','hex8',{'type':7})
    model1.property('interface','quad4',{'type':186})
    model1.property('rebar','line2',{'type':98})

    model1 = define_MMFX(model1)
    #model1.material('mat_rebar','uniaxial_elastic_plastic',{'E':4000,'mu':0.3,'mass':0.0,'sigma_y':100,'tabletag':None}) #'uniaxial_elastic',{'E':35000.0,'mu':0.3,'mass':0.0})  
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
    model1.section('rec1','SolidCircular3D',{'mattag':'mat_rebar','para':{'diameter':dia},})
    model1.section('interface','interface2d',{})  # default thickness as unit

    
    model1.link_sec_prop('rec1','rebar') 
    model1.link_sec_prop('interface','interface')
    
    model1.link_prop_conn('interface',setnamelist=['interface_bot'])
    model1.link_prop_conn('concrete',setnamelist=['element_sec',])
    model1.link_prop_conn('rebar',setnamelist=['rebar',])
    
    # rotate
    model1.nodelist.transform(ry=3.1415926/2.0)
    
    # define top interface and bottom interface

    rebar_nodes = model1.nodelist.select_node_coord(ry=[dow_height-dow_rebarcenter-0.01,dow_height-dow_rebarcenter+0.01], rz=[-0.01,0.01])
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
    
    # delete the top interface layer
    #model1.delete_elements(model1.setlist['interface_top'].elemlist)
    
    model1.sweep()
    exp1 = exporter(model1,name+'.proc','ex_Marc_dat')
    exp1.export(name)
    model1.modelsavetofile(name+'.pydat')
    print 1


def post_dowel():
    c1 = commandparser()    
    c1.parser('*macro_load,M:\\github\\webfe\\test\\dowel_base\\posyprocess.mac')

if __name__ == '__main__':
    '''
    test_baseline()
    test_group2()
    test_group3()
    test_group4()
    test_group5()
    '''
    #test_procedure_dowelaction()
    post_dowel()
