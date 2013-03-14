#!/usr/bin/env python

""" define setclass"""
import core.meta.meta_class as metacls

class itemset():
    __metaclass__ = metacls.metacls_item
    
    def __init__(self,paralib):
        
        self.settype = 'node'  # 'element', 'both'
        self.nodelist = []
        self.elemlist = []
        self.nn = 0
        self.ne = 0
        
        self.unfold(paralib)
        self.update()
    
    def getlist(self):
        
        return [len(self.nodelist),len(self.elemlist)]
                
    def add(self,itemlist,settype):
        if settype == 'node':
            self.addnode(itemlist)
        elif settype == 'element':
            self.addelem(itemlist)
        
    def delelemlist(self,elemlist):
        for elem in elemlist:
            self.delelem(elem)
            
    def delelem(self,elem):
        if elem in self.elemlist:
            self.elemlist.remove(elem)    
        
        
    def addelem(self,elemlist):
        self.elemlist.extend(elemlist)
        
    def addnode(self,nodelist):
        self.nodelist.extend(nodelist)        
    
    def update(self):
        self.nn = len(self.nodelist)
        self.ne = len(self.elemlist)
        
    def update_nodeseq(self,replacedict):
        ''' change the nodelist for element
            input:
                 updatelist --  a dictionary with target node seq as key and
                                replaceable node seq as values
        '''
        
        if len(self.nodelist) == 0:  # if no node in setlist
            return 0
        
        # get update dictionary
        
        updatenodeset = set(replacedict.keys())
        selnodeset = set(self.nodelist)
        
        mergenodelist = updatenodeset & selnodeset
        if len(mergenodelist) > 0:
            mergenodelist = list(mergenodelist)

            for i in range(0,len(mergenodelist)):
                ij = self.nodelist.index(mergenodelist[i])
                self.nodelist[ij] = replacedict[mergenodelist[i]]
            self.nodelist = set(self.nodelist)
        
        '''
        if len(self.nodelist) == 0:  # if no node in setlist
            return 0
        else:            
            for seq in updatelist.keys():      # loop over master seq
                
                tempset = list(set(updatelist[seq]) & set(self.nodelist))
                if len(tempset) >0:
                    self.nodelist = list(self.nodelist)
                    for item in tempset:
                        ij= self.nodelist.index(item) # locate the position
                                                            # of slave seq in list
                        self.nodelist[ij] = seq   # replace slave with master
        '''
    def deleteelembylist(self,deleteelemlist):
        for elem in deleteelemlist:
            if elem in self.elemlist:
                self.elemlist.pop(self.elemlist.index(elem))
        