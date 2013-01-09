#!/usr/bin/env python

"""
This module defines the recorder class
"""
import core.meta.meta_class as metacls
import copy
###=======================  recorde item classes   =======================
class parameter():
    """
    This is the base class of the recorderitem
    """
    __metaclass__ = metacls.metacls_item

    def __init__(self,var):
        self.var = var
        self.key_update = False  # False as no update and True as update
        
        
        self.v_current = var
        self.v_update = 0.0
        self.v_history = []

    
    def try_update(self,tolerance=1e-6,hist=''):
        """
        Deterimine if need to update based on the v_update and v_current
        And commite update history to the v_history
        """
        if abs(self.v_current - self.v_update) > tolerance:
            # to be updated
            self.key_update = True  # should be updated
            self.v_history.append([self.v_current,hist])  # commit history
            
            self.v_current = self.v_update  # update value
        else:
            pass
        

