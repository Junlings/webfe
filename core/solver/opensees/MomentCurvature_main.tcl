wipe;				# clear memory of all past model definitions
model BasicBuilder -ndm 2 -ndf 3;	# Define the model builder, ndm=#dimension, ndf=#dofs
set dataDir Data/%(prjname)s/;				# set up name of data directory (you can remove this)
file mkdir $dataDir; 				# create data directory

source source/LibUnits.tcl;             # define units
source source/MomentCurvature_recorder.tcl;             # define units


## Insert material defination
%(exportmats)s
%(exportsec)s


  
	# Create recorder
recorder Node -file $dataDir/mc -time -node 1002 -dof 3 disp;	# output moment (col 1) & curvature (col 2)
	%(exportrecorder)s

puts "Modeling done"
MomentCurvature_recorder $%(sectag)s %(axialLoad)s %(maxK)s %(numIncr)s