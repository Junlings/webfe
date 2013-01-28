from __future__ import division

import numpy as np

from core.model.registry import model
from core.settings import settings
from core.lib.libop import save, load
from core.export.export import exporter
from core.utility.fem.create_2d_patch import block2d
from core.utility.geometry.DistancePointLine import DistancePointLine,UdirectionPointLine, Parameter,Find_angle
from core.imports.marc.import_marc_dat import importfile_marc_dat
from core.utility.table.stress_strain import add_mat_by_stressstrain
from math import atan,floor


def tsec_planeconfig(model1,name,bf,tf,tf1,hw,tw,d,ds):
    """ Create nodes and elements on surface """
    
    h = tf + hw
    
    nod1 = (-bf/2.0,h,0)
    nod2 = (-bf/2.0,h-tf1,0)
    nod3 = (-tw/2.0,hw,0)
    nod4 = (-tw/2.0,h,0)
    nod5 = (-tw/2.0,0,0)
    nod6 = (0.0,h,0)
    nod7 = (0,0,0)
    #nod8 = (0,h-d,0)
    nod9 = (-ds/2,h,0)
    nod10 = (-tw/2,h-d+ds/2,0)
    nod11 = (-tw/2,h-d-ds/2,0)
    nod12 = (-ds/2,h-d+ds/2,0)
    nod13 = (-ds/2,h-d-ds/2,0)
    nod14 = (0,h-d+ds/2,0)
    nod15 = (0,h-d-ds/2,0)
    nod16 = (-ds/2,0,0)
    
    model1 = create_2D_patch_xy(model1,nod1,nod2,nod3,nod4,1,0.25)
    model1 = create_2D_patch_xy(model1,nod4,nod10,nod12,nod9,0.25,0.25)
    model1 = create_2D_patch_xy(model1,nod10,nod11,nod13,nod12,0.25,0.25)
    model1 = create_2D_patch_xy(model1,nod11,nod5,nod16,nod13,0.25,0.25)
    model1 = create_2D_patch_xy(model1,nod9,nod12,nod14,nod6,0.25,0.25)
    model1 = create_2D_patch_xy(model1,nod13,nod16,nod7,nod15,0.25,0.25)
    
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