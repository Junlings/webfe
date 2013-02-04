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
import threading
import Queue
import time

global _maxdigits
_maxdigits = 3


DEBUG = False #True

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()


def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data
        
# Thread class that executes processing

command_queue = []

class WorkerThread(threading.Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window,handle):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.parser = handle
        self.command = Queue.Queue()
        command_queue.append(self.command)
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()
    
    
    def receive(self,data):
        for q in command_queue:
            q.put(data)
                
        
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread. Simulation of
        # a long process (well, 10s here) as a simple loop - you will
        # need to structure your processing so that you periodically
        # peek at the abort variable
        
        while True:
            if self._want_abort:  # when shut down the program
                break
            command = self.command.get()

            try:
                
                self.notify('Command Process in Running ...')
                
                t1 = time.time()
                wx.BeginBusyCursor()  # indicator command running
                output = self.parser(command)
                t2 = time.time()
                
                timelap = t2- t1
                self.notify('Command,"%s",succeed used "%s" second' % (output,str(timelap)))
                wx.EndBusyCursor()
                
                # refresh GUI
                self._notify_window.ForceReFresh()
                #wx.PostEvent(self._notify_window, ResultEvent(True))
            except Exception as inst:
                wx.EndBusyCursor()
                print "Error happened during command processing\n",inst
                self._notify_window.mainframe.MAIN_STATUSBAR.SetStatusText('Command Process Failed', 2)
                continue
                #wx.PostEvent(self._notify_window, ResultEvent(False))
    
    def notify(self,msg):
        self._notify_window.mainframe.MAIN_STATUSBAR.SetStatusText(msg, 2)
    
    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self._want_abort = 1
        
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
        self.worker = None
        self.OnStart(None)
        
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
        
        # Set up event handler for any worker thread results
        EVT_RESULT(self,self.OnResult)        
        
        return True

    def OnCommand(self,command): #,update=True):
        if DEBUG:
            wx.BeginBusyCursor()  # indicator command running
            try:
                self.com.parser(command.data)
            except Exception as inst:
                print inst
            
            wx.EndBusyCursor()
        else:
            #wx.BeginBusyCursor()  # indicator command running
            self.worker.receive(command.data)
            #wx.EndBusyCursor()
 
    def OnStart(self, event):
        """Start Computation."""
        # Trigger the worker thread unless it's already busy
        if not self.worker:
            #self.mainframe.MAIN_STATUSBAR.SetStatusText('Starting computation....', 2)
            self.worker = WorkerThread(self,self.com.parser)
    
    
    def OnStop(self, event):
        """Stop Computation."""
        # Flag the worker thread to stop if running
        if self.worker:
            #self.MAIN_STATUSBAR.SetStatusText('Trying to abort computation....', 2)
            self.worker.abort()

    def OnResult(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            self.mainframe.MAIN_STATUSBAR.SetStatusText('Computation aborted....', 2)
        else:
            # Process results here
            self.mainframe.MAIN_STATUSBAR.SetStatusText('Computation Complete Status: %s' % event.data, 2)
            #self.status.SetLabel('Computation Result: %s' % event.data)
        # In either event, the worker is done
        self.worker = None
        
        
    def OnGUI(self,GUI_event):
        wx.PostEvent(self,GUI_event)
    
    def ForceReFresh(self):
        self.resframe.OnForceResChange(None,self.com.results)
        self.mainframe.OnForceRefresh(None,self.com.model)
        
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
    
    for arg in sys.argv:
        print arg
    
    # take care of the command line inputs with mac file 
    if '-f' in sys.argv:
        commandsys = commandparser()
        commandsys.macro_load(sys.argv[2])
        

        
    else:
        app = MyApp(False)
        app.MainLoop()