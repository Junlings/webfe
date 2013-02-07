#!/usr/bin/env python
""" This module provide the way to create the coordinates """


def create_single_line_nodecoord(model1,coord_start,coord_end,N,
                                nodesetname=None,
                                elemsetname=None):
    ind = model1.node([coord_start,coord_end])
    
    model1 = create_single_line_nodelist(model1,ind+1,ind+2,N,nodesetname=nodesetname,elemsetname=elemsetname)
    
    return model1



def create_single_line_nodelist(model,coord_start_seq,coord_end_seq,N,
                                nodesetname=None,
                                elemsetname=None):
    """
    this is the function to create 2 node element
    along the straight line and disreitisize by the required numbers
    the node should be already defined.
    N is the total number of the segments
    """
    # get the current node and element seq
    nn = model.nodelist.get_seqmax()
    ne = model.connlist.get_seqmax()
    
    # get the start and end nodes
    coord_start = model.nodelist.itemlib[coord_start_seq]
    coord_end = model.nodelist.itemlib[coord_end_seq]
    
    ## specify the input parameters
    [X_start,Y_start,Z_start] = coord_start.xyz
    [X_end,Y_end,Z_end] = coord_end.xyz
    
    if nodesetname != None:
        model.add_to_set(nodesetname,[coord_start_seq,coord_end_seq],settype='node')
    
    if N == 1:
        ## case of single middle node
        mid_x = (X_start + X_end)/2
        mid_y = (Y_start - Y_end)/2
        mid_z = (Z_start - Z_end)/2
        
        # create new grid instance
        midnode = model.add_node([mid_x,mid_y,mid_z],setname=nodesetname)
        
        # create new element instance
        model.add_element([coord_start.seq,midnode.seq],setname=elemsetname)
        model.add_element([midnode.seq,coord_end.seq],setname=elemsetname)

            
    elif N==0:
        # create elements between the input two nodes
        model.add_element([coord_start.seq,coord_end.seq])
        
    else:
        step_x=((-X_start+X_end))/float(N)
        step_y=((-Y_start+Y_end))/float(N)
        step_z=((-Z_start+Z_end))/float(N)
        
        tempnodelist = []
        tempelementlist = []
        for i in range(1,N):
            tempnodelist.append([i*step_x+X_start,i*step_y+Y_start,i*step_z+Z_start])
            #tempnode = model.add_node(,setname=nodesetname)
        
        id_i = model.node(tempnodelist,setname=nodesetname)
        
        for i in range(1,N):
            if i == 1:
                tempelementlist.append([coord_start.seq,id_i  +i])
            else:
                tempelementlist.append([id_i+ i-1,id_i+i])
                
        tempelementlist.append([id_i+i,coord_end.seq])
        
        
        
        model.element(tempelementlist,setname=elemsetname)
    return model


'''
def create_single_line_nodelist(model,coord_start_seq,coord_end_seq,N,
                                nodesetname=None,
                                elemsetname=None):
    """
    this is the function to create 2 node element
    along the straight line and disreitisize by the required numbers
    the node should be already defined.
    N is the total number of the segments
    """
    # get the current node and element seq
    nn = model.nodelist.get_seqmax()
    ne = model.connlist.get_seqmax()
    
    # get the start and end nodes
    coord_start = model.nodelist.itemlib[coord_start_seq]
    coord_end = model.nodelist.itemlib[coord_end_seq]
    
    ## specify the input parameters
    [X_start,Y_start,Z_start] = coord_start.xyz
    [X_end,Y_end,Z_end] = coord_end.xyz
    
    if nodesetname != None:
        model.add_to_set(nodesetname,[coord_start_seq,coord_end_seq],settype='node')
    
    if N == 1:
        ## case of single middle node
        mid_x = (X_start + X_end)/2
        mid_y = (Y_start - Y_end)/2
        mid_z = (Z_start - Z_end)/2
        
        # create new grid instance
        midnode = model.add_node([mid_x,mid_y,mid_z],setname=nodesetname)
        
        # create new element instance
        model.add_element([coord_start.seq,midnode.seq],setname=elemsetname)
        model.add_element([midnode.seq,coord_end.seq],setname=elemsetname)

            
    elif N==0:
        # create elements between the input two nodes
        model.add_element([coord_start.seq,coord_end.seq])
        
    else:
        step_x=((-X_start+X_end))/float(N)
        step_y=((-Y_start+Y_end))/float(N)
        step_z=((-Z_start+Z_end))/float(N)
        
        tempnodelist = []
        for i in range(1,N):
            tempnode = model.add_node([i*step_x+X_start,i*step_y+Y_start,i*step_z+Z_start],setname=nodesetname)
            #grid.append([i*step_x+X_start,i*step_y+Y_start,i*step_z+Z_start])
            
            if i == 1:
                model.add_element([coord_start.seq,tempnode.seq],setname=elemsetname)
            else:
                model.add_element([tempnode.seq-1,tempnode.seq],setname=elemsetname)
        model.add_element([tempnode.seq,coord_end.seq],setname=elemsetname)
    
    return model
'''

