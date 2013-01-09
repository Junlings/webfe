import math
import numpy  as np

""" calculate the shortest distance between point and line segment"""

def Find_angle(P0,P1,axis='x'):
    if axis == 'x':
        vec=[1,0,0]
    P0 = np.array(P0)
    P1 = np.array(P1)
    vec = np.array(vec)
    uP = (P1-P0)/np.linalg.norm(P1-P0)
    #uPP = (uP-vec)/np.linalg.norm(uP-vec)
    
    return [0,np.arctan(uP[2]/uP[0]),np.arctan(-uP[1]/uP[0])]

def Parameter(P0,P1,rd0,rd1,P,Q):
    ''' Po,P1 as the center for left and right, P is the deepset point, and Q is arbray point
        In order to get
            dist: distance between TP and TQ
            fii : angel between TPP and TQQ
    
    '''
    
    TP,uTPP,Tdent = UdirectionPointLine(P0,P1,P)
    QP,uQPP,Qdent = UdirectionPointLine(P0,P1,Q)
    
    dist = np.linalg.norm(QP-TP)#QP[0] - TP[0]  # distance in x direction
    fii = np.arccos(np.dot(uQPP,uTPP))
    
    rx = rd0 + (rd1 - rd0)/(P1[0]-P0[0])*(Q[0]-P0[0])
    
    return float(dist),float(fii),rx,float(rx-Qdent)
    
    
    
    

def UdirectionPointLine(P0,P1,P):
    P0 = np.array(P0)
    P1 = np.array(P1)
    P = np.array(P)
    V = P1 - P0
    W = P - P0
    
    U = V/np.linalg.norm(V)

    u = np.dot(U,W)/np.dot(U,V)
    TP = P0 + u * V
    
    uTPP = (P-TP)/np.linalg.norm(P-TP)
    return TP,uTPP,np.linalg.norm(P-TP)


#Calc minimum distance from a point and a line segment (i.e. consecutive vertices in a polyline).
def DistancePointLine (P0,P1,P):
    #print P0,p1,P
    P0 = np.array(P0)
    P1 = np.array(P1)
    P = np.array(P)
    
    V = P1 - P0
    W = P - P0
    U = V/np.linalg.norm(V)
    return np.linalg.norm(np.cross(U,W))

    #return U,W,V


if __name__ == '__main__':
    
    P0 = [0,0,0]
    P1 = [2,0,0]
    P = [0,1,1]
    
    print DistancePointLine(P0,P1,P)
    print UdirectionPointLine(P0,P1,P)