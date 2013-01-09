#!/usr/bin/env python
""" This provide a frame which contain  grid

Grid Data driven decide by the data defined
"""

import wx
import wx.aui
import wx.grid
import numpy as np
from generic_frame_simple import GenericFrameSimple
import os
iconfolder, filename = os.path.split(os.path.abspath(__file__))
iconfolder = os.path.join(iconfolder,'icons')
import csv
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

class GenericTableDict(wx.grid.PyGridTableBase):
    """
    generic Grid Table Data class, driven by input dictionary
    """
    def __init__(self, inputsingleresult):
        wx.grid.PyGridTableBase.__init__(self)
        
        ## initialize the parameters
        self.databack = inputsingleresult

        self.rowlabels = list(self.databack.keys()) 
        self.setcollabels()
        self.setrowlabels()
        self.defaultstyle()   
        
    def setrowlabels(self):
        pass
   
    def setcollabels(self):
        self.colLabels= range(0,11)
        #self.colLabels = self.databack.label      

        
    def defaultstyle(self):
        self.odd=wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour("sky blue")
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.even=wx.grid.GridCellAttr()
        self.even.SetBackgroundColour("sea green")
        self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
    

    def GetNumberRows(self):
        return len(self.rowlabels)
        #return len(self.data)

    def GetNumberCols(self):
        mcol = 0
        for key,item in self.databack.items():
            if len(item.getlist()) > mcol: mcol = len(item.getlist())
                
        return mcol
    
    def GetColLabelValue(self, col):
        return self.colLabels[col]
       
    def GetRowLabelValue(self, row):
        return self.rowlabels[row]

   
    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        try:
            return self.databack[self.rowlabels[row]].getlist()[col]
        except:
            return ''
        
    def SetValue(self, row, col, value):
        self.databack[self.rowlabels[row]][col] = value
        
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
        wx.EVT_KEY_DOWN(self, self.OnKey)

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
            
    def OnKey(self, event):
        # If Ctrl+C is pressed...
        if event.ControlDown() and event.GetKeyCode() == 67:
            print "Ctrl+C"
            self.selection()
            # Call copy method
            self.copy()
            
    def update_grid(self,inputsingleresult):
        self.tableBase = GenericTableDict(inputsingleresult)
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
                
class DictGridFrame(GenericFrameSimple):
    
    def __init__(self,parent,settings = {'title':'GridFrame','size':(500,500)},ftype='None'):
        
        GenericFrameSimple.__init__(self, parent,-1,settings = settings)

        self.grid = SimpleGrid(self,None)
        self.ftype = ftype

        menuBar = wx.MenuBar()
        
        self.settings.update({'toolbarData':{'Mode':'HORIZONTAL','Data':[
                                  ('Export','OnFileExport',os.path.join(iconfolder,'export.png')),
                                  ('Import','OnFIleImport',os.path.join(iconfolder,'import.png'))
                                ]}})
        self.createToolBar()
    
    
            
    def update(self,inputdict):
        self.grid.update_grid(inputdict)
    
    def OnLoad(self,event):pass
    def onCloseWindow(self, event):
        self.Destroy()
        #return res
        
    def OnFileExport(self,event):
        wildcard = "Model component File (*.txt)|*.txt|" \
         "All files (*.*)|*.*"
        
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.CHANGE_DIR
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                print path        
        
            fullpath = paths[0]
        
            pub.sendMessage("COMMAND", '*export_model,%s,%s' % (self.ftype,fullpath))      
    
    def OnFIleImport(self,event):pass



class DictGridPanel(wx.Panel):
    
    def __init__(self,parent):
        
        wx.Panel.__init__(self, parent)

        self.grid = SimpleGrid(self,None)
        #self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        sizer = wx.BoxSizer()
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer) 
        
        
            
    def update(self,inputdict):
        self.grid.update_grid(inputdict)
    
    def OnLoad(self,event):pass
    def onCloseWindow(self, event):
        self.Destroy()
        #return res
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    GridFrame(None).Show()
    app.MainLoop()
