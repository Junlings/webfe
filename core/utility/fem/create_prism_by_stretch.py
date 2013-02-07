""" This is the module to stretch the existing 2d mesh to 3D mesh"""
import numpy as np

def sktretch_2dmesh(model1,incrN,incrD,ElemSetNameList=None,deleteorigin=True,stretchdir = 'z',setname='3d_stretch'):
    ''' This function can stretch 2D mesh into 3D mesh for selected connectivity group in certain direction
        model1: input model instance
        incrN: total increment
        incrD: increment distance in the given direction
        ElemSetNameList: List of the selected element list, default as None for all elements exist in the model
        deleteorigin: if or not to delete the source 2D mesh, default as delete (True)
        stretchdir: Mesh generation direction, default as 'z'
    
    '''
    # get process elem list
    elemkeylist = []
    if ElemSetNameList == None:
        elemkeylist = model1.connlist.itemlib.keys()
    else:
        for key in ElemSetNameList:
            elemkeylist.extend(model1.setlist[key].elemlist)
            
    # get involved nodes
    nodekeylist = model1.select_nodes_elemlist(elemkeylist)
    
    
    # create nodelist based on increment
    new_nodelist = []
    
    if stretchdir == 'z' or stretchdir == 'Z':
        for incr in range(1,incrN+1):
            for key in nodekeylist:
                x = model1.nodelist.itemlib[key].xyz[0]
                y = model1.nodelist.itemlib[key].xyz[1]
                z = model1.nodelist.itemlib[key].xyz[2] + incrD * incr
                
                new_nodelist.append([x,y,z])
        
    else:
        raise TypeError,('stretch direction ',stretchdir, ' not supported')
    new_id = model1.node(new_nodelist,setname='node_'+setname)
    
    
    
    # create 3d elements
    new_elemlist = []
    n_nodelist = len(nodekeylist)
    for incr in range(0,incrN):
        for key in elemkeylist:
            tempnodelist = list(model1.connlist.itemlib[key].nodelist)
            loopnodelist = []
            loopnodelist2 = []
            for nodekey in tempnodelist:
                loopnodelist.append(new_id + 1 + nodekeylist.index(nodekey)+ n_nodelist*(incr))
                loopnodelist2.append(new_id + 1 + nodekeylist.index(nodekey)+ n_nodelist*(incr-1))
            if incr == 0:
                tempnodelist.extend(loopnodelist)       
                new_elemlist.append(np.array(tempnodelist))
                
            else:
                loopnodelist2.extend(loopnodelist)
                new_elemlist.append(np.array(loopnodelist2))
            
    model1.element(new_elemlist,setname='element_'+setname)
    
    # delete the original 2D mesh source if required
    if deleteorigin == True:
    
        model1.delete_elements(elemkeylist)
    
    # return model and generated nodeketlys, new_id and total numbe of node generated
    return model1,nodekeylist,new_id,n_nodelist
    
