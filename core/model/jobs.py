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


class jobs():
    """
    Single conntivity item
    """
    __metaclass__ = metacls.metacls_item

    
    def __init__(self,paralib={}):
        self.loadcaselist = {}
        

class static_job(jobs):
    def __init__(self,paralib={}):
        self.loadcaselist = []
        self.initialcond = []
        self.reqresultslist = []
        self.submit = True
        self.para = {}
        self.unfold(paralib)        
        


class buckle_job(jobs):
    def __init__(self,paralib={}):
        self.loadcaselist = []
        self.initialcond = []
        self.reqresultslist = []
        self.nlevel = 2
        self.nplevel = 2
        self.submit = True
        self.method = 'power'
        self.para = {}
        self.unfold(paralib)        
        