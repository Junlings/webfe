""" This is the procedure to add dent to the regular meshed pole model"""
#import sys
#import os
#import datetime
#sys.path.append('../../webfe/')
import numpy as np
from core.model.registry import model
#from core.export.export import exporter
from core.settings import settings
#from core.procedures.t_section import tsec_planeconfig
#from core.procedures.rec_section import rec_planeconfig
#from core.imports.marc.import_marc_dat import importfile_marc_dat
#from core.post.import_marc_t16 import post_t16
#from core.plots.plots import tpfdb

#from command import commandparser
from core.utility.fem.create_arcplane import create_cylinderSurface

from numpy import exp,sin,cos,arctan,abs,sqrt
#import matplotlib.pyplot as plt
import time

def dent_function_numeric(x,y):
    ''' the defination of the curve fitting dent function
        Obtain by curve fitting the model scan files
    '''
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
    
    
    #if denty > 1:
    #    denty = 1
    
    if y < 0.2:
        denty = 1.*cos(3.345620398*y)
    return dentx * denty


def plot_dentmap(zcrit):
    ''' facilitate to show the dent map based on the input parameters '''
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
    
def dent_function_node(model1,nodeid,deepdent,zcrit):
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
    
    #zcrit = 200
    
    dent = dent_function_numeric(z/zcrit,fi/3.1415926)
    
    
    
    if rr != 0:
        dentvalue = (dent * deepdent)  #
        x = (rr-dentvalue) * xyz[0]/rr 
        y = (rr-dentvalue) * xyz[1]/rr 
        
        dx = xyz[0] - x
        dy = xyz[1] - y
        if z == 0: #and abs(fi) < 0.01:
            pass
            #print z,fi0,fi,dent,x,y,deepdent,rr
    else:
        x = 0
        y = 0
        z = 0
        fi = 0
        
    return x,y,z,fi


def add_dent_asdeform(model1,deepdent=1,zcrit=200):
    ''' apply function to all model nodes'''
    
    dentnode = []
    for key in model1.nodelist.itemlib.keys():
        '''loop over all nodes'''
        x,y,z,fi = dent_function_node(model1,key,deepdent,zcrit)
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

def add_dent_asdeform_filled(model1,deepdent=1,zcrit=200,wrap=None):
    ''' apply function to all model nodes with filled 3D solid elements'''
    critical_thickness = 1
    dentnode = []
    node_res = []
    node_alter_dict = {}
    ii = 1
    
    t0 = time.time()
    # apply dent function
    for key in model1.nodelist.itemlib.keys():
        '''loop over all nodes'''
        x,y,z,fi = dent_function_node(model1,key,deepdent,zcrit)
        xyz = model1.nodelist.itemlib[key].xyz
        

        if xyz[2] > 0:
            denttempnode = model1.nodelist.itemlib[key].xyz
            model1.nodelist.itemlib[key].xyz = np.array([x,y,z])
            
        else:
            denttempnode = model1.nodelist.itemlib[key].xyz  # due to function
            model1.nodelist.itemlib[key].xyz = np.array([x,y,-z])  # due to function
        
        if (x-xyz[0])*(x-xyz[0]) + (y-xyz[1])*(y-xyz[1]) > critical_thickness: # all dentnode
        
            if (x*x+y*y)- (xyz[0]*xyz[0]+xyz[1]*xyz[1]) < -1*critical_thickness and y>0:  # apply to the fill region
                dentnode.append(denttempnode)
                node_res.append([denttempnode[0],denttempnode[1],denttempnode[2],key])
                
                
                node_alter_dict[key] = ii   # this is 
                ii += 1
    t1 = time.time() - t0
    print '----time to collect node information %s ' % str(t1)
    
    t0 = time.time()
    nn = model1.node(dentnode,setname='dentnodes')
    t1 = time.time() - t0
    print '----time to create nodes %s ' % str(t1)    
    
    t0 = time.time()
    # update the wrap elements
    if 'wrap' in model1.setlist.keys():
        elemlist = model1.setlist['wrap'].elemlist
        
        for elem in elemlist:
            temp = []
            for nodeid in model1.connlist.itemlib[elem].nodelist:
                if nodeid in node_alter_dict.keys():
                    temp.append(node_alter_dict[nodeid]+nn)
                else:
                    temp.append(nodeid)
            model1.connlist.itemlib[elem].nodelist = temp
    t1 = time.time() - t0
    print '----time to create wrap %s ' % str(t1)                
            
    t0 = time.time()
    for i in range(0,len(node_res)):
        node_res[i].append(nn+i+1)
        
    model1 = create_fill(model1,node_res)
    # add node with dent to nodelist    
    t1 = time.time() - t0
    print '----time to create fill %s ' % str(t1)         
        
    return model1


def get_fi(xyz):

    if xyz[0] != 0:
        fi0 = arctan((xyz[1]/xyz[0]))
    else:
        fi0 = 3.1415926/2
        
    if (xyz[0] > 0) and (xyz[1] > 0):
        fi = 3.1415926/2 - abs(fi0)
    elif xyz[0] < 0 and xyz[1] < 0:
        fi = -3.1415926/2 + abs(fi0)
    elif xyz[0] > 0 and xyz[1] < 0:
        fi = 3.1415926/2 - abs(fi0)
    elif xyz[0] < 0 and xyz[1] > 0:
        fi = -3.1415926/2 + abs(fi0)
    else:
        fi = fi0
    
    return fi


def create_wrap(model1,left,right):
    ''' create the wrap element based on regular shape mesh'''
    # get node within range
    wrapnodelist = model1.nodelist.select_node_coord(rz=[left,right])
    # get elements within range
    wrapelementlist= model1.select_elements_nodelist(wrapnodelist)
    
    
    tempelement = []
    
    for elem in wrapelementlist:
        tempelement.append(model1.connlist.itemlib[elem].nodelist)
        
    model1.element(tempelement,setname='wrap')

    return model1




def create_fill(model1,node_res):
    ''' create fill based on the detected dent and original nodes '''
    
    zlist = []
    rlist = []
    temp = []
    # get the list of z and L
    for i in range(0,len(node_res)):
        if node_res[i][2] not in zlist:
            zlist.append(node_res[i][2])
        fi0 = get_fi(node_res[i])
        fi0 = round(fi0,2)
        if fi0 not in rlist:
            rlist.append(fi0)
            
        temp.append([node_res[i][0],node_res[i][1],node_res[i][2],fi0,node_res[i][3],node_res[i][4]])
        
    # detect the neibouring nodes
    temp = np.array(temp)
    zlist.sort()
    rlist.sort()
    
    ind = []
    for i in zlist:
        tempind = []
        for j in rlist:
            tempind.append(find_nearest2d(temp,i,2,j,3))
            
        ind.append(tempind)
    
    ind = np.array(ind)
    # Add solid elements
    tempelem = []
    for i in range(0,len(zlist)-1):
        for j in range(0,len(rlist)-1):
            Node1 = temp[ind[i,j],4]
            Node2 = temp[ind[i,j+1],4]
            Node3 = temp[ind[i+1,j+1],4]
            Node4 = temp[ind[i+1,j],4]
            Node5 = temp[ind[i,j],5]
            Node6 = temp[ind[i,j+1],5]
            Node7 = temp[ind[i+1,j+1],5]
            Node8 = temp[ind[i+1,j],5]
            
            try:
                Nodelist = map(int,[Node5,Node6,Node7,Node8,Node1,Node2,Node3,Node4])
                tempelem.append(Nodelist)
            except:
                pass
            
    model1.element(tempelem,setname='Fill Material')
    return model1

def find_nearest2d(array,value1,ind1,value2,ind2,err=0.01):
    for i  in range(0,array.shape[0]):
        
        if abs(array[i,ind1] - value1) < err and abs(array[i,ind2] - value2) < err:
            return i

def add_material(model1):
    ''' this is the defination of the steel and aluminum material'''
    '''
    ss_pole_steel = [[0,0],
                     [0.0018,53.800],
                     [0.03,54],
                     [0.12,64],
                     [0.121,0],
                     [0.5,0]]
    model1 = add_mat_by_stressstrain(model1,'pole_steel',ss_pole_steel,0.0018)
    model1 = add_mat_by_stressstrain(model1,'pole_steel_dent',ss_pole_steel,0.0018)
    
    ss_pole_alum = [[0,0],
                    [0.004,33],
                    [0.054,36],
                    [0.0541,0],
                    [0.5,0]]
    model1 = add_mat_by_stressstrain(model1,'pole_alum',ss_pole_alum,0.004)
    model1 = add_mat_by_stressstrain(model1,'pole_alum_dent',ss_pole_alum,0.004)
    '''
    # add filler material property
    model1.material('mat_alum','uniaxial_elastic',{'E':57.8,'mu':0.3,'mass':0.0})
    model1.material('mat_alum_dent','uniaxial_elastic_plastic',{'E':57.8,'mu':0.3,'mass':0.0,'sigma_y':0.203,'tabletag':'Alum'})
    model1.material('mat_interface','interface_marc_builtin',{'mattype':'linear','Gc':1,'vc':0.03,'vm':0.1,'s_n':1,'s_n_c':1,'stiff_c':1})
    model1.material('mat_fill','uniaxial_elastic',{'E':0.5464,'mu':0.3,'mass':0.0})
    model1.material('mat_wrap','uniaxial_elastic',{'E':1.263,'mu':0.3,'mass':0.0})
    
    return model1


def create_interface(model1):
    ''' create interface between wrap and fill/dent '''

    if 'wrap' in model1.setlist.keys():
        elemlist = model1.setlist['wrap'].elemlist
        temp = []    
        for elem in elemlist:
            temp.extend(model1.connlist.itemlib[elem].nodelist)
        
        tempset = set(temp)
        
        templist = list(tempset)
        templist.sort()
        nn = model1.node_copy(templist,setname='copy_wrap')
        
        elemtemp = []
        interfacetemp = []
        for elem in elemlist:
            nodelisttemp = []
            newnodelist = list(model1.connlist.itemlib[elem].nodelist)
            for node in model1.connlist.itemlib[elem].nodelist:
                nodelisttemp.append(nn + templist.index(node)+1)
            
            elemtemp.append(nodelisttemp)
            newnodelist.extend(nodelisttemp)
            interfacetemp.append(newnodelist)
        
        model1.element(elemtemp,setname='new_wrap')
        model1.element(interfacetemp,setname='interface')
        
        
        # delete the original wrap elements
        #elemlist = model1.setlist['wrap'].elemlist
        #model1.delete_elements(elemlist)
        return model1
    
    
    

def procedure_pole_imposedent(*args):
    model1 = model(settings)
    LEFTEND_XCOORD = float(args[0])
    RIGHTEND_XCOORD = float(args[1])
    LEFTEND_RAD= float(args[2])
    RIGHTEND_RAD = float(args[3])
    LENGTH_INCR = float(args[4])
    LENGTH_RAd = float(args[5])
    DEEP_DENT = int(args[6])
    CRIT_LENGTH = int(args[7])
    IFFILLED = args[8]
    
    IFWRAP = args[9]

    t0 = time.time()
    
    #create cylinder surface  x0,y0,z0,r0,r1,L,nfi,nZ)
    model1 = create_cylinderSurface(model1,0,0, LEFTEND_XCOORD,LEFTEND_RAD,RIGHTEND_RAD,RIGHTEND_XCOORD-LEFTEND_XCOORD,LENGTH_RAd,LENGTH_INCR)
    t1 = time.time() - t0
    print 'time to create cylinder surface %s ' % str(t1)
        
    # add wrap of possible    
    if IFWRAP == 'True':
        t0 = time.time()
        WRAPLEFT = float(args[10])
        WRAPRIGHT = float(args[11])
        model1 = create_wrap(model1,WRAPLEFT,WRAPRIGHT)
        t1 = time.time() - t0
        print 'time to create wrap %s ' % str(t1)
        
    # Add artificial dent and fill if possible
    if IFFILLED == 'False':
        t0 = time.time()
        model1 = add_dent_asdeform(model1,deepdent=DEEP_DENT, zcrit=CRIT_LENGTH)
        t1 = time.time() - t0
        print 'time to enforce dent %s ' % str(t1)
        
    elif IFFILLED == 'True':
        t0 = time.time()
        model1 = add_dent_asdeform_filled(model1,deepdent=DEEP_DENT, zcrit=CRIT_LENGTH,wrap=IFWRAP)
        t1 = time.time() - t0
        print 'time to enforce dent and fill %s ' % str(t1) 
    else:
        raise ValueError,("The key for fillment detection do not find")
    
    
    # add interface elements between the wrap and fill/steel
    if IFFILLED == 'True'  and IFWRAP == 'True':
        t0 = time.time()
        model1 = create_interface(model1)
        t1 = time.time() - t0
        print 'time to create interface %s ' % str(t1) 
    
        t0 = time.time()
        elemlist = model1.setlist['wrap'].elemlist
        model1.delete_element_byset('wrap')
        t1 = time.time() - t0
        print 'time to delete reference wrap %s ' % str(t1)
    
    
    # Add typical node for loading and support
    #pnodelist = model1.nodelist.select_node_coord([xmin,xmax],[ymin,ymax],[zmin,zmax])
    #model1.nodeset(name,{'nodelist':pnodelist})
    
    # add material
    model1 = add_material(model1)
     
        
    model1.property('prop_alum','quad4',{'type':75,'thinkness':4.59})
    model1.property('prop_alum_dent','quad4',{'type':75,'thinkness':4.59})
    model1.property('prop_fill','hex8',{'type':7})
    model1.property('prop_wrap','quad4',{'type':75})
    model1.property('interface','quad4',{'type':186})    

    model1.link_mat_prop('mat_alum','prop_alum')
    model1.link_mat_prop('mat_alum_dent','prop_alum_dent')
    model1.link_mat_prop('mat_interface','interface')
    model1.link_mat_prop('mat_fill','prop_fill')
    model1.link_mat_prop('mat_wrap','prop_wrap')
    
    return model1



if __name__ == '__main__':
    
    test_procedure()
    #plot_dentmap(200)
