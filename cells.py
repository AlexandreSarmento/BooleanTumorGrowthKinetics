'''
This script have the mother class Population and the daugther class Skmel and Hacat

'''

import neighbors
import random
import basin2attractor
import models
import settingInput

class Population():
    
    def __init__(self,index,nghVertexDict):
        
        
        self.index = index # index: the address in term of row and col of the cell (tuple)
        
        self.nghAddress = nghVertexDict[self.index] # nghAddress: list of tuples. here we get the values of a dicitionay as a list of tuples
     
    def updateBooleanNetwork(self,agents,i):
        
        
        [listOfEmptyIndex,numberOfEmptyIndex,numberOfSkmel,numberOfHacat] = neighbors.updateNeighbors(self,agents)
        [migration,proliferation] = basin2attractor.updateMicroEnvironment(numberOfEmptyIndex,numberOfSkmel,numberOfHacat)
        plog = models.updateProliferationProbability(self.lambA,i)
        r1 = random.uniform(0,1)
        r2 = random.uniform(0,1)
        self.proliferate = (numberOfEmptyIndex >= 1) and ((plog > r1) or proliferation)  
        self.migrate = (numberOfEmptyIndex >= 1) and migration 
        self.survive = not self.proliferate and self.migrate and ((1 - plog) > r2) 
        self.death = not self.proliferate and not self.migrate and not self.survive
        self.listOfEmptyIndex = listOfEmptyIndex
    
    def updateTumorGrowthKinetics(self,agents,nghVertexDict):
        
        if self.proliferate:
            if agents[self.index].id_number == 1:        
                emptyIndex = random.choice(self.listOfEmptyIndex)
                agents[emptyIndex] = Skmel(emptyIndex,nghVertexDict)
            else:
                emptyIndex = random.choice(self.listOfEmptyIndex)
                agents[emptyIndex] = Hacat(emptyIndex,nghVertexDict)
        elif self.migrate:
                if agents[self.index].id_number == 1:
                    del agents[self.index]
                    emptyIndex = random.choice(self.listOfEmptyIndex)
                    agents[emptyIndex] = Skmel(emptyIndex,nghVertexDict)
                else:
                    del agents[self.index]
                    emptyIndex = random.choice(self.listOfEmptyIndex)
                    agents[emptyIndex] = Hacat(emptyIndex,nghVertexDict)
        else:
            if self.survive:
                pass
            else:
                del agents[self.index]
            

class Skmel(Population):
          
    def __init__(self,index,nghVertexDict):
        
        super().__init__(index,nghVertexDict)
        self.id_number = 1
        self.lambA = settingInput.lamb[0]#0.1
         
class Hacat(Population):
          
    def __init__(self,index,nghVertexDict):
        
        super().__init__(index,nghVertexDict)
        self.id_number = 2
        self.lambA = settingInput.lamb[1]#0.17
        
        


# if self.proliferate:
    
#     if agents[self.index].id_number == 1:
#         emptyIndex = random.choice(self.listOfEmptyIndex)
#         agents[emptyIndex] = Skmel(emptyIndex,nghVertexDict)
#     else:
#         emptyIndex = random.choice(self.listOfEmptyIndex)
#         agents[emptyIndex] = Hacat(emptyIndex,nghVertexDict)
# else:
#     if self.migrate:
#         if agents[self.index].id_number == 1:
#             del agents[self.index]
#             emptyIndex = random.choice(self.listOfEmptyIndex)
#             agents[emptyIndex] = Skmel(emptyIndex,nghVertexDict)
#         else:
#             del agents[self.index]
#             emptyIndex = random.choice(self.listOfEmptyIndex)
#             agents[emptyIndex] = Hacat(emptyIndex,nghVertexDict)
#     else:
#         if self.death:
#             del agents[self.index]
#         else:
#             pass