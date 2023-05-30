'''

This module harbour some model useful to whole simulation. 
The function Velhurst is the logistic model present at Morais et al 2017
The function updateProliferationProbability return population growth be in log phase
The function getCorrelation return the spearman correlation among tumor growth dynamic

'''

import numpy as np
from scipy.stats import pearsonr,spearmanr

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


def updateProliferationProbability(lamb,i):
    '''
    Input
        lamb: parameter lambda
        i: arbitrary unit of time
    Processing
        calculate the probability of the population growth be in log phase as a function of time

    Output
        probability of the population growth be in log phase
    '''
    
    return np.exp(-lamb*i)

# def updateProliferationProbability(lamb,i):
    
#     return np.exp(-lamb*i)


def getCorrelation(meanDict):
    
    skmelPS, _ = spearmanr(meanDict['prolS'],meanDict['survS'])
    skmelPM, _ = spearmanr(meanDict['prolS'],meanDict['migS'])
    skmelPD, _ = spearmanr(meanDict['prolS'],meanDict['deathS'])
    hacatPS, _ = spearmanr(meanDict['prolH'],meanDict['survH'])
    hacatPM, _ = spearmanr(meanDict['prolH'],meanDict['migH'])
    hacatPD, _ = spearmanr(meanDict['prolH'],meanDict['deathH'])
    
    return skmelPS,skmelPM,skmelPD,hacatPS,hacatPM,hacatPD



