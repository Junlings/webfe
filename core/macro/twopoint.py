import sys
import os
sys.path.append('../../webfe/')
folder = os.path.dirname(os.path.realpath(__file__))

from model.registry import model
from export.export import exporter
import numpy as np
from settings import settings

from utility.sections import create_section
from lib import libop
from utility.models.create_twopointbending import twopoint_bending
from solver.opensees.moment_curvature import moment_curvature
from solver.opensees.opensees import run_OpenSees_abs, run_OpenSees_interact
from imports.opensees.import_opensees_dat import importfile_opensees_dat

def create_model(prjname,fsection,run=True,itype='Displacement',nstep=500, incr=-0.005):
        model1 = model(settings)
        model1.settings['prjname'] = prjname
        
        
        # create all available material models
        model1.material('mat1','uniaxial_elastic',{'E':29000.0,'mu':0.3,'mass':0.0})
        
        model1.material('CFRPBAR_BASE','uniaxial_elastic',{'E':18000.0,'mu':0.3,'mass':0.0})
        model1.material('CFRPCABLE_BASE','uniaxial_elastic',{'E':22300.0,'mu':0.3,'mass':0.0})
        
        model1.material('CFRPBAR','uniaxial_elastic_minmax',{'epsi_ut':0.016,'epsi_uc':-0.016,'baseseq':'CFRPBAR_BASE'})
        
        model1.material('CFRPCABLE','uniaxial_elastic_minmax',{'epsi_ut':0.016,'epsi_uc':-0.016,'baseseq':'CFRPCABLE_BASE'})
        
        model1.material('CFRPBAR_pre','uniaxial_elastic_InitStrain',{'iepsi':0.01,'basetag':'CFRPBAR'})
        
        model1.material('CFRPCABLE_pre','uniaxial_elastic_InitStrain',{'iepsi':0.01,'basetag':'CFRPCABLE'})
        
        
        
        model1.material('MMFX2','uniaxial_steel_02',{'E':29000.0,'mu':0.3,'mass':0.0,
                                                     'fy':165.0,'b':0.001,'r0':2.0,
                                                      'cr1':0.925,'cr2':0.15})
        
        
        model1.material('pstrand','uniaxial_steel_02',{'E':28000.0,'mu':0.3,'mass':0.0,
                                                     'fy':225,'b':0.001,'r0':2.0,
                                                      'cr1':0.925,'cr2':0.15})
        
        model1.material('pstrand_pre','uniaxial_elastic_InitStrain',{'iepsi':0.015,'basetag':'pstrand'})
        
        
        model1.material('UHPC1','uniaxial_UHPC',{'E':8000.0,'mu':0.3,'mass':0.0,
                                                 'sigt0':1.3,
                                                 'epst0':0.000179,
                                                 'sigt1':1.5,
                                                'epst1':0.004,
                                                'sigt2':1.501,
                                                'epst2':0.016,
                                                'epst3':0.016,
                                                'epsc0':0.003286,
                                                'sigc0':28,
                                                'sigc1':28.1,
                                                'epsc1':0.004,
                                                'epsc2':0.01,
                                                'alphaT1':1,
                                                'alphaT2':1,
                                                'alphaT3':1,
                                                'alphaC':1,
                                                'alphaC1':1,
                                                'alphaCU':1,
                                                'betaT':1,
                                                'betaC':1,       
                                                 })
        
        model1.material('UHPC2','uniaxial_UHPC2',{'E':6000.0,'mu':0.3,'mass':0.0,
                                                 'sigt0':1.1,
                                                 'epst0':0.000183,
                                                 'sigt1':1.1,
                                                'epst1':0.004,
                                                'epst2':0.016,
                                                'epsc0':-0.003286,
                                                'sigc0':-28,
                                                'epsc1':-0.01,
                                                'alphaT1':1,
                                                'alphaT2':1,
                                                'alphaC':1,
                                                'alphaCU':1,
                                                'betaT':1,
                                                'betaC':1,       
                                                 })
                
        matkeylist = ['mat1','CFRPBAR_BASE','CFRPCABLE_BASE','CFRPBAR','CFRPCABLE','MMFX2','UHPC1','UHPC2','CFRPBAR_pre','CFRPCABLE_pre','pstrand','pstrand_pre']
        
        
        #fsection = create_section.create_rec_section(1,2,20,mat='mat1',reinf=None)
        model1.section('section','fibersection',fsection)
        
        model1 = twopoint_bending(model1,'section',48,20,24,itype=itype,nstep=nstep, incr=incr)
        model1 = create_section.create_section_recorder(model1,12,'section',2, option='maxy')
        model1 = create_section.create_section_recorder(model1,12,'section',2, option='miny')
        model1 = create_section.create_section_recorder(model1,12,'section',2, option='fiberlib')
        model1 = create_section.create_section_recorder(model1,12,'section',2, option='all')
        
        exp1 = exporter(model1,'bending.tcl','ex_OpenSees')
        exp1.export(folder=prjname,matkeylist=matkeylist)
        
        
        ss = os.path.join(folder,prjname,'bending.tcl')
        
        ss = ss.replace('\\','\\\\')
        if run:
            run_OpenSees_abs(ss,version ='2.4.0')
        return model1

def create_reinf_layup():
    reinf_dict = {}

    reinf_dict['test'] = [{'id':'1','loc':'bottom|middle','desig':'us7','cover':(0.5,None),'mat':'CFRPBAR_pre'}]
    
    reinf_dict['test2'] = [{'id':'1','loc':'bottom|middle','desig':'CFRP_BAR_4','cover':(0.5,None),'mat':'CFRPBAR_pre'},
                           {'id':'2','loc':'top|middle','desig':'CFRP_BAR_4','cover':(0.375,None),'mat':'CFRPBAR'}]    
    

    reinf_dict['FRP_BAR_4_4|3_3_3'] = [{'id':'bot','loc':'bottom|middle','desig':'CFRP_BAR_4','cover':(0.25,None),'mat':'CFRPBAR'},
                                       {'id':'2','loc':'bottom|middle','desig':'CFRP_BAR_4','cover':(0.25+0.75,None),'mat':'CFRPBAR'},
                                       {'id':'3','loc':'top|middle','desig':'CFRP_BAR_3','cover':(0.25,None),'mat':'CFRPBAR'},
                                       {'id':'4','loc':'top|middle','desig':'CFRP_BAR_3','cover':(0.25,None),'mat':'CFRPBAR'},
                                       {'id':'top','loc':'top|middle','desig':'CFRP_BAR_3','cover':(0.25,None),'mat':'CFRPBAR'},]

    reinf_dict['FRP_BAR_4|4'] = [{'id':'bot','loc':'bottom|middle','desig':'CFRP_BAR_4','cover':(0.25,None),'mat':'CFRPBAR'},
                                 {'id':'top','loc':'top|middle','desig':'CFRP_BAR_4','cover':(0.25,None),'mat':'CFRPBAR'},]

    reinf_dict['P_FRP_BAR_4|4'] = [{'id':'bot','loc':'bottom|middle','desig':'CFRP_BAR_4','cover':(0.25,None),'mat':'CFRPBAR_pre'},
                                 {'id':'top','loc':'top|middle','desig':'CFRP_BAR_4','cover':(0.25,None),'mat':'CFRPBAR_pre'},]
    
    reinf_dict['P_FRP_BAR_4_4|3_3_3'] = [{'id':'bot','loc':'bottom|middle','desig':'CFRP_BAR_4','cover':(0.25,None),'mat':'CFRPBAR_pre'},
                                       {'id':'2','loc':'bottom|middle','desig':'CFRP_BAR_4','cover':(0.25+0.75,None),'mat':'CFRPBAR_pre'},
                                       {'id':'3','loc':'top|middle','desig':'CFRP_BAR_3','cover':(0.25,None),'mat':'CFRPBAR_pre'},
                                       {'id':'4','loc':'top|middle','desig':'CFRP_BAR_3','cover':(0.25,None),'mat':'CFRPBAR_pre'},
                                       {'id':'top','loc':'top|middle','desig':'CFRP_BAR_3','cover':(0.25,None),'mat':'CFRPBAR_pre'},]
    

    reinf_dict['P_FRP_CABLE_[7_12.5]|[7_12.5]'] = [{'id':'bot','loc':'bottom|middle','desig':'CFRP_CABLE|7_12.5','cover':(0.25,None),'mat':'CFRPCABLE_pre'},
                                                   {'id':'top','loc':'top|middle','desig':'CFRP_CABLE|7_12.5','cover':(0.25,None),'mat':'CFRPCABLE_pre'},]
    
    reinf_dict['7|3_3_3'] = [{'id':'bot','loc':'bottom|middle','desig':'us7','cover':(0.5,None),'mat':'MMFX2'},
             {'id':'2','loc':'top|middle','desig':'us3','cover':(0.375,None),'mat':'MMFX2'},
             {'id':'3','loc':'top|middle','desig':'us3','cover':(0.375,None),'mat':'MMFX2'},
             {'id':'top','loc':'top|middle','desig':'us3','cover':(0.375,None),'mat':'MMFX2'}
            ]         

    reinf_dict['p_13|9'] = [{'id':'bot','loc':'bottom|middle','desig':'pstrand_13','cover':(1,None),'mat':'pstrand_pre'},
             {'id':'top','loc':'top|middle','desig':'pstrand_9','cover':(0.5,None),'mat':'pstrand_pre'},
            ] 


    reinf_dict['5|3_3_3'] = [{'id':'bot','loc':'bottom|middle','desig':'us5','cover':(0.5,None),'mat':'MMFX2'},
             {'id':'2','loc':'top|middle','desig':'us3','cover':(0.375,None),'mat':'MMFX2'},
             {'id':'3','loc':'top|middle','desig':'us3','cover':(0.375,None),'mat':'MMFX2'},
             {'id':'top','loc':'top|middle','desig':'us3','cover':(0.375,None),'mat':'MMFX2'}
            ]         

    reinf_dict['6|3_3_3'] = [{'id':'bot','loc':'bottom|middle','desig':'us6','cover':(0.5,None),'mat':'MMFX2'},
             {'id':'2','loc':'top|middle','desig':'us3','cover':(0.375,None),'mat':'MMFX2'},
             {'id':'3','loc':'top|middle','desig':'us3','cover':(0.375,None),'mat':'MMFX2'},
             {'id':'top','loc':'top|middle','desig':'us3','cover':(0.375,None),'mat':'MMFX2'}
            ]    

    reinf_dict['4|4'] = [{'id':'bot','loc':'bottom|middle','desig':'us4','cover':(0.375,None),'mat':'MMFX2'},
                         {'id':'top','loc':'top|middle','desig':'us4','cover':(0.375,None),'mat':'MMFX2'}]
    
    return  reinf_dict




def decorate(p1):
    ''' decorate the load displacement curve to show the strain values
    
    
    
    '''
    resdict = {}    
    
    resdict['ec_t_0'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','section_miny:strain', 0.0)
    resdict['ec_t_0.00018'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','section_miny:strain', 0.00018)
    resdict['ec_t_0.004'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','section_miny:strain', 0.004)
    resdict['ec_t_0.016'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','section_miny:strain', 0.016)
    
    
    resdict['ec_c_-0.003'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','section_maxy:strain', -0.003286,mode='<')
    resdict['ec_c_-0.01'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','section_maxy:strain', -0.01,mode='<')
    
    
    resdict['es_t_0.016'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','reinf_bot:strain', 0.0159,mode='>')
    resdict['es_c_-0.016'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','reinf_top:strain', -0.0159,mode='<')
    
    resdict['ss_t_100'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','reinf_bot:stress', 100,mode='>')
    resdict['ss_c_100'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','reinf_top:stress', 100,mode='>')
    
    resdict['ss_t_140'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','reinf_bot:stress', 140,mode='>')
    resdict['ss_c_140'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','reinf_top:stress', -140,mode='<')
    
    resdict['ss_t_225'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','reinf_bot:stress', 140,mode='>')
    resdict['ss_c_0'] = p1.results.curve_search('mid_defl:load','mid_defl:disp','reinf_top:stress', 0,mode='<')
    return resdict
    
    
        
def plot_decorate(p1,resdict,pkey='time_disp',decokeys=None):
    p1.results.process_plotdata(pkey)
    
    
    for key,item in resdict.items():
        if decokeys == None or key in decokeys:
            load = item[0]
            disp = item[1]    
            if load != None:
                p1.results.decorate_plotdata(pkey,key,np.array([[-disp,-load-10],[-disp,-load+10]]),key)        
                
        
def sectionplot(p1,incr=1,col=2,pkey='sectionplot'):
    #pkey = 'section'
    p1.results.add_plotdata(pkey,[],units=['strain','in.'],xylabels=['strain','height'])
    p1.results.process_plotdata(pkey)
    
    for key,item in p1.model.reclist.items():
        
        if item.__class__.__name__ == 'section_fiber':
            strain = p1.results.tdb[key]['data'][incr,col]
            locy = item.locy
            p1.results.decorate_plotdata(pkey,key,np.array([[0,locy],[strain,locy]]),key)  
            #print data,locy
        
    p1.results.line(pkey,legend=False,skey='mono')
    p1.results.savefig(pkey,'png',path=[p1.model.settings['prjname']])



def prjpost(model,resfile=None,decokeys=None):
    ''' this is the post procedure for single model result file '''
    p1 = importfile_opensees_dat(model)
    
    p1.get_res_all(labellist=['load','stress','strain'],unitlist=['kip','ksi','strain'])
    
    p1.get_res('mid_defl',labellist=['load','disp'],unitlist=['kip','in.'])
    p1.get_res('section_miny',labellist=['load','stress','strain'],unitlist=['kip','ksi','strain'])
    p1.get_res('section_maxy',labellist=['load','stress','strain'],unitlist=['kip','ksi','strain'])
    p1.get_res('reinf_bot',labellist=['load','stress','strain'],unitlist=['kip','ksi','strain'])
    p1.get_res('reinf_top',labellist=['load','stress','strain'],unitlist=['kip','ksi','strain'])
    
    
    # get the section plot
    
    sectionplot(p1)
    
    p1.results.add_dmask('flip',{'oper':'FlipSign'})
    p1.results.add_dmask('cutend1',{'oper':'CutDrop','scalar':5})
    
    
    p1.results.add_plotdata('time_disp',[['mid_defl:disp|flip','mid_defl:load|flip']],units=['in.','kip'],xylabels=['displacement','load'],masklist=['cutend1'])
    
    resdict = decorate(p1)
    
    
    plot_decorate(p1,resdict,decokeys=decokeys)
    


    p1.results.line('time_disp')
    
    p1.results.saveallfig('png',path=[p1.model.settings['prjname']])
    
    f1 = open(p1.model.settings['prjname']+'//'+'summary.txt','w')
    
    for key,item in resdict.items():
        if decokeys == None or key in decokeys:
            f1.write('%s:%s\n'% (key,item))
    f1.close()
    
    
    return p1


def run_Tsection(bf):
        fsection_T = create_section.create_T_section_taper(bf,1.25,1.25,2,3.75,10,20,mat='UHPC2',reinf=reinf_dict['7|3_3_3']) 
        #model_T = create_model('t',fsection_T)
        #p_T = prjpost(model_T)
        
        return bf*2

if __name__ == '__main__':

        reinf_dict = create_reinf_layup()

        
        
        '''
        fsection_T = create_section.create_T_section_taper(12,1.25,1.25,2,3.75,10,20,mat='UHPC2',reinf=reinf_dict['7|3_3_3']) 
        model_T = create_model('t',fsection_T)
        p_T = prjpost(model_T)
        
        fsection_T_taper = create_section.create_T_section_taper(12,1.25,0.25,2,3.75,10,20,mat='UHPC2',reinf=reinf_dict['7|3_3_3'])
        model_T_taper = create_model('t_taper',fsection_T_taper)
        p_T_taper= prjpost(model_T_taper)
        
        

        fsection_T_taper_new = create_section.create_T_section_taper(12,1,0.5,1.625,4,10,20,mat='UHPC2',reinf=reinf_dict['5|3_3_3'])
        model_T_taper_new = create_model('t_taper_new',fsection_T_taper_new)
        p_T_taper= prjpost(model_T_taper_new)


        fsection_T_frp1 = create_section.create_T_section_taper(12,1,1,1.625,4,10,20,mat='UHPC2',reinf=reinf_dict['FRP_BAR_4_4|3_3_3'])
        model_T_frp1 = create_model('t_frp1',fsection_T_frp1)
        p_T_taper= prjpost(model_T_frp1)
        

        fsection_T_frp1_p = create_section.create_T_section_taper(12,1,1,1.625,4,10,20,mat='UHPC2',reinf=reinf_dict['P_FRP_BAR_4_4|3_3_3'])
        model_T_frp1_p = create_model('t_frp1_p',fsection_T_frp1_p)
        p_T_taper= prjpost(model_T_frp1_p)
        

        
        # create_I_section_taper                                 (bft,tft,nft1,tft1,bfb,tfb,nfb1,tfb1,hw,tw,nhw,mat=None,reinf=None)
        fsection_I_frp1_p = create_section.create_I_section_taper(12,0.75,5,0.5,1.5,12,0.75,5,0.5,1.5,3.5,1,20,mat='UHPC2',reinf=reinf_dict['P_FRP_CABLE_[7_12.5]|[7_12.5]'])
        model_I_frp1_p = create_model('I_frp1_p',fsection_I_frp1_p)
        p_T_taper= prjpost(model_I_frp1_p)
        '''
        fsection_T_frp1_p = create_section.create_T_section_taper(12,1,1,1.625,4,10,20,mat='UHPC2',reinf=reinf_dict['P_FRP_BAR_4_4|3_3_3'])
        model_T_frp1_p = create_model('t_frp1_p',fsection_T_frp1_p,run=True)
        p_T_taper= prjpost(model_T_frp1_p)
        print 1