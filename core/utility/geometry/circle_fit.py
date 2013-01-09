from numpy import mean, sum,array,linalg,sqrt

def find_circlecenter(model1,nodelist):
    r1_x = []
    r1_y = []
    r1_z = []
    
    for node in nodelist:
        r1_x.append(model1.nodelist.itemlib[node].xyz[0]) 
        r1_y.append(model1.nodelist.itemlib[node].xyz[1])    
        r1_z.append(model1.nodelist.itemlib[node].xyz[2])
        
    ry,rz,r,rr = circle_fit(r1_y,r1_z)
    
    return [mean(r1_x),ry,rz],r

def circle_fit(x,y):
    '''
    #x = [  9,  35, -13,  10,  23,   0]
    #y = [ 34,  10,   6, -14,  27, -10]
    # == METHOD 1 ==
    #method_1 = 'algebraic'
    '''
    
    # coordinates of the barycenter
    x_m = mean(x)
    y_m = mean(y)
    
    # calculation of the reduced coordinates
    u = x - x_m
    v = y - y_m
    
    # linear system defining the center (uc, vc) in reduced coordinates:
    #    Suu * uc +  Suv * vc = (Suuu + Suvv)/2
    #    Suv * uc +  Svv * vc = (Suuv + Svvv)/2
    Suv  = sum(u*v)
    Suu  = sum(u**2)
    Svv  = sum(v**2)
    Suuv = sum(u**2 * v)
    Suvv = sum(u * v**2)
    Suuu = sum(u**3)
    Svvv = sum(v**3)
    
    # Solving the linear system
    A = array([ [ Suu, Suv ], [Suv, Svv]])
    B = array([ Suuu + Suvv, Svvv + Suuv ])/2.0
    uc, vc = linalg.solve(A, B)
    
    xc_1 = x_m + uc
    yc_1 = y_m + vc
    
    # Calcul des distances au centre (xc_1, yc_1)
    Ri_1     = sqrt((x-xc_1)**2 + (y-yc_1)**2)
    R_1      = mean(Ri_1)
    residu_1 = sum((Ri_1-R_1)**2)
    
    return xc_1,yc_1,R_1,residu_1

if __name__ == '__main__':
    x = [  9,  35, -13,  10,  23,   0]
    y = [ 34,  10,   6, -14,  27, -10]
    
    print circle_fit(x,y)
    