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
        
class onetoonespring(nodalties):
    def __init__(self,paralib=None):
        nodalties.__init__(self)
        self.tietype = paralib['tietype']
        self.tieid = paralib['tieid']
        self.DOF = paralib['DOF']
        self.stiff = paralib['stiff']
        self.retnode = paralib['retnode']
        self.tienode = paralib['tienode']

class marc_rbe2(nodalties):
    def __init__(self,paralib=None):
        nodalties.__init__(self)
        self.tietype = paralib['tietype']
        self.tieid = paralib['tieid']
        self.retnode = paralib['retnode']
        self.tienodelist = paralib['tienodelist']
        
if __name__ == '__main__':
    pass
    
    print 1

    