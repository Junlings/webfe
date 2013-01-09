#!/usr/bin/env python
"""
This module can be used to run section analysis with OpenSees,
The moment curvature are the desired output
"""

import meta.meta_class as metacls


class analysis():
    __metaclass__ = metacls. metacls_item
    def __init__(self,paralib={}):
        self.system = 'SparseGeneral'
        self.system_opt = '-piv'
        self.numberer = 'Plain'
        self.constraints = 'Plain'
        self.integrator  =  'DisplacementControl'
        self.integrator_ctl =  -1
        self.integrator_dof =  1
        self.integrator_inc =  1e-8
        self.test =  'EnergyIncr'
        self.test_cri =  1e-012
        self.test_maxincr =  2000
        self.test_disp =  0
        self.algorithm  =  'Newton'
        self.algorithm_opt =  '' #'''-initial'
        self.analysis =  'Static'
        self.run_step = 1
        

        self.unfold(paralib)
    

class ana_section_mc(analysis):
    def __init__(self,paralib={}):
        self.sec_seq = -1
        self.axialLoad = 10
        self.maxK = 0.001
        self.numIncr = 100
        
        self.unfold(paralib)
            

class ana_material(analysis):
    def __init__(self,paralib={}):
        self.mat_seq = -1
        self.mode = ''
        self.strainincr = 0.001
        self.totalstep = 100

        self.unfold(paralib)
