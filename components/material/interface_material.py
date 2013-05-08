import wx
from wx import xrc
from interface_material_xrc import xrcInterfaceMaterial

import sys
import os
import numpy as np
#from wx.lib.pubsub import Publisher as pub


from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

class MatInterfaceDiag(xrcInterfaceMaterial):
    def __init__(self,parent):
        xrcInterfaceMaterial.__init__(self,parent)
        
        self.PoleProcess.Bind(wx.EVT_LEFT_UP,self.OnPoleSubmit)

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
    

