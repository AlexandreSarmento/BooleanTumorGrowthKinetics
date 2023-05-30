"""
The function in this module get 2 dicitionary and return 2 numpy array
    
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
"""

import numpy as np      
import random
from settingInput import squareSide,niter,deltaI,K
import neighbors

def CellularAutomata(seedDict,nghAddressDict):
    
    framesSimulation = [] 
    dataSimulation = []
    #t = 0
    for loop in range(0,niter):
        
        listOfCells = list(seedDict.values())
        random.shuffle(listOfCells)
        for cellsLine in listOfCells:
            cellsLine.updateBooleanNetwork(seedDict,loop)
            cellsLine.updateTumorGrowthKinetics(seedDict,nghAddressDict)
            
        Lattice = np.zeros((squareSide,squareSide))
        for cellsLine in seedDict.values():
            Lattice[cellsLine.index] = cellsLine.id_number
            
        if (loop % deltaI) == 0:
            
            [Ps,Ds,Ms,Ss,Ph,Dh,Mh,Sh] = neighbors.updateKineticsProbability(listOfCells)
            dataSimulation.append([
                                   len(Lattice[Lattice == 1])/K,
                                   len(Lattice[Lattice == 2])/K,
                                   len(Lattice[Lattice != 0])/K,
                                   loop,
                                   Ps,Ds,Ms,Ss,Ph,Dh,Mh,Sh
                                   ])
                                   
                
            framesSimulation.append(Lattice)
            #t += (1/(Ps+Ds+Ms+Ss+Ph+Dh+Mh+Sh)) #+ (1/(Ph+Dh+Mh+Sh)) 
            
    return np.array(dataSimulation),np.array(framesSimulation)