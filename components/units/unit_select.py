#!/usr/bin/env python

import  wx
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
from unit_Select_xrc import xrcDIALOG1
from core.plots.unitsystem import create_units
class UnitSelectDiag(xrcDIALOG1):
    """ Tree Frane """
    def __init__(self, parent,row,col):
        xrcDIALOG1.__init__(self,parent)   # Call the function PreXXX where XXX is your wx base class
        ModelNoteBook = parent.parent
        self.tablename = ModelNoteBook.GetPageText(ModelNoteBook.GetSelection()).split(':')[1]
        self.unitsystem = create_units()
        self.unitdict = self.unitsystem.get_unit_dict()
        self.row = row
        self.col = col
        self.UNIT_SYSTEM.Bind(wx.EVT_CHOICE, self.OnUnitSystem)
        self.UNIT_CAT.Bind(wx.EVT_CHOICE, self.OnUnitCAT)
        self.UNIT_LABEL.Bind(wx.EVT_CHOICE, self.OnUnitLABEL)
        
        self.UNIT_SYSTEM.Clear()
        self.UNIT_SYSTEM.AppendItems(list(self.unitsystem.get_unit_dict().keys()))
        self.UNIT_CAT.Enable(False)
        self.UNIT_LABEL.Enable(False)
        
    def OnUnitSystem(self,event):
        unitdict = self.unitsystem.get_unit_dict()
        SelSystem = self.UNIT_SYSTEM.GetStringSelection()
        self.UNIT_CAT.Clear()
        applist = []
        for key,item in unitdict[SelSystem].items():
            if len(item) > 0:
                applist.append(key) 
        self.UNIT_CAT.AppendItems(applist)
        self.UNIT_CAT.Enable(True)
        self.UNIT_LABEL.Enable(False)

    def OnUnitCAT(self,event):
        unitdict = self.unitsystem.get_unit_dict()
        SelSystem = self.UNIT_SYSTEM.GetStringSelection()
        SelCat = self.UNIT_CAT.GetStringSelection()
        self.UNIT_LABEL.Clear()
        self.UNIT_LABEL.AppendItems(list(unitdict[SelSystem][SelCat]))
        self.UNIT_LABEL.Enable(True)

    def OnUnitLABEL(self,event):
        unitlabel = self.UNIT_LABEL.GetStringSelection()
        
        original = self.Parent.grid.tableBase.GetValue(self.row,self.col)
        if original != unitlabel:
            self.Parent.grid.tableBase.SetValue(self.row,self.col,unitlabel)
            self.Parent.grid.ForceRefresh()
            pub.sendMessage("COMMAND", '*plot_edit_tdb_table_unit,%s,%s:%s,%s' % (self.tablename,self.row,self.row,unitlabel))
            
    def getunit(self,event):
        unitlabel = self.UNIT_LABEL.GetStringSelection()
        return unitlabel
if __name__ == '__main__':

    app = wx.App(redirect = False)
    
    #res1 = results('res1')
    #res1.label = ['aa','bb','vv']
    #res2 = results('res1')
    #res2.label = ['aa2','bb2','vv2']

    
    #da1.inputtreedict = {'aaaa' : ['aaa1','aaa2'],'bbbb' : ['bbb1','bbb2'],'CCCC': ['cccc1','cccc2','cccc3','cccc4',]}
   # da1.inputplotdict = {'aaaa' : ['aaa1','aaa2'],'bbbb':['bbb1','bbb2']}
    frame = UnitSelectDiag(None)
    
    frame.Show()
    app.MainLoop()