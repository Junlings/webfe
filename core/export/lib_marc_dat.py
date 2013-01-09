#!/usr/bin/env python
import core.meta.meta_export as metacls
import numpy as np
from lib_marc import ex_Marc

class ex_Marc_dat(ex_Marc):
    #__metaclass__ = metacls.metacls_export   # meat class
    
    def __init__(self):
        ex_Marc.__init__(self)

    def ex_variable_single(self,*args):
        return ''
    def ex_coord_single(self,node):
        ''' export coordinate defined nodes'''
        exp = self.nodes_op.create(node.xyz[0], node.xyz[1], node.xyz[2])
        self.node_seq_now += 1
        self.node_seq[node.seq] = self.node_seq_now

        return ''  # do not 
    
    def ex_conn_prop_single(self,conn,prop):
        ''' export single element connectivity'''
        return ''
    
    def ex_settings_single(self,settings):
        ''' export model settings'''
        inputstr= ''
        inputstr += "*new_model\n"
        inputstr += "yes\n"
        inputstr += "*save_model\n"
        ee = "*import marc_read %s\n" % (settings['expfolder']+'.dat')
        inputstr += ee
        return inputstr
    
    def  write_individual_file(self,model):
        str1 =  """title               job1
extended
$...................................
"""


        str3 = "elements,%s\n"
        str2 = """version                     11
end
$...................
"""
        
        # export header
        output = str1 + (str3 % '75') + str2
        
        # export connectivity
        output += 'connectivity\n'
        output += '0,0,1,\n'
        for key,elem in model.connlist.itemlib.items():
            etype = '75'
            nodestr = ''
            for i in elem.nodelist:
                nodestr += ','
                nodestr += str(i)
                
            output += '%s,%s%s\n' % (key,etype,nodestr)
            etype
        
        
        # export grid
        
        output += 'coordinates\n'
        output += '3,%s,0,1,\n' % len(model.nodelist.itemlib.keys())
        for key,node in model.nodelist.itemlib.items():
            output += '%s,%s,%s,%s\n' % (self.node_seq[key],node.xyz[0],node.xyz[1],node.xyz[2])
            
        return output