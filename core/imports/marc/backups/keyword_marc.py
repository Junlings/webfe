##### Define the keyword used in Marc, so the model writen in *.dat file could be exported to other platform.

##### The hiararathy of the list############## 
#####  ALLlist-
#             Genelist
#                     title
#                     sizing,extended,elements                      
#             Gridlist   
#                     coordinates

#             Program   
#             Elemlist--
#                     ElEm1dlist
#                     ElEm2dlist.
#                     ElEm3dlist
#             Proplist
#                     Prop1dlist
#                     Prop2dlist
#                     Prop3dlist
#             Matelist
#             Bondlist
#             Loadlist
#
#
#             Loadcaselist
#             Analysislist
#

########### Initial the ALList disctionary
from keyline import keylines

coordinates = {1:['5%i', '5%i', '5%i', '5%i',1],
               2:['5%i','10%f','10%f','10%f',2],
               'repeat':[2]}




ALLlist=dict
ALLlist={'Gridlist':['coordinates']}
ALLlist['Elemlist']=['connectivity']
ALLlist['Genelist']=['title','sizing','extended','elements']
ALLlist['Program']=['allco','version','feature','processor','define']
ALLlist['Loadlist']=[]
ALLlist['Bondlist']=['fixed']
ALLlist['Proplist']=[]
ALLlist['Proplist']=['damping']
ALLlist['Matelist']=['isotropic','crack','work']
ALLlist['Loadcaselist']=[]
ALLlist['Analysislist']=['dynamic']

########### Initial the ALList 'ALL' tage
ALLlist['ALL']=[]
ALLlist['ALL'].extend(ALLlist['Gridlist'])
ALLlist['ALL'].extend(ALLlist['Elemlist'])
ALLlist['ALL'].extend(ALLlist['Genelist'])
ALLlist['ALL'].extend(ALLlist['Program'])
ALLlist['ALL'].extend(ALLlist['Loadlist'])
ALLlist['ALL'].extend(ALLlist['Bondlist'])
ALLlist['ALL'].extend(ALLlist['Proplist'])
ALLlist['ALL'].extend(ALLlist['Matelist'])
ALLlist['ALL'].extend(ALLlist['Loadcaselist'])
ALLlist['ALL'].extend(ALLlist['Analysislist'])

#print ALLlist['ALL']

#####################Start define the keyword format####################
##################### refer to Marc user manel volume C program input for details
##########format list########
''' 's'   array
    'i'   integral
    'f'   float
    'i/s' integral or array
    'f/s' float or array
    None  Not used 





'''



######Define the grid keyword format


gridstyle=[[[12],['s']]]                                                   ### Line 1
gridstyle.append([[5,5,5],['i','i','i']])                                  ### Line 2
gridstyle.append([[5,5,5,5],['i','i','i','i']])                            ### Line 3
keywordstyle={'connectivity':gridstyle}


coordstyle=[[[11],['s']]]                                                  ### Line 1
coordstyle.append([[5,5,5,5],['i','i','i','i']])                           ### Line 1
coordstyle.append([[5,10,10,10,10],['i','f','f','f','f']])                 ### Line 1
keywordstyle['coordinates']=coordstyle

fixdispstyle=[[[10],['s']]]
fixdispstyle.append([[5,5],['i','i']])
fixdispstyle.append([[5,5],['i','i']])

######Define the material keyword format
matstyle=[[[9],['s']]]                                                                    ### Line 1
matstyle.append([[5,5],['i','i']])                                                        ### Line 2
matstyle.append([[5,10,10,5,5,5,5,10],['i','s','s','i','i','i','i','s']])                 ### Line 3
matstyle.append([[10,10,10,10,10,10,10,10],['f','f','f','f','f','f','f','f']])            ### Line 4 
#matstyle.append([[5,5,5,5,5,5],['i','i','i','i','i','i']])                                ### Line 5
matstyle.append([[6,6,6,6,6,6],['i','to/i','i','i','i','i']]) 
keywordstyle['isotropic']=matstyle
