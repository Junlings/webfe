import wx
import wx.aui
from results_xrc import xrcResultFrame
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

def add_method(self, method, name=None):
    if name is None:
        name = method.func_name
    setattr(self.__class__, name, method)
    
def add_method_cls(self,cls):
    for fun,obj in cls.__dict__.items():
        if hasattr(obj, '__call__'):
            add_method(self,obj)

class ResultFrame(xrcResultFrame):
    def __init__(self,parent,results):
        xrcResultFrame.__init__(self,parent)
        self.results = results
        
        add_method_cls(self.ResultTree,MyDictTree) # = MyDictTree(self.frame.ModelTree.GetParent())
        
        self.ResultTree.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeActivate)       
        

        self.Bind(wx.EVT_MENU, self.OnPdataCreate, self.MenuItem_Pdata_Create)
        self.Bind(wx.EVT_MENU, self.OnFigureCreate, self.MenuItem_Plot)
        self.ResultTree.root = self.ResultTree.AddRoot('Result Database')
        
        
        # bind file operation
        
        self.Bind(wx.EVT_MENU, self.OnNewResults,self.TOOL_RESULT_NEW)
        self.Bind(wx.EVT_MENU, self.OnLoadResults,self.TOOL_RESULT_LOAD)
        self.Bind(wx.EVT_MENU, self.OnSaveResults,self.TOOL_RESULT_SAVE)
        self.Bind(wx.EVT_MENU, self.OnCloseResults,self.TOOL_RESULT_SAVEAS )
        
        
        # bind postprocess
        self.Bind(wx.EVT_MENU, self.OnPostMarct16,self.TOOL_RESULT_MARC_T16)
        
        
        # bind tree butto
        self.TOOL_TREE_REFRESH.Bind(wx.EVT_LEFT_DOWN,self.OnResChange)
        self.TOOL_TREE_EXPAND.Bind(wx.EVT_LEFT_DOWN,self.ResultTree.OnExpandAll)
        self.TOOL_TREE_COLLAPSE.Bind(wx.EVT_LEFT_DOWN,self.ResultTree.OnCollapseAll)
        
        #self.OnResChange(event)
        
        # bind tool bar
        self.Bind(wx.EVT_TOOL, self.OnResChange, self.TOOL_TREE_REFRESH) 
        
        
        # add notebook
        self.ModelNoteBook = wx.aui.AuiNotebook(self.RESULT_PANEL_NOTEBOOK,1,size=(500,500),style=wx.aui.AUI_NB_DEFAULT_STYLE)
        #btn = wx.Button(self.RESULT_PANEL_NOTEBOOK,label='gg')
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.ModelNoteBook, 1, wx.EXPAND)
        #box.Add(btn, 2, wx.EXPAND)
        self.RESULT_PANEL_NOTEBOOK.SetSizer(box)
        self.RESULT_PANEL_NOTEBOOK.Layout() 

       

    def OnPostMarct16(self,event):
        diag = PostDiag(self,self.results)
        diag.Show()
        
        
    def OnTreeActivate(self,event):
        pathlist = self.ResultTree.GetSelectionPath()
        
        if pathlist[0] == 'Table':
            f1 = NumpyGridPanel(self.ModelNoteBook)
            f1.grid.update_grid(self.results.tdb[pathlist[1]])
            self.ModelNoteBook.AddPage(f1, "Table:"+pathlist[1])
            
            #f2 = NumpyGridFrame(self.ModelNoteBook)
            #f2.grid.update_grid(self.results.tdb[pathlist[1]])
            #f2.Show()
            

        if pathlist[0] == 'Figure':
            self.OnAddFigurePage(pathlist[1])
    
    def OnAddFigurePage(self,figurekey):
        mfigure = self.results.figurerealize(figurekey)
        f1 = CanvasPanel(self.ModelNoteBook,mfigure)
        self.ModelNoteBook.AddPage(f1, "Figure:"+figurekey)        
        
    def OnResChange(self,event):
        
        self.ResultTree.DeleteChildren(self.ResultTree.GetRootItem())
        
        if self.results != None:
            resldict = self.results.generate_libdict()
            self.ResultTree.create_nodes_dict(self.ResultTree.root,resldict)
            self.ResultTree.GetParent().Refresh()
            self.ResultTree.GetParent().SetFocus()
    
    def OnForceResChange(self,event,results):
        self.results = results
        self.OnResChange(event)
    
    def OnPdataCreate(self,event):
        contlist = self.results.getcollabes()
        p1 = PlotDataFrame(self,contlist)
        p1.Show()

    def OnFigureCreate(self,event):
        p1 = figurecreate(self)
        p1.update(self.results)
        p1.Show()
        
    def OnNewResults(self,event):
        pub.sendMessage("COMMAND", '*post_new')
        pub.sendMessage("GUIREFRESH", 'results')

        
    def OnLoadResults(self,event):
        ''' load pickle model file '''
        wildcard = "Model Data File (*.pyres)|*.pyres|" \
         "All files (*.*)|*.*"
        
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.CHANGE_DIR
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                print path

            pub.sendMessage("COMMAND", '*post_load,%s' % paths[0])
            pub.sendMessage("GUIREFRESH", 'results')

        
    def OnSaveResults(self,event):
        ''' save model by pickle module '''
        wildcard = "Result Data File (*.pyres)|*.pyres|" \
         "All files (*.*)|*.*"
        
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.CHANGE_DIR
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        pub.sendMessage("COMMAND", '*post_save,%s' % paths[0])
        
    def OnCloseResults(self,event):
        pub.sendMessage("COMMAND", '*post_new')