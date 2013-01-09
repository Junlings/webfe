#!/usr/bin/env python

"""
This module defines the recorder class
"""
import core.meta.meta_class as metacls

###=======================  recorde item classes   =======================
class recorderitem():
    """
    This is the base class of the recorderitem
    """
    __metaclass__ = metacls.metacls_item

    def __init__(self,header='',unit='',recfile=None,incrrange=None,timerange=None):
        self.header = header
        self.unit = unit
        self.recfile = recfile
        self.incrrange = incrrange
        self.timerange = timerange

    def export(self,target='plain'):
        return self.export_class(target)

def intersection_update(dict1,dict2):
    for key in dict1.keys():
        if key in dict2:
            dict1[key] = dict2[key]
    return dict1

class his_stress_node(recorderitem):
    def __init__(self,para):
        default_para = {'header':'default','unit':'unknown','recfile':None,'incrrange':None,'timerange':None}
        intersection_update(default_para,para)
        recorderitem.__init__(self,**default_para)
        
        self.nodelist = para['nodelist']
        self.DOF = para['DOF']

class his_strain_node(recorderitem):
    def __init__(self,para):
        default_para = {'header':'default','unit':'unknown','recfile':None,'incrrange':None,'timerange':None}
        intersection_update(default_para,para)
        recorderitem.__init__(self,**default_para)
        
        self.nodelist = para['nodelist']
        self.DOF = para['DOF']

        
class his_disp(recorderitem):
    """
    node Scalar recorder class
    """

    def __init__(self,para):
        default_para = {'header':'default','unit':'unknown','recfile':None,'incrrange':None,'timerange':None}
        intersection_update(default_para,para)
        self.DOF = para['DOF'] 
        self.nodelist = para['nodelist']
        if default_para['recfile'] == None:
            self.recfile = 'his_disp'
        else:
            self.recfile = default_para['recfile']
         
class section_fiber(recorderitem):
    def __init__(self,para):
        default_para = {'header':'default','unit':'unknown','recfile':None,'incrrange':None,'timerange':None}
        intersection_update(default_para,para)
        self.sectag = para['sectag'] 
        self.elemid = para['elemid']
        self.locy = para['locy']
        self.locz = para['locz']
        self.mattag = para['mattag']
        if default_para['recfile'] == None:
            self.recfile = 'section_fiber'
        else:
            self.recfile = default_para['recfile']   
    

class his_stress_fiber(recorderitem):
    """
    Recorder item class for fiber in the section
    """       
        
    def __init__(self,para={'header':'default','unit':'unknown','recfile':None,'incrrange':None,'timerange':None}):
        recorderitem.__init__(self,header=para['header'],unit=para['unit'],recfile=para['recfile'],
                              incrrange=para['incrrange'],timerange=para['timerange'])
        self.fiber = para['fiber'] 
        self.elemlist = para['elemlist']
        self.label = para['label'] 
        self.integ = para['integ'] 
    
'''
class recorder():
    __metaclass__ = metacls.metacls_instholder
    
    def cinit(self,*args,**kargs):
        self.defaultlib = 'recorder'
        self.recorder = {}
        updates = {}
        
        if len(args) == 1:
            input =args[0]
            if type(input) == type([1,2,3]):        # list of inputs
                for i in range(0,len(input)):
                    self.add(input[i])
            else:
                self.add(input)
        else:
            pass 
        return updates 
    
    def export(self,target):
        output = ''
        for i in range(1,len(self['recorder'])+1):
            output += self['recorder'][i].export(target)
        return output

    def ini_folder(self,root):
        folder = []
        for i in self['recorder'].keys():
            dir = os.path.split(self.recorder[i])
            folder.append(dir)
        return folder



'''

if __name__ == '__main__':
    rec1 = recorderitem(recfile='1')
    rec2 = item_node_disp([1,2,3],header='ana',unit='kip',recfile='2')
    rec3 = item_fiber(header='ana',unit='kip',recfile='3')
    
    print rec1.export('OpenSees')
    print rec2.export('OpenSees')
    print rec3.export('OpenSees')
    print '1'
