import numpy as np
from utility.fem.create_2d_patch import create_2d_patch as add_block


def create_pullout(model1,La=0,Ha=0,Za=0,Lb=0,Hb=0,Zb=0,Lsize=0,Hsize=0,offset=0,bond_region=None):
    """ create pullout model
    assumpition: 1) Part A at bottom, part B at top (Za<Zb), otherwise will casuse element upside-down error in marc
                 2) the width of part B is equal or smaller than part A
    
    """
    
    para = {'La':La,
            'Ha':Ha,
            'Za':Za,
            'nLa':La/Lsize,
            'nHa':Ha/Hsize,
            'Le':offset*Lsize,
            'Lb':Lb,
            'Hb':Hb,
            'Zb':Zb,
            'nLb':Lb/Lsize,
            'nHb':Hb/Hsize,}
    
    if bond_region == None:
        """ default bond region , all overlap area"""

        para['bond_origin'] = [para['Le'],-para['Hb']/2,para['Za']]
        para['bond_dx'] = Lsize
        para['bond_dy'] = Hsize
        para['bond_nx'] = (La)/Lsize - offset
        para['bond_ny'] = (Hb)/Hsize
        para['bond_Za'] = Za
        para['bond_Zb'] = Zb        
        
    
    
    model1 = create_single_lap_shear_3d(model1,**para)
    
    model1.property('PartA','quad4',{'type':75})
    model1.property('PartB','quad4',{'type':75})
    model1.property('interface','hex8',{'type':188})
    
    model1.link_prop_conn('PartA',setnamelist=['PartA'])
    model1.link_prop_conn('PartB',setnamelist=['PartB'])
    model1.link_prop_conn('interface',setnamelist=['interface'])
    
    return model1

def create_single_lap_shear_3d(model1,**args):
    """ create single lap plane stress/3D model with 8cube interface elements"""
    La = args['La']     # length of part A
    Ha = args['Ha']     # height of part A
    Za = args['Za']     # Z of part A
    nHa = args['nHa']   # segment number along height A
    nLa = args['nLa']
    
    Le = args['Le']
    Lb = args['Lb']     # length of part B 
    Hb = args['Hb']     # height of part B
    Zb = args['Zb']
    nHb = args['nHb']   # segment number along height B
    nLb = args['nLb']
   
    bond_origin = args['bond_origin']
    bond_dx = args['bond_dx']
    bond_dy = args['bond_dy']
    bond_nx = args['bond_nx']
    bond_ny = args['bond_ny']
    bond_Za = args['bond_Za']
    bond_Zb = args['bond_Zb']
   
    # create corner nodes for part A
    model1.node([[0,-Ha/2,Za],
                 [La,-Ha/2,Za],
                 [La,Ha/2,Za],
                 [0,Ha/2,Za]])
    
    # add corner nodes for part B
    model1.node([[Le,-Hb/2,Zb],
                 [Le+Lb,-Hb/2,Zb],
                 [Le+Lb,Hb/2,Zb],
                 [Le,Hb/2,Zb]])
    
    model1 = add_block(model1,[1,2,3,4],[nLa,nHa],setname='PartA',z=Za)
    model1 = add_block(model1,[5,6,7,8],[nLb,nHb],setname='PartB',z=Zb)

    # delete the unused nodes
    unused,missing = model1.check_node_unused()
    model1.delete_node(list(unused))
    
    
    #temp = create_interface_3d(model1,[Le,-Hb/2,Za],2,2,5,5,Za,Zb)
    temp = create_interface_3d(model1,bond_origin,bond_dx,bond_dy,bond_nx,bond_ny,bond_Za,bond_Zb)
    model1.element(temp,setname='interface')
    return model1    


def create_interface_3d(model1,xyz,dx,dy,nx,ny,Za,Zb):
    """ procedure to create interface for model1, start point at xyz and do loop of nx,ny,xz with increment of dx,dy,dz """
    temp = []
    coordlist = []
    for xx in range(0,nx):
        for yy in range(0,ny):
            
            x1 = xyz[0] + xx * dx
            y1 = xyz[1] + yy * dy
            
            coordlist.extend([[x1,y1,Za],
                              [x1+dx,y1,Za],
                              [x1+dx,y1+dy,Za],
                              [x1,y1+dy,Za],
                              [x1,y1,Zb],
                              [x1+dx,y1,Zb],
                              [x1+dx,y1+dy,Zb],
                              [x1,y1+dy,Zb]])
                
            
            '''
            N1 = onlyoneinset(model1.select_nodes_coord_setname([x1,y1,Za]))
            N2 = onlyoneinset(model1.select_nodes_coord_setname([x1+dx,y1,Za]))
            N3 = onlyoneinset(model1.select_nodes_coord_setname([x1+dx,y1+dy,Za]))
            N4 = onlyoneinset(model1.select_nodes_coord_setname([x1,y1+dy,Za]))

            N5 = onlyoneinset(model1.select_nodes_coord_setname([x1,y1,Zb]))
            N6 = onlyoneinset(model1.select_nodes_coord_setname([x1+dx,y1,Zb]))
            N7 = onlyoneinset(model1.select_nodes_coord_setname([x1+dx,y1+dy,Zb]))
            N8 = onlyoneinset(model1.select_nodes_coord_setname([x1,y1+dy,Zb]))
            '''
    
    res = model1.select_nodes_coordlist(coordlist)
    
    for i in range(0,len(coordlist)/8):
        temp.append([res[i*8][0],
                     res[i*8+1][0],
                     res[i*8+2][0],
                     res[i*8+3][0],
                     res[i*8+4][0],
                     res[i*8+5][0],
                     res[i*8+6][0],
                     res[i*8+7][0]])
    
    return temp

def onlyoneinset(set):
    
    mylist = list(set)
    
    if len(mylist) != 1:
        raise ValueError
        return None
    else:
        return mylist[0]
    

def create_single_lap_shear(model1,**args):
    """ create single lap plane stress model with 4quad interface elements"""
    La = args['La']     # length of part A
    Ha = args['Ha']     # height of part A
    nHa = args['nHa']   # segment number along height A

    
    Lb = args['Lb']     # length of part B 
    Hb = args['Hb']     # height of part B
    nHb = args['nHb']   # segment number along height B
    
    L1 = args['L1']     # offset of part A
    He = args['He']     # vertical distance between A and B
    nL = args['nL']     # segment length in the length direction
    
    if 'LL' in args.keys():
        LL = args['LL']  # interface distance to left edge
    else:
        LL = 0
        
    if 'LR' in args.keys():
        LR = args['LR']  # interface distance to left edge    
    else:
        LR = 0
    
    # here need to clear model1 in the future
    
    # create corner nodes for part A
    model1.node([[L1,0,0],
                 [L1 + La,0,0],
                 [L1 + La,Ha,0],
                 [L1,Ha,0]])
    
    # add corner nodes for part B
    model1.node([[0,Ha + He,0],
                 [Lb,Ha + He,0],
                 [Lb,Ha + He + Hb,0],
                 [0,Ha + He + Hb,0]])
    
    # create mesh blocks
    model1 = add_block(model1,[1,2,3,4],[La/nL,Ha/nHa],setname='PartA')
    model1 = add_block(model1,[5,6,7,8],[Lb/nL,Hb/nHb],setname='PartB')
    
    # delete the unused nodes
    unused,missing = model1.check_node_unused()
    model1.delete_node(list(unused))
    
    # start to create the interface
    Ninterface = (Lb - L1 -LL -LR)/nL
    for i in range(0,Ninterface):
        
        coord1 = [L1 + LL + nL*i,Ha,0]
        coord2 = [L1 + LL + nL*(i+1),Ha,0]
        coord3 = [L1 + LL + nL*(i+1),Ha+He,0]
        coord4 = [L1 + LL + nL*i,Ha+He,0]
        
        N1 = model1.pick_node_coord_2d(coord1)
        N2 = model1.pick_node_coord_2d(coord2)
        N3 = model1.pick_node_coord_2d(coord3)
        N4 = model1.pick_node_coord_2d(coord4)
        
        model1.element([[N1,N2,N3,N4]],'interface')
    
    # add special node sets
    #model.select_nodes_coord_2d()
    return model1



def add_block(model,nodeseq,N,type=4,setname='default',z=0):
    ''' mesh the region between the four nodes and merge into the database '''
    
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
    


if __name__ == '__main__':
    
    xy = np.array([[0.0,1,1,0],[0.0,0,1,1]]).T
    N = [2,3]
    bxy,btri = block(xy,N,type=4)
    
    print bxy
    print btri
    print 1
