import numpy as np
import random
import cells
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
        index: cell's vértex (tuple)
        nrow: number of rows (int)
        ncol: number of columns (int)

    Processing:
        use list comprehension to create a list of all positions in the cell's Moore neighborhood. Valid positions are 
        those that are within the confines of the domain (nrow, ncol) and not the same as the cell's current position.
    Output:
        nghList: list of the neighbors vértices of a given cell (list of tuple)
        
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



def getCellsSeed(nghVertexDict,rangeHacat):

    '''
    Input
        initialConditionSkmel: initial numbers of the object Skmel in the Lattice (int)
        initialConditionHacat: initial numbers of the object Hacat in the Lattice (int)
        nghVertexDict: vertex of each neighbor (dicitionary)
    Processing
        Here we have to create a dicitionary to seed the cells in random address (row,col) and at same time 
        instatiate an object (Hacat/Skmel) into the specific vertex. Thus, firstly we're going to generate many 
        tuples representing the initial address of each instance. In doing sowe're going to generate a dicitionary 
        where the keys represent a cell address and values are the instance.
    Output
        dictionary where the keys are tuples and the values are Hacat/Skmel objects itself
    '''
    
    
    initialConditionSkmel = int(rangeHacat/10)
    hacatDict = {} # dicitionary to save hacat vertex and it instance
    skmelDict = {} #  dictionary to save skmel vertex and it instance
    cellsSeedAddress = list(nghVertexDict.keys())
    seedSkmelIdx = random.sample(cellsSeedAddress, k=initialConditionSkmel)
    seedHacatIdx = random.sample(cellsSeedAddress, k=rangeHacat)
    
    for j in seedSkmelIdx:
        skmelDict[j] = cells.Skmel(j,nghVertexDict)
        
    for i in seedHacatIdx:
        hacatDict[i] = cells.Hacat(i,nghVertexDict)
     
    return {**skmelDict,**hacatDict}