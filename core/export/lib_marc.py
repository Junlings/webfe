#!/usr/bin/env python
import core.meta.meta_export as metacls
import numpy as np


class ex_Marc():
    __metaclass__ = metacls.metacls_export   # meat class
    def __init__(self):

        self.node_seq = {}
        self.node_seq_now = 0
        self.elem_seq = {}
        self.elem_seq_now = 0
        
        self.modeldbop = modeldb()  # database operation class
        self.nodes_op = nodes_op()
        self.elems_op = elems_op()
        self.table = table()
        self.select = select()
        self.node_ties = node_ties()
        self.contacts = contacts()
        self.material = material()
        self.geometry = geometry()
        self.bond_load = bond_load()
        self.loadcase = loadcase()
        self.jobop = jobop()
        self.post = post()
        self.nodaltie = node_ties()
    
    def ex_variable_single(self,*args):
        return '\n'
    
    def ex_coord_single(self,node):
        ''' export coordinate defined nodes'''
        exp = self.nodes_op.create(node.xyz[0], node.xyz[1], node.xyz[2])
        self.node_seq_now += 1
        self.node_seq[node.seq] = self.node_seq_now
        return exp
            
    def ex_conn_prop_single(self,conn,prop):
        ''' export single element connectivity'''
        exp = self.elems_op.connclass(prop.__class__.__name__)
        
        nodelist = []
        for node in conn.nodelist:
            nodelist.append(self.node_seq[node])
                
        exp += self.elems_op.connnodelist(nodelist)
        
        self.elem_seq_now += 1
        self.elem_seq[conn.seq] = self.elem_seq_now
        
        return exp
    
    def ex_table_single(self,key,table):
        '''create tables '''
        if table.varnum == 1:
            exp = self.table.new_var1(key,table.vartype[0],table.datapoints)
        
        return exp
    
    def ex_tables(self,EXP,tablelist,dkey=None):
        ''' export variables '''
        if dkey == None:
            for key in tablelist.keys():
                table = tablelist[key]
                EXP.write(self.ex_table_single(key,table))        
        else:
            table = tablelist[dkey]
            EXP.write(obj.ex_table_single(dkey,table))          
        return EXP
    
    def ex_settings_single(self,settings):
        ''' export model settings'''
        exp = self.modeldbop.new(settings['prjname'])
        return exp
    
    def ex_itemset_single(self,setname,itemset):
        ''' export single set which constains either node list or element list'''
        if itemset.settype == 'node':   
            exp = '*store_nodes %s\n' % (setname)
            #print itemset.nodelist
            n_line = 1
            for node in itemset.nodelist:
                if node in self.node_seq.keys():
                    exp += ' %s ' % self.node_seq[node]
                    if n_line == 10:
                        exp += '\n'
                        n_line = 1
                    else:
                        n_line += 1                    
                else:
                    raise KeyError,('node ',str(node),' in itemset ', setname,' do not exist')

                
            exp += '#\n'
            return exp
        elif itemset.settype == 'element':   
            exp = '*store_elements %s\n' % (setname)
            
            n_line = 1
            for elem in itemset.elemlist:
                exp += ' %s ' % str(elem)
                
                if n_line == 10:
                    exp += '\n'
                    n_line = 1
                else:
                    n_line += 1                
            
            exp += '#\n'
            return exp
        else:
            raise TypeError, "ItemSet type do not identified"
        
    def ex_mat_single(self,key,mat):
        ''' export single material '''
        if mat.__class__.__name__ == 'interface_marc_builtin':
        
            exp = self.material.interface_cohesive(key,mat)
        
        elif mat.__class__.__name__ == 'uniaxial_elastic':
            exp = self.material.create_elastic(key,mat.E,mat.mu,mat.mass)
        
        elif mat.__class__.__name__ == 'uniaxial_elastic_plastic':    
            exp = self.material.plasticity(key,mat.E,mat.mu,mat.sigma_y,tablename=mat.tabletag)
        else:
            raise TypeError, "Material type do not identified"
        
        return exp
    def ex_prop_single(self,key,prop):
        ''' specify the element number in marc '''
        exp = ''
        if prop.setnamelist != None:
            for setname in prop.setnamelist:
                exp += self.elems_op.elem_type_set(prop.type,setname)
        
            try:
                if prop.mattag != None:
                 exp += self.material.associate_setname(prop.mattag,prop.setnamelist)
            except:
                pass
            
            try:
                if prop.sectag != None:
                    exp += self.geometry.associate_setname(prop.sectag,prop.setnamelist)
            except:
                pass
        # need to add reverse for those not include in the set, but defined by associate
            return exp
    
    def ex_bond_single(self,key,bond):
        exp = ''
        if bond.type == 'bond':
            if bond.DOF == 6:
                exp = self.bond_load.support(key,bond.xyz)
            elif bond.DOF == 3:
                exp = self.bond_load.support(key,[bond.xyz[0],bond.xyz[1],0,0,0,bond.xyz[2]])
                
                
            
        elif bond.type == 'load':
            Label = []
            if bond.DOF == 6:
                if bond.xyz[0] == 1:
                    Label.append('x')
                if bond.xyz[1] == 1:
                    Label.append('y')
                if bond.xyz[2] == 1:
                    Label.append('z')
            elif bond.DOF == 3:
                if bond.xyz[0] == 1:
                    Label.append('x')
                if bond.xyz[1] == 1:
                    Label.append('y')
                    
            exp = self.bond_load.pointload(key,Label,bond.scalar,bond.tabletag)
            
        elif bond.type == 'disp':
            Label = []
            if bond.DOF == 6:
                if bond.xyz[0] == 1:
                    Label.append('x')
                if bond.xyz[1] == 1:
                    Label.append('y')
                if bond.xyz[2] == 1:
                    Label.append('z')
                if bond.xyz[3] == 1:
                    Label.append('rx')
                if bond.xyz[4] == 1:
                    Label.append('ry')
                if bond.xyz[5] == 1:
                    Label.append('rz')
            elif bond.DOF == 3:
                if bond.xyz[0] == 1:
                    Label.append('x')
                if bond.xyz[1] == 1:
                    Label.append('y')
                if bond.xyz[2] == 1:
                    Label.append('rz')
            

            exp += self.bond_load.disp(key,Label,bond.scalar,bond.tabletag)

        
        else:
            raise TypeError,('Boundary condition type not identified',bond.type)
        
        
        if bond.setnamelist != None and type(bond.setnamelist)  == type([]):
            exp += self.bond_load.associate_setname(key,bond.setnamelist)
        
        if bond.nodelist != None and len(bond.nodelist) > 0:
            exp += self.bond_load.associate_nodelist(key,bond.nodelist)
        return exp
        

    def ex_sec_single(self,key,sec,mat=None,mode=None):
        exp = ''
        if sec.__class__.__name__ == 'shell_section':
            exp = self.geometry.shell(key,sec.thickness)
        elif sec.__class__.__name__ == 'shape_section':
            if sec.shape == 'general_truss':
                exp = self.geometry.truss3d(key,sec.para['area'])
            
        #    exp = self.geometry.truss3d()
        return exp
    

    def ex_nodaltie_single(self,key,nodaltie):
        exp = ''
        if nodaltie.__class__.__name__ == 'marc_rbe2':
            exp = self.nodaltie.rbe2(nodaltie.tietype,nodaltie.tieid,nodaltie.retnode,nodaltie.tienodelist)
            
        elif nodaltie.__class__.__name__ == 'onetoonespring':
            exp = self.nodaltie.rbe2()
            
        elif nodaltie.__class__.__name__ == 'onetoonetie':
            exp = self.geometry.truss3d(key,sec.para['area'])
            
        #    exp = self.geometry.truss3d()
        return exp
    
        
    def ex_recorder_single(self,key,recorder):
        exp = ''
        
        if recorder.incrrange == 'ALL':
            start = 1
            end = 99999
            incr = 1
            
        else:
            [start,end,incr] = recorder.incrrange
            
        if recorder.__class__.__name__ == 'his_stress_node':
            type = 'stress'
            for DOF in recorder.DOF:
                for node in recorder.nodelist:
                    exp += self.post.draw_loc(recorder.recfile,node, type,DOF,
                                              start=start,end=end,incr=incr)

        if recorder.__class__.__name__ == 'his_strain_node':
            type = 'strain'
            for DOF in recorder.DOF:
                for node in recorder.nodelist:
                    exp += self.post.draw_loc(recorder.recfile,node, type,DOF,
                                              start=start,end=end,incr=incr)
            
        #    exp = self.geometry.truss3d()
        return exp
        
    
    def ex_loadcase_single(self,key,loadcase):
        exp = ''
        if loadcase.__class__.__name__ == 'static':
            exp = self.loadcase.create_static_fixed(key,loadcase.para['nstep'])
        
        elif loadcase.__class__.__name__ == 'static_arclength':
            exp = self.loadcase.create_arclength(key,loadcase.para['nstep'])
            
        else:
            raise KeyError,('load case type',loadcase.__class__.__name__,' do not defined')
            
        exp += self.loadcase.select_load(key,loadcase.boundarylist,clear='Yes')
        return exp
    
    def ex_job_single(self,key,job):
        exp = ''
        if job.__class__.__name__ == 'static_job':
            exp = self.jobop.create_general(key,lcasename=job.loadcaselist,elastic=0,dim='3D')
            
        else:
            raise KeyError,('job type',job.__class__.__name__,' do not defined')
        
        
        if len(job.initialcond) > 0:            
            exp += self.jobop.initialcond(key,job.initialcond)
        
        if len(job.reqresultslist) > 0:            
            exp += self.jobop.req_result(key,job.reqresultslist)
        
        if job.submit == True:
            exp += self.jobop.submit_job(key)
        return exp
    
class modeldb():
    ''' class of marc database (*.mud file) operations'''
    
    def __init__(self):
        ''' initialize the operator'''

    def openmodel(self,jname):
        '''open existing model'''
        inputstr= ''
        inputstr += "*open_model\n"
        dbname=jname + '.mud\n'
        inputstr += dbname
        return inputstr

    def new(self,name):
        '''create new model'''
        inputstr= ''
        inputstr += "*new_model\n"
        inputstr += "yes\n"
        inputstr += "*save_model\n" 
        return inputstr

    def savemodelas(self,jname):
        ''' save model to new location with new name'''
        inputstr= ''
        inputstr += "*save_as_model\n"
        dbname=jname + '.mud\n'
        inputstr += dbname 
        inputstr += "yes\n"
        return inputstr

    def save(self):
        ''' save model to current location'''
        inputstr= ''
        inputstr += "*save_model\n"
        return inputstr

    def quit(self):
        '''  quit MARC without saving'''
        inputstr= ''
        inputstr += "*quit\n"
        inputstr += "*yes\n"
        return inputstr   

class nodes_op():
    ''' this is the class defines the node operation'''
    def __init__(self):
        pass
    
    def create(self,x,y,z=0):
        ''' create node based on the input coord[inates]'''
        inputstr = ''
        inputstr += "*add_nodes %6.6f %6.6f %6.6f\n" % (x, y, z)
        return inputstr 
    
    def sweep(self):
        '''
        sweep the node with the same coordinates
        '''
        inputstr = ''
        inputstr +=  "*sweep_nodes\n"
        inputstr +=  "all_selected\n"
        inputstr += "\n"
        return inputstr 
    
    def remove_unused(self):
        '''
        remove unused node
        '''
        inputstr = ''
        inputstr += '*remove_unused_nodes\n'
        return inputstr 

class elems_op():
    '''
    This class is for element operation
    '''
    def __init__(self):
        pass
    
    def connnodelist(self,conn_nodelist):
        '''
        create the two node line element
        '''
        inputstr = '*add_elements'
        for node in conn_nodelist:
            inputstr += ' %s ' % node    # shall be transferred node sequence
        inputstr += '\n'
        return inputstr
    
    def connclass(self,conn_class):
        '''
        create the element class
        '''
        inputstr = ''
        
        if conn_class == 'hex8':
            inputstr += '*set_element_class hex8\n'
        
        elif conn_class == 'quad4':
            inputstr += "*set_element_class quad4\n"
        
        elif conn_class == 'line2':
            inputstr += "*set_element_class line2\n"
        return inputstr
        
    def subdivide(self,nx,ny,nz):
        '''
        divide the selected element to nx,ny,nz divident
        '''
        inputstr = ''   
        inputstr += "*sub_divisions\n %d %d %d \n"  % (nx,ny,nz)
        inputstr += "*subdivide_elements \n"
        inputstr += "all_selected\n"
        return inputstr
    
    def elem_type_set(self,type,setname):
        inputstr = '*element_type %s\n' % type
        inputstr += '%s\n' % setname
        return inputstr
    
class table():
    '''
    This is the table operator
    '''
    def __init__(self):
        pass
    
    def addpoint(self,points):
        ''' add point to the table'''
        inputstr = ''
        inputstr += '*table_add\n'
        for i in range(0,len(points)):
            inputstr += '%g\n%g\n' % (points[i][0],points[i][1])
        return inputstr
        
    def new_var1(self,name,type,points=None):
        '''
        setup the type and data for the first var
        create one independent variable table
        '''
        inputstr = ''
        inputstr += '*new_md_table 1 1\n'
        inputstr += '*table_name\n'
        inputstr += '%s\n'% name
        inputstr += '*set_md_table_type 1\n'
        inputstr += '%s\n'% type
        #return inputstr

        if points != None:
            inputstr += self.addpoint(points)
        return inputstr

class select():
    '''
    This is the class to facilite the selection of nodes and/or elements
    '''
    def __init__(self):
        self.mode = 'Add'  # default select mode is add to selection
        #self.recorder = recorder
        
    def select_mode(self,mode):
        '''
        change seelct mode
        '''
        
        self.mode = mode
        inputstr = ''
        if mode=='Add':
            inputstr += "*select_mode_and\n"
        elif mode=='Invert':
            inputstr += "*select_mode_invert\n"
        elif mode=='Intersect':
            inputstr += "*select_mode_intersect\n"
        elif mode=='Except':
            inputstr += "*select_mode_except\n"
        return inputstr
    
    def clear(self):
        '''
        clear the selection
        '''
        
        self.nodes = []
        self.elems = []
        inputstr = ''
        inputstr += "*select_clear_elements\n"
        inputstr += "*select_clear_nodes\n"
        return inputstr
        
        self.select_mode('Add')
    
    def node_all(self):
        '''
        select all nodes
        '''
        self.select_mode('Add')
        inputstr = ''
        inputstr += "*select_method_single\n"
        inputstr += "*select_nodes\n"
        inputstr += "all_existing\n"
        return inputstr
    
    def elem_all(self):
        '''
        select all elements
        '''
        inputstr = ''
        inputstr += self.select_mode('Add')
        
        inputstr += "*select_elements\n"
        inputstr += "all_existing\n"
        return inputstr     
    
    def elem_set(self,name):
        '''
        select element by set name
        '''
        inputstr = ''
        inputstr += "*select_sets\n"
        inputstr += "%s \n" % name
        return inputstr             
    
    def node_seq(self,seq):
        '''
        select node by sequence
        '''
        inputstr = ''
        inputstr += "*select_nodes\n"
        for i in range(0,len(seq)):
            inputstr += str(seq[i]) 
            inputstr += ' '
        inputstr += '#\n'
        return inputstr
    
    def node_elem(self):
        '''
        select nodes by the selected elements
        '''
        
        inputstr = ''
        inputstr += "*select_nodes_elements\n"
        inputstr += "all_selected\n"
        return inputstr
        
    def node_box(self,data):
        '''
        select node by boundarying box
        '''
        inputstr = ''
        inputstr += "*select_method_box\n"
        inputstr += "*select_nodes\n"
        for i in range(0,6):
            inputstr +='%g' % data[i]
            inputstr += ' '            
        inputstr += '#\n'
        return inputstr
        
    def node_set(self,name):
        '''
        select node by set name
        '''
        
        inputstr = ''
        inputstr += "*select_sets\n"
        inputstr += "%s \n" % name
        return inputstr
        
    def elem_seq(self,data):
        '''
        select element by sequence
        '''
        inputstr = ''
        inputstr += "*select_method_single\n"
        inputstr += "*select_elements\n"
        for i in range(0,len(data)):
            inputstr +='%i' % data[i]
            inputstr += ' '
        inputstr += '#\n'
        return inputstr     
    
    def elem_node(self):
        '''
        select element by the selected nodes
        '''
        inputstr = ''
        inputstr += "*select_elements_nodes\n"
        inputstr += "all_selected\n"
        return inputstr
        
    def elem_box(self,data):
        '''
        select elements by boundarying box
        '''
        inputstr = ''
        inputstr += "*select_method_box\n"
        inputstr += "*select_elements\n"
        for i in range(0,6):
            inputstr +='%g' % data[i]
            inputstr += ' '            
        inputstr += '#\n'
        return inputstr
    
    def elem_Mat(self,mat_name):
        '''
        select element by material properity
        '''
        
        inputstr = ''
        inputstr += "*select_elements_material\n"
        inputstr += mat_name 
        inputstr += '\n # \n'
        return inputstr
    
    def elem_Geo(self,geo_name):
        '''
        select element by geometry properity
        '''
        inputstr = ''
        inputstr = "*select_elements_geometry\n"
        inputstr += geo_name
        inputstr += '\n # \n'
        return inputstr
            
    def elem_class(self,elemclass):
        '''
        select elements by element class
        '''
        inputstr = ''
        inputstr += "*select_elements_class\n"
        inputstr += elemclass
        inputstr += '\n # \n'
        return inputstr
            
    def store_elem(self,setname):
        '''
        store selected element to setname
        '''
        inputstr = ''
        inputstr += "*store_elements\n %s \n" % setname
        inputstr += "all_selected\n"
        return inputstr

    def store_node(self,setname):
        '''
        store selected node to setname
        '''
        inputstr = ''
        inputstr += "*store_nodes\n %s \n" % setname
        inputstr += "all_selected\n"
        return inputstr
        
    def apply_mat(self,name_material):
        '''
        assign the materail peoperties to selected elements
        '''
        inputstr = ''
        inputstr += "*edit_material\n"
        inputstr += name_material +'\n'
        inputstr += "*add_material_elements\n"
        inputstr += "all_selected\n #\n"
        
        return inputstr
        
    def apply_geo(self,name_geo):
        '''
        assign the geometry peoperties to selected elements
        '''
        inputstr = ''
        inputstr += "*edit_geometry\n"
        inputstr += name_geo +'\n'

        inputstr += "*add_geometry_elements\n"
        inputstr += "all_selected\n #\n"
        return inputstr
    
    def apply_bound(self,name_bound):
        '''
        assign the boundary condition to selected nodes
        '''
        inputstr = ''
        inputstr += "*edit_apply\n"
        inputstr += name_bound +'\n'

        inputstr += "*add_apply_nodes\n"
        inputstr += "all_selected\n"
        return inputstr
    
    def apply_elemtype(self,type):
        '''
        assign the select element type to selected nodes
        '''
        inputstr = ''
        inputstr += "*element_type %s \n" % type
        inputstr += "all_selected\n"
    
class node_ties():
    '''
    class to create/edit the nodal ties,
    include rbe2,rbe3,rigid links, spring, and etc.
    '''
    def __init__(self):
        pass
        #self.recorder = recorder
    
    def ties(self,tietype,tieid,retnode,tienode):
        '''
        create ties between retnode and tienode
        '''
        inputstr = ''
        inputstr += "*new_link *link_class tie\n"
        inputstr += "*link_name ties_%s_%s\n" % (tieid,tietype)
        inputstr += "*link_class tie *tie_type\n"
        inputstr += "%i" % int(tieid)
        inputstr += "*link_class tie *tied_node %i\n" % int(retnode)
        inputstr += "*link_class tie *retained_node 1 %i\n" % tienode
        return inputstr 
                
    def multitie(self,tietype,tieid,retnode,setname=None):
        '''
        create multiple ties based on the single tie node and selected nodes
        '''
        
        inputstr = ''
        inputstr += "*link_multi_tie_type\n"
        inputstr += "%i\n" % int(tietype)       
        inputstr += "*link_multi_tie_rnode 1\n"
        inputstr += "%i\n" % int(tieid)
        inputstr += "*link_multi_tie_n_to_1\n"
        if setname == None:  # if no setname provided, use the current selected
            inputstr += "all_selected\n"
        else:
            inputstr += "%s\n" % setname
        return inputstr 
        
        
    def rbe2(self,tietype,tieid,retnode,tienodelist):
        '''
        create rbe2
        '''
        inputstr = ''
        inputstr += "*new_rbe2\n"  
        inputstr += "*rbe2_name reb2_%s_%s\n" % (tieid,tietype)

        if tietype=='pin':
           inputstr += "*rbe2_tied_dof 1\n"
           inputstr += "*rbe2_tied_dof 2\n"
           inputstr += "*rbe2_tied_dof 3\n"
           
        elif tietype=='fix':
           inputstr += "*rbe2_tied_dof 1\n"
           inputstr += "*rbe2_tied_dof 2\n"
           inputstr += "*rbe2_tied_dof 3\n"
           inputstr += "*rbe2_tied_dof 4\n"
           inputstr += "*rbe2_tied_dof 5\n"
           inputstr += "*rbe2_tied_dof 6\n"
           
        elif tietype=='hinge_X':
           inputstr += "*rbe2_tied_dof 1\n"
           inputstr += "*rbe2_tied_dof 2\n"
           inputstr += "*rbe2_tied_dof 3\n"
           inputstr += "*rbe2_tied_dof 5\n"
           inputstr += "*rbe2_tied_dof 6\n"
           
        elif tietype=='hinge_Z':
           inputstr += "*rbe2_tied_dof 1\n"
           inputstr += "*rbe2_tied_dof 2\n"
           inputstr += "*rbe2_tied_dof 3\n"
           inputstr += "*rbe2_tied_dof 4\n"
           inputstr += "*rbe2_tied_dof 5\n"

        elif tietype=='RX':
           inputstr += "*rbe2_tied_dof 4\n"
           
        inputstr += "*rbe2_ret_node %s\n" % int(retnode)
        
        if type(tienodelist) == type([]):   # nodelist
            for nodeid in tienodelist:
                inputstr += "*add_rbe2_tied_nodes %s # \n" % nodeid
        elif type(tienodelist) == type(''):  # setname
            inputstr += "*add_rbe2_tied_nodes %s # \n" % tienodelist
        else:
            raise TypeError,('for rbe2 tied nodelist shall be list or setname, get',tienodelist)
        inputstr += "#\n"
        return inputstr   

    def  spring(self,tietype,tieid,DOF,retnode,stiff,tienode=None):
        '''
        Create spring,
        Three type, ture-direciton,fixed_dof, and link to ground
        '''
        name = "%s_%s_%s" % ('spring',tieid,tietype)
        inputstr = ''
        inputstr += "*new_link *link_class spring\n"
        inputstr += "*link_name\n"
        inputstr += name + '\n'
        
        if tietype == 'fixed_dof':
    
            inputstr += "*link_class spring *spring_dof 0 %i\n" % DOF
            inputstr += "*link_class spring *spring_dof 1 %i\n" % DOF
            inputstr += "*link_class spring *spring_param stiffness %g\n" % k
            inputstr += "*link_class spring *spring_option spring_type:fixed_dof\n"
            inputstr += "*link_class spring *spring_node 0\n"
            inputstr += "%i\n" % tienode
            inputstr += "%i\n" % int(retnode)
            
        elif tietype == 'true_dir':

  
            inputstr += "*link_class spring *spring_option spring_type:true_dir\n"
            inputstr += "*link_class spring *spring_param stiffness %g\n" % k
            inputstr += "*link_class spring *spring_node 0\n"
            inputstr += "%i\n" % tienode
            inputstr += "%i\n" % int(retnode)
            
        elif tietype == 'to_ground':

            inputstr += "*link_class spring *spring_option spring_type:to_ground\n"
            inputstr += "*link_class spring *spring_dof 0 %i\n" % DOF
            inputstr += "*link_class spring *spring_param stiffness %g\n" % k
            inputstr += "*link_class spring *spring_node 0\n"
            inputstr += "%i\n" % retnode    
        else:
            raise TypeError
        
        inputstr += self.update_springk(name,stiff)
        return inputstr

    def  update_springk(self,name,k):
        '''
        update the spring stiffness based on the spring name
        '''
        inputstr = ''
        inputstr += "*edit_link \n"
        inputstr += name+'\n'
        inputstr += "*link_class spring *spring_param stiffness %g\n" % k
        return inputstr
        
class contacts():
    '''
    class to define the contact body and contact table
    '''
    def __init__(self):
        #self.recorder = recorder
        self.cbody = {}  # contact body library
        self.count = 0
        
    def add_body_deformable(self,name,setname):
        '''
        add deformable contact body as name by the elements in setname 
        '''
        inputstr = ''
        inputstr += "*new_contact_body\n"
        inputstr += "*contact_body_name\n"
        inputstr += '%s\n' % name
        inputstr += "*contact_deformable\n"
        inputstr += "*add_contact_body_elements\n"
        inputstr += "%s\n" % setname
        
        return inputstr
        self.count = self.count+1
        self.cbody[name] = self.count
        
    def add_glue(self,breaktype=None):
        '''
        add glue between contact body
        '''
        inputstr = ''
        inputstr += '*contact_table_option $ctbody1 '
        inputstr += '$ctbody2 contact_type:glue\n'
        
        if breaktype != None:
            inputstr += '*contact_table_option $ctbody1 '
            inputstr += '$ctbody2 glue_separation:breaking\n'
        
        if breaktype == 'tangent':
            inputstr += '*contact_table_option $ctbody1 '
            inputstr += '$ctbody2 breaking_glue_mode:tangential\n'
            
        return inputstr     

            
    def add_glue_prop(self,sig=None,n_sig=None,ta=None,n_ta=None):
        '''
        add glue properties
        '''
        inputstr = ''
        if sig != None:
            inputstr += '*contact_table_property $ctbody1 '
            inputstr += '$ctbody2 breaking_normal_stress\n'
            inputstr += '%s\n' % sig
            if n_sig != None:
                inputstr += '*contact_table_property $ctbody1 '
                inputstr += '$ctbody2 breaking_normal_exp\n'
                nputstr += '%i\n' % n_sig
            else:
                inputstr += '*contact_table_property $ctbody1 '
                inputstr += '$ctbody2 breaking_normal_exp\n'            
                nputstr += '1\n' # default

        if ta != None:
            inputstr += '*contact_table_property $ctbody1 '
            inputstr += '$ctbody2 breaking_tangent_stress\n'
            inputstr += '%g\n' % ta
            if n_ta != None:
                inputstr += '*contact_table_property $ctbody1 '
                inputstr += '$ctbody2 breaking_tangent_exp\n'
                inputstr += '%i\n' % n_ta
            else:
                inputstr += '*contact_table_property $ctbody1 '
                inputstr += '$ctbody2 breaking_tangent_exp\n'           
                inputstr += '1\n' # default
        inputstr += '\n' # default      
        return inputstr
        
    def add_contact_table(self,tablename,name1,name2):
        '''
        Specify the contact table between cbody name1 and name2
        '''
        inputstr = ''
        inputstr += "*new_contact_table\n"
        inputstr += "*contact_table_name\n"
        inputstr += "%s\n" % tablename
        id1 = self.cbody[name1]
        id2 = self.cbody[name2]
        
        inputstr += "*contact_table_entry %s %s\n" % (id1,id2)
        return inputstr


class material():
    '''
    This is the class to define new material
    '''
    def __init__(self):#,recorder):
        pass
        #self.recorder = recorder
        
    def associate_setname(self,matname,setnamelist=None):
        ''' add elements in setname to matname '''
        inputstr = '*edit_mater\n'
        inputstr += '%s\n#\n' % matname
        
        if setnamelist != None and type(setnamelist) == type([]):
            inputstr += '*add_mater_elements\n'
            for setname in setnamelist:
                inputstr += '%s\n' % setname
            inputstr += '#\n'
        return inputstr
        
    def create_elastic(self,name,E,u,mass=0):
        '''
        Create elastic material with modulus E and poisssion'ratio u,mass 
        '''
        inputstr = ''
        inputstr += "*new_mater standard\n"
        inputstr += "*mater_option general:state:solid\n"
        inputstr += "*mater_name\n"
        inputstr += name +'\n'
        inputstr += "*mater_option structural:type:elast_plast_iso\n"
        inputstr += "*mater_param structural:youngs_modulus\n"
        inputstr += "%g\n" % E
        inputstr += "*mater_param structural:poissons_ratio\n"
        inputstr += "%g\n" % u
      
        ## no mass assignment
        if mass !=0:
            inputstr += "*material_value isotropic:mass_density\n"
            inputstr += '%f\n' % mass
            
        return inputstr
    
    def low_tension(self,name,E,u,ft,Es,epsilon,shear):
        '''
        Create the low tension concrete material
        '''
        self.create_elastic(name,E,u)
        inputstr = ''
        inputstr += "*material_type damage:cracking\n"
        inputstr += "*material_value cracking:stress\n"
        inputstr += "%g \n %g \n %g \n %g \n #\n" % (ft,Es,epsilon,shear)

        return inputstr
    
    def plasticity(self,name,E,u,fy,tablename=None):
        '''
        create the plasticity material with yielding stress fy and.or harding
        table
        '''
        
        inputstr = self.create_elastic(name,E,u)
        inputstr += "*mater_option structural:plasticity:on\n"
        inputstr += "*mater_param structural:yield_stress\n"
        inputstr += "%g\n" % fy
        
        if tablename != None:
            inputstr += "*mater_param_table structural:yield_stress\n"
            inputstr += "%s\n" % tablename
        
        return inputstr
    
    def interface_cohesive(self,key,mat):
    
        exp = '*new_mater interface *mater_option general:state:solid\n'
        exp += '*mater_name\n'
        exp += '%s\n' % key
        exp += '*mater_option structural:interf_model:%s\n' % mat.mattype
        exp += '*mater_param structural:cohesive_energy\n'
        exp += '%s\n' % mat.Gc
        exp += '*mater_param structural:interf_crit_opening_disp\n'
        exp += '%s\n' % mat.vc
        exp += '*mater_param structural:interf_shr_nrml_wght_coeff\n'
        exp += '%s\n' % mat.s_n
        exp += '*mater_param structural:interf_shr_nrml_wght_coeff_c\n'
        exp += '%s\n' % mat.s_n_c
        exp += '*mater_param structural:interf_stiff_fact_comp\n'
        exp += '%s\n' % mat.stiff_c
        
        if mat.mattype == 'linear':
            exp += '*mater_param structural:interf_max_opening_disp\n'
            exp += '%s\n' % mat.vm
        elif mat.mattype == 'linear_exp':
            exp += '*mater_param structural:interf_exp_decay_factor\n'
            exp += '%s\n' % mat.q               
        return exp

    def failure_maxstress(self,name,E,u,maxtx=None,maxcx=None,
                                        maxty=None,maxcy=None,
                                        maxtz=None,maxcz=None,
                                        maxsxy=None,maxsyz=None,maxszx=None):
        '''
        add failure criterion of maximum stress, mainly used with FRPs
        '''
        inputstr = ''
        inputstr += self.create_elastic(name,E,u)
        inputstr += "*mater_option structural:damage:on\n"
        inputstr += "*mater_option structural:damage_type:failure\n"
        inputstr += "*mater_option structural:fail_criterion1:max_stress\n"

        # add maximum stress limits based on the input parameters
        if maxtx != None:
            inputstr += "*mater_param structural:fail_max_tens_strs_x\n"
            inputstr += ("%f\n") % maxtx

        if maxcx != None:
            inputstr += "*mater_param structural:fail_max_compr_strs_x\n"
            nputstr += ("%f\n") % maxcx

        if maxty != None:
            inputstr += "*mater_param structural:fail_max_tens_strs_y\n"
            inputstr += ("%f\n") % maxty

        if maxcy != None:
            inputstr += "*mater_param structural:fail_max_compr_strs_y\n"
            inputstr += ("%f\n") % maxcy
        if maxtz != None:
            inputstr += "*mater_param structural:fail_max_tens_strs_z\n"
            inputstr += ("%f\n") % maxtz
        if maxcz != None:
            inputstr += "*mater_param structural:fail_max_compr_strs_z\n"
            inputstr += ("%f\n") % maxcz
        if maxsxy != None:
            inputstr += "*mater_param structural:fail_max_shr_strs_xy\n"
            inputstr += ("%f\n") % maxsxy
        if maxsyz != None:
            inputstr += "*mater_param structural:fail_max_shr_strs_yz\n"
            inputstr += ("%f\n") % maxsyz
        if maxszx != None:
            inputstr += "*mater_param structural:fail_max_shr_strs_zx\n"
            inputstr += ("%f\n") % maxszx
        inputstr += "\n"
        return inputstr 
        
class geometry():
    '''
    class of define the geometry
    '''
    def __init__(self):##:,recorder):
        pass
        #self.recorder = recorder

    def associate_setname(self,matname,setnamelist=None):
        ''' add elements in setname to matname '''
        inputstr = '*edit_geometry\n'
        inputstr += '%s\n#\n' % matname
        
        if setnamelist != None and type(setnamelist) == type([]):
            inputstr += '*add_geometry_elements\n'
            for setname in setnamelist:
                inputstr += '%s\n' % setname
            inputstr += '#\n'
        return inputstr

    def truss3d(self,name,area):
        '''
        geomery of 3D truss
        input parameter; Area of truss
        '''
        inputstr = ''
        inputstr += "*new_geometry\n"
        inputstr += "*geometry_name %s\n" % name
        inputstr += "*geometry_type mech_three_truss\n"
        inputstr += "*geometry_param area\n"
        inputstr += "%g\n" % area
        return inputstr
        
    def beam3d(self,name,Area,Ixx,Iyy,vec,tstiff=0,xshear=0,yshear=0):
        '''
        Geomerty of 3d beam
        input parameter: Area
                         Ixx: second moment of inertia in y-y axis
                         Iyy: second moment of inertia in x-x axis
                         Vec: orientation vec
                         tstiff: tortional stiffness
                         xshear: effective shear resistance area in x direction
                         yshear: effective shear resistance area in y direction
        '''
        inputstr = ''
        
        inputstr += "*new_geometry\n"
        inputstr += "*geometry_name %s\n" % name

        inputstr += "*geometry_type mech_three_beam_ela\n"
        
        inputstr += "*geometry_value area\n"
        inputstr += "%g\n" % Area
        
        inputstr += "*geometry_value ixx\n"
        inputstr += "%s\n" % Ixx
        
        inputstr += "*geometry_value iyy\n"
        inputstr += "%s\n" % Iyy
        
        inputstr += "*geometry_value orientx\n"
        inputstr += "%s\n" % vec[0]
        inputstr += "*geometry_value orienty\n"
        inputstr += "%s\n" % vec[1]
        inputstr += "*geometry_value orientz\n"
        inputstr += "%s\n" % vec[2]
        

        if tstiff != 0 or xshear != 0 or yshear != 0:
            inputstr += "*geometry_option addprops:on\n"
            
        if tstiff != 0:
            inputstr += "*geometry_value tstiff\n"
            inputstr += "%g #\n" % tstiff   ### this is the torsional inertia
            
            
        if xshear != 0:
            inputstr += "*geometry_value tsareax\n"
            inputstr += "%g #\n" % xshear   ### this is the effective shear resistant area
            
            
        if yshear != 0:
            inputstr += "*geometry_value tsareay\n"
            inputstr += "%g #\n" % yshear
                 
        return inputstr
    
    def shell(self,name,thickness):
        '''
        Geometry of 3d shell
        input parameter: thickness
        '''
        
        inputstr = ''
        inputstr += "*new_geometry\n"
        
        inputstr += "*geometry_name %s\n" % name
        
        inputstr += "*geometry_type mech_three_shell\n"
        inputstr += "*geometry_value thick\n"
        inputstr += "%s\n" % thickness
        
        return inputstr
    
    def planestress(self,name,thickness):
        '''
        Geometry of planestress case
        input parameter: thickness
        '''
        inputstr = ''
        inputstr += "*new_geometry\n"
        inputstr += "*geometry_name %s\n" % name
        inputstr += "*geometry_type mech_planar_pstress\n"
        inputstr += "*geometry_param norm_to_plane_thick\n"
        inputstr += "%s\n" % thickness
        return inputstr    

    def straightbeam2d(self,name,h,A):
        '''
        geomerty of 2d straight beam
        input parameter: h: height
                         A: area
        '''
        inputstr = ''
        inputstr += "*new_geometry\n"
        inputstr += "*geometry_name %s\n" % name
        inputstr += "*geometry_type mech_planar_beam_str\n"
        inputstr += "*geometry_param height\n"
        inputstr += "%f\n" % h
        inputstr += "*geometry_param area\n"
        inputstr += "%f\n" % A
        return inputstr     
            
    def axisym_solid(self,name):
        '''
        Geometery of axisy symmetric solid
        '''
        inputstr = ''
        inputstr += "*new_geometry\n"
        inputstr += "*geometry_name %s\n" % name
        inputstr += "*geometry_type mech_axisym_solid\n"
        return inputstr
        
class bond_load():
    '''
    class for create boundary conditions including the loads
    '''
    def __init__(self):# ,recorder):
        pass
        #self.recorder = recorder
        
    def associate_setname(self,bondname,setnamelist=None):
        ''' add elements in setname to matname '''
        inputstr = '*edit_apply\n'
        inputstr += '%s\n#\n' % bondname
        
        if setnamelist != None and type(setnamelist) == type([]):
            inputstr += '*add_apply_nodes\n'
            for setname in setnamelist:
                inputstr += '%s\n' % setname
            inputstr += '#\n'
        return inputstr

    def associate_nodelist(self,bondname,nodelist=None):
        ''' add elements in setname to matname '''
        inputstr = '*edit_apply\n'
        inputstr += '%s\n#\n' % bondname
        
        if nodelist != None and type(nodelist) == type([]):
            inputstr += '*add_apply_nodes\n'
            for node in nodelist:
                inputstr += '%s ' % node
            inputstr += '#\n'
        return inputstr
    
    def support(self,name,coord):
        '''
        create nodal support for selected nodes based on input coords
        coords: 1 for restained, None for free
        '''
        inputstr = ''
        inputstr += "*new_apply\n"

        inputstr += "*apply_name\n %s \n" % (name)

        inputstr += "*apply_type fixed_displacement\n"
        
        if coord[0]==1:
            inputstr += "*apply_dof x\n"
            inputstr += "*apply_dof_value x %g\n" % 0
            
        if coord[1]==1:
            inputstr += "*apply_dof y\n"
            inputstr += "*apply_dof_value y %g\n" % 0
            
        if coord[2]==1:
            inputstr += "*apply_dof z\n"
            inputstr += "*apply_dof_value z %g\n" % 0
            
        if coord[3]==1:
            inputstr += "*apply_dof rx\n"
            inputstr += "*apply_dof_value rx %g\n" % 0
            
        if coord[4]==1:
            inputstr += "*apply_dof ry\n"
            inputstr += "*apply_dof_value ry %g\n" % 0
        
        if coord[5]==1:
            inputstr += "*apply_dof rz\n"
            inputstr += "*apply_dof_value rz %g\n" % 0
        return inputstr


    def apply_table(self,tablename,label):
        inputstr  = ''
        if tablename != None:  # apply table
            inputstr += '*apply_dof_table ' + label +'\n'
            inputstr += '%s\n' % tablename        

            
        return inputstr
        
    def disp(self,name,label,value,tablename=None):
        '''
        create nodal support for selected nodes based on input coords
        coords: 1 for restained, None for free
        '''
        inputstr = ''
        inputstr += "*new_apply\n"

        inputstr += "*apply_name\n %s \n" % (name)

        inputstr += "*apply_type fixed_displacement\n"
        
        if 'x' in label:
            inputstr += "*apply_dof x\n"
            inputstr += "*apply_dof_value x %g\n" % value
            inputstr += self.apply_table(tablename,'x')
            
        if 'y' in label:
            inputstr += "*apply_dof y\n"
            inputstr += "*apply_dof_value y %g\n" % value
            inputstr += self.apply_table(tablename,'y')
            
        if 'z' in label:
            inputstr += "*apply_dof z\n"
            inputstr += "*apply_dof_value z %g\n" % value
            inputstr += self.apply_table(tablename,'z')
            
        if 'rx' in label:
            inputstr += "*apply_dof rx\n"
            inputstr += "*apply_dof_value rx %g\n" % value
            inputstr += self.apply_table(tablename,'rx')
            
        if 'ry' in label:
            inputstr += "*apply_dof ry\n"
            inputstr += "*apply_dof_value ry %g\n" % value
            inputstr += self.apply_table(tablename,'ry')
            
        if 'rz' in label:
            inputstr += "*apply_dof rz\n"
            inputstr += "*apply_dof_value rz %g\n" % value
            inputstr += self.apply_table(tablename,'rz')

        return inputstr
    
    def pointload(self,name,label,load,tablename=None):
        '''
        add pointload on selected node groups
        input parameters load: load mangnitude
                        label: load DOFs
                        table: time history of the loads
        '''
        inputstr = ''        
        inputstr += "*new_apply\n"
        inputstr += "*apply_name\n %s\n" % name

        inputstr += "*apply_type point_load\n"
        
        if 'x' in label or 'X' in label:
            inputstr += "*apply_dof x *apply_dof_value x %g\n" % load
        
        if 'y' in label or 'Y' in label:
            inputstr += "*apply_dof y *apply_dof_value y %g\n" % load

        if 'z' in label or 'Z' in label:
            inputstr +=  "*apply_dof z *apply_dof_value z %g\n" % load
        
        if tablename != None:  # apply table
            inputstr += '*apply_dof_table ' + label[0] +'\n'
            inputstr += '%s\n' % tablename
        return inputstr
        
class loadcase():
    '''
    class to define the load case, and select the boundaries
    '''
    def __init__(self):#,recorder):
        pass
        #self.recorder = recorder
    
    def create(self,name):
        '''
        create new load case
        '''
        inputstr = ''
        inputstr += "*new_loadcase\n"
        inputstr += "*loadcase_name\n"
        inputstr += name +'\n'
        inputstr += '*clear_loadcase_loads\n'
        return inputstr
    
    def create_static_fixed(self,name,nstep=1):
        '''
        create load analysis with fixed time increment
        '''
        
        inputstr = self.create(name)
        inputstr += "*loadcase_type struc:static\n"
        inputstr += "*loadcase_option stepping:fixed\n"
        inputstr += "*loadcase_value nsteps\n %i\n" % nstep
        return inputstr
    
    def create_multi(self,name):
        '''
        create load analysis with multi-criterion stepping scheme
        '''
        
        inputstr = self.create(name)
        inputstr += "*loadcase_type struc:static\n"
        inputstr += "*loadcase_option stepping:multicriteria\n"
        return inputstr
        
    def create_arclength(self,name,nstep=50):
        '''
        create load analysis with arc-length scheme
        '''
        
        inputstr = self.create(name)
        inputstr += "*loadcase_type struc:static\n"
        inputstr += "*loadcase_option stepping:arclength\n"
        inputstr += "*loadcase_value maxinc\n%i#\n" % (nstep)
        return inputstr
        
    def create_dynmodel(self,name,lowfreq=0,nmode=10):
        '''
        create nmode mode shape that above the lowfreq
        '''
        
        inputstr = self.create(name)
        inputstr += "*loadcase_type struc:dyn_modal\n"
        inputstr += "*loadcase_value low %f \n"  % lowfreq
        inputstr += "*loadcase_value nmodes %i \n"  % nmode
        return inputstr
        
    def create_buck(self,name):
        '''
        create bucking analysis case
        '''
        inputstr = self.create(name)
               
        inputstr += "*loadcase_type struc:buckle\n"
        return inputstr
    
    def select_load(self,name,bondlist,clear='No'): 
        '''
        select boundary conditions into load cases
        '''
        inputstr = ''   
        inputstr += "*edit_loadcase\n"
        inputstr += name +'\n'
        
        #delete all esxisting bond
        if clear=='yes':
            inputstr += "*clear_loadcase_loads\n"
        
        
        ##add bondlist
        for j in range(0,len(bondlist)):
            inputstr += "*add_loadcase_loads %s\n" % bondlist[j]

        return inputstr
        
    def add_contacttable(self,ctablename):
        '''
        add contact table to the load case
        '''
        inputstr = ''
        inputstr += "*loadcase_ctable\n"
        inputstr += "%s\n" % ctablename
        return inputstr
        
class jobop():
    '''
    class to define jobs
    '''
    def __init__(self):#,recorder):
        pass
        #self.recorder = recorder
    
    def create_basic(self,name,dim='3D'):
        '''
        create basic job, default in 3D
        '''
        inputstr = ''
        inputstr += "*new_job\n"
        
        if name != None:
            inputstr += "*job_name\n"
            inputstr += name +'\n'
            inputstr += '*job_option post:both\n'  # add *.t19 to result file
            inputstr += '*job_option echo_coordinates:on\n'  # add coordinates to *.t19 to result file
            inputstr += '*job_option echo_connectivity:on\n'  # add connectivity*.t19 to result file
            
        if dim == '3D':
            inputstr += "*job_option dimen:three\n"
        elif dim == 'axisym':
            inputstr += "*job_option dimen:axisym\n"
            
        return inputstr
    
    def create_general(self,name,lcasename=None,elastic=0,dim='3D'):
        '''
        create general job with selection of load cases
        input parameters  lcasename: set of the load case
                          elastic : switch for an elastic analysis
                          dim: problem dimensions 
        '''
       
        inputstr =  self.create_basic(name,dim=dim)   
        inputstr += "*job_class structural\n"
        inputstr += self.add_loadcase(name,lcasename)
        inputstr += "*clear_job_applys\n"
        if elastic == 1:
            inputstr += "*job_option elastic:on\n"
        return inputstr
    
    def create_dyn(self,name,lcasename):
        '''
        create dynamic analysis job
        '''
        inputstr = ''
        inputstr += self.create_basic(name)
        inputstr += self.add_loadcase(name,lcasename)
        return inputstr     

    
    def add_loadcase(self,name,lcasename):
        '''
        add load case to the job
        '''
        inputstr = ''
        inputstr += "*edit_job\n"
        inputstr += name +'\n'
        for i in range(0,len(lcasename)):
            inputstr += "*add_job_loadcases %s\n"  % lcasename[i]
        return inputstr
    
    def initialcond(self,name,bondlist):
        '''
        add initial condition to job
        '''
        inputstr = ''
        inputstr += "*edit_job\n"
        inputstr += name +'\n'
        
        for j in range(0,len(bondlist)):
            inputstr += "*add_job_applys %s\n" % bondlist[j]
        return inputstr
    
    def extend_requestresults(self,req):
        require = []
        if req == 'total_strain':
            require.extend(["strain_1","strain_2","strain_3","strain_4","strain_5","strain_6"])
        if req == 'elastic_strain':
            require.extend(["el_strain_1","el_strain_2","el_strain_3","el_strain_4","el_strain_5","el_strain_6"])
        if req == 'plastic_strain':
            require.extend(["pl_strain_1","pl_strain_2","pl_strain_3","pl_strain_4","pl_strain_5","pl_strain_6"])
        if req == 'crack_strain':    
            require.extend(["ck_strain_1","ck_strain_2","ck_strain_3","ck_strain_4","ck_strain_5","ck_strain_6"])
        if req == 'stress':
            require.extend(["stress_1","stress_2","stress_3","stress_4","stress_5","stress_6"])
        if req == 'beam internal':
            require.extend(["bm_axi_for","bm_bnd_mom_x","bm_bnd_mom_y","bm_tor_mom","bm_shr_for_x","bm_shr_for_y"])
        
        return require
    
    
    def req_result(self,key,reqlist):
        '''
        Make special results requests
        '''
        require=[]
        inputstr = ''
        inputstr += "*edit_job\n"
        inputstr += key +'\n'
        
        for req in reqlist:
            require.extend(self.extend_requestresults(req))
      
        for i in range(0,len(require)):
            inputstr += "*add_post_var\n "
            inputstr += "%s \n" % require[i]
        return inputstr
    
    def submit_job(self,name):
        '''
        submit a job
        '''
        inputstr = "*save_as_model model1.mud yes\n"
        inputstr += "*edit_job\n"
        inputstr += name +'\n'
        inputstr += "*submit_job 1 *monitor_job\n"
        
        #inputstr += "*post_open_default\n"
        return inputstr     
   
class post():
    '''
    class of defining the post process 
    '''
    def __init__(self):#,recorder):
        pass
        #self.recorder = recorder

    def open_default(self):
        '''
        open default t16 result files
        '''
        inputstr = ''
        inputstr += "*post_open_default\n"
        return inputstr
    
    def loadcolorscheme(self,colorschemename=None):
        '''
        Load color scheme for display and figure export prupose 
        '''
        
        inputstr = ''
        inputstr += '*load colors\n'
        inputstr += colorschemename +'\n'
        
        return inputstr

    def add_node(self,node):
        '''
        add node to sampling list
        '''
        inputstr = ''
        inputstr += "*add_sample_points\n"
        inputstr += '%s\n' % node
        return inputstr
    
    
    def add_node_setname(self,setname):
        '''
        add node to sampling list
        '''
        inputstr = ''
        inputstr += "*add_sample_points\n"
        inputstr += '%s\n' % setname
        return inputstr
        
    def collect_data(self,start,end,incr):
        '''
        collect results for the sampling nodes
        '''
        inputstr = ''
        inputstr += "*history_collect %i %i %i\n" % (start,end,incr)
        
    def draw_time_node(self,nodeid,quantity,start=1,end=99999,incr=1):
        '''
        draw the time history plots
        '''
        inputstr = ''
        inputstr += "*set_history_locations"
        inputstr += "%i\n\n" % nodeid
        inputstr += "*history_collect %i %i %i\n" % (start,end,incr)
        inputstr += "*history_add_location"
        inputstr += "n:%i\n" % nodeid
        inputstr += "Time\n"
        inputstr += "%s\n" % quantity
        return inputstr

    def draw_loc1_loc2(self,filename,nodeid1,item1,nodeid2,item2,start=1,end=99999,incr=1):
        '''
        draw the time history plots
        '''
        xyplot = xy_plot()
        inputstr = ''
        inputstr += "*set_history_locations"
        inputstr += "%i %i\n\n" % (nodeid1,nodeid2)
        inputstr += "*history_collect %i %i %i\n" % (start,end,incr)
        inputstr += "*history_add_loc_vs_loc"
        inputstr += "n:%i\n%s\n" % (nodeid1,item1)
        inputstr += "n:%i\n%s\n" % (nodeid2,item2)
        inputstr += "*history_fit\n"
        
        inputstr += xyplot.addexport('history',filename)
        return inputstr
    
    def match(self,type,DOF):
        if type == 'stress':
            if DOF == 1:
                return '1st Comp of Stress'
            elif DOF == 2:
                return '2nd Comp of Stress'
            elif DOF == 3:
                return '3rd Comp of Stress'
            elif DOF == 4:
                return '4th Comp of Stress'
            elif DOF == 5:
                return '5th Comp of Stress'
            elif DOF == 6:
                return '6th Comp of Stress'
        if type == 'strain':
            if DOF == 1:
                return '1st Comp of Total Strain'
            elif DOF == 2:
                return '2nd Comp of Total Strain'
            elif DOF == 3:
                return '3rd Comp of Total Strain'
            elif DOF == 4:
                return '4th Comp of Total Strain'
            elif DOF == 5:
                return '5th Comp of Total Strain'
            elif DOF == 6:
                return '6th Comp of Total Strain'            

        if type == 'strain':
            if DOF == 1:
                return '1st Comp of Total Strain'
            elif DOF == 2:
                return '2nd Comp of Total Strain'
            elif DOF == 3:
                return '3rd Comp of Total Strain'
            elif DOF == 4:
                return '4th Comp of Total Strain'
            elif DOF == 5:
                return '5th Comp of Total Strain'
            elif DOF == 6:
                return '6th Comp of Total Strain'
        if type == 'disp':
            if DOF == 1:
                return 'Displacement X'
            elif DOF == 2:
                return 'Displacement Y'
            elif DOF == 3:
                return 'Displacement Z'
           
    def draw_loc(self,filename,nodeid,type,DOF,start=1,end=99999,incr=1):
        '''
        draw the time history plots
        '''
        xyplot = xy_plot()
        inputstr = ''
        inputstr += "*set_history_locations\n"
        inputstr += "%i\n#\n" % (nodeid)
        inputstr += "*history_collect %i %i %i\n" % (start,end,incr)
        inputstr += "*history_add_loc_vs_loc\n"
        inputstr += "n:%i\n%s\n" % (nodeid,'Time')
        inputstr += "n:%i\n%s\n" % (nodeid,self.match(type,DOF))
        inputstr += "*history_fit\n"
        
        inputstr += xyplot.addexport('history',filename)
        return inputstr

class xy_plot():
    def __init__(self):
        pass
    
    def add(self,itemtype):
        exp = ''
        if itemtype == 'history':
            exp += '*get_history_plots\n'
        elif itemtype == 'path':
            exp += '*get_path_plots\n'
        elif itemtype == 'table':
            exp += '*get_table_plots\n'
        return exp
        
    def clear(self):
        exp = ''
        exp += '*xy_plot_clear\n'
        return exp
    
    def export(self,filename):
        exp = ''
        exp += '*xy_plot_export %s yes\n' % filename
        return exp
    
    def addexport(self,itemtype,file):
        exp = ''
        exp += self.clear()
        exp += self.add(itemtype)
        exp += self.export(file)
        exp += self.clear()
        return exp