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

import neighbors
#import numpy as np
#import matplotlib.pyplot as plt 

squareSide = 200 # squareSide: number of rows and columns (int)
K = squareSide*squareSide # CC: Carring capacity, it is the total number of cells into domain (int)
rangeHacat = [400,800,1200,1600,2000,2400,2800,3200,3600,4000]  #initialConditionSkmel*10 # initialConditionHacat: initial numbers of the object Hacat in the Lattice (int)
time = list(range(1,9))
indexOfngh = 1
deltaI = 1  # deltaI: number of interaction which is equivalent to one day (int)
numberOfSavedValues = 8 # numberOfSavedValues: the number of rows in the longitudinal dataframe (int)
niter = numberOfSavedValues*deltaI # niter: total number of iteration (int)
# dataFrameKeys: the identification of each columns from the longitudinal dataframe (List of Strings)
#dataFrameKeys = ['dSdt','dHdt','time','ratio','prolS','deathS','survS','migS','prolH','deathH','survH','migH']
dataFrameKeys = ['dSdt','dHdt','time','ratio','prolS','deathS','migS','prolH','deathH','migH']
#replicate = 3
nghVertexDict = neighbors.makeNeighborsDicitionary(nrow = squareSide,ncol = squareSide,d = indexOfngh)
#dataCube = np.empty((replicate,numberOfSavedValues,len(dataFrameKeys)))
initialGuessHacat = [0.6,1,4]
initialGuessSkmel = [0.2,1,4]


# Moore2nd
# VonNeumman2nd12
# VonNeumman2nd24

