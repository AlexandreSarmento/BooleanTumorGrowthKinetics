# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 07:47:45 2022

@author: Alexandre Sarmento
"""

'''
Here in this script we shall assign values to variables which is going to be usefull to set domain of 
population dynamic simulation as well those variables which is going to be usefull to set results. This module
is going to be imported to others 
'''

squareSide = 200 # squareSide: number of rows and columns (int)
initialConditionSkmel = 5 # initialConditionSkmel: initial numbers of the object Skmel in the Lattice (int)
initialConditionHacat = initialConditionSkmel*10 # initialConditionHacat: initial numbers of the object Hacat in the Lattice (int)
initialNumberOfCells = initialConditionSkmel + initialConditionHacat # initialNumberOfCells: initial numbers of cells (int)
K = squareSide*squareSide # CC: Carring capacity, it is the total number of cells into domain (int)
#niter = 48 # niter: total number of iteration (int)
deltaI = 6 # deltaI: number of interaction which is equivalent to one day (int)
numberOfSavedValues = 8 # numberOfSavedValues: the number of rows in the longitudinal dataframe (int)
niter = 48 # niter: total number of iteration (int)
# dataFrameKeys: the identification of each columns from the longitudinal dataframe (List of Strings)
dataFrameKeys = ['dSdt','dHdt','time','ratio','prolS','deathS','survS','migS','prolH','deathH','survH','migH']
replicate = 7
