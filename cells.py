import neighbors
import random
# import sys
# sys.path.append("C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/runDynamic")
# from runDynamic import auxVars 
from settingInput import K

class Population():
    
    def __init__(self,index,nghVertexDict):
        
        self.index = index # index: the address in term of row and col of the cell (tuple)
        
        self.nghAddress = nghVertexDict[self.index] # nghAddress: list of tuples. here we get the values of a dicitionay as a list of tuples
        
        self.CC = K # CC: carrying capacity (int)
    
    def updateBooleanNetwork(self,agents):
        
        
        [listOfEmptyIndex,numberOfEmptyIndex,numberOfSkmel,numberOfHacat] = neighbors.updateNeighbors(self,agents)
        
        hL = 1 - (len(agents)/self.CC)
        
        self.proliferate = (numberOfEmptyIndex >= 1) and ((numberOfSkmel >= numberOfEmptyIndex) 
                                                          or (numberOfHacat <= numberOfEmptyIndex))
        
        self.migrate = not self.proliferate and (numberOfEmptyIndex >= 1) and ((numberOfSkmel <= numberOfEmptyIndex) or 
                                                                               (numberOfHacat >= numberOfEmptyIndex))
        
        self.survive = not self.proliferate and not self.migrate and (random.uniform(0,1) < (1 - hL))        
        self.death = not self.proliferate and not self.migrate and not self.survive
        self.listOfEmptyIndex = listOfEmptyIndex

    
    def updateKinetics(self,agents,nghVertexDict):
        
        
        if self.proliferate:
            
            if agents[self.index].id_number == 1:
                emptyIndex = random.choice(self.listOfEmptyIndex)
                agents[emptyIndex] = Skmel(emptyIndex,nghVertexDict)
            else:
                emptyIndex = random.choice(self.listOfEmptyIndex)
                agents[emptyIndex] = Hacat(emptyIndex,nghVertexDict)
        else:
            if self.migrate:
                if agents[self.index].id_number == 1:
                    del agents[self.index]
                    emptyIndex = random.choice(self.listOfEmptyIndex)
                    agents[emptyIndex] = Skmel(emptyIndex,nghVertexDict)
                else:
                    del agents[self.index]
                    emptyIndex = random.choice(self.listOfEmptyIndex)
                    agents[emptyIndex] = Hacat(emptyIndex,nghVertexDict)
            else:    
                if self.death:
                    del agents[self.index]
                else:
                    if self.survive:
                        pass
                    
                    
    

class Skmel(Population):
          
    def __init__(self,index,nghVertexDict):
        
        super().__init__(index,nghVertexDict)
        self.id_number = 1
        

         
class Hacat(Population):
          
    def __init__(self,index,nghVertexDict):
        
        super().__init__(index,nghVertexDict)
        self.id_number = 2
        
    
    