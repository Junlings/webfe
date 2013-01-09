#!/usr/bin/env python

import core.meta.meta_class as metacls

class orient():
    """
    Basic class for orientation
    """
    __metaclass__ = metacls.metacls_item
    def __init__(self,paralib={}):
        pass

        
class orient_linear(orient):
    def __init__(self,paralib={}):
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        
        self.unfold(paralib)
    