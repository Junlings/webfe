#!/usr/bin/env python
"""
This is the class for elements
elements include material, geometry and orientation properties and
designated element seq list 

"""

import meta.meta_class as metacls

class element():
    '''element is the property hold for elements and has one-to-one relation
    with conn'''
    __metaclass__ = metacls.metacls_item  

    def __init__(self,ndm,connseq):
        
        self.connseq = connseq
        if self.ndm == 2:
            self.ndfe = 3
            self.ndfb = 3
            
        elif self.ndm == 3:
            self.ndfe = 6
            self.ndfb = 6        
        else:
            raise ValueError,('Dimension of line2 elements should be',
                              'either 2 or 3 got', ndm)
            
class line2(element):
    ''' two node elements '''
    def __init__(self,ndm,connlist):
        element.__init__(self,ndm,connlist)

class beam(line2):    
    ''' two node element with section tag and orientation tag '''
    def __init__(self,paralib={}):
        
        ndm = paralib['ndm']
        connlist = paralib['connlist']
        line2.__init__(self,ndm,connlist)
        self.nIntgp = 3
        self.intType = 'Gauss'
        self.sectag = 'default'        # section tag for the elements (if the same )
        self.orienttag = 'default'   # orientationtag
        self.seclist = {}
        self.unfold(paralib)

class dispBeamColumn(beam):
    ''' beam element with specific integration point locations and
        section instance for each integration point
    '''
    def __init__(self,paralib={}):
        beam.__init__(self,paralib)
        self.build()
        
    def build(self,*args,**kargs):
        # deterimine the location and weight of the integration points
        if self.intType == 'Gauss':
            res = integ.Gauss(self.nIntgp)
            self.nIP = res[0]
            self.wIP = res[1]
        elif self.intType == 'Labotto':
            [self.nIP,self.wIP] = __.integ.Labotto(self.integ)
        else:
            print 'intergration scheme:' + self.intType +'do not deined'
            raise TypeError        
        
        for i in range(0,self.nIntgp):    
            self.seclist[i] = self.sectag
        
        

if __name__ == '__main__':
    import coordinates as coord
    import FEA.__init__ as __
    n1 = coord.coord([1,1,1],seq=1)
    n2 = coord.coord([2,1,1],seq=2)
    n3 = coord.coord([2,1,3],seq=3)

    clist = coord.coordlist([n1,n2,n3])
    
    #by direct build
    sec_Tsec=__.load('sec','sec_Tsec')
    seclist = {1:sec_Tsec}
    
    e2 = beam(n1,n2)

    e1 = displacementBeam(n1,n2,ndm = 3,secseq=1,seq=1,nIntgp=3)
    e3= displacementBeam(n1,n2,ndm = 2,secseq=1,seq=1,nIntgp=3)
    e1.build(clist,seclist)
    for sec in e1.seclist.keys():
        print e1.seclist[sec].position
            