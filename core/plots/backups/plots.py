""" This is the module """
""" This is the module """
import os
from unitsystem import create_units
from plottypes.line import double_axis_line, single_axis_line

class tpfdb():
    ''' result plot database '''
    def __init__(self):
        self.pdb = {}  # plot database:  table format
        self.fdb = {}  # figure database: figure format
        self.tdb = {}  # result table database
        self.UI = create_units()
    
    def add(self,key,array2D,unitlist=None,labellist=None):
        self.tdb[key] = {'data':array2D,'unitlist':unitlist,'labellist':labellist}
        
    
    def add_plotdata_table(self,plotkey,tablekey,pairidlist,mode='xy',units=None,xylabels=None,scale=None,shift=None):
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
                
        
        self.add_plotdata(plotkey,keypairlist,units=units,xylabels=xylabels)
        
    def add_plotdata(self,pkey,keypairlist,units=None,xylabels=None,transform=None):
        ''' specify the data source name with 'table:col' indicate a column in table '''

        self.pdb[pkey] = {'datalabelpair':keypairlist,
                          'units':units,
                          'xylabels':xylabels,
                          'transform':transform}

    
   
    def process_plotdata(self,pkey):
        pdatalist = []
        plabel = []
        punitlist = []
        icurve = 1
        for key in self.pdb[pkey]['datalabelpair']:
            # deal with x axis
            datax,unitx = self.retrive_result(pkey,key[0],mode='x',icurve=icurve)
            
            # deal with y axis
            datay,unity = self.retrive_result(pkey,key[1],mode='y',icurve=icurve)
            
            pdataxy = np.vstack([datax,datay]).T
            icurve += 1
            pdatalist.append(pdataxy)
            plabel.extend([key[0],key[1]])
            punitlist.extend([unitx,unity])    
        pdata = pdatalist[0]
        for datai in pdatalist[1:]:
            pdata = np.hstack([pdata,datai])
            
        self.pdb[pkey]['pdata'] = pdata
        self.pdb[pkey]['pdatalist'] = pdatalist
        self.pdb[pkey]['plabel'] = plabel
        self.pdb[pkey]['punits'] = punitlist


    
    def retrive_result(self,pkey,dkey,mode='x',icurve=0):
        
        # locate record in table
        key_b = dkey
        tablekey,columnid =key_b.split(':')
        if type(columnid) != int:
            columnid = self.tdb[tablekey]['labellist'].index(columnid)        
        
        
        # retract unit target
        if mode == 'x':
            targetunit = self.pdb[pkey]['units'][0]
        else:
            targetunit = self.pdb[pkey]['units'][1]
        
       
       # do unit convert
        if tablekey in self.tdb.keys():  # defined in table
            
            sourcedata = self.tdb[tablekey]['data'][:,columnid]
            sourceunit = self.tdb[tablekey]['unitlist'][columnid]
            
            [uscale,ushift] = self.UI.convert(sourceunit,targetunit)
            if not (uscale == 1 and ushift == 0):
                sourcedata = sourcedata * uscale + ushift
                
        # do transformation if needed
        
        if icurve != 0:
            if icurve in self.pdb[pkey]['transform'].keys():
                if mode in self.pdb[pkey]['transform'][icurve].keys():
                    tscale,tshift = self.pdb[pkey]['transform'][icurve][mode]
                    sourcedata = sourcedata * tscale + tshift
        
        return sourcedata,targetunit
            
    def line(self,fkey,pkey,mode='single'):
        plotdata = self.pdb[pkey]['pdata']
        units = self.pdb[pkey]['units']
        xylabels = self.pdb[pkey]['xylabels']
        
        if mode == 'single':
            fig = single_axis_line(plotdata,units,xylabels)
            
        elif mode == 'double':
            fig = double_axis_line(plotdata,units,xylabels)
    
        self.fdb[fkey] = fig
        
    def saveall(self,format,dpi=300,path=None):
        for fkey in self.fdb.keys():
            
            name = fkey+'.'+format
            if path != None:
                resfolder = os.path.join(*path)
                if not os.path.isdir(resfolder):
                    os.mkdir(resfolder)
                name = os.path.join(resfolder,name)
            
            self.save(fkey,format,name=name,dpi=dpi)
    
    def save(self,fkey,format,name=None,dpi=300):
        if name == None:
            name = fkey+'.'+format
        self.fdb[fkey].savefig(name,format=format,dpi=dpi)
    
    def savepdata(self,pkey,path=None,delimiter='\t'):
        
        if delimiter == '\t':
            extension = '.txt'
        elif delimiter == ',':
            extension = '.csv'
        else:
            extension = '.out'
            
        pdata = self.pdb[pkey]['pdata']
        if path != None:
            filename = os.path.join(path,pkey,extension)
        else:
            filename = pkey + extension
            
        f1 = open(filename,'w')
        labels = delimiter.join(self.pdb[pkey]['plabel']) + '\n'
        f1.write(labels)

        units = delimiter.join(self.pdb[pkey]['punits']) + '\n'
        f1.write(units)

        
        np.savetxt(f1,pdata,delimiter=delimiter)
        f1.close()

    
if __name__ == '__main__':
    import numpy as np
    rp = tpfdb()
    
    rp.add('da',np.array([[1,2,3,6,7,8,8]]).T,unitlist=['m'],labellist=['dx'])
    rp.add('db',np.array([[5,6,8,6,7,8,8],[1,2,3,5,6,1,7]]).T,unitlist=['m','m'],labellist=['dx','dy'])
    

    
    rp.add_plotdata('plot1',[['da:dx','db:dx'],['da:dx','db:dy']],units=['m','m'],xylabels=['x','y'],transform={1:{'x':[2,10]}})
    rp.add_plotdata('plot2',[['da:dx','db:dx'],['da:dx','db:dy']],units=['m','m','in.','in.'],xylabels=['x1','y1','x2','y2'],transform={1:{'x':[2,-10]}})
    
    rp.process_plotdata('plot1')
    rp.process_plotdata('plot2')
    rp.line('plot1','plot1')
    rp.line('plot2','plot2',mode='double')
    rp.save('plot1','eps')
    rp.save('plot2','eps')
    rp.savepdata('plot1')
    print 1