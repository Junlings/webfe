#!/usr/bin/env python
"""
provide the abstracted wxpanel class, by feed the GUI data structure and data class
separatly
"""
import wx



    

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
    
    
      

class GenericPanel(wx.Panel):
    """
    a generic panel class that will create the GUI based on the parameter generated
    function is to create view and identify each GUI component
    """
    def __init__(self,parent,Paneldata,id,size=(400,400),pos=(100,100)):
        """
        obj: handle
        Paneldata: GUI data structure for panel
        id: panel id
        size: panel size
        pos: panel position
        """
        self.GUIdata = Paneldata
        wx.Panel.__init__(self, parent, id,size=size,pos=pos)
        
      
        
        self.TextCtrl = {}
        self.createButtonBar(self)
        self.createTextFields(self)
        self.createStaticText(self)
        
        self.GUIdata.set_textctrl(self.TextCtrl)
        
        '''
        ##Check box
        wx.CheckBox(self, -1, "Alpha", (235, 40), (150, 20))
        wx.CheckBox(self, -1, "Beta", (235, 60), (150, 20))
        wx.CheckBox(self, -1, "Gamma", (235, 80), (150, 20))
        
    
        ##Radio box
        sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
        'six', 'seven', 'eight']
        wx.RadioBox(self, -1, "A Radio Box", (10, 200), wx.DefaultSize,
        sampleList, 2, wx.RA_SPECIFY_COLS)
        
        ## list box
        sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
        'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
        'twelve', 'thirteen', 'fourteen']
        listBox = wx.ListBox(self, -1, (220, 220), (80, 120), sampleList,
        wx.LB_SINGLE)
        listBox.SetSelection(3)
        
        ## pulldownlist box
        sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
        'six', 'seven', 'eight']
        wx.StaticText(self, -1, "Select one:", (15, 20))
        wx.Choice(self, -1, (285, 218), choices=sampleList)
        '''
        
    
    ### create the button bar based on the predefined data
    
    def createButtonBar(self, panel, yPos = 0):
        if self.GUIdata.buttonbarData!=None:
            xPos = 0
            for eachLabel, eachHandler in self.GUIdata.buttonbarData:
                pos = (xPos, yPos)
                button = self.buildOneButton(panel, eachLabel, eachHandler, pos)
                xPos += button.GetSize().width
            
    def buildOneButton(self, parent, label, handler, pos=(0,0)):
        button = wx.Button(parent, -1, label, pos)
        handler=getattr(self.GUIdata,handler)
        self.Bind(wx.EVT_BUTTON, handler, button)
        return button
    
    ### ==========setup text field
    def createTextFields(self, panel):
        if self.GUIdata.textFieldData!=None:
            for eachLabel, eachPos in self.GUIdata.textFieldData:
                self.createCaptionedText(panel, eachLabel, eachPos)
    
    def createCaptionedText(self, panel, label, pos):
        static = wx.StaticText(panel, wx.NewId(), label, pos)
        #static.SetBackgroundColour("White")
        textPos = (pos[0] + 75, pos[1])
        self.TextCtrl[label] = wx.TextCtrl(panel, wx.NewId(), "", size=(100, -1), pos=textPos)

    
    def createStaticText(self, panel):
        if self.GUIdata.StaticText!=None:
            for eachLabel, eachPos in self.GUIdata.StaticText:
                #self.textFields[eachLabel]=self.createCaptionedText(panel, eachLabel, eachPos)
                static = wx.StaticText(panel, wx.NewId(), eachLabel, eachPos)
                static.SetBackgroundColour("White")


    ###==========setuo sketch
class MyPanel_Dict(GenericPaneldata):
    """
    Panel based on dictionary datasource,
    Automatic create the GUI textctrl field and then provide global load and update function
    """
    def __init__(self,data):
        GenericPaneldata.__init__(self)
        self.buttonbarData = (("Load", 'OnLoad'),("Update", 'OnUpdate'))
        self.datasource = data
        
    def OnLoad(self,event):
        self.Set_value_all()
    
    def OnUpdate(self,event):
        self.Get_value_all()
            
if __name__ == '__main__':
    
    from generic_plot import *
    from generic_opengl import *
    import sys
    sys.path.append('../..')
    from FEA.prj.project import *
  
    def DataFresh():
        datax = list([data1['aa'],data1['bb'],data1['cc'],data1['dd']])
        datay = list([data2['aa'],data2['bb'],data2['cc'],data2['dd']])
        return datax,datay
    
    data1 = {}
    data1['aa'] = 1
    data1['bb'] = 20
    data1['cc'] = 29
    data1['dd'] = 28
 
    data2 = {}
    data2['aa'] = 1
    data2['bb'] = 200
    data2['cc'] = 290
    data2['dd'] = 280   
    
    panel1= MyPanel_Dict(data1)
    panel1.create_TextCtrl_dict(data1,(100,50),(0,25))

    panel2= MyPanel_Dict(data2) 
    panel2.create_TextCtrl_dict(data2,(100,50),(0,25))   
    
    app = wx.PySimpleApp()

    top = wx.Frame(None, title='title')
    box = wx.BoxSizer(wx.HORIZONTAL)
    
    p1 = GenericPanel(top,panel1,-1)
    p2 = GenericPanel(top,panel2,-1)
    
    myplot1 = baseplot()
    plotframe = CanvasFrame(None,plot=myplot1)
    myplot1.DataFresh = DataFresh
    
    
    
    prj1 = lib.load('uhpc','22')
  
    coordlist =  prj1.coordlist[1]
    connlist = prj1.connlist[1]
    openglframe = Model3dFrame(title='title',coordlist=coordlist,connlist=connlist)
    
    box.Add(p1, 1,wx.EXPAND)
    box.Add(p2, 1,wx.EXPAND)  
    
    
    top.SetAutoLayout(True)
    top.SetSizer(box)
    top.Layout()
    top.Show()
    
    app.MainLoop()
    