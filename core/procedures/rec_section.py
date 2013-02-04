from __future__ import division

import numpy as np

from core.model.registry import model
from core.settings import settings
from core.lib.libop import save, load
from core.export.export import exporter
from core.utility.fem.create_2d_patch import block2d
from core.utility.fem.create_single_line_nodelist import create_single_line_nodecoord
from core.utility.geometry.DistancePointLine import DistancePointLine,UdirectionPointLine, Parameter,Find_angle
from core.imports.marc.import_marc_dat import importfile_marc_dat
from core.utility.table.stress_strain import add_mat_by_stressstrain
from math import atan,floor
from core.utility.fem.create_prism_by_stretch import sktretch_2dmesh

def rec_planeconfig(model1,name,b,h,d,bh,hh,LL,dL):
    """ Create nodes and elements on surface """
    
    nsegL = int(LL/dL)
    nod1 = (-b/2.0,h,0)
    nod2 = (-b/2.0,h-d+hh/2.0,0)
    nod3 = (-b/2.0,h-d-hh/2.0,0)
    nod4 = (-b/2.0,0,0)
    nod5 = (-bh/2.0,h,0)
    nod6 = (-bh/2.0,h-d+hh/2.0,0)
    nod7 = (-bh/2.0,h-d-hh/2.0,0)
    nod8 = (-bh/2.0,0,0)
    nod9 = (0,h,0)
    nod10 = (0,h-d+hh/2.0,0)
    nod11 = (0,h-d-hh/2.0,0)
    nod12 = (0,0,0)
    
    
    # create plane 2d connectivity
    model1 = create_2D_patch_xy(model1,nod1,nod4,nod8,nod5,0.25,0.25)
    model1 = create_2D_patch_xy(model1,nod5,nod6,nod10,nod9,0.25,0.25)
    model1 = create_2D_patch_xy(model1,nod7,nod8,nod12,nod11,0.25,0.25)
    
    # strecth 2d to 3d
    model1,nodekeylist,new_id,n_nodelist = sktretch_2dmesh(model1,nsegL,dL)
    
    
    # add reinforcement
    model1 = create_single_line_nodecoord(model1,[0,h-d,0],[0,h-d,LL],nsegL)
    
    
    # create interface elements
    topnodeid = model1.pick_node_coord_3d([0,h-d+hh/2.0,0])
    botnodeid = model1.pick_node_coord_3d([0,h-d-hh/2.0,0])
    centernodeid = model1.pick_node_coord_3d([0,h-d,0])
    
    tempquadnodelist = []
    for i in range(0,nsegL):
        if i == 0:
            tempquadnodelist.append([centernodeid,centernodeid+2,new_id+1+nodekeylist.index(topnodeid),topnodeid])
            tempquadnodelist.append([botnodeid,new_id+1+nodekeylist.index(botnodeid),centernodeid+2,centernodeid])
        elif i == nsegL-1:
            
            tempquadnodelist.append([centernodeid+i+1,centernodeid+1,
                                     new_id+1+nodekeylist.index(topnodeid)+n_nodelist*(i),
                                     new_id+1+nodekeylist.index(topnodeid)+n_nodelist*(i-1)])
            tempquadnodelist.append([new_id+1+nodekeylist.index(botnodeid)+n_nodelist*(i-1),
                                     new_id+1+nodekeylist.index(botnodeid)+n_nodelist*(i),
                                     centernodeid+1,centernodeid+i+1])
        else:
            tempquadnodelist.append([centernodeid+i+1,centernodeid+i+2,
                                     new_id+1+nodekeylist.index(topnodeid)+n_nodelist*(i),
                                     new_id+1+nodekeylist.index(topnodeid)+n_nodelist*(i-1)])
            tempquadnodelist.append([new_id+1+nodekeylist.index(botnodeid)+n_nodelist*(i-1),
                                     new_id+1+nodekeylist.index(botnodeid)+n_nodelist*(i),
                                     centernodeid+i+2,centernodeid+i+1])

    model1.element(tempquadnodelist)
    

    return model1
    
def create_2D_patch_xy(model1,N1,N2,N3,N4,lsize,bsize):
    xy = np.array([[N1[0],N2[0],N3[0],N4[0]],
                   [N1[1],N2[1],N3[1],N4[1]]]).T
    
    dx = max(abs(N1[0]-N2[0]),abs(N1[0]-N3[0]),abs(N1[0]-N4[0]),abs(N2[0]-N3[0]),abs(N2[0]-N4[0]),abs(N3[0]-N4[0]))
    dy = max(abs(N1[1]-N2[1]),abs(N1[1]-N3[1]),abs(N1[1]-N4[1]),abs(N2[1]-N3[1]),abs(N2[1]-N4[1]),abs(N3[1]-N4[1]))
    
    nb = int(floor(dx/lsize))
    nl = int(floor(dy/bsize))
    N = [nl,nb]
    model1 = block2d(model1,xy,N,type=4,z=0,setname=None)    
    
    return model1
    
    
if __name__ == '__main__':
    
    model1 = model(settings)
    tsec_planeconfig(model1,name,bf,tf,tf1,hw,tw,d,ds)