import wx
from patch_xrc import xrc2DPatch
#from wx.lib.pubsub import Publisher as pub
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
import sys
sys.path.append('../../webfe')



class PatchDiag(xrc2DPatch):
    def __init__(self,parent,model):
        xrc2DPatch.__init__(self,parent)
        self.model = model
        self.BTN_APPLY_Line.Bind(wx.EVT_LEFT_UP,self.OnApplyLine)
        self.BTN_APPLY_CYL.Bind(wx.EVT_LEFT_UP,self.OnApplyCyl)    
    
    
    def OnApplyLine(self,event):pass
    
    def OnApplyCyl(self,event):
        
        x0 = self.PATCH_CYL_X0.GetValue()
        y0 = self.PATCH_CYL_Y0.GetValue()
        z0 = self.PATCH_CYL_Z0.GetValue()
        r0 = self.PATCH_CYL_R0.GetValue()
        r1 = self.PATCH_CYL_R1.GetValue()
        L = self.PATCH_CYL_L.GetValue()
        nfi = self.PATCH_CYL_NF.GetValue()
        nZ  = self.PATCH_CYL_NZ.GetValue()



        
                                #model1,x0,y0,z0,R1,R2,L,nfi,nL
        #self.model = create_cylinderSurface(self.model,x0,y0,z0,r0,r1,L,nfi,nZ)
        command = '*create_cylinderSurface,%(x0)s,%(y0)s,%(z0)s,%(r0)s,%(r1)s,%(L)s,%(nfi)s,%(nZ)s' % {
                    'x0' : x0,
                    'y0' : y0,
                    'z0' : z0,
                    'r0' : r0,
                    'r1' : r1,
                    'L' : L,
                    'nfi' : nfi,
                    'nZ' : nZ }

        
        pub.sendMessage("COMMAND", command)
                
        self.Destroy()