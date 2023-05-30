# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 07:47:45 2022

@author: Alexandre Sarmento
"""

'''
This module harbour variables helpful to set simulations. The variables here are going to be imported to others modules or scripts 
'''


squareSide = 200 # squareSide: number of rows and columns (int)
K = squareSide*squareSide # CC: Carring capacity (int)
C0 = 3080 # C0: initial numer of cells (int)
indexOfngh = 0 # indexOfngh: id number to set focal cell neighborhood (int). One may check the function makeNeighborsList inside the module neighbors 
lamb = [0.3,0.4] # lamb: parameter lambda value (list of float)
deltaI = 1 # deltaI: number of interaction which is equivalent to one arbitrary unit of time (int)
numberOfSavedValues = 12  # numberOfSavedValues: the number of rows in the longitudinal dataframe (int)
niter = numberOfSavedValues*deltaI # niter: total number of iteration (int)
# dataFrameKeys:identification of data to be saved at each simulation (list of string)
dataFrameKeys = ['dSdt','dHdt','N','iter','prolS','deathS','migS','survS','prolH','deathH','migH','survH']
# initial guess to curve fit of Hacat and skmel respectivelly
paramsHacat,paramsSkmel = [0.6,1,4],[0.2,1,4]
