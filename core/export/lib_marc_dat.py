#!/usr/bin/env python
""" This module help export the model node and element to marc dat format and the rest in procedure file
    to help accelerate the import process in MSC.Marc
"""
import core.meta.meta_export as metacls
import numpy as np
from lib_marc import ex_Marc

# define derived class based on export marc class
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
    
    def ex_itemset_single(self,setname,itemset):
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
    
    def ex_itemset_single_dat(self,setname,itemset):
        ''' export single set which constains either node list or element list'''
        if itemset.settype == 'node':   
            #exp = '*store_nodes %s\n' % (setname)
            exp = 'define,node,set,%s\n' % (setname)
            #print itemset.nodelist
            n_line = 1
            for node in itemset.nodelist:
                if node in self.node_seq.keys():
                    exp += ' %s ' % self.node_seq[node]
                    if n_line == 10:
                        exp += ' c\n'
                        n_line = 1
                    else:
                        n_line += 1                    
                else:
                    raise KeyError,('node ',str(node),' in itemset ', setname,' do not exist')

                
            exp += '\n'
            return exp
        elif itemset.settype == 'element':   
            exp = 'define,element,set,%s\n' % (setname)
            
            n_line = 1
            for elem in itemset.elemlist:
                exp += ' %s ' % str(elem)
                
                if n_line == 10:
                    exp += ' c\n'
                    n_line = 1
                else:
                    n_line += 1                
            
            exp += '\n'
            return exp
        else:
            raise TypeError, "ItemSet type do not identified"

    

            
        
    
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
        output = str1
        typelist = model.get_model_element_type()

        typelist.sort()
        for typeid in typelist:
            if typeid == 98:   #some thing not working with element id 98, use truss element 9 and change it back using the procedure file
                typeid = 9
            output += str3 % str(typeid)
            
        output += str2
        
        # export connectivity
        output += 'connectivity\n'
        output += '0,0,1,\n'
        for key,elem in model.connlist.itemlib.items():
            #etype = str(model.get_element_typeid(key))
            etype = 'None'
            nodestr = ''
            for i in elem.nodelist:
                nodestr += ','
                nodestr += str(self.node_seq[i])
                
                if etype == 'None':
                    if len(elem.nodelist) == 4:
                        etype = '75'
                    elif len(elem.nodelist) == 2:
                        etype = '9'
                    elif len(elem.nodelist) == 8:
                        etype = '7'
                
            output += '%s,%s%s\n' % (key,etype,nodestr)
        
        
        # export grid
        output += 'coordinates\n'
        output += '3,%s,0,1,\n' % len(model.nodelist.itemlib.keys())
        for key,node in model.nodelist.itemlib.items():
            output += '%s,%s,%s,%s\n' % (self.node_seq[key],node.xyz[0],node.xyz[1],node.xyz[2])
        
        
        for setname,itemset in model.setlist.items():
            output += self.ex_itemset_single_dat(setname,itemset)
            
        return output