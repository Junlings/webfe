#!/usr/bin/env python
""" This is the module to define material base class and other derived classes
"""
import core.meta.meta_class as metacls

class material():
    __metaclass__ = metacls.metacls_item
    
    def __init__(self,E,mu,mass=0.00):
        
        # input vaidation
        E = self.isfloat(E)
        mu = self.isfloat(mu)
        mass = self.isfloat(mass)
        
        self.E = E
        self.mu = mu
        self.mass = mass        
    
    def __getitem__(self,key):
        return self.__getattribute__(key)
        
class uniaxial(material):
    """ uniaxial material
        The base class will take care of the transformation
    """
    def __init__(self,E,mu,mass=0.0):
        material.__init__(self,E,mu,mass)
    
class uniaxial_elastic(uniaxial):
    
    """ uniaxial elastic material """
    def __init__(self,paralib={'E':0.0,'mu':0.0,'mass':0.0}):
        if type(paralib) == type({}):
            uniaxial.__init__(self,paralib['E'],
                                   paralib['mu'],
                                   paralib['mass'])
        else:
            uniaxial.__init__(self,*paralib)
        self.G = self.E/2/(1+self.mu)
    
class uniaxial_elastic_NT(uniaxial_elastic):
    """ uniaxial elastic material with zero tension """
    def __init__(self,paralib={'E':0.0,'mu':0.0,'mass':0.0}):
        if type(paralib) == type({}):
            uniaxial_elastic.__init__(self,paralib['E'],
                               paralib['mu'],
                               paralib['mass'])
        else:
            uniaxial_elastic.__init__(self,*paralib)
            
class uniaxial_elastic_minmax(uniaxial_elastic):
    def __init__(self,paralib={'E':0.0,'mu':0.0,'mass':0.0,
                               'epsi_ut':0.0,'epsi_uc':0.0}):
        ''' inputs:
                epsi_ut --  ultimate tensile strain
                epsi_uc --  ultimate compressive strain
        '''
        #uniaxial_elastic.__init__(self,{'E':paralib['E'],'mu':paralib['mu'],'mass':paralib['mass']})      
        self.epsi_ut = paralib['epsi_ut']
        self.epsi_uc = paralib['epsi_uc']
        self.baseseq = paralib['baseseq']
    
class uniaxial_elastic_InitStrain(uniaxial_elastic):
    def __init__(self,paralib={'E':0.0,'mu':0.0,'mass':0.0,
                               'epsi_ut':0.0,'epsi_uc':0.0}):
        ''' inputs:
                epsi_ut --  ultimate tensile strain
                epsi_uc --  ultimate compressive strain
        '''
        #uniaxial_elastic.__init__(self,{'E':paralib['E'],'mu':paralib['mu'],'mass':paralib['mass']})      
        self.iepsi = paralib['iepsi']
        self.basetag = paralib['basetag']

    
class uniaxial_EPP(uniaxial):
    """ uniaxial elastic and perfect plastic material """
    
    def __init__(self,paralib={'E':0.0,'mu':0.0,'mass':0.0,
                               'epsi_y':0.0,'epsi_u':0.0}):
        '''
        inputs:
            E -- modulus
            mu -- possison's ratio
            mass -- mass of material
            epsi_y -- yielding strain
            epsi_u -- ulyimate strain
        '''
        uniaxial.__init__(self,paralib['E'],
                               paralib['mu'],
                               paralib['mass'])
        self.epsi_y = paralib['epsi_y']
        self.epsi_u = paralib['epsi_u']


class uniaxial_elastic_plastic(uniaxial):
    """ uniaxial elastic and perfect plastic material
        compatible with plastic material in marc with table driven plastic responses
    """
    
    def __init__(self,paralib={'E':0.0,'mu':0.0,'mass':0.0,'sigma_y':0.0,'tabletag':None}):
        '''
        inputs:
            E -- modulus
            mu -- possison's ratio
            mass -- mass of material
            epsi_y -- yielding strain
            epsi_u -- ulyimate strain
        '''
        uniaxial.__init__(self,paralib['E'],
                               paralib['mu'],
                               paralib['mass'])
        self.sigma_y = float(paralib['sigma_y'])
        self.epsi_y = float(self.sigma_y/self.E)
        self.tabletag = paralib['tabletag']
        
        
class uniaxial_steel_02(uniaxial):
    """ steel02 uniaxial mode defined in OpenSees."""
    def __init__(self,paralib={'E':0.0,'mu':0.0,'mass':0.0,
                               'fy':0.0,'b':0.0,'r0':0.0,
                                'cr1':0.0,'cr2':0.0}):
        uniaxial.__init__(self,paralib['E'],
                               paralib['mu'],
                               paralib['mass'])
        self.fy = paralib['fy']
        self.b = paralib['b']
        self.r0 = paralib['r0']
        self.cr1 = paralib['cr1']
        self.cr2 = paralib['cr2']


class uniaxial_UHPC(uniaxial):
    """ uniaxial UHPC material model with hardneing and softening """
    def __init__(self,paralib={'E':0.0,'mu':0.0,'mass':0.0}):

        uniaxial.__init__(self,paralib['E'],
                               paralib['mu'],
                               paralib['mass'])
        self.sigt0 = paralib['sigt0']
        self.epst0 = paralib['epst0']
        self.sigt1 = paralib['sigt1']
        self.epst1 = paralib['epst1']
        self.sigt2 = paralib['sigt2']
        self.epst2 = paralib['epst2']
        self.epst3 = paralib['epst3']
        self.sigc0 = paralib['epst0']
        self.epsc0 = paralib['epsc0']
        self.sigc1 = paralib['sigc1']
        self.epsc1 = paralib['epsc1']
        self.epsc2 = paralib['epsc2']
        self.alphaT1 = paralib['alphaT1']
        self.alphaT2 = paralib['alphaT2']
        self.alphaT3 = paralib['alphaT3']
        self.alphaC = paralib['alphaC']
        self.alphaC1 = paralib['alphaC1']
        self.alphaCU = paralib['alphaCU']
        self.betaT = paralib['betaT']
        self.betaC = paralib['betaC']
    
class uniaxial_UHPC2(uniaxial):
    """ uniaxial UHPC material model with hardneing and softening """
    def __init__(self,paralib={'E':0.0,'mu':0.0,'mass':0.0}):

        uniaxial.__init__(self,paralib['E'],
                               paralib['mu'],
                               paralib['mass'])
        self.sigt0 = paralib['sigt0']
        self.epst0 = paralib['epst0']
        self.sigt1 = paralib['sigt1']
        self.epst1 = paralib['epst1']
        #self.sigt2 = paralib['sigt2']
        self.epst2 = paralib['epst2']
        #self.epst3 = paralib['epst3']
        self.sigc0 = paralib['sigc0']
        self.epsc0 = paralib['epsc0']
        #self.sigc1 = paralib['sigc1']
        self.epsc1 = paralib['epsc1']
        #self.epsc2 = paralib['epsc2']
        self.alphaT1 = paralib['alphaT1']
        self.alphaT2 = paralib['alphaT2']
        #self.alphaT3 = paralib['alphaT3']
        self.alphaC = paralib['alphaC']
        #self.alphaC1 = paralib['alphaC1']
        self.alphaCU = paralib['alphaCU']
        self.betaT = paralib['betaT']
        self.betaC = paralib['betaC']
        
class interface_marc_builtin(material):
    """ interface model defined in marc """
    def __init__(self,paralib,E=0.0,mu=0.0,mass=0.0):
        
        material.__init__(self,E,mu,mass)
        self.mattype = paralib['mattype']
        self.Gc = paralib['Gc']
        self.vc = paralib['vc']
        
        self.s_n = paralib['s_n']
        self.s_n_c = paralib['s_n_c']
        self.stiff_c = paralib['stiff_c']
        
        if self.mattype == 'linear':
            self.vm = paralib['vm']
        elif self.mattype == 'linearexp':
            self.q = paralib['q']


class lowtension_marc_builtin(uniaxial):
    """ low tension material model defined in marc """
    def __init__(self,paralib={'E':8000.0,'mu':0.3,'mass':0.0,'ft':0.1,'Es':50,'epsilon':0.003,'shear':0.1}):
        
        material.__init__(self,paralib['E'],
                               paralib['mu'],
                               paralib['mass'])
        #self.mattype = paralib['mattype']
        self.ft = paralib['ft']
        self.Es = paralib['Es']
        self.epsilon = paralib['epsilon']
        self.shear = paralib['shear']
            
if __name__ == '__main__':
   pass
