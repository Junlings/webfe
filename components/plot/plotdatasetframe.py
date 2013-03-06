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
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
import time

class PlotDataSetPanel(wx.Panel):
    def __init__(self,parent,plotkey):
        wx.Panel.__init__(self,parent)
        #self.panel = wx.Panel(self)
        self.parent = parent
        self.results = parent.results
        self.plotdata = self.results.pdb[plotkey]
        self.plotkey = plotkey

        self.SetNoteBook = wx.aui.AuiNotebook(self,1,size=(500,500),style=wx.aui.AUI_NB_DEFAULT_STYLE - wx.aui.AUI_NB_CLOSE_BUTTON)
        self.SetNoteBook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.SetNoteBook, 1, wx.EXPAND)
        
        
        self.add_unitpage()
        self.add_labelpage()
        self.add_legendpage()
        self.add_maskpage()
        self.add_datapairpage()
        self.add_previewpage()
        self.add_settingpage()
        self.add_exportpage()

        
        #self.SetNoteBook.Split(5,wx.RIGHT)
        
        self.SetSizer(box)
        self.Layout()        
        # add resize event
        #wx.EVT_SIZE(self.SetNoteBook, self.OnSize) 
        
    def add_exportpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Export")            

        # add legend and point picker
        gs = wx.FlexGridSizer(5, 2, 5, 5)

        cont = []

        
        self.Export = wx.Button(f1,label='Export')
        self.Export.Bind(wx.EVT_LEFT_DOWN,self.OnExport)        

        

        vbox.Add(gs, proportion=0,border=50)
        vbox.Add(self.Export, proportion=0,border=50)
        f1.SetSizer(vbox)
                 
        
        
    def add_previewpage(self):
        mfigure = self.results.figurerealize(self.plotkey)  # realize figure with all updates
        self.CanvasPanel = CanvasPanel(self.SetNoteBook,mfigure)     # create figure canvas
        self.previewpagename = "Preview Figure:"+self.plotkey
        self.previewpage = self.SetNoteBook.AddPage(self.CanvasPanel,self.previewpagename , select=True)       # add figure canvas to notebook             
        # try refresh 
        self.SetNoteBook.Update()
        
    def add_maskpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Masks")           
        
    
    def add_settingpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Settings")            

        # add legend and point picker
        gs = wx.FlexGridSizer(5, 2, 5, 5)
        self.settigdict = {}
        
        
        self.settigdict['style'] = wx.Choice(f1,size=(150,20),choices=list(self.results.sdb.keys()))
        self.settigdict['type'] = wx.Choice(f1,size=(150,20),choices=['line-one axis',])
        self.settigdict['style'].SetStringSelection(self.plotdata.style)
        self.settigdict['type'].SetStringSelection(self.plotdata.type)
        
        
        cont = []
        cont.append((wx.StaticText(f1, label='    Figure Style    '), 0, wx.ALIGN_CENTER))
        cont.append((self.settigdict['style'], 0, wx.ALIGN_CENTER))
        cont.append((wx.StaticText(f1, label='    Figure Type    '), 0, wx.ALIGN_CENTER))
        cont.append((self.settigdict['type'], 0, wx.ALIGN_CENTER))
        
        self.UpdateSettings = wx.Button(f1,label='Update')
        self.UpdateSettings.Bind(wx.EVT_LEFT_DOWN,self.OnUpdateSettings)        

        
        gs.AddMany(cont)
        vbox.Add(gs, proportion=0,border=50)
        vbox.Add(self.UpdateSettings, proportion=0,border=50)
        f1.SetSizer(vbox)
            
        
    def add_datapairpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Data Pair")
        
        # add legend and point picker
        gs = wx.FlexGridSizer(50, 5, 5, 5)
        self.labeldict = {}
        
        cont = []
        cont.append(((0,0), 0, 0))# wx.EXPAND))
        cont.append((wx.StaticText(f1, label='X-Table'), 0, wx.ALIGN_CENTER))
        cont.append((wx.StaticText(f1, label='X-Column'), 0, wx.ALIGN_CENTER))
        cont.append((wx.StaticText(f1, label='Y-Table'), 0, wx.ALIGN_CENTER))
        cont.append((wx.StaticText(f1, label='Y-Column'), 0, wx.ALIGN_CENTER))
        
        for key in self.plotdata.curvelib.keys():
            cont.append((wx.StaticText(f1, label='    curve'+str(key)+'   '), 0, wx.ALIGN_CENTER))
            icurve =  self.plotdata.curvelib[key]
            self.labeldict[key] = {'X-Table':wx.Choice(f1,size=(150,20),choices=self.results.get_tdbkeys()), #, label='Show Legend?') #,style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
                                    'X-Column' : wx.Choice(f1,size=(150,20),choices=self.results.get_tdblabelkeys(icurve.xtablekey)),
                                    'Y-Table' : wx.Choice(f1,size=(150,20),choices=self.results.get_tdbkeys()),
                                    'Y-Column' : wx.Choice(f1,size=(150,20),choices=self.results.get_tdblabelkeys(icurve.ytablekey))}
            
            self.labeldict[key]['X-Table'].SetStringSelection(icurve.xtablekey)
            self.labeldict[key]['X-Column'].SetStringSelection(icurve.xcolumnname)
            self.labeldict[key]['Y-Table'].SetStringSelection(icurve.ytablekey)
            self.labeldict[key]['Y-Column'].SetStringSelection(icurve.ycolumnname)
            
            
            cont.append((self.labeldict[key]['X-Table'], 0, wx.ALIGN_CENTER))
            cont.append((self.labeldict[key]['X-Column'], 0, wx.ALIGN_CENTER))
            cont.append((self.labeldict[key]['Y-Table'], 0, wx.ALIGN_CENTER))
            cont.append((self.labeldict[key]['Y-Column'], 0, wx.ALIGN_CENTER))

        self.AddCurve = wx.Button(f1,label='Add Curve')
        self.AddCurve.Bind(wx.EVT_LEFT_DOWN,self.OnAddCurve)


        gs.AddMany(cont)
        vbox.Add(gs, proportion=0,border=50)
        vbox.Add(self.AddCurve, proportion=0,border=50)
        f1.SetSizer(vbox)
    
    
    def AddCurveRow(self):
        pass
    
    
    def OnAddCurve(self,event):
        pass
        
        
    def add_legendpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Legend")
        
        # add legend and point picker
        gs = wx.FlexGridSizer(50, 5, 5, 5)
        self.legenddict = {}
        
        cont = []
        cont.append(((0,0), 0, 0))# wx.EXPAND))
        cont.append((wx.StaticText(f1, label='Show Legend?'), 0, wx.ALIGN_CENTER))
        cont.append((wx.StaticText(f1, label='Legend Text?'), 0, wx.ALIGN_CENTER))
        cont.append((wx.StaticText(f1, label='Legend Style?'), 0, wx.ALIGN_CENTER))
        cont.append((wx.StaticText(f1, label='Marker Size?'), 0, wx.ALIGN_CENTER))
        
        for key in self.plotdata.curvelib.keys():
            icurve = self.plotdata.curvelib[key]
            #cont.append(wx.StaticText(f1, label='curve'+str(key),style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL))
            cont.append((wx.StaticText(f1, label='    curve'+str(key)+'   '), 0, wx.ALIGN_CENTER))
            self.legenddict[key] = {'legendkey':wx.CheckBox(f1), #, label='Show Legend?') #,style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
                                    'legendstyleid' : wx.TextCtrl(f1,size=(150,20)),
                                    'legendtext' : wx.TextCtrl(f1,size=(150,20)),
                                    'legendmarkersize' : wx.TextCtrl(f1,size=(150,20))}
            
            self.legenddict[key]['legendtext'].SetValue(icurve.legend)
            showlegend  = icurve.legend == 'None'
            self.legenddict[key]['legendkey'].SetValue(not showlegend)
            self.legenddict[key]['legendstyleid'].SetValue('Style Based')
            self.legenddict[key]['legendmarkersize'].SetValue('Style Based')
            
            #self.Bind(wx.EVT_CHECKBOX, self.OnCheckLegend,self.legenddict[key]['legendkey']) # working
            
            cont.append((self.legenddict[key]['legendkey'], 0, wx.ALIGN_CENTER))
            cont.append((self.legenddict[key]['legendtext'], 0, wx.ALIGN_CENTER))
            cont.append((self.legenddict[key]['legendstyleid'], 0, wx.ALIGN_CENTER))
            cont.append((self.legenddict[key]['legendmarkersize'], 0, wx.ALIGN_CENTER))
            
        # bind the button function
        self.update_legend = wx.Button(f1,label='Update')
        self.update_legend.Bind(wx.EVT_LEFT_DOWN,self.OnUpdateLegends)

        cont.append((self.update_legend, 0, 0))# wx.EXPAND))
        
        gs.AddMany(cont)
        vbox.Add(gs, proportion=0,border=50)
        f1.SetSizer(vbox)
        
    
        
    
    def add_unitpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Units")        
        gs = wx.GridSizer(5, 2, 5, 5)
        

        
        self.unit_x1_label = wx.StaticText(f1, label='Unit for X1 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.unit_y1_label = wx.StaticText(f1, label='Unit for Y1 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.unit_x2_label = wx.StaticText(f1, label='Unit for X2 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.unit_y2_label = wx.StaticText(f1, label='Unit for Y2 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.unit_x1 = wx.TextCtrl(f1,size=(150,20))
        self.unit_y1 = wx.TextCtrl(f1,size=(150,20))
        self.unit_x2 = wx.TextCtrl(f1,size=(150,20))
        self.unit_y2 = wx.TextCtrl(f1,size=(150,20))
        #self.space1 = wx.Spacer(f1,size=(20,20))
        
        # bind the button function
        self.update_unit = wx.Button(f1,label='Update')
        self.update_unit.Bind(wx.EVT_LEFT_DOWN,self.OnUpdateUnits)

        cont = []
        cont.append((self.unit_x1_label, 0, wx.ALIGN_CENTER))#wx.EXPAND))
        cont.append((self.unit_x1, 0, 0))# wx.EXPAND))
        cont.append((self.unit_y1_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.unit_y1, 0, 0))# wx.EXPAND))
        cont.append((self.unit_x2_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.unit_x2, 0, 0))# wx.EXPAND))
        cont.append((self.unit_y2_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.unit_y2, 0, 0))# wx.EXPAND))
        cont.append(((0,0), 0, 0))# wx.EXPAND))
        
        cont.append((self.update_unit, 0, 0))# wx.EXPAND))
        
        gs.AddMany(cont)
        vbox.Add(gs, proportion=0,border=50)
        f1.SetSizer(vbox)
        
        # set initial values
        self.unit_x1.SetValue(self.plotdata.unit[0])
        self.unit_y1.SetValue(self.plotdata.unit[1])
        self.unit_x2.SetValue(self.plotdata.unit[2])
        self.unit_y2.SetValue(self.plotdata.unit[3])

    def add_labelpage(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        f1 = wx.Panel(self.SetNoteBook)
        self.SetNoteBook.AddPage(f1, "Labels")        
        gs = wx.GridSizer(6, 4, 5, 5)
        
        self.scaleminlabel = wx.StaticText(f1, label='Min',size=(50,20),style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.scalemaxlabel = wx.StaticText(f1, label='Max',size=(50,20),style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
      
        
        self.x1_label = wx.StaticText(f1, label='Label for X1 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.y1_label = wx.StaticText(f1, label='Label for Y1 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.x2_label = wx.StaticText(f1, label='Label for X2 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.y2_label = wx.StaticText(f1, label='Label for Y2 axis',style=wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        self.x1 = wx.TextCtrl(f1,size=(150,20))
        self.y1 = wx.TextCtrl(f1,size=(150,20))
        self.x2 = wx.TextCtrl(f1,size=(150,20))
        self.y2 = wx.TextCtrl(f1,size=(150,20))

        self.x1_max = wx.TextCtrl(f1,size=(50,20))
        self.y1_max = wx.TextCtrl(f1,size=(50,20))
        self.x2_max = wx.TextCtrl(f1,size=(50,20))
        self.y2_max = wx.TextCtrl(f1,size=(50,20))
        
        self.x1_min = wx.TextCtrl(f1,size=(50,20))
        self.y1_min = wx.TextCtrl(f1,size=(50,20))
        self.x2_min = wx.TextCtrl(f1,size=(50,20))
        self.y2_min = wx.TextCtrl(f1,size=(50,20))
        self.update_label = wx.Button(f1,label='Update')
        self.update_label .Bind(wx.EVT_LEFT_DOWN,self.OnUpdateLabels)
        
        cont = []
        cont.append(((0,0), 0, 0))# wx.EXPAND))
        cont.append(((0,0), 0, 0))# wx.EXPAND))
        cont.append((self.scaleminlabel, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.scalemaxlabel, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        
        cont.append((self.x1_label, 0, wx.ALIGN_CENTER))#wx.EXPAND))
        cont.append((self.x1, 0, 0))# wx.EXPAND))
        cont.append((self.x1_min, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.x1_max, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        
        cont.append((self.y1_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.y1, 0, 0))# wx.EXPAND))
        cont.append((self.y1_min, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.y1_max, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        
        cont.append((self.x2_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.x2, 0, 0))# wx.EXPAND))
        cont.append((self.x2_min, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.x2_max, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        
        
        cont.append((self.y2_label, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.y2, 0, 0))# wx.EXPAND))
        cont.append((self.y2_min, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        cont.append((self.y2_max, 0, wx.ALIGN_CENTER))# wx.EXPAND))
        
        cont.append(((0,0), 0, 0))# wx.EXPAND))
        cont.append(((0,0), 0, 0))# wx.EXPAND))
        cont.append(((0,0), 0, 0))# wx.EXPAND))
        cont.append((self.update_label, 0, 0))# wx.EXPAND))
        
        gs.AddMany(cont)
        vbox.Add(gs, proportion=0,border=50)
        f1.SetSizer(vbox)
        
        # setup labesl
        # set initial values
        self.x1.SetValue(self.plotdata.label[0])
        self.y1.SetValue(self.plotdata.label[1])
        self.x2.SetValue(self.plotdata.label[2])
        self.y2.SetValue(self.plotdata.label[3])

        self.x1_min.SetValue(self.plotdata.minlimits[0])
        self.y1_min.SetValue(self.plotdata.minlimits[1])
        self.x2_min.SetValue(self.plotdata.minlimits[2])
        self.y2_min.SetValue(self.plotdata.minlimits[3])        

        self.x1_max.SetValue(self.plotdata.maxlimits[0])
        self.y1_max.SetValue(self.plotdata.maxlimits[1])
        self.x2_max.SetValue(self.plotdata.maxlimits[2])
        self.y2_max.SetValue(self.plotdata.maxlimits[3])
        
    def OnUpdateFigure(self,event):
        self.CanvasPanel.FigureUpdate(self.results.figurerealize(self.plotkey))
        
        #self.SetNoteBook.ChangeSelection(5)
        #self.OnPageChanged(self, event)
        #pass  # need to up
        
    def OnPageChanged(self, evt):
        pageename = self.SetNoteBook.GetPageText(self.SetNoteBook.GetSelection())
        
        # try update the preview figure when tab changed to
        if 'Preview' in pageename:
            #print 'preview page selected'
            self.CanvasPanel.FigureUpdate(self.results.figurerealize(self.plotkey))
        #ptype,pname = pageename.split(':')
        #self.activepage = {'type':ptype,'key':pname}
        #print self.activepage
        
    def OnUpdateUnits(self,event):
        x1 = self.unit_x1.GetValue()
        y1 = self.unit_y1.GetValue()
        x2 = self.unit_x2.GetValue()
        y2 = self.unit_y2.GetValue()
        
        pub.sendMessage("COMMAND", '*plot_edit_pdb_units,%s,%s,%s,%s,%s' % (self.plotkey,x1,y1,x2,y2))
        #self.OnUpdateFigure(event)

    def OnUpdateLegends(self,event):
        for key,item in self.legenddict.items():
            if item['legendkey'].GetValue():
                pub.sendMessage("COMMAND", '*plot_edit_pdb_legends,%s,%s,%s' % (self.plotkey,key,item['legendtext'].GetValue()))
            else:
                pub.sendMessage("COMMAND", '*plot_edit_pdb_legends,%s,%s,%s' % (self.plotkey,key,None))

        
    def OnUpdateLabels(self,event):
        x1 = self.x1.GetValue()
        y1 = self.y1.GetValue()
        x2 = self.x2.GetValue()
        y2 = self.y2.GetValue()
        
        pub.sendMessage("COMMAND", '*plot_edit_pdb_labels,%s,%s,%s,%s,%s' % (self.plotkey,x1,y1,x2,y2))
        
        # check if need to do limits updates
        x1_max = self.x1_max.GetValue()
        y1_max = self.y1_max.GetValue()
        x2_max = self.x2_max.GetValue()
        y2_max = self.y2_max.GetValue()        
        x1_min = self.x1_min.GetValue()
        y1_min = self.y1_min.GetValue()
        x2_min = self.x2_min.GetValue()
        y2_min = self.y2_min.GetValue()           
        
        if not str(x1_max) == str(self.plotdata.maxlimits[0]):
            pub.sendMessage("COMMAND", '*plot_edit_pdb_limits,%s,%s,%s' % (self.plotkey,'x1_max',x1_max))
        if not str(y1_max) == str(self.plotdata.maxlimits[1]):
            pub.sendMessage("COMMAND", '*plot_edit_pdb_limits,%s,%s,%s' % (self.plotkey,'y1_max',y1_max))
        if not str(x2_max) == str(self.plotdata.maxlimits[2]):
            pub.sendMessage("COMMAND", '*plot_edit_pdb_limits,%s,%s,%s' % (self.plotkey,'x2_max',x2_max))
        if not str(y2_max) == str(self.plotdata.maxlimits[3]):
            pub.sendMessage("COMMAND", '*plot_edit_pdb_limits,%s,%s,%s' % (self.plotkey,'y2_max',y2_max))
        if not str(x1_min) == str(self.plotdata.minlimits[0]):
            pub.sendMessage("COMMAND", '*plot_edit_pdb_limits,%s,%s,%s' % (self.plotkey,'x1_min',x1_min))
        if not str(y1_min) == str(self.plotdata.minlimits[1]):
            pub.sendMessage("COMMAND", '*plot_edit_pdb_limits,%s,%s,%s' % (self.plotkey,'y1_min',y1_min))
        if not str(x2_min) == str(self.plotdata.minlimits[2]):
            pub.sendMessage("COMMAND", '*plot_edit_pdb_limits,%s,%s,%s' % (self.plotkey,'x2_min',x2_min))
        if not str(y2_min) == str(self.plotdata.minlimits[3]):
            pub.sendMessage("COMMAND", '*plot_edit_pdb_limits,%s,%s,%s' % (self.plotkey,'y2_min',y2_min))
        

        
        #self.OnUpdateFigure(event)
    def OnUpdateSettings(self,event):
        stylekey = self.settigdict['style'].GetStringSelection()
        typekey = self.settigdict['type'].GetStringSelection()
        
        pub.sendMessage("COMMAND", '*plot_edit_pdb_settings,%s,%s,%s' % (self.plotkey,typekey,stylekey))
        #self.OnUpdateFigure(event)
        
        
    def OnExport(self,event):
        ''' save model by pickle module '''
        wildcard = "Model Data File (*.csv)|*.csv|" \
         "All files (*.*)|*.*"
        
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.CHANGE_DIR
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        pub.sendMessage("COMMAND", '*plot_pdata_save,%s,%s' % (self.plotkey,paths[0]))        