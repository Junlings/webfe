import wx
from post_t16_xrc import xrcFRAME1
#from wx.lib.pubsub import Publisher as pub
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
import sys
sys.path.append('../../webfe')
import random
from quickplot.loaddisp.loaddisp import ldframe
from quickplot.loadstressstrain.loadstressstrain import lssframe

class PostDiag(xrcFRAME1):
    def __init__(self,parent,results):
        xrcFRAME1.__init__(self,parent)
        self.results = results
        
        self.POST_t16_Open.Bind(wx.EVT_LEFT_DOWN,self.OnOpen)
        self.POST_t16_Apply.Bind(wx.EVT_LEFT_DOWN,self.OnApply)
        self.POST_t16_Submit.Bind(wx.EVT_LEFT_DOWN,self.OnSubmit)
        
        self.POST_t16_ItemType.Bind(wx.EVT_CHOICE, self.OnChoice1)
        self.POST_t16_Incr.Bind(wx.EVT_CHOICE, self.OnChoiceIncr)
        
        self.POST_t16_QP_LD.Bind(wx.EVT_LEFT_DOWN,self.OnQPLD)
        self.POST_t16_QP_LSTRESS.Bind(wx.EVT_LEFT_DOWN,self.OnQPLSS)
        
        #self.BTN_APPLY_CYL.Bind(wx.EVT_LEFT_UP,self.OnApplyCyl)    
        
        if 'marc_t16' in self.results.source.keys():
            if self.results.source['marc_t16']['file'] != None:
                self.POST_t16_File.SetValue(self.results.source['marc_t16']['file'])
    
    
    def OnChoiceIncr(self,event):
        selected = self.POST_t16_Incr.GetStringSelection()
        if selected == 'ALL' or selected == 'First' or selected == 'Last':
            self.POST_OPTION3.Clear()
            self.POST_OPTION3.Enable(False)
            
        elif selected == 'Every':
            self.POST_OPTION3.Clear()
            self.POST_OPTION3.AppendItems(['2','5','10',])
            self.POST_OPTION3.Enable(True)
            
        elif selected == 'Particular':
            self.POST_OPTION3.Clear()
            if len(self.results.source['marc_t16']['handler'].increment_str) == 0:
                self.results.source['marc_t16']['handler'].disp_increment_str()
            self.POST_OPTION3.AppendItems(self.results.source['marc_t16']['handler'].increment_str)
            self.POST_OPTION3.Enable(True)
            

    
    def EnabelDisablePanel2(self,option=False):
        self.POST_t16_ItemSelSingle.Enable(option)
        self.POST_t16_ItemSingle.Enable(option)
        self.POST_t16_ItemSelList.Enable(option)
        self.POST_t16_ItemList.Enable(option)
        self.POST_t16_ItemSelSet.Enable(option)
        self.POST_t16_ItemSet.Enable(option)
    
    def OnChoice1(self,event):
        
        selected = self.POST_t16_ItemType.GetStringSelection()
        self.POST_t16_Request.Clear()
        
        if selected == 'Time':
            self.POST_OPTION1.Enable(True)
            self.POST_OPTION1.SetValue('1')
            self.POST_OPTION2.Enable(False)
            self.POST_t16_Request.Enable(False)
            self.EnabelDisablePanel2(False)
            
        elif selected == 'Node Scalar':
            self.POST_OPTION1.Enable(False)
            self.POST_OPTION2.Enable(False)
            self.POST_t16_Request.Enable(True)
            sellist = self.results.source['marc_t16']['handler'].nodescalarlib.keys()
            sellist.sort()
            self.POST_t16_Request.AppendItems(sellist)
            self.EnabelDisablePanel2(True)
            
        elif selected == 'Element Scalar':
            self.POST_OPTION1.Enable(False)
            self.POST_OPTION2.Enable(True)
            self.POST_OPTION2.SetValue('0')
            self.POST_t16_Request.Enable(True)
            self.EnabelDisablePanel2(True)
            
            sellist = self.results.source['marc_t16']['handler'].elemscalarlib.keys()
            sellist.sort()
            self.POST_t16_Request.AppendItems(sellist)       
        else:
            print "Error"
            
    def OnOpen(self,event):
        ''' load pickle model file '''
        wildcard = "Model Data File (*.t16)|*.t16|" \
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
                
                
            pub.sendMessage("COMMAND", "*post_marc_t16_open,%s" % paths[0])
            #self.POST_t16_File.setValue(self.results.source['marc_t16'])
            
            self.POST_t16_File.SetValue(paths[0])
            self.POST_t16_ItemSet.Clear()
            self.POST_t16_ItemSet.AppendItems(self.results.source['marc_t16']['handler'].setlib.keys())  
            
            
    def OnApply(self,event):
        
        itemtype = self.POST_t16_ItemType.GetStringSelection()
        selected = self.POST_t16_Request.GetStringSelection()
        ninc = self.POST_t16_Incr.GetStringSelection()
        tablename = self.POST_t16_TableName.GetValue()
        target = ''
        option1 = self.POST_OPTION1.GetValue()
        option2 = self.POST_OPTION2.GetValue()
        option3 = self.POST_OPTION3.GetStringSelection()
        
        # cleanup target list
        if self.POST_t16_ItemSelSingle.GetValue() == True:
            target = self.POST_t16_ItemSingle.GetValue()
        
        if self.POST_t16_ItemSelList.GetValue() == True:
            target = self.POST_t16_ItemList.GetValue()
            
        if self.POST_t16_ItemSelSet.GetValue() == True:
            target = self.POST_t16_ItemSet.GetStringSelection()
        
        # cleanup table name
        if len(tablename) == 0:
            tablename = itemtype + '_' + str(random.randint(1, 10000))
        
        # cleanup the increment
        
        if ninc == 'ALL':
            nincstr = '-1,1e6,1'
        elif ninc == 'Every':
            option3_clean = option3
            nincstr = '-1,1e6,' + option3_clean
        elif ninc == 'First':
            nincstr = '1,1,1'
        elif ninc == 'Last':
            nincstr = '1e6,1e6,1'
        elif ninc == 'Particular':
            option3_clean = option3.split(':')[0].split(' ')[1]
            nincstr = '%s,%s,1' % (option3_clean,option3_clean)
        else:
            print ninc,'not defined'
        
        # generate the request item
        if itemtype == 'Time':
            command = "%s,%s,%s,%s" % (tablename,itemtype,option1,nincstr)
        
        elif itemtype == 'Node Scalar':
            command = "%s,%s,%s,%s,%s" % (tablename,itemtype,selected,target,nincstr)
        
        elif itemtype == 'Element Scalar':
            command = "%s,%s,%s,%s,%s,%s" % (tablename,itemtype,selected,option2,target,nincstr)
            
        pub.sendMessage("COMMAND", '*post_marc_t16_addrequest,%s' % command)
        
        self.POST_RequestList.InsertItems([command],0)
        #self.Destroy()
        self.SetFocus()
        
    def OnSubmit(self,event):
        pub.sendMessage("COMMAND", '*post_marc_t16_getdata')
    
    
    def OnQPLD(self,event):
        myldframe = ldframe(self).Show()
        
    def OnQPLSS(self,event):
        myldframe = lssframe(self).Show()        