#!/usr/bin/env python
""" This module provide the way to create line elements by the inputed setname """
import numpy as np

def create_single_line_setname(model1,setname,mode='x',ressetname='default_line'):
    ''' create single line based on the input setname, which contains a series of nodes
    that intended to be connected based on the sort coordinates specified by the mode '''
    
    if setname not in model1.setlist.keys():
        raise KeyError, ('Specified node set with name',setname,'do not exist')
    
    if len(model1.setlist[setname].nodelist) == 0:
        raise ValueError, ('Specified node set with name',setname,'contains no nodes')
    
    
    tempdict = []
    
    for node in model1.setlist[setname].nodelist:
        xyz = model1.nodelist.itemlib[node].xyz
        tempdict.append([node,xyz[0],xyz[1],xyz[2]])
    
    tempdict =np.array(tempdict)
    
    if mode == 'x':
        tempdict = tempdict[tempdict[:,1].argsort()]
    elif mode == 'y':
        tempdict = tempdict[tempdict[:,2].argsort()]
    elif mode == 'z':
        tempdict = tempdict[tempdict[:,3].argsort()]
    else:
        raise ValueError, ('Specified mode type',mode,'do not predefined')
    
    tempelem = []
    for i in range(0,tempdict.shape[0]-1):
        tempelem.append([tempdict[i,0],tempdict[i+1,0]])
        
    model1.element(tempelem,setname=ressetname)
        
    return model1



if __name__ == '__main__':
    pass

