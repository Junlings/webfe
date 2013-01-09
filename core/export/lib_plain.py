#!/usr/bin/env python
import core.meta.meta_export as metacls
import numpy as np
   
    
class ex_plain():
    __metaclass__ = metacls.metacls_export  
    def __init__(self):
        pass
        
    def ex_coord_single(self,node):
        exp = '%i %6.6f %6.6f %6.6f\n' % (node.seq, node.xyz[0],
                                                    node.xyz[1],
                                                    node.xyz[2])
        return exp
    
    
    def ex_conn_single(self,conn):
        exp = '%i %s\n' % (conn.seq, np.array_str(conn.nodelist)[1:-1])
        return exp        
    
    
    def ex_mat_single(self,key,mat):
        mtype = mat.__class__.__name__ 
        
        if mtype == 'uniaxial_elastic':
            exp = 'uniaxialMaterial Elastic $%s %g\n' % (key,mat.E)
        else:
            raise TypeError,('Material type ', mtype,' Do not found')
        return exp

        
        
'''

Gen_OS = {}
Gen_OS['para'] = 'set %(tag)s %(seq)i \n'
Gen_OS['coord'] = 'node %(seq)i %(xyz)s \n'
Gen_OS['model'] = 'wipe;\n' + 'model BasicBuilder -ndm %(ndm)i -ndf %(ndf)i;\n'
Gen_OS['conn'] =  'conn %(seq)i %(nodelist)s\n'
Gen_OS['beam'] =  'conn %(seq)i %(nodelist)s\n'
Gen_OS['bond'] = 'bond %(seq)i %(str_DOF)s %(scalar)g\n'
# ==============================defination of material=====================
Mat_OS = {}
Mat_OS['uniaxial_elastic'] = 'uniaxialMaterial Elastic $%(tag)s %(E)g\n'
Mat_OS['uniaxial_elastic_NT'] = 'uniaxialMaterial ENT $%(tag)s %g\n'
Mat_OS['uniaxial_elastic_minmax'] = 'uniaxialMaterial MinMax $%(tag)s $%(basetag)s -max %(epsi_ut)g -min %(epsi_uc)g\n'
Mat_OS['uniaxial_EPP'] = 'uniaxialMaterial ElasticPP $%(tag)s %(epsi_y)g %(epsi_u)g\n'
Mat_OS['steel_02'] = 'uniaxialMaterial Steel02 $%(tag)s %(fy)g %(E)g %(b)g %(r0)g %(cr1)g %(cr2)g\n'

output =  'uniaxialMaterial ECC01  $%(tag)s '
output += '%(sigt0)g  %(epst0)g  %(sigt1)g '
output += '%(epst1)g  %(sigt2)g  %(epst2)g '
output += '%(epst3)g  %(sigc0)g  %(epsc0)g '
output += '%(sigc1)g  %(epsc1)g  %(epsc2)g '
output += '%(alphaT1)g  %(alphaT2)g  %(alphaT3)g '
output += '%(alphaC)g  %(alphaC1)g  %(alphaCU)g '
output += '%(betaT)g  %(betaC)g \n '
Mat_OS['UHPC'] = output

# ==============================defination of section=====================
Sec_OS = {}
Sec_OS['fiber'] = 'fiber      %(locy)g %(locz)g     %(area)g   $%(mattag)s \n'
Sec_OS['layer_section'] = Gen_OS['para'] + 'section fiberSec  $%(tag)s  {\n %(layerinfo)s \n}\n'


# ==============================defination of analysis=====================
Ana_OS = {}
Ana_OS['analysis'] = ''
Ana_OS['ana_section_mc'] = readfile(os.path.join(root,'proc/OpenSees/mc.tcl'))
Ana_OS['ana_material'] = readfile(os.path.join(root,'proc/OpenSees/uniaxial_mono.tcl'))


# ==============================defination of recorder=====================
Rec_OS = {}
Ana_OS['recorderitem'] = ''
Ana_OS['item_node_disp'] = ('recorder Node -file %(recfile)s -time -node ' +
                           '%(node_seq)s -dof %(dof)s disp\n')
Ana_OS['item_fiber'] = ('recorder Element -file %(recfile)s -time -ele '+ 
                        '%(elem_seq)s section fiber %(locy)f %(locz)f $%(mat_tag)s stressStrain \n')


def export(obj):
    name = obj.__class__.__name__
    if name in Mat_OS.keys():
        return (Gen_OS['para'] + Mat_OS[name]) % obj
    elif name in Ana_OS.keys():
        return Ana_OS[name] % obj
    elif name in Gen_OS.keys():
        return Gen_OS[name] % obj
    elif name in Sec_OS.keys():
        return  Sec_OS[name] % obj
    else:
        print 'class:"' + name +'" do not defined export to OpenSees\n'
        raise KeyError
'''