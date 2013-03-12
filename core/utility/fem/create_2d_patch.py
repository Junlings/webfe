import numpy as np

    
def create_2d_patch(model,nodeseq,N,type=4,setname='default',z=0):
    """ mesh the region between the four nodes and merge into the database """
    
    # get corner coordinates based on nodes
    xy = np.array([model.nodelist.itemlib[nodeseq[1-1]].xyz,
                   model.nodelist.itemlib[nodeseq[2-1]].xyz,
                   model.nodelist.itemlib[nodeseq[3-1]].xyz,
                   model.nodelist.itemlib[nodeseq[4-1]].xyz])
    
    # create the coordinates and connectivity based on one
    bxy,btri = block(xy,N,type=4,z=z)
    
    # add node to model starting with current highest node seq
    nn = model.node(bxy)
    nodeline = {}
    nodeline['1-2'] = range(nn+1,nn + N[0]+1+1)
    nodeline['2-3'] = range(nn+N[0]+1,nn +1+ (N[0]+1)*(N[1]+1),N[0]+1)
    nodeline['3-4'] = range(nn+1+(N[0]+1)*(N[1]),nn +1+ (N[0]+1)*(N[1]+1))
    nodeline['1-4'] = range(nn+1,nn +1+ (N[0]+1)*(N[1]+1),N[0]+1)
    nodeline['1'] = [nn + 1]
    nodeline['2'] = [nn + N[0]+1]
    nodeline['3'] = [nn+1+(N[0]+1)*(N[1])]
    nodeline['4'] = [nn + (N[0]+1)*(N[1]+1)]
    # update the nodelist seq for connectivity
    update_btri = btri + nn
    
    # add connectivity to model
    pelemset = model.element(update_btri,setname)
    
    #
    for key in nodeline:
        nodesetname = '-'.join([setname , key])
        model.nodeset(nodesetname,{'nodelist':nodeline[key]})
    return model

def block2d(model,xy,N,type,z=0,setname=None):
    bxy,btri = block(xy,N,type=4,z=z)
    nn = model.node(bxy)
    update_btri = btri + nn
    pelemset = model.element(update_btri,setname)
    return model
    
def block(xy,N,type=None,z=0):
    """
    % B=BLOCK(XY,N,TYPE) Generate triangular finite element mesh
    % 
    % Given quadrilateral node coordinates xy, return a data structure
    % for generating a finite element mesh with n(1) by n(2) elements.
    %
    % Input Variables
    % ---------------
    % XY = 4 element node arrays
    % N = 2-vector with number of elements in node 1-2 and node 2-3 directions
    % TYPE = element type 3=triangules, 4=4-node quadrilaterals
    %
    % The coordinates for the four corner nodes of the block
    % must follow the following numbering convention
    % and the right hand rule for the XY coordinate system
    %
    %     4 --------- 3
    %     |           |
    %     |           |
    %     |           |
    %     |           |
    %     |           |
    %     1 --------- 2
    %
    % Example:
    %    x = [0 1 2 -1] ;
    %    y = [0 0 1 1] ;
    %    XY = [x',y']
    %
    %    b = block(XY,[2;2]) ;
    %
    % creates a 2x2 mesh of elements with corners 1: (0,0), 2: (1,0),
    % 3: (2,1) and 4: (-1,1)
    
    % Daniel C. Simkins, Jr. (dsimkins@ce.berkeley.edu)
    % Gregory L. Fenves (fenves@ce.berkeley.edu)
    % University of California, Berkeley
    % ------------------------------------------------------
    """
    
    N[0] = int(N[0])
    N[1] = int(N[1])
    
    l = len(xy)
    
    if type == None:
        type = 3
        
    if type != 3 and type != 4:
        raise TypeError, 'BLOCK--> only element types 3 and 4 currently supported'
        return -1
    
    if len(N) != 2:
        raise ValueError,'ERROR in function block --> n not of lenth 2',len(N)
        return -1
    
    if min(N) < 1:
        raise ValueError,'ERROR in function block --> n does not contain valid sizes',min(N)
        return -1

    nodesx = N[0] + 1
    nodesy = N[1] + 1
    
    if xy[1-1,1-1] == xy[4-1,1-1]:
        xl = np.ones((nodesy)) * xy[1-1,1-1]
        
    else:
        xl = np.linspace(xy[1-1,1-1],xy[4-1,1-1],nodesy)
        
        
    if xy[2-1,1-1] == xy[3-1,1-1]:
        xr = np.ones((nodesy)) * xy[2-1,1-1]
    else:
        xr = np.linspace(xy[2-1,1-1],xy[3-1,1-1],nodesy)        

    if xy[1-1,2-1] == xy[4-1,2-1]:
        yl = np.ones((nodesy)) * xy[1-1,2-1]
    else:
        yl = np.linspace(xy[1-1,2-1],xy[4-1,2-1],nodesy)  

    if xy[2-1,2-1] == xy[3-1,2-1]:
        yr = np.ones((nodesy)) * xy[2-1,2-1]
    else:
        yr = np.linspace(xy[2-1,2-1],xy[3-1,2-1],nodesy)


        
    #print xy
    #print xl,xr,yl,yr
    
    bxy = np.zeros((nodesx*nodesy,3))
    
    for i in range(1,nodesy+1):
        istart = (i - 1) * nodesx + 1
        istop = i * nodesx
        #print np.linspace(xl[i-1],xr[i-1],nodesx)
        #print np.linspace(yl[i-1],yr[i-1],nodesy)
        #print bxy[istart-1:istop,0]
        bxy[istart-1:istop,0] = np.linspace(xl[i-1],xr[i-1],nodesx)
        bxy[istart-1:istop,1] = np.linspace(yl[i-1],yr[i-1],nodesx)
        bxy[istart-1:istop,2] = z  # z coordinates
    ''' 
    print xy
    print xl,xr,yl,yr
    print bxy
    print 1
    '''
    
    ncells = N[1-1] * N[2-1]  # number of total cells
    numtri = 2 * ncells       # number of total trianglers
    tri_count = 1             # count of current item

    if type == 3:
        btri = np.zeros((numtri,3))
    else: 
        btri = np.zeros((ncells,4))
    
    for i in range(1,ncells+1):
        ll = i + np.floor((i-1)/N[1-1])
        lr = ll + 1
        ur = lr + nodesx
        ul = ll + nodesx
        
        if type == 3:
            btri[tri_count,:] = [ll,lr,ur]
            btri[tri_count+1,:] = [ll,ur,ul]
            tri_count = tri_count+2
        else:
            #print btri
            btri[i-1,:] = np.array([ ll, lr, ur, ul])
      
    return bxy,btri
    
"""

if __name__ == '__main__':
    
    xy = np.array([[0.0,1,1,0],[0.0,0,1,1]]).T
    N = [2,3]
    bxy,btri = block(xy,N,type=4)
    
    print bxy
    print btri
    print 1
"""