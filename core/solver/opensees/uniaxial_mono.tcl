#==================================================================================================
# This file serve as material verification in tension by
# using forcebeamcolumn element in opensees
# Replaceable parameters are
# (exportdoc)s:       material export documentation
# $(tag)s:  variable name as material tag name
# (strainincr)f  :   Strain increment
# (totalstep)i   :   total analyze steps 
#================================================================================================== 

 
wipe;				# clear memory of all past model definitions
model BasicBuilder -ndm 2 -ndf 3;	# Define the model builder, ndm=#dimension, ndf=#dofs
set dataDir Data;				# set up name of data directory (you can remove this)
file mkdir $dataDir; 				# create data directory

#source LibUnits.tcl;             # define units
 		


## Insert material defination
set %(mat.tag)s 1
%(exportdoc)s


set current_matID  $%(mat.tag)s		 
set current_secID 1

section fiberSec $current_secID {;
#     locy locx area mat
fiber 0     0     1   $current_matID
}
 
node 1 0 0
node 2 1 0

# Define nodal BOUNDARY CONDITIONS
fix 1 1 1 1
fix 2 0 1 1

pattern Plain 200 Linear {;			# define load pattern
			load 2 1 0 0
	}

puts "Whole Model Built"
# Define Beam-Column Elements
set np 3;	# number of Gauss integration points for nonlinear curvature distribution-- np=2 for linear distribution ok

# Define Beam-Column Elements
set geo_tranf $current_secID
geomTransf Linear $geo_tranf

element dispBeamColumn 1 1 2 $np $current_secID $geo_tranf;	


recorder Element -file $dataDir/%(prjname)s_stress_strain_force.out ¨Ctime -ele 1 section 1 fiber 0 0  stressStrain
recorder Node -file $dataDir/%(prjname)s_tension_force.out -time -node 2 -dof 1 disp;	
recorder plot $dataDir/%(prjname)s_tension_force.out uniaxialload 625 10 625 450 -columns 2 1

set disp 2
if { $disp == 1 } {   
   recorder display "material" 110 100 800 800
   prp 20 20 20
   vup 0 1 0
   vpn 0 0 1
   viewWindow -350 350 -350 350
   display 1 6 5

}


# Create the system of equation, a
system BandGeneral
# Create the DOF numberer,
numberer Plain
# Create the constraint handler, a Plain handler is used as homo constraints
constraints Plain
#constraints Lagrange
# Create the integration scheme, the LoadControl scheme using steps of 1.0
integrator DisplacementControl 2 1 %(strainincr)f
# test
test EnergyIncr  1.0e-8  200   1
# Create the solution algorithm, a Linear algorithm is created
algorithm ModifiedNewton
# create the analysis object 
analysis Static 


analyze %(totalstep)i
puts "Analysis finished"
