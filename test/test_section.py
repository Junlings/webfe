
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

from numpy import exp,sin,cos,arctan,abs,sqrt

import numpy as np
import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

    
def test_section():
    model1 = model(settings)
    
    model1.material('m1','uniaxial_elastic',paralib={'E':29000.0,'mu':0.3,'mass':0.0})
    prop = {'mattag':'m1','numLine':10,'widthLine':1,'yStart':0,'zStart':0,'yEnd':10,'zEnd':10}
    prop2 = {'mattag':'m1','numLine':10,'widthLine':1,'yStart':0,'zStart':0,'yEnd':10,'zEnd':-10}
    
    model1.section('sec1','fibersection',{'layerlib':{'1':{'type':'line','prop':prop},
                                                      '2':{'type':'line','prop':prop2}},
                                           'patchlib':{},
                                           'fiberlib':{}})
    model1.seclist['sec1'].collect_fibers()
    
    
    PlotFiberSection(model1,'sec1')
    print 1

def PlotFiberSection(model1,seckey):
    ''' create section plot for the fiber section '''
    SecInst = model1.seclist[seckey]
    
    # start plot
    fig=plt.figure()
    ax=fig.add_subplot(111)

    PlotFiber(SecInst,ax)
    
    PlotPatchRec(SecInst,ax)
    
    plt.show()
    
def PlotPatchRec(SecInst,ax):
    ''' create the patch '''
    
    for key,item in SecInst.layerlib.items():
        if item['type'] == 'line':
            PlotPatchLine(ax,item['prop'])

def PlotPatchLine(ax,prop):
    length = ((prop['yEnd']-prop['yStart'])**2+(prop['zEnd']-prop['zStart'])**2) ** 0.5
    ang = arctan((prop['zEnd']-prop['zStart'])/(prop['yEnd']-prop['yStart']))
    ang = ang / 3.1415926*180
    width = prop['widthLine']
    patchi = Rectangle((prop['yStart'],prop['zStart']-width/2.0),length,width,color='blue',alpha=0.5)

    
    t2 = matplotlib.transforms.Affine2D().rotate_deg(ang) + ax.transData
    patchi.set_transform(t2)
    
    ax.add_patch(patchi)    
    
def PlotFiber(SecInst,ax):
    
    areafactor = 0.5 # area display factor 
    
    circlelist = []
    
    # max and min of the range
    ymax = 1
    ymin = 0
    zmax = 1
    zmin = 0
    
    for key,fiber in SecInst.fiber.items():
        # get coordinates
        x1 = fiber.locy
        y1 = fiber.locz
        # uodate limits
        if x1 > ymax: ymax = x1
        if x1 < ymin: ymin = x1
        if y1 > zmax: zmax = y1
        if y1 < zmin: zmin = y1
        #calculate display area
        r = (fiber.area / 3.14159265358) ** 0.5 * areafactor
        circlelist.append(Circle((x1,y1), r))
    

    # set limits for both axis    
    yzmax = max(ymax,zmax) * 2
    yzmin = max(ymin,zmin) * 2
    
    yband = ymax - ymin
    zband = zmax - zmin
    
    ydis = (yzmax - yband) / 2.0
    zdis = (yzmax - zband) / 2.0

    ax.set_xlim( ymin - ydis,ymax + ydis)
    ax.set_ylim( zmin - zdis,zmax + zdis)

    ax.set_aspect('equal')    
    
    p = PatchCollection(circlelist, cmap=matplotlib.cm.jet, alpha=1.0,color='red')
    ax.add_collection(p)    

if __name__ == '__main__':
    
    test_section()
    
