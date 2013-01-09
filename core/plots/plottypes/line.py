#from plotsettings import publish_style
from plot_backbone import plotbackbone, FigureCanvas

def single_axis_line(plotdata,units,xylabels,datalabel=None,style=None,legend=True):
    
    if style == None:
        plotsetting1 = publish_style()
    else:
        plotsetting1 = style
    try:
        del plotsetting1.axislib['x2']
        del plotsetting1.axislib['y2']
        del plotsetting1.axeslib['axes_minor']
    except:
        pass

    # determine the locator for each axis
    plotsetting1.add('locatorlib','x1',mode='auto')
    plotsetting1.add('locatorlib','y1',mode='auto')
    
    '''
    if 'x1' not in limits.keys():
        limits['x1'] = ['auto','auto']
    if 'y1' not in limits.keys():
        limits['y1'] = ['auto','auto']        
    '''    
    plotsetting1.update('axislib','x1',unit=units[0],locator='x1',label=xylabels[0])#,limits=limits['x1'])#,locator='auto')
    plotsetting1.update('axislib','y1',unit=units[1],locator='y1',label=xylabels[1])#,limits=limits['y1'])#,locator='auto') 
    
                     
    # create plot backbone
    pl1 = plotbackbone(plotsetting1)
    pl1.addPlot('axes_major',plotdata,datalabel=datalabel,legend=legend)
    
    #pl1.setTextbox('firstbox','axes_major')
    #pl1.setTextbox('secondbox','axes_major')
    #pl1.linkLimits()
    pl1.setLimits('x1')
    pl1.setLimits('y1')
    canvas1 = FigureCanvas(pl1.figure)
    return pl1#.figure


def double_axis_line(plotdata,units,xylabels,style=None):

    # create plotsettings
    plotsetting1 = publish_style()
    
    # determine the locator for each axis
    plotsetting1.add('locatorlib','x1',mode='auto',minor=2)
    plotsetting1.add('locatorlib','y1',mode='auto',minor=2)
    plotsetting1.add('locatorlib','x2',mode='auto')
    plotsetting1.add('locatorlib','y2',mode='auto')
    
    
    plotsetting1.update('axislib','x1',unit=units[0],locator='x1')#,limits=['auto','auto'],locator='auto')
    plotsetting1.update('axislib','y1',unit=units[1],locator='y1')#,limits=['auto','auto'],locator='auto')
    plotsetting1.update('axislib','x2',unit=units[2],locator='x2',limits=['link','x1'])#,limits=['auto','auto'],locator='auto')
    plotsetting1.update('axislib','y2',unit=units[3],locator='y2',limits=['link','y1'])#,limits=['auto','auto'],locator='auto')
    
    
                     
    # create plot backbone
    pl1 = plotbackbone(plotsetting1)
    pl1.addPlot('axes_major',plotdata,datalabel=datalabel)
    

    #pl1.linkLimits()
    
    canvas1 = FigureCanvas(pl1.figure)    
    return pl1.figure