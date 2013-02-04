#!/usr/bin/python
# -*- coding: utf-8 -*-

# calculator.py
import wx
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
import random 
class SelRadioButton(wx.RadioButton):
    def __init__(self,parent,skey=None):
        super(SelRadioButton, self).__init__(parent)
        self.key = skey


class SelCheckButton(wx.CheckBox):
    def __init__(self,parent,skey=None):
        super(SelCheckButton, self).__init__(parent, style=wx.SHAPED)
        self.key = skey
        
class PlotDataFrame(wx.Frame):
    def __init__(self,parent,contlist=None,title='Create Plot Data'):
        size = (-1,150 + 30*len(contlist))
        
        super(PlotDataFrame, self).__init__(parent,size=size,title=title,style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        Example(self,contlist)
        self.Show()
        
        
class Example(wx.Panel):
  
    def __init__(self, parent,contlist):
        
        super(Example, self).__init__(parent)
        
        cont = self.create_list(contlist)
        self.InitUI(cont)
        #self.Centre()
        self.BTN_OK.Bind(wx.EVT_LEFT_DOWN,self.OnSubmit)
        self.BTN_Reset.Bind(wx.EVT_LEFT_DOWN,self.OnReset)
        self.BTN_QUICKPL.Bind(wx.EVT_LEFT_DOWN,self.OnQuickPlot)

    
    def create_list(self,inputlist):
        cont =[]
        self.control = {}
        axislist = ['x%i Axis' % i for i in range(1,11)]
        self.results = {}
        for item in axislist:
            self.results[item] = {'x':None,'y':[]}
            
        cont.append((wx.StaticText(self, label='Table Name',style=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL), 0, wx.EXPAND))
        cont.append((wx.StaticText(self, label='Column Name',style=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL), 0, wx.EXPAND))
        self.xchoice = wx.Choice(self, choices=axislist)
        self.xchoice.SetStringSelection(axislist[0])
        cont.append((self.xchoice, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL))
        cont.append((wx.StaticText(self, label='y Axis',style=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL), 0, wx.EXPAND))
        self.xchoice.Bind(wx.EVT_CHOICE, self.OnXChoice)
        
        for item in inputlist:
            item_a,item_b = item.split(':')
            ilabel_a = wx.StaticText(self, label=item_a)
            ilabel_b = wx.StaticText(self, label=item_b)
            
            iradio = SelRadioButton(self, skey=item)
            icheck = SelCheckButton(self, skey=item)
            
            cont.append((ilabel_a, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL))
            cont.append((ilabel_b, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL))
            cont.append((iradio, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL))
            cont.append((icheck, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL))
            
            self.control[item] = {'label_a':ilabel_a,'label_b':ilabel_b,'radio':iradio,'check':icheck}
            
            self.Bind(wx.EVT_RADIOBUTTON,self.SelectRadioButton,iradio)
            self.Bind(wx.EVT_CHECKBOX,self.SelectCheckButton,icheck)
        return cont
        
    def SelectRadioButton(self,event):
        xasix = self.xchoice.GetStringSelection()
        
        self.results[xasix]['x'] = event.GetEventObject().key
        #print self.results
    
    def SelectCheckButton(self,event):
        xasix = self.xchoice.GetStringSelection()
        icheckbox = event.GetEventObject()
        if event.IsChecked():
            if icheckbox.key in self.results[xasix]['y']:
                pass
            else:
                self.results[xasix]['y'].append(icheckbox.key)
            
        else:
            if icheckbox.key in self.results[xasix]['y']:
                self.results[xasix]['y'].remove(icheckbox.key)
            else:
                pass        
            
        #print self.results
    
    def OnXChoice(self,event):
        xasix = self.xchoice.GetStringSelection()
        if self.results[xasix]['x'] != None:
            for key,item in self.control.items():
                if item['radio'].key == self.results[xasix]['x']:
                    item['radio'].SetValue(True)
                else:
                    item['radio'].SetValue(False)
        else:
            for key,item in self.control.items():
                item['radio'].SetValue(False)            
                
        if len(self.results[xasix]['y']) > 0:
            for key,item in self.control.items():
                if item['check'].key in self.results[xasix]['y']:
                    item['check'].SetValue(True)
                else:
                    item['check'].SetValue(False)
        else:
            for key,item in self.control.items():
                item['check'].SetValue(False)          
        
    def OnReset(self,event):
        xasix = self.xchoice.GetStringSelection()
        for key,item in self.control.items():
            item['radio'].SetValue(False)                            
            item['check'].SetValue(False)            
        
        self.results[xasix]['x'] = None
        self.results[xasix]['y'] = []
        
    def InitUI(self,cont):
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        ntotal = len(cont)
        nrow = ntotal/4+1
        
        gs = wx.FlexGridSizer(nrow, 4, 5, 5)

        gs.AddMany(cont)
        gs.AddGrowableCol(0, 1)
        gs.AddGrowableCol(1, 2)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(gs, proportion=1, flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL,border=5)
        vbox.Add(hbox1,border=5)#, flag=wx.ALIGN_CENTER)
        vbox.Add(hbox2,border=5)#, flag=wx.ALIGN_CENTER)
        
        self.BTN_OK = wx.Button(self,label='OK')
        self.BTN_Reset = wx.Button(self,label='Reset')
        self.BTN_QUICKPL = wx.Button(self,label='QUICK Plot')
        self.Pdatakeylabel = wx.StaticText(self,label='Plot Data Key')
        self.Pdatakey = wx.TextCtrl(self,size=(150,20))
        hbox1.Add(self.Pdatakeylabel)# , flag=wx.ALIGN_CENTER)
        hbox1.Add(self.Pdatakey)# , flag=wx.ALIGN_CENTER)
        
        hbox2.Add(self.BTN_Reset)#, flag=wx.ALIGN_CENTER)
        hbox2.Add(self.BTN_QUICKPL)#, flag=wx.ALIGN_CENTER)
        hbox2.Add(self.BTN_OK)#, flag=wx.ALIGN_CENTER)
        self.SetSizer(vbox)

    def OnSubmit(self,event):
        #print self.results
        plotkey = self.Pdatakey.GetValue()
        if len(plotkey) == 0 :
            plotkey = 'plot' + '_' + str(random.randint(1, 10000))
            
        for key,item in self.results.items():
            reqlist = []
            
            if item['x'] != None and len(item['y']) > 0:
                reqlist.append(str(item['x']))
                for ylabel in item['y']:
                    reqlist.append(str(ylabel))
                
                com = ''
                for req in reqlist:
                    com += ',%s' % req
                pub.sendMessage("COMMAND", "*plot_pdata_add,%s%s" % (plotkey,com))
                
        self.plotkey = plotkey
        #self.Destroy()
    
    def OnQuickPlot(self,event):
        self.OnSubmit(event)
        fname = self.plotkey
        pdataname = self.plotkey 
        pub.sendMessage("COMMAND", '*plot_figure_add,%s,%s,%s,%s' % (fname,pdataname,'publish','line-one axis'))
        
        # =============== show figure
        #pub.sendMessage("GUIREFRESH", 'show_figure:%s' % fname)
        #pub.sendMessage("GUIREFRESH", 'results')
        self.Parent.Destroy()
if __name__ == '__main__':
  
    app = wx.App()
    PlotDataFrame(None,contlist=['a','b','c','d','e'])
    app.MainLoop()