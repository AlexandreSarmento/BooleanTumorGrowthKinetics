# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 16:25:03 2022

@author: Alexandre Sarmento
"""

'''
HACAT
'''

proliferate = (numberOfEmptyIndex >= 1) and \
    ((numberOfSkmel >= numberOfEmptyIndex) or (numberOfHacat <= numberOfEmptyIndex))

death = not proliferate and (numberOfSkmel < numberOfHacat) #or \
                                       #(numberOfHacat >= numberOfEmptyIndex))

survive = not (proliferate and death) and (numberOfSkmel == numberOfHacat)

listOfEmptyIndex = listOfEmptyIndex


'''
SKMEL
'''

proliferate = (numberOfEmptyIndex >= 1)

death = not proliferate and ((numberOfSkmel < numberOfHacat) or \
                                      (numberOfHacat == numberOfEmptyIndex))
        
survive = not (proliferate and death) and (numberOfSkmel == numberOfHacat)

listOfEmptyIndex = listOfEmptyIndex

