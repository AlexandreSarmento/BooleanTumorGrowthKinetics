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
          listOfEmptyIndex: first empty neighbors address (list of tuple)
          numberOfSkmel: number of skmel in the neighborhood (int)
          numberOfHacat: number of hacat in the neighborhood (int)
          numberOfEmptyIndex: number of empty neighbors (int)     
          
    ''' 
    
    listOfEmptyIndex = [emptyAddress for emptyAddress in self.nghAddress if emptyAddress not in agents]
    listOfOccupiedIndex = [occupiedAddress for occupiedAddress in self.nghAddress if occupiedAddress in agents]
    neighborsInstanceIDs = [agents[idx].cellsID for idx in listOfOccupiedIndex]    
    
    numberOfSkmel = neighborsInstanceIDs.count(1)
    numberOfHacat = neighborsInstanceIDs.count(2)
    numberOfEmptyIndex = len(listOfEmptyIndex)
        
    return listOfEmptyIndex,numberOfEmptyIndex,numberOfSkmel,numberOfHacat


def makeNeighborsDicitionary(nrow,ncol,d,geo):
    """
    Input:
        nrow: number of rows (int)
        ncol: number of col (int)
    Processing:
        create dictionary containing in the keys a tuple representing the cell vértex and in the values a list of tuples representing the
        neighbors vértices
    Output:
        nghIdxDict: neighbors index dictionary's (dictionary)
    """
    listOfIndex = [(r,c) for r in np.arange(0,nrow) for c in np.arange(0,ncol)]
    nghIdxDict = {index: makeNeighborsList(index,nrow,ncol,d,geo) for index in listOfIndex}
    
    return nghIdxDict

def makeNeighborsList(index, nrow, ncol,d,geo):
    """
    Input:
        index: cell's vertex (tuple)
        nrow: number of rows (int)
        ncol: number of columns (int)
        d: auxiliar parameter to calculate neighborhood address (int)
        geo: type of neighborhood geometry (string) 

    Processing:
        use list comprehension to create a list of all positions in the cell's neighborhood. Valid positions are 
        those that are within the confines of the domain (nrow, ncol) and not the same as the cell's current position.
    Output:
        nghStyle: dictionary of the focal cell neighbors style. key are interger and values are list of tuple
        
    """
    # Unpack the tuple containing the cell's position
    row,col = index
    
    neighbor_geometry = {'moore':[(row+i, col+j)
                                   for i in range(-d,d+1)
                                   for j in range(-d,d+1)
                                   if 0 <= row + i < nrow
                                   if 0 <= col + j < ncol
                                   if not (j == 0 and i == 0)
                                 ],
                
                         'vonNeumman':[(row+i, col+j)
                                        for i in range(-d,d+1)
                                        for j in range(abs(i)-d,d+1-abs(i))
                                        if 0 <= row + i < nrow
                                        if 0 <= col + j < ncol
                                        if not (j == 0 and i == 0)
                                      ]
                        }

    return neighbor_geometry[geo]



def getCellsSeed(nghVertexDict,density0,prolifCap):

    '''
    Input
        density0: initial number of cells
        nghVertexDict: dictionary where each focal cell address (tuple) are at key and the focal cell neighbors address (list of tuple) are at values
        prolifCap: proliferation capacity
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
    pmaxS,pmaxH = prolifCap[0],prolifCap[1]
    for j in seedSkmelIdx:
        skmelDict[j] = cells.Skmel(j,nghVertexDict,pmaxS)
        
    for i in seedHacatIdx:
        hacatDict[i] = cells.Hacat(i,nghVertexDict,pmaxH)
     
    return {**skmelDict,**hacatDict}
