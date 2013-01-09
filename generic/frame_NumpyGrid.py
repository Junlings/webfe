#!/usr/bin/env python
""" This provide a frame which contain  grid

Grid Data driven decide by the data defined
"""

import wx
import wx.aui
import wx.grid
import numpy as np
from generic_frame_simple import GenericFrameSimple
from GUI_uti import textEntry
from components.units.unit_select import UnitSelectDiag

class GenericTableNumpy(wx.grid.PyGridTableBase):
    """
    generic Table class
    """
    def __init__(self, inputsingleresult=None):
        wx.grid.PyGridTableBase.__init__(self)
        
        ## initialize the parameters
        #self.databack = results(inputsingleresult.tag)
        
        if  type(inputsingleresult['data']) == type(np.array([])):
            self.data = inputsingleresult['data']
            if len(self.data.shape) == 1:
                self.data = np.reshape(self.data, (-1, 1))
            self.labellist = inputsingleresult['labellist']
            self.unitlist = inputsingleresult['unitlist']
        else:
            raise TypeError, 'data is not numpy array'

        self.setcollabels()
        self.setrowlabels()

        self.defaultstyle()   
        
    def setrowlabels(self):
        self.rowLabels = []
        for i in range(0,1 + self.data.shape[0]):
            if i == 0:
                self.rowLabels.append('unit')
            else:
                self.rowLabels.append(str(i))        
    
    def setcollabels(self):
        self.colLabels= []
        self.colLabels = self.labellist      

        
    def defaultstyle(self):
        self.odd=wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour("sky blue")
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.even=wx.grid.GridCellAttr()
        self.even.SetBackgroundColour("sea green")
        self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
    def GetNumberRows(self):
        return self.data.shape[0]
        #return len(self.data)

    def GetNumberCols(self):
        if len(self.data.shape) == 1:
            return 1
        else:
            return self.data.shape[1]
        
    def GetColLabelValue(self, col):
        try:
            return self.colLabels[col]
        except:
            return 'Unknown Column'
       
    def GetRowLabelValue(self, row):
        return self.rowLabels[row]

        
    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        if row == 0:
            try:
                return self.unitlist[col]
            except:
                return 'N/A'
        else:
            return self.data[row,col]

    def SetValue(self, row, col, value):
        ''' need to update here to call the command and refresh the grid '''
        if row == 0:
            self.unitlist[col] = str(value)
        else:
            self.data[row,col] = value
        
    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][row % 2]
        attr.IncRef()
        return attr
    
    def OnCloseMe(self, event):
        ## update the database
        self.Close(True)
        
        

        
class NumpyGrid(wx.grid.Grid):
    def __init__(self, parent,data):
        wx.grid.Grid.__init__(self, parent, 1,style=wx.ALL|wx.EXPAND)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)        
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)  
        wx.EVT_KEY_DOWN(self, self.OnKey)
        
    def update_grid(self,inputsingleresult):
        self.tableBase = GenericTableNumpy(inputsingleresult=inputsingleresult)
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

    def OnKey(self, event):
        # If Ctrl+C is pressed...
        if event.ControlDown() and event.GetKeyCode() == 67:
            print "Ctrl+C"
            self.selection()
            # Call copy method
            self.copy()

    def selection(self):
        # Show cell selection
        # If selection is cell...
        if self.GetSelectedCells():
            print "Selected cells " + str(self.GetSelectedCells())
        # If selection is block...
        if self.GetSelectionBlockTopLeft():
            print "Selection block top left " + str(self.GetSelectionBlockTopLeft())
        if self.GetSelectionBlockBottomRight():
            print "Selection block bottom right " + str(self.GetSelectionBlockBottomRight())
       
        # If selection is col...
        if self.GetSelectedCols():
            print "Selected cols " + str(self.GetSelectedCols())
       
        # If selection is row...
        if self.GetSelectedRows():
            print "Selected rows " + str(self.GetSelectedRows())
            
    def copy(self):
        print "Copy method"
        # Number of rows and cols
        rows = self.GetSelectionBlockBottomRight()[0][0] - self.GetSelectionBlockTopLeft()[0][0] + 1
        cols = self.GetSelectionBlockBottomRight()[0][1] - self.GetSelectionBlockTopLeft()[0][1] + 1
       
        # data variable contain text that must be set in the clipboard
        data = ''
       
        # For each cell in selected range append the cell value in the data variable
        # Tabs '\t' for cols and '\r' for rows
        for r in range(rows):
            for c in range(cols):
                data = data + str(self.GetCellValue(self.GetSelectionBlockTopLeft()[0][0] + r, self.GetSelectionBlockTopLeft()[0][1] + c))
                if c < cols - 1:
                    data = data + '\t'
            data = data + '\n'
        # Create text data object
        clipboard = wx.TextDataObject()
        # Set data object value
        clipboard.SetText(data)
        # Put the data in the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")

    def paste(self):
        print "Paste method"
        clipboard = wx.TextDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")
        data = clipboard.GetText()
        table = []
        y = -1
        # Convert text in a array of lines
        for r in data.splitlines():
            y = y +1
            x = -1
            # Convert c in a array of text separated by tab
            for c in r.split('\t'):
                x = x +1
                self.SetCellValue(self.GetGridCursorRow() + y, self.GetGridCursorCol() + x, c)
               
    def delete(self):
        print "Delete method"
        # Number of rows and cols
        rows = self.GetSelectionBlockBottomRight()[0][0] - self.GetSelectionBlockTopLeft()[0][0] + 1
        cols = self.GetSelectionBlockBottomRight()[0][1] - self.GetSelectionBlockTopLeft()[0][1] + 1
        # Clear cells contents
        for r in range(rows):
            for c in range(cols):
                self.SetCellValue(self.GetSelectionBlockTopLeft()[0][0] + r, self.GetSelectionBlockTopLeft()[0][1] + c, '')
                
class NumpyGridFrame(GenericFrameSimple):
    
    def __init__(self,parent,settings = {'title':'NumpyGridFrame','size':(500,500)}):
        
        GenericFrameSimple.__init__(self, parent,-1,settings = settings)

        self.grid = NumpyGrid(self,None)

        menuBar = wx.MenuBar()
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        
    def update(self,inputdict):
        self.grid.update_grid(inputdict)
    
    def OnLoad(self,event):pass
    def onCloseWindow(self, event):
        self.Destroy()
        #return res
    def OnCellLeftClick(self, event):
        if event.GetRow() == 0:
            row = event.GetRow()
            col = event.GetCol()
            diag = UnitSelectDiag(self,col,row)

            if diag.ShowModal() == wx.ID_OK:
                unitlabel = diag.getunit()
                self.SetValue(row,col,unitlabel)

        event.Skip()
        
    def SetValueEvent(self,row,col,value):
        self.SetValue(row,col,value)


class NumpyGridPanel(wx.Panel):
    
    def __init__(self,parent):
        
        wx.Panel.__init__(self, parent,-1,style=wx.ALL|wx.EXPAND)

        self.grid = NumpyGrid(self,None)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        sizer = wx.BoxSizer()
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer) 
        
    def update(self,inputdict):
        self.grid.update_grid(inputdict)
    
    def OnCellLeftClick(self, event):
        if event.GetRow() == 0:
            row = event.GetRow()
            col = event.GetCol()
            diag = UnitSelectDiag(self,col,row)

            if diag.ShowModal() == wx.ID_OK:
                unitlabel = diag.getunit()
                self.SetValue(row,col,unitlabel)

        event.Skip()
        
    def SetValueEvent(self,row,col,value):
        self.SetValue(row,col,value)
        
if __name__ == '__main__':
    import numpy as np
    app = wx.PySimpleApp()
    res = {'data':np.array([[1,2,3],[4,5,6],[7,8,9]]),'unit':['in.','in.','in.'],'label':['aa','bb','cc']}
    f1 = NumpyGridFrame(None)
    f1.Show()
    f1.grid.update_grid(res,None)
    app.MainLoop()
