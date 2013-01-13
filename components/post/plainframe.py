import wx
from plain_xrc import xrcDIALOG1

from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
import glob


class plainpost(xrcDIALOG1):
    
    def __init__(self,parent):
        xrcDIALOG1.__init__(self,parent)
        self.filter = None
        self.FILE_EXTENSION_INPUT.Enable(False)
        
        self.FILE_EXTENSION_CHOICE.Bind(wx.EVT_CHOICE, self.OnEXTChoice)
        self.FILE_EXTENSION_INPUT.Bind(wx.EVT_TEXT, self.OnEXTInput)
        self.FILE_SELECT_SCAN.Bind(wx.EVT_LEFT_DOWN,self.OnScan)
        self.FILE_SELECT_APPLY.Bind(wx.EVT_LEFT_DOWN,self.OnApply)
        
        


        # events
        tree = self.FILE_SELECTION.GetTreeCtrl()
        #self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.dirBrowser_OnItemSelected, tree)
        #self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.dirBrowser_OnRightClick, tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.dirBrowser_OnSelectionChanged, tree)
    
    #def dirBrowser_OnItemSelected(self,event):pass
    
    #def dirBrowser_OnRightClick(self,event):pass
    
    def OnScan(self,event):
        try:
            self.filepathlist = glob.glob(self.pathget+'//'+self.filter)
        except:
            self.filepathlist = [self.pathget]
        self.FILE_SELECT_NUM.SetValue(str(len(self.filepathlist)))
        
    def OnApply(self,event):
        com = ''
        for pathitem in self.filepathlist:
            com += ',' + pathitem
        pub.sendMessage("COMMAND", '*post_plain_filelist %s' % com)
        pub.sendMessage("GUIREFRESH", 'results')
    
    def dirBrowser_OnSelectionChanged(self,event):
        self.pathget = self.FILE_SELECTION.GetPath()
        self.FILE_SELECT_PATH.SetValue(self.pathget)
    
    def OnEXTChoice(self,event):
        selstr = self.FILE_EXTENSION_CHOICE.GetStringSelection()
        if selstr == 'Other':
            self.FILE_EXTENSION_INPUT.Enable(True)
            self.filter = self.FILE_EXTENSION_INPUT.GetValue()
        else:
            self.FILE_EXTENSION_INPUT.Enable(False)
            self.filter = selstr
        
        #print self.FILE_SELECTION.GetFilter()
        self.FILE_SELECTION.SetFilter(self.filter)
        parentpath = self.FILE_SELECTION.GetPath()
        
        self.FILE_SELECTION.ReCreateTree()
        self.FILE_SELECTION.ExpandPath(parentpath)
        
        
    def OnEXTInput(self,event):
        selstr = self.FILE_EXTENSION_INPUT.GetValue()
        if '*' not in selstr:
            selstr = '*.' + selstr
            
        self.filter = selstr