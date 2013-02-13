import numpy as np
import time
    
def create_interface(model1,originx,originy,DZincr,Nincr,setname='default',DXincr=0,DYincr=0):
    """ create interface between two lines from originx and originy """
    tempelem = []
    nodecoordlist = []
    for i in range(0,Nincr):
        N1_coord = [originx[0] + i * DXincr,originx[1] + i * DYincr,originx[2] + i * DZincr]
        N2_coord = [originx[0] + (i+1) * DXincr,originx[1] + (i+1) * DYincr,originx[2] + (i+1) * DZincr]
        N3_coord = [originy[0] + i * DXincr,originy[1] + i * DYincr,originy[2] + i * DZincr]
        N4_coord = [originy[0] + (i+1) * DXincr,originy[1] + (i+1) * DYincr,originy[2] + (i+1) * DZincr]
        
        nodecoordlist.extend([N1_coord,N2_coord,N3_coord,N4_coord])
    
    #t0 = time.time()
    res = model1.nodelist.pick_node_coordlist(nodecoordlist)
    
    model1.nodeset('node_'+setname,{'nodelist':res})
    #t1 = time.time() - t0
    #print 'time to pick nodes %s ' % str(t1)
    
    #t0 = time.time()
    for i in range(0,Nincr):
        
        N1 = res[i*4]
        N2 = res[i*4+1]
        N3 = res[i*4+2]
        N4 = res[i*4+3]
        
        tempelem.append([N2,N1,N3,N4])    
    
    model1.element(tempelem,setname=setname)
    #t1 = time.time() - t0
    #print 'time to construct elements %s ' % str(t1)    
    
    
    return model1
"""

if __name__ == '__main__':
    
    xy = np.array([[0.0,1,1,0],[0.0,0,1,1]]).T
    N = [2,3]
    bxy,btri = block(xy,N,type=4)
    
    print bxy
    print btri
    print 1
"""