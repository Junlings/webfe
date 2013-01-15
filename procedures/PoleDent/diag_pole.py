import wx
from wx import xrc
from Pole_diag_xrc import xrcPoleDiag

import sys
import os
import numpy as np
#from wx.lib.pubsub import Publisher as pub


from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

class PoleDiag(xrcPoleDiag):
    def __init__(self,parent):
        xrcPoleDiag.__init__(self,parent)
        
        self.PoleProcess.Bind(wx.EVT_LEFT_UP,self.OnPoleSubmit)
        self.PoleSelectFile.Bind(wx.EVT_LEFT_UP,self.OnFileSelect)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnExtend, self.IF_EXTEND)
        self.Bind(wx.EVT_CHECKBOX, self.OnProc, self.IF_PROCEDURE )
        
        self.Bind(wx.EVT_RADIOBUTTON,self.FourPointCheck,self.CHECK_BENDPROC)
        self.Bind(wx.EVT_RADIOBUTTON,self.BendCheck,self.CHECK_MONPROC)
        
        self.RIGHTEND_XCOORD.Enable(False)
        self.LEFTEND_XCOORD.Enable(False)
        self.LENGTH_INCR.Enable(False)
        self.CHECK_MONPROC.Enable(False)
        self.CHECK_BENDPROC.Enable(False)              
        self.PARA_leftsupportx.Enable(False)   
        self.PARA_rightsupportx.Enable(False)   
        self.PARA_supporty.Enable(False)   
        self.PARA_leftplatecenterx.Enable(False)   
        self.PARA_rightplatecenterx.Enable(False)   
        self.PARA_plateheighty.Enable(False)   
        self.PARA_lengthx.Enable(False)   
        self.PARA_heighty.Enable(False)   
        self.PARA_stiffness.Enable(False)   
    
    def BendCheck(self,event):
        self.PARA_leftsupportx.Enable(False)   
        self.PARA_rightsupportx.Enable(False)   
        self.PARA_supporty.Enable(False)   
        self.PARA_leftplatecenterx.Enable(False)   
        self.PARA_rightplatecenterx.Enable(False)   
        self.PARA_plateheighty.Enable(False)   
        self.PARA_lengthx.Enable(False)   
        self.PARA_heighty.Enable(False)   
        self.PARA_stiffness.Enable(False)         
        
    def FourPointCheck(self,event):
        self.PARA_leftsupportx.Enable(True)   
        self.PARA_rightsupportx.Enable(True)     
        self.PARA_supporty.Enable(True)    
        self.PARA_leftplatecenterx.Enable(True)      
        self.PARA_rightplatecenterx.Enable(True)     
        self.PARA_plateheighty.Enable(True)      
        self.PARA_lengthx.Enable(True)      
        self.PARA_heighty.Enable(True)      
        self.PARA_stiffness.Enable(True)             
        
    def OnExtend(self,event):
        if self.IF_EXTEND.IsChecked():
            self.RIGHTEND_XCOORD.Enable(True)
            self.LEFTEND_XCOORD.Enable(True)
            self.LENGTH_INCR.Enable(True)
        else:
            self.RIGHTEND_XCOORD.Enable(False)
            self.LEFTEND_XCOORD.Enable(False)
            self.LENGTH_INCR.Enable(False)
    
    def OnProc(self,event):
        if self.IF_PROCEDURE.IsChecked():
            self.CHECK_MONPROC.Enable(True)
            self.CHECK_BENDPROC.Enable(True)

        else:
            self.CHECK_MONPROC.Enable(False)
            self.CHECK_BENDPROC.Enable(False)       
    
    def OnPoleSubmit(self,event):
        
        fullpath = self.PoleFile.GetValue()
        dentperc = self.SLIDE_DENTPER.GetValue()
        procname = ''
        if self.CHECK_MONPROC.GetValue() == True:
            procname = 'curvature'
        if self.CHECK_BENDPROC.GetValue() == True:
            procname = 'fullbending'

        rightend_xcoord = self.RIGHTEND_XCOORD.GetValue()
        leftend_xcoord = self.LEFTEND_XCOORD.GetValue()
        incrlength = self.LENGTH_INCR.GetValue()
        ifextend = self.IF_EXTEND.IsChecked()
        
        self.Hide()
        
        if ifextend:
            pub.sendMessage("COMMAND", "*procedure_poledent,%s,%s,%s,%s,%s,%s" % (fullpath,dentperc,procname, rightend_xcoord,leftend_xcoord,incrlength))
        else:
            pub.sendMessage("COMMAND", "*procedure_poledent,%s,%s,%s" % (fullpath,dentperc,procname))
        
        
        if procname == 'fullbending':
            pub.sendMessage("COMMAND", "*procedure_poledent_fourpoint,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
                self.PARA_leftsupportx.GetValue(),
                self.PARA_rightsupportx.GetValue(),     
                self.PARA_supporty.GetValue(),  
                self.PARA_leftplatecenterx.GetValue(),
                self.PARA_rightplatecenterx.GetValue(),
                self.PARA_plateheighty.GetValue(),
                self.PARA_lengthx.GetValue(),
                self.PARA_heighty.GetValue(),
                self.PARA_stiffness.GetValue())  
            )
        
        #self.Destroy()
    
    
    def OnFileSelect(self,event):
        wildcard = "Marc Data File (*.dat)|*.dat|" \
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
                
        self.PoleFile.SetValue(paths[0])
        dlg.Destroy()  
