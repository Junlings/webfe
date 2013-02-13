import numpy as np

    
def create_3d_patch(model,orgin,size,N,setname='default'):
    """ mesh the region between the four nodes and merge into the database """
    
    N = map(int,N)
    # create the coordinates and connectivity based on one
    bxyz,bcube = block3d(orgin,size,N)
    
    # add node to model starting with current highest node seq
    nn = int(model.node(bxyz))
    update_bcube = bcube + int(nn)
    
    pelemset = model.element(update_bcube,setname)
    
    
    nx = N[0] + 1
    ny = N[1] + 1
    nz = N[2] + 1
    
    
    nodeline = {}

    nodeline['1'] = [nn + 1]
    nodeline['2'] = [nn + 1 + ny*nz*(nx-1)]
    nodeline['3'] = [nn + 1 + ny*nz*(nx-1) + (ny-1)*nz]
    nodeline['4'] = [nn + 1 + nz*(ny-1)]
    nodeline['5'] = [nodeline['1'][0] + (nz-1)]
    nodeline['6'] = [nodeline['2'][0] + (nz-1)]
    nodeline['7'] = [nodeline['3'][0] + (nz-1)]
    nodeline['8'] = [nodeline['4'][0] + (nz-1)]
    
    nodeline['1-2'] = range(nodeline['1'][0],nodeline['2'][0]+1,ny*nz)
    nodeline['2-3'] = range(nodeline['2'][0],nodeline['3'][0]+1,nz)
    nodeline['3-4'] = range(nodeline['4'][0],nodeline['3'][0]+1,ny*nz)
    nodeline['1-4'] = range(nodeline['1'][0],nodeline['4'][0]+1,nz)

    nodeline['5-6'] = range(nodeline['5'][0],nodeline['6'][0]+1,ny*nz)
    nodeline['6-7'] = range(nodeline['6'][0],nodeline['7'][0]+1,nz)
    nodeline['7-8'] = range(nodeline['8'][0],nodeline['7'][0]+1,ny*nz)
    nodeline['5-8'] = range(nodeline['5'][0],nodeline['8'][0]+1,nz)
    
    nodeline['1-5'] = range(nodeline['1'][0],nodeline['5'][0]+1,1)
    nodeline['4-8'] = range(nodeline['4'][0],nodeline['8'][0]+1,1)
    nodeline['2-6'] = range(nodeline['2'][0],nodeline['6'][0]+1,1)
    nodeline['3-7'] = range(nodeline['3'][0],nodeline['7'][0]+1,1)
    
    nodeline['1-2-3-4'] = []
    nodeline['5-6-7-8'] = []
    nodeline['1-2-6-5'] = []
    nodeline['4-3-7-8'] = []
    nodeline['1-4-8-5'] = []
    nodeline['2-3-7-6'] = []
    
    for i in range(0,nx):
        for j in nodeline['1-4']:
            nodeline['1-2-3-4'].append(j + i*ny*nz)
        for j in nodeline['5-8']:
            nodeline['5-6-7-8'].append(j + i*ny*nz) 
        
        for j in nodeline['1-5']:
            nodeline['1-2-6-5'].append(j + i*ny*nz) 
        for j in nodeline['4-8']:
            nodeline['4-3-7-8'].append(j + i*ny*nz)
        
    for i in range(0,ny):
        for j in nodeline['1-5']:
            nodeline['1-4-8-5'].append(j + i*nz)
        for j in nodeline['2-6']:
            nodeline['2-3-7-6'].append(j + i*nz)
   #
    for key in nodeline:
        nodesetname = '-'.join([setname , key])
        model.nodeset(nodesetname,{'nodelist':nodeline[key]})

    return model

def block3d(orign,size,N):
    L,B,H = size
    nL,nB,nH = N
    
    
    bxyz = []
    bcube = []
    for i in range(0,nL+1):
        for j in range(0,nB+1):
            for k in range(0,nH+1):
                bx = orign[0] + i * L
                by = orign[1] + j * B 
                bz = orign[2] + k * H
                
                bxyz.append([bx,by,bz])
                
    
    for i in range(0,nL):
        for j in range(0,nB):
            for k in range(0,nH):
                N1 = 1 + k + j * (nH+1) + i * ((nB+1)*(nH+1)) 
                N2 = 1 + k + j * (nH+1) + (i+1) * ((nB+1)*(nH+1)) 
                N3 = 1 + k + (j+1) * (nH+1) + (i+1) * ((nB+1)*(nH+1)) 
                N4 = 1 + k + (j+1) * (nH+1) + i * ((nB+1)*(nH+1))
                N5 = N1 + 1 
                N6 = N2 + 1
                N7 = N3 + 1
                N8 = N4 + 1
                bcube.append([N1,N2,N3,N4,N5,N6,N7,N8])
                #print [N1,N2,N3,N4,N5,N6,N7,N8]
                
    return np.array(bxyz),np.array(bcube)
    
"""

if __name__ == '__main__':
    
    xy = np.array([[0.0,1,1,0],[0.0,0,1,1]]).T
    N = [2,3]
    bxy,btri = block(xy,N,type=4)
    
    print bxy
    print btri
    print 1
"""