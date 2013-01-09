#!/usr/bin/env python

import core.meta.meta_class as metacls

class boundary():
    """
    Basic class for bondary and load
    """
    __metaclass__ = metacls.metacls_item
    
    def __init__(self,paralib):
        self.type = ''
        self.xyz = [0,0,0,0,0,0]                # restraint indicator
        self.fxyz = [0.0,0.0,0.0,0.0,0.0,0.0]   # designated displacement
        self.DOF = 6                            # Degree of freedom
        self.scalar = 0.0                       # magnitude
        self.nodelist = []                      # add nodelist of node seqs
        self.setnamelist = []
        self.tabletag = None                    # related table tag (mainly for time based inputs)
        self.unfold(paralib)

'''        
class bondlist():
    """
    The boundary container
    """
    __metaclass__ = metacls.metacls_itemlist
    
    def __init__(self,type='bond',bondlist=None):
        self.itemlib = {}
        if type == 'bond' or type == 'load':
            self.type = type
        else:
            raise ValueError,('bond type should be either "bond" or "load"',
                              'got ', type, ' instead')
        
        if bondlist != None:
            for key,value in bondlist.items():
                if isinstance(value,boundary):
                    self.itemlib[key] = value
                else:
                    raise TypeError,('Input to bondlist shoud be bond instance',
                                     'got ', type(value),' instead')
        
    def addbybond(self,bond,coordlist):
        dx,dy,dz,rx,ry,rz = [0,0,0,0,0,0]  # 0 means free
        if 'dx' in bond:
            dx = 1
        if 'dy' in bond:
            dy = 1
        if 'dz' in bond:
            dz = 1
        if 'rx' in bond:
            rx = 1
        if 'ry' in bond:
            ry = 1
        if 'rz' in bond:
            rz = 1
        if 'ALL' in bond:
            dx,dy,dz,rx,ry,rz = [1,1,1,1,1,1]
        if 'Hinge' in bond:
            dx,dy,dz,rx,ry,rz = [1,1,1,0,0,0]
        
        self.nbond += 1
        self.bond[self.nbond] = bond(self.nbond,DOF=[dx,dy,dz,rx,ry,rz])
        self.bond[self.nbond].add_items(coordlist.coord.keys())
        return self.nbond
'''   
        
if __name__ == '__main__':
    bond1 = bond([1,2,3],xyz=[1,1,0,0,0,0],DOF=3)
    bond1.addlist([5])
    bond2 = bond([2,3,4])
    #bond2.nodelist = [7,8,9]
    bond2.addlist([7,8,9])
    
    load1 = bond([1,2,3],xyz=[1,1,0,0,0,0],scalar=1.0,DOF=3)   
    
    
    blist1 = bondlist([bond1,bond2])
    llist1 = loadlist([load1])
    blist1.seq_shift(11,10)
    
    print blist1.export('OpenSees')

    print llist1.export('OpenSees')
    
    print '1'