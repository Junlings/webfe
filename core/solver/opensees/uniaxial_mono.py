import os.path
from export.export import exporter
from opensees import run_OpenSees, run_OpenSees_interact
folder = os.path.dirname(os.path.realpath(__file__))

def loop(step):
    if step < 10:
        return 'analyze 1 \n'
    else:
        return None
    

def uniaxial_mono(model,matname,strainincr,totalstep,prjname=None):
    
    # read analysis template file
    f1 = open(os.path.join(folder,'uniaxial_mono.tcl'),'r')
    text = f1.read()
    
    # get material export string
    exp1 = exporter(model,'opensees.txt','ex_OpenSees')
    mat = model.matlist[matname]
    exportdoc = exp1.write_mat(matname)
    
    # generate source file name
    if prjname == None:
        sourcefile = 'uniaxial_mono_'+matname +'.tcl'
    else:
        sourcefile = prjname + '.tcl'
    sourcefilepath = os.path.join('source',sourcefile)

    # Fill the template file 
    output = text % {'exportdoc':exportdoc,'mat.tag':matname,'strainincr':strainincr,
                     'totalstep':totalstep,'prjname':prjname}
    
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