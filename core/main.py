from model.registry import model
from export.export import exporter
import numpy as np
from settings import settings

from utility.geometry import create_section 
from lib import libop

# create model instance
model1 = model(settings)

# create node
model1.node([[0,0,0],
            [1,0,0],
            [2,0,0],
            [3,0,0],
            [3,0,0],
            [5,0,0]])

# create element
model1.element([[1,2],
                [2,3],
                [3,4]])

model1.material('mat1','uniaxial_elastic',{'E':29000.0,'mu':0.3,'mass':0.0})
model1.material('UHPC','uniaxial_elastic',{'E':8000.0,'mu':0.3,'mass':0.0})

'''
model1.section('sec1','fiber',{'locy':1.0,
               'locz':1.0,
               'area':1.0,
               'width':1.0,
               'thickness':1.0})
'''

model1.section('sec2','elastic_section',{
        'mattag':'mat1',
        'A' : 0.0,
        'Iz': 0.0,
        'Iy': 0.0,
        'J' : 0.0,
        'Sy': 0.0,
        'Sz' :0.0})


layer = {
    1:{'locy':1.0,'locz':1.0,'area':1.0,'width':1.0,'thickness':1.0,'mattag':'mat1'},
    2:{'locy':1.0,'locz':1.0,'area':1.0,'width':2.0,'thickness':1.0,'mattag':'mat1'},
    3:{'locy':1.0,'locz':1.0,'area':1.0,'width':3.0,'thickness':1.0,'mattag':'mat1'},
}
model1.section('sec3','layer_section',{'nl':3,'d':4,'fiber':layer})


bf = 12
tf = 1.25
bw = 2
hw = 3.75
nfl =50
nw =50
mat = 'UHPC'
reinf = [{'loc':'bottom|middle','desig':'us7',
          'cover':(0.5,None),'mat':'MMFX2_minmax'}]
    
Tsection = create_section.create_T_section(bf,tf,bw,hw,nfl,nw,mat,reinf)
model1.section('sec4','layer_section',{'fiber':Tsection})


model1.property('prop1','line2',{'type':'dispBeamColumn',
                                'nIntgp': 3})
model1.orient('orient1','orient_linear',{})


model1.link_mat_prop('mat1','prop1')
model1.link_sec_prop('sec3','prop1')
model1.link_orient_prop('orient1','prop1')
model1.link_prop_conn('prop1',[1,2,3])
model1.bond('left support',{'xyz':[1,1,1,1,1,1],'nodelist':[1,2,3]})


print model1.get_mat_prop('mat1','E')

model1.parameter('E1',{'lib':'matlist','obj':'mat1','prop':'E'})

# ==========test exporter ========
#exp1 = exporter(model1,'Opensees.txt','ex_OpenSees')
#exp1 = exporter(model1,'Ansys.txt','ex_Ansys')

#exp1.write_variables()
#exp1.write_settings()
#exp1.write_coord()
#exp1.write_conn_prop()
#exp1.write_mat()
#exp1.write_sec()
#exp1.write_out()

exp1 = exporter(model1,'Marc.txt','ex_Marc')
exp1.write_settings()
exp1.write_coord()
exp1.write_conn_prop()
exp1.write_out()
print 1


libop.save('model',model1,'trial_model')