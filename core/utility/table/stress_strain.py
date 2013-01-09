import numpy as np

def add_mat_by_stressstrain(model1,matname,stressstrainpoints,elastic_strain_limit):
    
    # create elastic model
    matlib = stress_strain(stressstrainpoints,elastic_strain_limit)
    
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
