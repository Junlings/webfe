from loaddisp_xrc import xrcLDFRAME
import wx
import random
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

class ldframe(xrcLDFRAME):
    def __init__(self,parent):
        xrcLDFRAME.__init__(self,parent)
        
        self.LD_LOAD_SOURCE.Bind(wx.EVT_RADIOBOX, self.OnLoadChoice)
        
        self.POST_LD_QUICKPLOT.Bind(wx.EVT_LEFT_DOWN,self.POST_LD_QUICKPLOT_Submit)

        self.source_L = [self.POST_L_ItemSelSingle,
                         self.POST_L_ItemSingle,
                         self.POST_L_ItemSelList,
                         self.POST_L_ItemList,
                         self.POST_L_ItemSelSet ,
                         self.POST_L_ItemSet,
                         self.POST_L_ItemSourceLabel,
                         self.POST_L_ItemSource]
        
        for item in self.source_L:
            item.Enable(False)
            
    def OnLoadChoice(self,event):
        selected = self.LD_LOAD_SOURCE.GetStringSelection()
        print selected
        if selected == 'Load from time':
            for item in self.source_L:
                item.Enable(False)
        else:
            for item in self.source_L:
                item.Enable(True)
    
    def POST_LD_QUICKPLOT_Submit(self,event):
        nincstr = '-1,1e6,1'
        option1 = '1'
        
        # ========process load command
        loadsource = self.LD_LOAD_SOURCE.GetStringSelection()
        if loadsource == 'Load from time':
            itemtype = 'Time'
            ltablename = itemtype + '_' + str(random.randint(1, 10000))
            lcommand = "%s,%s,%s,%s" % (ltablename,itemtype,option1,nincstr)
        
        else:
            itemtype = 'Node Scalar'
            selected = self.POST_L_ItemSource.GetStringSelection()

        # cleanup target list
            if self.POST_L_ItemSelSingle.GetValue() == True:
                target = self.POST_L_ItemSingle.GetValue()
            
            if self.POST_L_ItemSelList.GetValue() == True:
                target = self.POST_L_ItemList.GetValue()
                
            if self.POST_L_ItemSelSet.GetValue() == True:
                target = self.POST_L_ItemSet.GetStringSelection()
                
            ltablename = itemtype + '_' + str(random.randint(1, 10000))
            lcommand = "%s,%s,%s,%s,%s" % (ltablename,itemtype,selected,target,nincstr)
        
        pub.sendMessage("COMMAND", '*post_marc_t16_addrequest,%s' % lcommand)
        
        # =========process Displacement command
        itemtype = 'Node Scalar'
        selected = self.POST_D_ItemSource.GetStringSelection()

        # cleanup target list
        if self.POST_D_ItemSelSingle.GetValue() == True:
            target = self.POST_D_ItemSingle.GetValue()
        
        if self.POST_D_ItemSelList.GetValue() == True:
            target = self.POST_D_ItemList.GetValue()
            
        if self.POST_D_ItemSelSet.GetValue() == True:
            target = self.POST_D_ItemSet.GetStringSelection()
            
        dtablename = itemtype + '_' + str(random.randint(1, 10000))
        dcommand = "%s,%s,%s,%s,%s" % (dtablename,itemtype,selected,target,nincstr)
    
        pub.sendMessage("COMMAND", '*post_marc_t16_addrequest,%s' % dcommand)
    
        
        # ================retrive from results files
        pub.sendMessage("COMMAND", '*post_marc_t16_getdata')
        
        
        # =================add data plot
        pdataname = 'plot' + '_' + str(random.randint(1, 10000))
        com = "*plot_pdata_add,%s," % pdataname
        
        if loadsource == 'Load from time':
            com += ltablename + ':time,'
            
        else:
            print 'LD quick plot, right now only support time as load source'
            
        if self.POST_D_ItemSelSingle.GetValue() == True:
            com += dtablename + ':Node_%s' % target
        else:
            print 'LD quick plot, right now only support single node displacement as displacement source'
        
        pub.sendMessage("COMMAND",  com)
        

        #  =============== add figure
        fname = 'figure' + '_' + str(random.randint(1, 10000))
        pub.sendMessage("COMMAND", '*plot_figure_add,%s,%s,%s,%s' % (fname,pdataname,'publish','line-one axis'))
        
        # =============== show figure
        pub.sendMessage("GUIREFRESH", 'show_figure:%s' % fname)
        