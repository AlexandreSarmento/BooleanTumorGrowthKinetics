# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 07:47:45 2022

@author: Alexandre Sarmento
"""

'''
This module harbour variables helpful to set simulations. The variables here are going to be imported to others modules or scripts 
'''


# nRowCols: number of rows and columns (int)
nRowCols = 200 
# K: Carring capacity (int)
K = nRowCols*nRowCols
# C0: initial numer of cells (int) 
C0 = 2000 
# indexOfngh: id number to set focal cell neighborhood (int). One may check the function makeNeighborsList inside the module neighbors
indexOfngh = 0  
# prolifCap: proliferation capacity (list of int). The first element willb assigned to MEL and the second on to KCT
prolifCap = [5,6]
# finalTime: final time of simulation (int) 
finalTime = 8
# deltaT: the time-step (float) 
deltaT = 1/2 
# niter: total number of iteration (int)
niter = int(finalTime/deltaT) 
# dataFrameKeys:identification of data to be saved at each simulation (list of string)
dataFrameKeys = ['dSdt','dHdt','N','iter','prolS','deathS','migS','survS','prolH','deathH','migH','survH']
# initial guess to curve fit of Hacat and skmel respectivelly
paramsHacat,paramsSkmel = [0.6,1,4],[0.2,1,4]
