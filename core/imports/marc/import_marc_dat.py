import re
from keyword_marc import ALLlist, coordinates, connectivity

class importfile_marc_dat():
    """ ## class to import marc *.dat file """
    def __init__(self,inputfile,stylesetting='Free',logfile=None):
        self.inf = open(inputfile,'r')                    ### define the input file  
        self.content = []                                 ### initialize the file content
        self.contentdict = {}
        self.ALLlist = ALLlist                ### initialized the keywords list
        self.style = stylesetting                         ### define the style
        self.leftkey = []                                 ### define leftkeys
        self.logfile = logfile
        
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


    def scientific(self,aa):
        try:
            num = float(re.search(r'^.\d+.\d+',aa).group())
        except:
            num = float(re.search(r'^\d+.\d+',aa).group())
        
        exp = int(re.search(r'\d+$',aa).group())
        expsign = re.search(r'[\+/-]\d+$',aa).group()[0]
        
        if expsign == '+':
            value = num * (10 ** (exp))
        
        elif expsign == '-':
            value = num / (10 ** (exp))
        
        else:
            raise TypeError
        
        return float(value)
            
            
    def convert_val(self,mystr, format):
        
        if format == 'f':
            res = self.scientific(mystr)
        elif format == 'i':
            try:
                res = int(mystr)
            except:
                return None
        else:
            res= None
        
        return res
    
    
    def get_length(self,charlen):
        if self.style == 'Extended':
            charlen = int(charlen)*2
        else:
            charlen = int(charlen)        
        return charlen
    
    

    
    def scanf_single_line(self,mystr,formatlist):
        
        nstart = 0
        res = []
        for format in formatlist:
            charlen,chartype = format.split('%')
            if charlen == 'repeat':
                charlen,chartype = formatlist[int(chartype)].split('%')
                charlen = self.get_length(charlen)
                # deal with the rest of line, use the last designation
                nn = (len(mystr)-nstart)/charlen
                
                for i in range(0,nn):
                    try:
                        res.append(self.convert_val(mystr[nstart:nstart+charlen],chartype))
                    #res.append(mystr[nstart:nstart+charlen])
                    except:
                        raise Error
                    nstart += charlen
                return res                
            
            else:  

                charlen = self.get_length(charlen)
                if chartype != 'repeat':
                    try:
                        res.append(self.convert_val(mystr[nstart:nstart+charlen],chartype))
                    #res.append(mystr[nstart:nstart+charlen])
                    except:
                        raise Error
                    
                    nstart += charlen
        return res 
 
    def scanf_lines(self,inputlines,formatdict):
        
        res = []
        for n_line in range(0,len(inputlines)):
            
            inputstr = inputlines[n_line]
            if n_line not in formatdict.keys():
                res.append(self.scanf_single_line(inputstr,formatdict[formatdict['repeat'][0]]))
            else:
                res.append(self.scanf_single_line(inputstr,formatdict[n_line]))
        return res
                  
    
    def get_coordinates(self):
        if 'coordinates' not in self.contentdict:
            self.processf()   
        vv = self.scanf_lines(self.contentdict['coordinates'],coordinates)
        return vv
    
    def get_connectivity(self):
        if 'connectivity' not in self.contentdict:
            self.processf()
        vv = self.scanf_lines(self.contentdict['connectivity'],connectivity)
        return vv
    
    def add_nodes(self,model1):
        ''' add nodes to the model '''
        coords = self.get_coordinates()
        model1.node(coords[2:])
        if self.logfile != None:
            print 'Imported %s nodes\n' % len(coords[2:])
        return model1
    
    def add_elements(self,model1):
        ''' add nodes to the model '''
        conns = self.get_connectivity()
        model1.element(conns[2:],daterange=[2,9])
        if self.logfile != None:
            print 'Imported %s elements\n' % len(conns[2:])
        return model1
    
    
if __name__ == '__main__':
    imp1 = importfile_marc_dat('pullout_job1.dat',stylesetting='Extended')
    imp1.processf()
    vv1 = imp1.scanf_lines(imp1.contentdict['coordinates'],coordinates)
    vv2 = imp1.scanf_lines(imp1.contentdict['connectivity'],connectivity)
    print vv