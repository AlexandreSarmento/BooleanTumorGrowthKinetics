# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 09:43:38 2022

@author: Alexandre Sarmento
"""
import numpy as np
import random
import cells

def updateNeighbors(self,agents):
    '''
    Input: 
          one object (<class '__main__.name_of_class'>).
    Processing: 
          check the amount of vertex occupied by skmel, hacat and those which are empty.
    Output: 
          listOfEmptyIndex: first empty neighbors (list of tuple)
          neighborsInstance: a list of object instantiate in the neighborhood
          neighborsInstanceIDs: a list of id_number which is an attribute of each object
          
    ''' 
    
    listOfEmptyIndex = [emptyAddress for emptyAddress in self.nghAddress if emptyAddress not in agents]
    listOfOccupiedIndex = [occupiedAddress for occupiedAddress in self.nghAddress if occupiedAddress in agents]
   
    neighborsInstance = []
    neighborsInstanceIDs = []
    for loopIDs in range(len(listOfOccupiedIndex)):
        
        neighborsInstance.append(agents[listOfOccupiedIndex[loopIDs]])
        neighborsInstanceIDs.append(neighborsInstance[loopIDs].id_number)
   
    return listOfEmptyIndex,len(listOfEmptyIndex),neighborsInstanceIDs.count(1),neighborsInstanceIDs.count(2)

def makeNeighborsDicitionary(nrow,ncol):
    """
    Input:
        parameter nrow and ncol
    Processing:
        create dictionary containing the list of all neighbors (value) for a central position (key)
    Output:
        dictionary where the key= central position, and the value=list of neighboring positions around that center
    """
    listOfIndex = [(r,c) for r in np.arange(0,nrow) for c in np.arange(0,ncol)]
    nghIdxDict = {index: makeNeighborsList(index,nrow,ncol) for index in listOfIndex}
    
    return nghIdxDict

def makeNeighborsList(index, nrow, ncol):
    """
    Input:
        index: cell's position (tuple)
        nrow: maximum width of domain (int)
        ncol: maximum height of domain (int)

    Processing:
        use list comprehension to create a list of all positions in the cell's Moore neighborhood. Valid positions are 
        those that are within the confines of the domain (nrow, ncol) and not the same as the cell's current position.
    Output: 
        list of all valid positions around the cell (list)
    """
    # Unpack the tuple containing the cell's position
    row, col = index
    nghList = [(row+i, col+j)
         for i in [-1, 0, 1]
         for j in [-1, 0, 1]
         if 0 <= row + i < nrow
         if 0 <= col + j < ncol
         if not (j == 0 and i == 0)]
    return nghList


def getCellsSeed(nghAddressDict,initialConditionSkmel,initialConditionHacat):
    

    '''
    Input
        initialConditionSkmel: initial numbers of the object Skmel in the Lattice (int)
        initialConditionHacat: initial numbers of the object Hacat in the Lattice (int)
        listOfSeedIdx: list of address to seed initials cells (list of tuples)
    Processing
        Here we have to create a dicitionary to seed the cells in random address (row,col) and at same instatiate an object (Hacat/Skmel) 
        into the specific address. Thus, firstly we're going to generate many tuples representing the initial address of each object. In doing so
        we're going to generate a dicitionary where the keys represent a cell address and values are the objects.
    Output
        joinDict: dictionary where the keys are tuples and the values are Hacat/Skmel objects itself
    '''
    '''
    AQUI TEM QUE DAR UM JEITO DE INSTANCIAR COM O DICIONÁRIO QUE TEM ENDEREÇOS (KEY) DO DOMÍNIO COM O ENDEREÇOS 
    DE CADA VIZINHO (VALUE), MAS TAMBÉM UM DICIONÁRIO COM O ENDEREÇO (KEY) DE CADA INSTÂNCIA (VALUE)
    '''
    
    hacatDict = {}
    skmelDict = {}
    cellsSeedAddress = list(nghAddressDict.keys())
    seedSkmelIdx = random.sample(cellsSeedAddress, k=initialConditionSkmel)
    seedHacatIdx = random.sample(cellsSeedAddress, k=initialConditionHacat)
    
    for j in seedSkmelIdx:
        skmelDict[j] = cells.Skmel(j,nghAddressDict)
        
    for i in seedHacatIdx:
        hacatDict[i] = cells.Hacat(i,nghAddressDict)
     
    return {**skmelDict,**hacatDict}

