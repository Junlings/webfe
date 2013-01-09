from __future__ import division
from utility.fem.create_single_line_nodelist import create_single_line_nodelist



def twopoint_bending(model,secname,LL,totalload,ne,percenta=48.0/14.0,percentb=48.0/20.0,itype='Displacement',nstep=500, incr=-0.005):
    ''' generate the bending material model
    scename: predefined section name
    LL:  total length of the beam
    totalload: totalload applied
    ne: segments of the beam
    percenta: load point location
    percentb: second load point location
    
    '''
    model.node([[0,0,0], [LL,0,0]])
    model.settings['ndm'] = 2
    model.settings['ndf'] = 3
    
    create_single_line_nodelist(model,1,2,ne)
    
    model.bond('left',{'nodelist':[1],'xyz':[1,1,0],'DOF':3})
    model.bond('right',{'nodelist':[2],'xyz':[0,1,0],'DOF':3})
    
    err = 0.01
    n1 = model.nodelist.select_node_coord(rx=[float(LL)/percenta-err,float(LL)/percenta+err])
    n2 = model.nodelist.select_node_coord(rx=[float(LL)/percenta+float(LL)/percentb-err,float(LL)/percenta+float(LL)/percentb+err])
    nc = model.nodelist.select_node_coord(rx=[float(LL)/2-err,float(LL)/2+err])
    
    model.load('load',{'nodelist':[list(n1)[0],list(n2)[0]],'xyz':[0,0.5,0],'DOF':3,'scalar':totalload/2})
    #model.load('load',{'nodelist':[list(nc)[0]],'xyz':[0,1,0],'DOF':3,'scalar':totalload/2})
    
    #model.load(
    #print n1,n2
    model.orient('orient1','orient_linear',{})
    
    model.property('prop1','line2',{})
    
    #model.link_mat_prop
    model.link_sec_prop(secname,'prop1')
    model.link_orient_prop('orient1','prop1')
    model.link_prop_conn('prop1','ALL')
    
    
    model.recorder('mid_defl','his_disp',{'DOF':2,'nodelist':list(nc),'recfile':model.settings['prjname']+'//'+'disp'})
    
    model.loadcase('loadcase1','static',{'itype':itype,'nstep':nstep,'ctrlnodeid':list(nc)[0],'incr':incr})
    model.job('job1','static_job',{})


    return model
    