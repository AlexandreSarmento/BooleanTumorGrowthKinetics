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
# auxGeometry: auxiliar parameter to calculate neighborhood address (int) One may check the function makeNeighborsList 
# inside the module neighbors
auxGeometry = 1
# geometry: type of neighborhood geometry (string). Enter with either moore or vonNeumman
geometry = 'moore'
melRhoMax = 7
kctRhoMax = 7
# prolifCap: proliferation capacity (tuple of int). The first element willb assigned to MEL and the second on to KCT
prolifCap = (melRhoMax,kctRhoMax)
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
