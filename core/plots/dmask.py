#!/usr/bin/env python
""" This module define the data mask and operations to support decoration of plot column data """

import numpy as np

SINGLE_OPERATION_OPTIONS = (
    ('Shift','Shift'),                                     # shift certain amount
    ('FlipSign','FlipSign'),                               # flip the sign of whole column data
    ('CutStart','CutStart'),                               # delete the first few data points
    ('CutEnd','CutEnd'),                                   # delete the last few data points
    ('Scale','Scale'),                                     # scale the column data
    ('StartUntilLargerThan','StartUntilLargerThan'),       # delete the first few data unit read large then certain amount
)

COOP_OPERATION_OPTIONS = (
     ('Shift','Shift'),
     ('FlipSign','FlipSign'),
     ('CutStart','CutStart'),
     ('CutEnd','CutEnd'),
     ('Scale','Scale'),
     ('CutNegative','CutNegative'),                        # cut the megative part of the column data, default mode 'X'
     ('CutDrop','CutDrop'),                                # Cut the drop part of the pair data, default mode 'y'
)



def search_average(data,datanum,doorvalue,mode='LargerThan'):
    ''' search the one dimension data when the average of these datanum of continuous data larger than doorvalue
        data: column data in table
        datanum : total number of data points
        doorvalue: target values that compared to the data points
        mode: define the select criteria average of "data point" mode "doorvalue"
    
    '''
    
    for i in range(0,data.shape[0]):
        if np.average(data[i:i+datanum]) > doorvalue and mode =='LargerThan':
            return i
    
    
def search_continue(data,datanum,doorvalue,mode='LargerThan'):
    ''' search the one dimension data when there are datanum of continuous data larger than doorvalue
            data: column data in table
        datanum : total number of data points
        doorvalue: target values that compared to the data points
        mode: define the select criteria "data point" mode "doorvalue"
    '''
    count = 0
    for i in range(0,data.shape[0]):
        
        if mode == 'LargerThan':
            if data[i] > doorvalue: 
                count += 1
                if count >= datanum:
                    return i-datanum
            else:
                count = 0

def search_drop(data,dropamount):
    ''' search the data index when value of dropamount happen in the column data '''
    for i in range(data.shape[0]-1,1,-1):
        drop = float(data[i] - data[i-1])
        if  abs(drop) >  dropamount: 
                return i-1

class dmask():
    ''' class to define the data mask'''
    def __init__(self,name,paralib):
        self.name = name          # identification in the lib
        self.paralib = paralib    # define the operation lib
    

    # single column operation
    def operlist(self,coldata,operlist):
        '''operate based on the operation list'''
        for oper in operlist:
            coldata = self.oper(coldata,oper)
            #print coldata
        return coldata
    
    
    def apply(self,*args):
        ''' generic data operation '''
        if len(args) == 1:
            return self.oper(args[0])
            
        elif len(args) == 2:
            return self.coop(args[0],args[1])
             
    
    def oper(self,coldata):
        ''' single operation on input coldata '''
        oper = self.paralib
        
        if oper['oper'] == 'Shift':
            newcoldata = coldata + oper['scalar']
            
        elif oper['oper'] == 'FlipSign':
            #print coldata.shape
            newcoldata =  -1 * coldata
        
        elif oper['oper'] == 'CutStart':
            newcoldata =  coldata[oper['scalar']:]
            
        elif oper['oper'] == 'CutEnd':
            newcoldata =  coldata[0:-oper['scalar']]

        elif oper['oper'] == 'Scale':
            newcoldata =  oper['scalar'] * coldata
            
        elif oper['oper'] == 'StartUntilLargerThan':  # do not start until reach some value
            if nodenum not in oper.keys():
                oper['nodenum'] = 5  # 5 node continuous
                
            newcoldata =  oper['scalar'] * coldata
            
        else:
            raise KeyError,('Operation',oper['oper'], ' do not defined\n')
        
        #print coldata
        #print newcoldata
        return newcoldata
        
    
    # double column operation
    def coop(self,coldatax,coldatay):
        oper = self.paralib
        if oper['oper'] in  ['Shift','FlipSign','CutStart','CutEnd','Scale']:
            newcoldatax = self.oper(coldatax)
            newcoldatay = self.oper(coldatay)
            
        elif oper['oper'] == 'CutNegative':
            ''' cut the initial negative portion and until n continuous point reach certain value'''
            # which column to detect
            if 'mode' not in oper.keys():
                oper['mode'] = 'x'
            
            if 'nodenum' not in oper.keys():
                oper['nodenum'] = 10
            
            # operation
            if oper['mode'] == 'x':
                id = search_continue(coldatax,oper['nodenum'],0,mode='LargerThan')
                newcoldatax = coldatax[id:]
                newcoldatay = coldatay[id:]
                
        elif oper['oper'] == 'CutDrop':
            if 'mode' not in oper.keys():
                oper['mode'] = 'y'
            
            if oper['mode'] == 'y':  
                id = search_drop(coldatay,oper['scalar'])
                newcoldatax = coldatax[:id]
                newcoldatay = coldatay[:id]               
                    
        elif oper['oper'] == 'Sort':
            if 'mode' not in oper.keys():
                oper['mode'] = 'y'
            
            #datapair = np.vstack([[coldatax.T],[coldatay.T]])
            # sort based on y column
            if oper['mode'] == 'y':  
                ind = np.lexsort((coldatax, coldatay))     
                newcoldatax = coldatax[ind]
                newcoldatay = coldatay[ind]        
            # sort based on x column
            
            elif oper['mode'] == 'x':  
                ind = np.lexsort((coldatay, coldatax))     
                newcoldatax = coldatax[ind]
                newcoldatay = coldatay[ind]         
                
            else:
                raise KeyError,('Operation',oper['oper'], ' do not defined\n')
            
        return newcoldatax,newcoldatay
        
        


def create_default():
    ''' create commonly used default data masks'''
    frequent_masklib = {}
    frequent_masklib['col_flipsign'] = dmask('col_flipsign',{'oper':'FlipSign','scalar':None})
    frequent_masklib['pair_sortx'] = dmask('pair_sort',{'oper':'Sort','scalar':None,'mode':'x'})
    frequent_masklib['pair_sorty'] = dmask('pair_sort',{'oper':'Sort','scalar':None,'mode':'y'})
    return frequent_masklib


if __name__ == '__main__':
    import numpy as np
    

    
    a1 = np.array([1,2,3,4,5,6,8,9,0,1,2,3,4,5,6])
    a2 = np.array([1,2,3,4,5,6,8,9,0,1,2,3,4,5,6])
    a3 = np.array([1,2,3,4,5,6,8,9,0,1,2,3,4,5,6])
    print search_continue(a1,3,5,mode='LargerThan')
    print search_drop(a3,1)

    m1 = dmask('d1',{'oper':'Shift','scalar':2})

    a1 = m1.oper(a1)
    print a1
    print 1

    
    
        
        
        
        
