'''
This script have the mother class Population and the daugther class Skmel and Hacat

The function updateBooleanNetwork apply the equation 3 to 9 in the manuscript which also are atribute of class, than we go through
the function updateTumorGrowthDynamic which generates the states transiton    

'''

import neighbors
import random
import models
import inputData

class Population():
    
    def __init__(self,index,nghVertexDict,pmax):
        
        
        self.index = index # index: the address in term of row and col of the cell (tuple)
        self.nghAddress = nghVertexDict[self.index] # nghAddress: list of tuples. here we get the 
        #values of a dicitionay as a list of tuples
        self.CC = inputData.K ## self.CC: carrying capacity (int)
        

        
    def updateBooleanNetwork(self,agents): #probMigProlS,probMigProlH,i
        
        [listOfEmptyIndex,numberOfEmptyIndex,numberOfSkmel,numberOfHacat] = neighbors.updateNeighbors(self,agents)
        [migration,proliferation] = models.updateMicroEnvironment(numberOfEmptyIndex,numberOfSkmel,numberOfHacat)
        pprol = 1 - (len(agents)/self.CC)
 
        if self.cellsID == 1:
            self.death = (self.rhoMax <= 0) and (numberOfEmptyIndex == 0)
            self.proliferate = (numberOfEmptyIndex >= 1) and (proliferation or (pprol > random.uniform(0,1))) and not self.death
            self.migrate = (numberOfEmptyIndex >= 1) and migration and not self.death
            self.survive = not self.death and not self.proliferate and not self.migrate
        else:
            self.survive = self.rhoMax <= 0
            self.proliferate = (numberOfEmptyIndex >= 1) and (proliferation or (pprol > random.uniform(0,1))) and not self.survive           
            self.migrate = (numberOfEmptyIndex >= 1) and migration and not self.survive 
            self.death = not self.survive and not self.proliferate and not self.migrate
            
        self.listOfEmptyIndex = listOfEmptyIndex
        
    def updateTumorGrowthKinetics(self,agents,nghVertexDict):
        
        if self.proliferate:
            if agents[self.index].cellsID == 1:        
                emptyIndex = random.choice(self.listOfEmptyIndex)
                pmax = self.rhoMax - 1
                agents[self.index] = Skmel(self.index,nghVertexDict,pmax)
                agents[emptyIndex] = Skmel(emptyIndex,nghVertexDict,pmax)
            else:
                emptyIndex = random.choice(self.listOfEmptyIndex)
                pmax = self.rhoMax - 1
                agents[self.index] = Hacat(self.index,nghVertexDict,pmax)
                agents[emptyIndex] = Hacat(emptyIndex,nghVertexDict,pmax)
                
                
        elif self.migrate:
                if agents[self.index].cellsID == 1:
                    del agents[self.index]
                    emptyIndex = random.choice(self.listOfEmptyIndex)
                    pmax = self.rhoMax
                    agents[emptyIndex] = Skmel(emptyIndex,nghVertexDict,pmax)
                else:
                    del agents[self.index]
                    emptyIndex = random.choice(self.listOfEmptyIndex)
                    pmax = self.rhoMax 
                    agents[emptyIndex] = Hacat(emptyIndex,nghVertexDict,pmax)
        else:
            if self.survive:
                pass                
            else:
                del agents[self.index]
            
                

class Skmel(Population):
          
    def __init__(self,index,nghVertexDict,pmax):
        
        super().__init__(index,nghVertexDict,pmax)
        self.cellsID = 1
        self.rhoMax = pmax

class Hacat(Population):
          
    def __init__(self,index,nghVertexDict,pmax):
        
        super().__init__(index,nghVertexDict,pmax)
        self.cellsID = 2
        self.rhoMax = pmax
