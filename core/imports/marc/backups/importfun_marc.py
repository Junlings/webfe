import unittest
import re
import sys

class keylines():
    ''' single line parser'''
    def __init__(self,spliter = ' '):
        self.mode = 'Free'
        self.spliter = spliter
        self.format = []
        self.spaces = []
        
    def addlineformat(self,formatline):
        """ input formatline should be instance of singlelineformat class """
        self.format.append(formatline)
        
    def addspace(self,spaceline):
        """ input formatline should be instance of singlelineformat class """
        self.spaces.append(spaceline)
        
    def split_line(self,seq, length,times=1):
        temp = []
        ind_s = 0
        for i in range(0,len(length)):
            tempstr = seq[ind_s:ind_s+length[i]*times].strip()
            
            temp.append(tempstr)
            ind_s += length[i]*times
        
        return temp
    
    def scientific(self,aa,mode):
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
        
        '''
        if mode == 'Extended':
            num = float(re.search(r'^.\d+.\d+',aa).group())
            exp = int(re.search(r'\d+$',aa).group())
            expsign = re.search(r'[\+/-]\d+$',aa).group()[0]
            
            if expsign == '+':
                value = num * (10 ** (exp))
            
            elif expsign == '-':
                value = num / (10 ** (exp))
            
            else:
                raise TypeError
            
            return float(value)
            
        elif mode == 'Free':
            bb = re.search(r'\d[\+/-]\d',aa)
            
            if bb != None:
                str2 = bb.group()
                aa = re.sub(str2,''.join([str2[0:1],'E',str2[1:3]]),aa)
        return aa
        '''
    def zip_format(self,lista,stringb=None):
        formatstr = ''
        for i in range(0,len(lista)):
            if stringb == None:
                # in form of '%f,%f'
                formatstr += '%' + str(lista[i]) + ' '
            else:
                formatstr += '%' + str(stringb[i]) + str(lista[i])
        return formatstr
    
    def num_item_format(self,item,formatstring,mode):
        if formatstring == None:
            pass  
        elif 's' in formatstring or 'S' in formatstring:
            return item
        elif 'i' in formatstring or 'I' in formatstring:
            try:
                int(item)
            except ValueError:
                print '[Warning] convert"' + item+'" to integral failed' 
            else:
                return int(item)
            
        elif 'f' or 'F' in formatstring:
            try:
                float(item)
            except ValueError:
                try:
                    item = self.scientific(item,mode)
                    float(item)
                except ValueError:
                    print '[Warning] convert"' + item+'" to floating failed'
                else:
                    return float(item) 
            else:
                return float(item) 
        else:
            return item
        
    def num_list_format(self,list,formatarray,mode='Free'):
        """
        Convert the string to numerical value based on the format requirement
        """
        if len(list)==0:
            print 'blank line encountered'
            return None
        else:
            if len(list) != len(formatarray):
                print 'length of list and format not match'
                return -1
            else:
                line = map(self.num_item_format,list,formatarray,mode)
                return line
        
    def extract(self,lines,mode='Free'):
        templine = []

        for i in range(0,len(lines)):
            if mode == 'Free':
                if i < len(self.format):
                    format = self.format[i]
                else:
                    format = self.format[-1] # use last one
                    
                newline = lines[i].split(self.spliter)
                templine.append(self.num_list_format(newline,format))
            
            else:

                if i < len(self.format):
                    format = self.format[i]
                else:
                    format = self.format[-1] # use last one
                    
                if i < len(self.spaces):
                    spaces = self.spaces[i]
                else:
                    spaces = self.spaces[-1] # use last one
                if mode == 'Extended':
                    convlines = self.split_line(lines[i],spaces,times=2)  # split by spaces
                elif mode == 'Fixed':
                    convlines = self.split_line(lines[i],spaces)  # split by spaces
                
                else:
                    raise TypeError
                #formatstr = self.zip_format(format)    # convert to format
                templine.append(self.num_list_format(convlines,format,mode))               
            
        return templine
        
class importfun_marc():
    def __init__(self,style='Extended'):
        self.filestyle = style  # can be 'free','Fixed', or 'Extend'
        #self.prj = project()
    def __getitem__(self,line):
        try:
            fun = getattr(self,line)
        except:
            print 'keyword:"',line,'" not defined,skipped'
            fun = getattr(self,'skipped')
        return fun
    
    ## following are the handle for the keywords
    def skipped(self,lines):
        for i in lines:
            print i
    
    def title(self,lines):
        pass
    def coordinates(self,lines):
        lines1 = keylines()
        lines1.spliter = ' '
        
        lines1.addlineformat(['s'])
        lines1.addspace([11])
        
        lines1.addlineformat(['i','i','i','i'])
        lines1.addspace([5,5,5,5])
        
        lines1.addlineformat(['i','f','f','f'])
        lines1.addspace([5,10,10,10])        
        
        res = lines1.extract(lines,mode=self.filestyle)
        return res
        

class test_keylines(unittest.TestCase):
    def test_singleline_freeinput(self):
        lines1 = keylines()
        lines1.spliter = ','
        lines1.addlineformat(['s','i','f','f'])
        strs1 =[ 'asasas,98,0.1,0.2,']
        strs2 =[ 'asasas,98,0.1,0.2']
        strs3 =[ 'asasas 98 0.1 0.2']
        
        res = [('asasas', 98, 0.1000000000000000, 0.2000000000000000)]

        self.assertEquals(res,lines1.extract(strs1))
        self.assertEquals(res,lines1.extract(strs2))
        self.assertEquals(res,lines1.extract(strs3))
        
    def test_multiline_freeinput(self):
        lines1 = keylines()
        lines1.spliter = ','
        lines1.addlineformat(['s','i','f','f'])
        lines1.addlineformat(['f','f','f','f'])
        
        strs1 =[ 'asasas,98,0.1,0.2,','1,2,3,4','1,2,3,4','1,2,3,4.256']

        res = lines1.extract(strs1)
        #print res

    def test_singleline_fixinput(self):
        lines1 = keylines()
        lines1.addlineformat(['s','i','f','f'])
        lines1.addspace([10,5,5,5])
        
        strs =['asasas99  8    0.1  0.2  ']

        res = lines1.extract(strs,mode='Fixed')
        print res

if __name__ == '__main__':
    #unittest.main()
    #f1 = importfun_marc()
    lines1 = keylines()
    strs1 = ['coordinates x 0 0 0']
    lines1.addlineformat(['s','s','f','f','f'])
    
    res = lines1.extract(strs1)
    print res
    
    ff1 = importfun_marc()
    n1 = node([1,2,3])
    print 'aa'
    #f1['coordinates'](line)