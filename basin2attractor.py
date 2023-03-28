# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 14:16:48 2023

@author: Alexandre Sarmento
"""

def updateAttractors(numberOfEmptyIndex,numberOfSkmel,numberOfHacat):
    
    attractor1 = (numberOfHacat >= numberOfEmptyIndex) or (numberOfSkmel <= numberOfHacat) or (numberOfSkmel <= numberOfEmptyIndex)
    attractor2 = (numberOfSkmel >= numberOfEmptyIndex) or (numberOfHacat <= numberOfEmptyIndex) or (numberOfSkmel >= numberOfHacat)
    
    return attractor1,attractor2