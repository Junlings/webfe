import numpy as np

def ALPHA(ax,ay,az):
    Tz = np.array([[np.cos(az), -np.sin(az), 0, 0],
                   [np.sin(az), np.cos(az),  0,0],
                   [0,          0,           1,0],
                   [0,          0,           0,1]
                   ])
    Tx = np.array([[1,          0,           0,0],
                   [0,          np.cos(ax),   -np.sin(ax),0],
                   [0,          np.sin(ax),   np.cos(ax),0],
                   [0,          0,           0,1]])
    
    Ty = np.array([[np.cos(ay),          0,   np.sin(ay),0],
                   [0,                   1,   0,0],
                   [-np.sin(ay),          0,   np.cos(ay),0],
                   [0,          0,           0,1]])
    
    
    return [Tx,Ty,Tz]

def DELTA(dx,dy,dz):
    Td = np.array([[1,          0,   0,dx],
                   [0,          1,   0,dy],
                   [0,          0,   1,dz],
                   [0,          0,   0,1]])
    return Td
    

def transform(xyz,rx,ry,rz,dx,dy,dz):
    ''' generic transformation operation
        operation sequence rx,ry,rz,dx,dy,dz
    
    '''
    
    [Tx,Ty,Tz] = ALPHA(rx,ry,rz)
    Td = DELTA(dx,dy,dz)
        
    ox = np.array([xyz[0],xyz[1],xyz[2],1])
    ox = np.dot(Tx,ox)
    #print ox
    ox = np.dot(Ty,ox)
    #print ox
    ox = np.dot(Tz,ox)
    #print ox
    ox = np.dot(Td,ox)
    #print 'Tx',Tx
    #print 'Ty',Ty
    #print 'Tz',Tz
    #print 'Td',Td
    #print ox
    rxyz = ox[0:3]
    
    return rxyz


res = transform([1,0,0],3.1415926,0,0,1,2,3)

print res