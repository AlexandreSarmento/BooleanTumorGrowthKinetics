"""

This module harbour functions that represent the transformation of boolean network basin into
cellular automata dynamic rules

"""


def updateMicroEnvironment(numberOfEmptyIndex,numberOfSkmel,numberOfHacat):
    
    '''
    Input
        numberOfEmptyIndex: number of empty neighbors (int)
        numberOfSkmel: number of vertex occupied by skmel (int)
        numberOfHacat: number of vertex occupied by hacat (int)
    Processing
        This function update the boolean expressions that describes the tolerance to high density
    Output
        migration: condition to cell migrate (boolean)
        proliferation: condition to cell proliferate (boolean)
        
    '''
    
    migration = (numberOfSkmel <= numberOfEmptyIndex) or (numberOfHacat >= numberOfSkmel)
    proliferation = (numberOfSkmel >= numberOfEmptyIndex) or (numberOfHacat <= numberOfSkmel)
      
    return migration, proliferation
