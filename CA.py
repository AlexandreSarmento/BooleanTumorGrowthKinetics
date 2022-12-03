# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 15:21:03 2022

@author: Alexandre Sarmento
"""
import numpy as np      
import math
#import cells   
#shuffle = np.random.shuffle
#randomChoice = random.choice

                
def ABM(auxVars,seedDict,nghAddressDict):
    
    framesRatio,niter,K,gridSize = auxVars.values()
    framesSimulation = [] # save the frame of dynamic simulation were we took a shot of dynamic
    dataSimulation = []
    count = int(1)
    
    for loop in range(1,niter):
        
        # at each iteraction we loop over all instances and call updateKinetic function
        #timeCount = t[loopSim-1]
        listOfCells = list(seedDict.values())
        #shuffle(listOfCells)
        for species in listOfCells:
            species.updateBooleanNetwork(seedDict)
            species.updateKinetics(seedDict,nghAddressDict)
            
        Lattice = np.zeros((gridSize,gridSize))
        for species in seedDict.values():
            Lattice[species.index] = species.id_number
            
        if loop == count:
            
            skmelProlif = len([p for p in listOfCells if p.id_number == 1 and p.proliferate == True])
            skmelDeath = len([p for p in listOfCells if p.id_number == 1 and p.death == True])
            skmelSurv = len([p for p in listOfCells if p.id_number == 1 and p.survive == True])
            hacatProlif = len([p for p in listOfCells if p.id_number == 2 and p.proliferate == True])
            hacatDeath = len([p for p in listOfCells if p.id_number == 2 and p.death == True])
            hacatSurv = len([p for p in listOfCells if p.id_number == 2 and p.survive == True])
            dataSimulation.append([len(Lattice[Lattice == 1])/K,
                                   len(Lattice[Lattice == 2])/K,
                                   loop,
                                   (len(Lattice[Lattice == 2])/len(Lattice[Lattice == 1])),
                                   (skmelProlif/(skmelProlif+skmelDeath+skmelSurv)),
                                   (skmelDeath/(skmelProlif+skmelDeath+skmelSurv)),
                                   (skmelSurv/(skmelProlif+skmelDeath+skmelSurv)),
                                   (hacatProlif/(hacatProlif+hacatDeath+hacatSurv)),
                                   (hacatDeath/(hacatProlif+hacatDeath+hacatSurv)),
                                   (hacatSurv/(hacatProlif+hacatDeath+hacatSurv))])
                        
            framesSimulation.append(Lattice)
            nn = round(math.log10(loop)) # nn: this an auxiliary parameter to record the smoothness of the curve we must to round the log10 of iteration.
            deltaLoop = math.ceil((10**(nn+1) - 10**(nn))/framesRatio) # delta_ii: this auxiliary variable calculate how much 
            # interation do we have to wait to record a new data?
            count = count + deltaLoop # update count to record data
           
            
    return np.array(dataSimulation),np.array(framesSimulation)



