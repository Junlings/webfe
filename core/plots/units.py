#!/usr/bin/env python
""" This is the module define the units and their operations """
import unittest

try:
    set
except NameError:
    from sets import Set as set # for python 2.3 compatible...

# define the unit constants


class unit():
    ''' class define the single unit
    '''
    
    def __init__(self, coef, dimensions,name='',latex=None,const=0,sys='SI'):
        ''' Define single unit.
            args:
                coef: values
                dimensions: string for dimensions dict of {'L':1,'T':1,
                                                           'M':1,'C':1}
        '''
        # check if dimension sis dict or string
        if isinstance(dimensions,dict):
            self.dimensions = dimensions
        else:
            raise TypeError,'dimensions should be dict'
            
        self.coef = coef
        self.const = const
        self.name = name
        self.latex = latex
        self.sys = sys
        
    def setName(self,name):
        self.name = name
        
    def setLatex(self,latex):
        self.latex = latex

    
    def isunit(self,other):
        ''' check if the input is unit instance
        '''
        if isinstance(other,unit):
            return True
        else:
            return False
    
    def issamedim(self,other):
        ''' check if the dimension of self is the same as other
        '''
        sd, od = self.dimensions, other.dimensions
        for key in ['T','C','L','M']:
            if sd.get(key,0) != od.get(key,0): # get vakue-key default as 0.
                return False
        return True
            
    def isequivalent(self,other):
        ''' check if the unit is equivalent to other
        '''
        if self.issamedim(other) and (
           self.coef == other.coef and self.const == other.const):
                return True
        else:
            return False
            
            
    
    def conversion(self,other):
        ''' get the conversion factor that self/other = factor
        '''
        if not self.issamedim(other):
            raise TypeError,("dimension do not match, conversion failed between'",self.name,"'and'",other.name)           
        else:
            return [float(self.coef) / float(other.coef),
                    float(self.const) - float(other.const)]
    
    def __add__(self, other):
        ''' override the operator '+'.
            args:
                other: unit instance
        '''
        # check type of other unit 
        if not self.isunit(other):
            raise TypeError, ('not unit instance', self, other)
        
        # check the dimension compatibility
        if not self.issamedim(other):
            raise TypeError, ('Dimension mismatch', self, other)
            
        # return unit instance
        return unit(self.coef + other.coef, self.dimensions)
    
    def __sub__(self,other):
        ''' use alreay defined _add_ operator to achieve minus
        '''
        return self + (-1.0) * other

    def __rmul__(self, x):
        ''' unit multiply pure number
        '''
        return x * self

    def __rdiv__(self, x):
        '''  unit divide pure number
        '''
        return x / self

    def __mul__(self, other):
        ''' over ride the operator '*'
            args:
                other: another unit
            return:
                new unit instance
        '''
        # get coefficient
        pc = self.coef * other.coef
        # get dimensions
        sd, od = self.dimensions, other.dimensions
        basis = set(sd.keys()) | set(od.keys())
        pa = [(d, sd.get(d,0)+od.get(d,0)) for d in basis]
        pd = dict([(d,a) for d,a in pa if a != 0])
        return unit(pc, pd)

    def get_repr(self):
        ''' form expressions
        '''
        # get coeff
        a = [repr(self.coef)]
        for d,c in self.dimensions.iteritems():
            s = str(d)
            if c != 1:
                s += '^'+str(c)
                a.append(s)
        return '*'.join(a)

    def get_dim(self):
        ''' form expressions
        '''
        # get coeff
        a = ''
        for d,c in self.dimensions.iteritems():
            s = str(d)
            if c != 1:
                s += '^'+str(c)
            a += '[' + s +']'
        return a
    
    def __div__(self, other):
        ''' define unit division
        '''
        # check type of other unit 
        if not self.isunit(other):
            raise TypeError, ('not unit instance', self, other)
            
        od = other.dimensions
        inv = unit(1.0 / other.coef, dict([(d, -od[d]) for d in od]))
        return self * inv
    
    def __pow__(self, n):
        ''' override pow operation
        '''
        n = n.coef
        #if self.dimensions and type(n) not in (int,long):
        #    raise TypeError, ('exponent must be integer', self,n)
        
        sd = self.dimensions
        return unit(self.coef ** n,dict([(d,sd[d]*n) for d in sd]))
                    

    def __coerce__(self, other):
        
        if isinstance(other, unit): return self, other
        return self, unit(other, {})

    def __float__(self):
        if self.dimensions:
            raise TypeError, ('unit must be dimensionless for float cast', self)
        return float(self.coef)
        
    def __int__(self):
        return int(float(self))
    
    def __eq__(self,other):
        ''' coef and dimensions equal each other means eq in unit
        '''
        if self.coef == other.coef and self.issamedim(other):
            return True
        else:
            return False
    
# define the unitest for unit class
class MyTest(unittest.TestCase):

    def setUp(self):
        ''' Create units used in the test
        '''
        self.a = unit(1,{'M':1,'L':2,'T':0,'C':0},name='a')
        self.b = unit(2,{'M':1,'L':2})
        self.c = unit(3,{'M':1,'L':2})
        self.d = unit(1,{'M':1,'L':3})
        self.e = unit(2,{'M':2,'L':4})
        self.a_m_e = unit(2,{'M':3,'L':6})
        self.a_d_e = unit(0.5,{'M':-1,'L':-2})
        
    def test_add(self):
        ''' test unit add and exception
        '''
        self.assertEqual(self.a + self.b,self.c)
        self.assertEqual(self.c - self.b,self.a)
        self.assertRaises(TypeError, self.a.__add__, self.d)
    
    def test_rmul(self):
        self.assertEqual(self.a*3,self.c)
        self.assertEqual(self.c/3,self.a)
    
    def test_mul(self):
        self.assertEqual(self.a * self.e,self.a_m_e)
        self.assertEqual(self.a / self.e,self.a_d_e)
        
    def test_conv(self):
        self.assertEqual(self.a.conversion(self.b),[0.5,0])
        self.assertRaises(TypeError, self.a.conversion,self.e)
    
if __name__ == '__main__':
    unittest.main()
    #unit(1,{'m':1,'L':2})+unit(2,{'m':2,'L':2})
    '''
    meter = unit(1.0, {'m' : 1})
    second = unit(1.0, {'s' : 1})
    kg = unit(1.0, {'kg' : 1})
    coulomb = unit(1.0, {'coulomb' : 1})
    centimeter = meter / 100
    inch = 2.54 * centimeter
    foot = ft = 12 * inch
    mile = 5280*foot
    minute=60*second
    hour=60*minute
    speed_limit = 55 * mile / hour
    furlong = mile / 8
    day = 24 * hour
    fortnight = 14 * day
    # could include more units but you get the idea
    
    c = 186282*mile/second
    print 'speed of light =', c/(furlong/fortnight), 'furlongs per fortnight'
    '''