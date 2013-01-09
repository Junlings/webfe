import sys
import pickle
sys.path.append('C:/marcworking/pythonlib')
import numpy as np
import collect as coll

#####Dealwith 1T1S_no anchorage
d1=coll.collect('data')
d1.import_cvs('original/UHPC_deck/s_1t1s_noanchorage.csv')
print d1.database.keys()
### use three strain gauges results to calculate the average middle span deflection
defl=(d1.database['S.Pot-2'][1]+d1.database['S.Pot-3'][1]+d1.database['S.Pot-1'][1])/3
d1.add_para('average_defl',[d1.database['S.Pot-2'][0],defl])
d1.export_pydat('Exp/s_1t1s_noanchorage')


#####Dealwith 1T1S_endplate 
d2=coll.collect('data')
d2.import_cvs('original/UHPC_deck/s_1t1s_steelplate.csv')
print d2.database.keys()
defl=(d2.database['S.Pot-2'][1]+d2.database['S.Pot-3 (mid)'][1]+d2.database['S.Pot-1'][1])/3
d2.add_para('average_defl',[d2.database['S.Pot-2'][0],defl])
d2.export_pydat('Exp/s_1t1s_steelplate')


#####Dealwith 1T1S_endplate 
d3=coll.collect('data')
d3.import_cvs('original/UHPC_deck/s_1t1s_hook.csv')
print d3.database.keys()
defl=(d3.database['S.Pot-4'][1]+d3.database['S.Pot-3'][1]+d3.database['S.Pot-1'][1])/3
d3.add_para('average_defl',[d3.database['S.Pot-1'][0],defl])
d3.export_pydat('Exp/s_1t1s_hook')

#####Dealwith 1T1S_tapered
d4=coll.collect('data')
d4.import_cvs('original/UHPC_deck/s_1t1s_taper.csv')
print d4.database.keys()
defl=(d4.database['S.Pot-4'][1]+d4.database['S.Pot-3'][1]+d4.database['S.Pot-1'][1])/3
d4.add_para('average_defl',[d4.database['S.Pot-1'][0],defl])
d4.export_pydat('Exp/s_1t1s_taper')

##### dealwith 1T1S_2NO4
d5=coll.collect('data')
d5.import_cvs('original/UHPC_deck/s_1t1s_2no4.csv')
print d5.database.keys()
### use three strain gauges results to calculate the average middle span deflection
defl=(d5.database['S.Pot-4'][1]+d5.database['S.Pot-3'][1]+d5.database['S.Pot-1'][1])/3
d5.add_para('average_defl',[d5.database['S.Pot-4'][0],defl])
d5.export_pydat('Exp/s_1t1s_2no4')



##### dealwith 1T1S_2NO4
d6=coll.collect('data')
d6.import_cvs('original/UHPC_deck/s_1T1S_NO4_2No3.csv')
print d6.database.keys()
### use three strain gauges results to calculate the average middle span deflection
defl=(d6.database['S.Pot-4'][1]+d6.database['S.Pot-3'][1]+d6.database['S.Pot-1'][1])/3
d6.add_para('average_defl',[d6.database['S.Pot-4'][0],defl])
d6.export_pydat('Exp/s_1t1s_NO4_2No3')

d7=coll.collect('data')
d7.import_cvs('original/UHPC_deck/s_1T1S_NO7_2shear.csv')
print d7.database.keys()
### use three strain gauges results to calculate the average middle span deflection
defl=(d7.database['S.Pot-4'][1]+d7.database['S.Pot-3'][1]+d7.database['S.Pot-1'][1])/3
d7.add_para('average_defl',[d7.database['S.Pot-4'][0],defl])
d7.export_pydat('Exp/s_1t1s_NO7_2shear')



