import numpy as np 


def create_cylinderSurface(model1,x0,y0,z0,R1,R2,L,nfi,nL,deepdent=0,setname='surface',dent=False,folder='default'):
    ''' create the cylinder shell surface'''
    # create model instance
    x0 = float(x0)
    y0 = float(y0)
    z0 = float(z0)
    R1 = float(R1)
    R2 = float(R2)
    L = float(L)
    nfi = int(nfi)
    nL = int(nL)
    
    
    r0 = R1
    fi0 = -3.1415926/2.0  # set the start angel as Pi/2 to make sure there is a node on top of circular pole
    dfi = 2 * 3.141592/nfi
    
    dz = float(L)/float(nL)     # get increment of z
    dr = float(R2-R1)/float(nL) # get increment of r
    
    nfi = nfi
    nz = nL

    model1 = create_arcplane(model1,x0,y0,z0,r0,fi0,dfi,dz,dr,nfi,nz,setname=setname)
    
    return model1

def create_arcplane(model,x0,y0,z0,r0,fi0,dfi,dz,dr,nfi,nz,setname='default'):
    """ function to create a arc plane,
        x0: x coordinate of left center
        y0: y coordinate of left center
        z0: x coordinate of left center
        r0: radisu at the left center
        fi0: initial angle at the left center
        dfi: angle increment
        dz: z increment
        dr: radius increment
        nfi: number of angle increment
        nz: number of z increment
    
    """
    nodelist = create_arcplane_node(x0,y0,z0,r0,fi0,dfi,dz,dr,nfi,nz)
    
    no = model.node(nodelist,setname=setname+'_nodes')
    no = no + 1
    model.nodeset(setname+'_leftend',{'nodelist':range(no,nfi)})
    model.nodeset(setname+'_rightend',{'nodelist':range(no + nfi*nz +1,no + nfi*(nz+1))})

    elemlist = []
    for i in range(0,nz):

        for j in range(0,nfi-1):
            N1 = no + j  + i * nfi
            N4 = N1 +  1
            N2 = no + j  + (i+1)*nfi
            N3 = N2 +  1
            
            elemlist.append([N1,N2,N3,N4])
            
        NS1 = no   + i * nfi
        NS2 = no   + (i+1)*nfi        
        elemlist.append([N4,N3,NS2,NS1])
        
    model.element(elemlist,setname=setname+'_elements')
    
    return model

def create_arcplane_node(x0,y0,z0,r0,fi0,dfi,dz,dr,nfi,nz):
    '''create the arc shape plane with variing radius '''
    nodelist = []
    
    for i in range(0,nz+1):
        r = r0 + i * dr
        z = z0 + i * dz
        for j in range(0,nfi):
            
            fi = fi0 + j * dfi
            
            x = x0 + r * np.cos(fi)
            y = y0 - r * np.sin(fi)
            nodelist.append([x,y,z])
            
    return nodelist
    
if __name__ == '__main__':
    
    x0 = 0
    y0 = 0
    z0 = 0
    r0 = 1
    fi0 = 0
    dfi = 2*3.141592/10
    dz = 1
    dr = 0.05
    nfi = 10
    nz = 10
    
    nodelist = create_arcplane(x0,y0,z0,r0,fi0,dfi,dz,dr,nfi,nz)
    print nodelist