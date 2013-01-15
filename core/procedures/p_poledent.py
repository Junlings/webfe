from __future__ import division
#import os
import numpy as np

from core.model.registry import model
from core.settings import settings
from core.lib.libop import save, load
from core.export.export import exporter
from core.utility.geometry.circle_fit import circle_fit,find_circlecenter
from core.utility.geometry.DistancePointLine import DistancePointLine,UdirectionPointLine, Parameter,Find_angle
from core.imports.marc.import_marc_dat import importfile_marc_dat
from core.utility.table.stress_strain import add_mat_by_stressstrain
from math import atan



def pole_contact_plate(model1,name,centercoord,length,width,plateyloc,stiffness,spring=True):
    """ This procedure add the contact plate in the model for use as either support or loading
         name: plate set name
         centercoord: center coordinates of the plate center [x,y,z]
         length: length of contact plate in x direction
         width: widtb of the contact plate in y direction
         platezloc: location of the plate
         stiffness: stiffness of the connection springs
    """
    
    #  searchig the connecting nodes
    xcenter,ycenter,zcenter = centercoord
    xmin = xcenter - length/2.0
    xmax = xcenter + length/2.0
    ymin = min(ycenter,plateyloc)
    ymax = max(ycenter,plateyloc)
    zmin = zcenter - width/2.0
    zmax = zcenter + width/2.0
    
    pnodelist = model1.nodelist.select_node_coord([xmin,xmax],[ymin,ymax],[zmin,zmax])
    model1.nodeset(name,{'nodelist':pnodelist})
    
    
    if spring:
        #  add additonal nodes on plate and create springs
        nodecoordlist = []
        for nodeseq in pnodelist:
            xyz = model1.nodelist.itemlib[nodeseq].xyz
            nodecoordlist.append([xyz[0],plateyloc,xyz[2]])
        
        snodeseq = model1.node(nodecoordlist,setname=name+'_plate')
        
        
        # add plate center node and tie this node to all nodes in plate
        cnodeseq = model1.node([[centercoord[0],plateyloc,centercoord[2]]],setname=name+'_plate_center') 
    
        model1.nodaltie(name,'marc_rbe2',paralib={'tietype':'fix',
                                                            'retnode':cnodeseq+1,
                                                            'tienodelist':name+'_plate'})
    
    
        # add springs
        nodei = 1
        for nodeseq in pnodelist:
    
            springname = 'spring_'+str(nodeseq)
            
            model1.nodaltie(springname,'onetoonespring',paralib={'tietype':'fixed_dof',
                                                            'retnode':nodeseq,
                                                            'tienode':snodeseq + nodei,
                                                            'stiff':stiffness,
                                                            'DOF':'y'})
            #model1.nodaltie(name+str(nodei),'marc_rbe2',paralib={'tietype':'spring_Y',
            #                                                'retnode':nodeseq,
            #                                                'tienodelist':[snodeseq + nodei]})
            nodei += 1
        
        return model1
    
    else:
        return model1

def pole_extend(model1,setname,targetendcoord,incrementlength,center=(0,0),mode='yz'):
    """ extend the selected set nodelist to one side by length of "length" and disp of "increment"
        setname: setname of the selected nodes
        targetendcoord: the end of the extend, also determine the direction
        increment: number of increment
        center: center of nodelist for searching nearest node
        mode: nodelist plane 
    
    """
    
    nodedict = model1.select_coordinates_setname(setname)
    nodecoordlist = []
    xcoordlist = []
    
    for key,item in nodedict.items():
        if mode == 'yz':
            xcoordlist.append(item.xyz[0])
            ycoord = item.xyz[1]
            zcoord = item.xyz[2]
            ang = atan((zcoord-center[1])/(ycoord-center[0]))
            if ycoord<0 and zcoord<0:
                ang += 3.1415926
            elif ycoord>0 and zcoord<0:
                ang += 3.1415926*2
            elif ycoord<0 and zcoord>0:
                ang += 3.1415926

            
            nodecoordlist.append([key,ycoord,zcoord,ang])
    
    # get distance
    maxend, minend = max(xcoordlist),min(xcoordlist)
    maxdist,mindist = abs(targetendcoord-maxend),abs(targetendcoord-minend)
    avgdist = (float(maxdist) + float(mindist))/2.0
    
    increment = int(avgdist/incrementlength)
    
    
    avgdistincr = avgdist/float(increment)*float(targetendcoord)/abs(float(targetendcoord))
    
    
    
    
    nodecoordlist = np.array(nodecoordlist)
    nodecoordlist = nodecoordlist[nodecoordlist[:,3].argsort()]
    
    print 'edge nodelist based on setname '+ setname +' detected and sorted'

    # create nodes
    newnodelist = []
    for i in range(0,increment):
        
        for j in range(0,nodecoordlist.shape[0]):
            x = targetendcoord - avgdistincr * (increment-1-i)
            y = nodecoordlist[j,1]
            z = nodecoordlist[j,2]
            newnodelist.append([x,y,z])
    
    nolist = model1.node(newnodelist,setname='extension_nodes_'+setname) + 1
    
    # create elements
    newelemlist = []
    for i in range(0,increment):
        
        if i == 0:  # connection portion
            for j in range(0,nodecoordlist.shape[0]):
                n1 = nodecoordlist[j,0]
                n4 = nolist + j
                if j != nodecoordlist.shape[0]-1:
                    n2 = nodecoordlist[j+1,0]
                    n3 = n4 + 1 
                else:
                    n4 = nodecoordlist[j,0]
                    n1 = nolist + j
                    
                    n3 = nodecoordlist[0,0]
                    n2 = nolist
                
                newelemlist.append([int(n1),int(n2),int(n3),int(n4)])
            
        else:    # extension portion
            for j in range(0,nodecoordlist.shape[0]):
                nodeidincr = nodecoordlist.shape[0]
                n1 = nolist + j + nodeidincr * (i-1)
                n4 = nolist + j + nodeidincr * i
                if j != nodecoordlist.shape[0]-1:
                    n2 = n1 + 1
                    n3 = n4 + 1
                else:
                    n4 = nolist + j + nodeidincr * (i-1)
                    n1 = nolist + j + nodeidincr * i                    
                    n3 = nolist + 0 + nodeidincr * (i-1)
                    n2 = nolist + 0 + nodeidincr * (i)               
                newelemlist.append([int(n1),int(n2),int(n3),int(n4)])    
            
    elemnolist = model1.element(newelemlist,setname='extension_elements_'+setname)
    
    print "Extension nodes and elements created"
    
    return model1

def process_pole_dat(model1,fullfilename,dentpercent=0.5):
    ''' process the pole marc dat file

        the node with +/-xerror will be selected to curvefit the circle center
        dentpercent: Percentage of the dent that shall be apply different material property
    '''
    dentpercent = float(dentpercent)
    
    p1 = importfile_marc_dat(fullfilename,stylesetting='Extended')
    model1 = p1.add_nodes(model1)
    model1 = p1.add_elements(model1)
    
    print 'Marc mat file imported, nodes and elements only'
    eff_nodelist = model1.nodelist.itemlib.keys()
    
    
    # find min and max, based on the fact that the model is cleaned up
    nmax,nmin = model1.nodelist.get_maxmin()
    xleft = nmin[0]
    xright = nmax[0]
    xerror = 1
    print 'edge detected, xleft:%s xright:%s' % (str(xleft), str(xright))
    
    
    # find the nodes at left and right ends and curve fit to get the center
    leftnodes = model1.nodelist.select_node_coord(rx=[xleft-xerror,xleft+xerror])
    rightnodes = model1.nodelist.select_node_coord(rx=[xright-xerror,xright+xerror])
    
    model1.nodeset('surface_leftend',{'nodelist':leftnodes})
    model1.nodeset('surface_rightend',{'nodelist':rightnodes})
    
    
    # find the center of circle at edges
    r1,rd1 = find_circlecenter(model1,leftnodes)
    r2,rd2 = find_circlecenter(model1,rightnodes)
    rdist = r2[0] - r1[0]
    
    print 'Center found, r1:%s r2:%s' % (str(r1), str(r2))


    nrefnode = model1.node([r1,r2])
    nodeid_leftcenter = nrefnode + 1
    nodeid_rightcenter = nrefnode + 2
    model1.nodeset('left_center',{'nodelist':[nodeid_leftcenter]})
    model1.nodeset('right_center',{'nodelist':[nodeid_rightcenter]})
    print 'Center reference nodes added'
    
    
    # adjust the node coordinates
    model1.nodelist.transform(dx=-r1[0],dy=-r1[1],dz=-r1[2])
    ang = Find_angle(r1,r2,axis='x')
    model1.nodelist.transform(rx=ang[0],ry=ang[1],rz=ang[2])

    
    r1 = [0,0,0]
    r2 = [rdist,0,0]
    print 'Model trasnformed to x center'

    
    # find the deepest node
    mindist = 1e10 
    point = None
    dent_dict = {}
    
    for node in eff_nodelist:
        xyz = model1.nodelist.itemlib[node].xyz
        dist = DistancePointLine(r1,r2,xyz)
        dent_dict[node] = dist
        if dist < mindist:
            mindist = dist
            point = node

    print 'Deepest dent found %s @ node %s' % (str(mindist),str(point))

    
    # search for dent_node_set
    dent_nodes_set = []

 
    # calculate the direction cosine of the node
    P = model1.nodelist.itemlib[point].xyz
    TP,ud,dd = UdirectionPointLine(r1,r2,P)
    
    dent_map = []
    for nodes in eff_nodelist:
        Q = model1.nodelist.itemlib[nodes].xyz
        distdent = Parameter(r1,r2,rd1,rd2,P,Q)
        dent_map.append(distdent)
        if distdent[3] > mindist * dentpercent/100.0:
            dent_nodes_set.append(nodes)
            
    model1.dent_map = np.asarray(dent_map)
    model1.nodeset('dent_nodes_sets',{'nodelist':dent_nodes_set})
    print 'Found total %s nodes for %s%% dent limits' % (str(len(dent_nodes_set)),str(dentpercent))


  
    
    # convert the model to demand coordinate system
    model1.nodelist.shift_coord(shx=-TP[0],shy=-TP[1],shz=-TP[2])
    model1.nodelist.transform(rx=-np.arctan(ud[2]/ud[1]))
    print 'Model adjust to the upright position'


    Allelements = list(model1.connlist.itemlib.keys())
    model1.elemset('surface_elements',{'elemlist':Allelements})
    
    dentelemlist = model1.select_elements_nodeset('dent_nodes_sets')
    model1.elemset('dentelems',{'elemlist':dentelemlist})
    
    print "Element set Created: %s # 'Full Surface' and %s # 'dentelems'" % (len(Allelements),len(dentelemlist))

    return model1

def add_material(model1):
    ''' this is the defination of the steel and aluminum material'''
    ss_pole_steel = [[0,0],
                     [0.0018,53.800],
                     [0.03,54],
                     [0.12,64],
                     [0.121,0],
                     [0.5,0]]
    model1 = add_mat_by_stressstrain(model1,'pole_steel',ss_pole_steel,0.0018)
    model1 = add_mat_by_stressstrain(model1,'pole_steel_dent',ss_pole_steel,0.0018)
    
    ss_pole_alum = [[0,0],
                    [0.004,33],
                    [0.054,36],
                    [0.0541,0],
                    [0.5,0]]
    model1 = add_mat_by_stressstrain(model1,'pole_alum',ss_pole_alum,0.004)
    model1 = add_mat_by_stressstrain(model1,'pole_alum_dent',ss_pole_alum,0.004)
    
    return model1


def PoleModeling(model1):
    ''' create the circular shell surface'''
    # add material

    model1 = add_material(model1)
    
    nodeid_leftcenter = model1.setlist['left_center'].nodelist[0]
    nodeid_rightcenter = model1.setlist['right_center'].nodelist[0]
    
    #model1.nodeset('left_center',{'nodelist':[nodeid_leftcenter]})
    #model1.nodeset('right_center',{'nodelist':[nodeid_rightcenter]})

    # add reb3 to simulate the bending
    model1.nodaltie('left_support','marc_rbe2',paralib={'tietype':'fix',
                                                        'retnode':nodeid_leftcenter,
                                                        'tienodelist':'surface_leftend'})

    model1.nodaltie('right_support','marc_rbe2',paralib={'tietype':'fix',
                                                        'retnode':nodeid_rightcenter,
                                                        'tienodelist':'surface_rightend'})
    
    model1.bond('leftbond',{'xyz':[1,1,1,0,1,1],'DOF':6,'setnamelist':['left_center']})
    model1.bond('rightbond',{'xyz':[1,1,1,0,1,1],'DOF':6,'setnamelist':['right_center']})
    model1.disp('leftdisp',{'xyz':[0,0,0,1,0,0],'DOF':6,'scalar':0.1,'setnamelist':['left_center']})
    model1.disp('rightdisp',{'xyz':[0,0,0,1,0,0],'DOF':6,'scalar':-0.1,'setnamelist':['right_center']})    

    model1.section('sec_1','shell_section',{'thickness':0.1875})

    
    model1.property('prop1','quad4',{'type':75,'thinkness':0.01})
    model1.property('prop_dent','quad4',{'type':75})
    
    
    model1.elemset_sub_setname('surface_elements','dentelems')
    
    model1.link_prop_conn('prop1',setnamelist=['surface_elements-dentelems'])
    model1.link_prop_conn('prop_dent',setnamelist=['dentelems'])
    
    model1.link_sec_prop('sec_1','prop1')
    model1.link_sec_prop('sec_1','prop_dent')
    
    # associate the material
    model1.link_mat_prop('pole_alum','prop1')
    model1.link_mat_prop('pole_alum_dent','prop_dent')
    
    model1.loadcase('loadcase1','static_arclength',{'boundarylist':['leftbond','leftdisp','rightbond','rightdisp'],'para':{'nstep':30}})
    
    #model1.job('job1','static_job',{'loadcaselist':['loadcase0','loadcase1'],'submit':True,'reqresultslist':['stress','total_strain','plastic_strain']})
    model1.job('job1','static_job',{'loadcaselist':['loadcase0','loadcase1'],'submit':False,'reqresultslist':['stress','total_strain','plastic_strain']})
    
    return model1


def add_support(model1,name,xcenter,ycenter,zcenter,length,width):
    # select supporting plate
    plateyloc = -1e6  # a big number to simulate the ground
    xmin = xcenter - length/2.0
    xmax = xcenter + length/2.0
    ymin = min(ycenter,plateyloc)
    ymax = max(ycenter,plateyloc)
    zmin = zcenter - width/2.0
    zmax = zcenter + width/2.0
    
    pnodelist = model1.nodelist.select_node_coord([xmin,xmax],[ymin,ymax],[zmin,zmax])
    model1.nodeset(name,{'nodelist':pnodelist})    
    
    model1.disp(name,{'xyz':[1,1,1,1,1,1],'DOF':6,'scalar':0,'setnamelist':[name]})
    
    return model1

def pole_bending_modeling(model1,leftsupportx,rightsupportx,supporty,leftplatecenterx,rightplatecenterx,plateheighty,lengthx,heighty,stiffness):
    """ continue with pole_extend command and add support and load plate """
    
    
    # add loading plate
    model1 = pole_contact_plate(model1,'rightloadplate',(rightplatecenterx,heighty,0),lengthx,1000,plateheighty,stiffness)
    model1 = pole_contact_plate(model1,'leftloadplate',(leftplatecenterx,heighty,0),lengthx,1000,plateheighty,stiffness)
    
    
    # add support
    model1 = add_support(model1,'leftsupport',leftsupportx,supporty,0,lengthx * 2,10000)  # due to fact that only one side of plate will be selected
    model1 = add_support(model1,'rightsupport',rightsupportx,supporty,0,lengthx * 2,10000) # big width number to seelct all nodes
       
    
    model1 = add_material(model1)
    
    model1.load('leftrightload',{'xyz':[0,1,0,0,0,0],'DOF':6,'scalar':-1,'setnamelist':['leftloadplate_plate_center','rightloadplate_plate_center']}) 

    model1.section('sec_1','shell_section',{'thickness':0.1875})

    
    model1.property('prop1','quad4',{'type':75,'thinkness':0.01})
    model1.property('prop_dent','quad4',{'type':75})
    
    
    model1.elemset_sub_setname('surface_elements','dentelems')
    
    model1.link_prop_conn('prop1',setnamelist=['surface_elements-dentelems'])
    model1.link_prop_conn('prop_dent',setnamelist=['dentelems','extension_elements_surface_leftend','extension_elements_surface_rightend'])
    
    model1.link_sec_prop('sec_1','prop1')
    model1.link_sec_prop('sec_1','prop_dent')
    
    # associate the material
    model1.link_mat_prop('pole_alum','prop1')
    model1.link_mat_prop('pole_alum_dent','prop_dent')
    
    model1.loadcase('loadcase1','static_arclength',{'boundarylist':['leftsupport','rightsupport','leftrightload'],'para':{'nstep':1}})
    
    #model1.job('job1','static_job',{'loadcaselist':['loadcase0','loadcase1'],'submit':True,'reqresultslist':['stress','total_strain','plastic_strain']})
    model1.job('job1','static_job',{'loadcaselist':['loadcase0','loadcase1'],'submit':False,'reqresultslist':['stress','total_strain','plastic_strain']})
    
    return model1    