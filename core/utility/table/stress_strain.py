import numpy as np
import csv

def add_mat_by_stressstrain(model1,matname,stressstrainpoints,elastic_strain_limit):
    ''' create material model by input stress and strain relations'''
    # create elastic model
    matlib = stress_strain(stressstrainpoints,elastic_strain_limit)
    
    # create table
    model1.table(matname,1,['eq_plastic_strain'],matlib['plastic_stress_strain'])
    model1.material(matname,'uniaxial_elastic_plastic',{'E':matlib['E'],'mu':0.3,'mass':0.0,
                                                        'sigma_y':matlib['sigma_y'],
                                                        'tabletag':matname})
    return model1

def search_proplimit(data,ratio=0.05):
    ''' search propotional limits with stiffness shift limits '''
    
    pass  # wait for implementation
    
def find_nearest(arrayx,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def find_nearestpair(arrayx,arrayy,value):
    idx = (np.abs(arrayx-value)).argmin()
    return arrayx[idx],arrayy[idx]

def add_mat_by_file(model1,matname,filename,mode,proplimit=None,propstrain=None,straincinr=0.0001):
    ''' read csv file , shall have two columns '''
    
    f1 = open(filename,'r')
    #matname = os.path.split(filename)[-1].split('.')[0]
    res = csv.reader(f1,delimiter=',')
    
    data = []
    for row in res:
        data.append(map(float,row))
    
    
    xmode,ymode=mode.split('|')
    
    # clean up the x column data
    if xmode == 'Ratio':
        pass  # already as stress ratio
    elif xmode == 'Value':
         # get propotional limits if not provided
        if proplimit == None:
            proplimit,propstrain = search_proplimit(data)  # search the propotional limits
        for iline in range(0,len(data)):
            data[iline][0] = data[iline][0]/float(proplimit)
    
    # clean up the y column data
    if ymode == 'Total Strain':
        if propstrain == None:
            proplimit,propstrain = search_proplimit(data)
            
        for iline in range(0,len(data)):
            data[iline][1] = data[iline][1]-float(propstrain)        
            if data[iline][1] <0 :
                data[iline][1] = 0
    
    # clean up data
    data = np.array(data)
    current_strain = 0
    cleaned_data = []
    max_strain = max(data[:,1])
    while 1:
        current_strain += straincinr
        if current_strain > max_strain:
            break
        strain,stress = find_nearestpair(data[:,1],data[:,0],current_strain)
        cleaned_data.append([strain,stress])
    
    
    matlib = {}
    matlib['plastic_stress_strain'] = cleaned_data
    matlib['E'] = float(proplimit)/float(propstrain)
    matlib['sigma_y'] = float(proplimit)
    
    # create table
    model1.table(matname,1,['eq_plastic_strain'],matlib['plastic_stress_strain'])
    model1.material(matname,'uniaxial_elastic_plastic',{'E':matlib['E'],'mu':0.3,'mass':0.0,
                                                        'sigma_y':matlib['sigma_y'],
                                                        'tabletag':matname})
    return model1



def stress_strain(stressstrainpoints,elastic_strain_limit):
    """ 
        convert the stress strain curve to the the marc style inputs
        input stressstrainpoint = [[strain1,stress1],[strain2,stress2],...[strainn,stressn]]
        elastic_strain_limit  = scalar of elastic strain limit
        
        with out put of
        E = elastic stress limit/elastic strrain limit
        fy = elastic stress limit (curve search and interpolate)
        plastic strain = []
        stress factor
    
    """
    stressstrainpoints = np.array(stressstrainpoints).T
    
    #print stressstrainpoints
    fy = np.interp(elastic_strain_limit,stressstrainpoints[0,:],stressstrainpoints[1,:])
    E = float(fy)/elastic_strain_limit
    plastic_stress_strain = [[0,1]]
    
    for i in range(0,stressstrainpoints.shape[1]):
        if stressstrainpoints[0,i] <= elastic_strain_limit:
            pass
        else:
            eq_plastic_strain = (stressstrainpoints[0,i]-elastic_strain_limit)  # convert one dimensional strain to equivalent plastic strain
            plastic_stress_strain.append([eq_plastic_strain,
                                          stressstrainpoints[1,i]/fy])
            
    
    return {'E':E,'sigma_y':fy,'plastic_stress_strain':plastic_stress_strain}

if __name__ == '__main__':
    
    ss = [[0,0],[0.01,60],[0.02,61],[0.05,70],[0.051,0]]
    es = 0.01
    
    print stress_strain(ss,es)

    print 1
