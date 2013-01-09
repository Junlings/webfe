"""
This is the module to read the *.t16 results geneted by the marc
"""
import sys
#from math import *
import numpy as np
#from py_post import *  # now the python connection has not been setup yet
import time
from py_post import *

class post_t16:
    """
    class to extract the results from t16 result file based on the provided
    py API files
    work with python 2.5, and change the numerical data type to numpy array
    Function list:
    
    post_t16(t16file)   usage   :create the postprocess class
                           inputs  :*.t16 file
    
    disp_node_all()     usage   :display all exist nodes
                           inputs  :None
    
    disp_element_all()  usage   :display all exist elements
                           inputs  :None

    disp_sets()         usage   :display all exist sets name
                           inputs  :None
    
     disp_element_scalar() usage   :display all exist element scalar
                           inputs  :None
    
     disp_node_scalar()    usage   :display all exist node scalar
                           inputs  :None

     index_node_scalar(str1)   usage   :Find internal node scalar id from name
                              inputs  :Node Scalar name

     index_element_scalar(str1)  usage   :Find internal element scalar id from name
                                inputs  :Element scalar name

     index_set(str1)           usage   :Fina internal set id from name
                              inputs  :Set name

     getset_content(setseq)      usage   :get set content list, node or element
                                 inputs  :set internal ID
                                 output  :node or element list from certain set
    
     getdata_node_scalar(node_id,scalar_seq)            usage   :get node scalar value
                                                        inputs  :node id and scalar id
                                                        output  :scalar value of specify node at current increment
    
     getdata_element_scalar(element_id,scalar_seq,node_insideseq)       usage   :get element scalar at certain inside node 
                                                                        inputs  :element id, scalar id, inside node number 
                                                                        output  :scalar value of specify node from element at current increment
    
     select_node_coord(criterion)       usage   : get node list from coordinates ranges
                                        inputs  : [xmin,xmax,ymin,ymax,zmin,zmax]
                                        outpus  : node list

      select_element_node(nodeid)       usage   :select all element that contain the node 
                                        inputs  :node id 
                                        output  : element list      

     loadsetfile(setfile)               usage   : load the setting file
                                        inputs  : setting file name
    
    
     postset1(req,ninc)                 usage   : get the results based on the request str1ing
                                        inputs  : request str1ing, [start increment, end increment, increment step]
    
    
     postset2(setfile,outfile,ninc)     usage   : batch operation of results extraction based on setting file
                                        inputs  : setting file name, outputfile name, [start increment, end increment, increment step]
                                        outputs : results will be stored in the outfile
    
    """
    
    def __init__(self,t16file):
        self.p = post_open(t16file)
        """ try if the file is successfully readed"""
        self.ptime = 0
        self.nodescalarlib = {}
        self.elemscalarlib = {}
        self.setlib = {}
        self.ninc = [0,10000,1]
        try:
            self.p.moveto(1)
            self.increment = self.p.increments()
        except:
            print "Error opening post file:",t16file
            
        
        # obtain the scalar results dictionary
        self.disp_element_scalar()
        self.disp_node_scalar()
        #self.disp_increment_str()
        self.increment_str = []
    def disp_increment_str(self):
        
        for i in range(0,self.increment):
            self.p.moveto(i)
            self.increment_str.append('Incr %i:%3.3f' % (i,self.p.time))
    
    
    def incr(self,incr):
        ## this is the part where the time consuming is
        start_time = time.clock()
        self.p.moveto(incr)  # move to the next time increment
        self.ptime += time.clock() - start_time
        print self.ptime
    
    
    #======================Display function group============
    def disp_node_all(self):
        
        nn = self.p.nodes()  # total nodes 
        row = nn
        column = 5
        headdata = ["Node seq","node id","node_X","node_Y","node_Z"]
        resdata = [[0]*column for i in range(row)]
        
        for i in range(0,nn):
            nod = self.p.node(i)
            resdata[i][0] = i
            resdata[i][1] = nod.id
            resdata[i][2] = nod.x
            resdata[i][3] = nod.y
            resdata[i][4] = nod.z
        
        # change to numpy type
        resdata = np.array(resdata)
        return headdata,resdata
    
    def disp_element_all(self):
        """ Now support up to 4 nodes element """
        ne = self.p.elements()  # get total element number
            
        row = ne
        column = 10
        headdata = ["Element seq","Element id","node_Seq_1","node_Seq_2",
                    "node_Seq_3","node_Seq_4","node_Seq_5","node_Seq_6",
                    "node_Seq_7","node_Seq_8"]
        
        resdata=[[0]*column for i in range(row)]
        
        for i in range(0,ne):
            ele = self.p.element(i)
            resdata[i][0] = i
            resdata[i][1] = self.p.element_id(i)
            
            if ele.len==2:  # two node element
                resdata[i][2]=(ele.items[0])
                resdata[i][3]=(ele.items[1])
            if ele.len==4:  # four node element
                resdata[i][2]=(ele.items[0])
                resdata[i][3]=(ele.items[1])
                resdata[i][4]=(ele.items[2])
                resdata[i][5]=(ele.items[3])
            if ele.len==8:  # four node element
                resdata[i][2]=(ele.items[0])
                resdata[i][3]=(ele.items[1])
                resdata[i][4]=(ele.items[2])
                resdata[i][5]=(ele.items[3])
                resdata[i][6]=(ele.items[4])
                resdata[i][7]=(ele.items[5])
                resdata[i][8]=(ele.items[6])
                resdata[i][9]=(ele.items[7])
        
        resdata = np.array(resdata)  
        return headdata,resdata
    
    def disp_set(self):
        nset=self.p.sets()  # get total set number
        
        resdata=[]
        
        for i in range(0,nset):
            s=self.p.set(i)
            resdata.append(s.name)
            self.setlib[s] = i
        return resdata
    
    def disp_element_scalar(self):
        """
        Get the element scalar result
        """
        self.p.moveto(1)
        ners=self.p.element_scalars()
        row=ners
        column=2
        resdata=[]
    
        for i in range (0,ners):
            s=self.p.element_scalar_label(i)
            resdata.append(s)
            self.elemscalarlib[s] = i
        return resdata
    
    
    def disp_node_scalar(self):
        nnrs=self.p.node_scalars()
        row=nnrs
        column=2
        resdata=[]
        
        for i in range (0,nnrs):
            s=self.p.node_scalar_label(i)
            resdata.append(s)
            self.nodescalarlib[s] = i
        return resdata  
    

    #======================index function group================================
    def index_node_scalar(self,str1):
        """ findout the index of certain node scalar """
        index = self.disp_node_scalar().index(str1)
        return index
    
    def index_element_scalar(self,str1):
        """ find index of certain element scalar """
        index=self.disp_element_scalar().index(str1)
        return index
 
    def index_set(self,str1):
        """ Find the index of certail set"""
        index=self.disp_set().index(str1)
        return index
        

    def index_coord(self,nodeID):
        """ Get the coordinates of certain node ID """
        nod = self.p.node(self.p.node_sequence(nodeID))
        return [nod.x,nod.y,nod.z]
        
        
    
    #======================set function group================================
    def getset_content(self,setseq):
        """ Obtain the content of certain set, nodes or elements """
        s=self.p.set(setseq)
        
        resdata=[]
        if s.type=='node':
            for i in range(0,s.len):
                resdata.append(s.item[i])    
        elif s.type=='element':
            for i in range(0,s.len):
                resdata.append(s.item[i])
                
        resdata = np.array(resdata) # change to numpy type
        return s.type,resdata
    
    

    #=============getdata function group================================

    def getdata_node_scalar(self,node_id,scalar_seq):
        """ Obtain the node scalar results based on the node_id """
    
        node_seq = self.p.node_sequence(node_id)

        #start_time = time.clock()
        resdata = self.p.node_scalar(node_seq,scalar_seq)
        #self.ptime += time.clock() - start_time
        #print self.ptime

        return resdata
    
    def getdata_element_scalar(self,element_id,scalar_seq,node_insideseq):
        """
        Find the element scalar based on the current increment
        using element seq and node seq,scalar seq
        """
        element_seq = self.p.element_sequence(element_id)
        slist = self.p.element_scalar(element_seq,scalar_seq)
        if node_insideseq == -1: # element value
            resdata = slist.value
        elif node_insideseq >= 0: # integration point value
            resdata = slist[node_insideseq].value
        return resdata
    

    #======================select function group================================       
    def select_node_coord(self,criterion):  
        """ input coordinats and output id """
        nn = self.p.nodes()
        nodelist = []
            
        for i in range(0,nn):
            nod = self.p.node(i)
            err = 0.00001                 # error for selection
            a0 = (nod.x >= criterion[0] - err)
            a1 = (nod.x <= criterion[1] + err)
            a2 = (nod.y >= criterion[2] - err)
            a3 = (nod.y <= criterion[3] + err)
            a4 = (nod.z >= criterion[4] - err)
            a5 = (nod.z <= criterion[5] + err)
                
            if (a0 * a1 * a2 * a3 * a4 * a5 == 0):
                continue
            else:
                nodelist.append(self.p.node_id(i))
        nodelist = np.array(nodelist)
        return nodelist
    
    

    def select_element_node(self,node_id):  
        """ Find the element contain the node and identify the node sequence """
        ne = self.p.elements()
        ele_seq_list = []
        ele_seq_posi =[ ]
        
        for i in range(0,ne):
            ele = self.p.element(i)
            ecount = ele.item.count(node_id)
            if ecount>0:
                posi = ele.item.index(node_id)  # the node list
                                                # start from the third item  
                
                if posi >= 0:
                    ele_seq_posi.append(posi)
                    ele_seq_list.append(self.p.element_id(i))
        
        return [ele_seq_list,ele_seq_posi]
        
    
    

    def postset_incr(self,req):
        """
        Get results based on the request sequence and time increment range
        """
        res = []
        labellist = []
        reqtype = req[0]


        
        
        if reqtype=='Node Scalar': # nodal scalar results
            
            reqitem = req[2:-3]
            reqcontent = req[1]
            itemlist = []
            
            if len(reqitem) == 1:
                try:
                    settype,itemlist=self.getset_content(reqitem)  # setname input
                except:
                    itemlist = reqitem                           # single input
            else:
                itemlist = reqitem                                 # list input


            for nodeid in itemlist:
                res.append(self.getdata_node_scalar(int(nodeid),self.nodescalarlib[reqcontent]))
                
            labellist = ['Node_'+str(item) for item in itemlist]


        elif reqtype=='Element Scalar': # element scalar

            reqitem = req[3:-3]
            reqcontent = req[1]
            elemnodeid = req[2]

            if len(reqitem) == 1:
                try:
                    settype,itemlist=self.getset_content(reqitem)  # setname input
                except:
                    itemlist = reqitem                           # single input
            else:
                itemlist = reqitem                                 # list input


            for elemid in itemlist:
                res.append(self.getdata_element_scalar(int(elemid),self.elemscalarlib[reqcontent],int(elemnodeid)))

            labellist = ['Elem_'+str(item)+ '-'+str(elemnodeid) for item in itemlist]
            
        elif req[0]=='Time': # get analysis time
            
            res.append(self.p.time * float(req[1]))
            labellist = ['time']
        
        elif req[0]==None:
            print "req type do not understand"
            raise TypeError
        else:
            pass
        res = np.array(res)
        return res,labellist

    
    
    def postset1(self,req,ninc=None):
        """
        Get results based on the request sequence and time increment range
        """
        array_result=[[] for i in range(len(req))]    
        
        if ninc == None:
            ninc = self.ninc
        # decide the increment        
        if ninc[0] < 0:
            ## start increment number should greater than 0
            print "number of incrment should >0"
            return -1
        
        if ninc[1] > (self.increment-1):
            ## finish increment number should less than maximum increment number
            str1 = "exceed maximum increment number,"
            str1 += "automatically change to maximum increment %i" % (
                                                    self.increment-1)
            print str1
            ninc[1] = (self.increment-1) 
        
        if ninc[1] == -1:
            ## if finish increment equal to -1, use all increments
            ninc[1]=(self.increment-1)
            ninc[0]=1
            
        if len(ninc)==2:
            ## if no increment step given , use default 1
            ninc.append(1)
        
        # start to loop over the desinated increments
        for i in range(ninc[0],ninc[1],ninc[2]):
            self.incr(i+1)             # increment result file
            
            s_time='%g' % self.p.time  # get analysis file
            print 'Now extracting results at time step:'+s_time+'\n'
            for j in range(0,len(req)):
                if req[j][0]=='ns': # nodal scalar results
                    #['ns',nodeid,scalar seq]
                    array_result[j].append(self.getdata_node_scalar(
                                                      req[j][1],req[j][2]))
                elif req[j][0]=='es': # element scalar
                    #['es',elemeid,nodeside,scalarid]
                    array_result[j].append(self.getdata_element_scalar(
                                              req[j][1],req[j][3],req[j][2]))
                elif req[j][0]=='set': # results of certain set
                    type,items=self.getset_content(req[j][1])
                    res=[]
                    if type=='node': # node scalar
                        for k in range(0,len(items)):
                            res.append(self.getdata_node_scalar(
                                items[k],req[j][2]))
                            
                    elif type=='element': # element scalar
                        for k in range(0,len(items)):
                            res.append(self.getdata_element_scalar(
                                items[k],req[j][3],req[j][2]))
                    array_result[j].append(res)
                            
                elif req[j][0]=='time': # get analysis time
                    #['time',factor]
                    array_result[j].append(self.p.time*float(req[j][1]))
                
                elif req[j][0]==None:
                    print "req type do not understand"
                    raise TypeError
                else:
                    pass
        array_result = np.array(array_result)
        print 'total pypost module time is:' +str(self.ptime)
        return array_result
    
    
    def postset3(self,recorder):
        """
        postset3 was defined working with the new recorder instance
        """

        reqlist = []
        for reqitem in recorder.reqlist:  # loop over request list
            if reqitem.type == 'time':
                reqlist.append(['time',reqitem.factor])
            elif reqitem.type == 'ns':
                # get scalar id
                scalar_seq = self.index_node_scalar(reqitem.label)
                # loop for all in reqitem.entry
                for nodeid in reqitem.entry:
                    reqlist.append(['ns',nodeid,scalar_seq])
                    
            elif reqitem.type == 'es':
                # get scalar id
                scalar_seq = self.index_node_scalar(reqitem.label)
                for elemid in reqitem.entry:
                    elemid,nodeinsider = elemid.split(':')
                    reqlist.append(['es',elemid,nodeinsider,scalar_seq])
            else:
                print 'recorder type"' + reqitem.type +'" not defined yet\n'
                print "check extract_marc_t16.py"
                raise KeyError
        
        
        return self.postset1(reqlist,recorder.ninc)
    
    
    def postset_dict(self,results):
        """
        postset3 was defined working with the new wxpython GUI command settings
        """
        self.results = results

        reqdict = self.results.source['marc_t16']['request']
        resdict = {}
        for incr in range(0,self.increment):
            self.p.moveto(incr)
            
            for key,item in reqdict.items():
                #print item
                if key in resdict.keys():
                    data,labellist = self.postset_incr(item)
                    resdict[key]['data'] = np.vstack((resdict[key]['data'],data))
                    resdict[key]['labellist'] = labellist
                else:
                    resdict[key] = {}
                    resdict[key]['data'] = self.postset_incr(item)
                    resdict[key]['labellist'] = []
        
        for key,item in reqdict.items():
            self.results.add(key,resdict[key]['data'][2:,:],labellist=resdict[key]['labellist'],unitlist = ['N/A'] * len(labellist))
        
    '''
    The following commented out function is for future file communication 
    def postset2(self,setfile,outfile,ninc,exporttype,unitfile='No'):
        """
        A more versail extract function including adding the units and
        specify the export results
        """
        
        # get request sequence from reading the setting files
        seq1=self.loadsetfile(setfile)
        
        # get the results
        res=self.postset1(seq1,ninc)
        
        # get labels and unit  from setting files
        label,unit=self.getlabel(setfile,unitfile)  

    
        # apply label to res
        f2=open(outfile, 'w')


        
        if exporttype=='pydat':  #### export as pydat format using pickling modulus
            pickle.dump([label,unit,res], f2)
            
        elif exporttype=='csv':  #### export as csv file format that could be used by excel and KaleidaGraph
            lmax=0
            for i in range(0,len(res)):
                if len(res[i])>lmax:
                    lmax=len(res[i])

 
            for j in range(0,len(label)):   ###write label
                temp='%s' % label[j] 
                f2.write(temp+',')
            f2.write('\n')

            for j in range(0,len(unit)):  ###write unit
                temp='%s' % unit[j] 
                f2.write(temp+',')
            f2.write('\n')
            
            
            for i in range(0,lmax):
                for j in range(0,len(res)):
                    if len(res[j])>i:
                        if res[j][i]!=None:
                            #print res[j][i]
                            temp='%f' % res[j][i]
                        else:
                            temp=''
                    else:
                        temp=''
                    f2.write(temp+',')
                f2.write('\n')
        else:
            print 'no predefined export file type'
    
        f2.close()
        
    def getlabel(self,setfile,unitfile='No'):
        """
        Get the last item in the setting file as the label for export purpose
        Set file format
        """
        f2 = open(setfile,'r')
        label = []
        unit = []
        while(1):
            str1 = f2.readline()
            if len(str1)==0:
                break
            else:
                str1=str1.split(',')  # cvs file with ',' as spliter
                
                if str1[len(str1)-1]!=' ':
                    if unitfile=='yes':
                        unit_str1=str1[len(str1)-1]
                        label_str1=str1[len(str1)-2]
                    else:
                        label_str1=str1[len(str1)-1]
                else:
                    if unitfile=='yes':
                        unit_str1=str1[len(str1)-2]
                        label_str1=str1[len(str1)-3]
                    else:
                        label_str1=str1[len(str1)-2]
                
                if label_str1[len(label_str1)-1]!='\n':
                    label.append(label_str1)
                else:
                    label.append(label_str1[0:len(label_str1)-1])
                    
                if unitfile=='yes':
                    if unit_str1[len(unit_str1)-1]!='\n':
                        unit.append(unit_str1)
                    else:
                        unit.append(unit_str1[0:len(unit_str1)-1])
                else:
                    unit.append(None)
                    
        return label,unit
        
    def loadsetfile(self,setfile):
        f2=open(setfile,'r')
        req=[]
            
        while(1):
            str1=f2.readline()
            if len(str1)==0:
                break
            else:
                str1=str1.split(',')
                if str1[0]=='ns':
                    req.append([str1[0],str1ing.atoi(str1[1]),self.index_node_scalar(str1[2])])
                elif str1[0]=='es':
                    req.append([str1[0],str1ing.atoi(str1[1]),str1ing.atoi(str1[2]),self.index_element_scalar(str1[3])])
                elif str1[0]=='set':
                    req.append([str1[0],self.index_set(str1[1]),self.index_node_scalar(str1[2]),str1[3]])
                elif str1[0]=='time':
                    req.append([str1[0],str1[1]])
                else:
                    print 'no predefined keywords'+req[0]
        return req
    
    '''
    
if __name__ == '__main__':
    import py_post
    for key,item in py_post.__dict__.items():
        print item