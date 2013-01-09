#!/usr/bin/env python
from __future__ import division

import core.meta.meta_class as metacls
from math import cos, sin

def patch_taper(bb,bt,h,numSubdivh=1,mattag='',starty=0,startz=0):
    ''' patch the taper section
                bt  |
                            h
                bb  |
        --------b---------  |
        numSubdivb:   ,
        numSubdivh,
        starty:
        startz:  middle of the bottom
        
    '''
    fiberlist = []
    dy =  h/numSubdivh
    
    for i in range(0,int(numSubdivh)):
            
        z = startz 
        y = starty + dy * (i+0.5)
        y_top = dy * (i)
        y_bot = dy * (i+1)
        
        w_top = bb + (bt-bb)/h*y_top
        w_bot = bb + (bt-bb)/h*y_top
        
        A = (w_top + w_bot)/2 * dy
    
        tempfiber = fiber(paralib={'locy':y,'locz':z,'area':A,'mattag':mattag})            
        fiberlist.append(tempfiber) 
    return fiberlist    
    

def patch_rectangle(b,h,mattag='',numSubdivb=1,numSubdivh=1,starty=0,startz=0):
    ''' rectangular patch with
    b: width
    h: height
    numSubdivb = segments of b
    numSubdivh = segments of h
    starty = y of the lower left corner
    startz = z of the lower left corner
    '''
    
    fiberlist = []
    dz =  b/numSubdivb
    dy =  h/numSubdivh
    A = dy*dz
    
    for i in range(0,numSubdivb):
        for j in range(0,numSubdivh):
            
            z = startz + (i+0.5) * dz 
            y = starty + (j+0.5) * dy
    
    
            tempfiber = fiber(paralib={'locy':y,'locz':z,'area':A,'mattag':mattag})
            fiberlist.append(tempfiber)    
    return fiberlist

def patch_circ(mattag='',numSubdivCirc=1,numSubdivRad=1,
                 intRad=0,extRad=1,yCenter=0,zCenter=0,startAng=0,endAng=360):
    ''' define the circular patch'''
    
    fiberlist = []
    dfi = (endAng-startAng)/numSubdivCirc
    dr =  (extRad-intRad)/numSubdivRad
    
    for ifi in range(0,numSubdivCirc):
        for ir in range(0,numSubdivRad):
            
            angi = float(startAng +  ifi * dfi)
            angj = float(startAng + (ifi+1) * dfi)
            ri = float(intRad + ir * dr)
            rj = float(intRad + (ir + 1) * dr)
            
            
            ra = (ri + rj) / 2.0
            anga = (angi + angj) / 2.0
            
            y = yCenter + ra * cos(anga/180*3.1415926)
            z = zCenter + ra * sin(anga/180*3.1415926)
            A = 3.1415926 * (rj*rj - ri*ri) /360 * abs((angj-angi))
            
            tempfiber = fiber(paralib={'locy':y,'locz':z,'area':A,'mattag':mattag})
            fiberlist.append(tempfiber)
            
            
    return fiberlist


def layer_circ(mattag='',numBar=1,areaBar=1,yCenter=0,zCenter=0,radius=0,startAng=0,endAng=360):
    fiberlist = []
    dfi = (endAng-startAng)/(numBar-1)
    
    for ifi in range(0,numBar):

        angi = float(startAng +  ifi * dfi)
        #angj = float(startAng + (ifi+1) * dfi)        
        ra = radius
        anga = angi
        
        y = yCenter + ra * cos(anga/180.0*3.1415926)
        z = zCenter + ra * sin(anga/180.0*3.1415926)
        A = areaBar
        tempfiber = fiber(paralib={'locy':y,'locz':z,'area':A,'mattag':mattag})
        fiberlist.append(tempfiber)
                    
    return fiberlist

class section():
    __metaclass__ = metacls.metacls_item
    def __init__(self):
        pass
    
class fiber():
    __metaclass__ = metacls.metacls_item
    
    paralib = {'locy':0.0,
               'locz':0.0,
               'area':0.0,
               'width':0.0,
               'thickness':0.0,
               'mattag':''
               }
    
    def __init__(self,paralib=paralib):
        self.locy = 0.0
        self.locz = 0.0
        self.area = 0.0
        self.width = 0.0
        self.thickness = 0.0
        self.mattag = 'default'
        self.unfold(paralib)
        
class elastic_section(section):
    paralib = {
        'A' : 0.0,
        'Iz': 0.0,
        'Iy': 0.0,
        'J' : 0.0,
        'Sy': 0.0,
        'Sz' :0.0,
        'mattag':None
        }
    
    def __init__(self,paralib=paralib):
        section.__init__(self)
        self.A = 0.0
        self.Iz = 0.0
        self.Iy = 0.0
        self.J = 0.0
        self.Sy = 0.0
        self.Sz = 0.0
        self.mattag = None
        self.unfold(paralib)


class shape_section(section):
    paralib = {
        'shape' : 'rectangular',
        'mattag':None,
        'para':{},
        }
    
    def __init__(self,paralib=paralib):
        section.__init__(self)
        self.shape = 'rectangular'
        self.mattag = None
        self.para = {}
        self.unfold(paralib)
        
        
class layer_section(section):
    """
    Class of layer section
    the structure of initial secdata
    =========list: secdata================
    [0] id [str]
    [1] locy [float]
    [2] locz [float]
    [3] width [float]
    [4] thickness [float]
    [5] material ID [str]
    ======================================
    """
    
    def __init__(self,paralib={}):
        self.nl = 0
        self.position = 0.0
        self.fiber = {}
        self.defaultlib = 'fiber'
        self.d = 4
        self.mattag = None
        
        for fiber,prop in paralib['fiber'].items():
            paralib['fiber'][fiber] = self.create_fiber(prop)
        
        self.unfold(paralib)
     
    
    def create_fiber(self,fiberprop):
        tempfiber = fiber(fiberprop)
        return tempfiber

class shell_section(section):
    def __init__(self,paralib={}):
        self.thickness = 1.0
        self.unfold(paralib)    
        self.mattag = None


class fibersection(section):
    ''' section that can include predefined patch or layer
    '''
    def __init__(self,paralib={}):
        self.patchlib = paralib['patchlib']
        self.layerlib = paralib['layerlib']
        self.fiberlib = paralib['fiberlib']
        self.fiber = {}
        
        if 'fiberlist' in paralib.keys():
            nfiber = 1
            for fiber in paralib['fiberlist']:
                self.fiberlib[nfiber] = fiber    
            
    def collect_fibers(self):
        ''' convert all patch and layer to fibers
            follow the sequence patch--layer--fiber
        '''
        
        # unpack the pacth
        for key in self.patchlib.keys():
            if self.patchlib[key]['type'] == 'circ':
                tempfibers = patch_circ(**self.patchlib[key]['prop'])
            
            elif self.patchlib[key]['type'] == 'rectangle':
                tempfibers = patch_rectangle(**self.patchlib[key]['prop'])
                
            elif self.patchlib[key]['type'] == 'taper_h':
                tempfibers = patch_taper(**self.patchlib[key]['prop'])                
                
            else:
                raise TypeError,('patch type:',self.patchlib[key]['type'],' do not defined')
            
            '''
            if len(list(self.fiberlib.keys())) == 0:
                n = 1
            else:
                n = max(list(self.fiberlib.keys())) + 1
            '''
            n = 1
            for fiber in tempfibers:
                self.fiber[key+'_'+str(n)] = fiber
                n += 1
        
        # unpack the layer
        for key in self.layerlib.keys():
            if self.layerlib[key]['type'] == 'circ':
                tempfibers = layer_circ(**self.layerlib[key]['prop'])
            
            else:
                raise TypeError,('patch type:',self.layerlib[key]['type'],' do not defined')
            
            n = max(list(self.fiberlib.keys())) + 1
            
            for fiber in tempfibers:
                self.fiber[n] = fiber
                n += 1
        # update from fiber lib
        self.fiber.update(self.fiberlib)

    def create_fiber(self,fiberprop):
        tempfiber = fiber(fiberprop)
        return tempfiber
    
    
    
if __name__ == '__main__':
    from FEA.prj.project import *
    
    f1 = fiber(area=1,locy=1,locz=1,tag='bottom',mattag='sc')
    f2 = fiber(area=2,locy=2,locz=1,tag='bottom',mattag='sc')
    f3 = fiber([1,0,1,2,'sc3'])  # four inputs initialize
    f4 = fiber([1,0,0.2,'sc4'])  # three inputs initialize
    
    s1 = layer_section([f1,f2],tag='sec1')
    s2 = layer_section([f1,f2])
    s3 = layer_section([[1,0,1,2,'f1'],[1,0,1,2,'f2']])

    s4 = aggregator_section(mattagVy='uhpc',basetag='sec1')
    
    print s4.export('OpenSees')
    #by direct build
    bf = 12
    tf = 1.25
    bw = 2
    hw = 3.75
    nfl =50
    nw =50
    mat = 'uhpc'
    reinf = [{'loc':'bottom|middle','desig':'us7',
              'cover':(0.5,None),'mat':'MMFX2_minmax'}] 
    secdata = []
    secdata = create_T_section(bf,tf,bw,hw,nfl,nw,mat,reinf)

    sec_Tsec =layer_section(layer=secdata,tag='sec_Tsec')
    sec_Tsec.save('sec','sec_Tsec')
    
    print 1

    