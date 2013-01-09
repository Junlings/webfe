#!/usr/bin/env python
"""
a generic frame class that will create the GUI based on the parameter:settings
support
  a) Menubar
  b) Toolbar
  c) Status bar
  
  Usually, need to define derived class with event handing functions mentioned  in the settings dictionary
"""
import wx
import os
iconfolder = os.path.join(os.path.realpath(__file__),'icon')

class GenericFrameSimple(wx.Frame):
    def __init__(self, parent, id, settings={'title':'Title','size':(500,500)}):
        self.settings = settings        
        wx.Frame.__init__(self, parent, id, title=self.settings['title'], size=self.settings['size'])
        
        # bind close event
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
        # create components
        self.createMenuBar()
        self.createToolBar()
        self.initStatusBar()


    ### create menu bar based on the predefined data
    def createMenuBar(self):
        if 'menuData' in self.settings.keys():
            menuBar = wx.MenuBar()
            for eachMenuData in self.settings['menuData']:
                menuLabel = eachMenuData[0]
                menuItems = eachMenuData[1:]
                menuBar.Append(self.createMenu(menuItems), menuLabel)
            self.SetMenuBar(menuBar)
            

    
    def createMenu(self, menuData):
        
        menu = wx.Menu()
        for eachLabel, eachStatus, eachHandler in menuData:
            if not eachLabel:
                menu.AppendSeparator()
                continue
            menuItem = menu.Append(-1, eachLabel, eachStatus)
            
            eachHandler=getattr(self,eachHandler)  ## here convert the string function name to the function attr
            self.Bind(wx.EVT_MENU, eachHandler, menuItem)
        return menu

    
    def createToolBar(self):
        if 'toolbarData' in self.settings.keys() != None:
            
            if self.settings['toolbarData']['Mode'] == 'VERTICAL':
                toolbar = self.CreateToolBar(wx.TB_VERTICAL)
            elif self.settings['toolbarData']['Mode'] == 'HORIZONTAL':
                toolbar = self.CreateToolBar(wx.TB_HORIZONTAL)
            else:
                print 'please identify the toolbar mode'
            
            for eachLabel, eachHandler,eachimage in self.settings['toolbarData']['Data']:
                self.buildOnetoolButton(toolbar,eachLabel, eachHandler,eachimage)
                
            toolbar.Realize()
            
    def buildOnetoolButton(self,toolbar,eachLabel, eachHandler,eachimage):
        toolbutton=toolbar.AddLabelTool(wx.ID_ANY, '', wx.Bitmap(eachimage))
        handler=getattr(self,eachHandler)
        self.Bind(wx.EVT_MENU, handler, toolbutton)

    
    ### ==========setup status bar
    def initStatusBar(self):
        if 'statusbar' in self.settings.keys():
            if self.settings['statusbar'] != None:
                self.statusbar = self.CreateStatusBar()
                self.statusbar.SetFieldsCount(len(self.settings['statusbar']))
                self.statusbar.SetStatusWidths(self.settings['statusbar'])

    def OnCloseWindow(self, event):
        self.Destroy()

   
if __name__ == '__main__':
    settings = {'title':'my Title','size':(500,500)}
    settings['menuData']=(("&File",
                            ("&Add", "Add", 'OnCloseWindow'),
                            ("&Edit", "Clear database", 'OnCloseWindow')),
                       ("&Export",
                            ("&to csv", "Export to csv", 'OnCloseWindow')
                            )
                )
    
    settings['statusbar']=[-1,-1,-1]   
    settings['toolbarData'] = {'Mode':'HORIZONTAL',
                               'Data':[
                                  ('aa','OnCloseWindow',os.path.join(iconfolder,'apply.png')),
                                  ('bb','OnCloseWindow',os.path.join(iconfolder,'icons/Prop.png'))
                                ]}
    
    app = wx.PySimpleApp()
    GenericFrameSimple(None,-1,settings).Show()
    app.MainLoop()
    
    