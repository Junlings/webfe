#!/usr/bin/env python
""" This is the module support the plot function
    including the table management
    plotdata management
    figure management
"""
import os.path

# create default unit system predefined
from unitsystem import create_units

# Import the plot style from inividual files
from plottypes.line import double_axis_line, single_axis_line

# Import predefined plot styles
from plotsettings import publish_style, testresult_style,default_style,mono_style

# Import data mask for data manipulation
from dmask import dmask, create_default

import timeit
import numpy as np

from core.lib.libop import loadbyfile, savebyfile

class icurve():
    def __init__(self,ind,inputdict={}):
        self.ind = ind
        self.xtablekey = ''
        self.xcolumnid = ''
        self.xcolumnname = ''
        self.xmasklist = []
        self.xdata = None
        self.xunit = ''
        
        self.ytablekey = ''
        self.ycolumnid = ''
        self.ycolumnname = ''
        self.ymasklist = []
        self.ydata = None
        self.yunit = ''
        
        self.xymasklist = []
        self.legend = ''
        #self.showlegend = True
        #self.legendstyle = None

        
        for key in inputdict.keys():
            if key in self.__dict__.keys():
                self.__dict__[key] = inputdict[key]

    def retrive(self,targetunits,results):
        ''' retrive results from table
            pkey: plotdata key
            dkey: in format of tablename:columnid|mask1|mask2|mask3|
        
        '''
        # locate record in table

        xunit = targetunits[0]
        yunit = targetunits[1]
        self.xdata,self.xunit = results.retrive(self.xtablekey,self.xcolumnid,xunit)
        self.ydata,self.yunit = results.retrive(self.ytablekey,self.ycolumnid,yunit) 
    
    def xapply(self,results):
        for maskkey in self.xmasklist:
            self.xdata = results.mdb[maskkey].apply(self.xdata)
           
    def yapply(self,results):
        for maskkey in self.ymasklist:
            self.ydata = results.mdb[maskkey].apply(self.ydata)

    def xyapply(self,results):
        for maskkey in self.xymasklist:
            self.xdata,self.ydata = results.mdb[maskkey].apply(self.xdata,self.ydata)
            
    def process(self,targetunits,results):
        # retrive results from tables
        self.retrive(targetunits,results)
        # apply xmask
        self.xapply(results)
        # apply ymask
        self.yapply(results)
        # apply xymask
        self.xyapply(results)
        
    
class plotdata():
    def __init__(self,inputdict={}):
        self.curvelib = {}
        self.curvekeylist = []
        self.unit = ['N/A','N/A','N/A','N/A']
        self.label = ['x1','y1','x2','y2']
        self.type = None
        self.style = None
        
        # add axis control variable
        self.minlimits = ['auto','auto','auto','auto']
        self.maxlimits = ['auto','auto','auto','auto'] 
        # update parameters based on the input dictionary
        for key in inputdict.keys():
            if key in self.__dict__.keys():
                self.__dict__[key] = inputdict[key]    
    
    def add_curve(self,icurve):
        if icurve.ind == -1:
            if len(self.curvekeylist) == 0:
                icurve.ind = 1
            else:
                icurve.ind = max(self.curvekeylist)+1
            self.add_curve(icurve)
        else:
            if icurve.ind not in self.curvelib:
                self.curvelib[icurve.ind] = icurve
                self.curvekeylist.append(icurve.ind)
            else:
                icurve.ind = -1
                self.add_curve(icurve)
    
    def generate_libdict(self):
        
        temp = {'curves':self.curvelib,
                'unit':self.unit,
                'label':self.label,
                'type':self.type,
                'style':self.style}
        return temp
                
    def process(self,results,selcurvelist = None):
        if selcurvelist == None:
            selcurvelist = self.curvekeylist
            
        
        for curvekey in self.curvekeylist:
            # retrive column data
            if curvekey in selcurvelist:
                self.curvelib[curvekey].process(self.unit,results)
        
        
        
        
    def edit_unit(self,unit_x1,unit_y1,unit_x2,unit_y2):
        self.unit = [unit_x1,unit_y1,unit_x2,unit_y2]

    def edit_label(self,label_x1,label_y1,label_x2,label_y2):
        self.label = [label_x1,label_y1,label_x2,label_y2]
        
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
        self.mdb = create_default()  # data column mask lib
        self.fdb = {}  # figure database: figure format
        #self.fsdb = {}  # figure database: figure settings format
        self.tdb = {}  # result table database
        self.UI = create_units()
        self.source = {}
    
    def generate_libdict(self):
        ''' define the database '''
        resdict = {}
        
        resdict['Source'] = self.source   # for data source control, imports
        resdict['Table'] = self.tdb       # result table database
        resdict['Mask'] = self.mdb        # mask database
        
        resdict['Style'] = self.sdb       # plot style database
        resdict['Figure'] = self.fdb     # plot figure database
        resdict['Plot'] = {}
        
        for key in self.pdb:
            resdict['Plot'][key] = self.pdb[key].generate_libdict()       # plotata database
        
        return resdict
    
    def get_tdbkeys(self):
        return list(self.tdb.keys())
    
    def get_tdblabelkeys(self,tablekey):
        return self.tdb[tablekey]['labellist']
    
    def sparse_keystr(self,inputstr):
        masklist = []
        
        if ':' in inputstr:
            tablename,columnname = inputstr.split(':')[0:2]
            
            # sparser out the mask list
            if '|' in columnname:
                temp = columnname.split('|')
                columnname = temp[0]
                masklist = temp[1:]
            
            #columnid = self.get_table_column_id_by_label(tablename,columnname)
            try:
                #columnname = self.get_table_column_label_by_id(tablename,columnname)
                columnid = self.get_table_column_id_by_label(tablename,columnname)
            
            except:
                #columnid = self.get_table_column_id_by_label(tablename,columnname)
                try:
                    columnid = int(columnname)
                except:
                    raise Error,("table column do not found for input str",inputstr)
            
            return tablename,columnid,masklist
        else:
            raise TypeError,('error table:column|mask input string:',inputstr)
    
    
    def get_table_column_label_by_id(self,tablekey,columnid):
        ''' input columnid to get column name '''
        if tablekey in self.tdb.keys():
            
            if type(columnid) != type(int(1)):
                try:
                    return self.get_table_column_label_by_id(self,tablekey,int(columnid))
                except:
                    raise TypeError,('Input columnid shall be type int, got',type(columnid))
            else:
                if len(self.tdb[tablekey]['labellist']) < columnid:
                    raise ValueError,('request column id:',columnid,'larger than the maximum length of table: ',tablekey,' of ',len(self.tdb[tablekey]['labellist']))
                else:
                    return self.tdb[tablekey]['labellist'][columnid]
        else:
            raise KeyError,('Table:', tablekey,' do not exist')
        
        
    def get_table_column_id_by_label(self,tablekey,columnname):
        ''' input columnid to get column name '''
        if tablekey in self.tdb.keys():
            
            if type(columnname) != type(''):
                raise TypeError,('Input columnname shall be type str, got',type(columnname))
            else:
                if columnname not in self.tdb[tablekey]['labellist']:
                    raise ValueError,('request column name: ',columnname,'not found in: ',tablekey)
                else:
                    return self.tdb[tablekey]['labellist'].index(columnname)
        else:
            raise KeyError,('Table:', tablekey,' do not exist')

    def get_table_column_unit_by_label(self,tablekey,columnname):
        ''' input columnid to get column name '''
        if tablekey in self.tdb.keys():
            
            if type(columnname) != type(''):
                raise TypeError,('Input columnname shall be type str, got',type(columnname))
            else:
                if columnname not in self.tdb[tablekey]['labellist']:
                    raise ValueError,('request column name: ',columnname,'not found in: ',tablekey)
                else:
                    return self.tdb[tablekey]['unitlist'].index(columnname)
        else:
            raise KeyError,('Table:', tablekey,' do not exist')
        
    def get_table_column_unit_by_id(self,tablekey,columnid):
        ''' input columnid to get column name '''
        if tablekey in self.tdb.keys():
            
            if type(columnid) != type(int(1)):
                try:
                    return self.get_table_column_unit_by_id(self,tablekey,int(columnid))
                except:
                    raise TypeError,('Input columnid shall be type int, got',type(columnid))
            else:
                if len(self.tdb[tablekey]['labellist']) < columnid:
                    raise ValueError,('request column id:',columnid,'larger than the maximum length of table: ',tablekey,' of ',len(self.tdb[tablekey]['labellist']))
                else:
                    return self.tdb[tablekey]['unitlist'][columnid]
        else:
            raise KeyError,('Table:', tablekey,' do not exist')
    
    def get_table_column_size_by_label(self,tablekey,columnlabel):
        ''' input columnid to get column name '''
        if tablekey in self.tdb.keys():
            columnid = self.get_table_column_id_by_label(tablekey,columnlabel)
            
            pdata,punit = self.retrive(tablekey,columnid)
            return len(pdata)
    

    
    def add_plotdata_command(self,plotkey,pairidlist): # default mode 'xyy'):
        ''' add plot data by refering table name and column labels
            mode can be specified to simplify 
        '''
        if plotkey not in self.pdb.keys():  # new plot data
            p1 = plotdata()
        else:
            p1 = self.pdb[plotkey]
            
        xtablename,xcolumnid,xmasklist = self.sparse_keystr(pairidlist[0])
        xunit = self.get_table_column_unit_by_id(xtablename,xcolumnid)
        
        for pairy in pairidlist[1:]:
            ytablename,ycolumnid,ymasklist = self.sparse_keystr(pairy)
            yunit = self.get_table_column_unit_by_id(ytablename,ycolumnid)
            
            icurveins = icurve(-1,inputdict={
                         'xtablekey' : xtablename,
                         'xcolumnid' : xcolumnid,
                         'xmasklist' : xmasklist,
                         'xcolumnname': self.get_table_column_label_by_id(xtablename,xcolumnid),
                         'ytablekey' : ytablename,
                         'ycolumnid' : ycolumnid,
                         'ycolumnname': self.get_table_column_label_by_id(ytablename,ycolumnid),
                         'ymasklist' : ymasklist,
                         'legend'    : self.get_table_column_label_by_id(ytablename,ycolumnid),
                         'xunit'     : xunit,
                         'yunit'     : yunit,
                                    })
            p1.add_curve(icurveins)
        
        p1.unit = [p1.curvelib[p1.curvekeylist[0]].xunit,
                   p1.curvelib[p1.curvekeylist[0]].yunit,'N/A','N/A']
        self.pdb[plotkey] = p1
    
    
    def append_plotdata_mask(self,plotkey,masktype,maskkey,icurvekey=-1):
        ''' add mask to individual curve '''
        if icurvekey == -1:  # apply mask to all sub icurves
            maskcurvelist = self.pdb[plotkey].curvekeylist
        
        for key in self.pdb[plotkey].curvekeylist:
            if key in maskcurvelist:
                if masktype == 'xy':
                    self.pdb[plotkey].curvelib[key].xymasklist.append(maskkey)
                elif masktype == 'x':
                    self.pdb[plotkey].curvelib[key].xmasklist.append(maskkey)
                elif masktype == 'y':
                    self.pdb[plotkey].curvelib[key].ymasklist.append(maskkey)
                else:
                    raise TypeError,('mask type:',masktype,' do not defined, options are "x","y", or "xy"')
        

    def add_plotdata(self,plotkey,pairidlist,xymasklist=[]): # default mode 'xyy'):
        ''' add plot data by refering table name and column labels
            mode can be specified to simplify 
        '''
        
        p1 = plotdata()
        
        xtablename,xcolumnid,xmasklist = self.sparse_keystr(pairidlist[0])
        xunit = self.get_table_column_unit_by_id(xtablename,xcolumnid)
        

        ytablename,ycolumnid,ymasklist = self.sparse_keystr(pairidlist[1])
        yunit = self.get_table_column_unit_by_id(ytablename,ycolumnid)
            
        icurveins = icurve(-1,inputdict={
                     'xtablekey' : xtablename,
                     'xcolumnid' : xcolumnid,
                     'xmasklist' : xmasklist,
                     'ytablekey' : ytablename,
                     'ycolumnid' : ycolumnid,
                     'ymasklist' : ymasklist,
                     'legend'    : self.get_table_column_label_by_id(ytablename,ycolumnid),
                     'xunit'     : xunit,
                     'yunit'     : yunit,
                     'xymasklist': xymasklist,
                                })
        p1.add_curve(icurveins)
        
        p1.unit = [p1.curvelib[p1.curvekeylist[0]].xunit,
                   p1.curvelib[p1.curvekeylist[0]].yunit,'N/A','N/A']
        self.pdb[plotkey] = p1
    
    
    def process(self,pkey):
        self.pdb[pkey].process(self)
        

    def add(self,key,array2D,unitlist=None,labellist=None):
        ''' add single table to the tdb'''
        #if array2D.dtype != np.float32:
        #    array2D.dtype = np.float32
        self.tdb[key] = {'data':array2D,'unitlist':unitlist,'labellist':labellist}
        
 
    def add_dmask(self,key,paralib):
        ''' add mask to mask list '''
        self.mdb[key] = dmask(key,paralib)
        
    # the following are the drawing style functions
    def add_style(stylekey):
        ''' add mask to mask list '''
        self.sdb[stylekey] = self.sdb['default']  # copy default
        
        

    def getcollabes(self,keylist=None):
        ''' Get Column label of the table give tablekey '''
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
    
    
    
    def row_to_column(self,tablekey,rowid_start,rowid_end,rowid_step,seqtablekey=None):
        ''' get the row vector from table with targeted unit
            if the seqtablekey is not blank, the the rowid start,end,and step will be quantity searching
        '''

        if tablekey in self.tdb.keys():  # defined in table
            if seqtablekey == None:
                rowid_start,rowid_end,rowid_step =map(int,[rowid_start,rowid_end,rowid_step])
                
                if rowid_start == -1:
                    rowid_start = 0
                
                if rowid_end == -1:
                    rowid_end = self.tdb[tablekey]['data'].shape[0]
                
                req_rows = range(rowid_start,rowid_end,rowid_step)
            
            else:
                rowid_start,rowid_end,rowid_step =map(float,[rowid_start,rowid_end,rowid_step])
                req_rows = self.raw_retrive_colrow_range(seqtablekey,rowid_start,rowid_end,rowid_step)
            
            row_data = self.tdb[tablekey]['data'][req_rows,:].T   # transpose
            row_label = map(str,req_rows)
            
            row_unit = ['N/A'] * len(req_rows)
            
  
            return row_label,row_unit,row_data
        else:
            raise TypeError,('Table name:',tablekey, 'not existed, row-to-column operation aborted')
        
    def raw_retrive(self,inputstr):
        tablekey,columnid,masklist = self.sparse_keystr(inputstr)
        sourcedata,sourceunit = self.retrive(tablekey,columnid)
        
        return tablekey,columnid,masklist,sourcedata,sourceunit
    
    def raw_retrive_colrow(self,inputstr):
        ''' strict input of $table:columnlabel:rowid:unitlabel'''
        
        tablekey,columnlabel,rowid,targetunit = inputstr[1:].split(':')
        columnid = self.get_table_column_id_by_label(tablekey,columnlabel)
        sourcedata,sourceunit = self.retrive(tablekey,columnid,targetunit=targetunit)

        
        return sourcedata[int(rowid)],sourceunit
    
    def raw_retrive_colrow_range(self,inputstr,start,end,step):
        ''' strict input of $table:columnlabel'''
        tablekey,columnlabel,targetunit = inputstr.split(':')
        columnid = self.get_table_column_id_by_label(tablekey,columnlabel)
        sourcedata,sourceunit = self.retrive(tablekey,columnid,targetunit=targetunit)
        ind_i = []
        
        n_step = int(abs(end-start)/step)
        for i in range(0,n_step):
            value = start + i*step
            if value > np.max(sourcedata):
                ind_i.append(sourcedata.shape[0])
                ind_i.append(ind)
                break

            ind = np.min(np.nonzero(sourcedata > value)[0])
            ind_i.append(ind)
        
        ind_i = list(set(ind_i))
        ind_i.sort()
        return ind_i
        
        
        
        
    def retrive(self,tablekey,columnid,targetunit=None):
        ''' strict parameter inputs'''
 
       # do unit convert
        if tablekey in self.tdb.keys():  # defined in table
            
            sourcedata = self.tdb[tablekey]['data'][:,columnid]
            sourceunit = self.tdb[tablekey]['unitlist'][columnid]
            
            if targetunit != None:
                try:
                    [uscale,ushift] = self.UI.convert(str(sourceunit),str(targetunit))
                except:
                    raise ValueError,('unit conversion for table:',tablekey,' Column:',columnid,' Column name:', self.get_table_column_label_by_id(tablekey,columnid),
                                      'failed','Source unit:',sourceunit,'Target unit',targetunit)
            
                if not (uscale == 1 and ushift == 0):
                    sourcedata =   uscale * sourcedata  + ushift            
        
        return sourcedata,sourceunit
    
    
    def replace(self,tablekey,columnlabel,sourcedata,sourceunit=None,sourcelabel=None):
        if tablekey not in self.tdb.keys():  # defined in table
            raise TypeError,('Table name:',tablekey, 'not existed, replace operation aborted')
        else:
            columnid = self.get_table_column_id_by_label(tablekey,columnlabel)
            origindata,originalunit = self.retrive(tablekey,columnid)
            
            if origindata.shape != sourcedata.shape:
                raise TypeError,('Source data length',sourcedata.shape,' not the same as origin',origindata.shape)
            else:
                columnid = self.get_table_column_id_by_label(tablekey,columnlabel)
                self.tdb[tablekey]['data'][:,columnid] = sourcedata
                
                if sourceunit != None:
                    self.tdb[tablekey]['unitlist'][columnid] = sourceunit
                
                if sourcelabel != None:
                    self.tdb[tablekey]['labellist'][columnid] = sourcelabel
            
            
    def insert(self,tablekey,columnlabel,sourcedata,sourceunit,sourcelabel,mode='after'):
        
        if tablekey in self.tdb.keys():  # defined in table
            columnid = self.get_table_column_id_by_label(tablekey,columnlabel)
            
            
            self.tdb[tablekey]['data'] = np.insert(self.tdb[tablekey]['data'],columnid+1,sourcedata,axis=1)
            self.tdb[tablekey]['unitlist'].insert(columnid, sourceunit)
            self.tdb[tablekey]['labellist'].insert(columnid, sourcelabel)
            
        else:
            raise TypeError,('Table name:',tablekey, 'not existed, insert operation aborted')
            
    def append(self,tablekey,sourcedata,sourceunit,sourcelabel):
        
        if tablekey in self.tdb.keys():  # defined in table
            columnlabel = self.tdb[tablekey]['labellist'][-1]
            self.insert(tablekey,columnlabel,sourcedata,sourceunit,sourcelabel)
        else:
            raise TypeError,('Table name:',tablekey, 'not existed, insert operation aborted')
        
        
    
    def new_or_replace(self,tablekey,columnlabel,sourcedata,sourceunit=None,sourcelabel=None):
        if tablekey in self.tdb.keys():  # defined in table
            self.replace(tablekey,columnlabel,sourcedata,sourceunit=sourceunit,sourcelabel=sourcelabel)
        # new table
        else:
            self.tdb[tablekey] = {'data':sourcedata,'unitlist':'N/A','labellist':['Col0']}

            if sourceunit != None:
                self.tdb[tablekey]['unitlist'] = [sourceunit]
            
            if sourcelabel != None:
                self.tdb[tablekey]['labellist'] = [sourcelabel]
                
    def tmask_select_row(self,tablekey,rowid,targettablekey,targetcolumnid):
        ''' select the rowid of tablekey and add to targettablekey at columnid '''
    
        slabel,sunit,sdata = self.row_to_column(tablekey,rowid,rowid+1)
        
        self.new_or_replace(targettablekey,targetcolumnid,sdata,sourceunit=sunit[0],sourcelabel=slabel[0])
        
        return 
    
    
    def tmask_incrment_setresults(self,targettablekey,tablekey,incr_start,incr_end,incr_step,seqtablekey=None):
        ''' collect certain increment results from the whole table '''
        if tablekey in self.tdb.keys():
            
            slabel,sunit,sdata = self.row_to_column(tablekey,incr_start,incr_end,incr_step,seqtablekey=seqtablekey)
        
            #targettablekey = tablekey + '_'.join([str(incr_start),str(incr_end),str(incr_step)])
            self.add(targettablekey,sdata,sunit,slabel)
        else:
            raise TypeError,('Table name:',tablekey, 'not existed, increment operation aborted')
    
    
    def tmask_coordlist(self,model1,tablekey,labellist):
        ''' input labellist get location information '''
        res = []
        
        for label in labellist:
            ltype,lcontent,options = self.parses_label(label)
            #print ltype,lcontent,options
            if ltype == 'Elem':
                if options[0] in map(str,range(0,20)): # for certain node
                    nodeseq = model1.connlist.itemlib[int(lcontent)].nodelist[int(options[0])]
                    node = model1.nodelist.itemlib[nodeseq]
                    res.append(node.xyz)
                else:        # 
                    nodeseq = model1.connlist.itemlib[int(lcontent)].nodelist[0]  # use first integration points, may need modification in the future
                    node = model1.nodelist.itemlib[nodeseq]
                    res.append(node.xyz)
                    
            elif ltype == 'Node':
                node = model1.nodelist.itemlib[int(lcontent)]
                res.append(node.xyz)                
                
                
                
                
            else:
                raise TypeError,('Item request:',ltype,'not defined')
                
        self.add(tablekey,np.array(res),labellist=['Coord X','Coord Y','Coord Z'],unitlist = ['in.','in.','in.'])
        #return res
        
        
        
    def parses_label(self,inputstr):
        
        ltype,lcontent = inputstr.split('_')
        options = []
        if '-' in lcontent:
            temp = lcontent.split('-')
            
            lcontent = temp[0]
            options = temp[1:]
        
        return ltype,lcontent,options
        
        
        
        
    
    """
    
    
    def add_plotdata_table(self,plotkey,tablekey,pairidlist,mode='xy',units=None,xylabels=None,scale=None,shift=None,limits=None):
        ''' add plot data by refering table name and column labels
            mode can be specified to simplify 
        '''
        keylist = []
        if mode == 'xy':  # single pair [x,y]
            for pairid in pairidlist:
                keylist.append([tablekey+':'+str(pairid[0]),tablekey+':'+str(pairid[1])])
        
        elif mode == 'xyy':  # multiple pair [x,y1,y2,...yn]
            xlabel = pairidlist[0]
            for pairy in pairidlist[1]:
                keylist.append([xlabel,tablekey+':'+str(pairy)])

        elif mode == 'xxy': # multiple pair [x1,x2,x3,...,xn,y]
            ylabel = pairidlist[-1]
            for pairx in pairidlist[:-1]:
                keylist.append([tablekey+':'+str(pairx),ylabel])
   
        else:
            raise KeyError,('mode ',mode, 'do not defined')
                
        
        self.add_plotdata(plotkey,keypairlist,units=units,xylabels=xylabels,limits=limits)
        
        

    
    
    
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
            if len(key) == 2:  # normal [x,y] data pair
                # deal with x axis
                datax,unitx = self.retrive_result(pkey,key[0],mode='x',icurve=icurve)
                
                # deal with y axis
                datay,unity = self.retrive_result(pkey,key[1],mode='y',icurve=icurve)
                plabel[icurve] = key[1]
                
            elif len(key) == 1: # single [x] with index as x axis
                # deal with x axis
                datax,unitx = self.retrive_result(pkey,key[0],mode='index',icurve=icurve)
                
                # deal with y axis
                datay,unity = self.retrive_result(pkey,key[0],mode='y',icurve=icurve)                
                plabel[icurve] = key[0]
                
            
            #apply local mask apply on the curve
            elif len(key) == 3: # the third one will be mask list separate on both axis
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
            
            icurve += 1  # increment curve index
            punitlist.extend([unitx,unity])
            
        #self.pdb[pkey]['pdata'] = pdatadict
        self.pdb[pkey]['pdatadict'] = pdatadict
        self.pdb[pkey]['plabel'] = plabel
        self.pdb[pkey]['punits'] = punitlist
    
    
    def get_data(self,dkey):
        ''' get column data based on the dkey in format of
            a) tablename:column name
            b) tablename:column index
            c) tablename:column id/name|mask1|mask2|
        '''
        tablekey,columnid =dkey.split(':')
        
        masklist = None
        if '|' in columnid:
            temp = columnid.split('|')
            columnid = temp[0]
            masklist = temp[1:]
            
        
        if type(columnid) != int:
            columnid = self.tdb[tablekey]['labellist'].index(columnid)          
        
        
        
        sourcedata = self.tdb[tablekey]['data'][:,columnid]
        sourceunit = self.tdb[tablekey]['unitlist'][columnid]
        
        if masklist != None:
            for maskkey in masklist:
                sourcedata = self.mdb[masklist].apply(sourcedata)
        
            
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
    
    
    def retrive_result_simple(self,tablekey,columnid,mode='x'):
        
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
                sourcedata =   uscale * sourcedata  + ushift            
        
        return sourcedata,targetunit
    
    def retrive_result(self,pkey,dkey,mode='x',icurve=0):
        ''' retrive results from table
            pkey: plotdata key
            dkey: in format of tablename:columnid|mask1|mask2|mask3|
        
        '''
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
                sourcedata =   uscale * sourcedata  + ushift
                
        # do transformation if needed
        
        if icurve != 0 and self.pdb[pkey]['transform'] != None:
            if icurve in self.pdb[pkey]['transform'].keys():
                if mode in self.pdb[pkey]['transform'][icurve].keys():
                    tscale,tshift = self.pdb[pkey]['transform'][icurve][mode]
                    sourcedata = tscale * sourcedata  + tshift
        
        
        
        # apply the masks
        for key in masklist:
            sourcedata = self.mdb[key].oper(sourcedata)
        
        
        # change data to index
        
        if mode == 'index':
            sourcedata = range(1,len(sourcedata)+1)
            targetunit = 'N/A'
        return sourcedata,targetunit
    
    

    
    # ================== the modification functions API for GUI functions ===
    
    """
    def edit_tdb_unitlabel(self,tablename,col_id_start,col_id_end,unitlabel):
        for ind in range(col_id_start,col_id_end+1):
            self.tdb[tablename]['unitlist'][ind] = unitlabel

    def edit_tdb_label(self,tablename,columnid,updatelabel):
        self.tdb[tablename]['labellist'][columnid] = updatelabel
            
    def edit_pdb_unit(self,pkey,x1unit,y1unit,x2unit='N/A',y2unit='N/A'):
        ''' edit the plot data unit list '''
        self.pdb[pkey].unit = [x1unit,y1unit,x2unit,y2unit]

    def edit_pdb_limits(self,pkey,label,value):
        ''' edit the plot data unit list '''
        if label == 'x1_max':
            self.pdb[pkey].maxlimits[0] = value
        elif label == 'y1_max':
            self.pdb[pkey].maxlimits[1] = value
        elif label == 'x2_max':
            self.pdb[pkey].maxlimits[2] = value
        elif label == 'y2_max':
            self.pdb[pkey].maxlimits[3] = value
        elif label == 'x1_min':
            self.pdb[pkey].minlimits[0] = value
        elif label == 'y1_min':
            self.pdb[pkey].minlimits[0] = value
        elif label == 'x2_min':
            self.pdb[pkey].minlimits[0] = value
        elif label == 'y2_min':
            self.pdb[pkey].minlimits[0] = value
        else:
            raise KeyError,('Plot data ',pkey,'limit label ',label,' wrong, shall be (x1_max,x2_min,y1_max,y2_max.etc)')
    def edit_pdb_label(self,pkey,x1,y1,x2='x2',y2='y2'):
        ''' edit the plot data label list '''
        self.pdb[pkey].label = [x1,y1,x2,y2]

    def edit_pdb_legend(self,pkey,icurvekey,legendlabel):
        ''' edit the plot data label list '''
        try:
            icurvekey = int(icurvekey)
        except:
            raise TypeError,('The key for icurve instance shall be int or shall be able to convert to int,got',type(icurvekey),icurvekey)
        
        
        # convert the quantity request sign of $
        
        if '$' in legendlabel:
            data,unit = self.raw_retrive_colrow(legendlabel)
            legendlabel = '%6.3f %s' % (data,unit)
        
        self.pdb[pkey].curvelib[icurvekey].legend = legendlabel
        
        #if legendlabel =='None':
        #    self.pdb[pkey].curvelib[icurvekey].showlegend = False
        #else:
        #    self.pdb[pkey].curvelib[icurvekey].showlegend = True
        #    self.pdb[pkey].curvelib[icurvekey].legend = legendlabel

    def edit_pdb_settings(self,pkey,typekey,stylekey):
        ''' edit the plot data label list '''
        self.pdb[pkey].type = typekey
        self.pdb[pkey].style = stylekey
        
        
    # ===================following are drawing functions
    
    def add_figure(self,fskey,pkey,skey,ftype):
        ''' create figure configuration '''
        #self.fsdb[fskey] = {'fskey':fskey,'pkey':pkey,'skey':skey,'ftype':ftype}
        
        # update the plot data settings for figure type and style
        self.pdb[pkey].type = ftype
        self.pdb[pkey].style = skey
        
        # process plot data
        self.process(pkey)
        
        # realize the figures
        self.figurerealize(pkey,fskey=fskey)
    
    def figurerealize(self,pkey,fskey=None):  # figurename and plotdata name
        # process and retrive plot data and apply masks
        self.pdb[pkey].process(self)
        
        # obtain the plot settings
        fssetting = self.pdb[pkey]
        
        # realize the figures
        ftype = fssetting.type
        
        # setup figure keys
        if fskey == None:
            fname = pkey
        else:
            fname = fskey
        
        if ftype == 'line-one axis':
            fig = self.line(fname,pkey=pkey,skey=fssetting.style,mode='single',legend=True)
        else:
            print 'figure type ',ftype,' do not defined'
        

        return fig.figure
    
    def line(self,fkey,pkey=None,skey='default',mode='single',legend=True):
        if pkey == None:
            pkey = fkey
        
        plotdata = self.pdb[pkey]
        
        if mode == 'single':
            fig = single_axis_line(plotdata,style=self.sdb[skey])
            
        elif mode == 'double':
            fig = double_axis_line(plotdata,style=self.sdb[skey])
    
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
    
    def savefig(self,fkey,format,name=None,dpi=300):
        ''' save single figure in database'''
        if name == None:
            name = fkey+'.'+format
            resfolder = os.path.join(*path)
            if not os.path.isdir(resfolder):
                os.mkdir(resfolder)
            name = os.path.join(resfolder,name)        
        
        

        self.figurerealize(fkey)
        self.fdb[fkey].figure.savefig(name,format=format,dpi=dpi)
    
    
    def saveallpdata(self,path=None,delimiter='\t'):
        ''' save all plot data'''
        for pkey in self.pdb.keys():
            self.savepdata(pkey,path=path,delimiter=delimiter)
    
    def savepdata(self,pkey,name=None,delimiter='\t'):
        ''' save single plot data'''
        if name == None:
            name = pkey+'.csv'
            #resfolder = os.path.join(*path)
            #if not os.path.isdir(resfolder):
             #   os.mkdir(resfolder)
            #name = os.path.join(resfolder,name)
            
        pdata = self.pdb[pkey]
        
        if delimiter == '\t':
            extension = '.txt'
        elif delimiter == ',':
            extension = '.csv'
        else:
            extension = '.out'
        
        name = pkey + extension
        

        for keys in pdata.curvelib.keys():
            
            newfilename = name + '_' + str(keys) + '.txt'
            f1 = open(newfilename,'w')
            labels = delimiter.join([pdata.curvelib[keys].xcolumnname,pdata.curvelib[keys].ycolumnname]) + '\n'
            f1.write(labels)
    
            units = delimiter.join([pdata.curvelib[keys].xunit,pdata.curvelib[keys].yunit]) + '\n'
            f1.write(units)

            dataxy = np.vstack([pdata.curvelib[keys].xdata,pdata.curvelib[keys].ydata]).T
            np.savetxt(f1,dataxy,delimiter=delimiter)
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
   
    
    #==================prodceures
    
    
    def plot_procedure_dist(self,*args):
        plotkey = args[0]
        Xinput = args[1]
        Yinput = args[2]
        Linput = args[3]
        #incrstart = int(args[4])
        #incrend = int(args[5])
        #incrstep = int(args[6])

        savefig = args[4]
        savepdata = args[5]
        
        fstyle = 'test'
        ftype = 'line-one axis'
        
        #if incrend == -1:
        #    tablekey,columnlabel = Linput.split(':')[0:2]
        #    incrend = self.get_table_column_size_by_label(tablekey,columnlabel)
        
        curvecount = 1
        for label in self.tdb[Yinput]['labellist']:#incrstart,incrend+1,incrstep):
            Yinputfull = Yinput+':'+label  # increment name
            self.add_plotdata_command(plotkey,[Xinput,Yinputfull]) #plotkey,tablekey,pairidlist,mode='xy')
            
            
            Linputfull = '$'+Linput % {'incr':str(label)}
            
            self.edit_pdb_legend(plotkey,curvecount,Linputfull)    # update the plot legend
            curvecount += 1    
            
        self.append_plotdata_mask(plotkey,'xy','pair_sortx')   
        self.add_figure(plotkey,plotkey,fstyle,ftype)
        if len(savefig) >0: self.savefig(plotkey,savefig,name=plotkey+'.'+savefig)
        if savepdata == '1':self.savepdata(plotkey+'.csv')

        
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
    
    
    rp.add_plotdata_command('plot1',['da:dx|flip','db:dx'])
    rp.edit_pdb_unit('plot1','in.','in.','mm','mm')
    rp.process('plot1')
    rp.line('plot1','plot1',skey='publish')
    rp.savefig('plot1','jpg')
    print 1
    
    '''
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
    '''
    
    