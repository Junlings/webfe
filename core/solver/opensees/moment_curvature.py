import os.path
import sys
sys.path.append('../../export')

from export.export import exporter
from opensees import run_OpenSees, run_OpenSees_interact
folder = os.path.dirname(os.path.realpath(__file__))
import shutil

def moment_curvature(model,secname,axialLoad,maxK,numIncr=100,prjname=None,recorderfiber=None):
    """ triger a sectional moment curvature analysis for certain layered section
    in the model defination"""
    
    # copy all required files
    shutil.copy2(os.path.join(folder,'MomentCurvature_recorder.tcl'),'source')
    shutil.copy2(os.path.join(folder,'LibUnits.tcl'),'source')
    
    # read main control file
    f1 = open(os.path.join(folder,'MomentCurvature_main.tcl'),'r')
    text = f1.read()
    
    
    # get material and section export string
    exp1 = exporter(model,'opensees.txt','ex_OpenSees')
    sec = model.seclist[secname]
    exportsec = 'set %s 1\n' % secname
    exportsec += exp1.write_sec(secname)
    
    matlist = model.get_material_by_section(secname)
    exportmat = ''
    nmat = 1
    for matname in matlist:
        exportmat += 'set %s %i\n' % (matname,nmat)
        exportmat += exp1.write_mat(matname)
        nmat +=1
    
    # get recorder string if needed
    if recorderfiber != None:
        exportrecorder = ''
        for fibertag in recorderfiber:
            fiber = sec.fiber[fibertag]
            exp2 = 'recorder Element -file $dataDir/%(path)s -time -ele 2001 section fiber %(locy)s 0 $%(mattag)s stressStrain\n' % ({
                'path':fibertag,
                'locy':fiber.locy,
                'mattag':fiber.mattag,}
            )
            exportrecorder += exp2
    
    else:
        exportrecorder = ''
    
    
    
    output = text % {'exportmats':exportmat,'exportsec':exportsec,'axialLoad':axialLoad,'sectag':secname,
                     'maxK':maxK,'numIncr':numIncr,'prjname':prjname,'exportrecorder':exportrecorder}
    
        
    # generate source file name
    if prjname == None:
        sourcefile = 'moment_curvature'+secname +'.tcl'
    else:
        sourcefile = prjname + '.tcl'
    sourcefilepath = os.path.join('source',sourcefile)


    
    # write source file to working folder
    if not os.path.exists('source'):
        os.makedirs('source')
    f1 = open(sourcefilepath,'w')
    f1.write(output)
    f1.close()
    
    # call external opensees program
    run_OpenSees(sourcefile)
    #run_OpenSees_interact(sourcefile,loop)
    return 1