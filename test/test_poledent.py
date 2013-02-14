
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
from core.utility.fem.create_arcplane import create_cylinderSurface

from numpy import exp,sin,cos,arctan,abs,sqrt
import matplotlib.pyplot as plt

def dent_function_numeric(x,y):
    ''' the defination of the curve fitting dent function '''
    _C3 = 1
    _C4 = 1
    gamma = 0.5
    _C5 = 1
    _C6 = 1
    gamma2 = 3.1415926
    Pi = 3.1415926
    
    #dent = (_C3*exp(-gamma*x) * sin(gamma*x) + _C4*exp(-gamma*x)*cos(gamma*x)) * (_C5*exp(-gamma2*(y/Pi)**1)*sin(-gamma2*(y/Pi)**1)+_C6*exp(-gamma2*(y/Pi)**1)*cos(-gamma2*(y/Pi)**1))
    denty = .5250000000*cos(6.283185200*y)+.2250000001+.5624999860*cos(3.141592600*y)+.1875000141*cos(9.424777800*y)
    dentx = exp(-3*x)*cos(x)
    if denty > 1:
        denty = 1
    return dentx * denty


def plot_dentmap(zcrit):
    zcrit = 430
    nz = 100
    nr = 100
    dentz = []
    locz = []
    locr = []
    dentr = []
    # variation from length direction
    for iz in range(0,nz):
        z = iz * 2*float(zcrit)/(float(nz))
        locz.append(z)
        dentz.append(dent_function_numeric(z/zcrit,0))
    
    # variation in the hoop direction
    for ir in range(0,nr):
        r = ir * float(3.1415926*2.0/nr)
        locr.append(r)
        dentr.append(dent_function_numeric(0,r/3.1415926))
    
    
        
    
    plt.plot(locz,dentz)
    plt.show()
    
    plt.plot(locr,dentr)
    plt.show()
    
def dent_function_node(model1,nodeid,deepdent):
    ''' add dent to the node '''
    
    xyz = model1.nodelist.itemlib[nodeid].xyz
    
    if abs(xyz[0]) < 0.001 and  abs(xyz[1]) < 0.001:
        ''' this is the control nodes at two ends, no need for deformation'''
        return xyz[0],xyz[1],xyz[2],0
    
    z = abs(xyz[2])
    if xyz[0] != 0:
        fi0 = arctan((xyz[1]/xyz[0]))
    else:
        fi0 = 3.1415926/2
        
    if (xyz[0] > 0) and (xyz[1] > 0):
        fi = 3.1415926/2 - abs(fi0)
    elif xyz[0] < 0 and xyz[1] < 0:
        fi = 3.1415926/2 + abs(fi0)
    elif xyz[0] > 0 and xyz[1] < 0:
        fi = 3.1415926/2 + abs(fi0)
    elif xyz[0] < 0 and xyz[1] > 0:
        fi = 3.1415926/2 - abs(fi0)
    else:
        fi = fi0
    
    rr = sqrt(xyz[0]*xyz[0] +xyz[1]*xyz[1])
    
    zcrit = 200
    
    dent = dent_function_numeric(z/zcrit,fi/3.1415926)
    
    
    
    if rr != 0:
        dentvalue = (dent * deepdent)  #
        x = (rr-dentvalue) * xyz[0]/rr 
        y = (rr-dentvalue) * xyz[1]/rr 
        
        dx = xyz[0] - x
        dy = xyz[1] - y
        if z == 0: #and abs(fi) < 0.01:
            print z,fi0,fi,dent,x,y,deepdent,rr
    else:
        x = 0
        y = 0
        z = 0
        fi = 0
        
    return x,y,z,fi

def add_dent_asdeform(model1,deepdent=1):
    ''' apply function to all model nodes'''
    
    dentnode = []
    for key in model1.nodelist.itemlib.keys():
        x,y,z,fi = dent_function_node(model1,key,deepdent)
        xyz = model1.nodelist.itemlib[key].xyz
        
        if xyz[2] > 0:
            model1.nodelist.itemlib[key].xyz = np.array([x,y,z])
        else:
            model1.nodelist.itemlib[key].xyz = np.array([x,y,-z])  # due to function
        
        
        if (x-xyz[0])*(x-xyz[0]) + (y-xyz[1])*(y-xyz[1]) > 0.05:
            dentnode.append(key)
    
    # add node with dent to nodelist    
    model1.nodeset('dentnodes',{'nodelist':dentnode})
    
    return model1

    
def test_procedure_pole():
    model1 = model(settings)

    x0 = 0 
    y0 = 0 
    z0 = -1600
    R1 = 71
    R2 = 73
    L = 2743
    nfi = 16
    nL = 270
    deepdent = 50
    ifdent = True
    dent = "add_dent_asdeform"
    
    model1 = create_cylinderSurface(model1,x0,y0,z0,R1,R2,L,nfi,nL,deepdent=0,setname='surface',dent=ifdent,folder='default')
    

    if dent == 'add_dent_asdeform':
        model1 = add_dent_asdeform(model1,deepdent=deepdent)
        
        elemlist = model1.select_elements_nodeset('dentnodes')
        
        elemseqlist = []

        for key in elemlist:#.keys():
            elemseqlist.append(key)#elemlist[key])
        '''
        for key in elemlist.keys():
            elemseqlist.extend(elemlist[key])
        '''
        elemseqlist = list(set(elemseqlist))
        
        model1.elemset('dentelems',{'elemlist':elemseqlist})
        print 1
        
    
    
    model1.modelsavetofile('temp.pydat')
    
    
    #model1 = model1.modelloadbyfile('temp.pydat')
    #print model1.get_element_typeid(100)
    print 1


if __name__ == '__main__':
    
    #test_procedure_pole()
    plot_dentmap(200)
