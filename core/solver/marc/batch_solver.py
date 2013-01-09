import csv
import os
import shlex, subprocess
from time import clock, time

def run_marc_dat(folder,sourcefile):
    # define subprocess
    OP=subprocess.Popen(['run_marc.bat','-jid',sourcefile,'-dir',folder],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
    
    # link the pipe 
    flag = OP.stdout
    pipe = OP.stdin
    
    # write the opensees file
    #pipe.write('source '+ 'source'+ r'/'+ sourcefile + '\n')
    print flag.readline()
    
    #retcode = OP.wait()

    return 1

class generate_batch():
    ''' This is the module to generate batch dat file based on the
        properly rewritted dat file for parametric analysis reasons
    '''
    def __init__(self,sourcefile,parafile=None,keylist=None):
        '''
        need input sourcefile and parameter list file
        '''
        self.sourcefile = sourcefile
        self.keylist = keylist
        # get folder name and project name 
        self.pjname = os.path.basename(self.sourcefile)
        self.folder = os.path.split(os.path.abspath(sourcefile))
        self.datfolder = []
        
        # read the source file and record the content      
        f1 = open(sourcefile,'r')
        self.cont = f1.read()
        f1.close()
        
        # read the parameter file if needed
        if parafile != None:
            self.para_dict = self.read_para(parafile)
    
    
    def read_para(self,filename,delimiter=','):
        f1 = open(filename,'r')
        
        csvreader = csv.reader(f1, delimiter=delimiter)
        para_dict = {}
        
        title =  csvreader.next()  #read first line as parameter name
    
        for row in csvreader:
            temp_dict = {}
            for i in range(1,len(title)):      # skip column 1 as id
                temp_dict[title[i]] = row[i]   # read parameter value
            
            para_dict[row[0]] = temp_dict      # add parameter value to 
        
        self.para_dict = para_dict
        
        return para_dict
            
        
    def convertToScientific(self,nr,total_len=20):
        '''
        This function convert the number in nr to the fixlength marc fix input style
        '''
        
        nr = float(nr)
        total_len = total_len
        
        # deal with value zero
        if nr == 0:
            return ' 0.0' + '0'* (total_len-6) + '+0'
        
        # get exponential with single digits float
        coefficient = float(nr)
        exponent = 0
        while abs(coefficient) >= 10:
            exponent += 1
            coefficient = coefficient / 10
        while abs(coefficient) < 1:
            exponent -= 1
            coefficient = coefficient * 10
        
        # construct the fix length output
        exp = ''
        if coefficient >= 0:
            exp1 = ' %s' % str(coefficient)  # if pisitive, neglect the positive sign
        else:
            exp1 = '%s' % str(coefficient)   # if negative, sign include in coefficient
        
        if exponent >= 0:
            exp2 = '+%s' % str(exponent)
        else:
            exp2 = '%s' % str(exponent)
        
        
        # check if length of exp1 exceed the request and chunk it if needed        
        len_exp = len(exp2)
        len_float = total_len - len_exp
        exp_final = ''
        
        if len_float <= exp1:
            exp_final = exp1 + '0'*(len_float-len(exp1))+ exp2
        else:
            exp_final = exp1[:len_float+1]+ exp2
        return exp_final
    
    
    def generate(self):
        '''
        This function generate the parameter filled dat file under designated folder
        '''
        if len(self.para_dict.keys()) >0:  # loop over para groups
            for key in self.para_dict.keys():
                
                # check if key in required keylist
                if self.keylist != None:
                    if key not in self.keylist:
                        continue
                
                # start generate batch file
                resfolder = os.path.join(self.folder[0],key)
                self.datfolder.append(resfolder)
                
                if not os.path.isdir(resfolder):
                    os.mkdir(resfolder)
                
                filename = os.path.join(resfolder,self.folder[1])
                self.generate_single(filename,self.para_dict[key])
        
    
    def generate_single(self,filename,para):
        '''
        This will generate singel dat file based on the folder and parametric dict
        '''
        f2 = open(filename,'w')
        for key in para:
            if key != 'notes':
                para[key] = self.convertToScientific(para[key])
        f2.write(self.cont % para)
        
    
    def run_all(self):
        for folder in self.datfolder:
            # check if key in required keylist
            key = folder.split('\\')[-1]
            if self.keylist != None:
                if key not in self.keylist:
                    continue
            self.run_single(folder)
        
    def run_single(self,folder):
        print 'Runing Job at folder:',folder
        t1 = time()
        sourcefile = os.path.join(folder,self.folder[1])
        OP=subprocess.Popen(['run_marc.bat','-jid',sourcefile,'-dir',folder],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
        
        # link the pipe 
        flag = OP.stdout
        pipe = OP.stdin
        
        # write the opensees file
        #pipe.write('source '+ 'source'+ r'/'+ sourcefile + '\n')
        print flag.readline()
        
        #retcode = OP.wait()
        t2 = time()
        print 'Job at folder:',folder,' finished, use',t2-t1,'seconds'
        return 1
        
    
    def post_all(self,postfun):
        for key in self.para_dict.keys():
            # check if key in required keylist
            if self.keylist != None:
                if key not in self.keylist:
                    continue
            self.post_single(key,postfun)
            
    def post_single(self,key,postfun):
        postfun(key,self.folder[1].split('.')[0]+'.t19')
        

if __name__ == '__main__':
    di = generate_batch('model1_job1.dat')
    di.read_para('para.csv',delimiter=',')
    di.generate()
    di.run_all()
