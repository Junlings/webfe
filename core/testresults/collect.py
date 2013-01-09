import sys
import os
import string
from math import *
from time import strftime
import numpy as np
import csv
from plots.plots import tpfdb

def force_float(str):
    if len(str) > 0:
        return float(str)
    else:
        return 0.0
class collect:
    ''' collect summarized csv file into python based result file '''
    def __init__(self,title):
        self.database = tpfdb()  # table, plot and fig database
 
    def import_cvs(self,folder,importfile,label=None,unit=None,delimiter=',',tablename=None):
        ''' import cvs file'''
        f2=open(os.path.join(folder,importfile),'r')
        if tablename == None:
            tablename = '_'.join(folder)+':'+importfile
        csvreader = csv.reader(f2, delimiter=delimiter)
        
        #### collect the label
        if label != None:
            labellist = csvreader.next()
 
        #### collect the unit
        if unit != None:
            unitlist = csvreader.next()
        
        dataset = []
        #### read data start from the third line, first:paraname, second:unit
        for row in csvreader:
            dataset.append(map(force_float,row))
        
        dataset = np.array(dataset)
        
        if label == None:
            labellist = ['unknown'] * dataset.shape[1]
        
        if unit == None:
            unitlist = ['n/a'] * dataset.shape[1]

        
        self.database.add(tablename,np.array(dataset),unitlist=unitlist,labellist=labellist)
        
        self.writelog(strftime("%Y-%m-%d %H:%M:%S"))
        message='Successfully import file [%s]' % importfile
        self.writelog(message)
        
    def add_labellist(self,key,labellist):
        ''' replace the original labellist '''
        self.database.tdb[key]['labellist'] = labellist        
        
    def add_unitlist(self,key,unitlist):
        ''' replace the original unitlist '''
        self.database.tdb[key]['unitlist'] = unitlist
    

    
    def writelog(self,message):
        f3=open('log.txt','a')
        f3.write(message)
        f3.write('\n')
        f3.close()
    
    
    
    # ======== Following are drawing functions
    def singlescatter(self,plotdata,plotname='plot1',units=None,xylabels=None,format='jpg',skey='default',masklist=[]):
        self.database.add_plotdata(plotname,plotdata,units=units,xylabels=xylabels,masklist=masklist)
        self.database.line(plotname,plotname,skey=skey)
        self.database.savefig(plotname,format)    
    
    # ======== Following are drawing functions
    def line(self,plotdata,plotname='plot1',units=None,xylabels=None,format='jpg',skey='default',masklist=[]):
        self.database.add_plotdata(plotname,plotdata,units=units,xylabels=xylabels,masklist=masklist)
        self.database.line(plotname,plotname,skey=skey)
        self.database.savefig(plotname,format)