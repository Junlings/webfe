#!/usr/bin/env python

import  wx

class MyDictTree(wx.TreeCtrl):
    """ Tree Frane """
    def __init__(self, parent,treerootname='model'):
        wx.TreeCtrl.__init__(self,parent,style=wx.TR_HAS_BUTTONS|wx.ALL|wx.EXPAND,size=(200,400))   # Call the function PreXXX where XXX is your wx base class

    def create_nodes_dict(self,parentitem,inputdict):
        
        if type(inputdict) == type({}):
            for key,value in inputdict.items():
                child = self.AppendItem(parentitem, "%s" % key)
                
                if type(value) == type({}):
                    self.create_nodes_dict(child,value)
        else:
            return 1
    
    
    def bind(self):
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnListRClick, self)
    
    def OnActivated(self, evt):
        print "OnActivated:    ", self.GetItemText(evt.GetItem())
        
    def GetSelectionPath(self):
        pieces = []
        item = self.GetSelection()
        
        while self.GetItemParent(item):
          piece = self.GetItemText(item)
          pieces.insert(0, piece)
          item = self.GetItemParent(item)
        return pieces
    
    def OnSelect(self, event):
        list = ['1','2','3','4']
        #self.lc1.InsertStringItem(0, list[1])

    def HandleDrop(self, text):
        self._text = text
        self.PopupMenu(self.menu)

    def OnBeginDrag(self, event):
        item = event.GetItem()
        tree = event.GetEventObject()

        if item != tree.GetRootItem(): # prevent dragging root item
            def DoDragDrop():
                txt = tree.GetItemText(item)
                print "Starting drag'n'drop with %s..." % repr(txt)
                dd = DropData()
                dd.setObject(txt)

                comp = wx.DataObjectComposite()
                comp.Add(dd)
                dropSource = wx.DropSource(self)
                dropSource.SetData(comp)
                result = dropSource.DoDragDrop(wx.Drag_AllowMove)
                print "drag'n'drop finished with:", result, "\n"

            wx.CallAfter(DoDragDrop) # can't call dropSource.DoDragDrop here..
            
    def OnMouseLeftUp(self, evt):
        self.tree.Unbind(wx.EVT_MOTION)
        self.tree.Unbind(wx.EVT_LEFT_UP)
        evt.Skip()
        
    def OnMotion(self, evt):
        size = self.tree.GetSize()
        x,y = evt.GetPosition()
        
        if y < 0 or y > size[1] and not hasattr(self, 'timer'):
            self.timer = wx.Timer(self)
            self.timer.Start(70)
        evt.Skip()
        
    def OnTime(self, evt):
        x,y = self.tree.ScreenToClient(wx.GetMousePosition())
        size = self.tree.GetSize()

        if y < 0:
            self.ScrollUp()
        elif y > size[1]:
            self.ScrollDown()
        else:
            del self.timer
            return
        self.timer.Start(70)
        
    def ScrollUp(self):
        if "wxMSW" in wx.PlatformInfo:
            self.tree.ScrollLines(-1)
        else:
            first = self.tree.GetFirstVisibleItem()
            prev = self.tree.GetPrevSibling(first)
            if prev:
                # drill down to find last expanded child
                while self.tree.IsExpanded(prev):
                    prev = self.tree.GetLastChild(prev)
            else:
                # if no previous sub then try the parent
                prev = self.tree.GetItemParent(first)

            if prev:
                self.tree.ScrollTo(prev)
            else:
                self.tree.EnsureVisible(first)

    def ScrollDown(self):
        if "wxMSW" in wx.PlatformInfo:
            self.tree.ScrollLines(1)
        else:
            # first find last visible item by starting with the first
            next = None
            last = None
            item = self.tree.GetFirstVisibleItem()
            while item:
                if not self.tree.IsVisible(item): break
                last = item
                item = self.tree.GetNextVisible(item)

            # figure out what the next visible item should be,
            # either the first child, the next sibling, or the
            # parent's sibling
            if last:
                if self.tree.IsExpanded(last):
                    next = self.tree.GetFirstChild(last)[0]
                else:
                    next = self.tree.GetNextSibling(last)
                    if not next:
                        prnt = self.tree.GetItemParent(last)
                        if prnt:
                            next = self.tree.GetNextSibling(prnt)

            if next:
                self.tree.ScrollTo(next)
            elif last:
                self.tree.EnsureVisible(last)

    def traverse(self, traverseroot, function, res_p,res_s,cookie=0):
        """ recursivly walk tree control """
        # step in subtree if there are items or ...
        #res2 = function(traverseroot)
        #self.treedict2[res2] = {}
        
        text_child = None
        if self.tree.ItemHasChildren(traverseroot):
            firstchild, cookie = self.tree.GetFirstChild(traverseroot)#, cookie)
            text_child = function(firstchild)
            res_s[text_child] = {}
            self.traverse(firstchild, function, res_s,res_s[text_child], cookie)

        # ... loop siblings
        child = self.tree.GetNextSibling(traverseroot)
        if child:
            text_slib = function(child)
            res_p[text_slib] = {}
            self.traverse(child, function,res_p,res_p[text_slib], cookie)

        return res_p,res_s
                
    def getallnode(self):
        """ get all node is a dict"""
        self.treedict2 = {}
        list = []
        traverseroot = self.tree2.GetRootItem()
        fun = self.GetItemText

        self.traverse(traverseroot,fun,None,self.treedict2)
    
    def findItem(self, item):
        parent = self.tree.GetItemParent(item)
        for n,i in enumerate(self.traverse(parent)):
            if item == i:
                return n
                
    def OnSize(self, event):
        w,h = self.GetClientSizeTuple()
        self.tree.SetDimensions(0, 0, w, h)

    def OnSelChanged(self, event):
        self.item = event.GetItem()
        print "OnActivated:    ", self.GetItemText(event.GetItem())
        event.Skip()
    
    def conndata(self,value):
        print value
    def OnCloseWindow(self, event):
        self.getallnode()
        print self.treedict2
        self.conndata((self.Title,self.treedict2))
        self.Destroy()
        #return res
    
    def OnListRClick(self,event):
        print 'detected'

    def OnExpandAll(self, e):
        """ expand all nodes """
            #root = self.GetRootItem()
            #fn = self.Expand
            #self.traverse(root, fn)
        self.ExpandAll()
        
    def OnCollapseAll(self, e):
        """ collapse all nodes of the tree """
            #root = self.GetRootItem()
            #fn = self.Collapse
            #self.traverse(root, fn)
        self.CollapseAll()
    def traverse(self, traverseroot, function, cookie=0):
            """ recursivly walk tree control """
            # step in subtree if there are items or ...
            if self.ItemHasChildren(traverseroot):
                    firstchild, cookie = self.GetFirstChild(traverseroot, cookie)
                    #firstchild, cookie = self.GetFirstChild(traverseroot)
                    function(firstchild)
                    self.traverse(firstchild, function, cookie)

            # ... loop siblings
            child = self.GetNextSibling(traverseroot)
            if child:
                    function(child)
                    self.traverse(child, function, cookie)
                        
if __name__ == '__main__':
    #__test()
    app = wx.App(redirect = False)
    
    #res1 = results('res1')
    #res1.label = ['aa','bb','vv']
    #res2 = results('res1')
    #res2.label = ['aa2','bb2','vv2']

    
    #da1.inputtreedict = {'aaaa' : ['aaa1','aaa2'],'bbbb' : ['bbb1','bbb2'],'CCCC': ['cccc1','cccc2','cccc3','cccc4',]}
   # da1.inputplotdict = {'aaaa' : ['aaa1','aaa2'],'bbbb':['bbb1','bbb2']}
    frame = wx.Frame(None)
    panel1 = wx.Panel(frame)
    tree = MyDictTree(parent = panel1)
    tree.root = tree.AddRoot('bb')
    tree.AppendItem(tree.root, "aaa")
    
    frame.Show()
    app.MainLoop()