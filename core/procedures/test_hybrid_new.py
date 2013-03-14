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
    H = 4.875           # total height
    B = 10          # total width
    t1 = 0.4375       # thickness of the ploymer concrete
    t3 = 0.125        # offset of the top plate
    t2 = H - t1 -t3    # height of the second portion
    
    b3 = 1.375          # top-left portion
    b4 = B - b3 * 2 # top-middle portion
    
    b1 = 3.75
    b2 = B - b1 * 2
    
    alpha = atan(t2/(b1-b3))
    #alpha = 60.0/180.0* 3.1415926  # incline angle
    #b1 = b3 + t2 / float(alpha)
    #b2 = B - b1 * 2
    
    
    
    # Define nodes
    N1 = [0.0,H,0]
    N2 = [0,t2,0]
    N3 = [0,0,0]
    N4 = [b3,t2,0]
    N5 = [b1,0,0]
    
    N6 = [b3+b4,t2,0]
    N7 = [b1+b2,0,0]
    
    N8 = [B,H,0]
    N9 = [B,t2,0]
    N10 = [B,0,0]
    N11 = [b3,H,0]
    N12 = [b3+b4,H,0]
    N13 = [0,t2 + t3,0]
    N14 = [b3,t2 + t3,0]
    N15 = [b3 + b4,t2 + t3,0]
    N16 = [B,t2 + t3,0]
    
    tempnodes = [N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N11,N12,N13,N14,N15,N16]
    
    # create t1
    model1.node(tempnodes)
    
    Lsize_seg_B = 0.5
    Lsize_seg_H = 0.25
    
    model1 = create_2d_patch(model1,[2,3,5,4],[floor(int(t2/Lsize_seg_H)),floor(int(b3/Lsize_seg_B))*2],setname='bottom_left')
    model1 = create_2d_patch(model1,[4,5,7,6],[floor(int(t2/Lsize_seg_H)),floor(int(b4/Lsize_seg_B))],setname='bottom_middle')
    model1 = create_2d_patch(model1,[6,7,10,9],[floor(int(t2/Lsize_seg_H)),floor(int(b3/Lsize_seg_B))*2],setname='bottom_right')

    model1 = create_2d_patch(model1,[1,13,14,11],[floor(int(t1/Lsize_seg_H))+1,floor(int(b3/Lsize_seg_B))*2],setname='top_left')
    model1 = create_2d_patch(model1,[11,14,15,12],[floor(int(t1/Lsize_seg_H))+1,floor(int(b4/Lsize_seg_B))],setname='top_middle')
    model1 = create_2d_patch(model1,[12,15,16,8],[floor(int(t1/Lsize_seg_H))+1,floor(int(b3/Lsize_seg_B))*2],setname='top_right')
    

    # create line elements that will be stretched to the frp plate
    model1 = create_single_line_setname(model1,'bottom_left-1-4',mode='x',ressetname='L1')
    model1 = create_single_line_setname(model1,'bottom_middle-1-4',mode='x',ressetname='L1')
    model1 = create_single_line_setname(model1,'bottom_right-1-4',mode='x',ressetname='L1')
    
    model1 = create_single_line_setname(model1,'bottom_left-1-4',mode='x',ressetname='L2')
    model1 = create_single_line_setname(model1,'bottom_right-1-4',mode='x',ressetname='L2')
    
    model1 = create_single_line_setname(model1,'bottom_middle-1-2',mode='x',ressetname='L3')
    model1 = create_single_line_setname(model1,'bottom_middle-3-4',mode='x',ressetname='L3')
    
    model1 = create_single_line_setname(model1,'bottom_middle-2-3',mode='x',ressetname='L4')
    
    model1 = create_single_line_setname(model1,'bottom_left-2-3',mode='x',ressetname='L5')
    model1 = create_single_line_setname(model1,'bottom_middle-2-3',mode='x',ressetname='L5')
    model1 = create_single_line_setname(model1,'bottom_right-2-3',mode='x',ressetname='L5')
 
 
    # stretch the mesh to generate 3D
    
    L_total = 50.0
    Lincr = 2.0
    n_incr = int(L_total/Lincr)
    
    
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L1'],setname='plate_frp_L1')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L2'],setname='plate_frp_L2')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L3'],setname='plate_frp_L3')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L4'],setname='plate_frp_L4')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L5'],setname='plate_frp_L5')
    

    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['bottom_left'],setname='solid_bottom_left')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['bottom_middle'],setname='solid_bottom_middle')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['bottom_right'],setname='solid_bottom_right')
    
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['top_left'],setname='solid_top_left')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['top_middle'],setname='solid_top_middle')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['top_right'],setname='solid_top_right')

    
    # merge duplicate nodes
    model1.sweep()

    # create interface
    #for i in range(0,floor(int(B/Lsize_seg_B)))
    interfacenodelist = model1.nodelist.select_node_coord(rz=[-0.001,0.001],ry=[t2-0.01,t2+0.01])
    #model1 = create_interface(model1,[-b1/2.0,h-tf,0],[-b1/2.0,h-tf1,0],2,24,setname='interface_left')
    
    for nodeid in interfacenodelist:
        xyz = model1.nodelist.itemlib[nodeid].xyz
        xyz = list(xyz)
        model1 = create_interface(model1,xyz,[xyz[0],xyz[1]+t3,xyz[2]],Lincr,n_incr,setname='interface')
    

    exp1 = exporter(model1,'hybrid.proc','ex_Marc_dat')
    exp1.export('default')
    
    #t0 = time.time()    
    model1.modelsavetofile('hybrid.pydat')
    #t1 = time.time() - t0
    #print 'time to save model %s ' % str(t1)
    
    

def BuildModel_hybrid():
    model1 = model(settings)
    H = 4.875           # total height
    B = 10          # total width
    t1 = 0.5       # thickness of the ploymer concrete
    t3 = 0.125        # offset of the top plate
    t2 = H - t1 -t3    # height of the second portion
    
    b3 = 1.375          # top-left portion
    b4 = B - b3 * 2 # top-middle portion
    
    b1 = 3.75
    b2 = B - b1 * 2
    
    alpha = atan(t2/(b1-b3))    # incline angle
    
    # Define nodes
    N1 = [0.0,H,0]
    N2 = [0,t2,0]
    N3 = [0,0,0]
    N4 = [b3,t2,0]
    N5 = [b1,0,0]
    
    N6 = [b3+b4,t2,0]
    N7 = [b1+b2,0,0]
    
    N8 = [B,H,0]
    N9 = [B,t2,0]
    N10 = [B,0,0]
    N11 = [b3,H,0]
    N12 = [b3+b4,H,0]
    N13 = [0,t2 + t3,0]
    N14 = [b3,t2 + t3,0]
    N15 = [b3 + b4,t2 + t3,0]
    N16 = [B,t2 + t3,0]
    
    tempnodes = [N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N11,N12,N13,N14,N15,N16]
    
    # create t1
    model1.node(tempnodes)
    
    Lsize_seg_B = 0.5
    Lsize_seg_H = 0.25
    
    model1 = create_2d_patch(model1,[2,3,5,4],[floor(int(t2/Lsize_seg_H)),floor(int(b3/Lsize_seg_B))*2],setname='bottom_left')
    model1 = create_2d_patch(model1,[4,5,7,6],[floor(int(t2/Lsize_seg_H)),floor(int(b4/Lsize_seg_B))],setname='bottom_middle')
    model1 = create_2d_patch(model1,[6,7,10,9],[floor(int(t2/Lsize_seg_H)),floor(int(b3/Lsize_seg_B))*2],setname='bottom_right')

    model1 = create_2d_patch(model1,[1,13,14,11],[floor(int(t1/Lsize_seg_H))+1,floor(int(b3/Lsize_seg_B))*2],setname='top_left')
    model1 = create_2d_patch(model1,[11,14,15,12],[floor(int(t1/Lsize_seg_H))+1,floor(int(b4/Lsize_seg_B))],setname='top_middle')
    model1 = create_2d_patch(model1,[12,15,16,8],[floor(int(t1/Lsize_seg_H))+1,floor(int(b3/Lsize_seg_B))*2],setname='top_right')
    

    # create line elements that will be stretched to the frp plate
    model1 = create_single_line_setname(model1,'bottom_left-1-4',mode='x',ressetname='L1')
    model1 = create_single_line_setname(model1,'bottom_middle-1-4',mode='x',ressetname='L1')
    model1 = create_single_line_setname(model1,'bottom_right-1-4',mode='x',ressetname='L1')
    
    model1 = create_single_line_setname(model1,'bottom_left-1-4',mode='x',ressetname='L2')
    model1 = create_single_line_setname(model1,'bottom_right-1-4',mode='x',ressetname='L2')
    
    model1 = create_single_line_setname(model1,'bottom_middle-1-2',mode='x',ressetname='L3')
    model1 = create_single_line_setname(model1,'bottom_middle-3-4',mode='x',ressetname='L3')
    
    model1 = create_single_line_setname(model1,'bottom_middle-2-3',mode='x',ressetname='L4')
    
    model1 = create_single_line_setname(model1,'bottom_left-2-3',mode='x',ressetname='L5')
    model1 = create_single_line_setname(model1,'bottom_middle-2-3',mode='x',ressetname='L5')
    model1 = create_single_line_setname(model1,'bottom_right-2-3',mode='x',ressetname='L5')
 
 
    # stretch the mesh to generate 3D
    
    L_total = 10.0
    Lincr = 2.0
    n_incr = int(L_total/Lincr)
    
    
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L1'],setname='plate_frp_L1')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L2'],setname='plate_frp_L2')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L3'],setname='plate_frp_L3')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L4'],setname='plate_frp_L4')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L5'],setname='plate_frp_L5')
    
    
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['bottom_left'],setname='solid_bottom_left')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['bottom_middle'],setname='solid_bottom_middle')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['bottom_right'],setname='solid_bottom_right')
    
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['top_left'],setname='solid_top_left')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['top_middle'],setname='solid_top_middle')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['top_right'],setname='solid_top_right')
    
    

    # merge duplicate nodes
    model1.sweep()
    
    # create interface
    #for i in range(0,floor(int(B/Lsize_seg_B)))
    interfacenodelist = model1.nodelist.select_node_coord(rz=[-0.001,0.001],ry=[t2-0.01,t2+0.01])
    #model1 = create_interface(model1,[-b1/2.0,h-tf,0],[-b1/2.0,h-tf1,0],2,24,setname='interface_left')
    
    for nodeid in interfacenodelist:
        xyz = model1.nodelist.itemlib[nodeid].xyz
        xyz = list(xyz)
        model1 = create_interface(model1,xyz,[xyz[0],xyz[1]+t3,xyz[2]],Lincr,n_incr,setname='interface')
    

    
    exp1 = exporter(model1,'hybrid_A2.proc','ex_Marc_dat')
    exp1.export('default')
    
    #t0 = time.time()    
    model1.modelsavetofile('hybrid_A2.pydat')
    #t1 = time.time() - t0
    #print 'time to save model %s ' % str(t1)
    
       

def BuildModel_hybrid_command(*args):
    model1 = model(settings)
    
    H = float(args[0])
    B = float(args[1])
    t1 = float(args[2])
    t3 = float(args[3])  # mess with t2 as t3
    b3 = float(args[4])
    a = float(args[5])
    L = float(args[6])
    Mesh_H = float(args[7])
    Mesh_B = float(args[8])
    Mesh_L = float(args[9])
        
        
    #H = 4.875           # total height
    #B = 10          # total width
    #t1 = 0.5       # thickness of the ploymer concrete
    #t3 = 0.125        # offset of the top plate
    t2 = H - t1 -t3    # height of the second portion
    
    #b3 = 1.375          # top-left portion
    b4 = B - b3 * 2 # top-middle portion
    
    b1 = b3 + t2/tan(a/180.0*3.1415926)
    b2 = B - b1 * 2
    
    #alpha = atan(t2/(b1-b3))    # incline angle
    
    # Define nodes
    N1 = [0.0,H,0]
    N2 = [0,t2,0]
    N3 = [0,0,0]
    N4 = [b3,t2,0]
    N5 = [b1,0,0]
    
    N6 = [b3+b4,t2,0]
    N7 = [b1+b2,0,0]
    
    N8 = [B,H,0]
    N9 = [B,t2,0]
    N10 = [B,0,0]
    N11 = [b3,H,0]
    N12 = [b3+b4,H,0]
    N13 = [0,t2 + t3,0]
    N14 = [b3,t2 + t3,0]
    N15 = [b3 + b4,t2 + t3,0]
    N16 = [B,t2 + t3,0]
    
    tempnodes = [N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N11,N12,N13,N14,N15,N16]
    
    # create t1
    model1.node(tempnodes)
    
    Lsize_seg_B = Mesh_B
    Lsize_seg_H = Mesh_H
    
    model1 = create_2d_patch(model1,[2,3,5,4],[floor(int(t2/Lsize_seg_H)),floor(int(b3/Lsize_seg_B))*2],setname='bottom_left')
    model1 = create_2d_patch(model1,[4,5,7,6],[floor(int(t2/Lsize_seg_H)),floor(int(b4/Lsize_seg_B))],setname='bottom_middle')
    model1 = create_2d_patch(model1,[6,7,10,9],[floor(int(t2/Lsize_seg_H)),floor(int(b3/Lsize_seg_B))*2],setname='bottom_right')

    model1 = create_2d_patch(model1,[1,13,14,11],[floor(int(t1/Lsize_seg_H))+1,floor(int(b3/Lsize_seg_B))*2],setname='top_left')
    model1 = create_2d_patch(model1,[11,14,15,12],[floor(int(t1/Lsize_seg_H))+1,floor(int(b4/Lsize_seg_B))],setname='top_middle')
    model1 = create_2d_patch(model1,[12,15,16,8],[floor(int(t1/Lsize_seg_H))+1,floor(int(b3/Lsize_seg_B))*2],setname='top_right')
    

    # create line elements that will be stretched to the frp plate
    model1 = create_single_line_setname(model1,'bottom_left-1-4',mode='x',ressetname='L1')
    model1 = create_single_line_setname(model1,'bottom_middle-1-4',mode='x',ressetname='L1')
    model1 = create_single_line_setname(model1,'bottom_right-1-4',mode='x',ressetname='L1')
    
    model1 = create_single_line_setname(model1,'bottom_left-1-4',mode='x',ressetname='L2')
    model1 = create_single_line_setname(model1,'bottom_right-1-4',mode='x',ressetname='L2')
    
    model1 = create_single_line_setname(model1,'bottom_middle-1-2',mode='x',ressetname='L3')
    model1 = create_single_line_setname(model1,'bottom_middle-3-4',mode='x',ressetname='L3')
    
    model1 = create_single_line_setname(model1,'bottom_middle-2-3',mode='x',ressetname='L4')
    
    model1 = create_single_line_setname(model1,'bottom_left-2-3',mode='x',ressetname='L5')
    model1 = create_single_line_setname(model1,'bottom_middle-2-3',mode='x',ressetname='L5')
    model1 = create_single_line_setname(model1,'bottom_right-2-3',mode='x',ressetname='L5')
 
 
    # stretch the mesh to generate 3D
    
    L_total = L
    Lincr = Mesh_L
    n_incr = int(L_total/Lincr)
    
    
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L1'],setname='plate_frp_L1')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L2'],setname='plate_frp_L2')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L3'],setname='plate_frp_L3')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L4'],setname='plate_frp_L4')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['L5'],setname='plate_frp_L5')
    
    
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['bottom_left'],setname='solid_bottom_left')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['bottom_middle'],setname='solid_bottom_middle')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['bottom_right'],setname='solid_bottom_right')
    
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['top_left'],setname='solid_top_left')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['top_middle'],setname='solid_top_middle')
    model1,a,b,c = sktretch_2dmesh(model1,n_incr,Lincr,ElemSetNameList=['top_right'],setname='solid_top_right')
    
    

    # merge duplicate nodes
    model1.sweep()
    
    # create interface
    #for i in range(0,floor(int(B/Lsize_seg_B)))
    interfacenodelist = model1.nodelist.select_node_coord(rz=[-0.001,0.001],ry=[t2-0.01,t2+0.01])
    #model1 = create_interface(model1,[-b1/2.0,h-tf,0],[-b1/2.0,h-tf1,0],2,24,setname='interface_left')
    
    for nodeid in interfacenodelist:
        xyz = model1.nodelist.itemlib[nodeid].xyz
        xyz = list(xyz)
        model1 = create_interface(model1,xyz,[xyz[0],xyz[1]+t3,xyz[2]],Lincr,n_incr,setname='interface')
    

    return model1
      
if __name__ == '__main__':
    print 11
    BuildModel_hybrid()
    
