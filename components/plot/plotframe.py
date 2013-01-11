import wx
import wx.aui

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.backends.backend_wx import _load_bitmap

from core.plots.plots import tpfdb
import os
filepath= os.path.realpath(__file__)
filefolder, filename = os.path.split(filepath)
resourcefolder = os.path.join(filefolder,'..','resource','self')

class MyNavigationToolbar(NavigationToolbar2WxAgg):
    """
    Extend the default wx toolbar with your own event handlers
    """
    ON_CUSTOM = wx.NewId()
    def __init__(self, canvas, cankill):
        NavigationToolbar2WxAgg.__init__(self, canvas)

        # for simplicity I'm going to reuse a bitmap from wx, you'll
        # probably want to add your own.
        self.AddSimpleTool(self.ON_CUSTOM, _load_bitmap(resourcefolder + '//' + 'L_D.png'), #stock_left.xpm'),
                           'Click me', 'Activate custom contol')
        #self.AddSimpleTool(self.ON_CUSTOM, _load_bitmap('stock_left.xpm'),
                           #'Click me', 'Save to PDF format')       
        wx.EVT_TOOL(self, self.ON_CUSTOM, self._on_custom)
        #wx.EVT_TOOL(self, self.ON_SAVETOPDF, self._on_savetopdf)
        
    def _on_custom(self, evt):

        self.canvas.draw()
        if evt != None:
            evt.Skip()
            
    def _on_savetopdf(self, evt):
        # add some text to the axes in a random location in axes (0,1)
        # coords) with a random color

        # get the axes
        #self.canvas.figure = fun(self.canvas.figure)
        format = 'PDF'
        self.canvas.figure.savefig(name_fig+'.pdf',format=format)
        
class CanvasPanel(wx.Panel):
    """ plot frame based on the Generic Frame class"""
    def __init__(self,parent,figure,*args,**kargs):
        wx.Panel.__init__(self,parent)
        # initialize the external data source
        figure.set_dpi(150)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        self.figurecavas = FigureCanvas(self, -1, figure)
        sizer.Add(self.figurecavas, 0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)

        self.figurecavas.mpl_connect('motion_notify_event', self.UpdateStatusBar)
        self.figurecavas.Bind(wx.EVT_ENTER_WINDOW, self.ChangeCursor)
        
        # setup the tool bar
        self.toolbar = MyNavigationToolbar(self.figurecavas, True)
        self.toolbar.Realize()
    
        sizer.Add(self.toolbar, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        
        self.text_x = wx.TextCtrl(self, wx.NewId(), "Value X:", size=(100, -1))
        self.text_y = wx.TextCtrl(self, wx.NewId(), "Value Y:", size=(100, -1))
        sizer.Add(self.text_x, 0, wx.TOP |wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.text_y, 0, wx.TOP |wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        
        # show the frame

        self.Show()
        
    def ChangeCursor(self, event):
        """ change the cursor within the canvas"""
        self.figurecavas.SetCursor(wx.StockCursor(wx.CURSOR_BULLSEYE))

    def UpdateStatusBar(self, event):
        """ update the statue bar for point position"""
        if event.inaxes:
            x, y = event.xdata, event.ydata
            self.text_x.SetValue(str(x))
            self.text_y.SetValue(str(y))
            #self.statusBar.SetStatusText(( "x= " + str(x) +
            #                               "  y=" +str(y) ),
            #                               0)
    def set_limits(self,limits):
        """
        Set limits for the x and y axes,
        Operation based on current ax
        """
        ax1 = self.figurecavas.figure.axes[0]
        if limits!=None:
            if limits[0]!=None and limits[0]!='None':
                ax1.set_xlim(xmin=float(limits[0]))
            if limits[1]!=None and limits[1]!='None':
                ax1.set_xlim(xmax=float(limits[1]))
            if limits[2]!=None and limits[2]!='None':
                ax1.set_ylim(ymin=float(limits[2]))
            if limits[3]!=None and limits[3]!='None':
                ax1.set_ylim(ymax=float(limits[3]))
        return ax1
    
    def set_labels(self,label):
        """
        Set labels for the x and y axes
        """
        ax = self.figurecavas.figure.axes[0]
        ax.set_xlabel(label[0])
        ax.set_ylabel(label[1])
        
        
class FigureFrame(wx.Frame):
    
    def __init__(self,parent,settings,figure):
        size = (600,420)
        figure.set_dpi(150)
        super(FigureFrame,self).__init__(parent,size=size,title=settings['title'])
        self.panel = CanvasPanel(self,figure)
        
        
if __name__ == '__main__':
    
    
    rp = tpfdb()
    rp.add('da',np.array([[-1,-0.1,0,6,7,8,8]]).T,unitlist=['m'],labellist=['dx'])
    rp.add('db',np.array([[5,6,8,6,7,8,8],[1,2,3,5,6,1,7]]).T,unitlist=['m','m'],labellist=['dx','dy'])
    
    rp.add_dmask('shiftx',{'oper':'Shift','scalar':10})
    rp.add_dmask('flip',{'oper':'FlipSign'})
    rp.add_dmask('cutstart1',{'oper':'CutNegative','nodenum':2})
    
    rp.add_plotdata('plot1',[['da:dx','db:dx','cutstart1'],['da:dx','db:dy']],units=['m','m'],xylabels=['x','y'],masklist=None)
    #rp.add_plotdata('plot2',[['da:dx','db:dx'],['da:dx','db:dy']],units=['m','m','in.','in.'],xylabels=['x1','y1','x2','y2'],transform={1:{'x':[2,-10]}})
    rp.add_plotdata('plot2',[['da:dx','db:dx'],['da:dx','db:dy']],units=['m','m'],xylabels=['x','y'],masklist=None)
    
   
    rp.line('plot1','plot1',skey='mono')
    
    
    app = wx.PySimpleApp()
    frame1 =  FigureFrame(None,rp.fdb['plot1'].figure)
    frame1.Show()
    app.MainLoop()