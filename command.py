
import sys
import os
import datetime
sys.path.append('../webfe/')
from core.imports.marc.import_marc_dat import importfile_marc_dat
from core.model.registry import model
from core.export.export import exporter
from core.settings import settings
from core.utility.fem.create_arcplane import create_cylinderSurface
from core.procedures.p_poledent import process_pole_dat,PoleModeling, pole_extend
from core.export.export import exporter
from core.post.import_marc_t16 import post_t16
from core.post.import_plain import import_plain
from core.plots.plots import tpfdb

class commandparser():
    """ This is the wrap class, wrap all model operations and
    provide list input interface as marco framework
    """
    
    def __init__(self):
        self.model = None
        self.results = tpfdb()
        self.commandhis = []
    
    def SetModel(self,model):
        self.model = model
    
    def parser(self,inputstr):
        """ Parser the input command """
        
        inputstr = inputstr.strip()
        if inputstr[-1] == '\n':
            inputstr = inputstr[:-1]
        print inputstr
        inputstrlist = inputstr.split(',')
        
        if inputstrlist[0][0] == '*':
            fun_handle = self.__class__.__dict__[inputstrlist[0][1:].strip()]
            fun_handle(self,*inputstrlist[1:])
            
            self.commandhis.append(inputstr)
            
        elif inputstrlist[0][0] == '#':  # comments
            self.commandhis.append(inputstr)
            
        else:
            print "command error, not start with '*'"
        
    
    
    # functions callable


    def new_project(self,*args):
        settings['prjname'] = args[0]
        settings['ndm'] = args[1]
        settings['ndf'] = args[2]
        settings['root'] = args[3]
        self.model = model(settings)
        
        print "New model created @ %s" % datetime.datetime.now()

    def open_project(self,*args):
        self.model = self.model.modelloadbyfile(args[0])

    def close_project(self,*args):
        self.model = None

    def save_project(self,*args):
        self.model.modelsavetofile(args[0])
  
    def new_node(self,*args):
        self.model.add_node(args)
        
    
    def new_conn(self,*args):
        self.model.add_element(args)
        
    def new_material(self,*args):
        matname = args[0]
        matclass = args[1]
        self.model.material(matname,matclass,args[2:])

    def new_section(self,*args):
        matname = args[0]
        matclass = args[1]
        self.model.section(matname,matclass,args[2:])
        
    
    def create_cylinderSurface(self,*args):
        self.model = create_cylinderSurface(self.model,*args) #x0,y0,z0,r0,r1,L,nfi,nZ)
    
    
    def procedure_poledent(self,*args):
        process_pole_dat(self.model,args[0],args[1])
        
        if len(args) > 2:
            if args[2] == 'True':
                self.model = PoleModeling(self.model)
                
        if len(args) == 6:
            rightxcoord = float(args[4])
            leftxcoord = float(args[5])
            self.model = pole_extend(self.model,"surface_rightend",rightxcoord,10)
            self.model = pole_extend(self.model,"surface_leftend",leftxcoord,10)
            
    def export_model(self,*args):
        fullpath = args[1]
        libtype = args[0]
        exp1 = exporter(self.model,fullpath,'ex_plain')
        #path,filename = os.path.split(fullpath)
        exp1.export_target(libtype,fullpath)
        
    def export_marc_proc(self,*args):
        fullpath = args[0]
        exp1 = exporter(self.model,fullpath,'ex_Marc')
        path,filename = os.path.split(fullpath)
        exp1.export(path)    

    def export_marc_dat(self,*args):
        fullpath = args[0]
        exp1 = exporter(self.model,fullpath,'ex_Marc_dat')
        path,filename = os.path.split(fullpath)
        exp1.export(path)
    
    def export_opensees_tcl(self,*args):
        fullpath = args[0]
        exp1 = exporter(self.model,fullpath,'ex_OpenSees')
        path,filename = os.path.split(fullpath)
        exp1.export(path)
        
    
    def post_new(self,*args):
        self.results = tpfdb()
        
    def post_save(self,*args):
        filename = args[0]
        self.results.save(filename)
        
    def post_load(self,*args):
        filename = args[0]
        newresults = self.results.load(filename)  
        self.results = newresults
    
    def post_plain_new(self,*args):
        self.results.source['plain'] = {'handler':import_plain()}
        
    def post_plain_filelist(self,*args):
        self.results = self.results.source['plain']['handler'].addfilelist(*args,db=self.results)
        
    
    def post_marc_t16_open(self,*args):
        fullpath = args[0]
        self.results.source['marc_t16'] = {'file':fullpath,'handler':post_t16(fullpath),'request':{}}

    def post_marc_t16_addrequest(self,*args):
        
        tablename = args[0]
        command = args[1:]
        
        self.results.source['marc_t16']['request'][tablename] = command
        
    def post_marc_t16_getdata(self):
        self.results.source['marc_t16']['handler'].postset_dict(self.results)
        #try:
        #    self.post_t16.postset_dict(self.results.source['marc_t16']['request'])
        #except:
        #    print 'process t16 request failed'
        
    def plot_pdata_add(self,*args):
        key = args[0]
        parlist = args[1:]
        self.results.add_plotdata_command(key,parlist) #plotkey,tablekey,pairidlist,mode='xy')
    
    def plot_figure_add(self,*args):
        self.results.add_figure(*self.strfiy(args))
    
    def macro_start(self):
        self.macro_start = len(self.commandhis)
        
    def macro_end(self):
        self.macro_end = len(self.commandhis)

    def macro_save(self,filename):
        f1 = open(filename,'w')
        for line in self.commandhis[self.macro_start:self.macro_end+1]:
            f1.write(line)
            f1.write('\n')
        f1.close()

    def macro_load(self,filename):
        f1 = open(filename,'r')
        for line in f1.readlines():
            self.parser(line)

        
    def strfiy(self,slist):
        tlist = []
        for item in slist:
            tlist.append(item)
        return tlist
    
if __name__ == '__main__':
    p1 = commandparser()
    
    str1 = '*new_project myprj 3 6 c:/data'
    p1.parser(str1)
    
    
    str1 = '*new_node 1 2 3'
    p1.parser(str1)
    
    str1 = '*new_node 2 2 3'
    p1.parser(str1)

    str1 = '*new_conn 1 2'
    p1.parser(str1)

    str1 = '*new_material mymat uniaxial_elastic 29000 0.3'
    p1.parser(str1)
    
    print 1