"""
Este módulo recebe 3 dicionários

    auxVars: aqui temos temos as variáveis auxiliares que determinarão tamanho do domínio (gridSize), 
    quantidade de iterações (niter), a capacidade de suporte do domínio (K) 
    e a taxa de captura de frames (framesRatio).

    seedDict: contém nos "keys" uma tupla representando o vértex inicial de cada célula
    e nos "values" uma instancia de classe. No fim das contas é o dicionário que resgistras as células que
    estão no domínio
 
    nghAddressDict: contém nos "keys" uma tupla representando um vértex específico do domínio
    e nos "values" o endereço de cada vértex vizinho
    
Este módulo retorna 2 numpy arrays

    dataSimulation: este array bidimensional apresenta 10 colunas, cada uma guarda em suas linhas valores referentes
    as densidade de cada subpopulação, a razão entre as densidades de cada população, a proporção
    de proliferação, morte e sobrevivência de cada subpolpulação
    
    framesSimulation: este array tridimensional registra a dinâmica espacial da população em uma dada iteração


"""

import numpy as np      
#import math
#import random
from settingInput import squareSide,niter,deltaI,K


def CellularAutomata(seedDict,nghAddressDict):
    
    #framesRatio,niter,K,gridSize = auxVars.values()
    framesSimulation = [] 
    dataSimulation = []
    t = 0
    for loop in range(niter):
        
        
        listOfCells = list(seedDict.values())
        #random.shuffle(listOfCells)
        # N = [len([p for p in listOfCells if p.id_number == 1]),len([p for p in listOfCells if p.id_number == 1])]
        for cellsLine in listOfCells:
            cellsLine.updateBooleanNetwork(seedDict)
            cellsLine.updateKinetics(seedDict,nghAddressDict)
            
        Lattice = np.zeros((squareSide,squareSide))
        for cellsLine in seedDict.values():
            Lattice[cellsLine.index] = cellsLine.id_number
            
        if (loop % deltaI) == 0:
            
            skmelProlif = len([p for p in listOfCells if p.id_number == 1 and p.proliferate == True])
            skmelDeath = len([p for p in listOfCells if p.id_number == 1 and p.death == True])
            skmelSurv = len([p for p in listOfCells if p.id_number == 1 and p.survive == True])
            skmelMig = len([p for p in listOfCells if p.id_number == 1 and p.migrate == True])
            hacatProlif = len([p for p in listOfCells if p.id_number == 2 and p.proliferate == True])
            hacatDeath = len([p for p in listOfCells if p.id_number == 2 and p.death == True])
            hacatSurv = len([p for p in listOfCells if p.id_number == 2 and p.survive == True])
            hacatMig = len([p for p in listOfCells if p.id_number == 2 and p.migrate == True])
            dataSimulation.append([len(Lattice[Lattice == 1])/K,
                                   len(Lattice[Lattice == 2])/K,
                                   t,
                                   (len(Lattice[Lattice == 2])/len(Lattice[Lattice == 1])),
                                   (skmelProlif/(skmelProlif+skmelDeath+skmelSurv+skmelMig)),
                                   (skmelDeath/(skmelProlif+skmelDeath+skmelSurv+skmelMig)),
                                   (skmelSurv/(skmelProlif+skmelDeath+skmelSurv+skmelMig)),
                                   (skmelMig/(skmelProlif+skmelDeath+skmelSurv+skmelMig)),
                                   (hacatProlif/(hacatProlif+hacatDeath+hacatSurv+hacatMig)),
                                   (hacatDeath/(hacatProlif+hacatDeath+hacatSurv+hacatMig)),
                                   (hacatSurv/(hacatProlif+hacatDeath+hacatSurv+hacatMig)),
                                   (hacatMig/(hacatProlif+hacatDeath+hacatSurv+hacatMig))])
                
            framesSimulation.append(Lattice)
            t = t + 1
    
            
    return np.array(dataSimulation),np.array(framesSimulation)  


        
# return np.array(dataSimulation),np.array(framesSimulation)              


# if loop == count:
    
#     skmelProlif = len([p for p in listOfCells if p.id_number == 1 and p.proliferate == True])
#     skmelDeath = len([p for p in listOfCells if p.id_number == 1 and p.death == True])
#     skmelSurv = len([p for p in listOfCells if p.id_number == 1 and p.survive == True])
#     skmelMig = len([p for p in listOfCells if p.id_number == 1 and p.migrate == True])
#     hacatProlif = len([p for p in listOfCells if p.id_number == 2 and p.proliferate == True])
#     hacatDeath = len([p for p in listOfCells if p.id_number == 2 and p.death == True])
#     hacatSurv = len([p for p in listOfCells if p.id_number == 2 and p.survive == True])
#     hacatMig = len([p for p in listOfCells if p.id_number == 2 and p.migrate == True])
   
#     dataSimulation.append([len(Lattice[Lattice == 1])/K,
#                            len(Lattice[Lattice == 2])/K,
#                            loop,
#                            (len(Lattice[Lattice == 2])/len(Lattice[Lattice == 1])),
#                            (skmelProlif/(skmelProlif+skmelDeath+skmelSurv+skmelMig)),
#                            (skmelDeath/(skmelProlif+skmelDeath+skmelSurv+skmelMig)),
#                            (skmelSurv/(skmelProlif+skmelDeath+skmelSurv+skmelMig)),
#                            (skmelMig/(skmelProlif+skmelDeath+skmelSurv+skmelMig)),
#                            (hacatProlif/(hacatProlif+hacatDeath+hacatSurv+hacatMig)),
#                            (hacatDeath/(hacatProlif+hacatDeath+hacatSurv+hacatMig)),
#                            (hacatSurv/(hacatProlif+hacatDeath+hacatSurv+hacatMig)),
#                            (hacatMig/(hacatProlif+hacatDeath+hacatSurv+hacatMig))])
    
#     framesSimulation.append(Lattice)
#     nn = round(math.log10(loop)) # nn: this an auxiliary parameter to record the smoothness of the curve. 
#     # We must to round the log10 of iteration.
#     deltaLoop = math.ceil((10**(nn+1) - 10**(nn))/framesRatio) # this variable update how much 
#     # interation do we have to wait to record a new data
#     count = count + deltaLoop # update count to record data