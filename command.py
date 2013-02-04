
import sys
import os
import datetime
sys.path.append('../webfe/')
from core.imports.marc.import_marc_dat import importfile_marc_dat
from core.model.registry import model
from core.export.export import exporter
from core.settings import settings
from core.utility.fem.create_arcplane import create_cylinderSurface
from core.procedures.p_poledent import process_pole_dat,PoleModeling, pole_extend, pole_bending_modeling
from core.export.export import exporter
from core.post.import_marc_t16 import post_t16
from core.post.import_plain import import_plain
from core.plots.plots import tpfdb

class commandparser():
    """ This is the wrap class, wrap all model operations and
    provide list input interface as marco framework
    """
    
    def __init__(self):
        self.model = model(settings)
        self.results = tpfdb()
        self.commandhis = []
        self.currentsettings = {}
        self.macro_start = 0
        self.macro_end = 0
    
    def SetModel(self,model):
        self.model = model
    
    def parser(self,inputstr):
        """ Parser the input command """
        
        inputstr = inputstr.strip()
        if len(inputstr) == 0:  # blank line
            return 0
        
        if inputstr[-1] == '\n':
            inputstr = inputstr[:-1]
            
        print inputstr
        inputstrlist = inputstr.split(',')
        
        if inputstrlist[0][0] == '*':
            commandname = inputstrlist[0][1:].strip()
            fun_handle = self.__class__.__dict__[commandname]
            fun_handle(self,*inputstrlist[1:])
            
            self.commandhis.append(inputstr)
            return commandname
        
        elif inputstrlist[0][0] == '#':  # comments
            self.commandhis.append(inputstr)
            return 'Comments'
        else:
            print "command error, not start with '*'"
            return 'Command Syntax Error Occured'
        
        
    
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
        # generate basic modeling
        process_pole_dat(self.model,args[0],args[1])
        
        # add analysis procedures if needed
        if len(args) > 2:
            if args[2] == 'curvature':
                self.model = PoleModeling(self.model)
                
        if len(args) == 6:
            rightxcoord = float(args[3])
            leftxcoord = float(args[4])
            self.model = pole_extend(self.model,"surface_rightend",rightxcoord,float(args[5]))
            self.model = pole_extend(self.model,"surface_leftend",leftxcoord,float(args[5]))

    def procedure_poledent_fourpoint(self,*args):
        leftsupportx,rightsupportx,supporty,leftplatecenterx,rightplatecenterx,plateheighty,lengthx,heighty,stiffness = map(float,args)
        self.model = pole_bending_modeling(self.model,leftsupportx,rightsupportx,supporty,leftplatecenterx,rightplatecenterx,heighty,lengthx,plateheighty,stiffness)
    
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
        
    def import_marc_dat(self,*args):
        # readin the marc dat file
        f1 = importfile_marc_dat(args[0],stylesetting=args[1])
        
        # add nodes to model
        self.model = f1.add_nodes(self.model)
        
        # add elements to model
        self.model = f1.add_elements(self.model)
    
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
    
    def plot_edit_tdb_table_unit(self,*args):
        ''' modify the column unit label for sepcify table and col'''
        tablename = args[0]
        col_id_start,col_id_end = map(int,args[1].split(':'))
        unitlabel = args[2]
        self.results.edit_tdb_unitlabel(tablename,col_id_start,col_id_end,unitlabel)

    def plot_edit_tdb_table_label(self,*args):
        ''' modify the column unit label for sepcify table and col'''
        tablename = args[0]
        columnid = int(args[1])
        updatelabel = args[2]
        self.results.edit_tdb_label(tablename,columnid,updatelabel)
    
    def plot_edit_pdb_units(self,*args):
        pdbkey = args[0]
        self.results.edit_pdb_unit(pdbkey,*args[1:])

    def plot_edit_pdb_labels(self,*args):
        pdbkey = args[0]
        self.results.edit_pdb_label(pdbkey,*args[1:])
        
    def plot_edit_pdb_settings(self,*args):
        pdbkey = args[0]
        self.results.edit_pdb_settings(pdbkey,*args[1:])
        
    def plot_edit_tdb_increment(self,*args):
        ''' get increment for table '''
        
        try:
            newtablekey = str(args[0])
            tablekey = str(args[1])
            incr_start = int(args[2])
            incr_end = int(args[3])
            incr_step = int(args[4])
        except:
            raise ValueError,("input parameter not in format of ('str','int')",'got',map(type,*args))
        
        self.results.tmask_incrment_setresults(newtablekey,tablekey,incr_start,incr_end,incr_step)
        
    def plot_edit_tdb_coordlist(self,*args):
        origntablekey = args[0]
        newtablekey = args[1]
        self.results.tmask_coordlist(self.model,newtablekey,self.results.tdb[origntablekey]['labellist'])
    
    def plot_figure_add(self,*args):
        self.results.add_figure(*self.strfiy(args))
        
    def plot_figure_save(self,*args):
        figurekey = args[0]
        fileformat = args[1]
        plotname = args[2]
        
        self.results.savefig(figurekey,fileformat,name=plotname)
    
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
        
        currentfolder,absfilename = os.path.split(filename)
        self.currentsettings['currentfolder'] = currentfolder
        
        for line in f1.readlines():
            # assign folder path if needed
            if '%' in line:
                line = line % self.currentsettings
            
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