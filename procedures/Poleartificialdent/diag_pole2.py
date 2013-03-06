import wx
from wx import xrc
from Pole_diag2_xrc import xrcPoleDiag

import sys
import os
import numpy as np
#from wx.lib.pubsub import Publisher as pub


from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

class PoleDiag2(xrcPoleDiag):
    def __init__(self,parent):
        xrcPoleDiag.__init__(self,parent)
        
        #self.PoleProcess.Bind(wx.EVT_LEFT_UP,self.OnPoleSubmit)
        #self.Destroy()
        self.PoleProcess.Bind(wx.EVT_LEFT_DOWN,self.OnPoleSubmit)
    
    
    def OnPoleSubmit(self,event):
        
        DEEP_DENT = self.DEEP_DENT.GetValue()
        CRIT_LENGTH = self.CRIT_LENGTH.GetValue()
        RIGHTEND_XCOORD = self.RIGHTEND_XCOORD.GetValue()
        RIGHTEND_RAD = self.RIGHTEND_RAD.GetValue()
        LEFTEND_XCOORD = self.LEFTEND_XCOORD.GetValue()
        LEFTEND_RAD = self.LEFTEND_RAD.GetValue()
        LENGTH_INCR = self.LENGTH_INCR.GetValue() 
        LENGTH_RAd = self.LENGTH_RAd.GetValue() 
        LENGTH_RAd = self.LENGTH_RAd.GetValue() 
        if self.NEEDFILL.GetValue():
            NEEDFILL = 'True'
        else:
            NEEDFILL = 'False'

        if self.NEEDWRAP.GetValue():
            NEEDWRAP = 'True'
            WRAPLEFT = self.WRAPLEFT.GetValue() 
            WRAPRIGHT = self.WRAPRIGHT.GetValue() 
        else:
            NEEDWRAP = 'False'            
            WRAPLEFT = 'n/a'
            WRAPRIGHT = 'n/a'           
        
        pub.sendMessage("COMMAND", "*procedure_pole_imposedent,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (LEFTEND_XCOORD,RIGHTEND_XCOORD,
                                                                                                       LEFTEND_RAD,RIGHTEND_RAD,
                                                                                                       LENGTH_INCR,LENGTH_RAd,
                                                                                                       DEEP_DENT,CRIT_LENGTH,
                                                                                                       NEEDFILL,
                                                                                                       NEEDWRAP,WRAPLEFT,WRAPRIGHT))
  
        #self.PARA_leftplatecenterx
        #self.PARA_rightplatecenterx
        #self.PARA_plateheighty
        #self.PARA_lengthx
        #self.PARA_heighty
        #self.PARA_stiffness