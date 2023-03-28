"""
The function in this module get 3 dicitionary and return 2 numpy array
    
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

def CellularAutomata(seedDict,nghAddressDict):
    
    #framesRatio,niter,K,gridSize = auxVars.values()
    framesSimulation = [] 
    dataSimulation = []
    t = 1
    for loop in range(niter):
        
        listOfCells = list(seedDict.values())
        random.shuffle(listOfCells)
        for cellsLine in listOfCells:
            cellsLine.updateBooleanNetwork1(seedDict)
            #cellsLine.updateBooleanNetwork2(seedDict)
            cellsLine.updateTumorGrowthKinetics(seedDict,nghAddressDict)
            
        Lattice = np.zeros((squareSide,squareSide))
        for cellsLine in seedDict.values():
            Lattice[cellsLine.index] = cellsLine.id_number
            
        if (loop % deltaI) == 0:
            
            skmelProlif = len([p for p in listOfCells if p.id_number == 1 and p.proliferate == True])
            skmelDeath = len([p for p in listOfCells if p.id_number == 1 and p.death == True])
            skmelMig = len([p for p in listOfCells if p.id_number == 1 and p.migrate == True])
            hacatProlif = len([p for p in listOfCells if p.id_number == 2 and p.proliferate == True])
            hacatDeath = len([p for p in listOfCells if p.id_number == 2 and p.death == True])
            hacatMig = len([p for p in listOfCells if p.id_number == 2 and p.migrate == True])
            dataSimulation.append([len(Lattice[Lattice == 1])/K,
                                   len(Lattice[Lattice == 2])/K,
                                   t,
                                   (len(Lattice[Lattice == 2])/len(Lattice[Lattice == 1])),
                                   (skmelProlif/(skmelProlif+skmelDeath+skmelMig)),
                                   (skmelDeath/(skmelProlif+skmelDeath+skmelMig)),
                                   (skmelMig/(skmelProlif+skmelDeath+skmelMig)),
                                   (hacatProlif/(hacatProlif+hacatDeath+hacatMig)),
                                   (hacatDeath/(hacatProlif+hacatDeath+hacatMig)),
                                   (hacatMig/(hacatProlif+hacatDeath+hacatMig))])
                
            framesSimulation.append(Lattice)
            t = t + 1 
            
    return np.array(dataSimulation),np.array(framesSimulation)