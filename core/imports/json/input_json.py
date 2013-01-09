from model.registry import model
from export.export import exporter
import numpy as np
from settings import settings
import json


class model_json():
    """ class to create model via json """ 
    def __init__(self,jsonfile):
        # open json input file
        self.jsonfile = open(jsonfile,'r')
        # load json data
        self.data = json.load(self.jsonfile)
        # update default settings
        self.settings = settings.update(self.data['settings'])
        # create models
        self.model = model(self.settings)
    
    def decoder(self,jsoninput):
        jsonfile = open(jsoninput,'r')
        data = json.load(jsonfile)
        return data
        
    def build_nodes(self,inputnodes):
        self.model.node(inputnodes)
        
    def build_conn(self,inputconn):
        self.model.element(inputconn)
        
    def build_mat(self,inputmat):
        for key in inputmat.keys():
            mattype = inputmat[key]['type']
            prop = inputmat[key]['prop']
            self.model.material(key,mattype,prop)
    
    def build_sec(self,inputsec):
        for key in inputsec.keys():
            sectype = inputsec[key]['type']
            prop = inputsec[key]['prop']
            self.model.section(key,sectype,prop)
            
    def build_orient(self,inputorient):
        for key in inputorient.keys():
            orienttype = inputorient[key]['type']
            prop = inputorient[key]['prop']
            self.model.orient(key,orienttype,prop)        
        
        
    def build(self,target,inputdict):
        if target == 'node':
            self.build_nodes(inputdict)
            
        elif target == 'element':
            self.build_conn(inputdict)
            
        elif target == 'material':
            self.build_mat(inputdict)
        
        elif target == 'section':
            self.build_sec(inputdict)

        elif target == 'orient':
            self.build_orient(inputdict)
            
    def build_all(self):
        for key in self.data['model'].keys():
            self.build(key,self.data['model'][key])
        
if __name__ == '__main__':
    
    join1 = model_json('input.txt')
    
    join1.build_all()
    print 1