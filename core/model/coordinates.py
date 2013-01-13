#!/usr/bin/env python
"""
This is the class for coordinates based on the metaclass
"""

import core.meta.meta_class as metacls
import numpy as np
def ALPHA(ax,ay,az):
    Tz = np.array([[np.cos(az), -np.sin(az), 0, 0],
                   [np.sin(az), np.cos(az),  0,0],
                   [0,          0,           1,0],
                   [0,          0,           0,1]
                   ])
    Tx = np.array([[1,          0,           0,0],
                   [0,          np.cos(ax),   -np.sin(ax),0],
                   [0,          np.sin(ax),   np.cos(ax),0],
                   [0,          0,           0,1]])
    
    Ty = np.array([[np.cos(ay),          0,   np.sin(ay),0],
                   [0,                   1,   0,0],
                   [-np.sin(ay),          0,   np.cos(ay),0],
                   [0,          0,           0,1]])
    
    
    return [Tx,Ty,Tz]

def DELTA(dx,dy,dz):
    Td = np.array([[1,          0,   0,dx],
                   [0,          1,   0,dy],
                   [0,          0,   1,dz],
                   [0,          0,   0,1]])
    return Td
    



class coordinate():
    """ Single grid item """
    __metaclass__ = metacls.metacls_item

    def __init__(self,xyz,mass=np.array([0.0]),tag=None,seq=-1):
        '''
        customize initialize deal with the multi-input style
        '''
        # default properties
        self.xyz = np.zeros((3,1),dtype=float)   # coordinates
        self.dxyz = np.zeros((3,1),dtype=float)  # updated coordinates
        self.disp = np.zeros((6,1),dtype=float)  # displacement
        self.mass = np.zeros((1,1),dtype=float)  # point mass
        self.bound = False                       # applied boundary
        self.boundarray = np.zeros((6,1),dtype=float) # boundary arraies
        self.seq = -1                            # internal seq
        self.tag = None                          # node tag
        # Validate xyz
        self.isfloatarray(xyz)
        # validate mass
        self.isfloatarray(mass)
        # validate seq
        self.isint(seq)
        
        
        self.xyz = xyz    # xyz need to be np.array(dtype=float)
        self.mass = mass
        self.tag = tag
        self.seq = seq
            

    def getlist(self):
        return ['%.3f' % self.xyz[0],'%.3f' % self.xyz[1],'%.3f' %self.xyz[2]] 
    
    def getlistlabel(self):
        return ['x','y','z']
    
    def update_deform(self,deform):
        ''' update node deformations'''
        # validate inputs
        self.isfloatarray(deform)
        self.isrightshape(deform,(6,1))
        
        # assign new deformation
        self.disp = deform
        self.dxyz = self.xyz + self.disp[:3]  #only translational disp
        
        
    def shift_seq(self,seq_shift):
        ''' shift self.seq '''
        self.seq += seq_shift
        
    def shift_coord(self,shx=0,shy=0,shz=0):
        '''
        shift of node coordinates
        '''
        self.xyz += np.array([shx,shy,shz])
    
        
    def transform(self,rx,ry,rz,dx,dy,dz):
        ''' generic transformation operation
            operation sequence rx,ry,rz,dx,dy,dz
        
        '''
        
        [Tx,Ty,Tz] = ALPHA(rx,ry,rz)
        Td = DELTA(dx,dy,dz)
            
        ox = np.array([self.xyz[0],self.xyz[1],self.xyz[2],1])
        ox = np.dot(Tx,ox)
        #print ox
        ox = np.dot(Ty,ox)
        #print ox
        ox = np.dot(Tz,ox)
        #print ox
        ox = np.dot(Td,ox)
        #print 'Tx',Tx
        #print 'Ty',Ty
        #print 'Tz',Tz
        #print 'Td',Td
        #print ox
        rxyz = ox[0:3]
        
        self.xyz = rxyz
            
    
    def rot_coord(self,rxy=0,ryz=0,rzx=0):
        '''
        rot of node coordinates around[0,0,0]
        Now only ryz implemented
        '''
        if ryz != None:
            x0 = self.xyz[0]
            y0 = self.xyz[1]
            z0 = self.xyz[2]
            xr = x0
            yr = y0*np.cos(ryz)-z0*np.sin(ryz)
            zr = y0*np.sin(ryz)+z0*np.cos(ryz)
            
        self.xyz = np.array([xr,yr,zr])
        
    def cal_dist(self,other):
        ''' calculate coordinate distance'''
        dxyz = math.abs(self - other)
        dist = (dxyz[0]**2+dxyz[1]**2+dxyz[2]**2)**(0.5)
        return dist
        
    def check_overlap(self,other):
        '''
        check if the node is overlap with the other as inputed
        '''
        rangex = [other.xyz[0],other.xyz[0]]
        rangey = [other.xyz[1],other.xyz[1]]
        rangez = [other.xyz[2],other.xyz[2]]
        
        return self.check_range(rangex,rangey,rangez,err=1e-6)
    
    def check_online(self,coord1,coord2, err=0.00001):
        """ check if node is on linear defined by the two end node """
        rx = [max(coord[0],coord[1]),min(coord[0],coord[0])]
        ry = [max(coord[1],coord[1]),min(coord[1],coord[1])]
        rz = [max(coord[2],coord[2]),min(coord[2],coord[2])]
        
        if not self.check_range(rx,ry,rz):
            return -1
        
        else:
            pass
            " here need the implemenation of the point to line segment "


        
    def check_range(self,rangex=None,rangey=None,rangez=None, err=0.00001):
        '''
        Check if a node is within the coordinate range,
        default tolarance range err = 0.00001
        return True for within range, False for otherwise
        '''
        
        if rangex != None:
            res_x = (min(rangex)-err)< self.xyz[0] <(max(rangex)+err)
        else:
            res_x = True
            
        if rangey != None:
            res_y = (min(rangey)-err)< self.xyz[1] <(max(rangey)+err)
        else:
            res_y = True
            
        if rangez != None:
            res_z=(min(rangez)-err)< self.xyz[2] <(max(rangez)+err)
        else:
            res_z = True
        
        return res_x and res_y and res_z
    
    def __add__(self,other):
        ''' define '+' operation ''' 
        if isinstance (other,coordinate):
            return self.xyz + other.xyz
        else:
            raise TypeError, ('The other obj should be coordinate')
        
    def __sub__(self,other):
        ''' define '-' operation '''
        if isinstance (other,coordinate):
            return self.xyz - other.xyz
        else:
            raise TypeError, ('The other obj should be coordinate')
            
    def __str__(self):
        return '%i   %f   %f   %f' % (self.seq,
                                      self.xyz[0],self.xyz[1],self.xyz[2])         
class coordlist():
    """
    Basic coordlist, contains the list of the coordinates
    """
    __metaclass__ = metacls.metacls_itemlist
    

    
    def __init__(self,coordinatelist=None,ndim=3):
        '''
        customization initialize
        '''
        # define constants
        self.SYSTEM_CHOICES = ('cartesian',) 
        self.SYSTEM_in_use = 'cartesian'          # coordinate system
        self.ndim = 3                             # dimensions
        self.itemlib = {}                         # dict of all nodes
        self.seqlist = []                         # list of sequence
        self.nnode = 0                            # number of total node in list
        self.coordtable = []                      # coordinate table
        self.maxmin = [[0,0,0],[0,0,0]]           # range of [maxx,maxy,maxz],
                                             # [minx,miny,minz]
                                         
        if coordinatelist != None:
            for item in coordinatelist:
                self.add(item,update=False)
            # get sequence list
            self.update()
            
        self.isint(ndim)
        self.ndim = ndim
        self.coordbound = {}

    
    def update(self):
        self.get_seqlist()
        self.get_coordtable()
        self.get_maxmin()
    
    def get_seqlist(self):
        ''' get sequence in list '''
        self.seqlist = np.array(list(self.itemlib.keys()))
        self.nnode = len(self.seqlist)
            
    def get_seqmax(self):
        ''' get the max seq in the list'''
        if len(self.seqlist) != 0:
            return max(self.seqlist)
        else:
            return 0
        
    def get_maxmin(self):
        ''' get the range of the list'''
        self.get_coordtable()
        return [[self.coordbound['xmax'],self.coordbound['ymax'],self.coordbound['zmax']],
                [self.coordbound['xmin'],self.coordbound['ymin'],self.coordbound['zmin']]]
                
                
                
                
    
    def get_coordtable(self):
        '''
        Generate the coordinates table for display and export purpose
        '''
        out = np.empty((self.nnode,3))
        ind = 0
        for seq in self.seqlist:
            out[ind,:] = self.itemlib[seq].xyz
            ind += 1

        self.coordtable = out
        self.coordbound = {}
        self.coordbound['xmax'] = np.amax(out[:,0])
        self.coordbound['xmin'] = np.amin(out[:,0])
        self.coordbound['ymax'] = np.amax(out[:,1])
        self.coordbound['ymin'] = np.amin(out[:,1])
        self.coordbound['zmax'] = np.amin(out[:,2])
        self.coordbound['zmin'] = np.amin(out[:,2])
        

    def get_seqcoordtable(self):
        '''
        Generate the coordinates table for display and export purpose
        '''
        out = []
        ind = 0
        for seq in self.seqlist:
            out.append([seq,self.itemlib[seq].xyz])
        return out
        #self.coordtable = out
        
    def addbylist(self,itemlist,update=False):
        for item in itemlist:
            self.add(item,update=False)
        self.update()
        
    def deletebylist(self,itemseqlist,update=False):
        for item in itemseqlist:
            self.delete(item,update=False)
        self.update()        
        
    def add(self,item,update=True):
        ''' add coordinate to the itemlib'''
        if isinstance(item,coordinate):
            if item.seq not in self.itemlib.keys():
                self.itemlib[item.seq] = item   # sequence based dictionary keys
            else:
                raise KeyError,('The node with sequence:"',item.seq,
                                '" already exist',item.xyz)
        else:
            raise TypeError,('Input to coordlist should be list of' +
                             'coordinate instance, got',type(item))
        if update == True:
            # instance update list properties
            self.update()
            
    def delete(self,itemseq,update=True):
        if itemseq in self.itemlib.keys():    
            del self.itemlib[itemseq]   # sequence based dictionary keys
        else:
            raise KeyError,('The node with sequence:"',itemseq,
                            '" do not exist')

        if update == True:
            # instance update list properties
            self.update()
                    
        
    # ==========introspect methods ( function within list and modify self)
    
    def shift_coord(self,shx=0,shy=0,shz=0):
        ''' Geometry shift '''
        for seq in self.seqlist:
            self.itemlib[seq].shift_coord(shx=shx,shy=shy,shz=shz)
        
        # update the coordtable and ranges
        self.get_coordtable()
        self.get_maxmin()
    
    
    def transform(self,rx=0,ry=0,rz=0,dx=0,dy=0,dz=0):
        for seq in self.seqlist:
            self.itemlib[seq].transform(rx,ry,rz,dx,dy,dz)
        
        # update the coordtable and ranges
        self.get_coordtable()
        self.get_maxmin()
    
    def rot_coord_yz(self,ryz=0):
        ''' Geometry shift '''
        for seq in self.seqlist:
            self.itemlib[seq].rot_coord(rxy=None,ryz=ryz,rzx=None)
        
        # update the coordtable and ranges
        self.get_coordtable()
        self.get_maxmin()


    def shift_seq(self,seqshift):
        '''
        Shift the sequence for all nodes in coordlist
        Not recommended, only useful when merge models
        '''
        if seqshift == 0:
            return
        else:
            newlib = self.copy()  # copy 

            for seq in self.seqlist:
                item = self.itemlib[seq]
                item.shift_seq(seqshift)
                newlib.add(item,update=False)
            
            # assign to self
            self.itemlib = newlib.itemlib
            
            # update list properties
            self.update()
            
    def sweep(self,include=None,exclude=None):
        '''
        Get rid of overlaping nodes
        if overlap == None, searching all existing overlapping nodes
        otherwise, only search within input overlap request
        '''
        nodedict = self.check_overlap(include=include,exclude=exclude)
        self.del_nodes(nodedict)
        
    
    def del_nodes(self,nodedict):
        for seq1 in nodedict.keys():
            for seq2 in nodedict[seq1]:
                del self.itemlib[seq2]
            
        # update list properties
        self.update()
        return nodedict    
    
    # ==============operation on self, do not change self and return other
    def copy(self):
        ''' copy the list with basic setting and empty itemlib'''
        newlist = coordlist()
        newlist.SYSTEM_in_use = self.SYSTEM_in_use
        newlist.ndim = self.ndim
        newlist.itemlib = {}
        return newlist
    
    def select_node_coordlist(self,rxyzlist,err=0.00001,nodelist=None):
        
        if nodelist == None:
            nodelist = self.seqlist        
        

        res = {}

        for seq in nodelist:
            for i in range(0,len(rxyzlist)):
                rxyz = rxyzlist[i]
                rx = [rxyz[0] - err,rxyz[0] + err]
                ry = [rxyz[1] - err,rxyz[1] + err]
                rz = [rxyz[2] - err,rxyz[2] + err]
                
                if self.itemlib[seq].check_range(rx,ry,rz,err=err):
                    if i in res.keys():
                        res[i].append(seq)  # if range check OK, add seq to set
                    else:
                        res[i] = [seq]
                      # no duplicate in coordlist
        return res
    
    
    def select_node_coord(self,rx=None,ry=None,rz=None,err=0.00001,nodelist=None):
        '''
        Generate sub coordlist based on the coordinate ranges
        '''
        res_seq = set([]) # empty set
        if nodelist == None:
            nodelist = self.seqlist
            
        for seq in nodelist:
            if self.itemlib[seq].check_range(rx,ry,rz,err=err):
                res_seq.add(seq)  # if range check OK, add seq to set
        return res_seq

    def select_node_line(self,coord1,coord2,err=0.00001):
        '''
        Generate sub coordlist based on the line defined by the two endnode  '''
        res_seq = set([]) # empty set


        for seq in self.seqlist:
            if self.itemlib[seq].check_range(rx,ry,rz):
                res_seq.add(seq)  # if range check OK, add seq to set
        return res_seq
   
    def update_deform(self,disp):
        '''
        Update the node deformation
        input:
            disp: displacement dictionary with seq as keys
        '''
        for seq in self.seqlist:
            nodei = self.itemlib[seq] 
            nodei.update_deform(disp[seq])

    def check_overlap(self,include=None,exclude=None):
        '''
        Check overlap and generate list of overlaped sequence
        include: the nodes to be included in the searching, defualt,None
                 for all nodes within the list
        exclude: node should be excluded from the overlapping checking.
                 default, None, no nodes should be excluded from the list
        '''
        nodelist = set(self.seqlist) # get sequence list
        
        # apply include set
        if include != None: nodelist.intersection_update(set(include))
        # apply exclude set
        if exclude != None: nodelist.difference_update(set(exclude))
        
        overlap_seq = {}   #overlap sequence
        
        while len(nodelist)>0:
            seq1 = nodelist.pop()
            node1 = self.itemlib[seq1] # base node
            temp = []
            for seq2 in nodelist:
                node2 = self.itemlib[seq2]
                if node1.check_overlap(node2):  # if overlap
                    temp.append(seq2)
                #print seq1,seq2,temp  # for debug purpose
            # record overlap
            if len(temp) > 0:
                for item in temp:
                    nodelist.remove(item)
                overlap_seq[seq1] = temp
        return  overlap_seq


    # ============ retrospect method (function within self and other list)
    def check_contact(self,otherlist):
        '''
        check if the two body is contactable
        '''
        # get ranges for both list
        max1,min1 = self.get_range()
        max2,min2 = otherlist.get_range()
        
        # check overlapping
        return (max1[0]<min2[0] or
                max1[1]<min2[1] or
                max1[2]<min2[2] or
                max2[0]<min1[0] or
                max2[1]<min1[1] or
                max2[2]<min1[2])
    
    def merge(self,otherlist):
        ''' merge two node list together
            no check for overlapping
            the seq of otherlist will be shiffted by max(seq(self) 
        '''
        try:
            seq_self = self.get_seqlist()
            seq_other = otherlist.get_seqlist()
        except:
            raise TypeError,('Extract coordinate list sequence list failed')
        
        # maximum seq of self
        max_seq_self = max(seq_self)
        
        # shift the otherlist
        otherlist.shift_seq(max_seq_self)
        
        # merge the itemlib of otherlist to self
        self.itemlib.update(other.itemlib)
        
        # update the self property list
        self.update()
        
    
    def check_overlaps(self,otherlist,include_self=None,exclude_self=None,
                                     include_other=None,exclude_other=None):
        '''
        Obtain the joint nodelist of self and otherlist
        assumptions: there is no overlaping for each node list set
        operation:  1) 
        '''
        jointlist = {}
        try:
            seq_self = self.get_seqlist()
            seq_other = otherlist.get_seqlist()
        except:
            raise TypeError,('Extract coordinate list sequence list failed')
            
        # apply include set
        if include_self != None: seq_self.intersection_update(set(include_self))
        # apply exclude set
        if exclude_self != None: seq_self.difference_update(set(exclude_self))  
        
        # apply include set
        if include_other != None: seq_other.intersection_update(
                                   set(include_other))
        # apply exclude set
        if exclude_other != None: seq_other.difference_update(
                                   set(exclude_other))
        
        for seqi in seq_self:
            nodei = self.itemlib[seqi]
            templist = []
            for seqj in seq_other:
                nodej = otherlist.itemlib[seqj]
                
                if nodei.check_overlap(nodej):
                    templist.append(seqj)
            if len(templist) >1:
                jointlist[seqi] = templist
        return jointlist

            
if __name__ == '__main__':
    
    
    n1 = coordinate(np.array([1.0,2.0,2.0]),seq=1)
    print n1
    
    n2 = coordinate(np.array([1.0,2.0,3.0]),seq=2)
    print n2
    
    n3 = coordinate(np.array([1.0,2.0,3.0]),seq=3)
    print n3

    n4 = coordinate(np.array([1.0,2.0,3.0]),seq=4)
    print n4
    
    coord1 = coordlist([n1,n2,n3,n4])
    print coord1.coordtable
    print coord1.select_node_coord(rx=[1.0,1.0])
    
    coord1.shift_seq(10)
    print coord1.itemlib
    print coord1.seqlist
    print coord1.coordtable
    
    print coord1.check_overlap(include=[11,12])
    
    coord1.sweep()
    print coord1.coordtable
    
    print 1
