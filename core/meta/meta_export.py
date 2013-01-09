#!/usr/bin/env python
""" This is defination of the meta-class for all model export class"""

def ex_coord(obj,EXF,coordlist):
    ''' function to export coordinates, call ex_coord_single for each model'''
    for seq in coordlist.seqlist:
        node = coordlist.itemlib[seq]
        EXF.write(obj.ex_coord_single(node))

def ex_commands(obj,EXF,command,model):
    ''' export settings '''
    EXF.write(obj.ex_commands_single(command,model))
    
def ex_settings(obj,EXF,settings):
    ''' export settings '''
    EXF.write(obj.ex_settings_single(settings))
    
def ex_conn(obj,EXF,connlist):
    '''export connectivity '''
    for seq in connlist.seqlist:
        conn = connlist.itemlib[seq]
        EXF.write(obj.ex_conn_single(conn))
    


def ex_conn_prop(obj,EXF,connlist,paralist):
    ''' export element properties '''
    for seq in connlist.seqlist:
        conn = connlist.itemlib[seq]
        try:
            proptype = paralist[conn.property]
        except:
            proptype = None
        EXF.write(obj.ex_conn_prop_single(conn,proptype))
        
def ex_orient(obj,EXP,orientlist,dkey=None):
    ''' export orientation list'''
    if dkey == None:
        
        for key in orientlist.keys():
            orient = orientlist[key]
            EXP.write(obj.ex_orient_single(key,orient))
        return EXP
    else:
        orient = orientlist[dkey]
        EXP.write(obj.ex_orient_single(dkey,orient))
        return EXP
    
def ex_itemset(obj,EXP,setlist,dkey=None):
    if dkey == None:
        for key in setlist.keys():
            itemset = setlist[key]
            EXP.write(obj.ex_itemset_single(key,itemset))
        return EXP
    else:
        itemset = setlist[dkey]
        EXP.write(obj.ex_itemset_single(dkey,itemset))
        return EXP
            

def ex_mat(obj,EXP,matlist,dkey=None,keylist=None):
    ''' export material properity '''
    
    if keylist == None:
        keylist = matlist.keys()
    if dkey == None:
        for key in keylist:
            mat = matlist[key]
            EXP.write(obj.ex_mat_single(key,mat))
        return EXP
    else:
        mat = matlist[dkey]
        EXP.write(obj.ex_mat_single(dkey,mat))
        return EXP
    
def ex_prop(obj,EXP,proplist,dkey=None):
    ''' export property '''
    if dkey == None:
        for key in proplist.keys():
            prop = proplist[key]
            EXP.write(obj.ex_prop_single(key,prop))
        return EXP
    else:
        prop = proplist[dkey]
        EXP.write(obj.ex_prop_single(dkey,prop))
        return EXP
    
def ex_sec(obj,EXP,seclist,matlist,dkey=None,mode='yz'):
    ''' export section properties '''
    
    if dkey == None:
        for key in seclist.keys():
            sec = seclist[key]
            try:
                mat = matlist[sec.mattag]
                EXP.write(obj.ex_sec_single(key,sec,mat,mode=mode))
            except:
                EXP.write(obj.ex_sec_single(key,sec,mode=mode))
    else:
        sec = seclist[dkey]
        EXP.write(obj.ex_sec_single(dkey,sec,mode=mode))
        
        '''
        if sec.mattag != None:
            mat = matlist[sec.mattag]
            EXP.write(obj.ex_sec_single(dkey,sec,mat))
        else:
            EXP.write(obj.ex_sec_single(dkey,sec))
        '''
    return EXP
    
def ex_para(obj,EXP,paralist):
    ''' export parameters '''
    for key in paralist.keys():
        para = paralist[key]
        EXP.write(obj.ex_para_single(key,para))        

def ex_recorder(obj,EXP,reclist,dkey=None):
    ''' export parameters '''
    if dkey == None:
        for key in reclist.keys():
            rec = reclist[key]
            EXP.write(obj.ex_recorder_single(key,rec))               
    else:
        rec = reclist[dkey]
        EXP.write(obj.ex_recorder_single(dkey,rec))        
    return EXP        
                
def ex_bonds(obj,EXP,bondlist,dkey=None):
    if dkey == None:
        for key in bondlist.keys():
            bond = bondlist[key]
            EXP.write(obj.ex_bond_single(key,bond))        
    else:
        bond = bondlist[dkey]
        EXP.write(obj.ex_bond_single(dkey,bond))          
    return EXP

def ex_nodaltie(obj,EXP,nodaltielist,dkey=None):
    if dkey == None:
        for key in nodaltielist.keys():
            nodaltie = nodaltielist[key]
            EXP.write(obj.ex_nodaltie_single(key,nodaltie))        
    else:
        nodaltie = nodaltielist[dkey]
        EXP.write(obj.ex_nodaltie_single(dkey,nodaltie))          
    return EXP

def ex_loadcases(obj,EXP,loadcaselist,dkey=None):
    if dkey == None:
        for key in loadcaselist.keys():
            loadcase = loadcaselist[key]
            EXP.write(obj.ex_loadcase_single(key,loadcase))        
    else:
        loadcase = loadcaselist[dkey]
        EXP.write(obj.ex_loadcase_single(dkey,loadcase))          
    return EXP

def ex_jobs(obj,EXP,joblist,dkey=None):
    if dkey == None:
        for key in joblist.keys():
            job = joblist[key]
            EXP.write(obj.ex_job_single(key,job))        
    else:
        job = joblist[dkey]
        EXP.write(obj.ex_job_single(dkey,job))          
    return EXP

def ex_variables(obj,EXP,lib):
    ''' export variables '''
    count_i = 1
    for key in lib.keys():
        EXP.write(obj.ex_variable_single(key,count_i))
        count_i += 1
        
class metacls_export(type):
    registered = {}
    def __new__(meta, classname, supers, classdict):
        
        # define export function
        classdict['ex_coord']    = ex_coord
        classdict['ex_conn']     = ex_conn  # export only connecivitty
        classdict['ex_conn_prop']     = ex_conn_prop # export conn and prop
        classdict['ex_mat']      = ex_mat
        classdict['ex_sec']      = ex_sec
        classdict['ex_orient']   = ex_orient
        classdict['ex_itemset'] = ex_itemset
        classdict['ex_para']     = ex_para
        classdict['ex_prop']     = ex_prop
        classdict['ex_settings']     = ex_settings
        classdict['ex_variables']     = ex_variables
        classdict['ex_bonds']     = ex_bonds
        classdict['ex_commands']     = ex_commands
        classdict['ex_nodaltie']     = ex_nodaltie
        classdict['ex_recorder']     = ex_recorder
        classdict['ex_loadcases']     = ex_loadcases
        classdict['ex_jobs']     = ex_jobs
        newtype = type.__new__(meta, classname, supers, classdict)
        meta.registered[classname] = newtype
        
        return newtype
    
    @classmethod
    def class_by_name(cls, name):
        # get a class from the registerd classes
        return cls.registered[name]  