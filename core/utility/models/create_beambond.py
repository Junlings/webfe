import numpy as np
from utility.fem.create_single_line_nodelist import create_single_line_nodelist
from utility.fem.create_2d_patch import create_2d_patch as add_block

def create_beambond(model1,**args):
    """ create 2d beam strength with FRP model, beam use quad4 and FRP use beam with rectangular section"""  
        
    La = args['La']     # length of part A
    Ha = args['Ha']     # height of part A
    nHa = args['nHa']   # segment number along height A
    nLa = args['nLa']
    
    Le = args['Le']
    He = args['He']
    
    Lb = args['Lb']     # length of part B 
    nLb = args['nLb']

   
    # create corner nodes for part A
    model1.node([[0,0,0],
                 [La,0,0],
                 [La,Ha,0],
                 [0,Ha,0]])
    
    # add corner nodes for part B
    model1.node([[Le,-He,0],
                 [Le+Lb,-He,0]])
    
    model1 = add_block(model1,[1,2,3,4],[nLa,nHa],setname='PartA',z=0)
    model1 = create_single_line_nodelist(model1,5,6,nLb,nodesetname='PartB_Node',elemsetname='PartB_elem')

    # delete the unused nodes
    unused,missing = model1.check_node_unused()
    model1.delete_node(list(unused))
    
    bond_origin = [Le,-He]
    bond_dx = Lb/nLb
    bond_dy = He
    bond_nx = nLb
    temp = create_interface_2d(model1,bond_origin,bond_dx,bond_dy,bond_nx,z=0)
    model1.element(temp,setname='interface')
    return model1    

def onlyoneinset(set):
    
    mylist = list(set)
    
    if len(mylist) != 1:
        raise ValueError
        return None
    else:
        return mylist[0]
        
def create_interface_2d(model1,xy,dx,dy,nx,z=0):
    """ procedure to create interface for model1, start point at xy and do loop of nx,with increment of dx,dy,dz """
    temp = []
    for xx in range(0,nx):
            
        x1 = xy[0] + xx * dx
        y1 = xy[1]
        
        N1 = onlyoneinset(model1.select_nodes_coord_setname([x1,y1,z]))
        N2 = onlyoneinset(model1.select_nodes_coord_setname([x1+dx,y1,z]))
        N3 = onlyoneinset(model1.select_nodes_coord_setname([x1+dx,y1+dy,z]))
        N4 = onlyoneinset(model1.select_nodes_coord_setname([x1,y1+dy,z]))
        
        temp.append([N1,N2,N3,N4])
    return temp


    
"""

if __name__ == '__main__':
    
    xy = np.array([[0.0,1,1,0],[0.0,0,1,1]]).T
    N = [2,3]
    bxy,btri = block(xy,N,type=4)
    
    print bxy
    print btri
    print 1
"""