import csv
import os
import numpy as np

class import_plain():
    def __init__(self):
        self.filedict = {}
    
    def addfilelist(self,*args,**kargs):
        for filepath in args:
            fkey = self.addfile(filepath)
            self.readin(fkey)
            if 'db' in kargs.keys():
                if kargs['db'] != None:
                    kargs['db'].add(fkey,self.filedict[fkey]['data'],unitlist=self.filedict[fkey]['unitlist'],labellist=self.filedict[fkey]['labellist'])
        return kargs['db']
    
    def addfile(self,fullfilepath,fkey=None):
        if fkey == None:
            fkey = os.path.split(fullfilepath)[-1]
            if '.' in fkey:
                fkey,ftype = fkey.split('.')
                
                i = 2
                while fkey in self.filedict.keys():
                    fkey = os.path.split(fullfilepath)[-i] + '_' +fkey
                    i += 1
                
            self.filedict[fkey] = {'path':fullfilepath,'type':ftype}
        return fkey
    
    def readinall(self):
        for key in self.filedict.keys():
            self.readin(key)
    
    def readin(self,fkey,delimiter=',',header='',formatarray=None):
        ''' readin the file content'''
        
        # set delimiter based on file extension
        if self.filedict[fkey]['type'] == 'csv':
            delimiter=','
            
        elif self.filedict[fkey]['type'] == 'out':
            delimiter=' '
        
        # read in file
        cr = csv.reader(open(self.filedict[fkey]['path'],'rb'), delimiter=delimiter)
        
        # initial data
        n = 1
        datalist = []
        labellist = []
        unitlist = []
        
        
        # readin
        for line in cr:
            if n == 1 and 'label' in header:
                labellist = line
            elif n == 1 and 'unit' in header:
                unitlist = line
            else:
                datatemp = []
                mode = 'data'
                for item in line:
                    item = item.strip()
                    if len(item) > 0:
                        try:
                            datatemp.append(float(item))
                            
                        except:  # do not specify header but exist
                            if len(labellist) < len(line):
                                labellist.append(item)
                                mode = 'label'
                            else:
                                unitlist.append(item)
                                mode = 'unit'
                                
                    else:  # empty cell, regard as 0
                        if mode == 'data':
                            datatemp.append(0.0)
                        elif mode =='label':
                            labellist.append('N/A')
                        else:
                            unitlist.append('N/A')
                
                if len(datatemp) > 0:
                    datalist.append(datatemp)
        
        # add default label
        if len(labellist) == 0:
            labellist = ['col_'+str(i) for i in range(0,len(datalist[0]))]
        
        if len(unitlist) == 0:
            unitlist =  ['N/A' for i in range(0,len(datalist[0]))]
        self.filedict[fkey]['labellist'] = labellist
        self.filedict[fkey]['unitlist'] = unitlist
        self.filedict[fkey]['data'] = np.array(datalist)
        
if __name__ == '__main__':
    a1 = import_plain()
    a1.addfile("11//aa.txt")
    a1.addfile("22//aa.txt")
    a1.readin('aa')
    a1.readin('22_aa')
    print 1