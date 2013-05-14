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

class stepping():
    def __init__(self):   
        self.scheme = 'fixed'
        self.nstep = 50
        


class loadcases():
    """
    Single conntivity item
    """
    __metaclass__ = metacls.metacls_item

    
    def __init__(self,paralib={}):
        self.boundarylist = []
        self.para = {}
        self.unfold(paralib)        
        
class static(loadcases):   # static fix
    def __init__(self,paralib={}):
        self.boundarylist = []
        self.nstep = paralib['nstep']
        self.ctrlnodeid = paralib['ctrlnodeid']
        self.incr = paralib['incr']
        self.itype = paralib['itype']
        #self.unfold(paralib)

        
class static_arclength(loadcases):
    def __init__(self,paralib={}):
        self.boundarylist = []
        self.para = {}
        self.unfold(paralib)        
        
class buckle(loadcases):
    def __init__(self,paralib={}):
        self.boundarylist = []
        self.para = {}
        self.unfold(paralib)           
        