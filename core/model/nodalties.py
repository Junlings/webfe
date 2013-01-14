#!/usr/bin/env python
import core.meta.meta_class as metacls

class nodalties():
    __metaclass__ = metacls.metacls_item
    def __init__(self):
        pass
    

class onetoonetie(nodalties):
    def __init__(self,paralib=None):
        nodalties.__init__(self)
        self.tietype = paralib['tietype']
        self.tieid = paralib['tieid']
        self.retnode = paralib['retnode']
        self.tienode = paralib['tienode']
    
    def get_parlist(self):
        return [self.retnode,self.tienode]
    
    
class onetoonespring(nodalties):
    def __init__(self,paralib=None):
        nodalties.__init__(self)
        self.tietype = paralib['tietype']
        self.tieid = paralib['tieid']
        self.DOF = paralib['DOF']
        self.stiff = paralib['stiff']
        self.retnode = paralib['retnode']
        self.tienode = paralib['tienode']
        
    def get_parlist(self):
        return [self.retnode,self.tienode]
    
class marc_rbe2(nodalties):
    def __init__(self,paralib=None):
        nodalties.__init__(self)
        self.tietype = paralib['tietype']
        self.tieid = paralib['tieid']
        self.retnode = paralib['retnode']
        self.tienodelist = paralib['tienodelist']

    def get_parlist(self):
        output = []
        if type(self.tienodelist) == type("setname"):
            output.extend([self.retnode,self.tienodelist])            
            
        else:
            for node in self.tienodelist:
                output.extend([self.retnode,node])
        return output
    
if __name__ == '__main__':
    pass
    
    print 1

    