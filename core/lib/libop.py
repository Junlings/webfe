#!/usr/bin/env python
""" This is the module provide database operation """
import sys
import os
import cPickle as pickle
import time

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

def save(lib,obj,file):
    '''generate the rsave folder based on the root folder and required lib folder'''
    folder = os.path.join(current_path,lib)
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # create save file
    file = os.path.join(folder,file)
    
    # dump objects
    f1 = open(file,'w')
    t1 = time.time()
    pickle.dump(obj,f1)
    t2 = time.time()
    timelap = t2- t1
    print 'save obj:' + str(obj) + 'success, took:' 
    print timelap ,' second'
    
    f1.close()

def savebyfile(obj,file):
    ''' save to specific file name '''
    f1 = open(file,'w')
    t1 = time.time()
    pickle.dump(obj,f1)
    t2 = time.time()
    timelap = t2- t1
    print 'save obj:' + str(obj) + 'success, took: ' + str(timelap) + ' second'
    
    f1.close()    
    
def load(lib,file):
    ''' load file based on lib and file name'''
    folder = os.path.join(current_path,lib)
    file = os.path.join(folder,file)
    
    f1 = open(file,'r')
    t1 = time.time()
    newobj = pickle.load(f1)
    t2 = time.time()
    timelap = t2- t1
    print 'load obj:' + str(newobj) + 'success, took: ', timelap ,' second'

    return newobj

def loadbyfile(file):
    ''' load file directly '''
    f1 = open(file,'r')
    t1 = time.time()
    newobj = pickle.load(f1)
    t2 = time.time()
    timelap = t2- t1
    print 'load obj:' + str(newobj) + 'success, took:' + str(timelap) + ' second'

    return newobj
