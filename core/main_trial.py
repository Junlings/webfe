from model.registry import model
from export.export import exporter
import numpy as np
from settings import settings

from utility.geometry import create_section 
from lib import libop
from utility.geometry.create_nodes import create_single_line_nodelist

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
model1.property('prop1','line2',{'type':'dispBeamColumn',
                                'nIntgp': 3})

create_single_line_nodelist(model1,5,6,3)

model1.property('prop1','line2',{'type':'dispBeamColumn',
                                'nIntgp': 3})

model1.link_prop_conn('prop1','ALL')

print model1.connlist
print model1.nodelist.coordtable
exp1 = exporter(model1,'Marc.txt','ex_Marc')
exp1.write_settings()
exp1.write_coord()
exp1.write_conn_prop()
exp1.write_out()
print 1
