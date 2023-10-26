'''
This module harbour some model useful to whole simulation. 
The function Velhurst is the logistic model present at Morais et al 2017
The function updateProliferationProbability return population growth be in log phase
The function getCorrelation return the spearman correlation among tumor growth dynamic

'''

import numpy as np
from scipy.stats import pearsonr,spearmanr
import math

def Velhurst(t,CC,rho,tau):
    
    '''
    Input
        t: time
        CC: carrying capacity
        rho: proliferation rates
        tau: half asymptote time
    Processing
        This function is as input of curve fit present at graphics module and at same time
        this function return the growth curve once the parmeters were estimated
    Output
        Density of cells over time
    '''
    
    return CC/(1 + np.exp(-rho*(t-tau))) 


def updateKineticsProbs(listOfCells):
    
    '''
    Input
        listOfCells: list of object Skmel/Hacat instantiated at a given iteration
    Processing
        Here we count the amount of cell which proliferate, migrate, died and survive
    Output
        Ps: skmel probability of proliferation
        Ds: skmel probability of death
        Ms: skmel probability of migration
        Ss: skmel probability of survive
        Ph: hacat probability of proliferation
        Dh: hacat probability of death
        Mh: hacat probability of migration
        Sh: hacat probability of survive
    
    '''
    
    skmelProlif = len([p for p in listOfCells if p.cellsID == 1 and p.proliferate == True])
    skmelDeath = len([p for p in listOfCells if p.cellsID == 1 and p.death == True])
    skmelMig = len([p for p in listOfCells if p.cellsID == 1 and p.migrate == True])
    skmelSurv = len([p for p in listOfCells if p.cellsID == 1 and p.survive == True])
    hacatProlif = len([p for p in listOfCells if p.cellsID == 2 and p.proliferate == True])
    hacatDeath = len([p for p in listOfCells if p.cellsID == 2 and p.death == True])
    hacatMig = len([p for p in listOfCells if p.cellsID == 2 and p.migrate == True])
    hacatSurv = len([p for p in listOfCells if p.cellsID == 2 and p.survive == True])
    
    Ps = skmelProlif/(skmelProlif+skmelDeath+skmelMig+skmelSurv)
    Ds = skmelDeath/(skmelProlif+skmelDeath+skmelMig+skmelSurv)
    Ms = skmelMig/(skmelProlif+skmelDeath+skmelMig+skmelSurv)
    Ss = skmelSurv/(skmelProlif+skmelDeath+skmelMig+skmelSurv)
    Ph = hacatProlif/(hacatProlif+hacatDeath+hacatMig+hacatSurv)
    Dh = hacatDeath/(hacatProlif+hacatDeath+hacatMig+hacatSurv)
    Mh = hacatMig/(hacatProlif+hacatDeath+hacatMig+hacatSurv)
    Sh = hacatSurv/(hacatProlif+hacatDeath+hacatMig+hacatSurv)
    
    
    return Ps,Ds,Ms,Ss,Ph,Dh,Mh,Sh #,net_skmel,net_hacat


def updateMicroEnvironment(SPC,MEL,KCT):
    
    '''
    Input
        SPC: number of empty neighbors (int)
        MEL: number of vertex occupied by skmel (int)
        KCT: number of vertex occupied by hacat (int)
    Processing
        This function update the boolean expressions that describes the tolerance to high density
    Output
        migration: condition to cell migrate (boolean)
        proliferation: condition to cell proliferate (boolean)
        
    '''
    
    migration = (MEL <= SPC) or (MEL <= KCT)
    proliferation = (MEL >= SPC) or (MEL >= KCT)
      
    return migration, proliferation
    

def getCorrelation(dataSimulation):
    
    skmelPS, _ = pearsonr(dataSimulation['survS'],dataSimulation['prolS'])
    skmelPM, _ = pearsonr(dataSimulation['migS'],dataSimulation['prolS'])
    skmelPD, _ = pearsonr(dataSimulation['deathS'],dataSimulation['prolS'])
    hacatPS, _ = pearsonr(dataSimulation['survH'],dataSimulation['prolH'])
    hacatPM, _ = pearsonr(dataSimulation['migH'],dataSimulation['prolH'])
    hacatPD, _ = pearsonr(dataSimulation['deathH'],dataSimulation['prolH'])
    
    return skmelPS,skmelPM,skmelPD,hacatPS,hacatPM,hacatPD
