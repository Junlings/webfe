
import sys
import os
import datetime
sys.path.append('../webfe/')
from core.model.registry import model
from core.export.export import exporter
from core.settings import settings
from core.procedures.t_section import tsec_planeconfig
from core.procedures.rec_section import rec_planeconfig


model1 = model(settings)

#model1 = tsec_planeconfig(model1,'tsec1',12,1.25,1,3.75,2,4,1) #bf,tf,tf1,hw,tw,d,ds
model1 = rec_planeconfig(model1,'rec1',2,4,3,1,1,16,2)


model1.modelsavetofile('temp.pydat')
print 1