#!/usr/bin/env python

"""
plotback bone based on plotdata and plotsetting module 
"""

from unitsystem import create_units  # load unit system
import matplotlib
matplotlib.use('wxagg')               # 
#import plotsettings                  # load default plot settings
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas # for print out
import numpy as np 

class plotbackbone():
    """
    This is the data class to support the GUI and command line ploting work
    """
    def __init__(self,plotsetting): #,plotdata,UI_CURRENT):
        """ plot back bones """
        self.presetting = plotsetting   # predefined plot settings
        self.UI = create_units()        # predefined unit system
        
        # reinitial property libs
        self.axeslib = {}
        self.axislib = {}
        self.fontlib = {}
        self.locatorlib = {}
        self.legendlib = {}
        
        # initialize lib
        self.setFonts()
        self.setLocatorlib()
        self.setFigure()  
        self.setAxes()
        self.setAxis()
        self.setLegends()
        
  
    def setLegends(self):
        ''' set the legendary style '''
        for legendstyle in self.presetting.legendlib.keys():
            prop = self.presetting.legendlib[legendstyle]
            self.legendlib[legendstyle] = prop
                    
    
    # setfontlib
    def setFonts(self):
        ''' add predefined font styles to the font manager '''
        for font in self.presetting.fontlib.keys():
            prop = self.presetting.fontlib[font]
            self.fontlib[font] = matplotlib.font_manager.FontProperties(**prop)
            
            
    def setLocatorlib(self):
        ''' create locator for tick
            Notice that eahc axis should have individual locator
        '''
        
        for key in self.presetting.locatorlib.keys():
            mode = self.presetting.locatorlib[key]['mode']
            prop = self.presetting.locatorlib[key]['prop']
            labels = self.presetting.locatorlib[key]['labels']
            
            if mode == 'auto':
                self.locatorlib[key] = matplotlib.ticker.AutoLocator()
             
            elif mode == 'index':
                self.locatorlib[key] = matplotlib.ticker.IndexLocator(prop[0],prop[1])
                
            elif mode == 'fixed':
                self.locatorlib[key] = matplotlib.ticker.FixedLocator(prop[0],prop[1])
                
            elif mode == 'linear':
                self.locatorlib[key] = matplotlib.ticker.LinearLocator(prop[0]) #,prop[1])            
    
            elif mode == 'multiple':
                self.locatorlib[key] = matplotlib.ticker.MultipleLocator(prop[0]) #,prop[1])            
            
            elif mode == 'maxN':
                self.locatorlib[key] = matplotlib.ticker.MaxNLocator(**prop) #,prop[1])  
            
            elif mode == 'none':
                self.locatorlib[key] = matplotlib.ticker.NullLocator()
                
            elif mode == 'interval':
                pass            
        
            
    def setFigure(self):
        ''' set the basic property for figure'''
        # generate figure
        self.figure = matplotlib.figure.Figure(**self.presetting.figure)
        # set subplot
        self.SubplotParams = matplotlib.figure.SubplotParams(**self.presetting.subplot)
        
    def setAxes(self):
        for key in self.presetting.axeslib:
            if key == 'default':
                continue
                
            axes_dict = self.presetting.axeslib[key]

            self.axeslib[key] = self.figure.add_axes(axes_dict['loc'],
                                            polar=axes_dict['polar'],
                                            label=key,
                                            frameon = axes_dict['frameon'])
            self.axeslib[key].grid(axes_dict['grid'])
            self.axeslib[key].hold(axes_dict['hold'])


    def AxisFinder(self,key):
        axissetting = self.presetting.axislib[key]
        # get axes
        if axissetting['axes'] == None:
            raise KeyError,('axis do not relate to axes')
        else:
            axes_in_use = self.axeslib[axissetting['axes']]        
        
        # get axis
        if axissetting['mode'] == 'x':
            axis_in_use = axes_in_use.get_xaxis()
        elif axissetting['mode'] == 'y':
            axis_in_use = axes_in_use.get_yaxis()
        else:
            raise TypeError,('Mode setting is not correct',mode)    
        return axis_in_use
    
    def AxisLibFinder(self):
        for key in self.presetting.axislib.keys():
            if key != 'default':
                self.axislib[key] = self.AxisFinder(key)
    
    
    def setAxis(self):
                
        # generate axislib
        self.AxisLibFinder()
        # generate Axislib
        for key in self.presetting.axislib.keys():
            if key != 'default':
                self.setSingleAxis(key)
                #self.setLimits(key)
    
    def setLimitsall(self):
        for key in self.presetting.axislib.keys():
            if key != 'default':
                self.setLimits(key)            

    def linkLimitsall(self):
        for key in self.presetting.axislib.keys():
            if key != 'default':
                self.linkLimits(key)  
    
    def setSingleAxis(self,key):

        # get axis settings
        axissetting = self.presetting.axislib[key]
        
        # get axes
        if axissetting['axes'] == None:
            raise KeyError,('axis do not relate to axes')
        else:
            axes_in_use = self.axeslib[axissetting['axes']]
        
        axis_in_use = self.axislib[key]
        
        ticksetting = self.presetting.ticklib[key]    
        
        
        # set label postion
        axis_in_use.set_label_position(axissetting['position'])            
        
           
        # set tick location
        axes_in_use.tick_params(**ticksetting)
     
        
        # set label content
        axis_in_use.set_label_text(axissetting['label'] + " (" +
                          axissetting['unit'] +   ")" ) 

        # Set labelfont
        labeltext = axis_in_use.get_label()
        labeltext.set_fontproperties(self.fontlib[axissetting['labelfont']])
        
        
        # set tick position
        axis_in_use.set_ticks_position(axissetting['position'])
        
        # set tick fonts
        for label in axis_in_use.get_ticklabels():
            label.set_fontproperties(self.fontlib[axissetting['ticklabelfont']])            

        
        # set tick locator
        locatorkey = axissetting['locator']
        axis_in_use.set_major_locator(self.locatorlib[locatorkey])
        
        # apply customrized labels
        labels = self.presetting.locatorlib[locatorkey]['labels']
        minor = self.presetting.locatorlib[locatorkey]['minor']
        if labels != None:
            axis_in_use.set_ticklabels(labels)            
         
        # add minor tick
        if minor != 0:
            minor_locator = matplotlib.ticker.AutoMinorLocator(
                minor)
            axis_in_use.set_minor_locator(minor_locator)            

    def linkLimits(self,key):

        axissetting = self.presetting.axislib[key]
        axis_in_use = self.axislib[key]
        axes_in_use = self.axeslib[axissetting['axes']]
        [lmin,lmax] = axissetting['limits']
        mode = axissetting['mode']
        
        if lmin == 'link':
            # link current axis to another axis
            linkaxissetting = self.presetting.axislib[lmax]
            linkaxes = self.axeslib[linkaxissetting['axes']]
            
            target = linkaxissetting['unit']
            orign = axissetting['unit']
            factor = self.UI.convert(target,orign)
            
            # got current max/min
            if  mode == 'x':
                [lmin,lmax] = linkaxes.get_xlim()
                lmax= lmax * factor[0] + factor[1]
                lmin= lmin * factor[0] + factor[1]
                axes_in_use.set_xlim([lmin,lmax])
                
            elif mode == 'y':
                [lmin,lmax] = linkaxes.get_ylim()
                lmax= lmax * factor[0] + factor[1]
                lmin= lmin * factor[0] + factor[1]
                axes_in_use.set_ylim([lmin,lmax])
    
   # plot manopulation
    def setLimits(self,key):
        """
        Set limits for the x and y axes,
        Operation based on current ax
        """
        
        axissetting = self.presetting.axislib[key]
        axis_in_use = self.axislib[key]
        axes_in_use = self.axeslib[axissetting['axes']]
        [lmin,lmax] = axissetting['limits']
        mode = axissetting['mode']

        if lmin != 'link':
            # set specific limits
            if  mode == 'x':
                if lmax != None and lmax != 'auto':
                    axes_in_use.set_xlim(xmax=float(lmax))
                if lmin != None and lmin != 'auto':
                    axes_in_use.set_xlim(xmin=float(lmin))                
            elif mode == 'y':
                if lmax != None and lmax != 'auto':
                    axes_in_use.set_ylim(ymax=float(lmax))
                if lmin != None and lmin != 'auto':
                    axes_in_use.set_ylim(ymin=float(lmin))
            else:
                raise TypeError,('Mode should be x or y but got',mode)

    
    def getUnit(self,axeskey):
        tunitx = ''
        tunity = ''
        for key in self.presetting.axislib.keys():
            if self.presetting.axislib[key]['axes'] == axeskey:
                if self.presetting.axislib[key]['mode'] == 'x':
                    tunitx = self.presetting.axislib[key]['unit']
                elif self.presetting.axislib[key]['mode'] == 'y':
                    tunity = self.presetting.axislib[key]['unit']
        return [tunitx,tunity]
    
    

    def addPlot(self,axeskey,plotdata,showlegend=True):
        ax = self.axeslib[axeskey]
        linehandle = []
        labellist = []
        legendhandle = []
        legendlabel = []

        for icurvekey in plotdata.curvekeylist:
            icurve = plotdata.curvelib[icurvekey]
            try:
                style_in_use = self.presetting.linelib[icurve.ind]
            except KeyError:
                style_in_use = self.presetting.linelib['default']
                
            handle = ax.plot(icurve.xdata,icurve.ydata,**style_in_use) 
            linehandle.append(handle[0]) 
        
            labellist.append(icurve.legend)
            
            if icurve.legend != 'None':
                legendhandle.append(handle[0])
                legendlabel.append(icurve.legend)

        
        if showlegend and len(legendhandle) > 0:
            ax.legend(legendhandle,legendlabel,**self.legendlib['default'])
            #ax.legend(labellist,**self.legendlib['default'])
        # adjust limits if nesessary
        self.linkLimitsall()
        
    def addPlotOld(self,axeskey,plotdata,datalabel=None,legend=True):
        ax = self.axeslib[axeskey]
        linehandle = []
        labellist = []

        #ndm = plotdata.shape
        #ndm = len(plotdata.keys())
        line_seq = 1 # total line number
        for key in plotdata.keys():
            try:
                style_in_use = self.presetting.linelib[line_seq]
            except KeyError:
                style_in_use = self.presetting.linelib['default']
                
            handle = ax.plot(plotdata[key][:,0],plotdata[key][:,1],**style_in_use) 
            linehandle.append(handle) 
            line_seq += 1
        
            if datalabel != None:
                labellist.append(datalabel[key])
            else:
                labellist.append('N/A')
        
        if legend == True:
            ax.legend(labellist,**self.legendlib['default'])
        # adjust limits if nesessary
        self.linkLimitsall()
        
        
    def addPlot2(self,axeskey,tshift_x=[None,None],tshift_y=[None,None]):  #target shift
        
        ''' generate plot based on the self.plotdata'''
        
        [tunitx,tunity] = self.getUnit(axeskey)
        ax = self.axeslib[axeskey]
        
        line_seq = 0 # total line number
        for i in range(0,len(self.data.data_x)):
            for j in range(0,len(self.data.data_y[i])):
                line_seq += 1
                
                # calculate shift x
                if tshift_x[0] == 'uniform':
                    shift_x = tshift_x[1]
                elif tshift_x[0] == 'increment':
                    shift_x += tshift_x[1]
                else:
                    shift_x = 0
                    
                # calculate shift y
                if tshift_y[0] == 'uniform':
                    shift_y = tshift_y[1]
                elif tshift_x[0] == 'increment':
                    shift_y += tshift_y[1]
                else:
                    shift_y = 0
                    
                if self.data.data_y[i][j].style == 'default':
                    # use default line style settings
                    style_in_use = self.setting.linelib['default']
                elif self.data.data_y[i][j].style == 'sequence':
                    # use predefined sequence based styles
                    try:
                        style_in_use = self.presetting.linelib[line_seq]
                    except KeyError:
                        style_in_use = self.presetting.linelib['default']
                else:
                    try:
                        style_in_use = self.presetting.linelib[
                                                 self.data.data_y[i][j].style]
                    except KeyError:
                        style_in_use = self.presetting.linelib['default']                    
                        
                # plot based on required unit and shift
                #ax.scatter(self.data.data_x[i][0].getPdata(tunitx,[1,shift_x]),
                #             self.data.data_y[i][j].getPdata(tunity,[1,shift_y]))
                
                ax.plot(self.data.data_x[i][0].getPdata(tunitx,[1,shift_x]),
                             self.data.data_y[i][j].getPdata(tunity,[1,shift_y]),
                             **style_in_use)
                
        # adjust limits if nesessary
        self.linkLimitsall()
    
    def setTextbox(self,textboxkey,axeskey):
        dicttextbox = self.presetting.textboxlib[textboxkey]
        bboxkey = dicttextbox['bbox']
        fontkey = dicttextbox['fontproperties']
        dictbbox = self.presetting.boxlib[bboxkey]
        textboxfont = self.fontlib[fontkey]
        # update the textbox properties
        dicttextbox.update({'bbox':dictbbox})
        dicttextbox.update({'fontproperties':textboxfont})
        
        if dicttextbox['transform'] == 'transAxes':
            dicttextbox.update({'transform':self.axeslib[axeskey].transAxes})
        
        self.axeslib[axeskey].text(**dicttextbox)
    
    
    def save_fig_pdf(self,name='fig'):
        format = 'PDF'
        self.figure_canvas.figure.savefig(name+'.pdf',format=format,size=self.figsize)
    
if __name__ == '__main__':
    pass