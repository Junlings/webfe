#!/usr/bin/env python
"""this module is to organize the plot data
"""
import unittest
import numpy as np
import unitsystem

UI_CURRENT = unitsystem.create_units()

class unitcoldata():
    ''' Unit column data class
    '''
    def __init__(self,data,unit=None,style='default',label='data'):
        ''' initialize '''    
        if isinstance(data,type(np.array([]))):
            self.data = data
        else:
            self.data = np.array(data)
        
        self.pdata = self.data
        self.unit = unit
        self.style = style       # style for data points
        self.label = label
        
    def reset_pdata(self):
        self.pdata = self.data
    
    def transf(self,scale,shift):
        self.pdata = self.pdata * scale + shift
        return self.pdata
    
    def unit_convert(self,targetunit):
        [scale,shift] = UI_CURRENT.convert(self.unit,targetunit)
        self.pdata = self.transf(scale,shift)
        return self.pdata
    
    def __add__(self, other):
        ''' add other unitdata to the current unitdata
        '''
        
        if not isinstance(other,type(self)):
            raise TypeError,('input should be unitcoldata')
        
        try:
            [scale,shift] = UI_CURRENT.convert(self.unit,other.unit)
            
            if self.data.shape != other.data.shape:
                raise TypeError, ('Input data do not have same shape',
                                  self.data.shape,
                                  other.data.shape)
            else:
                data = self.data + (other.data * 1/scale + shift)
                return unitcoldata(data,self.unit)
        
        except TypeError:
            raise TypeError,('Input data do not have same dim',self.unit,other.unit)
         
    def __sub__(self,other):
        ''' use alreay defined _add_ operator to achieve minus
        '''
        return self + (-1.0) * other

    def __rmul__(self, x):
        ''' unit multiply pure number
        '''
        return unitcoldata(self.data * x,self.unit)
        
    def __rdiv__(self, x):
        '''  unit divide pure number
        '''
        return 1/float(x) * self
        
    def __mul__(self, other):
        ''' over ride the operator '*'
            args:
                other: another unitcoldata
            return:
                new unitcoldata instance
        '''
        # get coefficient
        pc = np.multiply(self.data, other.data)
        
        # get target unit
        targetunit = UI_CURRENT.multiply(self.unit,other.unit)
        
        unitname = UI_CURRENT.search(targetunit)
        # search unitlib for unit name
        if len(unitname) > 1:
            return unitcoldata(pc, unitname[0])
        else:
            targetunit.name = self.unit + '*' + other.unit
            UI_CURRENT.add(targetunit)
            return unitcoldata(pc, targetunit.name)
            
    def __coerce__(self, other):
        
        if isinstance(other, unitcoldata): return self, other
        #return self, unitcoldata(other)
        
class MyTest(unittest.TestCase):

    def setUp(self):
        ''' Create unitcoldata test
        '''
        self.data_a = unitcoldata(np.array([1,2,3]),unit='mm')
        self.data_b = unitcoldata([1,2,5],unit='m')
        self.data_apb = unitcoldata([1001,2002,5003],unit='mm')
        self.data_c = unitcoldata([1,2,5,7],unit='s')
        self.data_d = unitcoldata([1,2,5,7],unit='m')
    


if __name__ == '__main__':
    #unittest.main()
    data_a = unitcoldata(np.array([1,2,3]),unit='mm')
    data_b = unitcoldata([1,2,5],unit='m')
    
    data_c = data_a + data_b
    data_d = data_a - data_b
    
    data_e = 2 / data_a
    data_f = data_a *data_b
    print data_c.data
    print data_c.unit
    print data_e.data
    print data_e.unit
    
    print data_f.getPdata()
    print data_f.getPdata('in^2')
    
    print data_f.getPdata('in^2',tshift=[1,-1.55])