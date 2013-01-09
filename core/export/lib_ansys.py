#!/usr/bin/env python
import core.meta.meta_export as metacls
import numpy as np

class ex_Ansys():
    __metaclass__ = metacls.metacls_export   # meat class
    def __init__(self):
        pass
    
    def ex_coord_single(self,node):
        exp = 'N,%i,%6.6f,%6.6f,%6.6f\n' % (node.seq, node.xyz[0],
                                                    node.xyz[1],
                                                    node.xyz[2])
        return exp


    def ex_conn_single(self,conn):
        exp = 'E,%s\n' % (conn.seq, np.array_str(conn.nodelist)[1:-1])
        return exp
    
    
    def ex_conn_prop_single(self,conn,prop):
        exp = 'MAT, %s\n' % prop.mattag
        #print str(conn.nodelist)[1:-1].replace(' ',',')
        exp += 'E, %s \n' % str(conn.nodelist)[1:-1].replace(' ',',')
    
        return exp    

    def ex_variable_single(self,name,value):
        exp = '*SET, %s, %i\n' % (name,value)
        return exp
    
    def ex_settings_single(self,settings):
        exp = '/title %s\n' % settings['prjname']
        exp += '/PREP7 \n'
        #exp += 'model BasicBuilder -ndm %d -ndf %d;\n' % (settings['ndm'],
        #                                                settings['ndf'])
        return exp
    
    def ex_mat_single(self,key,mat):
        
        type = mat.__class__.__name__
        if type == 'uniaxial_elastic':
            exp = self.ex_mat_single_elastic_Isotropic(key,mat)


    def ex_mat_single_elastic_Isotropic(self,key,mat):
        exp = 'MP,ex,%s,%f\n' % (key,mat.E)
        exp += 'MP,nuxy,%s,%f\n' % (key,mat.mu)
        exp += 'MP,dens,%s,%f\n' % (key,mat.mass)
        
        return exp

    def ex_mat_single_elastic_orthotropic(mat):
        exp = 'MP,ex,%s,%f\n' % (key,mat.Ex)
        exp += 'MP,ey,%s,%f\n' % (key,mat.Ey)
        exp += 'MP,ez,%s,%f\n' % (key,mat.Ez)
        exp += 'MP,gxy,%s,%f\n' % (key,mat.Gxy)
        exp += 'MP,gxz,%s,%f\n' % (key,mat.Gxz)
        exp += 'MP,gyz,%s,%f\n' % (key,mat.Gyz)
        exp += 'MP,nuxy,%s,%f\n' % (key,mat.muxy)
        exp += 'MP,nuxz,%s,%f\n' % (key, mat.muxz)
        exp += 'MP,nuyz,%s,%f\n' % (key,mat.muyz)
        exp += 'MP,dens,%s,%f\n' % (key,mat.dens)
        return exp
    
    
    def ex_sec_single(self,key,sec,mat=None):
        type = sec.__class__.__name__
        
        if type == 'elastic_section':
            exp = self.ex_sec_single_elastic(key,sec)
        else:
            exp = ''
        return exp


    def ex_sec_single_elastic(self,key,sec):
        exp = 'R,%s,%f\n' % (key,sec.A)
        return exp
        

"""          
    def ex_conn_prop_single(self,conn,prop):
        if prop.__class__.__name__ == 'line2':
            exp = 'element dispBeamColumn %i' % conn.seq
            exp += ' %s ' % str(conn.nodelist)[1:-1]
            exp += '%i $%s $%s\n' % (
                   prop.nIntgp, prop.sectag, prop.orienttag)
    
        return exp
        

    def ex_para_single(self,para):
        ''' need verify'''
        exp = 'set %s %i \n' % (key, para.seq)
        return exp
            
    def ex_model(self,settings):
        ''' export model settings'''
        exp = 'wipe;\n' + 'model BasicBuilder -ndm %i -ndf %i;\n' % (
                                            settings['NDM'],settings['DNF']
        )
        return exp
            
    def ex_orient_single(self,key,orient):    
            if orient.type == 'linear':
                exp == 'geomTransf %s $%s\n' % (orient.type, key)
            elif orient.type == '3d':
                exp == 'geomTransf %(type)s $%(tag)s %(vx)g %(vy)g %(vz)g\n' % (
                                    orient.type, key, orient.vx,
                                                      orient.vy,
                                                      orient.vz)
            else:
                raise TypeError,('orient type not defined',orient.type)
            
            return exp
                
    def ex_mat_single(self,key,mat):
        
        type = mat.__class__.__name__
        if type == 'uniaxial_elastic':
            exp = 'uniaxialMaterial Elastic $%s %g\n' % (key,mat.E) 
        
        elif type == 'uniaxial_elastic_NT':
            exp = 'uniaxialMaterial ENT $%s %g\n' % (key,mat.E)
            
        elif type == 'uniaxial_elastic_minmax':
            exp = 'uniaxialMaterial MinMax $%(tag)s %i' % (key,mat.baseseq)
            exp += ' -max %(epsi_ut)g -min %(epsi_uc)g\n' % (mat.epsi_ut,
                                                             mat.epsi_uc)
        elif type == 'uniaxial_EPP':
            exp = 'uniaxialMaterial ElasticPP $%s %g %g\n' % (
                                              key, mat.epsi_y,mat.epsi_u)
        elif type == 'uniaxial_steel_02':
            exp = 'uniaxialMaterial Steel02 $%s' % key
            exp += '%(fy)g %(E)g %(b)g %(r0)g %(cr1)g %(cr2)g\n' % mat
        elif type == 'uniaxial_UHPC':
            exp = 'uniaxialMaterial ECC01  $%s ' % key
            exp_temp = ''.join(['%(sigt0)g  %(epst0)g  %(sigt1)g ',
                            '%(epst1)g  %(sigt2)g  %(epst2)g ',
                            '%(epst3)g  %(sigc0)g  %(epsc0)g ',
                            '%(sigc1)g  %(epsc1)g  %(epsc2)g ',
                            '%(alphaT1)g  %(alphaT2)g  %(alphaT3)g ',
                            '%(alphaC)g  %(alphaC1)g  %(alphaCU)g ',
                            '%(betaT)g  %(betaC)g \n '])
            exp += exp_temp % mat
            
        else:
            raise TypeError,('Material type do not find',type)
        
        return exp
        
    def ex_sec_single(self,key,sec,mat=None):
        type = sec.__class__.__name__
        
        if type == 'elastic_section':
            exp = 'section Elastic  $%s' % key
            #exp += '%g %g %g %g %g %g\n' % (
            #        sec.E, sec.A, sec.Iy, sec.Iz, sec.G, sec.J)
            exp += '%g %g %g %g %g %g\n' % (
                    mat.E, sec.A, sec.Iy, sec.Iz, mat.G, sec.J)

            
        elif type == 'layer_section':
            exp = 'section fiberSec  $%s' % key
            exp += '{\n'
            
            for fiberkey in sec.fiber.keys():
                exp += self.ex_fiber(fiberkey,sec.fiber[fiberkey])
            exp += '}\n'
        
        elif type == 'aggregator_section':
            exp = 'section  Aggregator $%s %s -section $%s \n' % (key,
                                                        str_aggregator,basetag)
        else:
            exp = ''
        return exp
    
    def ex_fiber(self,key,fiber):
        
        exp = 'fiber   %g %g   %g   $%s \n' %(
                        fiber.locy,fiber.locz,fiber.area,fiber.mattag)    
        return exp
    
    def ex_settings_single(self,settings):
        
        exp = 'wipe;\n'
        exp += 'model BasicBuilder -ndm %d -ndf %d;\n' % (settings['ndm'],
                                                        settings['ndf'])
        return exp
    
    def ex_variable_single(self,name,value):
        exp = 'set %s %d\n' % (name,value)
        return exp
       


==============================defination of connectivity=====================

CONN_OS = {}
CONN_OS['3Dbeam'] = 'element dispBeamColumn %(seq)i %(str_nodelist)s %(nIntgp)i $%(sectag)s $%(orienttag)s\n'
                    #% (elemid,elemnodelist[0],elemnodelist[1],nIntgp,SecID,TransfID)
CONN_OS['line2:dispBeamColumn'] = 'element dispBeamColumn %(seq)i %(str_nodelist)s %(str_property)s\n'
                    #% (elemid,elemnodelist[0],elemnodelist[1],nIntgp,SecID,TransfID)                  
CONN_OS['line2:'] = 'element dispBeamColumn %(seq)i %(str_nodelist)s %(str_property)s\n'
CONN_OS['line2:nonlinearBeamColumn'] = 'element nonlinearBeamColumn %(seq)i %(str_nodelist)s %(str_property)s\n'
CONN_OS['line2_user:nonlinearBeamColumn'] = 'element nonlinearBeamColumn %(seq)i %(str_nodelist)s %(str_property)s\n'
CONN_OS['zeroLength:ALL'] = 'element zeroLength %(seq)i  %(str_nodelist)s -mat %(str_property)s -dir 1 2 3 4 5 6\n'

CONN_OS['rigidLink:beam'] = 'rigidLink beam %(str_nodelist)s\n'
CONN_OS['rigidLink'] = 'rigidLink beam %(str_nodelist)s\n'

CONN_OS['3D_brick'] = 'element stdBrick $(seq)i %(str_nodelist)s $%(matTag)s\n'
                       #element stdBrick $eleTag $node1 $node2 $node3 $node4 $node5 $node6 $node7 $node8 $matTag
CONN_OS['3D_truss'] = 'element truss $(seq)i %(str_nodelist)s $(area)f $%(matTag)s\n'
                       #element truss $eleTag $iNode $jNode $A $matTag

# ==============================defination of connectivity=====================
PROP_OS = {}
PROP_OS['line2'] = '%(nIntgp)i $%(sectag)s $%(orienttag)s\n'
PROP_OS['line2_user'] = '$%(orienttag)s UserDefined %(nIntgp)i %(str_seclist)s %(str_location)s %(str_weight)s\n'
PROP_OS['zeroLength:nonlinearBeamColumn'] = '%(str_mattaglist)s'
PROP_OS['zeroLength'] = '%(str_mattaglist)s'

# additional
PROP_OS['rigidLink'] = 'rigidLink beam %(str_nodelist)s\n'

PROP_OS['para'] = Gen_OS['para'] + 'parameter $%(tag)s element %(elem_seq)i addition $%(item_tag)s %(vname)s\n'



# ==============================defination of section=====================
Sec_OS = {}
Sec_OS['fiber'] = 'fiber      %(locy)g %(locz)g     %(area)g   $%(mattag)s \n'
Sec_OS['layer_section'] = Gen_OS['para'] + 'section fiberSec  $%(tag)s  {\n %(layerinfo)s \n}\n'
Sec_OS['aggregator_section'] = Gen_OS['para'] + 'section  Aggregator $%(tag)s %(str_aggregator)s -section $%(basetag)s \n'
Sec_OS['elastic_section'] = Gen_OS['para'] + 'section Elastic  $%(tag)s    %(E)g %(A)g %(Iy)g %(Iz)g %(G)g %(J)g\n'

# ==============================defination of analysis=====================
Ana_OS = {}

Ana_OS['ana_section_mc'] = readfile(os.path.join(root,'proc/OpenSees/mc.tcl'))
Ana_OS['ana_material'] = readfile(os.path.join(root,'proc/OpenSees/uniaxial_mono.tcl'))
#Ana_OS['analysis'] = readfile(os.path.join(root,'proc/OpenSees/uniaxial_mono.tcl'))


Ana_OS['system'] = 'system %(system)s %(system_opt)s; \n'
Ana_OS['numberer'] =  'numberer %(numberer)s \n'
Ana_OS['constraints'] = 'constraints %(constraints)s \n'
Ana_OS['integrator'] = 'integrator %(integrator)s %(integrator_ctl)i %(integrator_dof)i %(integrator_inc)g\n'
Ana_OS['test'] = 'test %(test)s %(test_cri)g %(test_maxincr)i %(test_disp)i\n'
Ana_OS['algorithm'] = 'algorithm %(algorithm)s %(algorithm_opt)s\n'
Ana_OS['analysis'] = "analysis %(analysis)s \n "
Ana_OS['run_step'] = 'initialize \nanalyze %(run_step)i \n puts Analyze_Done\n'


# ==============================defination of recorder=====================
Rec_OS = {}
Rec_OS['recorderitem'] = ''
Rec_OS['item_node_disp'] = ('recorder Node -file %(recfile)s -time -node ' +
                           '%(str_nodelist)s -dof %(str_DOF)s disp\n')
Rec_OS['item_fiber'] = ('recorder Element -file %(recfile)s -time -ele '+ 
                        '%(str_elemlist)s section %(str_integlist)s fiber %(locy)f %(locz)f $%(mattag)s stressStrain \n')

# ==============================defination of boundary and load=====================

Bond_OS = {}

Bond_OS['load'] = 'load %i  %s \n'#'load %(nodeseq)i  %(str_DOF)s \n'
Bond_OS['bond'] = 'fix %i  %s \n'#'load %(nodeseq)i  %(str_Force)s \n'



Bond_OS['Pattern_linear'] = 'pattern Plain 1 Linear {\n%(loadlist)s}\n'


def export_recorder(obj):
    name = obj.__class__.__name__
    if name == 'item_node_disp':
        nodelist = '%s' % obj['nodelist']
        nodelist = nodelist[1:-1]
        obj.str_nodelist  = re.sub(',',' ',nodelist)
        
        if obj.str_nodelist == '-1':
            obj.str_nodelist = 'all'

        str_DOF = '%s' % obj['DOF']
        str_DOF = str_DOF[1:-1]
        obj.str_DOF  = re.sub(',',' ',str_DOF)        
        if obj.str_DOF == '-1':
            obj.str_DOF = '1 2 3 4 5 6'
            
    elif name == 'item_fiber':
        elemlist = '%s' % obj['elemlist']
        obj.str_elemlist  = re.sub(',',' ',elemlist[1:-1])
        
        integlist = '%s' % obj['integ']
        obj.str_integlist  = integlist
    
    output = Rec_OS[name] % obj     
    return output         

def export_coord(obj):
    str_node = '[%f,%f,%f]' % (obj['xyz'][0],obj['xyz'][1],obj['xyz'][2])
    obj.str_node  = re.sub(',',' ',str_node[1:-1])
    return Gen_OS['coord'] % obj
    
def export_ana(obj):
    
    output = (Ana_OS['system'] +
              Ana_OS['numberer'] +
              Ana_OS['constraints'] +
              Ana_OS['integrator'] +
              Ana_OS['test'] +
              Ana_OS['algorithm'] +
              Ana_OS['analysis'] +
              Ana_OS['run_step'])
    
    return output % obj

def export_prop(obj):
    if obj.mode == 'line2':
        return PROP_OS[obj.mode] % obj
    elif obj.mode == 'line2_user':
        obj.str_seclist = str_listdict(obj.sectaglist,tag='$')
        obj.str_location = str_listdict(obj.nIP)
        obj.str_weight = str_listdict(obj.wIP)
    elif obj.mode == 'zeroLength':
        obj.str_mattaglist = str_listdict(obj.mattaglist,tag='$')
        

    return PROP_OS[obj.mode] % obj


def export_conn(obj):
    nodelist = '%s' % obj['nodelist']
    nodelist = nodelist[1:-1]
    obj.str_nodelist  = re.sub(',',' ',nodelist)
    
    obj.str_property = export_prop(obj.property)
    
    output = CONN_OS[obj.property.mode+':'+obj.property.type] % obj
    
    return output


def export_bond(obj):
    # update to opensees format
    str_DOF = obj.str_DOF[1:-1]
    str_Force = obj.str_Force[1:-1]
    str_DOF  = re.sub(',',' ',str_DOF)
    str_Force  = re.sub(',',' ',str_Force)
    output =''
    
    if 'load' in obj.type: 
        loadlist = ''
        for node in range(0,len(obj['nodelist'])):
            loadlist += Bond_OS[obj.type] % (obj['nodelist'][node],str_Force)
            
        obj.loadlist = loadlist
        output = Bond_OS['Pattern_linear'] % obj
    
    elif 'bond' in obj.type:

        for node in range(0,len(obj['nodelist'])):
            output += Bond_OS[obj.type] % (obj['nodelist'][node],str_DOF)
    return output

def export_para(obj):
    return PROP_OS['para'] % obj

def export(obj):
    name = obj.__class__.__name__
    
    if name == 'conn':
        '''
        export element information
        '''
        return export_conn(obj)
    
    elif name == 'bond':
        return export_bond(obj)
        
    elif name == 'analysis':
        return export_ana(obj)
        
    elif name == 'coord':
        return export_coord(obj)
    
    elif name == 'property':
        return export_prop(obj)
        
    elif name =='parameter':
        return export_para(obj)
    
    elif name == 'orient':
        if obj.vx == 0 and obj.vy == 0 and obj.vz == 0:
            return Gen_OS['orient2d'] % obj
        else:
            return Gen_OS['orient'] % obj
            
    elif name in Rec_OS.keys():
        return export_recorder(obj)
        
    elif name in Mat_OS.keys():
        return Gen_OS['para'] % obj + Mat_OS[name] % obj
        
    elif name in Ana_OS.keys():
        nodelist = '%s' % obj['nodelist']
        nodelist = nodelist[1:-1]
        obj.str_nodelist  = re.sub(',',' ',nodelist)
        output = Ana_OS[name] % obj
                
        return output
    
    elif name in Gen_OS.keys():
        return Gen_OS[name] % obj
    elif name in Sec_OS.keys():
        return  Sec_OS[name] % obj
        
    else:
        print 'class:"' + name +'" do not defined export to OpenSees\n'
        raise KeyError
"""
