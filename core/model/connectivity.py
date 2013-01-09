#!/usr/bin/env python
"""
This is the class for elements, property,connlist
"""
import sys
sys.path.append('../..')
import core.meta.meta_class as metacls
import coordinates as coord
import numpy as np
#from FEA.model.facility.intergration import *
       
class conn():
    """
    Single conntivity item
    """
    __metaclass__ = metacls.metacls_item

    
    def __init__(self,nodeseqlist,seq=-1,ndm=3,prop=''):
        self.ndm = 3
        self.property = ''                  # property tag
        self.nodelist = []            # nodelist
        # validate inputs
        self.isint(ndm)
        self.isint(seq)
        self.isintarray(nodeseqlist)
        
        self.ndm = ndm
        self.seq = seq
        self.property = prop
        self.nodelist = nodeseqlist

    def getlist(self):
        return self.nodelist
    
    def getlistlabel(self):
        return self.nodelist
    
        
    def check_overlap(self,other):
        '''
        Check if the element constructued by the same nodes 
        Noticed that different on node sequence will be view as different 
        '''
        if self.nodelist == other.nodelist:
            return True
        else:
            return False
    
    def shift_seq(self,seq_elemshift):
        ''' only shift the seq of the element, node seq do not change'''
        self.seq += seq_elemshift
        
    def update_nodeseq(self,updatelist):
        ''' change the nodelist for element
            input:
                 updatelist --  a dictionary with target node seq as key and
                                replaceable node seq as values
        '''
        for seq in updatelist.keys():      # loop over master seq
            for item in updatelist[seq]:   # loop over slave seq
                ij = np.where(self.nodelist == item) # locate the position
                                                        # of slave seq in list
                self.nodelist[ij] = seq   # replace slave with master
    
    def update_property(self,propseq):
        ''' update the property sequence'''
        self.property = propseq
        
            
class connlist():
    """
    Basic connectivity class
    """
    __metaclass__ = metacls.metacls_itemlist
    
    def __init__(self,conninstancelist=None,ndm=3):
        self.itemlib = {}
        self.ndm = 3
        self.ne = 0
        self.seqlist = []
        self.total_node_seq = set([])
    
        if conninstancelist != None:
            for item in conninstancelist:
                self.add(item)
                
    def copy(self):
        newlist = connlist()
        newlist.itemlib = {}
        newlist.ndm = self.ndm
        return newlist
    
    def addbylist(self,itemlist,update=False):
        seqlist = list
        for item in itemlist:
            self.add(item,update=False)
        self.update()
        
    def add(self,item,update=True):
        ''' add coordinate to the itemlib'''
        if isinstance(item,conn):
            if item.seq not in self.itemlib.keys():
                self.itemlib[item.seq] = item   # sequence based dictionary keys
            else:
                raise KeyError,('The element with sequence:"',item.seq,
                                '" already exist')
        else:
            raise TypeError,('Input to connlist should be list of' +
                             'connectivity instance, got',type(item))
        if update == True:
            # instance update list properties
            self.update()
    
    def update(self):
        self.get_seqlist()
        self.get_elemtable()
        self.get_nodeseq()

    def get_seqlist(self):
        ''' get sequence in list '''
        self.seqlist = np.array(list(self.itemlib.keys()))
        self.ne = len(self.seqlist)
        
    def get_seqmax(self):
        ''' get the max seq in the list'''
        if len(self.seqlist) != 0:
            return max(self.seqlist)
        else:
            return 0

    def get_elemtable(self):
        '''
        Generate element table for 3d display purpose
        '''
        out = []
        for seq in self.seqlist:
            elemi = self.itemlib[seq]
            
            temp = '%s %s ' % (elemi.seq,elemi.nodelist)
            out.append(temp)
        return out
    
    def get_seqelemtable(self):
        '''
        Generate element table for 3d display purpose
        '''
        out = []
        for seq in self.seqlist:
            elemi = self.itemlib[seq]
            
            temp = '%s %s ' % (elemi.seq,elemi.nodelist)
            out.append(temp)
        return out

        # need to thonk about the format the table
        
    def get_nodeseq(self):
        ''' obtain the used node seq set'''
        self.total_node_seq = set([])
        for seq in self.seqlist:
            self.total_node_seq = self.total_node_seq.union(set(self.itemlib[seq].nodelist))

        
    def check_compatible(self,coordlist):
        ''' check if the element list (self) is compatible with coordlist
            input:
                  coordlist -- coordinate list
            output:
                  unused -- unused node seq in coordlist
                  missing -- missing node seqs that in self but not in coordlist
            assume:
                 self.total_node_seq has been upto data by calling
                            self.get_nodeseq before call this funciton
        '''
        unused = set(coordlist.seqlist).difference(
                 set(self.total_node_seq))
        
        missing = set(self.total_node_seq).difference(
                 set(coordlist.seqlist))
        
        return [unused,missing]

               
    # casting operation on single elements by calling conn methods
    def update_property(self,propseq,include=None,exclude=None):
        ''' update the prop of the elements in list
            inputs:
                include -- list of element seqs that should be included,
                           default as all elements
                exclude --  the elements that should be excluded
        '''
        
        apply_seqlist = self.seqlist
        
        #apply include set
        if include != None: apply_seqlist.intersection_update(set(include))
        # apply exclude set
        if exclude != None: apply_seqlist.difference_update(set(exclude))
                    
        for seq in self.apply_seqlist:
            self.itemlib[seq].update_property(propseq)
        
    def sweep(self,include=None,exclude=None):
        '''
        Get rid of all existing overlaping elements
        '''
        elemdict = self.check_overlap(include=include,exclude=exclude)
        
        for seq1 in elemdict.keys():
            for seq2 in elemdict[seq1]:
                del self.itemlib[seq2]
            
        # update list properties
        self.update()
        return elemdict

    def check_overlap(self,include=None,exclude=None):
        ''' Obtain the seq of the elements with same nodelist,
            sequence of nodes counts
            inputs:
                include: the element seq should be included in checking,
                         default as all contained elements
                exclude: the element seq that should be excluded in checking
           output:
               overlap_seq --  dict with first detected overlaping (lowest)
                            element seq as key and rest seq list as value 
        '''
        elemlist = self.seqlist
        overlap_seq = []
        #apply include set
        if include != None: elemlist.intersection_update(set(include))
        # apply exclude set
        if exclude != None: elemlist.difference_update(set(exclude))        
        
        overlap_seq = {}
        while len(elemlist)>0:
            seq1 = elemlist.pop()
            elem1 = self.itemlib[seq1] # base node
            temp = []
            for seq2 in elemlist:
                elem2 = self.itemlib[seq2]
                if elem1.check_overlap(elem2):  # if overlap
                    temp.append(seq2)
                #print seq1,seq2,temp  # for debug purpose
            # record overlap
            if len(temp) > 0:
                for item in temp:
                    elemlist.remove(item)
                overlap_seq[seq1] = temp
        return  overlap_seq
        
    # ===========selection method by coord, node seq, and elem seq
    def select_elem_coord(self,coordlist,rx=None,ry=None,rz=None,
                          mode = 'ALL'):
        ''' select element based on the bounding box and coordlist
            inputs:
                coordlist  -- coordinate instance
                range x    -- [min,max] in x direction
                range y    -- [min,max] in y direction
                range z    -- [min,max] in z direction
                mode       -- selection option, can be ('ALL','ANY')
                              'ALL' for all nodes of element in range, or
                              'ANY  for any nodes of element in range
            outputs:
                out_seqlist -- seq list of the selected elements
                
        '''
        out_seqlist = []
        
        # first call the coordlist function to find included 
        nodeseq_inrange = coordlist.select_node_coord(
                            rx=rx,ry=ry,rz=rz,err=0.00001)
        
        for seq in self.seqlist:
            nodelist = self.itemlib[seq].nodelist
            
            if mode == 'ALL' and set(nodelist).issubset(set(nodeseq_inrange)):
                out_seqlist.append(seq)
            elif mode == 'ANY' and len(set(nodelist).intersection(
                       set(nodeseq_inrange))):
                out_seqlist.append(seq)
            else:
                continue
        return out_seqlist       
    
    def select_node(self,nodeseq):
        '''
        Select the element that contain the node with the input nodeseq
        inputs:
            nodeseqlist -- input target node seq list
        outputs:
            out_seqlist -- list of matching element seq list
        '''
        out_seqlist = []
           
        for seq in self.seqlist:
            
            temp = set(self.itemlib[seq].nodelist).intersection(
                   set([nodeseq]))
            if len(temp) > 0:
                out_seqlist.append(seq)
                
        return out_seqlist
        
    def select_nodelist_old(self,nodelist):
        ''' select element by input nodelist
            inputs:
                nodelist -- list of the input nodes
            output:
                out_seqdict -- dict with target node seq as key and matching
                               element seq as values
            dependency:
                call self.select_node()
        '''
        out_seqdict = {}
        for item in nodelist:
            out_seqdict[item] = self.select_node(item)
        return out_seqdict
            
            
    def select_nodelist(self,nodelist):
        self.update()
        out_seqlist = []
        nodelistset = set(nodelist)
        for seq in self.seqlist:
            
            temp = set(self.itemlib[seq].nodelist).intersection(nodelistset)
            if len(temp) > 0:
                out_seqlist.append(seq)
                
        return out_seqlist
        
            
        
    def select_elem_seq(self,seqlist):
        ''' select element that in the seqlist '''
        pass  # now seq selection is native


    #  == shift function group
    def shift_seq_elem(self,seqshift_elem):
        '''
        Shift the sequence of all elements
        '''
        if elemshift==0:
            return
        else:
            newlib = self.copy()  # copy 

            for seq in self.seqlist:
                item = self.itemlib[seq]
                item.shift_seq(seqshift_elem)
                newlib.add(item,update=False)
            
            # assign to self
            self.itemlib = newlib.itemlib
            
            # update list properties
            self.update() 
        
    def shift_seq_elemnode(self,seqshift_node):
        ''' Make seq shift for all nodes contained in the element
            inputs:
                seqshift_node -- node seq shift
            outputs:
                None  (self update)
                
        '''
        for seq in self.seqlist:
            self.itemlib[seq].nodelist += seqshift_node
        
    def update_nodeseq(self,updatelist):
        for seq in self.seqlist:
            elemi = self.itemlib[seq]
            elemi.update_nodeseq(updatelist)
        
        
if __name__ == '__main__':
    
    n1 = node([1,1,1])
    n2 = node([2,1,1])
    n3 = node([2,1,3])
    '''
    p1 = property('line2',type='nonlinearBeamColumn',
                  nIntgp=5,
                  sectag=1,
                  orienttag=1)
    
    p2 = property('line2_user',type='nonlinearBeamColumn',
                  nIntgp=5,
                  intType='Labotto',
                  sectaglist=[1,2,3,4,5],
                  orienttag='orient1')
    
    print p1.export('OpenSees')
    print p2.export('OpenSees')
    e1 = conn(n1,n2,property=p2)
    e2 = conn(n2,n3,property=p2)
    e3 = conn(n1,n2,property=p2)
    
    e4 = e3.copy()
    e4.nodelist=[0,0]
    
    
    print e1.export('OpenSees')
    print e1.check_overlap(e2)
    print e1['nodelist']
    print e2['nodelist']
    #e1.seq_shift(10,20)
    #print e1['nodelist']
    
    elist = connlist()
    elist.add([e1,e2,e3])
    elist.sweep()
    print elist['connlist']
    
    print elist.select_elem_node(1)['connlist']
    print elist.select_elem_seq(1)['connlist']
    elist.seq_shift(10,20)  #shift the element and node sequence
    print elist['connlist']
    
    
    print elist.get_elemtable()
    
    print elist.export()
    print elist.export('OpenSees')
    '''
    #print 1
    p1 = property('rigidLink', type='beam')
    e2 = conn(1,2,property=p1)
    
    #print 1