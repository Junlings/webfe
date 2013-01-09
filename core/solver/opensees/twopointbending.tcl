#--------------------------------------------------------------------------------
#

#setup---------------------------------------------------------------------------
wipe;
model BasicBuilder -ndm 2 -ndf 3;
file mkdir data;
#

#start to define grid-------------------------------------------------------------
%(exportnodes)s

#start to define material -----------------------------------------------
%(exportmats)s

#start to define element-------------------------------------------------------------
%(exportsecs)s

%(exportelems)s

#start to define transformation -------------------------------------------------------------
geomTransf Linear 1


#start to define boundary %i-------------------------------------------------------------
%(exportbounds)s
#

#start to define load pattern-1-----------------------------------------------------------
%(exportloads)s
#

%(exportrecords)s

%(exportanalysis)s
