from plots import plots
import csv
import numpy as np
class importfile_opensees_dat():
    """ ## class to import opensees file """
    def __init__(self,model,logfile=None):
        self.model = model                    ### define the input file  
        self.logfile = logfile
        self.results = plots.tpfdb()

    
    def convert(self,st):
        return float(st)
    
    def get_res(self,recorderkey,labellist=None,unitlist=None):
        ''' get results based on the recorderkey '''
        csvfile = self.model.reclist[recorderkey].recfile
        reader = csv.reader(open(csvfile, "rb"), delimiter=' ')
        result = np.array([[self.convert(col) for col in row] for row in reader])        
        
        self.results.add(recorderkey,result,unitlist=unitlist,labellist=labellist)
    
    def get_res_all(self,labellist=None,unitlist=None):
        for recorderkey,item in self.model.reclist.items():
            csvfile = self.model.reclist[recorderkey].recfile
            reader = csv.reader(open(csvfile, "rb"), delimiter=' ')
            result = np.array([[self.convert(col) for col in row] for row in reader])        
            
            self.results.add(recorderkey,result,unitlist=unitlist,labellist=labellist)
        
        
    
    
    
if __name__ == '__main__':
    imp1 = importfile_marc_dat('pullout_job1.dat',stylesetting='Extended')
    imp1.processf()
    vv1 = imp1.scanf_lines(imp1.contentdict['coordinates'],coordinates)
    vv2 = imp1.scanf_lines(imp1.contentdict['connectivity'],connectivity)
    print vv