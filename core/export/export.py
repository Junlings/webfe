#!/usr/bin/env python

# here import all export library
import core.meta.meta_export as metacls
import os
from lib_plain import ex_plain
from lib_OpenSees import ex_OpenSees
from lib_ansys import ex_Ansys
from lib_marc import ex_Marc
from lib_marc_dat import ex_Marc_dat

import StringIO
class exporter():
    def __init__(self,model,exportfile,target='ex_plain',path=None):
        self.model = model  # fem model
        self.EXP = {}       # export string dict
        
        self.exportfile = exportfile  # output file
        self.path = path
        
        # link exporter to the instance by the class name
        self.exporter = metacls.metacls_export.class_by_name(target)()
        self.model.settings['expfolder'] = exportfile.split('.')[0]
    
    def write_individual_file(self,exportfilefullpath):
        output = self.exporter.write_individual_file(self.model)
        
        f1 = open(exportfilefullpath,'w')
        f1.write(output)
        f1.close()
        
    
    def write_out(self,exportfolder=None):
        ''' function to write all exports'''
        if self.path == None:
            prjfolder = self.model.settings['prjname']
            if not os.path.isdir(prjfolder):
                os.mkdir(prjfolder)
        else:
            prjfolder = os.path.join(*self.path)
            if not os.path.isdir(prjfolder):
                os.mkdir(prjfolder)            
        
        if exportfolder == None or len(exportfolder)==0:
            exportfolder = prjfolder
        '''
        exportfolder = os.path.join(prjfolder,'export')
        if not os.path.isdir(exportfolder):
            os.mkdir(exportfolder)
        '''
        if not os.path.isdir(exportfolder):
            os.mkdir(exportfolder)
            
        f1 = open(os.path.join(exportfolder,self.exportfile),'w')
        f2 = open(os.path.join(exportfolder,self.exportfile+'.err'),'w')

        #f1 = open(self.exportfile,'w')
        #f2 = open(self.exportfile+'.err','w')
        
        if 'commands' in self.EXP.keys():
            f1.write(self.EXP['commands'].getvalue())
        #try:
        #    f1.write(self.EXP['commends'].getvalue())
        #except:
        #    f2.write('write commends error or empty commends\n')
            
        try:
            f1.write(self.EXP['settings'].getvalue())
        except:
            f2.write('write setting error or empty setting\n')
        
        try:
            f1.write(self.EXP['variables'].getvalue())
        except:
            f2.write('write variable error or empty variable\n')


        try:
            f1.write(self.EXP['tables'].getvalue())
        except:
            f2.write('write table error or empty tables\n')
            
        try:
            f1.write(self.EXP['coord'].getvalue())
        except:
            f2.write('write coordinates error or empty coordinates\n')

        try:
            f1.write(self.EXP['mat'].getvalue())
        except:
            f2.write('write material error or empty material\n')

        try:
            f1.write(self.EXP['orient'].getvalue())
        except:
            f2.write('write orient error or empty orient\n')
            
        try:
            f1.write(self.EXP['sec'].getvalue())
        except:
            f2.write('write section error or empty section\n')        
        
        try:
            f1.write(self.EXP['conn'].getvalue())
        except:
            f2.write('write connectivity error or empty connectivity\n')

            


        try:
            f1.write(self.EXP['setlist'].getvalue())
        except:
            f2.write('write itemset error or empty set\n')
            


        try:
            f1.write(self.EXP['prop'].getvalue())
        except:
            f2.write('write properties error or empty properties\n')
        
        #f1.write(self.EXP['nodaltie'].getvalue())
        try:
            f1.write(self.EXP['nodaltie'].getvalue())
        except:
            f2.write('write nodaltie error or empty nodaltie\n')
            
        try:
            f1.write(self.EXP['bond'].getvalue())
        except:
            f2.write('write bond error or empty bonds\n')

        try:
            f1.write(self.EXP['recorder'].getvalue())
        except:
            f2.write('write recorder error or empty recorder\n')
            
        try:
            f1.write(self.EXP['loadcases'].getvalue())
        except:
            f2.write('write loadcase error or empty loadcases\n')


        try:
            f1.write(self.EXP['jobs'].getvalue())
        except:
            f2.write('write joblist error or empty jobs\n')


      
            
        f1.close()
        f2.close()
        
        #'' additonal files
        
        
        self.write_individual_file(os.path.join(exportfolder,self.exportfile.split('.')[0]+'.dat'))
        
        
                        
    def write_commands(self,command):
        ''' write basic settings'''
        self.EXP['commands'] = StringIO.StringIO()
        self.exporter.ex_commands(self.EXP['commands'],command,self.model)
        
    def write_settings(self):
        ''' write basic settings'''
        self.EXP['settings'] = StringIO.StringIO()
        self.exporter.ex_settings(self.EXP['settings'],self.model.settings)        
    
    def write_variables(self):
        ''' write variables'''
        self.EXP['variables'] = StringIO.StringIO()
        self.exporter.ex_variables(self.EXP['variables'],self.model.matlist)
        self.exporter.ex_variables(self.EXP['variables'],self.model.seclist)
        self.exporter.ex_variables(self.EXP['variables'],self.model.orientlist)
        #self.exporter.ex_variables(self.EXP['variables'],self.model.matlib)
        
    def write_coord(self):
        ''' obtain coordinates export'''
        self.EXP['coord'] = StringIO.StringIO()
        self.exporter.ex_coord(self.EXP['coord'],self.model.nodelist)
        
    def write_conn(self):
        '''obtain elements export'''
        self.EXP['conn'] = StringIO.StringIO()
        self.exporter.ex_conn(self.EXP['conn'],self.model.connlist)

    def write_conn_prop(self):
        '''obtain elements export'''
        self.EXP['conn'] = StringIO.StringIO()
        self.exporter.ex_conn_prop(self.EXP['conn'],self.model.connlist,
                                                    self.model.proplist)
        
    def write_mat(self,key=None,keylist=None):
        '''obtain material export'''
        self.EXP['mat'] = StringIO.StringIO()
        EXP = self.exporter.ex_mat(self.EXP['mat'],self.model.matlist,key,keylist=keylist)
        return EXP.getvalue()

    def write_itemset(self,key=None):
        '''obtain itemset export'''
        self.EXP['setlist'] = StringIO.StringIO()
        EXP = self.exporter.ex_itemset(self.EXP['setlist'],self.model.setlist,key)
        return EXP.getvalue()
        
    def write_sec(self,key=None,mode='yz'):
        '''obtain section export'''
        self.EXP['sec'] = StringIO.StringIO()
        EXP = self.exporter.ex_sec(self.EXP['sec'],self.model.seclist,
                                             self.model.matlist,key,mode=mode)
        return EXP.getvalue()

    def write_orient(self,key=None):
        '''obtain orientation export'''
        self.EXP['orient'] = StringIO.StringIO()
        EXP = self.exporter.ex_orient(self.EXP['orient'],self.model.orientlist,key)
        return EXP.getvalue()
        
    def write_prop(self,key=None):
        '''obtain element property'''
        self.EXP['prop'] = StringIO.StringIO()
        EXP = self.exporter.ex_prop(self.EXP['prop'],self.model.proplist,key)
        return EXP.getvalue()

    def write_recorder(self,key=None):
        '''obtain recorder'''
        self.EXP['recorder'] = StringIO.StringIO()
        EXP = self.exporter.ex_recorder(self.EXP['recorder'],self.model.reclist,key)
        return EXP.getvalue()
        
    def write_bond(self,key=None):
        '''obtain boundary conditions, include fix, load amd disp'''
        self.EXP['bond'] = StringIO.StringIO()
        
        boundary = {}
        boundary.update(self.model.bondlist)
        boundary.update(self.model.loadlist)
        boundary.update(self.model.displist)
        
        EXP = self.exporter.ex_bonds(self.EXP['bond'],boundary,key)
        return EXP.getvalue()

    def write_tables(self,key=None):
        self.EXP['tables'] = StringIO.StringIO()
        try:
            EXP = self.exporter.ex_tables(self.EXP['tables'],self.model.tablelist,key)
            return EXP.getvalue()
        except:
            return ''
        
    def write_nodaltie(self,key=None):
        self.EXP['nodaltie'] = StringIO.StringIO()        
        EXP = self.exporter.ex_nodaltie(self.EXP['nodaltie'],self.model.nodaltielist,key)
        return EXP.getvalue()    
    
    def write_loadcases(self,key=None):
        try:
            self.EXP['loadcases'] = StringIO.StringIO()        
            EXP = self.exporter.ex_loadcases(self.EXP['loadcases'],self.model.loadcaselist,key)
            return EXP.getvalue()
        except:
            return ''
        
    def write_jobs(self,key=None):
        self.EXP['jobs'] = StringIO.StringIO()        
        EXP = self.exporter.ex_jobs(self.EXP['jobs'],self.model.joblist,key)
        return EXP.getvalue()
        
    def export(self,folder=None,matkeylist=None,secmode='yz'):
        self.write_settings()
        self.write_variables()
        self.write_coord()
        self.write_conn_prop()
        self.write_mat(keylist=matkeylist)
        self.write_sec(mode=secmode)
        self.write_itemset()
        self.write_prop()
        self.write_tables()
        self.write_bond()
        self.write_nodaltie()
        self.write_recorder()
        self.write_loadcases()
        self.write_jobs()
        self.write_orient()
        self.write_out(folder)
        
    def export_target(self,target,filename):
        f1 = open(filename,'w')
        
        if target == 'grid':
            self.write_coord()
            try:
                f1.write(self.EXP['coord'].getvalue())
            except:
                f1.write('write coordinates error or empty coordinates\n')
                
        elif target == 'connectivity':
            self.write_conn()
            try:
                f1.write(self.EXP['conn'].getvalue())
            except:
                f1.write('write connectivity error or empty connectivity\n')            
            
        
        f1.close()