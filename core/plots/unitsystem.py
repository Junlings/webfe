#!/usr/bin/env python
""" This is the module define the units and their operations """
import unittest
import pickle
from units import *


class unitsystem():
    """ define unit systems with basic unit specified
    """
    def __init__(self,system='SI'):
        self.unitlib = {}
        self.system = 'SI'
    
    def add(self,unitinst):
        ''' add derived units '''
        if isinstance(unitinst,unit):
            if unitinst.name not in self.unitlib.keys():
                self.unitlib[unitinst.name] = unitinst
            else:
                raise KeyError,('unit already exist',unitinst.name)
        else:
            raise TypeError,'input is not a unit instance'
        
    def get(self,key):
        try:
            return self.unitlib[key]
        except:
            try:
                return self.unitlib[self.alias(key)]
            except:
                raise KeyError, str(key) + ' do not exist'
                            
    def alias(self,name):
        ''' in order to process the alias of certain unit writing'''
        if name == 'in':
            return 'in.'
        else:
            return name
        
        
    def derive(self,name,coeff,dimstr,latex=None,const=0,sys='SI'):

        # create derived units
        pa={}
        coef = float(coeff)
        
        for para in dimstr.split(','):
            [units,power] = para.split(':')
            
            # check if the used derived unit exist in system
            if units in self.unitlib.keys():
                od = self.unitlib[units]
                basis = set(pa.keys()) | set(od.dimensions.keys())
                for d in basis:
                    pa[d] = pa.get(d,0) + (
                            od.dimensions.get(d,0) * float(power))
                            
                coef = coef * (od.coef ** float(power))
            else:
                print "unit'" + units + "'do not exist, create it first"
                raise KeyError        
        
        sd = unit(coef, pa,name=name,latex=latex,const=const,sys=sys)
        self.add(sd)
            
    def convert(self,key1,key2):
        ''' Get conversion factor coeff that key1 * coeff = key2
        fshould be two units with same dimensions
        '''
        if isinstance(key1,unit) and isinstance(key2,unit):  # unit input
            uleft = key1
            uright = key2
        elif isinstance(key1,type('')) and isinstance(key2,type('')): # key input
            uleft = self.get(key1)
            uright = self.get(key2)            
        else:    
            raise TypeError,('Unit conversion need unit or unitlib keys')
            
        return uleft.conversion(uright)

    def multiply(self,key1,key2):
        ''' Get conversion factor coeff that key1 * coeff = key2
        fshould be two units with same dimensions
        '''
        if isinstance(key1,unit) and isinstance(key2,unit):  # unit input
            uleft = key1
            uright = key2
        elif isinstance(key1,type('')) and isinstance(key2,type('')): # key input
            uleft = self.get(key1)
            uright = self.get(key2)            
        else:    
            raise TypeError,('Unit conversion need unit or unitlib keys')
            
        return uleft * uright
       
    def search(self,other):
        ''' search unit with same dimdict'''
        potential = []
        for key in self.unitlib.keys():
            if self.unitlib[key].isequivalent(other):
                potential.append(key)
        return potential
            
    def get_unit_dict(self):
        unitdict = {}
        unitdict['SI'] = {}
        unitdict['US'] = {}
        
        for key in self.unitlib.keys():
            tunit = self.unitlib[key]
            dimrepr = tunit.get_dim()
            name = tunit.name

            
            for syskey in unitdict.keys():
                if syskey in tunit.sys:
                    if dimrepr in list(unitdict[syskey].keys()):
                        unitdict[syskey][dimrepr].append(name)
                    else:
                        unitdict[syskey][dimrepr] = []
                else:
                    pass #print 'Unit system',syskey,'not understand'
        return unitdict
    
    
def create_units():
    '''create SI unit system
    '''
    units = unitsystem()
    units.add(unit(1,{},name='N/A',sys='SI|US'))
    units.add(unit(1,{'L':1},name='m',sys='SI'))
    units.add(unit(1,{'T':1},name='s',sys='SI|US'))
    units.add(unit(1,{'M':1},name='kg',sys='SI'))
    units.derive('cm',0.01,'m:1',sys='SI')
    units.derive('mm',0.001,'m:1',sys='SI')
    units.derive('in.',25.4,'mm:1',sys='US')
    units.derive('in',25.4,'mm:1',sys='US')
    units.derive('Inches',25.4,'mm:1',sys='US')
    units.derive('inches',25.4,'mm:1',sys='US')
    units.derive('ft',12,'in.:1',sys='US')
    units.derive('G',9.8,'m:1,s:-2',sys='SI')
    units.derive('N',1.0,'kg:1,G:1',sys='SI')
    units.derive('kN',1000.0,'N:1',sys='SI')
    units.derive('kip',4.448,'kN:1',sys='US')
    units.derive('Kips',4.448,'kN:1',sys='US')
    units.derive('lbf',0.001,'kip:1',sys='US')
    units.derive('Pa',1,'N:1,m:-2',sys='SI')
    units.derive('MPa',1e6,'Pa:1',sys='SI')
    units.derive('in^2',1,'in.:2',sys='US')
    units.derive('m^2',1,'m:2',sys='SI')
    units.derive('N*mm',1,'N:1,mm:1',latex=r'${\rm{N}} \cdot {\rm{mm}}$',sys='SI')
    units.derive('kN*m',1,'kN:1,m:1',latex=r'${\rm{kN}} \cdot {\rm{m}}$',sys='SI')
    units.derive('kip*in',1,'kip:1,in.:1',latex=r'${\rm{kip}} \cdot {\rm{in}}$',sys='US')
    units.derive('kN/m',1,'kN:1,m:-1',sys='SI')
    units.derive('in^(-1)',1,'in.:-1',sys='US')
    units.derive('in^(-2)',1,'in.:-2',sys='US')
    units.derive('m^(-1)',1,'m:-1',sys='SI')
    units.derive('mm^(-1)',1,'mm:-1',sys='SI')
    units.derive('kN/mm',1,'kN:1,mm:-1',sys='SI')
    units.derive('ksi',1,'kip:1,in.:-2',sys='US')
    units.derive('psi',1,'lbf:1,in.:-2',sys='US')
    units.derive('ksi^0.5',1,'ksi:0.5',latex=r'$\sqrt{\rm{ksi}}$',sys='US')
    units.derive('MPa^0.5',1,'MPa:0.5',latex=r'$\sqrt{{\rm{MPa}}}$',sys='SI')
    units.derive('in./in.',1,'m:0,s:0',sys='US')
    units.derive('1/in.',1,'in.:-1',sys='US')
    units.derive('1/m',1,'m:-1',sys='SI')
    units.derive('strain',1,'m:0',sys='US|SI')
    units.derive('ms',1e-6,'strain:0',sys='US|SI')
    units.derive('microstrain',1e-6,'strain:0',sys='US|SI')
    units.derive('Microstrain',1e-6,'strain:0',sys='US|SI')
    

    #f = open('unit.pydat','w')
    #pickle.dump(units,f)
    return units
    
# start unit test
class MyTest(unittest.TestCase):

    def setUp(self):
        ''' Create units used in the test
        '''
        self.units = unitsystem()
        self.units.add(unit(1,{'L':1},name='m'))
        self.units.derive('cm',0.01,'m:1')
        self.units.derive('mm',0.001,'m:1')
        
    def test_add_derive(self):
        pass

    
    def test_convert(self):
        self.assertEqual(self.units.convert('cm','m'),[0.01,0])
if __name__ == '__main__':
    create_units()
    unittest.main()
    
    