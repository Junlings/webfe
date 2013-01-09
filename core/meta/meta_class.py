#!/usr/bin/env python
""" This is defination of the meta-class for all model class"""


import inspect
import numpy as np

def validate_ndarray_float(obj,input):
    ''' Validate input as ndarray type '''
    if isinstance(input,np.ndarray):
        if input.dtype == float:
            return obj
        else:
            try:
                return float(obj)
            except:
                raise ValueError,('Input ' + str(input) + ' should be float array, got',
                              input.dtype)
    else:
        raise ValueError,('Input '+ str(input) + ' should be numpy array, got',
                              type(input))    
    return 1

def validate_ndarray_int(obj,input):
    # Validate input
    if isinstance(input,np.ndarray):
        if input.dtype == int:
            return obj
        else:
            raise ValueError,('Input ' + str(input) + ' should be int array, got',
                              input.dtype)
    else:
        raise ValueError,('Input '+ str(input) + ' should be numpy array, got',
                              type(input))    
    return 1

def validate_ndarray_size(obj,input,demsize):
    ''' check if the size of ndarray obj is the same size as demsize, (tulple)
    '''
    if isinstance(input,np.ndarray):
        if input.sizw == demsize:
            return 1
        else:
            raise ValueError,('Input ' + obj.__str__+
                              ' do not match designated size as', demsize)
    else:
        raise ValueError,('Input '+ obj.__str__ + ' should be numpy array, got',
                              type(input))         
            
    

def validate_int(obj,input):
    # Validate input
    if not isinstance(input,type(1)):
        try:
            return int(obj)
        except:
            raise ValueError,('Input ' + obj.__str__ + ' should be integral, got',
                              type(input))
    else:
        return input

def validate_float(obj,input):
    # Validate input
    if not isinstance(input,type(1.00)):
        try:
            return float(input)
        except:
            raise ValueError,('Input ',input, ' should be float, got', type(input))
    else:
        return input


def unfold(obj,paralib):
    for key,value in paralib.items():
        if key in obj.__dict__:
            obj.__setattr__(key,value)
        else:
            raise KeyError,('class',obj,'do not have property:', key)


def get(obj,prop):
    ''' get obj property '''
    if prop in obj.__dict__:
        return obj.__getattribute__(prop)
    else:
        raise KeyError,('class',obj,'do not have property:', prop)
     

''' Start to define metaclass '''

# a metaclass
class Registry(type):
    # store all the types we know
    registered = {}
    def __new__(cls, name, bases, attrs):
        # create the new type
        newtype = super(Registry, cls).__new__(cls, name, bases, attrs)
        # store it
        cls.registered[name] = newtype
        return newtype

    @classmethod
    def class_by_name(cls, name):
        # get a class from the registerd classes
        return cls.registered[name]

class metacls_item(type):
    registered = {}
    def __new__(meta, classname, supers, classdict):
        #print ('In MetaOne.new:', classname, supers, classdict)
        classdict['isfloatarray'] = validate_ndarray_float
        classdict['isintarray'] = validate_ndarray_int
        classdict['isrightshape'] = validate_ndarray_size
        classdict['isint'] = validate_int
        classdict['isfloat'] = validate_float
        classdict['unfold'] = unfold
        classdict['get'] = get
        
        newtype = type.__new__(meta, classname, supers, classdict)
        meta.registered[classname] = newtype
        
        return newtype
        
    @classmethod
    def class_by_name(cls, name):
        # get a class from the registerd classes
        return cls.registered[name]        
        
        
class metacls_itemlist(metacls_item):
    def __new__(meta, classname, supers, classdict):
        metacls_item.__new__(meta, classname, supers, classdict)

        return type.__new__(meta, classname, supers, classdict)
        
        
