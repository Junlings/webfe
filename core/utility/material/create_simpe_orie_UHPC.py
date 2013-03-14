""" This is the module to create the UHPC uniaxial ECC type material in modified opensees with """


def create_simpe_orie_UHPC(model1,matkey,sigt0,sigt1_0,factor=1.0):
    ''' create UHPC that consider the fiber orientation preference '''

    #sigt0 = sigt0

    #sigt1=1.5*ramda1
    sigt1 = sigt1_0 * factor
    sigt2 = sigt1 + 0.001
    
    epst0 = 0.000179  ## keep the strain the same
    epst1 = 0.004
    epst2 = 0.016
    epst3 = 0.016
            

    # compression properties  ## use treated material properties
    sigc0 = 28   # in unit of ksi
    epsc0 = 0.003286
    sigc1 = 28.1
    epsc1 = 0.004
    epsc2 = 0.01
    
    
    # parameter
    alphaT1 = 1
    alphaT2 = 1
    alphaT3 = 1
    alphaC = 1
    alphaC1 = 1
    alphaCU = 1
    betaT = 1
    betaC = 1
    
    model1.material(matkey,'uniaxial_UHPC',{
        'sigt0':sigt0,
        'epst0':epst0,
        'sigt1':sigt1,
        'epst1':epst1,
        'sigt2':sigt2,
        'epst2':epst2,
        'epst3':epst3,
        'epst0':epst0,
        'epsc0':epsc0,
        'sigc1':sigc1,
        'epsc1':epsc1,
        'epsc2':epsc2,
        'alphaT1':alphaT1,
        'alphaT2':alphaT2,
        'alphaT3':alphaT3,
        'alphaC':alphaC,
        'alphaC1':alphaC1,
        'alphaCU':alphaCU,
        'betaT':betaT,
        'betaC':betaC,
        })
    
    return model1
    


        