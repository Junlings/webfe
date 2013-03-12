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
from numpy import exp,sin,cos,arctan,abs,sqrt

import numpy as np
import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from math import tan

import time

def add_property(model1):
    ''' add material to the model'''

    
    model1.property('concrete','hex8',{'type':7})
    model1.property('interface','quad4',{'type':186})
    model1.property('frp_t1','quad4',{'type':75})
    model1.property('frp_t2','quad4',{'type':75})
    model1.property('frp_t3','quad4',{'type':75})
    model1.property('frp_t4','quad4',{'type':75})

    
    model1.material('mat_FRP_t1','uniaxial_elastic_plastic',{'E':4000,'mu':0.3,'mass':0.0,'sigma_y':30,'tabletag':None}) #'uniaxial_elastic',{'E':35000.0,'mu':0.3,'mass':0.0})
    model1.material('mat_FRP_t2','uniaxial_elastic_plastic',{'E':4000,'mu':0.3,'mass':0.0,'sigma_y':30,'tabletag':None})
    model1.material('mat_FRP_t3','uniaxial_elastic_plastic',{'E':4000,'mu':0.3,'mass':0.0,'sigma_y':30,'tabletag':None})
    model1.material('mat_FRP_t4','uniaxial_elastic_plastic',{'E':4000,'mu':0.3,'mass':0.0,'sigma_y':30,'tabletag':None})
    
    model1.material('mat_concrete','lowtension_marc_builtin',{'E':8000.0,'mu':0.3,'mass':0.0,'ft':1.1,'Es':50,'epsilon':0.003,'shear':0.1})
    model1.material('mat_interface','interface_marc_builtin',{'mattype':'linear','Gc':1,'vc':0.03,'vm':0.1,'s_n':1,'s_n_c':1,'stiff_c':1})
    
    model1.link_mat_prop('mat_concrete','concrete')
    model1.link_mat_prop('mat_interface','interface')
    model1.link_mat_prop('mat_FRP_t1','frp_t1')    
    model1.link_mat_prop('mat_FRP_t2','frp_t2')
    model1.link_mat_prop('mat_FRP_t3','frp_t3')
    model1.link_mat_prop('mat_FRP_t4','frp_t4')
    
    return model1
    
def divident(N1,N2,lsize,force=None):
    
    length = ((N1[0]-N2[0]) ** 2 + (N1[1]-N2[1]) ** 2+ (N1[2]-N2[2]) ** 2) ** 0.5
    
    divi = int(length/lsize) + 1
    
    if force == 'Even':
        if divi % 2 != 0:
            divi += 1
            
    if force  == 'Odd':
        if divi % 2 == 0:
            divi += 1
    
    return divi

def BuildModel():
    model1 = model(settings)
    bf = 12.0    # width of flange UHPportion
    tf = 1.0     # thickness of flange UHPportion
    h = 5.0      # total section height
    tf1 = 1.25   # distance between UHPC and frp top plate
    t1 = 0.25     # thickness of top portion FRP
    b1 = 6     # width of top portion FRP
    t2 = 0.25     # thickness of inclined FRP portion
    ang2 = 60    # angle of inclined FRP portion
    t3 = 0.25     # Thickness of the botton center part
    t4 = 0.25     # Thickness of the botton side part

    L = 48.0
    Lsize = 2.0
    bsize = 1.0
    hsize = 0.25

    
    d = h - max(t3,t4)/2.0  # effective depth from center
    
    # get width of center part
    h2 = d - tf1 
    b3 = b1 +  h2 *2 / tan(float(ang2)/180.0*3.1415926)

    b4h = (bf - b3) / 2.0

    
    # Define nodes
    N1 = [-bf/2.0,0,0]
    N2 = [-b3/2.0,0,0]
    N3 = [0,0,0]
    N4 = [b3/2.0,0,0]
    N5 = [bf/2.0,0,0]
    
    N6 = [-b1/2.0,h-tf1,0]
    N7 = [b1/2.0,h-tf1,0]
    
    N8 = [-b1/2.0,0,0]
    N9 = [b1/2.0,0,0]
    
    #t0 = time.time()
    # create t1
    mdoel1 = create_single_line_nodecoord(model1,N6,N7,divident(N6,N7,bsize,'Even'),elemsetname='frp_t1')
    mdoel1 = create_single_line_nodecoord(model1,N1,N2,divident(N1,N2,bsize),elemsetname='frp_t4_l')
    mdoel1 = create_single_line_nodecoord(model1,N2,N8,divident(N2,N6,bsize),elemsetname='frp_t3_l')
    mdoel1 = create_single_line_nodecoord(model1,N8,N9,divident(N8,N9,bsize,'Even'),elemsetname='frp_t3')
    mdoel1 = create_single_line_nodecoord(model1,N9,N4,divident(N7,N4,bsize),elemsetname='frp_t3_r')    
    mdoel1 = create_single_line_nodecoord(model1,N4,N5,divident(N4,N5,bsize),elemsetname='frp_t4_r')
    mdoel1 = create_single_line_nodecoord(model1,N2,N6,divident(N2,N6,bsize),elemsetname='frp_t2_l')
    mdoel1 = create_single_line_nodecoord(model1,N7,N4,divident(N7,N4,bsize),elemsetname='frp_t2_r')
    #t1 = time.time() - t0
    #print 'time to construct FRP layers %s ' % str(t1)
    
    #t0 = time.time()
    model1,a,b,c = sktretch_2dmesh(model1,24,2,ElemSetNameList=['frp_t1'],setname='plate_frp_t1')
    model1,a,b,c = sktretch_2dmesh(model1,24,2,ElemSetNameList=['frp_t2_l','frp_t2_r'],setname='plate_frp_t2')
    model1,a,b,c = sktretch_2dmesh(model1,24,2,ElemSetNameList=['frp_t3_l','frp_t3_r','frp_t3'],setname='plate_frp_t3')
    model1,a,b,c = sktretch_2dmesh(model1,24,2,ElemSetNameList=['frp_t4_l','frp_t4_r'],setname='plate_frp_t4')
    #t1 = time.time() - t0
    #print 'time to Extrude FRP layers %s ' % str(t1)
    
    
    
    # create top UHPC layer
    #t0 = time.time()
    model1 = create_3d_patch(model1,(0-bf/2.0,h-tf,0),(bsize,hsize,Lsize),(bf/bsize,tf/hsize,L/Lsize),setname='UHPC')
    #t1 = time.time() - t0
    #print 'time to construct UHPC %s ' % str(t1)
    
    #t0 = time.time()
    model1.sweep()
    #t1 = time.time() - t0
    #print 'time to sweep nodes  %s ' % str(t1)
    

    #t0 = time.time()
    model1.nodelist.get_sortedcoordtable()
    model1 = create_interface(model1,[-b1/2.0,h-tf,0],[-b1/2.0,h-tf1,0],2,24,setname='interface_left')
    model1 = create_interface(model1,[0,h-tf,0],[0,h-tf1,0],2,24,setname='interface_center')
    model1 = create_interface(model1,[b1/2.0,h-tf,0],[b1/2.0,h-tf1,0],2,24,setname='interface_right')
    #t1 = time.time() - t0
    #print 'time to construct interface %s ' % str(t1)
    
    
    
    
    
    # add and assign property
    model1 = add_property(model1)
    
    
    model1.section('frp_t1','shell_section',{'thickness':t1})
    model1.section('frp_t2','shell_section',{'thickness':t2})
    model1.section('frp_t3','shell_section',{'thickness':t3})
    model1.section('frp_t4','shell_section',{'thickness':t4})
    model1.section('interface','interface2d',{})

    model1.link_sec_prop('frp_t1','frp_t1') 
    model1.link_sec_prop('frp_t2','frp_t2')
    model1.link_sec_prop('frp_t3','frp_t3')
    model1.link_sec_prop('frp_t4','frp_t4')
    model1.link_sec_prop('interface','interface')
    
    model1.link_prop_conn('interface',setnamelist=['interface_left','interface_center','interface_right'])
    model1.link_prop_conn('concrete',setnamelist=['UHPC'])
    model1.link_prop_conn('frp_t1',setnamelist=['element_plate_frp_t1']) 
    model1.link_prop_conn('frp_t2',setnamelist=['element_plate_frp_t2'])
    model1.link_prop_conn('frp_t3',setnamelist=['element_plate_frp_t3'])
    model1.link_prop_conn('frp_t4',setnamelist=['element_plate_frp_t4']) 


    
    
    # create boundary conditions
    leftbond = model1.nodelist.select_node_coord(rz=[0,0],ry=[0,0])
    rightbond = model1.nodelist.select_node_coord(rz=[L,L],ry=[0,0])
    centerload = model1.nodelist.select_node_coord(rz=[L/2.0,L/2.0],ry=[h,h])
    centerlineload = model1.nodelist.select_node_coord(rx=[0,0],rz=[0,L],ry=[h-tf,h-tf])
    middlenode = model1.nodelist.select_node_coord(rx=[0,0],rz=[L/2.0,L/2.0],ry=[0,0])
    
    model1.nodeset('middlenode',{'nodelist':middlenode})
    model1.nodeset('leftbond',{'nodelist':leftbond})
    model1.nodeset('rightbond',{'nodelist':rightbond})
    model1.nodeset('centerload',{'nodelist':centerload})
    model1.nodeset('centerlineload',{'nodelist':centerlineload})
    
    model1.table('loadtable',1,['time'],[[0,0],[1,1]])
        
    model1.bond('leftbond',{'xyz':[1,1,1,0,0,0],'DOF':6,'setnamelist':['leftbond']})
    model1.bond('rightbond',{'xyz':[0,1,1,0,0,0],'DOF':6,'setnamelist':['rightbond']})
    model1.bond('support_z',{'xyz':[0,0,1,0,0,0],'DOF':6,'setnamelist':['centerlineload']})
    model1.load('centerload',{'xyz':[0,1,0,0,0,0],'DOF':6,'scalar':-4,'setnamelist':['centerload'],'tabletag':'loadtable'})


    # create Reb2
    loadlinenode = model1.nodelist.select_node_coord(rz=[L/2.0,L/2.0],ry=[h,h])
    loadlinecenter = model1.nodelist.select_node_coord(rz=[L/2.0,L/2.0],ry=[h,h],rx=[0,0])
    
    # remove center node fron list
    loadlinenode = loadlinenode.difference(loadlinecenter)
    loadlinenode = list(loadlinenode)
    loadlinecenter = list(loadlinecenter)
 
    model1.nodaltie('rbe_load','marc_rbe2',{'tietype':'DY','tieid':1,'retnode':loadlinecenter[0],'tienodelist':loadlinenode})

    model1.loadcase('loadcase1','static_arclength',{'boundarylist':['leftbond','centerload','rightbond','support_z'],'para':{'nstep':50}})
    
    model1.job('job1','static_job',{'loadcaselist':['loadcase1'],'submit':True,'reqresultslist':['stress','total_strain','crack_strain','plastic_strain']})    
    
    
    # rotate
    model1.nodelist.transform(ry=3.1415926/2.0)
    
    exp1 = exporter(model1,'hybrid.proc','ex_Marc_dat')
    exp1.export('default')
    
    #t0 = time.time()    
    model1.modelsavetofile('hybrid.pydat')
    #t1 = time.time() - t0
    #print 'time to save model %s ' % str(t1)
    
if __name__ == '__main__':
    
    BuildModel()
    
