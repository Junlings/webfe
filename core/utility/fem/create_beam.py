#!/usr/bin/env python
from create_single_line_nodelist import create_single_line_nodelist
from ../section/create_section import 

def create_model_twopoint_reinforced(model,paradict):
    ''' create one dimensional beam model with
    '''
    
    span = paradict['span']
    nseg = paradict['nseg']
    
    
    # create grid and connectivity
    model.node([[0,0,0],[span,0,0]])
    model = create_single_line_nodelist(model,1,2,nseg)
    
    
    


    
    # Create the boundary
    bond_left = bond([1],xyz=[0,1,0,0,0,0],DOF=3,type='bond')
    bond_right = bond([2],xyz=[1,1,0,0,0,0],DOF=3,type='bond')
    
    blist = bondlist()
    blist.add(bond_left)
    blist.add(bond_right)
    
    print [float(span)/3.0,float(span)/2.0]
    nodelist_loadleft = grid.search('coord',{'x':[float(span)/3.0,float(span)/3.0]})
    nodelist_loadright = grid.search('coord',{'x':[float(span)*2.0/3.0,float(span)*2.0/3.0]})
    nodelist_middle = grid.search('coord',{'x':[float(span)/2.0,float(span)/2.0]})
    
    #print grid.export()
    
    load_all = bond([nodelist_loadleft,nodelist_loadright],xyz=[0,1.0,0,0,0,0],scalar=0.5,type='load',DOF=3)
    loadlist1 = loadlist(load_all)
    
    rec1 = item_node_disp([nodelist_middle],prop={'header':'ana','unit':'kip','DOF':2,'recfile':'data/res'})
    reclist1 = recorder(rec1)
    
    
    for i in range(1,Integ+1):
        temp = record_section(section,conn.connlist.keys(),i,mode=[1,100,101])
        reclist1.add(temp)

    
    node_seq =  nodelist_middle.coord.keys()[0]
    ana1 = analysis(integrator_ctl=node_seq,integrator_dof=2,run_step=200,integrator_inc=0.01)
    
    # initialize the model
    prj1 = project(ndm=2,ndf=3)
    prj1.assemble({'coordlist':grid,
                 'connlist':conn,
                 'bondlist':[bond_right,bond_left],
                'orientlist':olist1,
                'loadlist':loadlist1,
                'matlib':materiallist,
                'seclib':section,
                'proplib':prop1,
                'reclist':reclist1})
    prj1.add('ana',ana1)
    return prj1


if __name__ == '__main__':
    pass