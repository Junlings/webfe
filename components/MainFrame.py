import wx
import wx.aui
from wx import xrc
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

from components.MainFrame_xrc import xrcMainFrame
from procedures.PoleDent.diag_pole import PoleDiag
from procedures.Poleartificialdent.diag_pole2 import PoleDiag2
from procedures.patch.diag_patch import PatchDiag
from procedures.hybridsystem.hybridsystem import hybridsystem
import datetime
import sys
import os

sys.path.append('../webfe/')
from core.imports.marc.import_marc_dat import importfile_marc_dat
from core.model.registry import model
from core.export.export import exporter
from core.settings import settings
from generic.dict_tree import MyDictTree
from generic.frame_DictGrid import DictGridFrame, DictGridPanel
from components.section.section_xrc import xrcDIAG_Section
from components.section.rebargroup_xrc import xrcDIAG_Rebar
from components.post.postframe import PostDiag
from components.post.resultframe import ResultFrame
from components.gl.glpanel import FEM_3D_window


global _maxdigits
_maxdigits = 3


        
        
def add_method(self, method, name=None):
    if name is None:
        name = method.func_name
    setattr(self.__class__, name, method)


def add_method_cls(self,cls):
    for fun,obj in cls.__dict__.items():
        if hasattr(obj, '__call__'):
            add_method(self,obj)
        
class MainFrame(xrcMainFrame):

    def __init__(self,parent,model,app):
        #self.feamodel = None
        xrcMainFrame.__init__(self,parent)
        self.model = model
        self.app = app
        # update tree ctrl
        add_method_cls(self.ModelTree,MyDictTree) 

        self.CreateBinding()
        self.ModelTree.bind()
        self.ModelTree.root = self.ModelTree.AddRoot('Model Informations')

        # add notebook
        self.ModelNoteBook = wx.aui.AuiNotebook(self.ModelNoteBookPanel,1,size=(500,500),style=wx.aui.AUI_NB_DEFAULT_STYLE)
        #btn = wx.Button(self.RESULT_PANEL_NOTEBOOK,label='gg')
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.ModelNoteBook, 1, wx.EXPAND)
        #box.Add(btn, 2, wx.EXPAND)
        self.ModelNoteBookPanel.SetSizer(box)
        self.ModelNoteBookPanel.Layout() 
        

        
    def CreateBinding(self):
        
        # bind the toolbar
        self.Bind(wx.EVT_MENU, self.OnNew,self.MAIN_TOOL_NEW)
        self.Bind(wx.EVT_MENU, self.OnOpen,self.MAIN_TOOL_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave,self.MAIN_TOOL_SAVE )
        self.Bind(wx.EVT_MENU, self.OnClose,self.MAIN_TOOL_SAVEAS)
        
        
        # bind additional toolbar as button
        self.MAIN_MACRO_RECORD.Bind(wx.EVT_LEFT_DOWN,self.OnMacroRecord)
        self.MAIN_MACRO_STOP.Bind(wx.EVT_LEFT_DOWN,self.OnMacroStop)
        self.MAIN_MACRO_SAVE.Bind(wx.EVT_LEFT_DOWN,self.OnMacroSave)
        self.MAIN_MACRO_LOAD.Bind(wx.EVT_LEFT_DOWN,self.OnMacroLoad)

        # bind model tree functions
        self.MAIN_TOOL_MODELREFRESH.Bind(wx.EVT_LEFT_DOWN,self.OnModelChange)
        self.MAIN_TOOL_EXPAND.Bind(wx.EVT_LEFT_DOWN,self.ModelTree.OnExpandAll)
        self.MAIN_TOOL_COLLAPSE.Bind(wx.EVT_LEFT_DOWN,self.ModelTree.OnCollapseAll)
        
        # Bind file menu
        self.Bind(wx.EVT_MENU, self.OnNew, self.MenuItem_New)
        self.Bind(wx.EVT_MENU, self.OnOpen, self.MenuItem_Open)
        self.Bind(wx.EVT_MENU, self.OnSave, self.MenuItem_Save)
        self.Bind(wx.EVT_MENU, self.OnClose, self.MenuItem_Close)
        
        
        # Bind FEM menu
        self.Bind(wx.EVT_MENU, self.OnFemGrid, self.MenuItem_Grid)
        self.Bind(wx.EVT_MENU, self.OnFemConn, self.MenuItem_Conn)
        self.Bind(wx.EVT_MENU, self.OnFemProp, self.MenuItem_Prop)
        self.Bind(wx.EVT_MENU, self.OnFemSet, self.MenuItem_Set)
        
        
        # Bind utility menu
        self.Bind(wx.EVT_MENU, self.OnUtiPatch, self.MenuItem_Patch)
        self.Bind(wx.EVT_MENU, self.OnUtiSection, self.MenuItem_Section)
        self.Bind(wx.EVT_MENU, self.OnUtiRebar, self.MenuItem_Rebar)
        
        # Bind export menu
        self.Bind(wx.EVT_MENU, self.OnExpMarcProc, self.MenuItem_ExpMarcProc)
        self.Bind(wx.EVT_MENU, self.OnExpMarcDat, self.MenuItem_ExpMarcDat)
        self.Bind(wx.EVT_MENU, self.OnExpOpenSees, self.MenuItem_ExpOpenSees)
        
        # Bind Procedure menu
        self.Bind(wx.EVT_MENU, self.OnPoleDiag, self.MenuItem_Pole)
        self.MenuItem_PoleDent = self.Menu_Proc.Append(wx.ID_EXIT, 'Dent Pole', 'Dent Pole')  # pole dent procedure
        self.MenuItem_Hybrid = self.Menu_Proc.Append(wx.ID_EXIT, 'Hybrid Deck', 'Hybrid Deck')
        self.Bind(wx.EVT_MENU, self.OnPoleDentDiag, self.MenuItem_PoleDent)
        self.Bind(wx.EVT_MENU, self.OnHybridDiag, self.MenuItem_Hybrid)
        
        
        # bind macro menu
        self.Bind(wx.EVT_MENU, self.OnMacroRecord, self.MenuItem_MacroRecord)
        self.Bind(wx.EVT_MENU, self.OnMacroStop, self.MenuItem_MacroStop)
        self.Bind(wx.EVT_MENU, self.OnMacroSave, self.MenuItem_MacroSave)
        self.Bind(wx.EVT_MENU, self.OnMacroLoad, self.MenuItem_MacroLoad)
        
        
        # bind post menu
        self.Bind(wx.EVT_MENU, self.OnPostResult, self.MenuItem_PostResults)
        self.Bind(wx.EVT_MENU, self.OnPostMarct16, self.MenuItem_PostMarcT16)
        
        
        # bind import option
        
        self.Bind(wx.EVT_MENU, self.OnImpMarcDat, self.MenuItem_ImpMarcDat)
        
        
        # Bind model tree
        self.ModelTree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeActivate)  


    
        # Bind close event to terminate the command parser process
        self.Bind(wx.EVT_CLOSE, self._when_closed)
        
    
    def _when_closed(self,event):
        self.Destroy()
        self.app.OnExit()
    
    def OnForceRefresh(self,event,model):
        self.model = model
        self.OnModelChange(event)
        
    # model tree 
    def OnTreeActivate(self,event):
        pathlist =  self.ModelTree.GetSelectionPath()
        if len(pathlist) == 0:
            p1 = FEM_3D_window(self.ModelNoteBookPanel,model=self.model)
            self.ModelNoteBook.AddPage(p1, "model")
        else:
            
            if pathlist[0] == 'setlist':           
                if len(pathlist) == 1:  # All setlist summary
                    self.OnFemSet(event)
                elif len(pathlist) == 2:  # setlist details
                    self.OnFemSetItem(event,pathlist[1])
                    
            elif pathlist[0] == 'nodelist':
                self.OnFemGrid(event)
    
            elif pathlist[0] == 'connlist':
                self.OnFemConn(event)            
                
            if pathlist[0] == 'Figure':
                self.OnAddFigurePage(pathlist[1])        

    def OnSave(self,event):
        ''' save model by pickle module '''
        wildcard = "Model Data File (*.pydat)|*.pydat|" \
         "All files (*.*)|*.*"
        
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.CHANGE_DIR
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        pub.sendMessage("COMMAND", '*save_project,%s' % paths[0])

    
    
    
    def OnImpMarcDat(self,event):
        ''' import model dat file '''
        wildcard = "MSC.Marc Data File (*.dat)|*.dat|" \
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
    
            pub.sendMessage("COMMAND", '*import_marc_dat,%s,%s' % (paths[0],'Extended'))
            pub.sendMessage("GUIREFRESH", 'model')
        

    def OnOpen(self,event):
        ''' load pickle model file '''
        wildcard = "Model Data File (*.pydat)|*.pydat|" \
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

            if self.model == None:  # not initialized yet
                self.OnNew(event)
    
            pub.sendMessage("COMMAND", '*open_project,%s' % paths[0])
            pub.sendMessage("GUIREFRESH", 'model')

        
    def OnNew(self,event):
        """ Create new model """
        #pub.sendMessage("COMMAND", '*new_project,myprj,3,6,c:/data')
        try:
            pub.sendMessage("COMMAND", '*new_project,myprj,3,6,c:/data')
            pub.sendMessage("GUIREFRESH", 'model')

        except:
            print "Created New Model Failed"
      

    def OnClose(self,event):
        try:
            self.OnSave(event)
        except:
            pass
        pub.sendMessage("COMMAND", '*close_project')        
            
    def OnUtiSection(self,event):
        """ Create sections """
        self.sectiondiag = xrcDIAG_Section(self)
        self.sectiondiag.Show()
        self.sectiondiag.Iconize(False)
        self.sectiondiag.Raise() 
        #self.OnTreeRefresh(event)        

    def OnUtiRebar(self,event):
        self.sectiondiag = xrcDIAG_Rebar(self)
        self.sectiondiag.Show()
        self.sectiondiag.Iconize(False)
        self.sectiondiag.Raise()         

        
    def OnUtiPatch(self,event):
        self.patchdiag = PatchDiag(self,self.model)
        self.patchdiag.Show()

    def OnPoleDiag(self,event):
        print "start pole data processing"
        self.polediag = PoleDiag(self)
        self.polediag.Show()
    
    def OnPoleDentDiag(self,event):
        print "start pole data processing"
        self.polediag2 = PoleDiag2(self)
        self.polediag2.Show()        

    
    def OnHybridDiag(self,event):
        print "start construct hybrid system"
        self.Hybriddiag = hybridsystem(self)
        self.Hybriddiag.Show()        
        

    def OnFemGrid(self,event):
        f1 = DictGridPanel(self.ModelNoteBook)
        f1.grid.SetRowLabelSize(100)
        f1.update(self.model.nodelist.itemlib)
        f1.grid.tableBase.colLabels = ["x","y","z"]
        self.ModelNoteBook.AddPage(f1, "Nodelist")
        
    def OnFemConn(self,event):
        f1 = DictGridPanel(self.ModelNoteBook)
        f1.grid.SetRowLabelSize(100)
        f1.update(self.model.connlist.itemlib)
        f1.grid.tableBase.colLabels = ["Node 1","Node 2","Node 3","Node 4"]
        self.ModelNoteBook.AddPage(f1, "Connectivity List")
        
    def OnFemProp(self,event):
        f1 = DictGridPanel(self.ModelNoteBook)
        f1.grid.SetRowLabelSize(100)
        f1.update(self.model.proplist)
        f1.grid.tableBase.colLabels = ["1","2","3","4","5","6","7","8"]
        self.ModelNoteBook.AddPage(f1, "Propery List")
        
    def OnFemSet(self,event):
        f1 = DictGridPanel(self.ModelNoteBook)
        f1.grid.SetRowLabelSize(300)

        f1.update(self.model.setlist)
        f1.grid.tableBase.colLabels = ["# of nodes","# of elements"]
        
        self.ModelNoteBook.AddPage(f1, "Set List:")
    
    def OnFemSetItem(self,event,itemkey):
        
        # get set
        targetset = self.model.setlist[itemkey]
        
        # if targetset.
        if len(targetset.nodelist) > 0:
            f1 = DictGridPanel(self.ModelNoteBook)
            f1.grid.SetRowLabelSize(100)
    
            f1.update(self.model.select_coordinates_setname(itemkey))
            f1.grid.tableBase.colLabels = ["x","y","z"]
            
            self.ModelNoteBook.AddPage(f1, "Node Set:%s" % itemkey)
        
        if len(targetset.elemlist) > 0:
            f1 = DictGridPanel(self.ModelNoteBook)
            f1.grid.SetRowLabelSize(100)
    
            f1.update(self.model.select_connectivity_setname(itemkey))
            f1.grid.tableBase.colLabels = ["Node 1","Node 2","Node 3","Node 4","Node 5","Node 6","Node 7","Node 8"]
            
            self.ModelNoteBook.AddPage(f1, "Element Set:%s" % itemkey)            
            

    def OnExpMarcProc(self,event):
        ''' save model by pickle module '''
        wildcard = "MSC.Marc Proc File (*.proc)|*.proc|" \
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
        
            pub.sendMessage("COMMAND", '*export_marc_proc,%s' % fullpath)  

    def OnExpMarcDat(self,event):
        ''' save model by pickle module '''
        wildcard = "MSC.Marc Proc File (*.proc)|*.proc|" \
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
        
            pub.sendMessage("COMMAND", '*export_marc_dat,%s' % fullpath)  
    
    def OnExpOpenSees(self,event):
        ''' save model in opensees format '''
        wildcard = "Opensees Tcl File (*.tcl)|*.tcl|" \
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
        
            pub.sendMessage("COMMAND", '*export_opensees_tcl,%s' % fullpath)          
    
    def OnPostResult(self,event):
        pub.sendMessage("GUIREFRESH", 'show_resultframe')
        '''
        if self.resframe == None:
            self.resframe = ResultFrame(self,self.results)
            self.resframe.Show()
        else:
            try:
                self.resframe.SetFocus()
                self.resframe.OnResChange(event)
            except:
                self.resframe = ResultFrame(self,self.results)
                self.resframe.Show()
        '''

    def OnPostMarct16(self,event):
        diag = PostDiag(self,self.results)
        diag.Show()

    def OnMacroRecord(self,event):
        pub.sendMessage("COMMAND", '*macro_start')
        self.MAIN_STATUSBAR.SetStatusText('Recording...........', 1)
        
    def OnMacroStop(self,event):
        pub.sendMessage("COMMAND", '*macro_end')
        self.MAIN_STATUSBAR.SetStatusText('Idle', 1)
        
    def OnMacroSave(self,event):
        wildcard = "Macro Recorder File (*.mac)|*.mac|" \
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
        
            pub.sendMessage("COMMAND", '*macro_save,%s' % fullpath)  
    def OnMacroLoad(self,event):
        ''' load macro file '''
        wildcard = "Macro Recorder File (*.mac)|*.mac|" \
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

            if self.model == None:  # not initialized yet
                self.OnNew(event)
    
            pub.sendMessage("COMMAND", '*macro_load,%s' % paths[0])   

        
    def OnModelChange(self,event):
        
        self.ModelTree.DeleteChildren(self.ModelTree.GetRootItem())
        
        if self.model != None:
            modeldict = self.model.generate_libdict()
            self.ModelTree.create_nodes_dict(self.ModelTree.root,modeldict)
            self.ModelTree.GetParent().Refresh()
            self.ModelTree.GetParent().SetFocus()        
    
    
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()