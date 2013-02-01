#!/usr/bin/env python

import os
import wx
import sys
import random
sys.path.append('../../..')

#from FEA.postprocess.import_plain import *
#from FEA.postprocess.uti_file_comm import *
#from FEA.postprocess.collector import *

class ListFrame(wx.Frame):
    def __init__(self,cols,rows,Dcfun):
        wx.Frame.__init__(self, None, -1,
                          "wx.ListCtrl in wx.LC_REPORT mode",
                          size=(600,400))
        self.Dcfun = Dcfun
        self.rows = rows
        self.list = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListDClick, self.list)
      

        # Add some columns
        for col, text in enumerate(cols):
            self.list.InsertColumn(col, text)

        # add the rows
        for item in rows:
            index = self.list.InsertStringItem(sys.maxint, item[0])
            for col, text in enumerate(item[1:]):
                self.list.SetStringItem(index, col+1, text)
                
        # set the width of the columns in various ways
        self.list.SetColumnWidth(0, 120)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
        
    def OnListDClick(self,event):
        pos = event.GetIndex()
        print str(pos)
        self.Dcfun(self.rows[pos][0])
        
class fileimport(wx.Frame):
    def __init__(self,dataconn=None):
        wx.Frame.__init__(self,None,title='Import from file')
        self.panel = wx.Panel(self)
        self.dataconn = dataconn
        static = wx.StaticText(self.panel, wx.NewId(), 'import options', (10,0))
        self.bt_selectfile =wx.Button(self.panel,-1, 'Select File', (20,140))
        self.bt_convert =wx.Button(self.panel,-1, 'Convert', (200,140))
        self.chk_header = wx.CheckBox(self.panel, -1, "Include Header", (20, 20), (150, 20))
        self.chk_unit = wx.CheckBox(self.panel, -1, "Include Unit", (20, 40), (150, 20))
        self.chk_pydat = wx.CheckBox(self.panel, -1, "Special pydat", (20, 60), (150, 20))
        self.chk_Unidict = wx.CheckBox(self.panel, -1, "Unidict", (20, 80), (150, 20))
        
        static = wx.StaticText(self.panel, wx.NewId(), 'Convert options', (200,0))
        sampleList = ['To list', 'To array', 'To Unidict']
        self.exp = wx.RadioBox(self.panel, -1, "A Radio Box", (200, 40), wx.DefaultSize,
                        sampleList, 1, wx.RA_SPECIFY_COLS)  
        self.Bind(wx.EVT_BUTTON, self.OnOpenFile, self.bt_selectfile)
        self.Bind(wx.EVT_BUTTON, self.Oncommit, self.bt_convert)
        #OpenFile(frame)
        self.Show()
    def OnOpenFile(self,event):
        self.filename = OpenFile(self)
    
    def dataconn2(self,value):
        col1 = collector()
        res = col1.importbysetting(value)
        print res
        self.dataconn(value,res)
        
    def Oncommit(self,event):
        res = {}
        res['filename'] = self.filename
        res['header'] = self.chk_header.GetValue()
        res['unit'] = self.chk_unit.GetValue()
        res['pydat'] = self.chk_pydat.GetValue()
        res['Unidict'] = self.chk_Unidict.GetValue()
        res['export'] = self.exp.GetStringSelection()
        print res
        self.dataconn2(res)
        self.Destroy()
        
    ### ==========setup text field
    def createTextFields(self, panel):
        if self.obj_data.textFieldData!=None:
            for eachLabel, eachPos in self.obj_data.textFieldData:
                self.createCaptionedText(panel, eachLabel, eachPos)

    
    def createCaptionedText(self, panel, label, pos):
        static = wx.StaticText(panel, wx.NewId(), label, pos)
        static.SetBackgroundColour("White")
        textPos = (pos[0] + 75, pos[1])
        wx.TextCtrl(panel, wx.NewId(), "", size=(100, -1), pos=textPos)
    
    
    def createStaticText(self, panel):
        if self.obj_data.StaticText!=None:
            for eachLabel, eachPos in self.obj_data.StaticText:
                static = wx.StaticText(panel, wx.NewId(), eachLabel, eachPos)
                static.SetBackgroundColour("White")
                
def OpenFile(obj):
    """
    Provide the openfile dialogu
    """
    wildcard = "python file (*.pydat)|*.pydat|All files (*.*)|*.*"
    dlg = wx.FileDialog(obj, "Open import file...", os.getcwd(),
                       style=wx.OPEN, wildcard=wildcard)
    filename=None
    if dlg.ShowModal() == wx.ID_OK:
        filename = dlg.GetPath()
    return filename


def textEntry(obj,display,default=None):
    dlg = wx.TextEntryDialog(obj, display,'Text Entry')
    if default != None:
        dlg.SetValue(default)
    else:
        dlg.SetValue("Default")
    if dlg.ShowModal() == wx.ID_OK:
        value =  dlg.GetValue()
        dlg.Destroy()
        return value

class TextEntryDialog(wx.Dialog):
    def __init__(self, parent, title, captionlist,valuelist=None):
        self.captionlist = captionlist
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super(TextEntryDialog, self).__init__(parent, -1, title, style=style)
        self.input = {}
        buttons = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        self.mysizer = wx.BoxSizer(wx.VERTICAL)
        self.create_multiinput()
        self.mysizer.Add(buttons, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizerAndFit(self.mysizer)
        if valuelist != None:
            self.valuelist = valuelist
            self.SetValue(valuelist)
            
        
    def create_singleinput(self,caption):
        text1 = wx.StaticText(self, -1, caption)
        input = wx.TextCtrl(self, -1)
        input.SetInitialSize((40, 30))
        self.mysizer.Add(text1, 0, wx.ALL, 5)
        self.mysizer.Add(input, 1, wx.EXPAND|wx.ALL, 5)
        return input
    
    def create_multiinput(self):
        for i in range(0,len(self.captionlist)):
            caption = self.captionlist[i]
            self.input[caption] = self.create_singleinput(caption)
        
    def SetSingleValue(self, key,value):
        self.input[key].SetValue(value)
    
    def SetValue(self,valuelist):
        for i in range(0,len(self.captionlist)):
            caption = self.captionlist[i]
            self.SetSingleValue(caption,valuelist[i])
    
    def GetSingleValue(self,key):
        return (self.input[key].GetValue())
        
    def GetValue(self):
        self.valuelist = []
        for i in range(0,len(self.captionlist)):
            caption = self.captionlist[i]
            res = self.GetSingleValue(caption)
            self.valuelist.append(res)
        return self.valuelist
        
if __name__ == '__main__':
    
    app = wx.App(0)
    #dlg= TextEntryDialog(None,'sdfgsdfg',['sdfgsdfg','ddd'],valuelist=['sdsds','ssdsdsd'])
    #dlg.Show()
    #a1 = fileimport()
    columns = ["Request ID", "Summary", "Date", "Submitted By"]
    rows = [("987441", "additions to RTTI?", "2004-07-08 10:22", "g00fy"),
    ("846368", "wxTextCtrl - disable auto-scrolling", "2003-11-20 21:25", "ryannpcs"),
    ("846368", "wxTextCtrl - disable auto-scrolling", "2003-11-20 21:25", "ryannpcs"),
    ("846368", "wxTextCtrl - disable auto-scrolling", "2003-11-20 21:25", "ryannpcs"),
    ("846368", "wxTextCtrl - disable auto-scrolling", "2003-11-20 21:25", "ryannpcs")]
    a1 = ListFrame(columns,rows,None)
    a1.Show()
    app.MainLoop()