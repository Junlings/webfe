""" This module is used to generate the cyclic increment"""
from __future__ import division
import numpy as np
from math import sin, asin,acos,cos


def gen_sinusoid(T=1,DT=0.01,TT=1.0,N=1,dmax=1,dmin=-1):
    
    iT = np.arange(0,TT+DT,DT)
    ia = iT/T*np.pi*2.0
    ds = np.zeros(ia.shape[0])
    ii = asin((dmax+dmin)/(dmax-dmin))
    ind = 0
    for i in ia:
        ds[ind] = sin(i-ii) *(dmax-dmin)/2.0 + (dmax+dmin)/2.0
        ind += 1
    return iT,ds


def gen_triangle(T=1,DT=0.05,TT=1.0,dmax=1,dmin=-1):
    
    nT = int(T/DT)
    n_max = int(nT/(dmax-dmin)*abs(dmax)/2.0)
    n_min = int(nT/(dmax-dmin)*abs(dmin)/2.0)
    
    peaklist = []
    incrlist = []
    for i in range(0,int(TT/T)):
        peaklist.extend([dmax,dmin,0])
        incrlist.extend([n_max,n_max+n_min,n_min])
        
        
    

    return gen_peakincr(peaklist,incrlist,DT)


def gen_peakincr(peaklist,incrlist,dt):
    iT = []
    ds = []
    cT = 0
    cs = 0
    for i in range(0,len(peaklist)):
        peak = peaklist[i]
        incr = incrlist[i]
        for j in range(0,incr):
            iT.append(cT)
            ds.append(cs) 
            cT += dt
            if i == 0:
                cs += peak/incr
            else:
                cs += (peak -peaklist[i-1])/incr
    #cT += dt
    #cs += (peak -peaklist[i-1])/incr
    iT.append(cT)
    ds.append(cs)     
    return iT,ds 
    

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    it,ds = gen_sinusoid(TT=2.5,DT=0.02,dmax=3,dmin=-2)
    #it,ds = gen_peakincr([1,-1,1,0],[10,20,20,10],0.1)
    #it,ds = gen_triangle(T=1,DT=0.05,TT=5.0,dmax=2,dmin=-1)
    plt.plot(it,ds,'-ro')
    plt.show()
