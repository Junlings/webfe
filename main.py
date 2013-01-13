import wx
#from wx import xrc
#from wx.lib.pubsub import Publisher as pub
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

from command import commandparser
from components.MainFrame import MainFrame
from components.post.resultframe import ResultFrame

import sys
import datetime

global _maxdigits
_maxdigits = 3

 
class RedirectText:
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        if string != '\n':
            if string[0] == '*':
                self.out.WriteText('...>> '+string)
            else:
                self.out.WriteText('........... '+string)
        else:
            self.out.WriteText(string)

class MyApp(wx.App):

    def OnInit(self):
        self.com = commandparser()
        self.mainframe = MainFrame(None,self.com.model)
        self.resframe = ResultFrame(self.mainframe,self.com.results)
        self.mainframe.Show()
        #self.resframe.Show()

        pub.subscribe(self.OnCommand, "COMMAND")
        pub.subscribe(self.OnGUI, "GUI")
        pub.subscribe(self.OnGUIREFRESH, "GUIREFRESH")
        
        redir = RedirectText(self.mainframe.TextMessage)
        sys.stdout = redir
        
        print '*Webfe desktop version started on %s' % datetime.datetime.now()
        return True
    
    def OnCommand(self,command): #,update=True):
        wx.BeginBusyCursor()  # indicator command running
        self.com.parser(command.data)
        wx.EndBusyCursor()

        
    def OnGUI(self,GUI_event):
        wx.PostEvent(self,GUI_event)
        
    def OnGUIREFRESH(self,request):
        if request.data == 'results':
            return self.resframe.OnForceResChange(None,self.com.results)
        elif request.data == 'model':
            return self.mainframe.OnForceRefresh(None,self.com.model)
        
        elif request.data == 'show_resultframe':
            if self.resframe == None:
                self.resframe = ResultFrame(self,self.results)
                self.resframe.Show()
            else:
                try:
                    self.resframe.SetFocus()
                    self.resframe.OnResChange(event)
                except:
                    self.resframe = ResultFrame(None,self.com.results)
                    self.resframe.Show()
                    
        elif 'show_figure' in request.data:
            fkey = request.data.split(':')[1]
            self.resframe.OnAddFigurePage(fkey)
            
        
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()