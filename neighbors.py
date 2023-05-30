import numpy as np
import random
import cells
import math
#from collections import Counter


def updateNeighbors(self,agents):
    '''
    
    Input: 
          one object (<class '__main__.name_of_class'>).
    Processing: 
          check the amount of vertex occupied by skmel, hacat and those which are empty.
    Output: 
          listOfEmptyIndex: first empty neighbors (list of tuple)
          neighborsInstance: a list of object instantiate in the neighborhood
          neighborsInstanceIDs: a list of instance attribute id_number 
          
    ''' 
    
    listOfEmptyIndex = [emptyAddress for emptyAddress in self.nghAddress if emptyAddress not in agents]
    listOfOccupiedIndex = [occupiedAddress for occupiedAddress in self.nghAddress if occupiedAddress in agents]
   
    neighborsInstance = []
    neighborsInstanceIDs = []
    for loopIDs in range(len(listOfOccupiedIndex)):
        
        neighborsInstance.append(agents[listOfOccupiedIndex[loopIDs]])
        neighborsInstanceIDs.append(neighborsInstance[loopIDs].id_number)
        
        
    if agents[self.index].id_number == 1:
        numberOfSkmel = neighborsInstanceIDs.count(1) + 1
        numberOfHacat = neighborsInstanceIDs.count(2)
      
    else:
        numberOfSkmel = neighborsInstanceIDs.count(1)
        numberOfHacat = neighborsInstanceIDs.count(2) + 1
            
    return listOfEmptyIndex,len(listOfEmptyIndex),numberOfSkmel,numberOfHacat


def makeNeighborsDicitionary(nrow,ncol,d):
    """
    Input:
        nrow: number of rows (integer)
        ncol: number of col (interger)
    Processing:
        create dictionary containing in the keys a tuple representing the cell vértex and in the values a list of tuples representing the
        neighbors vértices
    Output:
        nghIdxDict: neighbors index dictionary's (dictionary)
    """
    listOfIndex = [(r,c) for r in np.arange(0,nrow) for c in np.arange(0,ncol)]
    nghIdxDict = {index: makeNeighborsList(index,nrow,ncol,d) for index in listOfIndex}
    
    return nghIdxDict

def makeNeighborsList(index, nrow, ncol,d):
    """
    Input:
        index: cell's vertex (tuple)
        nrow: number of rows (int)
        ncol: number of columns (int)
        d: id of focal cell neighborhood. 0- Moore 1st order. 1-Moore 2nd order. 2. Von newman 1st order. 3. Von newman 2nd order. 

    Processing:
        use list comprehension to create a list of all positions in the cell's neighborhood. Valid positions are 
        those that are within the confines of the domain (nrow, ncol) and not the same as the cell's current position.
    Output:
        nghList: list of the neighbors vertice of a given cell (list of tuple)
        
    """
    # Unpack the tuple containing the cell's position
    row, col = index
    if d == 0:
        
        nghList = [(row+i, col+j)
              for i in [-1,0,1]
              for j in [-1,0,1]
              if 0 <= row + i < nrow
              if 0 <= col + j < ncol
              if not (j == 0 and i == 0)]
    else:
        if d == 1:
            
            nghList = [(row+i, col+j)
                       for i in [-2,-1,0,1,-2]
                       for j in [-2,-1,0,1,-2]
                       if 0 <= row + i < nrow
                       if 0 <= col + j < ncol
                       if not (j == 0 and i == 0)]
        
        else:
            if d > 1:
                nghList = [(row+i, col+j)
                           for i in range(-d,d+1)
                           for j in range(abs(i)-d,d+1-abs(i))
                           if 0 <= row + i < nrow
                           if 0 <= col + j < ncol
                           if not (j == 0 and i == 0)]
    
    return nghList



def getCellsSeed(nghVertexDict,density0):

    '''
    Input
        density0: initial number of cells
        nghVertexDict: dictionary where each focal cell address (tuple) are at key and the focal cell neighbors address (list of tuple) are at values
    Processing
        Here we have to create a dicitionary to seed the cells in random address (row,col) and at same time 
        instatiate an object (Hacat/Skmel) into the specific vertex. Thus, firstly we're going to generate many 
        tuples representing the initial address of each instance at random. In doing so we're going to generate a dicitionary 
        where the keys represent a cell address and values are the instance.
    Output
        dictionary where the keys are tuples and the values are Hacat/Skmel objects itself
    '''
    
    
    skmel0 = int(density0/10)
    hacat0 = density0 - skmel0
    hacatDict = {} # dicitionary to save hacat vertex and it instance
    skmelDict = {} #  dictionary to save skmel vertex and it instance
    
    cellsSeedAddress = list(nghVertexDict.keys())
    seedSkmelIdx = random.sample(cellsSeedAddress, k = skmel0)
    seedHacatIdx = random.sample(cellsSeedAddress, k = hacat0)
    
    for j in seedSkmelIdx:
        skmelDict[j] = cells.Skmel(j,nghVertexDict)
        
    for i in seedHacatIdx:
        hacatDict[i] = cells.Hacat(i,nghVertexDict)
     
    return {**skmelDict,**hacatDict}


def updateKineticsProbability(listOfCells):
    
    '''
    Input
        listOfCells: list of object Skmel/Hacat instantiated at a given iteration
    Processing
        Here we count the amount of cell which proliferate, migrate, died and survive
    Output
        Ps: skmel probability of proliferation
        Ds: skmel probability of death
        Ms: skmel probability of migration
        Ss: skmel probability of survive
        Ph: hacat probability of proliferation
        Dh: hacat probability of death
        Mh: hacat probability of migration
        Sh: hacat probability of survive
    
    '''
    
    skmelProlif = len([p for p in listOfCells if p.id_number == 1 and p.proliferate == True])
    skmelDeath = len([p for p in listOfCells if p.id_number == 1 and p.death == True])
    skmelMig = len([p for p in listOfCells if p.id_number == 1 and p.migrate == True])
    skmelSurv = len([p for p in listOfCells if p.id_number == 1 and p.survive == True])
    hacatProlif = len([p for p in listOfCells if p.id_number == 2 and p.proliferate == True])
    hacatDeath = len([p for p in listOfCells if p.id_number == 2 and p.death == True])
    hacatMig = len([p for p in listOfCells if p.id_number == 2 and p.migrate == True])
    hacatSurv = len([p for p in listOfCells if p.id_number == 2 and p.survive == True])
    
    Ps = skmelProlif/(skmelProlif+skmelDeath+skmelMig+skmelSurv)
    Ds = skmelDeath/(skmelProlif+skmelDeath+skmelMig+skmelSurv)
    Ms = skmelMig/(skmelProlif+skmelDeath+skmelMig+skmelSurv)
    Ss = skmelSurv/(skmelProlif+skmelDeath+skmelMig+skmelSurv)
    Ph = hacatProlif/(hacatProlif+hacatDeath+hacatMig+hacatSurv)
    Dh = hacatDeath/(hacatProlif+hacatDeath+hacatMig+hacatSurv)
    Mh = hacatMig/(hacatProlif+hacatDeath+hacatMig+hacatSurv)
    Sh = hacatSurv/(hacatProlif+hacatDeath+hacatMig+hacatSurv)
    
    return Ps,Ds,Ms,Ss,Ph,Dh,Mh,Sh



# def updateDistribution(squareSide,sigma):
    
#     point = int(squareSide/2)
#     seedVertex = np.zeros((squareSide,squareSide))

#     for row in range(squareSide):
#         for col in range(squareSide):
#             seedVertex[row,col] = (40000/(4*math.pi*sigma))*np.exp(-((row - point)**2 + (col - point)**2) /(4*sigma))
            
            
#     maskSeedVertex = seedVertex > 0
#     maskSeedVertexAddress = np.where(maskSeedVertex)
#     seedVertexAddress = np.vstack((maskSeedVertexAddress[0],maskSeedVertexAddress[1])).T
#     seedVertexList = [tuple(seedVertexAddress[i,:]) for i in range(len(seedVertexAddress))]

#     return seedVertexList

