""" This is the module """
""" This is the module """
import os.path
from unitsystem import create_units
from plottypes.line import double_axis_line, single_axis_line
import timeit
import numpy as np
from plotsettings import publish_style, testresult_style,default_style,mono_style
from dmask import dmask
from core.lib.libop import loadbyfile, savebyfile

class tpfdb():
    ''' result plot database
        has dictionary structure for
        a) numpy tables include unitlist and label list, column data
        b) plot data settings, include target units and axis labels
        c) figure settings, include the generate figure objects
        d) plot style settings, conbined with plot data , can generate figures plots
    '''
    
    def __init__(self):
        self.pdb = {}  # plot database:  table format
        self.sdb = {'default':default_style(),
                    'test':testresult_style(),
                    'publish':publish_style(),
                    'mono':mono_style()}  # plot style database
        self.mdb = {}  # data column mask lib
        self.fdb = {}  # figure database: figure format
        self.fsdb = {}  # figure database: figure settings format
        self.tdb = {}  # result table database
        self.UI = create_units()
        self.source = {}
    
    def generate_libdict(self):
        resdict = {}
        
        resdict['Source'] = self.source
        resdict['Table'] = self.tdb
        resdict['Mask'] = self.mdb
        resdict['Plot'] = self.pdb
        resdict['Style'] = self.sdb
        resdict['Figure'] = self.fsdb
        
        return resdict
    
    def getcollabes(self,keylist=None):
        collist = []
        if keylist == None:
            keylist = self.tdb.keys()
        
        for key in keylist:# self.tdb.keys():
            if key in self.tdb.keys():
                for label in self.tdb[key]['labellist']:
                    collist.append(key+':'+label)
            else:
                raise KeyError, ('Requested key: ',key,' Do not in the dabase table')
        return collist
            
    
    def add(self,key,array2D,unitlist=None,labellist=None):
        ''' add single table to the tdb'''
        self.tdb[key] = {'data':array2D,'unitlist':unitlist,'labellist':labellist}
        
    
    def add_plotdata_command(self,plotkey,pairidlist):#@,mode='xy'):
        ''' add plot data by refering table name and column labels
            mode can be specified to simplify 
        '''
        keylist = []

        xlabel = pairidlist[0]
        for pairy in pairidlist[1:]:
            keylist.append([xlabel,pairy])
        
        # add default unit x and y using the first item
        xunit = self.get_data(pairidlist[0])[1]
        yunit = self.get_data(pairidlist[1])[1]
        self.add_plotdata(plotkey,keylist,units=[xunit,yunit])
    
    
    def add_plotdata_table(self,plotkey,tablekey,pairidlist,mode='xy',units=None,xylabels=None,scale=None,shift=None,limits=None):
        ''' add plot data by refering table name and column labels
            mode can be specified to simplify 
        '''
        keylist = []
        if mode == 'xy':
            for pairid in pairidlist:
                keylist.append([tablekey+':'+str(pairid[0]),tablekey+':'+str(pairid[1])])
        elif mode == 'xyy':
            xlabel = pairidlist[0]
            for pairy in pairidlist[1]:
                keylist.append([xlabel,tablekey+':'+str(pairy)])

        elif mode == 'xxy':
            ylabel = pairidlist[-1]
            for pairx in pairidlist[:-1]:
                keylist.append([tablekey+':'+str(pairx),ylabel])
   
        else:
            raise KeyError,('mode ',mode, 'do not defined')
                
        
        self.add_plotdata(plotkey,keypairlist,units=units,xylabels=xylabels,limits=limits)
        
        
    def add_plotdata(self,pkey,keypairlist,units=None,xylabels=['x','y'],transform={},masklist=[]):
        ''' specify the data source name with 'table:col' indicate a column in table '''
        if units == None:
            units = ['N/A','N/A']
        
        if xylabels == None:
            xylabels = ['x','y']
        
        if pkey in self.pdb.keys():
            
            self.pdb[pkey]['datalabelpair'].extend(keypairlist)
            '''
            self.pdb[pkey] = {'datalabelpair':self.pdb[pkey]['datalabelpair'].extend(keypairlist),
                              'units':self.pdb[pkey]['units'].extend(units),
                              'xylabels':self.pdb[pkey],#.extend(xylabels),
                              'transform':self.pdb[pkey]['transform'].update(transform),
                              'masklist':self.pdb[pkey]['masklist'].extend(masklist)}
            '''
        else:
            self.pdb[pkey] = {'datalabelpair':keypairlist,
                              'units':units,
                              'xylabels':xylabels,
                              'transform':transform,
                              'masklist':masklist}            
    
    def decorate_plotdata(self,pkey,curvekey,linedata,linelegend=None):
        ''' decorate the pdata to add additional lines for labeling purposes'''
        
        if curvekey not in self.pdb[pkey]['pdatadict'].keys():
            self.pdb[pkey]['pdatadict'][curvekey] = linedata
            if linelegend != None:
                self.pdb[pkey]['plabel'][curvekey] = linelegend
        else:
            raise KeyError,('Plot curve key ', curvekey,' already exist')
    
    def process_plotdata(self,pkey):
        ''' obtain necessary information from plot data'''
        pdatadict = {}
        plabel = {}
        punitlist = []
        icurve = 1
        for key in self.pdb[pkey]['datalabelpair']:
            
            if len(key) == 2:
                # deal with x axis
                datax,unitx = self.retrive_result(pkey,key[0],mode='x',icurve=icurve)
                
                # deal with y axis
                datay,unity = self.retrive_result(pkey,key[1],mode='y',icurve=icurve)
                plabel[icurve] = key[1]
                
            elif len(key) == 1:
                # deal with x axis
                datax,unitx = self.retrive_result(pkey,key[0],mode='index',icurve=icurve)
                
                # deal with y axis
                datay,unity = self.retrive_result(pkey,key[0],mode='y',icurve=icurve)                
                plabel[icurve] = key[0]
                
            
            #apply local mask apply on the curve
            elif len(key) == 3: # the third one will be mask list separate by |
                datax,unitx = self.retrive_result(pkey,key[0],mode='x',icurve=icurve)
                
                # deal with y axis
                datay,unity = self.retrive_result(pkey,key[1],mode='y',icurve=icurve)
                
                masklist = key[2].split('|')
                for maskkey in masklist:
                    datax,datay = self.mdb[maskkey].coop(datax,datay)
                    plabel[icurve] = key[2]                    
                    
            else:
                raise KeyError, ('Key list number not recognized')
            
            # apply global mask apply on the plot
            if self.pdb[pkey]['masklist'] != None:
                for key in self.pdb[pkey]['masklist']:
                    datax,datay = self.mdb[key].coop(datax,datay)
                
            
            pdataxy = np.vstack([datax,datay]).T       
            pdatadict[icurve] = pdataxy
            
            icurve += 1
            punitlist.extend([unitx,unity])
            
        #self.pdb[pkey]['pdata'] = pdatadict
        self.pdb[pkey]['pdatadict'] = pdatadict
        self.pdb[pkey]['plabel'] = plabel
        self.pdb[pkey]['punits'] = punitlist
    
    
    def get_data(self,dkey):    
        tablekey,columnid =dkey .split(':')
        if type(columnid) != int:
            columnid = self.tdb[tablekey]['labellist'].index(columnid)          
        
        sourcedata = self.tdb[tablekey]['data'][:,columnid]
        sourceunit = self.tdb[tablekey]['unitlist'][columnid]
            
        return sourcedata,sourceunit
     

    def curve_search(self,cxtag,cytag,vcoltag, vvalue,mode='>'):
        ''' serach the corresponging value in cx and cy respect yo vvaue in vcol'''
    
        cx = self.get_data(cxtag)[0]
        cy = self.get_data(cytag)[0]
        vcol = self.get_data(vcoltag)[0]
        
        
        if mode == '>':
            try:
                ind = np.where( vcol > vvalue)[0][0]
                
            except:
                ind = None
        elif mode == '>=':
            ind = np.where( vcol >= vvalue)[0][0]
        
        elif mode == '<':
            try:
                ind = np.where( vcol < vvalue)[0][0]
            except:
                ind = None
        elif mode == '<=':
            ind = np.where( vcol <= vvalue)[0][0]
    
        elif mode == '!=':
            ind = np.where( vcol != vvalue)[0][0]
        
        else:
            raise TypeError,('mode ',mode, 'Do not predefined')
        
        if ind != None:
            return float(cx[ind]),float(cy[ind]),ind
        else:
            return None,None,None
    
    def retrive_result(self,pkey,dkey,mode='x',icurve=0):
        ''' retrive results from table '''
        # locate record in table
        key_b = dkey
        masklist = key_b.split('|')
        
        key_tag = masklist[0]
        masklist = masklist[1:]
        
        tablekey,columnid =key_tag.split(':')
        
        
        if type(columnid) != int:
            columnid = str(columnid)
            tablekey = str(tablekey)
            columnid = self.tdb[tablekey]['labellist'].index(columnid)        
        
        
        # retract unit target
        if self.pdb[pkey]['units'] == None:
            targetunit = 'N/A'
        else:
            
            if mode == 'x':
                targetunit = self.pdb[pkey]['units'][0]
            elif mode == 'index':
                targetunit = self.pdb[pkey]['units'][0]
            else:
                targetunit = self.pdb[pkey]['units'][1]
        
       
       # do unit convert
        if tablekey in self.tdb.keys():  # defined in table
            
            sourcedata = self.tdb[tablekey]['data'][:,columnid]
            sourceunit = self.tdb[tablekey]['unitlist'][columnid]
            
            [uscale,ushift] = self.UI.convert(sourceunit,targetunit)
            if not (uscale == 1 and ushift == 0):
                sourcedata =   np.float64(uscale) * sourcedata  + ushift
                
        # do transformation if needed
        
        if icurve != 0 and self.pdb[pkey]['transform'] != None:
            if icurve in self.pdb[pkey]['transform'].keys():
                if mode in self.pdb[pkey]['transform'][icurve].keys():
                    tscale,tshift = self.pdb[pkey]['transform'][icurve][mode]
                    sourcedata = np.float(tscale) * sourcedata  + tshift
        
        
        
        # apply the masks
        for key in masklist:
            sourcedata = self.mdb[key].oper(sourcedata)
        
        
        # change data to index
        
        if mode == 'index':
            sourcedata = range(1,len(sourcedata)+1)
            targetunit = 'N/A'
        return sourcedata,targetunit
    
    
    def add_dmask(self,key,paralib):
        self.mdb[key] = dmask(key,paralib)
        
    # the following are the drawing style functions
    def add_style(stylekey):
        self.sdb[stylekey] = self.sdb['default']  # copy default
    
    # ================== the modification functions API for GUI functions ===
    
    
    def edit_unitlabel(self,tablename,col_id_start,col_id_end,unitlabel):
        self.tdb[tablename]['unitlist'][col_id_start:col_id_end+1] = unitlabel
        
    # ===================following are drawing functions
    
    def add_figure(self,fskey,pkey,skey,ftype):
        self.fsdb[fskey] = {'fskey':fskey,'pkey':pkey,'skey':skey,'ftype':ftype}
        
    
    def figurerealize(self,fskey):
        fssetting = self.fsdb[fskey]
        ftype = fssetting['ftype']
        
        
        if ftype == 'line-one axis':
            fig = self.line(fskey,pkey=fssetting['pkey'],skey=fssetting['skey'],mode='single',legend=True)
        else:
            print 'figure type ',tkey,' do not defined'
            
        return fig.figure
    
    def line(self,fkey,pkey=None,skey='default',mode='single',legend=True):
        if pkey == None:
            pkey = fkey
        
        if 'pdatadict' not in self.pdb[pkey].keys():
            self.process_plotdata(pkey)
        plotdata = self.pdb[pkey]['pdatadict']
        units = self.pdb[pkey]['units']
        xylabels = self.pdb[pkey]['xylabels']
        datalabel = self.pdb[pkey]['plabel']
        #limits = self.pdb[pkey]['limits']
        
        if mode == 'single':
            fig = single_axis_line(plotdata,units,xylabels,datalabel,style=self.sdb[skey],legend=legend)
            
        elif mode == 'double':
            fig = double_axis_line(plotdata,units,xylabels,datalabel,style=self.sdb[skey])
    
        self.fdb[fkey] = fig
        
        return fig
    
    
    # =======================the following are save function groups
    def saveallfig(self,format,dpi=300,path=None):
        ''' save all figures in database '''
        for fkey in self.fdb.keys():
            
            name = fkey+'.'+format
            if path != None:
                resfolder = os.path.join(*path)
                if not os.path.isdir(resfolder):
                    os.mkdir(resfolder)
                name = os.path.join(resfolder,name)
            
            self.savefig(fkey,format,name=name,dpi=dpi)
    
    def savefig(self,fkey,format,name=None,dpi=300,path=None):
        ''' save single figure in database'''
        if name == None:
            name = fkey+'.'+format
            
        if path != None:
            resfolder = os.path.join(*path)
            if not os.path.isdir(resfolder):
                os.mkdir(resfolder)
            name = os.path.join(resfolder,name)
        self.fdb[fkey].figure.savefig(name,format=format,dpi=dpi)
    
    
    def saveallpdata(self,path=None,delimiter='\t'):
        ''' save all plot data'''
        for pkey in self.pdb.keys():
            self.savepdata(pkey,path=path,delimiter=delimiter)
    
    def savepdata(self,pkey,path=None,delimiter='\t'):
        ''' save single plot data'''
        pdata = self.pdb[pkey]['pdatadict']
        
        if delimiter == '\t':
            extension = '.txt'
        elif delimiter == ',':
            extension = '.csv'
        else:
            extension = '.out'
        
        name = pkey + extension
        
        if path != None:
            resfolder = os.path.join(*path)
            if not os.path.isdir(resfolder):
                os.mkdir(resfolder)
            filename = os.path.join(resfolder,name)
        
        basename = filename.split('.')[0]
        for keys in pdata.keys():
            newfilename = basename + '_' + str(keys) + '.txt'
            f1 = open(newfilename,'w')
            labels = delimiter.join(self.pdb[pkey]['plabel']) + '\n'
            f1.write(labels)
    
            units = delimiter.join(self.pdb[pkey]['punits']) + '\n'
            f1.write(units)

        
            np.savetxt(f1,pdata[keys],delimiter=delimiter)
        f1.close()
    
    
    def savetable(self,tkey,path=None,delimiter='\t'):
        ''' save single table'''
        if delimiter == '\t':
            extension = '.txt'
        elif delimiter == ',':
            extension = '.csv'
        else:
            extension = '.out'
        
        name = tkey + extension
        
        if path != None:
            resfolder = os.path.join(*path)
            if not os.path.isdir(resfolder):
                os.mkdir(resfolder)
            filename = os.path.join(resfolder,name)        
        f1 = open(filename,'w')
        labels = delimiter.join(self.tdb[tkey]['labellist']) + '\n'
        f1.write(labels)

        units = delimiter.join(self.tdb[tkey]['unitlist']) + '\n'
        f1.write(units)

        
        np.savetxt(f1,self.tdb[tkey]['data'],delimiter=delimiter)
        f1.close()
    
    def save(self,filename):
        
        self.fdb = {}
        for key in self.source.keys():
            self.source[key]['handler'] = None
        savebyfile(self,filename)
        return 1        
        
        
    def load(self,filename):
        results = loadbyfile(filename)
        return results

if __name__ == '__main__':
    t1 = timeit.timeit()
    import numpy as np
    t2 = timeit.timeit()
    rp = tpfdb()
    t3 = timeit.timeit()
    rp.add('da',np.array([[-1,-0.1,0,6,7,8,8]]).T,unitlist=['m'],labellist=['dx'])
    rp.add('db',np.array([[5,6,8,6,7,8,8],[1,2,3,5,6,1,7]]).T,unitlist=['m','m'],labellist=['dx','dy'])
    
    rp.add_dmask('shiftx',{'oper':'Shift','scalar':10})
    rp.add_dmask('flip',{'oper':'FlipSign'})
    rp.add_dmask('cutstart1',{'oper':'CutNegative','nodenum':2})
    
    rp.add_plotdata('plot1',[['da:dx','db:dx','cutstart1'],['da:dx','db:dy']],units=['m','m'],xylabels=['x','y'],masklist=None)
    #rp.add_plotdata('plot2',[['da:dx','db:dx'],['da:dx','db:dy']],units=['m','m','in.','in.'],xylabels=['x1','y1','x2','y2'],transform={1:{'x':[2,-10]}})
    rp.add_plotdata('plot2',[['da:dx','db:dx'],['da:dx','db:dy']],units=['m','m'],xylabels=['x','y'],masklist=None)
    
   
    rp.line('plot1','plot1',skey='publish')
    rp.line('plot2','plot2',skey='publish')
    
    rp.savefig('plot1','jpg')
    rp.savefig('plot2','jpg')
    #r#p.save('plot2','eps')
    #rp.savepdata('plot1')
    t4 = timeit.timeit()
    print t2-t1,t3-t2,t4-t3
    
    rp.save('tt.res')
    print 1
    
    