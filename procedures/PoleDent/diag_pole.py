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
        
        self.POLE_EXTEND_CHECK  # here need to bind check box to show/hide of extension inputs

    def OnPoleSubmit(self,event):
        
        fullpath = self.PoleFile.GetValue()
        dentperc = self.SLIDE_DENTPER.GetValue()
        domodeling = self.CHECK_MONPROC.GetValue()
        dobendmodeling = self.CHECK_BENDPROC.GetValue()
        rightend_xcoord = self.RIGHTEND_XCOORD.GetValue()
        leftend_xcoord = self.LEFTEND_XCOORD.GetValue()
        
        ifextend = self.POLE_EXTEND_CHECK.GetValue()
        if ifextend:
            pub.sendMessage("COMMAND", "*procedure_poledent,%s,%s,%s,%s,%s,%s" % (fullpath,dentperc,domodeling,dobendmodeling, rightend_xcoord,leftend_xcoord))
        else:
            pub.sendMessage("COMMAND", "*procedure_poledent,%s,%s,%s,%s" % (fullpath,dentperc,domodeling,dobendmodeling))
        
        
        
        self.Destroy()
    
    
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
