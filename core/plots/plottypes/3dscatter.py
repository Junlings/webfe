import numpy as np
from plotsettings import publish_style
from plot_backbone import plotbackbone, FigureCanvas
from mpl_toolkits.mplot3d import Axes3D

def pscatter3d(X,Y,Z,datalabel=None,type='scatter'):
    plotsetting1 = publish_style()
    del plotsetting1.axislib['x2']
    del plotsetting1.axislib['y2']
    del plotsetting1.axeslib['axes_minor'] 

    # determine the locator for each axis
    plotsetting1.add('locatorlib','x1',mode='auto')
    plotsetting1.add('locatorlib','y1',mode='auto')
        
    #plotsetting1.update('axislib','x1',unit=units[0],locator='x1',label=xylabels[0])#,limits=['auto','auto'],locator='auto')
    #plotsetting1.update('axislib','y1',unit=units[1],locator='y1',label=xylabels[1])#,limits=['auto','auto'],locator='auto') 
    
                     
    # create plot backbone
    pl1 = plotbackbone(plotsetting1)
    
    canvas1 = FigureCanvas(pl1.figure)
    
    #ax = pl1.figure.add_subplot(111, projection='3d')
    ax = Axes3D(pl1.figure)
    
    if type == 'scatter':
        p = ax.scatter(X, Y, Z)
        
    elif type == 'wireframe':
        p = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
        
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')


    
    return pl1.figure

def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin
    
if __name__ == '__main__':

    
    X = np.array([[1,2,3],[4,5,6],[7,8,9]])
    Y = np.array([[1,2,3],[1,2,3],[1,2,6]])
    Z = np.array([[1,2,3],[1,2,3],[1,2,7]])
    
    f = pscatter3d(X, Y, Z)


    f.savefig('aa')
        
    '''
    import matplotlib
    n = 100
    print matplotlib.__version__
    for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
        xs = randrange(n, 23, 32)
        ys = randrange(n, 0, 100)
        zs = randrange(n, zl, zh)
        cs = randrange(n, 0, 100)
    
    p = scatter3d(np.array([xs,ys,zs]),units=['m','m'],xylabels=['x','y'])
    p.savefig('a',dpi=300)
    '''