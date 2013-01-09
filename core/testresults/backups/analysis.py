import sys
import string
from math import *
import pickle
from time import strftime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import rc


class analysis:
    
    def __init__(self,title):
        self.database={'title':title}
        self.plotstyle=[]
    
    def import_database(self,dbname,db):
        self.database[dbname]=db
    
 
    def export_database(self,fname,dbname):
        
        f1=open(fname+'.pydat','w')
        
        if dbname=='ALL':
            pickle.dump(self.database,f1)
        elif dbname in self.database:
            pickle.dump(self.database[dbname],f1)
        else:
            print 'No specify result database exist'
                        
        f1.close()
            

    
    
    def import_pydat(self,importfile,libname=None):
        f2=open(importfile,'r')
        db=pickle.load(f2)
        if libname==None:
            dbname=importfile.split('.')[0]
        else:
            dbname=libname
        self.import_database(dbname,db)
        f2.close()

    def import_space(self,importfile,dbname,mode='title',label=None,unit=None):
        f2=open(importfile,'r')
        
        if mode=='title':
        #### collect the label
            label=f2.readline()
            label=label[0:len(label)-1].split()
        #### collect the unit
            unit=f2.readline()
            unit=unit[0:len(unit)-1].split()
        
        dataset=[]
        database=self.database
        #### read data start from the third line, first:paraname, second:unit
        while(1):
            str=f2.readline()
            if len(str)==0:
                break
            else:
                str=str[0:len(str)-1]
                str=str.split()
                
                #print str
                
                temp=[]
                for j in range(0,len(str)):
                    temp.append(self.num_line(str[j]))
                dataset.append(temp)
        
        #### change to the numpy array datatype to facilitate the operation
        dataset=np.array(dataset)
       
        #fill the database with parameter name, unit and numerical record
        for i in range(0,len(label)):
           
            database[label[i]]=[unit[i],dataset[:,i]]
 
 
        self.database[dbname]=database
        
    def export_format(self,exportfile,libname,resname):
        f1=open(exportfile,'w')
        
        le=len(self.database[libname][resname][1])         
        for i in range(0,le):
            
            temp='%15f' % self.database[libname][resname][1][i]
            f1.write(temp)
            if (i+1)%5==0:
                f1.write('\n')
        
        f1.close()
        
        
        

    
   
    def import_cvs(self,importfile,dbname):
        f2=open(importfile,'r')
        
        #### collect the label
        label=f2.readline()
        label=label[0:len(label)-1].split(',')
        
        
        #### collect the unit
        unit=f2.readline()
        unit=unit[0:len(unit)-1].split(',')
        
        dataset=[]
        database=[]
        #### read data start from the third line, first:paraname, second:unit
        while(1):
            str=f2.readline()
            if len(str)==0:
                break
            else:
                str=str[0:len(str)-1]
                str=str.split(',')
                
                #print str
                
                temp=[]
                for j in range(0,len(str)):
                    temp.append(self.num_line(str[j]))
                dataset.append(temp)
        
        #### change to the numpy array datatype to facilitate the operation
        dataset=np.array(dataset)
        
        #fill the database with parameter name, unit and numerical record
        for i in range(0,len(label)):
            database[label[i]]=[unit[i],dataset[:,i]]
        
        self.database[dbname]=database
        
        
    
    
    
    
    
    def export_cvs(self,exportfile,libname,res):
        f1=open(exportfile,'w')
        
        for i in range(0,len(libname)):
            temp='%s,' % (libname[i])
            f1.write(temp)
        f1.write('\n')
    
        lmax=0
        for i in range(0,len(res)):
            if len(res[i])>lmax:
                lmax=len(res[i])
            
        for i in range(0,lmax):
            for j in range(0,len(res)):
                if len(res[j])>i:
                    if res[j][i]!=None:
                        temp='%f' % res[j][i]
                    else:
                        temp=''
                else:
                    temp=''
                f1.write(temp+',')
            f1.write('\n')
  
        f1.close()
                
 
        
    def num_line(self,data):
        
        if data=='':
            data=0.0
        else:
            data=float(data)
        return data
        
        
    def sign_convert(self,dbname,libname):
        if dbname in self.database.keys():
            if libname in self.database[dbname].keys():
                self.database[dbname][libname][1]=self.database[dbname][libname][1]*(-1.00)
            else:
                print 'Specify the database itmes [%s] in database [%s] do not exist' % (libname,dbname)
                
        else:
            print 'Specify the database [%s] do not exist' % dbname
        
            
        
        
    def unit_convert(self,dbname,libname,post_unit):    #### this scale funciton will change the value in the database
        
        if dbname in self.database.keys():
            if libname in self.database[dbname].keys():
                pre_unit=self.database[dbname][libname][0]
                if post_unit!=pre_unit:
                    factor=self.unit_list(pre_unit,post_unit)
                    self.database[dbname][libname][0]=post_unit
                    self.database[dbname][libname][1]=self.database[dbname][libname][1]*factor
                
                else:
                    print 'Unit the same, no conversion operated'
                    
                
            else:
                print 'Specify the database itmes do not exist'
                
        else:
            print 'Specify the database do not exist'
            
            
    def unit_list(self,pre_unit,post_unit):
        
        unit_define=[]
        unit_define.append(['kN','lbf',224.809])
        unit_define.append(['N','lbf',0.225])
        unit_define.append(['lbf','kN',0.004448])
        unit_define.append(['lbf','N',4.448])
        unit_define.append(['lbf','kip',0.001])
        unit_define.append(['kip','lbf',1000])
        unit_define.append(['in','mm',25.4])
        unit_define.append(['psi','ksi',0.001])
        unit_define.append(['strain','ms',1000000])
        unit_define.append(['kip','kN',4.448])
        unit_define.append(['kips','kN',4.448])
        unit_define.append(['strain','ms',1000000])
        unit_define.append(['Micron','ms',1])
        unit_define.append(['g','g_in',1/386.089])
        
        unit_define=np.array(unit_define)
        factor=0
        
        for i in range(0,len(unit_define)):
            if pre_unit==unit_define[i,0] and post_unit==unit_define[i,1]:
                factor=float(unit_define[i,2])
                
            else:
                continue
        
        if factor==0:
            print 'No predefined convert rule for unit [%s] to unit [%s] exist' % (pre_unit,post_unit)
        else:
            return factor
    
    
    
    
    def postplot(self,title,paralist,shift=None,nshift=None,limits=None,unit=None,timestamp='NO',x_label=None,y_label=None,legend_user=None,legend_loc=0,user_style=None,user_pointnumb=None):   #### this scale will not change the value of database, only on plotouts
        
        font = {'family' : 'Times New Roman',
                'serif':'Times New Roman',
                'size'   : 12}
        
        legend_set={'fontsize':12}
        rc('font', **font)
        rc('legend',**legend_set)
        
        #rc('lines', markersize=20)

        
        if user_style!=None:
            self.plotstyle=user_style
        
        
        #### It will be designed that if the unit of all input is not the same 
        #### Will all convert to the first appear units
        paralist=np.array(paralist)
        
        #fig1 = plt.figure(figsize=[10,20])
        fig1 = plt.figure(figsize=[6,4])        
        ax1 = fig1.add_subplot(111)
        ax1.grid(True)
        
        totaldata=[]
        totalname=[]
        
        if unit==None: ### if no unit specified, use the unit of the first parameters
            Basic_unit_x=self.database[paralist[0,0]][paralist[0,1]][0]
            Basic_unit_y=self.database[paralist[0,0]][paralist[0,2]][0]
        else:   ### if not, use the input unit system as the default system
            Basic_unit_x=unit[0]
            Basic_unit_y=unit[1]
        #print Basic_unit_x,Basic_unit_y
        if x_label==None:
            x_label=paralist[0,1]+' ('+Basic_unit_x+')'
        else:
            x_label=x_label+' ('+Basic_unit_x+')'
            
        if y_label==None:
            y_label=paralist[0,2]+' ('+Basic_unit_y+')'
        else:
            y_label=y_label+' ('+Basic_unit_y+')'
        
        
        leg=[]  ### legend collector
        
        if user_pointnumb!=None:
            lcount=len(self.database[paralist[0,0]][paralist[0,1]][1])-user_pointnumb
            if lcount>len(self.database[paralist[0,0]][paralist[0,1]][1]):
                lcount=len(self.database[paralist[0,0]][paralist[0,1]][1])
        else:
            pass
            
        
        for i in range(0,len(paralist)):
            factor_x=1.0
            factor_y=1.0
            
            ###  get the length of each pair
            if user_pointnumb==None:
                lcount=len(self.database[paralist[i,0]][paralist[i,1]][1])
                
                
    
            if self.database[paralist[i,0]][paralist[i,1]][0]!=Basic_unit_x:
                factor_x=self.unit_list(self.database[paralist[i,0]][paralist[i,1]][0],Basic_unit_x)
                
            if self.database[paralist[i,0]][paralist[i,2]][0]!=Basic_unit_y:
                factor_y=self.unit_list(self.database[paralist[i,0]][paralist[i,2]][0],Basic_unit_y)
            
            data_x=self.database[paralist[i,0]][paralist[i,1]][1]*factor_x
            data_y=self.database[paralist[i,0]][paralist[i,2]][1]*factor_y
            
            if shift!=None:
                data_x=data_x+shift[0]
                data_y=data_y+shift[1]
            
            if nshift!=None:
                data_x=data_x+nshift[i][0]
                data_y=data_y+nshift[i][1]
                

            
            totaldata.append(data_x)
            totalname.append(paralist[i,0]+'_'+paralist[i,1])
            totaldata.append(data_y)
            totalname.append(paralist[i,0]+'_'+paralist[i,2])
            
            ax1.plot(data_x[0:lcount],data_y[0:lcount],self.plotstyle[i],ms=2)
            leg.append(paralist[i,0]+'_'+paralist[i,1])##+self.database[paralist[i,0]]['title'])
        
        if legend_user==None:
            plt.legend(leg,legend_loc)
        elif legend_user=='NO Legend':
            pass
        else:
            plt.legend(legend_user,legend_loc)
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        
        if limits!=None:
            if limits[0]!=None:
                ax1.set_xlim(xmin=limits[0])
            if limits[1]!=None:
                ax1.set_xlim(xmax=limits[1])
            if limits[2]!=None:
                ax1.set_ylim(ymin=limits[2])
            if limits[3]!=None:
                ax1.set_ylim(ymax=limits[3])

        if timestamp=='NO':
            name_fig=title
            name_cvs=title+'.txt'
        else:
            name_fig=title+'_'+strftime("%Y-%m-%d-%H-%M")
            name_cvs=title+'_'+strftime("%Y-%m-%d-%H-%M")+'.txt'
       
        fig1.savefig(name_fig) ###,format='eps')
        self.export_cvs(name_cvs,totalname,totaldata)

    def definestyle(self,style):
        self.plotstyle=style
        
        
    def legend_loc_find():
        print 'best 0 ,upper right 1,upper left 2 ,lower left 3 ,lower right 4'
        print 'right 5 ,center left 6 ,center right 7 ,lower center 8 ,upper center 9 ,center'
        
        
    def point_shift(self,label_datax,label_datay,label_refx,label_refy):
        ### this function will return the shifted x-y curve, the shift depend on the reference fx-fy
        datax=np.array(self.database[label_datax[0]][label_datax[1]][1],dtype=float)
        datay=np.array(self.database[label_datay[0]][label_datay[1]][1],dtype=float)
        refx=np.array(self.database[label_refx[0]][label_refx[1]][1],dtype=float)
        refy=np.array(self.database[label_refy[0]][label_refy[1]][1],dtype=float)
        
        temp=[]


        if len(datax)!=len(datay):
            print ('the length of data x and y should be the same')
        else:
            for i in range(0,len(datax)):
                temp.append(datax[i]-np.interp(datay[i],refy,refx))
            


        return temp
