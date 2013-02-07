#!/usr/bin/env python
"""
This is the class for properties of elements
"""
import sys
sys.path.append('../..')
import core.meta.meta_class as metacls
import connectivity as conn
import numpy as np








class property():
    """
    Basic class for property
    """
    __metaclass__ = metacls.metacls_item
        
    def __init__(self,prop):
        """
        Initialize the property based on the property type
        """
        self.mode = prop['mode']
        self.setnamelist = []
        # new element id property
        #self.element_id = -1
            
    def prop_update(self,prop,propdefault):
        proptemp = {}
        proptemp.update(propdefault)
        proptemp.update(prop)
        return proptemp

class interface_linear(property):

    
    
    def __init__(self,prop):
        prop_interface = {'mode':'interface',
                      'type':'linear',
                      'nIntgp': 3,
                      'mattag': None,
                      'sectag': None,
                      'orienttag': None,
                      'intType': 'Gauss',
                      'nIP' : [],
                      'wIP' : [],
                      'element_id':-1,
                        'setnamelist':[]
                      }
        prop = self.prop_update(prop,prop_interface)
        self.type = prop['type']
        self.mattag = prop['mattag']
        self.element_id = prop['element_id']
        self.setnamelist = prop['setnamelist']



class quad4(property):
    prop_quad4 = {'mode':'quad4',
                  'type':'quad4',
                  'nIntgp': 4,
                  'nIntgpS': 1,
                  'mattag': None,
                  'thinkness':1,
                  'elemtype':'PlainStress',
                  'intType': 'Gauss',
                  'nIP' : [],
                  'wIP' : [],
                  'element_id':-1,  # this is the element interface number, different for different platform 
                  }
    
    def __init__(self,prop):
        
        prop = self.prop_update(prop,self.prop_quad4)
        self.type = prop['type']
        self.nIntgp = prop['nIntgp']
        self.nIntgpS = prop['nIntgpS']
        self.nIP = prop['nIP']
        self.wIP = prop['wIP']
        self.intType = prop['intType']
        self.element_id = prop['element_id']
        self.setnamelist = prop['setnamelist']

class hex8(property):
    prop_hex8 = {'mode':'hex8',
                  'type':'hex8',
                  'nIntgp': 8,
                  'nIntgpS': 1,
                  'mattag': None,
                  'intType': 'Gauss',
                  'nIP' : [],
                  'wIP' : [],
                  'element_id':-1,
                  'setnamelist':[]
                  }
    
    def __init__(self,prop):
        prop = self.prop_update(prop,self.prop_hex8)
        self.type = prop['type']
        self.nIntgp = prop['nIntgp']
        self.nIntgpS = prop['nIntgpS']
        self.nIP = prop['nIP']
        self.wIP = prop['wIP']
        self.mattag = prop['mattag']
        self.intType = prop['intType']
        self.element_id = prop['element_id']
        self.setnamelist = prop['setnamelist']

class line2(property):
    prop_line2 = {'mode':'line2',
                  'type':'dispBeamColumn',
                  'nIntgp': 3,
                  'mattag': None,
                  'sectag': None,
                  'orienttag': None,
                  'intType': 'Gauss',
                  'nIP' : [],
                  'wIP' : [],
                  'element_id':-1,
                    'setnamelist':[]
                  }
    
    def __init__(self,prop):
        prop = self.prop_update(prop,self.prop_line2)
        self.type = prop['type']
        self.nIntgp = prop['nIntgp']
        self.mattag = prop['mattag']
        self.sectag = prop['sectag']
        self.orienttag = prop['orienttag']
        self.nIP = prop['nIP']
        self.wIP = prop['wIP']
        self.intType = prop['intType']
        self.element_id = prop['element_id']
        self.setnamelist = prop['setnamelist']
        
        
class line2_user(line2):
    
    def __init__(self,prop):
        line2.__init__(self,prop)
        
class zerolength(property):
    prop_zerolength = {'mode':'zerolength',
                       'type': 'ALL',
                       'mattaglist':[]}
    
    def __init__(self,prop):
        self.prop_update(prop,prop_zerolength)
        self.type = prop['type']
        self.mattaglist = prop['mattaglist']        
            
class rigidLink(property):
    prop_rigidLink = {'mode':'rigidLink',
                      'type':'beam',
                      'mattaglist':[]}
    
    def __init__(self,prop):
        self.prop_update(prop,prop_rigidLink)
        self.type = prop['type']
        self.mattaglist = prop['mattaglist']  
       



        
    # fillin the intergation locations and weights 
    '''
    def cinit_end(self,*args,**largs):
        if self.mode == 'line2' or self.mode == 'line2_user':
            if self.intType == 'Gauss':
                res = Gauss(self.nIntgp)
                self.nIP = (res[0]+1)/2.0
                self.wIP = res[1]/2.0
            elif self.intType == 'Labotto':
                res = Labotto(self.nIntgp)
                self.nIP = (res[0]+1)/2.0
                self.wIP = res[1]/2.0
            else:
                print 'intergration scheme:' + self.intType +'do not deined'
                raise TypeError         
    '''    