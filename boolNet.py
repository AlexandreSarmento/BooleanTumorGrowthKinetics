# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 15:28:14 2022

@author: Alexandre Sarmento
"""

import neighbors
import random

def updateBooleanNetworkA(self,agents):
    
    [listOfEmptyIndex,numberOfEmptyIndex,numberOfSkmel,numberOfHacat] = neighbors.updateNeighbors(self,agents)
    
    self.proliferate = (numberOfEmptyIndex >= 1) and ((numberOfSkmel >= numberOfEmptyIndex) or (numberOfHacat <= numberOfEmptyIndex))
    
    self.migrate = not self.proliferate and (numberOfEmptyIndex >= 1) and ((numberOfSkmel <= numberOfEmptyIndex) or (numberOfHacat >= numberOfEmptyIndex))
    
    self.survive = not self.proliferate and not self.migrate and ((numberOfEmptyIndex == 0) or (self.ProbOfSurv >= random.uniform(0,1)))
    
    self.death = not self.proliferate and not self.migrate and not self.survive
    
    self.emptyIndexList = listOfEmptyIndex
    
     
def updateBooleanNetworkB(self,agents):
    
    [listOfEmptyIndex,numberOfEmptyIndex,numberOfSkmel,numberOfHacat] = neighbors.updateNeighbors(self,agents)
    
    self.proliferate = (numberOfEmptyIndex >= 1) and ((numberOfSkmel >= numberOfEmptyIndex) or (numberOfHacat <= numberOfEmptyIndex))
    
    self.death = not self.proliferate and (numberOfEmptyIndex >= 1) and ((numberOfSkmel <= numberOfEmptyIndex) or (numberOfHacat >= numberOfEmptyIndex))
    
    self.survive = not self.proliferate and not self.death and ((numberOfEmptyIndex == 0) or (self.ProbOfSurv >= random.uniform(0,1)))
    
    self.migrate = self.proliferate and not self.death and not self.survive and (numberOfEmptyIndex >= 1) 
    
    self.listOfEmptyIndex = listOfEmptyIndex