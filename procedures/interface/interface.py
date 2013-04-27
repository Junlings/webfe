import wx
from wx import xrc
from interface_xrc import xrcinterface
import sys
import os
import numpy as np
#from wx.lib.pubsub import Publisher as pub


from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

class interface(xrcinterface):
    def __init__(self,parent):
        xrcinterface.__init__(self,parent)
        
        self.Process.Bind(wx.EVT_LEFT_DOWN,self.OnSubmit)
    
    
    def OnSubmit(self,event):
        
        mtype = self.TYPE.GetSelection()
        La = self.PARA_La.GetValue()
        Ha = self.PARA_Ha.GetValue()
        Za = self.PARA_Za.GetValue()
        Lb = self.PARA_Lb.GetValue()
        Hb = self.PARA_Hb.GetValue()
        Zb = self.PARA_Zb.GetValue()
        Mesh_H = self.MESH_H.GetValue()
        Mesh_L = self.MESH_L.GetValue()
        
        pub.sendMessage("COMMAND", "*procedure_interface3d,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (mtype,La,Ha,Za,Lb,Hb,Zb,Mesh_L,Mesh_H))    
        
