
import sys
import os
import datetime
sys.path.append('../../webfe/')
import numpy as np
from core.model.registry import model
from core.export.export import exporter
from core.settings import settings
from core.procedures.t_section import tsec_planeconfig
from core.procedures.rec_section import rec_planeconfig
from core.imports.marc.import_marc_dat import importfile_marc_dat
from core.post.import_marc_t16 import post_t16
from core.plots.plots import tpfdb

from command import commandparser



def test_postprocess():
    c1 = commandparser()
    
    '''
    c1.parser('*post_marc_t16_open,M:\\marcworking\\Tbeam_interface_tune\\1t1s\\1t1s_elastic.t16')
    c1.parser('*post_marc_t16_addrequest,Time_837,Time,58.63,-1,1000,1')
    c1.parser('*post_marc_t16_addrequest,Node Scalar_8481,Node Scalar,Displacement Y,MIDDLE_NODE,-1,1000,1')
    c1.parser('*post_marc_t16_addrequest,Element Scalar_9571,Element Scalar,Comp 11 of Total Strain,0,MIDDLE_REBAR_ELEMENT,-1,1000,1')
    c1.parser('*post_marc_t16_addrequest,Element Scalar_9668,Element Scalar,Comp 11 of Total Strain,-1,REBAR_ELEMENTS,-1,1e6,1')
    c1.parser('*post_marc_t16_addrequest,BOTTOM_INTERFACE11,Element Scalar,Comp 11 of Stress,-1,BOTTOM_INTERFACE,-1,1e6,1')
    c1.parser('*post_marc_t16_addrequest,TOP_INTERFACE11,Element Scalar,Comp 11 of Stress,-1,TOP_INTERFACE,-1,1e6,1')
    c1.parser('*post_marc_t16_addrequest,BOTTOM_INTERFACE22,Element Scalar,Comp 22 of Stress,-1,BOTTOM_INTERFACE,-1,1e6,1')
    c1.parser('*post_marc_t16_addrequest,TOP_INTERFACE22,Element Scalar,Comp 22 of Stress,-1,TOP_INTERFACE,-1,1e6,1')
    c1.parser('*post_marc_t16_addrequest,BOTTOM_INTERFACE33,Element Scalar,Comp 33 of Stress,-1,BOTTOM_INTERFACE,-1,1e6,1')
    c1.parser('*post_marc_t16_addrequest,TOP_INTERFACE33,Element Scalar,Comp 33 of Stress,-1,TOP_INTERFACE,-1,1e6,1')
    c1.parser('*post_marc_t16_getdata')
    
    c1.parser('*plot_edit_tdb_increment,RebarIncrments,Element Scalar_9668,-1,-1,1')
    c1.parser('*plot_edit_tdb_increment,TopInterfaceIncrments11,TOP_INTERFACE11,-1,-1,1')
    c1.parser('*plot_edit_tdb_increment,BotInterfaceIncrments11,BOTTOM_INTERFACE11,-1,-1,1')
    c1.parser('*plot_edit_tdb_increment,TopInterfaceIncrments22,TOP_INTERFACE22,-1,-1,1')
    c1.parser('*plot_edit_tdb_increment,BotInterfaceIncrments22,BOTTOM_INTERFACE22,-1,-1,1')
    c1.parser('*plot_edit_tdb_increment,TopInterfaceIncrments33,TOP_INTERFACE33,-1,-1,1')
    c1.parser('*plot_edit_tdb_increment,BotInterfaceIncrments33,BOTTOM_INTERFACE33,-1,-1,1')
    
    c1.parser('*import_marc_dat,M:\\marcworking\\Tbeam_interface_tune\\1t1s\\1t1s_elastic.dat,Extended')
    
    
    # read csv test results
    c1.parser('*post_plain_new')
    c1.parser('*post_plain_filelist ,M:\\marcworking\\Tbeam_interface_tune\\1t1s\\s_1t1s_hook.csv')
    
    # update the units of the FEM results
    c1.parser('*plot_edit_tdb_table_unit,Node Scalar_8481,0:0,in.')
    c1.parser('*plot_edit_tdb_table_unit,Time_837,0:0,kip')
    
    c1.parser('*post_save,tt.pyres')
    c1.parser('*save_project,tt.pydat')
    
    '''
    c1.parser('*open_project,tt.pydat')
    c1.parser('*post_load,tt.pyres')
    
    c1.parser('*plot_edit_tdb_coordlist,BOTTOM_INTERFACE11,BOTTOM_INTERFACE_coord')
    c1.parser('*plot_edit_tdb_coordlist,TOP_INTERFACE11,TOP_INTERFACE_coord')
    c1.parser('*plot_edit_tdb_coordlist,Element Scalar_9668,Rebar Location')
    
    
    # add load versus displacement curve
    c1.parser('*plot_pdata_add,plot_448,Node Scalar_8481:Node_865|col_flipsign,Time_837:time')
    c1.parser('*plot_pdata_add,plot_448,s_1t1s_hook:S.Pot-3,s_1t1s_hook:Load')
    c1.parser('*plot_figure_add,plot_448,plot_448,test,line-one axis')
    c1.parser('*plot_figure_save,plot_448,jpg,loaddisp.jpg')
    
    # add load versus bottom strain curve
    c1.parser('*plot_pdata_add,plot_strain,Element Scalar_9571:Elem_240-0,Time_837:time')
    c1.parser('*plot_pdata_add,plot_strain,s_1t1s_hook:S.G-0,s_1t1s_hook:Load')
    c1.parser('*plot_figure_add,plot_strain,plot_strain,test,line-one axis')
    c1.parser('*plot_figure_save,plot_strain,jpg,loadstrain.jpg')
    
    # add rebar strain distribution for certain increment
    c1.parser('*plot_pdata_add,plot_rebstrain,Rebar Location:Coord X,RebarIncrments:10')
    c1.parser('*plot_pdata_add,plot_rebstrain,Rebar Location:Coord X,RebarIncrments:20')
    c1.parser('*plot_pdata_add,plot_rebstrain,Rebar Location:Coord X,RebarIncrments:30')
    c1.parser('*plot_pdata_add,plot_rebstrain,Rebar Location:Coord X,RebarIncrments:40')
    c1.parser('*plot_pdata_add,plot_rebstrain,Rebar Location:Coord X,RebarIncrments:49')
    c1.parser('*plot_figure_add,plot_rebstrain,plot_rebstrain,test,line-one axis')
    c1.parser('*plot_figure_save,plot_rebstrain,jpg,rebarstrainincr.jpg')
    
    # add rebar strain distribution for certain increment
    c1.parser('*plot_pdata_add,plot_topstrain11,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments11:10')
    c1.parser('*plot_pdata_add,plot_topstrain11,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments11:20')
    c1.parser('*plot_pdata_add,plot_topstrain11,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments11:30')
    c1.parser('*plot_pdata_add,plot_topstrain11,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments11:40')
    c1.parser('*plot_pdata_add,plot_topstrain11,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments11:49')
    c1.parser('*plot_figure_add,plot_topstrain11,plot_topstrain11,test,line-one axis')
    c1.parser('*plot_figure_save,plot_topstrain11,jpg,topstrainincr11.jpg')
    
    # add rebar strain distribution for certain increment
    c1.parser('*plot_pdata_add,plot_botstrain11,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments11:10')
    c1.parser('*plot_pdata_add,plot_botstrain11,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments11:20')
    c1.parser('*plot_pdata_add,plot_botstrain11,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments11:30')
    c1.parser('*plot_pdata_add,plot_botstrain11,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments11:40')
    c1.parser('*plot_pdata_add,plot_botstrain11,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments11:49')
    c1.parser('*plot_figure_add,plot_botstrain11,plot_botstrain11,test,line-one axis')
    c1.parser('*plot_figure_save,plot_botstrain11,jpg,botstrainincr11.jpg')
    
    # add rebar strain distribution for certain increment
    c1.parser('*plot_pdata_add,plot_topstrain22,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments22:10')
    c1.parser('*plot_pdata_add,plot_topstrain22,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments22:20')
    c1.parser('*plot_pdata_add,plot_topstrain22,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments22:30')
    c1.parser('*plot_pdata_add,plot_topstrain22,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments22:40')
    c1.parser('*plot_pdata_add,plot_topstrain22,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments22:49')
    c1.parser('*plot_figure_add,plot_topstrain22,plot_topstrain22,test,line-one axis')
    c1.parser('*plot_figure_save,plot_topstrain22,jpg,topstrainincr22.jpg')
    
    # add rebar strain distribution for certain increment
    c1.parser('*plot_pdata_add,plot_botstrain22,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments22:10')
    c1.parser('*plot_pdata_add,plot_botstrain22,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments22:20')
    c1.parser('*plot_pdata_add,plot_botstrain22,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments22:30')
    c1.parser('*plot_pdata_add,plot_botstrain22,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments22:40')
    c1.parser('*plot_pdata_add,plot_botstrain22,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments22:49')
    c1.parser('*plot_figure_add,plot_botstrain22,plot_botstrain22,test,line-one axis')
    c1.parser('*plot_figure_save,plot_botstrain22,jpg,botstrainincr22.jpg')
    
    # add rebar strain distribution for certain increment
    c1.parser('*plot_pdata_add,plot_topstrain33,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments33:10')
    c1.parser('*plot_pdata_add,plot_topstrain33,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments33:20')
    c1.parser('*plot_pdata_add,plot_topstrain33,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments33:30')
    c1.parser('*plot_pdata_add,plot_topstrain33,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments33:40')
    c1.parser('*plot_pdata_add,plot_topstrain33,TOP_INTERFACE_coord:Coord X,TopInterfaceIncrments33:49')
    c1.parser('*plot_figure_add,plot_topstrain33,plot_topstrain33,test,line-one axis')
    c1.parser('*plot_figure_save,plot_topstrain33,jpg,topstrainincr33.jpg')
    
    # add rebar strain distribution for certain increment
    c1.parser('*plot_pdata_add,plot_botstrain33,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments33:10')
    c1.parser('*plot_pdata_add,plot_botstrain33,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments33:20')
    c1.parser('*plot_pdata_add,plot_botstrain33,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments33:30')
    c1.parser('*plot_pdata_add,plot_botstrain33,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments33:40')
    c1.parser('*plot_pdata_add,plot_botstrain33,BOTTOM_INTERFACE_coord:Coord X,BotInterfaceIncrments33:49')
    c1.parser('*plot_figure_add,plot_botstrain33,plot_botstrain33,test,line-one axis')
    c1.parser('*plot_figure_save,plot_botstrain33,jpg,botstrainincr33.jpg')
    
    #c1.results.save('tt.pyres')
    #c1.parser('*save_project,tt.pydat')
    print 1


def test_importt16():


    model1 = model(settings)
    f1 = post_t16('M:\\marcworking\\Tbeam_interface_tune\\1t1s\\1t1s_elastic.t16')
    res = f1.postset_incr(['Element Scalar','Comp 11 of Total Strain',0,'REBAR_ELEMENTS',-1,1e6,1])




def test_table_operation():
    aa = tpfdb()
    
    aa.add('a',np.array([[1,2,3],[4,5,6]]).T,unitlist=['N/A','N/A'],labellist=['L1','L2'])
    
    print aa.retrive('a',0)
    aa.replace('a','L1',np.array([1,5,7]).T)
    print aa.retrive('a',0)
    print aa.tdb['a']

    
    aa.insert('a','L2',np.array([6,8,9]).T,'mm','L4')
    print aa.tdb['a']
    print aa.retrive('a',0)
    print aa.retrive('a',1)
    print aa.retrive('a',2)
    
    aa.append('a',np.array([10,18,19]).T,'mm','L4')
    print aa.tdb['a']
    print 1
    
    oo_label,oo_unit,oo_data = aa.row_to_column('a',0,1)
    print oo_unit
    print oo_label
    print oo_data
    
    aa.new_or_replace('bb','L1',oo_data,oo_unit,oo_label)
    
    aa.tmask_incrment_setresults('a',1)
    print aa.tdb['bb']
    print aa.tdb


def test_import_marcdat():
    f1 = importfile_marc_dat('M:\\marcworking\\Tbeam_interface_tune\\22_elastic.dat',stylesetting='Extended')
    
    # add nodes to model
    model1 = f1.add_nodes(model1)
    
    # add elements to model
    model1 = f1.add_elements(model1)


def test_procedure_dowelaction():
    model1 = model(settings)

    #model1 = tsec_planeconfig(model1,'tsec1',12,1.25,1,3.75,2,4,1) #bf,tf,tf1,hw,tw,d,ds
    model1 = rec_planeconfig(model1,'rec1',2,4,3,1,1,16,1)
    
    
    
    
    model1.modelsavetofile('temp.pydat')
    
    
    model1 = model1.modelloadbyfile('temp.pydat')
    print model1.get_element_typeid(100)
    print 1


if __name__ == '__main__':
    
    test_procedure_dowelaction()
    
