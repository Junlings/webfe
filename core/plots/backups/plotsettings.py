#!/usr/bin/env python
"""
this module is to customarize the plot for publication purpose
ideally, this only define the plot format and data interface
and the plot can be realized by matlab, matplotlib, and html
or any other engines

"""
import re
import pickle
from math import *
import copy
class default_css_style():
    ''' css style figure settings '''
    label = {
        #'fontsize':10,
        #'font-family':'century',
        #'font-serif':'century',
        'fontstyle': 'default',
        'coding': 'latex',
        'angle':0,
        'size': 8,
        'text':'default'
    }
    
    tick = {
        'axis':'both',  # operation object
        'which': 'both',  # major|minor|both
        'left':'off',   # the display of ticks at the designated location
        'right':'off',
        'top':'off',
        'bottom':'off',
        'labeltop':'off',  # display of labels
        'labelbottom':'off',
        'labelleft':'off',
        'labelright':'off',
        'length': 4,  #in points
        'width': 1,
        'color': 'k',
        'direction' : 'in',
        'labelsize': 'medium',
        'pad':1,
        'labelcolor':'k',
        'zorder': 1,  # ticklabel zorder
        #'major.pad': 4,
        #'major.size': 4,
        #'minor.pad': 4,
        #'minor.size': 2,
    }
    

            
   
    axes = {
           'loc': [0.15,0.15,0.7,0.7],  # left,bottom,width,height
           'polar': False,
           #'color_cycle':['b','g','r','c','m','y','k'],
           #'edgecolor': 'k',
           #'facecolor': 'w',
           #'limits': [-7,7],
           #'use_locale': False,
           'grid': False,
           'hold': True,
           'frameon': False,
           #'label': '',
           #'frameon' : False,
           #'labelcolor': 'k',
           #'labelsize':  'medium',
           #'labelweight': 'normal',
           #'linewidth':1,
           #'titlesize': 'large',
           #'unicode_minus': True,
    }
    
    axis = {
        'axes': None,
        'limits': ['auto','auto'],
        # name of font styles
        'labelfont':'default',  # with respect to label style name
        'ticklabelfont':'default',
        # scheme of find tick locations, and customrized labels
        'locator': 'auto', 
        'position': 'bottom',
        'mode':'x',
        # units associate with axis
        'unit': None,
        'grid': 'grid',
    }
        
    locator = {
        'mode':'auto',  # mode of locator, 'auto','index','fixed','none','linear'
        'prop':None,    # this is the prop associate with locator mode
        'labels':None,  # this is the custom labels
        'minor':0       # this is the numbers of minor ticks
        
        
    }
    
    font = {
        #'cursive' : ['Apple Chancery', 'Textile', 'Zapf Chancery', 'Sand', 'cursive'],
        'family' : 'sans-serif',
        #'fantasy' : ['Comic Sans MS', 'Chicago', 'Charcoal',
        #             'ImpactWestern', 'fantasy'],
        #'monospace' : ['Bitstream Vera Sans Mono', 'DejaVu Sans Mono',
        #               'Andale Mono', 'Nimbus Mono L', 'Courier New',
        #               'Courier', 'Fixed', 'Terminal', 'monospace'],
        #'sans-serif' : ['Bitstream Vera Sans', 'DejaVu Sans',
        #                'Lucida Grande', 'Verdana', 'Geneva', 'Lucid',
        #                'Arial', 'Helvetica', 'Avant Garde', 'sans-serif'],
        #'serif' : ['Bitstream Vera Serif', 'DejaVu Serif',
        #           'New Century Schoolbook', 'Century Schoolbook L',
        #           'Utopia', 'ITC Bookman', 'Bookman', 'Nimbus Roman No9 L',
        #           'Times New Roman', 'Times', 'Palatino', 'Charter', 'serif'],
        'size' : 12,
        'stretch' : 'normal',
        'style' : 'normal',
        'variant' : 'normal',
        'weight' : 'normal',
    }
    
    latexfont = {
        'cursive' : ['Apple Chancery', 'Textile', 'Zapf Chancery', 'Sand', 'cursive'],
        'family' : 'sans-serif',

        'monospace' : ['Bitstream Vera Sans Mono', 'DejaVu Sans Mono',
                       'Andale Mono', 'Nimbus Mono L', 'Courier New',
                       'Courier', 'Fixed', 'Terminal', 'monospace'],
        'sans-serif' : ['Bitstream Vera Sans', 'DejaVu Sans',
                        'Lucida Grande', 'Verdana', 'Geneva', 'Lucid',
                        'Arial', 'Helvetica', 'Avant Garde', 'sans-serif'],
        'serif' : ['Bitstream Vera Serif', 'DejaVu Serif',
                   'New Century Schoolbook', 'Century Schoolbook L',
                   'Utopia', 'ITC Bookman', 'Bookman', 'Nimbus Roman No9 L',
                   'Times New Roman', 'Times', 'Palatino', 'Charter', 'serif'],
    }
    
    
    text = {
        'color' : 'k',
        'dvipnghack':None,
        'hinting':True,
        'usetex': False,
        'fontsize':10
        }
    
    box = {
        'boxstyle': 'square',
        'fc': 'w',          # face color
        'ec': 'k',          # edge color
        'lw': 2,             # line width
    }
    
    textbox = {
        'x' : 0,  # loc
        'y' : 0,  # loc
        'zorder': '0', 
        's' : '',  # content
        'fontproperties' : 'textbox', # font style
        'alpha':1,  # transparent
        'backgroundcolor':'w',
        'bbox': 'default',  # box style
        'color':'k',
        'ha': 'center', # horizontal alignment
        'va': 'center', # vertical alignment
        'visible':'True',
        'rotation':0,
        
    }
    
    annotate ={
        's':'',
        'xy': (0,0),         # location of annotate point
        'xytext':None,       # location of text
        'xycoords':'data',   # annotate point coordinate system
        'textcoords':'data', # text coordinate system
        'arrowprops':None,
        
        
        
    }
    
    
    latex = {
        'preamble' : [''],
        'preview': False,
        'unicode': False,
        
    }

        
    line = {
        'antialiased': True, 
        'color':'b', 
        'dash_capstyle':'butt', 
        'dash_joinstyle':'round', 
        'linestyle':'-', 
        'linewidth': 1, 
        'marker': None, 
        'markeredgewidth':0.5, 
        'markersize':6, 
        'solid_capstyle':'projecting', 
        'solid_joinstyle':'round',    
    }
    legend = {
        'borderaxespad': 0.5,
        'borderpad':0.4,
        'columnspacing':2, 
        'fancybox': False,
        'fontsize': 'large',
        'frameon': True,
        'handleheight': 0.7,
        'handlelength': 2,
        'handletextpad':0.8, 
        'isaxes': True,
        'labelspacing': 0.5, 
        'loc': 'upper right',
        'markerscale': 1, 
        'numpoints':2 ,
        'shadow': False, 

    }
    
    figure = {
        #'autolayout': False,
        'figsize':[8.0,6.0],
        'dpi':600,
        'edgecolor': 'w',
        'facecolor':"0.75",
    }
    
    subplot = {
        'bottom': 0.1,
        'hspace': 0.2,
        'right': 0.9,
        'left': 0.125,
        'top': 0.9,
        'wspace':0.2, 
        
    }
    
    backend = {
        'type': 'TkAgg',
        'qt4':'PyQt4',
        '_fallback': True,
        
    }
    
    
    mathtext = {
        'bf' : 'serif:bold',
        'cal' :	'cursive',
        'default' : 'it',
        'fallback_to_cm' : 'True',
        'fontset' : 'cm',
        'it' : 'serif:italic',
        'rm' : 	'serif',
        'sf' : 'sans\-serif',
        'tt' : 'monospace',
    }
    def get(self,key):
        return getattr(self,key)
        

class figstyle():
    """ this is the class to connect to css files """
    def __init__(self):
        self.default = default_css_style()
    
    def write_default(self,file):
        self.output = ''
        
        self.export_key('figure')
        self.export_key('axes')
        self.export_key('axis')
        self.export_key('locator')
        self.export_key('tick')
        
        f1 = open(file,'w')
        f1.write(self.output)
        
    def export_key(self,targetkey):
        self.output += '%s default {\n' % targetkey
        
        for key in self.default.get(targetkey).keys():
            self.output += ' '*4 + '%-15s:%-20s\n' % (key,self.default.get(targetkey)[key])
        self.output += '}\n\n'
        return 1

    
      
class stylelib():
    """ This is the stylelib that defines the plot style assembling"""
    def __init__(self):
        # default style 
        self.default = default_css_style()
        
        # unique style
        self.backend = self.default.backend.copy()  # specify the backend
        self.figure = self.default.figure.copy()    # specify the figure size
        self.subplot = self.default.subplot.copy()  # specify the subplot setting
        self.text = self.default.text.copy()  # specify the subplot setting

        
        # stylelib
        
        self.axeslib = {'default':self.default.axes} # lib of axes settings
        self.axislib = {'default':self.default.axis} # lib of axis settings
        self.ticklib = {'default':self.default.tick} # lib of tick settings
        self.linelib = {'default':self.default.line} # lib of plotline settingd
        self.guidelinelib = {'default':self.default.line} # lib of grid/edge line
        
        self.labellib = {'default':self.default.label} # lib of labels 
        self.mathtextlib = {'default':self.default.mathtext} 
        self.fontlib = {'default':self.default.font}   # lib of fonts
        self.latexfontlib = {'default':self.default.latexfont} #lib of latex fonts
        self.latex = {'default':self.default.latex}  # 
        self.legendlib = {'default':self.default.axes}
        self.locatorlib = {'default':self.default.locator}
        
        self.boxlib = {'default':self.default.box}  #textbooxlib
        self.textboxlib = {'default':self.default.textbox}  #textbooxlib
        
    def setSubplot(self,**kargs):
        self.Subplot.update(kargs)
        
    def setFigure(self,**kargs):
        self.figure.update(kargs)
        
    def setBackend(self,**kargs):
        self.backend.update(kargs)
    
    def add(self,target,key,**kargs):
        self.get(target)[key] = self.get(target)['default'].copy()
        self.get(target)[key].update(kargs)
    
    def update(self,target,key,**kargs):
        self.get(target)[key].update(kargs)
    
    def empty(self,target):
        self.get(target)['default'] = self.get(target)['default'].copy()
        
    def get(self,key):
        return getattr(self,key)
        
    def set(self,target,**kargs):
        self.get(target).update(kargs)

    def load_linelib_bw(self):
        # first reset the linelib
        self.empty('linelib')
        
        # then dump the 
        self.add('linelib',1,color='k',marker='*',linestyle='-',markersize=4)
        self.add('linelib',2,color='k',marker='o',linestyle='--',markersize=4)
        self.add('linelib',3,color='k',marker='+',linestyle='-.',markersize=4)
        self.add('linelib',4,color='k',marker='.',linestyle=':',markersize=4)
        self.add('linelib',5,color='k',marker=',',linestyle=':',markersize=4)
        self.add('linelib',6,color='k',marker='d',linestyle=':',markersize=4)
        self.add('linelib',7,color='k',marker='|',linestyle=':',markersize=4)
        self.add('linelib',8,color='k',marker='-',linestyle=':',markersize=4)
        self.add('linelib',9,color='k',marker='v',linestyle=':',markersize=4)
        self.add('linelib',10,color='k',marker='^',linestyle=':',markersize=4)
        self.add('linelib',11,color='k',marker='<',linestyle=':',markersize=4)
        self.add('linelib',12,color='k',marker='>',linestyle=':',markersize=4)
        self.add('linelib',13,color='k',marker='1',linestyle=':',markersize=4)
        self.add('linelib',14,color='k',marker='2',linestyle=':',markersize=4)
        self.add('linelib',15,color='k',marker='3',linestyle=':',markersize=4)
        self.add('linelib',16,color='k',marker='4',linestyle=':',markersize=4)
        self.add('linelib',17,color='k',marker='s',linestyle=':',markersize=4)
        self.add('linelib',18,color='k',marker='p',linestyle=':',markersize=4)
        self.add('linelib',19,color='k',marker='h',linestyle=':',markersize=4)
        self.add('linelib',20,color='k',marker='H',linestyle=':',markersize=4)
        self.add('linelib',21,color='k',marker='x',linestyle=':',markersize=4)
        
    def load_four_tick(self):
        ''' add major and minor axes and corresponing ticks '''
        # add axes
        self.add('axeslib','axes_major',grid=True,frameon=True)
        self.add('axeslib','axes_minor',grid=True)
        
        # add axis
        self.add('axislib','x1',axes='axes_major',label='x1',unit='Undefined',
                 position='bottom',mode='x',
                 labelfont='label',ticklabelfont='ticklabel')
        self.add('axislib','y1',axes='axes_major',label='y1',unit='Undefined',
                 position='left',mode='y',
                 labelfont='label',ticklabelfont='ticklabel')
        self.add('axislib','x2',axes='axes_minor',label='x2',unit='Undefined',
                 position='top',mode='x',
                 labelfont='label',ticklabelfont='ticklabel',
                 limits=['link','x1'])
        self.add('axislib','y2',axes='axes_minor',label='y2',unit='Undefined',
                 position='right',mode='y',
                 labelfont='label',ticklabelfont='ticklabel',
                 limits=['link','y1'])
        
        # add tickes
        self.add('ticklib','x1',axis='x',which='major',
                top='off',bottom='on',
                labeltop='off',labelbottom='on',labelsize=8,pad=2)
    
        self.add('ticklib','x2',axis='x',which='major',
                top='on',bottom='off',
                labeltop='on',labelbottom='off',labelsize=8,pad=2)
        
        self.add('ticklib','y1',axis='y',which='major',
                left='on',right='off',
                labelleft='on',labelright='off',labelsize=8)
    
        self.add('ticklib','y2',axis='y',which='major',
                left='off',right='on',
                labelleft='off',labelright='on',labelsize=8)          
        
    def load_default_locator(self):
        # based on the num of data plots, prop=[base, offset]
        self.add('locatorlib','auto',
                 mode='auto',prop=[0,0],labels=None,minor=0)  # interval, absolute
        
        self.add('locatorlib','index',
                 mode='index',prop=[2,0],labels=None,minor=0)  # interval, absolute
        
        # based on the fixed location prop=[[list of locs],maxnbin]
        self.add('locatorlib','fixed',
                 mode='fixed',prop=[[1,2,3,4,5,6,7],20],labels=None,minor=0)
        
        # no labels
        self.add('locatorlib','none',
                 mode='none',prop=[],labels=None,minor=0)
        
        # linear labels
        self.add('locatorlib','linear',
                 mode='linear',prop=[5,0],labels=None,minor=0)  # prop = [number ]
        
        # multiple lables prop = [base, offset]
        self.add('locatorlib','multiple',
                 mode='multiple',prop=[0.75,0],labels=None,minor=0)
                
        self.add('locatorlib','maxN',
                 mode='maxN',prop={'nbins':6,'steps':[1,2,6],'integral':True,
                                          'symmetric':False
                                          },labels=None,minor=0)       
    
    def load_boxlib(self):
        self.add('boxlib','larrow',boxstyle='larrow')
        self.add('boxlib','rarrow',boxstyle='rarrow,pad=0.3')
        self.add('boxlib','round',boxstyle='round,pad=0.3,rounding_size=None')
        self.add('boxlib','round4',boxstyle='round4,pad=0.3,rounding_size=None')
        self.add('boxlib','roundtooth',boxstyle='roundtooth,pad=3,tooth_size=None')
        self.add('boxlib','sawtooth',boxstyle='sawtooth')
        self.add('boxlib','square',boxstyle='square,pad=0.3')
    
    def write_default(self,file):
        self.output = ''
        
        #self.export_key('figure')
        self.export_lib('axes')
        self.export_lib('axis')
        self.export_lib('tick')
        self.export_lib('locator')
        self.export_lib('line')
        f1 = open(file,'w')
        f1.write(self.output)
        
    def export_lib(self,libname):
        lib = self.get(libname+'lib')
        for key in lib.keys():
            self.export_key(libname,lib[key],key)        
        
    def export_key(self,libname,lib,libkey):
        self.output += '%s %s {\n' % (libname,libkey)
        
        for key in lib.keys():
            self.output += ' '*4 + '%-15s:%-20s\n' % (lib[key])
        self.output += '}\n\n'
        return 1
    
    def get(self,key):
        return getattr(self,key)
        
def publish_style():
    """
    overrid by the subclass
    To create and return customized figure instance
    Now two mode of draft and publish are supported
    """
    pub = stylelib()
    
    # deterrmine figure size
    fig_width_pt = 246.0  # Get this from LaTeX using \showthe\columnwidth
    inches_per_pt = 1.0/72.27               # Convert pt to inch
    golden_mean = (sqrt(5)-1.0)/2.0         # Aesthetic ratio
    fig_width = fig_width_pt*inches_per_pt  # width in inches
    fig_height = fig_width*golden_mean      # height in inches
    pub.setFigure(figsize=[fig_width,fig_height])
    
    # set backend
    pub.setBackend(type='ps')
    
    # setfontlib
    pub.add('fontlib','label',family='century',size=8) 
    pub.add('fontlib','ticklabel',family='century',size=6) 
    pub.add('fontlib','textbox',family='century',size=6)
    
    # setsubplot
    #pub.set('subplot',left=0.18,right=0.9,bottom=0.18,top=0.95)
    pub.set('subplot',left=0.1,right=0.5,bottom=0.2,top=1)

    
    # line for grid
    pub.add('guidelinelib','grid',color='k',linestyle=':',linewidth=0.5)
    
    # line for plots sequence
    pub.load_linelib_bw()
    
    # add axes libs
    pub.load_four_tick()  
    
    
    # load default locator
    pub.load_default_locator()
    
    pub.load_boxlib()
    pub.add('mathtextlib','inuse',)
    
    return pub
    
        
if __name__ == '__main__':
    p1 = publish_style()
    p1.write_default('figurecss.txt')
    print p1

    