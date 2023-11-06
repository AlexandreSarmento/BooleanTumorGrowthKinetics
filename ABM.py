"""
The function in this module get 2 dicitionary and return 3 numpy array
    
dictionary
    seedDict: 
        key: initial vertex of each cell (tuple)
        value: instance of class
 
    nghAddressDict: 
        key: an specific vertex of domain (tuple)
        value: address of each neighbors of a given vertex (list of tuple)

numpy array
    dataSimulation: two-dimensional array where the columns represent a given data of the dynamic such density of cells
                    and the rows represent the value saved over iteration
    
    framesSimulation: three dimensional array which registrate the spatial dynamic of population over iterations 
    framesRhoMax: three dimensional array which registrate the spatial distribution of parameter rhoMax over iterations
    
"""

import numpy as np      
import random
from inputData import nRowCols,niter,K,deltaT
import models

def CellularAutomata(seedDict,nghAddressDict):
    
    t = 1
    framesSimulation = [] 
    dataSimulation = []
    preParamsFrames = [[-1]*nRowCols]*nRowCols
    paramsFrames = []
    for loop in range(niter):
        
        listOfCells = list(seedDict.values())
        random.shuffle(listOfCells)
        for cellsLine in listOfCells:
            cellsLine.updateBooleanNetwork(seedDict) 
            cellsLine.updateTumorGrowthKinetics(seedDict,nghAddressDict)
            
        
        Lattice = np.zeros((nRowCols,nRowCols))
        parameters = np.array(preParamsFrames)
        for cellsLine in seedDict.values():
            Lattice[cellsLine.index] = cellsLine.cellsID
            parameters[cellsLine.index] = cellsLine.rhoMax
            
        [Ps,Ds,Ms,Ss,Ph,Dh,Mh,Sh] = models.updateKineticsProbs(listOfCells)
        if (loop % 2) == 0:
            
            dataSimulation.append([len(Lattice[Lattice == 1])/K,
                                   len(Lattice[Lattice == 2])/K,
                                   len(Lattice[Lattice != 0])/K,
                                   t,
                                   Ps,Ds,Ms,Ss,
                                   Ph,Dh,Mh,Sh
                                 ])
            framesSimulation.append(Lattice)
            paramsFrames.append(parameters)
        
        else:
            pass
        
        t = t + deltaT
      
        
    return np.array(dataSimulation),np.array(framesSimulation),np.array(paramsFrames)
