import wx
from wx import xrc
from hybridsystem_xrc import xrchybrid
import sys
import os
import numpy as np
#from wx.lib.pubsub import Publisher as pub


from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

class hybridsystem(xrchybrid):
    def __init__(self,parent):
        xrchybrid.__init__(self,parent)
        
        self.PoleProcess.Bind(wx.EVT_LEFT_DOWN,self.OnPoleSubmit)
    
    
    def OnPoleSubmit(self,event):
        H = self.PARA_H.GetValue()
        B = self.PARA_B.GetValue()
        t1 = self.PARA_t1.GetValue()
        t2 = self.PARA_t2.GetValue()
        b3 = self.PARA_b3.GetValue()
        a = self.PARA_a.GetValue()
        L = self.PARA_L.GetValue()
        Mesh_H = self.MESH_H.GetValue()
        Mesh_B = self.MESH_B.GetValue()
        Mesh_L = self.MESH_L.GetValue()
        
        pub.sendMessage("COMMAND", "*procedure_hybriddeck,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (H,B,t1,t2,b3,a,L,Mesh_H,Mesh_B,Mesh_L))    
        
