#!/usr/bin/env python
"""
This module provide the utility for section
"""
from __future__ import division
from model.section import *
from rebarlib import get_rebars

def import_sec_text(importfile):
    """
    Read preformated text file to create section model and save in /lib
    """

    dataset = imf.import_plain('sec.txt',spliter='\t',
                               formatarray=['s','f','f','s'])
    
    print dataset
    

def create_section_recorder(model1,elemid,sectag,integid, option='none',optionvalue=None,recfile=None):
    ''' create the section recorder for particular element and integration point'''
    
    sec = model1.seclist[sectag]
    targetfiberdict = {}
    targetfiber = None
    if recfile == None:
        recfile =  sectag + '_' + option
    else:
        recfile =  recfile
        
    if option == 'maxy':
        maxvalue = -10000
        
        for key,fiber in sec.fiber.items():
            if (optionvalue != None and optionvalue == fiber.mattag) or optionvalue == None:
                if fiber.locy >maxvalue:
                    maxvalue = fiber.locy
                    targetfiber = fiber
        
    elif option == 'miny':   
        maxvalue = 10000
        for key,fiber in sec.fiber.items():
            if (optionvalue != None and optionvalue == fiber.mattag) or optionvalue == None:
                if fiber.locy < maxvalue:
                    maxvalue = fiber.locy
                    targetfiber = fiber    
    
    elif option =='fiberlib':
        #for key,fiber in sec.fiberlib.items():
        targetfiberdict.update(sec.fiberlib)
    
    elif option == 'all':
        targetfiberdict.update(sec.fiber)
        
    
    else:
        raise KeyError,('Option',option,' do not defined')
    
    if targetfiber != None:
        targetfiberdict[recfile] = targetfiber
    
    
    for key,tfiber in targetfiberdict.items():
        inputdict = {}
        inputdict['sectag'] = 1
        inputdict['elemid'] = elemid
        inputdict['locy'] = tfiber.locy
        inputdict['locz'] = tfiber.locz
        inputdict['mattag'] = tfiber.mattag
        inputdict['recfile'] = model1.settings['prjname'] + '//' 'fibers//'+key 
        model1.recorder(key,'section_fiber',inputdict)
    
    return model1
    


def create_rec_section(b,h,nl,mat=None,reinf=None):
    """
    Create the rectangular section
    ==============parameters=============description=================
    b               widht of the section
    h               height of the section
    nl              number of layers of the section
    mat             [None] T section material tag
    reinf           [None] information of the reinforcements
    =================================================================
    """
    
    paralib = {}
    
    rec= {
        'type':'rectangle',
        'prop':{
            'b':b,
            'h':h,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':nl,
            'startz':-b/2.0,
            'starty':-h/2.0}
    }
    
    paralib['patchlib'] = {'rec':rec}
    paralib['layerlib'] = {}
    paralib['fiberlib'] = {}
    
    if reinf != None:
        secdata = add_reinforcement(reinf,[[-b/2.0,h/2.0],
                                 [b/2.0,h/2.0],
                                 [-b/2.0,-h/2.0],
                                 [b/2.0,-h/2.0]])
    
    
        for key in secdata.keys():
            paralib['fiberlib'][key] = fiber(paralib=secdata[key])
        
    
    fsection = fibersection(paralib=paralib)
    fsection.collect_fibers()
    return fsection
    
def create_T_section(bf,tf,bw,hw,nfl,nw,mat=None,reinf=None):
    """
    Add T section and discritisize into layers
    ==============parameters=============description=================
    bf              witdth of the flanges
    tf              thickness of the flanges
    bw              witdth of the webs
    hw              height of the webs
    nfl             numbers of layers of the flanger
    nw              numbers of layers of the webs
    mat             [None] T section material tag
    reinf           [None] information of the reinforcements
    =================================================================
    
    The default coordinates shown as follows:
    z                     [=======]
    |                        [ ]
    |                        [ ] 
    |                        [ ] 
    |
    -------> y
    
    default origin at the center of the bottom of the webs
    """
    paralib = {}
    
    h_all = hw + tf
    
    flange= {
        'type':'rectangle',
        'prop':{
            'b':bf,
            'h':tf,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':nfl,
            'startz':-bf/2.0,
            'starty':h_all/2.0-tf}
    }
    
    web= {
        'type':'rectangle',
        'prop':{
            'b':bw,
            'h':hw,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':nw,
            'startz': -bw/2.0,
            'starty':-h_all/2.0}
    }    
    
    paralib['patchlib'] = {'flange':flange,'web':web}
    paralib['layerlib'] = {}
    paralib['fiberlib'] = {}
    
  
    # for reinforcement
    if reinf != None:
        secdata = add_reinforcement(reinf,[[-bf/2.0,h_all/2.0],
                                 [bf/2.0,h_all/2.0],
                                 [-bf/2.0,-h_all/2.0],
                                 [bf/2.0,-h_all/2.0]])
    
    
        for key in secdata.keys():
            paralib['fiberlib'][key] = fiber(paralib=secdata[key])
        
    
    fsection = fibersection(paralib=paralib)
    fsection.collect_fibers()
    return fsection
     
    
    return secdata


def create_T_section_taper(bf,tf,tf1,wf,tw,hw,nfl,nw,mat=None,reinf=None):
    """
    Add T section and discritisize into layers
    ==============parameters=============description=================
    bf              witdth of the flanges
    tf              thickness of the flanges
    bw              witdth of the webs
    hw              height of the webs
    nfl             numbers of layers of the flanger
    nw              numbers of layers of the webs
    mat             [None] T section material tag
    reinf           [None] information of the reinforcements
    =================================================================
    
    The default coordinates shown as follows:
    z                     [=======]
    |                        [ ]
    |                        [ ] 
    |                        [ ] 
    |
    -------> y
    
    default origin at the center of the bottom of the webs
    """
    paralib = {}
    
    h_all = hw + tf
    
    dh = tf/nfl    # thickness of the flange layer
    ntf1 = int(tf1/dh)
    ntf2 = int((tf - tf1)/dh)
    
    flange= {
        'type':'rectangle',
        'prop':{
            'b':bf,
            'h':tf1,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':ntf1,
            'startz':-bf/2.0,
            'starty':h_all/2.0-tf1}
    }

    flange_taper= {
        'type':'taper_h',
        'prop':{
            'bb':tw,
            'bt':wf,
            'h':tf-tf1,
            'mattag':mat,
            'numSubdivh':ntf2,
            'startz':-hw/2.0,
            'starty':h_all/2.0-tf}
    }
    
    web= {
        'type':'rectangle',
        'prop':{
            'b':tw,
            'h':hw,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':nw,
            'startz': -tw/2.0,
            'starty':-h_all/2.0}
    }    
    
    if flange_taper['prop']['numSubdivh'] != 0:
        paralib['patchlib'] = {'flange':flange,'web':web,'flange_taper':flange_taper}
    else:
        paralib['patchlib'] = {'flange':flange,'web':web}
        
    paralib['layerlib'] = {}
    paralib['fiberlib'] = {}
    
  
    # for reinforcement
    if reinf != None:
        secdata = add_reinforcement(reinf,[[-bf/2.0,h_all/2.0],
                                 [bf/2.0,h_all/2.0],
                                 [-bf/2.0,-h_all/2.0],
                                 [bf/2.0,-h_all/2.0]])
    
    
        for key in secdata.keys():
            paralib['fiberlib'][key] = fiber(paralib=secdata[key])
        
    
    fsection = fibersection(paralib=paralib)
    fsection.collect_fibers()
    return fsection
     
    


def create_I_section(bft,tft,nft,bfb,tfb,nfb,hw,tw,nhw,mat=None,reinf=None):
    """
    Create the rectangular section
    ==============parameters=============description=================
    bft,tft,nft     width, thickness, and layer number of top flange
    bfb,tfb,nfb     width, thickness, and layer number of bottom flange
    hw,tw,nhw       height, width, and numbe of segments of the section
    mat             [None] T section material tag
    reinf           [None] information of the reinforcements
    =================================================================
    """
    
    paralib = {}
    h_all = tft + tfb + hw
    ft_patch = {
        'type':'rectangle',
        'prop':{
            'b':bft,
            'h':tft,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':nft,
            'startz':-bft/2.0,
            'starty':h_all/2.0-tft}
    }
 
 
    fb_patch = {
        'type':'rectangle',
        'prop':{
            'b':bfb,
            'h':tfb,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':nfb,
            'startz':-bfb/2.0,
            'starty':-h_all/2.0}
    }


    web_patch = {
        'type':'rectangle',
        'prop':{
            'b':tw,
            'h':hw,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':nhw,
            'startz':-tw/2.0,
            'starty':-h_all/2.0+tfb}
    }
    
    
    paralib['patchlib'] = {'ft_patch':ft_patch,'fb_patch':fb_patch,'web_patch':web_patch  }
    paralib['layerlib'] = {}
    paralib['fiberlib'] = {}
    
    if reinf != None:
        secdata = add_reinforcement(reinf,[[-b/2.0,h/2.0],
                                 [b/2.0,h/2.0],
                                 [-b/2.0,-h/2.0],
                                 [b/2.0,-h/2.0]])
    
    
        for key in secdata.keys():
            paralib['fiberlib'][key] = fiber(paralib=secdata[key])
            
    
    fsection = fibersection(paralib=paralib)
    fsection.collect_fibers()
    return fsection


def create_I_section_taper(bft,tft,nft1,tft1,wft,bfb,tfb,nfb1,tfb1,wfb,hw,tw,nhw,mat=None,reinf=None):
    """
    Create the rectangular section
    ==============parameters=============description=================
    bft,tft,nft     width, thickness, and layer number of top flange
    bfb,tfb,nfb     width, thickness, and layer number of bottom flange
    hw,tw,nhw       height, width, and numbe of segments of the section
    mat             [None] T section material tag
    reinf           [None] information of the reinforcements
    =================================================================
    """
    
    paralib = {}
    h_all = tft + tfb + hw
    
    ft_patch = {
        'type':'rectangle',
        'prop':{
            'b':bft,
            'h':tft1,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':nft1,
            'startz':-bft/2.0,
            'starty':h_all/2.0-tft1}
    }

    ft_patch_taper = {
        'type':'taper_h',
        'prop':{
            'bt':wft,
            'bb':tw,
            'h':tft - tft1,
            'mattag':mat,

            'numSubdivh':int((tft - tft1)/(tft1/nft1)),
            'startz':0,
            'starty':h_all/2.0-tft}
    } 
 
    fb_patch = {
        'type':'rectangle',
        'prop':{
            'b':bfb,
            'h':tfb1,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':nfb1,
            'startz':-bfb/2.0,
            'starty':-h_all/2.0}
    }

    fb_patch_taper = {
        'type':'taper_h',
        'prop':{
            'bb':wfb,
            'bt':tw,
            'h':tfb - tfb1,
            'mattag':mat,
            'numSubdivh':int((tfb - tfb1)/(tfb1 /nfb1)),
            'startz':0,
            'starty':-h_all/2.0+tfb1}
    }
    
    web_patch = {
        'type':'rectangle',
        'prop':{
            'b':tw,
            'h':hw,
            'mattag':mat,
            'numSubdivb':1,
            'numSubdivh':nhw,
            'startz':-tw/2.0,
            'starty':-h_all/2.0+tfb}
    }
    
    
    paralib['patchlib'] = {'ft_patch':ft_patch,'ft_patch_taper':ft_patch_taper,'fb_patch':fb_patch,'fb_patch_taper':fb_patch_taper,'web_patch':web_patch  }
    paralib['layerlib'] = {}
    paralib['fiberlib'] = {}
    
    if reinf != None:
        secdata = add_reinforcement(reinf,[[-bfb/2.0,h_all/2.0],
                                 [bfb/2.0,h_all/2.0],
                                 [-bfb/2.0,-h_all/2.0],
                                 [bfb/2.0,-h_all/2.0]])
    
    
        for key in secdata.keys():
            paralib['fiberlib'][key] = fiber(paralib=secdata[key])
            
    
    fsection = fibersection(paralib=paralib)
    fsection.collect_fibers()
    return fsection

def add_reinforcement(reinf,conner):
    """
    Add reinforcement to the section model
    input datastructure
    =====================[list]: reinf, [dict]: reinf[i]==========
    reinf[i].type                     passive/pre/post/web
    reinf[i].desig
    reinf[i].loc          top/bottom/
    reinf[i].(cover1,cover2)                      us7
    reinf[i].mat
    ==============================================================
    """
    
    
    secdata = {}
    for i in range (0,len(reinf)):
        # obtain rebar properies
        reinf[i].update(rebar_property(reinf[i]['desig']))
        # obtain rebar location informations
        reinf_loc = rebar_locator(reinf[i],conner)
        
        secdata['reinf_'+reinf[i]['id']] = {'locy':reinf_loc[0],
                      'locz':reinf_loc[1],
                      'area':rebar_property(reinf[i]['desig'])['area'],
                      'width':None,
                      'thickness':None,
                      'mattag':reinf[i]['mat']}
    return secdata

def rebar_locator(rebar,conner):
    """
    Return the rebar location based on the location type and conner
    """
    loc = rebar['loc']
    cover = rebar['cover']
    dia = rebar['diameter']
    
    topleft = conner[0]
    topright = conner[1]
    bottomleft = conner[2]
    bottomright = conner[3]
    
    reinf_loc = None    
    if 'top' in loc and 'middle' in loc:
        reinf_loc = ((topleft[1]+topright[1])/2-cover[0]-dia/2.0,(topleft[0]+topright[0])/2)
        
    elif 'bottom' in loc and 'middle' in loc:
        reinf_loc = ((bottomleft[1]+bottomright[1])/2+cover[0]+ dia/2.0,(bottomleft[0]+bottomright[0])/2) # to the rebar center

    elif 'bottom' in loc and 'left' in loc:
        reinf_loc = ((bottomleft[1]+bottomright[1])/2+cover[0]+ dia/2.0,(bottomleft[0]+cover[1]))


    return reinf_loc
    
    
def rebar_property(desig):
    ''' provide the rebar area based on the designation'''
    rebarlib = get_rebars()
    
    if desig in rebarlib.keys():
        return rebarlib[desig]
    else:
        raise TypeError,('rebar designation:"',desig,'" do not defined')
    return rebar

def create_circular_reinforced(DSec,coverSec,numBarsSec,barAreaSec,coremattag,covermattag,rebarmattag,ri=0,nfCoreR=4,nfCoreT=8,nfCoverR=4,nfCoverT=8):
    ''' create a circular reinforced section
    set DSec [expr 1.*$ft]; 		# Column Diameter
    set coverSec [expr 0.75*$in];	# Column cover to reinforcing steel NA.
    set numBarsSec 10;		# number of uniformly-distributed longitudinal-reinforcement bars
    set barAreaSec [expr 2.*$in2];	# area of longitudinal-reinforcement bars
    set SecTag 1;			# set tag for symmetric section
    set ri 0.0;			# inner radius of the section, only for hollow sections
    set ro [expr $DSec/2];	# overall (outer) radius of the section
    set nfCoreR 8;		# number of radial divisions in the core (number of "rings")
    set nfCoreT 10;		# number of theta divisions in the core (number of "wedges")
    set nfCoverR 4;		# number of radial divisions in the cover
    set nfCoverT 10;		# number of theta divisions in the cover
    coremattag,covermattag,rebarmattag  # material tag of core concrete, cover concrete and steel rebars
   
    '''
    ro = DSec/2
    rc = ro - coverSec
    
    # Define the core patch
    patch_core = {'type':'circ',
                  'prop':{'mattag':coremattag,
                  'numSubdivCirc':nfCoreT,
                  'numSubdivRad': nfCoreR,
                  'intRad':ri,
                  'extRad':rc}}		
    
    # Define the core patch
    patch_cover = {'type':'circ',
                   'prop':{'mattag':covermattag,
                  'numSubdivCirc':nfCoverT,
                  'numSubdivRad': nfCoverR,
                  'intRad':rc,
                  'extRad':ro}}
    
    # Define the steel layer
    layer_reinf = {'type':'circ',
                   'prop':{'mattag':rebarmattag,
                   'numBar':numBarsSec,   # 
                   'areaBar':barAreaSec,
                   'radius':rc,
                   'startAng':360.0/float(numBarsSec),
                   'endAng':360}}    
    paralib = {}
    paralib['patchlib'] = {'core':patch_core,'cover':patch_cover}
    paralib['layerlib'] = {'reinf':layer_reinf}
    
    fsection = fibersection(paralib=paralib)
    return fsection
    
    

if __name__ == '__main__':
    create_T_section_ins()