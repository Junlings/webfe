import wx
import wx.aui
#from wx.lib.pubsub import Publisher as pub
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
import sys
sys.path.append('../../webfe')
from generic.dict_tree import MyDictTree
from generic.frame_NumpyGrid import NumpyGridFrame,NumpyGridPanel
from components.plot.plotdatadiag import PlotDataFrame
from components.plot.figurecreate import figurecreate
from components.plot.plotframe import FigureFrame, CanvasPanel
from components.post.postframe import PostDiag
from components.post.plainframe import plainpost

class PlotDataSetPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        #self.panel = wx.Panel(self)

        self.SetNoteBook = wx.aui.AuiNotebook(self,1,size=(500,500),style=wx.aui.AUI_NB_DEFAULT_STYLE - wx.aui.AUI_NB_CLOSE_BUTTON)
        self.SetNoteBook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.SetNoteBook, 1, wx.EXPAND)
        
        
        self.add_unitpage()
        self.add_labelpage()
        self.add_maskpage()
        self.add_datapairpage()
        
        self.SetSizer(box)
        self.Layout()
        
        
    def add_maskpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Masks")           
        
        
    def add_datapairpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Data Pair")           
    
    
    def add_unitpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Units")        
        gs = wx.GridSizer(4, 2, 5, 5)
        

        
        self.unit_x1_label = wx.StaticText(f1, label='Unit for X1 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.unit_y1_label = wx.StaticText(f1, label='Unit for Y1 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.unit_x2_label = wx.StaticText(f1, label='Unit for X2 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.unit_y2_label = wx.StaticText(f1, label='Unit for Y2 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.unit_x1 = wx.TextCtrl(f1,size=(150,20))
        self.unit_y1 = wx.TextCtrl(f1,size=(150,20))
        self.unit_x2 = wx.TextCtrl(f1,size=(150,20))
        self.unit_y2 = wx.TextCtrl(f1,size=(150,20))

        cont = []
        cont.append((self.unit_x1_label, 0, wx.ALIGN_CENTER))#wx.EXPAND))
        cont.append((self.unit_x1, 0, 0))# wx.EXPAND))
        cont.append((self.unit_y1_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.unit_y1, 0, 0))# wx.EXPAND))
        cont.append((self.unit_x2_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.unit_x2, 0, 0))# wx.EXPAND))
        cont.append((self.unit_y2_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.unit_y2, 0, 0))# wx.EXPAND))
    
        gs.AddMany(cont)
        vbox.Add(gs, proportion=0,border=50)
        f1.SetSizer(vbox)        

    def add_labelpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Labels")        
        gs = wx.GridSizer(4, 2, 5, 5)
        

        
        self.x1_label = wx.StaticText(f1, label='Label for X1 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.y1_label = wx.StaticText(f1, label='Label for Y1 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.x2_label = wx.StaticText(f1, label='Label for X2 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.y2_label = wx.StaticText(f1, label='Label for Y2 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.x1 = wx.TextCtrl(f1,size=(150,20))
        self.y1 = wx.TextCtrl(f1,size=(150,20))
        self.x2 = wx.TextCtrl(f1,size=(150,20))
        self.y2 = wx.TextCtrl(f1,size=(150,20))

        cont = []
        cont.append((self.x1_label, 0, wx.ALIGN_CENTER))#wx.EXPAND))
        cont.append((self.x1, 0, 0))# wx.EXPAND))
        cont.append((self.y1_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.y1, 0, 0))# wx.EXPAND))
        cont.append((self.x2_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.x2, 0, 0))# wx.EXPAND))
        cont.append((self.y2_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.y2, 0, 0))# wx.EXPAND))
    
        gs.AddMany(cont)
        vbox.Add(gs, proportion=0,border=50)
        f1.SetSizer(vbox)
        
    def OnPageChanged(self, evt):
        pageename = self.SetNoteBook.GetPageText(self.SetNoteBook.GetSelection())
        #ptype,pname = pageename.split(':')
        #self.activepage = {'type':ptype,'key':pname}
        #print self.activepage