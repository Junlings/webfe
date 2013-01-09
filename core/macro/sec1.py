from twopoint import *


reinf_dict = create_reinf_layup()

reinf_dict['FRP_BAR_4|3_3_3'] = [{'id':'bot','loc':'bottom|middle','desig':'CFRP_BAR_4','cover':(0.5,None),'mat':'CFRPBAR'},
                                {'id':'2','loc':'top|middle','desig':'CFRP_BAR_3','cover':(0.5,None),'mat':'CFRPBAR'},
                                {'id':'3','loc':'top|middle','desig':'CFRP_BAR_3','cover':(0.5,None),'mat':'CFRPBAR'},
                                {'id':'top','loc':'top|middle','desig':'CFRP_BAR_3','cover':(0.5,None),'mat':'CFRPBAR'},]
    
    
decokeys = ['es_t_0.016','es_c_-0.016','ec_t_0.00018','ec_t_0.004','ec_t_0.016','ec_c_-0.003','ec_c_-0.01']

 #                                                     bf,tf,tf1,wf,tw,hw,nfl,nw,mat=None,reinf=None
fsection_T_frp1 = create_section.create_T_section_taper(15,1.25,0.75,3.5,1.5,2.75,40,40,mat='UHPC2',reinf=reinf_dict['FRP_BAR_4|3_3_3'])
model_T_frp1 = create_model('sec1',fsection_T_frp1)
p_T_taper= prjpost(model_T_frp1,decokeys=decokeys)

