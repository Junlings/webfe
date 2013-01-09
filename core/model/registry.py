#!/usr/bin/env python
"""
This is the class to register all predefined class
and provide API for model operations
"""
# import global settings
from core.settings import *
import datetime
# import register class
import core.meta.meta_class as metacls

# import predefined classes
from coordinates import coordinate, coordlist
from connectivity import conn, connlist
from material import *  # import material lib
from section import *   # import section lib
from bond import boundary
from orient import orient
from itemset import itemset
from parameter import parameter
from property import property
from loadcases import loadcases
from recorder import *
from jobs import jobs
from nodalties import *
# import utilities
import numpy as np

# import export facility
import core.export.export as exporter

from core.imports.marc.import_marc_dat import importfile_marc_dat
from core.lib.libop import loadbyfile, savebyfile

class table():
    def __init__(self,datapoints=[],varnum=1,vartype=[]):
        self.varnum = varnum
        self.datapoints = datapoints
        self.vartype = vartype
        


class model():
    """ This is the model class serves as API for object operations """
    def __init__(self,settings):
        self.settings = settings
        self.nodelist = coordlist()
        self.connlist = connlist()
        self.matlist = {}
        self.seclist = {}
        self.bondlist = {}
        self.loadlist = {}
        self.displist = {}
        self.setlist = {}
        self.orientlist = {}
        self.paralist = {}
        self.reclist = {}
        self.proplist = {}
        self.loadcaselist = {}
        self.joblist = {}
        self.tablelist = {}
        self.nodaltielist = {}
        self.rebargrouplist = {}
        
    def generate_libdict(self):
        libdict = {}
        libdict['nodelist'] = self.nodelist.itemlib
        libdict['connlist'] = self.connlist.itemlib
        libdict['matlist'] = self.matlist
        libdict['seclist'] = self.seclist
        libdict['bondlist'] = self.bondlist
        libdict['loadlist'] = self.loadlist
        libdict['displist'] = self.displist
        libdict['setlist'] = self.setlist
        libdict['orientlist'] = self.orientlist
        libdict['setlist'] = self.setlist
        libdict['paralist'] = self.paralist
        libdict['setlist'] = self.setlist
        libdict['reclist'] = self.reclist
        libdict['proplist'] = self.proplist
        libdict['loadcaselist'] = self.loadcaselist
        libdict['joblist'] = self.joblist
        libdict['tablelist'] = self.tablelist
        libdict['nodaltielist'] = self.nodaltielist
        libdict['rebargrouplist'] = self.rebargrouplist
        return libdict


        
        
        
    
    def get_lib(self,libname):
        ''' Get library bu libname '''
        if libname == 'matlist':
            return self.matlist
        elif libname == 'seclist':
            return self.seclist        
        elif libname == 'bondlist':
            return self.bondlist
        elif libname == 'loadlist':
            return self.loadlist
        elif libname == 'displist':
            return self.displist
        elif libname == 'orientlist':
            return self.orientlist
        elif libname == 'setlist':
            return self.setlist
        elif libname == 'paralist':
            return self.paralist
        elif libname == 'proplist':
            return self.proplist
        elif libname == 'loadcaselist':
            return self.loadcaselist
        elif libname == 'joblist':
            return self.joblist
        else:
            raise keyError,('The libname of model', libname,' do not defined')
        
    def get_class(self,clsname):
        ''' Get predefined class by clsname '''
        return metacls.metacls_item.class_by_name(clsname)    
    
    def get_obj(self,libname,itemkey):
        ''' Get specific item in the lib based on libname and key '''
        lib = self.get_lib(libname)
        try:
            return lib[itemkey]
        except KeyError:
            raise KeyError, ('item key', itemkey, 'do not exist in lib',libname)
        
    def get_material(self,matname):
        ''' Get material from last '''
        return self.matlist[matname]
        
    def get_material_by_section(self,secname):
        
        sec = self.seclist[secname]
        matlib = set()
        
        for key,fiber in sec.fiber.items():
            matlib.add(fiber.mattag)
            
        return matlib
            
    def get(self,obj,prop):
        ''' Get property of model instance '''
        return obj.get(prop)
    
    def get_mat_prop(self,matname,prop):
        ''' get material property based on the name and property '''
        return self.get(self.get_material(matname),prop)
    
    # ======================= Start model construction function ==========
    def node(self,list,setname='default'):
        ''' create list of coordinate instance and add to nodelist
            input:
                list --  node location list [[x1,y1,z1],[x2,y2,z2],..,[xn,yn,zn]]
                         if in format of list, will be convert to numpy array
                         the sequence of node will be automatically assigned
                         based on the input sequence from current max sequence 
        '''
        # get current max sequence
        nn = self.nodelist.get_seqmax()
        no = nn
        tempnode = []
        tempnodeseqlist = []
        for item in list:
            nn += 1
            dseq = None
            # convert to the desired numpy array format
            try:
                if len(item) == 3:
                    item = np.array(item,dtype=float)
                elif len(item) == 2:
                    item = np.array([item[0],item[1],0],dtype=float)
    
                elif len(item) == 4:  # node coordinates include the seq at first column
                    dseq = int(item[0])
                    item = np.array([item[1],item[2],item[3]],dtype=float)
                    
    
                else:
                    raise ValueError, "Input coordinates size shall be 2 or 3"
            except:
                raise ValueError,('input node coordinates',item,
                                  'can not convert to numpy float array')
            if dseq == None:
                tempnode.append(coordinate(item,seq=nn))
            else:
                tempnode.append(coordinate(item,seq=dseq))
                
            tempnodeseqlist.append(nn)
            
        if setname not in self.setlist.keys():
            self.nodeset(setname,{'nodelist':tempnodeseqlist})
        else:
            self.setlist[setname].addnode(tempnodeseqlist)
        # add nodes to nodelist
        self.nodelist.addbylist(tempnode)
        return no
    
    def delete_node(self,seqlist):
        self.nodelist.deletebylist(seqlist)
        
        
    def add_node(self,coords,setname=None):
        nn = self.nodelist.get_seqmax()

        try:
            item = np.array(coords,dtype=float)
        except:
            raise ValueError,('input node coordinates',coords,
                                  'can not convert to numpy float array')
        tempnode = coordinate(item,seq=nn+1)
        self.nodelist.add(tempnode)
        if setname != None:
            self.add_to_set(setname,[nn+1],settype='node')
        
        return tempnode
    
    def element(self,elist,setname='default',daterange=None):
        ''' create list of Conn instance and add to connlist
            list --  connectivity information of the elements [[n11,n12,..1n],
                                                               [n21,n22,..2n]]
                    sequence will be automatically added based on the increment
                    from current max seq of elements
        '''
        # get current max seq
        ne = self.connlist.get_seqmax()
        tempelem = []
        tempelemseqlist = []
        for item in elist:
            ne += 1
            # try convert to desired numpy array

            try:
                if daterange == None:
                    item = np.array(item,dtype=int)
                else:
                    item = np.array(item[daterange[0]:daterange[1]],dtype=int)
            except:
                raise ValueError,('input element connectivity',item,
                                  'can not convert to numpy int array')

            tempelem.append(conn(item,seq=ne))
            tempelemseqlist.append(ne)
        # add to connnlist
        self.connlist.addbylist(tempelem)
        if setname not in self.setlist.keys():
            self.elemset(setname,{'elemlist':tempelemseqlist})
        else:
            self.setlist[setname].addelem(tempelemseqlist)
        
        return tempelemseqlist
    
    def add_element(self,item,setname=None):
        ne = self.connlist.get_seqmax()

        # try convert to desired numpy array 
        try:
            item = np.array(item,dtype=int)
        except:
            raise ValueError,('input element connectivity',item,
                                  'can not convert to numpy int array')
        tempelem = conn(item,seq=ne+1)
        
        # add to connnlist
        self.connlist.add(tempelem)
        if setname != None:
            self.add_to_set(setname,[ne+1],settype='element')
                
        return tempelem

    def material(self,matname,matclass,paralib={}):
        ''' add material instance to the matlist.
            inputs:
                matname -- user defined name of material, use as key for matlist
                matclass --  class name of the material, used to retrive class
                paralib -- dict of material properties to create material
        '''
        # retrive class 
        mat = self.get_class(matclass)
        # add material instance to mat list
        self.matlist[matname] = mat(paralib)

    def recorder(self,recordername,recorderclass,paralib={}):
        ''' add material instance to the matlist.
            inputs:
                recordername -- user defined name of recorder, use as key for matlist
                recorderclass --  class name of the recorder, used to retrive class
                paralib -- dict of recorder to create material
        '''
        # retrive class 
        rec = self.get_class(recorderclass)
        # add material instance to mat list
        self.reclist[recordername] = rec(paralib)
        
    def section(self,secname,secclass,paralib):
        ''' add section instance to the seclist.
            inputs:
                secname -- user defined name of section, use as key for seclist
                secclass --  class name of the section, used to retrive class
                paralib -- dict of section properties to create section
        '''
        # retrive class 
        sec = self.get_class(secclass)
        # add material instance to mat list
        
        if type(paralib) == sec:
            self.seclist[secname] = paralib
        else:
            self.seclist[secname] = sec(paralib)
        
    def nodaltie(self,tiename,tieclass,paralib):
        ''' add nodaltie instance to the nodaltielist'''
        nodaltie = self.get_class(tieclass)
        # add material instance to mat list
        ntie = len(self.nodaltielist.keys())
        paralib.update({'tieid':ntie})
        self.nodaltielist[tiename] = nodaltie(paralib)        
        
        
    def orient(self,orientname,orientclass,paralib):
        ''' add section instance to the seclist.
            inputs:
                orientname -- user defined name of orient, use as key
                orientclass --  class name of the orient, used to retrive class
                paralib -- dict of orient properties to create orient
        '''        
        orient = self.get_class(orientclass)
        self.orientlist[orientname] = orient(paralib)
    
    def table(self,tablename,tablevarnum,vartype,datapoints):
        self.tablelist[tablename] = table(varnum=tablevarnum,datapoints=datapoints,vartype=vartype)
    
    def property(self,propname,propclass,paralib):
        ''' add property to the proplist'''
        prop = self.get_class(propclass)
        self.proplist[propname] = prop(paralib)               

    def loadcase(self,loadcasename,loadcaseclass,paralib):
        loadcase = self.get_class(loadcaseclass)

        self.loadcaselist[loadcasename] = loadcase(paralib)

    def job(self,jobname,jobclass,paralib):
        job = self.get_class(jobclass)

        self.joblist[jobname] = job(paralib)    
    '''
    def table(self,tablename,tableclass,paralib):
        tabletype = self.get_class(tableclass)
        self.tablelist[tablename] = tabletype(paralib)   
    ''' 
    def bond(self,bondname,paralib):
        ''' add boundary conditions to bondlist'''
        paralib.update({'type':'bond'})
        bond = boundary(paralib)
        self.bondlist[bondname] = bond

    def load(self,bondname,paralib):
        ''' add point load to the loadlist'''
        paralib.update({'type':'load'})
        bond = boundary(paralib)
        self.loadlist[bondname] = bond
        
    def disp(self,bondname,paralib):
        ''' add displacement to the displist '''
        paralib.update({'type':'disp'})
        bond = boundary(paralib)
        self.displist[bondname] = bond
    
    def parameter(self,varname,prop):
        ''' add parameter to the paralist'''
        lib = self.get_lib(prop['lib'])
        var = lib[prop['obj']].get(prop['prop'])
        self.paralist[varname] = parameter(var)
    

            
    
        
    # start define the set operation==============
    def nodeset(self,setname,paralib):
        ''' create node set '''
        paralib.update({'settype':'node'})
        self.setlist[setname] = itemset(paralib)
        
    def elemset(self,setname,paralib):
        ''' create element set '''
        paralib.update({'settype':'element'})
        self.setlist[setname] = itemset(paralib)
    
    def elemset_sub_setname(self,setname1,setname2):
        ''' create element set by substract setname 1 by setname 2 '''
        newname = setname1 + '-' + setname2
        
        elemlist1 = self.setlist[setname1].elemlist
        elemlist2 = self.setlist[setname2].elemlist
        newelem = [item for item in elemlist1 if item not in elemlist2]

        
        self.setlist[newname] = itemset({'settype':'element','elemlist':newelem})
    
    def entityset(self,setname,paralib=None):
        ''' create set with both nodes and elements
            or node pairs
        '''
        paralib.update({'settype':'both'})
        self.setlist[setname] = itemset(paralib)
    
    def add_to_set(self,setname,itemlist,settype='node'):
        if setname not in self.setlist.keys():
            if settype == 'node':
                self.nodeset(setname,{})
            elif settype == 'element':
                self.elemset(setname,{})
        targetset = self.setlist[setname]
        #temp = []
        #for item in itemlist:
        #    temp.append(item.seq)
        #targetset.add(temp,settype)
        targetset.add(itemlist,settype)
        
    # ===============group of link functions
    
    def link_prop_conn(self,propkey,elemlist=None,setnamelist=None):
        ''' link properties to element list'''
        if elemlist == 'ALL':
            for key in self.connlist.itemlib.keys():
                self.connlist.itemlib[key].property = propkey
            return 1
        
        elif type([1,2,3]) == type(elemlist):
            pass
        else:
            elemlist = []
            
        if setnamelist != None:   # if specify the setname
            for setname in setnamelist:
                elemlist.extend(self.setlist[setname].elemlist)
            # record setnamelist to [roperty]
            self.proplist[propkey].setnamelist.extend(setnamelist)
        
        for item in elemlist:
            self.connlist.itemlib[item].property = propkey
        
        # add to setlist
        self.elemset('prop_'+propkey,{'elemlist':elemlist})
        self.proplist[propkey].setnamelist = ['prop_'+propkey]

        
    def link_mat_prop(self,matkey,propkey):
        self.proplist[propkey].mattag = matkey
        
    def link_sec_prop(self,seckey,propkey):
        self.proplist[propkey].sectag = seckey
        
    def link_orient_prop(self,orientkey,propkey):
        self.proplist[propkey].orienttag = orientkey
        
    # ==============start the check functions
    
    def sweep(self,includenodelist=None,excludenodelist=None):
        overlapnodedict = self.nodelist.check_overlap(include=includenodelist,exclude=excludenodelist)
    
        # update the connectivity
        self.connlist.update_nodeseq(overlapnodedict)
        
        # update the setcontent
        for key in self.setlist.keys():
            
            self.setlist[key].update_nodeseq(overlapnodedict)
        
        self.nodelist.del_nodes(overlapnodedict)
    
    
    
    def check_node_overlap(self):
        ''' find all overlaped node seq sets
            return overlaped node pair in dict format,
            see nodelist.check_overlap() for detail
        '''
        return self.nodelist.check_overlap()
        
    def check_node_unused(self):
        ''' find node in the nodelist but not used in connlist,
            also detect missing nodes from connlist defination
            return [unused,missing]
        
        '''
        return self.connlist.check_compatible(self.nodelist)
    
    def check_element_overlap(self):
        ''' find oberlap elements '''
        return self.connlist.check_overlap()
        
    def pick_node_coord_2d(self,coord):
        seq = list(self.nodelist.select_node_coord(rx=[coord[0],coord[0]],ry=[coord[1],coord[1]]))
        if len(seq) > 1:
            raise ValueError,"More than one node picked" 
        else:
            return seq[0]
            
    def select_nodes_online_2d(self,N1,N2):
        seq = list(self.nodelist.select_node_coord(rx=rx,ry=ry,rz=[0,0]))
        return seq

    def select_elements_nodelist(self,nodelist):
        res = self.connlist.select_nodelist(nodelist)
  
        return res
    
    
    def select_nodes_setname(self,setname):
        if setname in self.setlist.keys():
            nodelist = self.setlist[setname].nodelist
            return nodelist
        else:
            return []

    def select_elements_setname(self,setname):
        if setname in self.setlist.keys():
            elemlist = self.setlist[setname].elemlist
            return elemlist
        else:
            return []
    
    def select_coordinates_setname(self,setname):
        nodelist = self.select_nodes_setname(setname)
        outputdict = {}
        if nodelist != None:
            for node in nodelist:
                outputdict.update({node:self.nodelist.itemlib[node]})
        return outputdict
    
    def select_connectivity_setname(self,setname):
        elemlist = self.select_elements_setname(setname)
        outputdict = {}
        for elem in elemlist:
            outputdict.update(self.connlist[elem])
        return outputdict        
    
    def select_elements_nodeset(self,setname):
        if setname in self.setlist.keys():
            nodelist = self.setlist[setname].nodelist
        res = self.select_elements_nodelist(nodelist)
        return res
    
    def select_nodes_coordlist(self,coordlist,setname=None,err=0.1):
        if setname == None:
            nodelist = None
        else:
            nodelist = self.setlist[setname].nodelist

        seqset = self.nodelist.select_node_coordlist(coordlist,nodelist=nodelist,err=err)
        return seqset
        
        
    
    def select_nodes_coord_setname(self,coord,setname=None,err=0.5):
        if setname == None:
            nodelist = None
        else:
            nodelist = self.setlist[setname].nodelist
        
        seqset = self.nodelist.select_node_coord(rx=[coord[0],coord[0]],ry=[coord[1],coord[1]],rz=[coord[2],coord[2]],nodelist=nodelist,err=err)
        return seqset
    
    def import_marc_dat(self,filename,stylesetting='Extended',logfile=None):
        imp1 = importfile_marc_dat(filename,stylesetting=stylesetting,logfile=logfile)
       
        self = imp1.add_nodes(self)
        self = imp1.add_elements(self)
        #save('model',model1,filename.split('.')[0])
        
        
    def get_db_info(self):
        ''' get the general information of the current model '''
        
        info = {}
        info['modelname'] = self.settings['prjname']
        info['Time Stamp'] = datetime.datetime.now()
        info['Node Number'] = self.nodelist.nnode
        info['Node range'] = self.nodelist.maxmin
        info['Element Number'] = self.connlist.ne
        return info
    
    def modelsavetofile(self,filename):
        savebyfile(self,filename)
        return 1
    
    def modelloadbyfile(self,filename):
        return loadbyfile(filename)
