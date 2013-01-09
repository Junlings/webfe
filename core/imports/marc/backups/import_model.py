##### Import the keyword database
import keyword_marc as marcALLlist
import importfun_marc as marcfun
#import keyword_nastran as NastranALLlist
#import keyword_sap as sapALLlist
#import keyword_opensees as openseesALLlist

class import_file:
    """
    base class of import file
    ### Function of this base class including
    ### 1### Define the data structure of FEM analysis 
    ### 2### Define the 
    """
    
    def __init__(self):
        """  """
        pass
        
    def keyworddetect(self,line,ALLlist,style):
        """the program switcher form the derived class"""
        pass  ### left blank so the derived class to override tis function
    
    

class importfile_marc_dat(import_file):
    """ ## class to import marc *.dat file """
    def __init__(self,inputfile,stylesetting='Free',keywordlist=None):
        import_file.__init__(self)                        ### initiate the parent class
        self.inf = open(inputfile,'r')                    ### define the input file  
        self.content = []                                 ### initialize the file content
        self.contentdict = {}
        self.ALLlist = marcALLlist.ALLlist                ### initialized the keywords list
        self.style = stylesetting                         ### define the style
        self.marcfun = marcfun.importfun_marc(self.style)
        self.leftkey = []                                 ### define leftkeys
        #self.keywordlist=keywordlist                      ### optional keyword list for partial extraction
        
    def scanf(self):              ##### scan the file and create the key words driven input content
        preline = [] # previous line, temporary storage
        allline = [] 
        templine = ''
        while 1:
            line = self.inf.readline()  ### read the current line from file
            
            if line[0:1] == '$':  #### bypass the comment line
                continue
            
            elif len(line) == 0:  #### jump out of loop if went to the end of the file
                break
            
            elif len(line) == 1:  ### only one keyword
                testline = line
            
            else:
                testline=line.split()[0]  ## extract out the keywords
            
            # line start with keywords
            if testline in self.ALLlist['ALL']:  #### if found the keyword listed in the table
                allline.append(preline)  ### add the previous collection to allline list
                preline = []               ### empty preline
                
                if (line[len(line)-2]=='c' or line[len(line)-2]=='C' ) and line[len(line)-3]==' ':  ### detect if the current line is a continue line
                    templine=line[0:len(line)-2]                      ### if it is a continue line, put in templine
                else:    ## no continue line 
                    preline.append(line[0:len(line)-1])               ### if not a continue line, put in preline stack
                    templine=''                                       ### empty the templine   
            
            # line start without keyword, but with a continue line sign
            elif (line[len(line)-2]=='c' or line[len(line)-2]=='C' ) and line[len(line)-3]==' ':
                if len(templine)>0:
                    templine=templine+line[0:len(line)-5]
                else:
                    templine=line[0:len(line)-5]
            
            # 
            else:
                if len(templine)>0:           #### if templine not empty, add current line to it                       
                    templine=templine[0:len(templine)]+line[0:len(line)-1]  ### get rid of 'c' and '\n'
                else:   ### set as templine   #### if templine is empty, add current line to templine
                    templine=line[0:len(line)-1]
                    
                ## judge the "updated" current line be or not continue line
                if len(templine)>0 and (templine[len(templine)-1]=='c' or templine[len(templine)-1]=='C'):
                    templine=templine[len(templine)-1]      # if the current line still a continue line 
                    continue
                else:                                        # if not continue, add templine to preline stock and empty templine
                    preline.append(templine)
                    templine=''
                    
        allline.append(preline) #add the last preline as it will not be triggered in previous loop  
        
        self.content=allline
    
    def display_content(self,tag=None):
        """ display the key word driven content """
        for i in range(1,len(self.content)+1):
            if tag == None:
                # all detected keywords
                print self.content[i]
            else:
                # only specified keywords
                if self.content[i][0].split()[0] == tag:
                    print self.content[i]    

    def processf(self):
        """
        loop over all keyword driven lines 
        Scan the file and get content if have not done so far
        """
        if self.content == []:  # do the scan if have not done so
            self.scanf()
            

        for line in self.content:
            if len(line) > 0:
                keywords = line[0].split(' ')[0]
                self.contentdict[keywords] = line
    

if __name__ == '__main__':
    
    f1 = importfile_marc_dat('pullout_job1.dat',stylesetting='Extended')
    f1.processf()
    