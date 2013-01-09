#!/usr/bin/env python
## The collection of all grid realization
import wx
import wx.aui
import wx.grid
from GUI_uti import *
import numpy as np
from generic_panel import *
#from ..core.plots.unitsystem import *

class GenericPaneldata():
    """ datastructure to feed the generic panel"""
    def __init__(self):
        self.size = (800,500)
        self.pos = (100,100)
        self.label=("GenericPanel")
        
        self.StaticText= []
                        #(("First Name", (10, 50)),
                        #("Last Name", (10, 80)),
                        #("Occupation", (10, 110)),
                        #("Birthday", (10, 140))
                        #)
        self.buttonbarData =[]# (("First", 'OnFirst'),("<< PREV", 'OnPrev'))
        self.textFieldData = []
                        #(("First Name", (110, 50)),
                        #("Last Name", (110, 80)),
                        #("Occupation", (110, 110)),
                        #("Birthday", (110, 140))
                        #)
        self.datasource={}
        
    def __getitem__(self,lib):
        if lib == 'TextCtrl':
            return self.TextCtrl
        
    def create_TextCtrl_dict(self,dict1,loc,shift):
        n_TextCtrl = 0
        for key in dict1.keys():
            self.create_TextCtrl(key,(loc[0]+shift[0]*n_TextCtrl,
                                      loc[1]+shift[1]*n_TextCtrl))
            n_TextCtrl += 1
            
    def create_TextCtrl(self,key,loc):
        """
        Create TextCtrl based on the dictionary
        """
        self.textFieldData.append((key,loc))
        
    def set_textctrl(self,TextCtrl):
        """ get textCtrl dict from the created the panel instance""" 
        self.TextCtrl = TextCtrl
    
    def Get_value_all(self):
        res_dict = {}
        for i in range(0,len(self.textFieldData)):
            key = self.textFieldData[i][0]
            res = self.Get_value('TextCtrl',key)
            # here can add possible type check
            res_dict[key] = res
        self.datasource.update(res_dict)
        
    def Set_value_all(self):
        for i in range(0,len(self.textFieldData)):
            key = self.textFieldData[i][0]
            self.Set_value('TextCtrl',key,str(self.datasource[key]))
        
    def Get_value(self,lib,tag):
        value = self[lib][tag].GetValue()
        return value
    
    def Set_value(self,lib,tag,value):
        self[lib][tag].SetValue(value)
    
    
      
      
class results():
    def __init__(self,tag,*args):
        self.tag = tag
        #self.unitsys = unit_system()
        
        if len(args) == 3:
        
           self.dataset = args[0]
           self.label = args[1]
           self.unit = args[2]
           self.shape = self.dataset.shape
        
        elif len(args) == 2:
           self.dataset = args[0]
           self.shape = self.dataset.shape
           self.label = args[1]
           n = self.shape[1]
           self.unit = ['N/A' for i in range (1,n+1)]
           
        elif len(args) == 1:
           self.dataset = args[0]
           self.shape = self.dataset.shape
           n = self.shape[1]
           self.label = ['col' + str(i) for i in range (1,n+1)]
           self.unit = ['N/A' for i in range (1,n+1)]
           
        else:
           self.dataset = None
           self.label = None
           self.unit = None
           self.shape = (0,0)
           
    def Init_n(self,m,n):
            self.dataset = np.zeros([m,n])
            self.label = ['col' + str(i) for i in range (1,n+1)]
            self.unit = ['N/A' for i in range (1,n+1)]        
            self.shape = self.dataset.shape
            
    def update(self,other):
            self.dataset = other.dataset
            self.label = other.label
            self.unit = other.unit      
            self.shape = self.dataset.shape          

    def GetData(self,label,TargetUnit=None):
        """ convert one dimensional data from source unit to targetunit"""
        try:
            id = self.label.index(label)
        except:
            print 'label:"',label,'" do not defined'
            raise KeyError
        else:
            if TargetUnit == None:
                return self.dataset[:,id],self.unit[id]
            else:
                sourceunit = self.unit[id]
                factor = self.unitsys.convert(sourceunit,TargetUnit)
                
                return self.dataset[:,id]/factor,TargetUnit



class GenericTableData(GenericPaneldata):
    def __init__(self):
        GenericPaneldata.__init__(self)
        self.inputdata = None
        self.inputunit = None
        self.inputlabel = None
        self.initialsize = None
        self.conndata = None
        self.name ='gridData'

    def conv_list_cell(self,list):
        """
        convert the list to cell to support the grid display
        """
        res={}
        for i in range(0,len(list)):
            for j in range(0,len(list[i])):
                res[i,j]=list[i][j]
        return res    

    def OnRefresh(self,event):
        self.grid.ForceRefresh()
    
    def OnClear(self,event):pass
    
    def update_grid(self,singleresult):
        self.grid.update_grid(singleresult)        
        
    def ForceRefresh(self):
        self.grid.ForceRefresh()
        
    def OnLoadfromfile(self,event):
        filename = OpenFile(None)
        dataset,label,unit = import_plain(filename)
        celldata = np.array(dataset)
        singleresult = result(celldata,label,unit)
        
        self.update_grid(singleresult)
        self.ForceRefresh()
        self.grid.Show()
        
class GenericTable(wx.grid.PyGridTableBase):
    """
    generic Table class
    """
    def __init__(self, inputsingleresult=None,initialsize=None):
        wx.grid.PyGridTableBase.__init__(self)
        
        ## initialize the parameters
        self.databack = results(inputsingleresult.tag)
        
        # uodate the initial size
        if initialsize== None and inputsingleresult.dataset == None:
            self.initialsize = [21,2]
            self.databack.Init_n(21+1,2)
        elif  inputsingleresult.dataset != None:
            self.databack = inputsingleresult
        else:
            self.initialsize = [int(initialsize[0])+1,int(initialsize[1])]
            self.databack.Init_n(int(initialsize[0])+1,int(initialsize[1]))
            

        self.setcollabels()
        self.setrowlabels()

        if inputsingleresult == None:  # no initialize data
            self.databack.dataset = np.zeros([self.initialsize[0]-1,self.initialsize[1]])

        self.defaultstyle()   
        
    def setrowlabels(self):
        self.rowLabels = []
        for i in range(0,1+self.databack.shape[0]):
            if i == 0:
                self.rowLabels.append('unit')
            else:
                self.rowLabels.append(str(i))        
    
    def setcollabels(self):
        self.colLabels= []
        self.colLabels = self.databack.label      

        
    def defaultstyle(self):
        self.odd=wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour("sky blue")
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.even=wx.grid.GridCellAttr()
        self.even.SetBackgroundColour("sea green")
        self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
    def GetNumberRows(self):
        return self.databack.shape[0]
        #return len(self.data)

    def GetNumberCols(self):
        return self.databack.shape[1]
        
    def GetColLabelValue(self, col):
        return self.colLabels[col]
       
    def GetRowLabelValue(self, row):
        return self.rowLabels[row]

        
    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        if row == 0:
            return self.databack.unit[col]
        else:
            return self.databack.dataset[row,col]

    def SetValue(self, row, col, value):
        if row == 0:
            self.databack.unit[col] = value
        else:
            self.databack.dataset[row,col] = value
        
    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][row % 2]
        attr.IncRef()
        return attr
    
    def OnCloseMe(self, event):
        ## update the database
        self.Close(True)
        

        
class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent,data):
        wx.grid.Grid.__init__(self, parent, -1)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)        
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)  
    
    def update_grid(self,inputsingleresult,initialsize):
        self.tableBase = GenericTable(inputsingleresult=inputsingleresult,initialsize=initialsize)
        self.SetTable(self.tableBase)
    
    def OnLabelLeftDClick(self,event):
        col = event.GetCol()
        label = textEntry(self,'Editcolumn label')
        #print col,label
        if label != None:
            self.tableBase.colLabels[col] = label
            self.tableBase.GetColLabelValue(col)
        self.ForceRefresh()
        
    def OnLabelRightClick(self,event):
        """ column data manuipulation"""
        self.col = event.GetCol()
        frame = wx.Frame(None)        
        menu_id1 = wx.NewId()
        menu_id2 = wx.NewId()
        frame.menu = wx.Menu()
        frame.menu.AppendItem(wx.MenuItem(frame.menu, menu_id1, "Inverse"))
        frame.menu.AppendItem(wx.MenuItem(frame.menu, menu_id2, "Shift"))
        frame.Bind(wx.EVT_MENU, self.Inverse, id=menu_id1)
        frame.Bind(wx.EVT_MENU, self.menu, id=menu_id2)
        frame.PopupMenu(frame.menu)
        

    def Inverse(self,event):
        print self.col
        self.tableBase.databack.dataset[:,self.col] = self.tableBase.databack.dataset[:,self.col]*-1
        self.ForceRefresh()
        
    def menu(self,event):
        pass
        
class gridPanel(GenericPanel):
    def __init__(self,parent,obj,id):  #,initialsize=None,inputdata=None,inputunit=None,inputlabel=None,conndata=None):
        #wx.Panel.__init__(self, parent, id,style=wx.DEFAULT_FRAME_STYLE|wx.CLOSE_BOX)
        
        GenericPanel.__init__(self,parent,obj,id)
        self.obj = obj
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)       
        self.grid = SimpleGrid(self,None)
        sizer.Add(self.grid, 1, wx.EXPAND, 0)
        
        self.grid.update_grid(obj.inputsingleresult,obj.initialsize)
        
        #self.obj = GenericTableData()
        self.obj.grid = self.grid
    
    def onCloseWindow(self, event):
        self.Destroy()
        #return res


class MyNotebookPanel(wx.Panel):
    def __init__(self,parent,obj,*args,**kargs):
        self.obj = obj
        wx.Panel.__init__(self,parent,*args,**kargs)
        
        self.buttonPanel = wx.Panel(self)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)
        
        self.nb = wx.aui.AuiNotebook(self)#wx.Notebook(self)
        # create tool bar

        self.buttonbarData = (
            ("NEW", 'OnAddData'),
            ("IMPORT", 'OnImport'),
            ("SHOW", 'OnPrintData'))
        self.createButtonBar(self.buttonPanel)
            

        # add
        sizer.Add(self.buttonPanel,0,wx.RIGHT|wx.TOP |wx.LEFT,10)
        sizer.Add(self.nb, 1, wx.EXPAND, 0)
        self.Layout()
        
        self.resultslib = {}
        
    def createButtonBar(self, panel, xPos = 0):
        if self.buttonbarData!=None:
            yPos = 0
            for eachLabel, eachHandler in self.buttonbarData:
                pos = (xPos, yPos)
                button = self.buildOneButton(panel, eachLabel, eachHandler, pos)
                yPos += button.GetSize().height +5
                
    def buildOneButton(self, parent, label, handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos)
        handler=getattr(self,handler)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button
        
    def add_page(self,wxwindow,tabname):
        self.nb.AddPage(wxwindow, tabname,select=True)

    def add_grid(self,gridobj):
        page1 = gridPanel(self.nb,gridobj,-1)
        self.add_page(page1,gridobj.inputsingleresult.tag)
        self.resultslib[gridobj.inputsingleresult.tag] = page1.grid.tableBase.databack
        
        
    def OnAddData(self,event):
        """ add data from direct input"""
        # collect the user defined data shape and unit,labels
        dlg= TextEntryDialog(None,'Please specify the name of data and size',['name','nrow','ncol'])
        dlg.SetValue(['Group'+str(len(self.resultslib.keys())),'0','0'])
        dlg.Show()
        if dlg.ShowModal() == wx.ID_OK:
            name,nrow,ncol =  dlg.GetValue()
        dlg.Destroy()
        
        gridobj = GenericTableData()
        gridobj.initialsize = [nrow,ncol]
        gridobj.inputsingleresult = results(name)
        
        # triger the grid frame to realize the input
        self.add_grid(gridobj)
        
    def OnImport(self,event):
        """
        Import data from file, should notice that the data supported are dict
        with single key as column
        """
        # call the external file import frame to realize
        inputfileframe = fileimport(self.getfileinputsetting)
        inputfileframe.Show()
        
    def getfileinputsetting(self,obj,value):
        """
        read data from file and then show in the grid
        """
        dataset,label,unit = value
        tag = 'import' + str(len(self.resultslib.keys())+1)
        
        gridobj = GenericTableData()
        gridobj.inputsingleresult = results(tag,np.array(dataset),label,unit)
        self.add_grid(gridobj)

    def OnShowdata(self,event):
        """ show the data for current data key on grid frame"""
        tablist = []
        for pageNum in range(self.nb.GetPageCount()):
            tablabel = self.nb.GetPageText(pageNum)
            tablist.append(tablabel)
            #page = notebook.GetPage(pageNum) 
        
        for key in self.resultslib.keys():
            if key not in tablist:
                gridobj = GenericTableData()
                gridobj.inputsingleresult = self.resultslib[key]
                self.add_grid(gridobj)
    
    def OnPrintData(self,event):
        for key in self.resultslib.keys():
            print self.resultslib[key].label
        
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Simple Notebook Example",size=(800,600))

        # Here we create a panel and a notebook on the panel
        
        
        gridobj = GenericTableData()
        gridobj.inputsingleresult = results('trial',np.array([[10,10],[10,10]]),
                                            ['a','b'],['kn','mm'])
        
        # create the page windows as children of the notebook
        p = MyNotebookPanel(self,gridobj)
        
    def onCloseWindow(self, event):
        self.Destroy()
        #return res
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    MainFrame().Show()
    app.MainLoop()
