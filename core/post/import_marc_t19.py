import numpy as np
import re
import time
import itertools
from lib.libop import savebyfile, loadbyfile

def ninteg(elemtype):
    ninterg = None
    if elemtype == 75:
        ninterg = 4
        
    elif elemtype == 188:
        ninterg = 8

    elif elemtype == 7:
        ninterg = 8
        
    else:
        raise TypeError,( 'element type',elemtype,'do not have associate integration point number')
        
    return ninterg   
def nlayer(elemtype,style='default'):
    layer = None
    if elemtype == 75:
        if style == 'default':
            #layer = 2
            layer = 2  # this value is really wired, some times for 1 sometimes for 2, maybe dependent on the thickness
        else:
            raise ValueError,('Style',style,'do not defined')

    elif elemtype == 188:
        if style == 'default':
            layer = 1

    elif elemtype == 7:
        if style == 'default':
            layer = 1        
    
    else:
        raise ValueError,( 'element type',elemtype,'do not have associate layer number','for postcode',elemtype)
    
    return layer

    
class import_marc_t19():
    def __init__(self,filename,scan=True,positiveonly=False):
        ''' class to deal with t19 output file'''
        
        
        if scan == True:
            self.filename = filename
            self.resfilename = self.filename.split('.')[0] + '.pyres'
            
            self.segments = []
            self.element_results_pro = {}
            self.nodal_results_pro = {}            
            
            self.initialimport(positiveonly=positiveonly)
        
    def initialimport(self,positiveonly):
        
        print 'start import t19 result file',self.filename,'\n'
        t1 = time.time()
        self.decomposedict()
        t2 = time.time()
        print 'File scan and decoposition finished, use',t2-t1,'second\n'
        
        
        self.process(positiveonly)
        t3 = time.time()
        print 'File increment detection finshed, use',t3-t2,'second\n'
        
        self.extract_res_eleminterg()
        t4 = time.time()
        print 'element results extracted, use',t4-t3,'second\n'
        
        self.extract_res_node()
        t5 = time.time()
        print 'nodal results extracted, use',t5-t4,'second\n'
        
        self.extract_res_time()        
        t6 = time.time()
        print 'increment time extracted, use',t6-t5,'second\n'
        
        # save the results
        self.segments = []
        savebyfile(self,self.resfilename)
        
        
    def decomposedict(self):
        '''decomposte the *.t19 file into the segments '''
        f1 = open(self.filename)
        
        lines = f1.readlines()
        seg = []
        tempdict = {}
        current_id = None
        for line in lines:
            if '=beg=' in line:
                line = line.strip().split('g=')
                temp = line[1].split('(') 
                id = temp[0].rstrip()
                name = temp[1][:-1]
                current_id = id
                tempdict[id] = {'name':name,'contentlines':[]}
                continue

            if '=end=' in line:
                #templines.append(line)
                #tempseg.append(templines)
                #templines = []
                continue
                
            if line[0:4] == '****':
                #print 'new segment'
                seg.append(tempdict)
                tempdict = {}
                continue
            
            tempdict[current_id]['contentlines'].append(line.rstrip())
        self.segments = seg
        return seg
    



    
    def search_segment_incr(self,loadcase,reqincr):
        ''' find the result block that blong to loadcase and for certain incrment '''
        for i in range(0,len(self.segments)):
            seg = self.segments[i]
            if '51600' not in seg.keys():
                continue
            
            if seg['51600']['contentlines'][0] != loadcase:
                continue
            
            incrline = seg['51701']['contentlines'][0]
            incr = map(float,incrline.split())
            
            err = 0.01
            if np.abs(incr[1] - reqincr) > err:
                continue
            elif np.abs(incr[1] - reqincr) < err:
                return i
            
            self.segments[i]['incrnum'] = reqincr
            return None
    
    def process(self,positiveonly=False):
        # process incrment 0
        self.collect_nodelist()
        self.collect_elemlist()
        self.collect_elempostcode()
        self.collect_setlist()
        
        # process increment 1-N
        for i in range(1,len(self.segments)):
            
            t1 = time.time()
            current_ana_time = self.process_all_incr(i)
            t2 = time.time()
            print 'processed increment:',i,'at time:',current_ana_time,'use',t2-t1,'second\n'
            
            if current_ana_time == None:
                self.nincr = i-1  # change the total increment number
                print 'import error found, cease processing now\n'
                break        
                
            
            elif current_ana_time < 0 and positiveonly==True:  # only collect the positive increments
                self.nincr = i-1  # change the total increment number
                print 'found negative incrment time, the following increments negelcted\n'
                break
            elif current_ana_time > 10000000:
                self.nincr = i-1  # change the total increment number
                print 'found unreasonable large positive incrment time > 10^6, the following increments negelcted\n'
                break

    def split_line(self,line,n=13):
        temp = [float(line[i:i+n]) for i in range(0, len(line), n)]
        return temp
    
    '''
    def split_line(self,line):
        temp = []
        
        while 1:
            if len(line) > 0:
                temp.append(line[0:13])
                line = line[13:]
            else:
                break
        return temp
    '''        
                
    def collect_nodelist(self):
        ''' collect node list'''
        self.coordtable = []  # coordinate table
        self.coorddict = {}
        for iline in range(0,len(self.segments[0]['50800']['contentlines'])):
            line = self.segments[0]['50800']['contentlines'][iline]
            try:
                linenum = map(float,(line.split()))
            except:
                linenums = self.split_line(line)
                linenum = map(float,linenums) 
            self.coorddict[int(linenum[0])] = iline
            self.coordtable.append(linenum)
        self.nn = len(self.segments[0]['50800']['contentlines'])
        
    def collect_elemlist(self):
        ''' collect element list'''
        self.conntable = []
        self.conndict = {}
        self.ninterp = 0
        
        for i in range(0,len(self.segments[0]['50700']['contentlines'])/2):
            line1 = self.segments[0]['50700']['contentlines'][i*2]
            line2 = self.segments[0]['50700']['contentlines'][i*2+1]
            temp = map(int,(line1.split()))
            temp.extend(map(int,(line2.split())))
            self.conntable.append(temp)
            self.conndict[temp[0]] = i
            self.ninterp += temp[2]
            
        self.ne = len(self.segments[0]['50700']['contentlines'])/2
            
    def collect_elempostcode(self):
        ''' collect element post process code list '''
        self.connposttable = []
        
        
        for i in range(0,len(self.segments[0]['50600']['contentlines'])):
            line1 = self.segments[0]['50600']['contentlines'][i]
            temp = map(int,(line1.split()))
            
            self.connposttable.append(temp)
        
        self.nepost = len(self.segments[0]['50600']['contentlines'])
        self.nincr = len(self.segments)-1
    
    def collect_setlist(self):
        self.setlist = {}
        if '51301' not in self.segments[0].keys():
            print 'no setlist found in result file'
            return 0
        
        nset = int(self.segments[0]['51301']['contentlines'][0].strip())
        current_key = None
        setlist = {}
        for i in range(1,len(self.segments[0]['51301']['contentlines'])):
            
            line1 = self.segments[0]['51301']['contentlines'][i]
            
            if line1[0] != ' ':  # title line
                current_key = line1.strip()
                setlist[current_key] = []
            else:    
                temp = map(int,(line1.split()))
                setlist[current_key].append(temp)
        
        for key in setlist.keys():
            self.setlist[key] = {'num':setlist[key][0][0],'type':setlist[key][0][1]}
            temp = []
            for i in range(1,len(setlist[key])):
                temp.extend(setlist[key][i])
            self.setlist[key]['items'] = temp    
    
    def process_all_incr(self,segN):
        # self.process_51801_incr(segN)
        try:
            #t1 = time.time()
            current_ana_time = self.process_51801_incr(segN)
            #t2 = time.time()
            #print 'success process postcode',51801,'use',t2-t1,'second\n'
        except:
            print 'process 51801 error'
            return None

        try:
            #t1 = time.time()
            self.process_52401_incr(segN)
            #t2 = time.time()
            #print 'success process postcode',52401,'use',t2-t1,'second\n'
        except:
            print 'process 52401 error'
            return None
            
        try:
            #t1 = time.time()
            self.process_51701_incr(segN)
            #t2 = time.time()
            #print 'success process postcode',51701,'use',t2-t1,'second\n'
        except:
            print 'process 51701 error'
            return None
            
        try:
            #t1 = time.time()
            self.process_51600_incr(segN)
            #t2 = time.time()
            #print 'success process postcode',51600,'use',t2-t1,'second\n'
        except:
            print 'process 51600 error'
            return None
        

        
        #self.process_52300_incr(segN)
        try:
            #t1 = time.time()
            self.process_52300_incr(segN)
            #t2 = time.time()
            #print 'success process postcode',52300,'use',t2-t1,'second\n'
        except:
            print 'process 52300 error'
            return None
        

        return current_ana_time

    def process_50600(self,segN=0):
        ''' get element number and seqlist'''
        elemlist = []
        ne = len(self.segments[0]['50700']['contentlines'])
        
        for elem in self.segments[0]['50700']['contentlines']:
            elemlist.append((map(int,(elem.split()))))
        
        self.ne = ne
        self.elemlist = elemlist
        

    def process_51801_incr(self,segN):
        seg = self.segments[segN]
        if '51801' not in seg.keys():
            raise ValueError,('No Element Integration Point Values found in segment',segN)
        temp = map(float,seg['51801']['contentlines'][1].split())
        self.segments[segN]['time'] = temp[0]
        return temp[0]
        
    def process_51600_incr(self,segN):
        seg = self.segments[segN]
        if '51600' not in seg.keys():
            raise ValueError,('No increment loadcasename found in segment',segN)
        self.segments[segN]['loadcase'] = seg['51600']['contentlines'][0]
        
    def process_51701_incr(self,segN):
        seg = self.segments[segN]
        if '51701' not in seg.keys():
            raise ValueError,('No increment number found in segment',segN)
        
        temp = map(float,seg['51701']['contentlines'][0].split())
        self.segments[segN]['incrnum'] = int(temp[1])
            
    def process_52401_incr(self,segN):
        ''' process the nodal data results '''
        results_list = ['Displacement',
                        'External Force',
                        'External Moment',
                        'Reaction Force',
                        'Reaction Moment',
                        'Rotation',
                        ]
        contentlines = self.segments[segN]['52401']['contentlines']
        
        results = {}

        if '52401' not in self.segments[segN].keys():
            raise ValueError,('No nodal results found in segment',segN)
        
        n_line = None
        for iline in range(0,len(contentlines)):
            line = contentlines[iline]
            
            if line in results_list:   # see if start a new nodal result sector
                results[line] = {}
                results[line]['id_start'] = iline
                results[line]['npara'] = map(float,self.split_line(contentlines[iline+1]))[3]  # the line follow the keyword line
                results[line]['data'] = []
                current_key = line
                n_line = 0
                
            else:
                if n_line != None:
                    n_line += 1
                    if n_line == 1 or n_line == 2:
                        continue
                    else:
                        #temp = map(float,self.split_line(line))
                        temp = self.split_line(line)
                        results[current_key]['data'].extend(temp)
                        
        self.segments[segN]['nodal_results'] = results
            
        
    def process_52300_incr(self,segN):
        ''' process the element intergration results '''
        seg = self.segments[segN]
        
        if '52300' not in seg.keys():
            raise ValueError,('No element intergration value found in segment',segN)
        
        results = []
        for line in seg['52300']['contentlines']:
            #temp = map(float,self.split_line(line))
            temp = self.split_line(line)
            results.append(temp)

        self.segments[segN]['element_results'] = results       

    
    def add_unique_to_list(self,list,item):
        if item in list:
            return list
        
        else:
            list = list.append(item)
            return list
    
    def generate_post_vector(self):
        ''' generate post vector group '''
        pgroup = {'total_strain':[],'stress':[],'crack_strain':[],'plastic_strain':[]}
        pgroupseq = []
        for code in self.connposttable:
            code_id = code[0]
            if code_id in [1,2,3,4,5,6]:    
                pgroup['total_strain'].append(code_id)
                self.add_unique_to_list(pgroupseq,'total_strain')

                
            elif code_id in [11,12,13,14,15,16]:
                pgroup['stress'].append(code_id)
                self.add_unique_to_list(pgroupseq,'stress')
                
            elif code_id in [81,82,83,84,85,86]:
                pgroup['crack_strain'].append(code_id)
                self.add_unique_to_list(pgroupseq,'crack_strain')
                
            elif code_id in [21,22,23,24,25,26]:
                pgroup['crack_strain'].append(code_id)
                self.add_unique_to_list(pgroupseq,'plastic_strain')
                
            else:
                print 'element post code id do not identified',code_id
        self.connpostgroup = pgroup
        self.connpostgroupseq = pgroupseq
    
    def extract_res_eleminterg(self):
        self.generate_post_vector()
        for incr in range(1,self.nincr+1):
            self.extract_res_eleminterg_incr(incr)

    def extract_res_time(self):
        time = []
        for incr in range(1,self.nincr+1):
            time.append(self.segments[incr]['time'])
        self.time = np.array(time).T
    
    def extract_res_eleminterg_incr(self,incr=0):
        element_results_pro = {}
        '''extract result for element integration point '''
        
        nline = 0
        # loop over elements
        for elem in self.conntable:
            elemid = elem[0]
            elemtype = elem[1]
            elemninteg = ninteg(elemtype)
            elemnlayer = nlayer(elemtype,style='default')
            res = {}
            # loop over elem layer (for shell and beam elements)
            for layer in range(1,elemnlayer+1):
                res[layer] = {}
                # loop over integration points
                for interp in range(1,elemninteg+1):
                    res[layer][interp] = {}
                    
                    # loop over the postprocess vector groups
                    for postgroup in self.connpostgroupseq:
                        
                        res[layer][interp][postgroup] = self.segments[incr]['element_results'][nline]
                        nline += 1  # increase line number
                        
            element_results_pro[elemid] = res                        # record results for element id
        self.element_results_pro[incr] = element_results_pro         # record results for increments
        

    def extract_res_node(self):
        for incr in range(1,self.nincr+1):
            self.extract_res_node_incr(incr)
            
    def extract_res_node_incr(self,incr=0):
        nodal_results_pro = {}
        '''extract result for element integration point '''
        
        res = self.segments[incr]['nodal_results']
        
        for key in res:
            
            datatable = np.array(res[key]['data'])
            npara = np.array(res[key]['npara'])
            
            if datatable.shape[0] == 0:
                datatable = np.zeros([self.nn,npara])
            else:
                #if datatable[2:,:].shape[0] * datatable[2:,:].shapep[0] != self.nn*npara:
                #    raise ValueError, ('nodal results shape:',datatable[2:,:].shape,' do not compatible with model', self.nn,'*',npara)
                
                datatable = datatable.reshape(self.nn,npara)
            
            nodal_results_pro[key] = datatable
            
            self.nodal_results_pro[incr] = nodal_results_pro
        
    
    def obtain_res_eleminterg_incr(self,elemid,postname,postcode,incr=0,ilayer=1):
        req = []
        res = self.element_results_pro[incr][elemid][ilayer]
        
        postcodeseq = self.connpostgroup[postname].index(postcode)
        for interp in res.keys():
            req.append(res[interp][postname][postcodeseq])
            
        return req
    
    
    def post_history_elem_set(self,setname,postname,postcode,incr='ALL',ilayer=1,average=False):
        if setname in self.setlist.keys():
            elemlist = self.setlist[setname]['items'] 
            req = self.post_history_elem(elemlist,postname,postcode,incr=incr,ilayer=ilayer,average=average)
        else:
            req = None
            
        return req
        
        
    def post_history_elem(self,elemlist,postname,postcode,incr='ALL',ilayer=1,average=False):
        ''' post history data for element list '''
        req = []
        for elemid in elemlist:
            req.append(self.post_history_single_elem(elemid,postname,postcode,incr=incr,ilayer=ilayer,average=average))
            
        return np.array(req).T
        
    
    def post_history_single_elem(self,elemid,postname,postcode,incr='ALL',ilayer=1,average=False):
        req = []
        if incr == 'ALL':
            incr = range(1,self.nincr+1)
            
        for iincr in incr:
            temp = self.obtain_res_eleminterg_incr(elemid,postname,postcode,incr=iincr,ilayer=ilayer)
            if average == True:
                temp = np.array(temp)
                temp = np.average(temp)
            else:
                pass
            req.append(temp)
            
        return req
                
    def post_history_time(self,incr='ALL'):
        incrtime = []
        if incr == 'ALL':
            incr = range(1,self.nincr+1)
            
        for iincr in incr:        
            incrtime.append([self.time[iincr-1]])
            
        return np.array(incrtime)
            
            
    def post_history_node_set(self,setname,postname,postcode=None,incr='ALL',sum=False):
        if setname in self.setlist.keys():
            nodelist = self.setlist[setname]['items']
            req = self.post_history_node_list(nodelist,postname,postcode=postcode,incr=incr,sum=sum)
            
        return req
        
    def post_history_node_list(self,nodelist,postname,postcode=None,incr='ALL',sum=False):
        req = []
        for nodeid in nodelist:
            req.append(self.post_history_single_node(nodeid,postname,postcode,incr=incr))
            
        return np.array(req).T        
        
        
        
            
    def post_history_single_node(self,nodeid,postname,postcode=None,incr='ALL'):
        req = []
        
        if incr == 'ALL':
            incr = range(1,self.nincr+1)
            
        for iincr in incr:
            temp = self.obtain_res_node_incr(nodeid,postname,postcode,incr=iincr)
            
            req.append(temp)
        
        req = np.array(req)
        return req
    
 
    def obtain_res_node_incr(self,nodeid,postname,postcode=None,incr=1):
        
        res = self.nodal_results_pro[incr]
        ind = self.coorddict[nodeid]
        req = res[postname][ind]
        if postcode == 'z' or postcode == 'Z' or postcode == 3:
            return [req[2]]
        elif postcode == 'x' or postcode == 'X' or postcode == 1:
            return [req[0]]
            
        elif postcode == 'rz' or postcode == 'RZ' or postcode == 'Rz' or postcode == 6:
            return [req[2]]
        elif postcode == 'rx' or postcode == 'RX' or postcode == 'Rx' or postcode == 4:
            return [req[0]]
        else:
            raise KeyError,('postcode for nodal results:', postcode, ' do not defined')
        return req        
    
    
    def retrive_node_elemset(self,setname):
        if setname in self.setlist.keys():
            elemlist = self.setlist[setname]['items']
            req = self.retrive_node_elemlist(elemlist)
        else:
            req = None
            
        return req        
        
        
    def retrive_node_elemlist(self,elemlist):
        conn = []
        for elemid in elemlist:
            conn.append(self.retrive_node_elemid(elemid))
        return conn
    
    def retrive_node_elemid(self,elemid):
        seq = self.conndict[elemid]
        nnode = self.conntable[seq][2]
        conn = self.conntable[seq][3:nnode+3]
        
        return conn
    
    
    def retrive_elem_set_coord(self,setname,average=True):
        if setname in self.setlist.keys():
            elemlist = self.setlist[setname]['items']
            req = self.retrive_elem_list_coord(elemlist,average=average)
            
        else:
            req = None
            
        return req
    
    def retrive_elem_list_coord(self,elemlist,average=True):
        ''' retrive the element position by average the coordinates of all nodes within element
            if average is false, then export the node coordinate list
        
        '''
        
        nodelist1 = self.retrive_node_elemlist(elemlist)
        xyzlist = []
        
        for nodes in nodelist1:
            xyz = np.array(self.retrive_node_list_coord(nodes))
            
            if average:
                xyz = np.average(xyz, axis=0)
            
            xyzlist.append(xyz)    
        
        return np.array(xyzlist)
        
    
    def retrive_node_set_coord(self,setname):
        if setname in self.setlist.keys():
            nodelist = self.setlist[setname]['items']
            req = self.retrive_node_list_coord(nodelist)
        else:
            req = None
            
        return req     
    
    def retrive_node_list_coord(self,nodelist):
        xyz = []
        for nodeid in nodelist:
            xyz.append(self.retrive_node_single_coord(nodeid))
        return xyz   
    
    def retrive_node_single_coord(self,nodeid):
        seq = self.coorddict[nodeid]
        xyz = self.coordtable[seq][1:4]
        
        return xyz
        
        
    #============== The final group of aggregrate post process ========
    
    def nodalset_force(self,setname,postcode='z'):
        req = self.post_history_node_set(setname,'Reaction Force',postcode=postcode,incr='ALL',sum=False)
        #np.savetxt("temp1.txt", req[0], delimiter="\t") 
        loadx = np.sum(req, axis=2).T
        #np.savetxt("temp2.txt", loadx, delimiter="\t")
        return loadx
    
if __name__ == '__main__':
    res = marc_t19('model1_job1.t19')
    res.decomposedict()
    res.process()
    
    print len(res.segments[5]['52300']['contentlines'])
    print res.ne
    print res.ninterp
    print res.conntable
    print res.nepost
    print res.connposttable
    
    res.generate_post_vector()
    
    
    #print res.segments[5]
    print 1