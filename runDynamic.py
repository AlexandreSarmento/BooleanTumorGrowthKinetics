# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 10:53:28 2023

@author: Alexandre Sarmento
"""

import os
import neighbors,ABM
import graphics
#from scipy.stats import pearsonr
from settingInput import rangeHacat,dataFrameKeys,nghVertexDict
import pandas as pd

if __name__ == "__main__":
    

    os.chdir(
            'C:\\Users\\Alexandre Sarmento\\Documents\\PYTHON\\UFRN\\BooleanKinetics'
            )
 
    paramsDict = dict()
    C0 = []
    rho_skmel = []
    tau_skmel = []
    rho_hacat = []
    tau_hacat = []
    for loop in range(len(rangeHacat)):
        print('loop: ',loop)
        
        resultsDir = "C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/Hipo1/"+"H_"+str(rangeHacat[loop])+"/"
        seedDict = neighbors.getCellsSeed(nghVertexDict,rangeHacat[loop])
        [dataSimulation,framesSimulation] = ABM.CellularAutomata(seedDict,nghVertexDict)
        graphics.makeHeatmap(framesSimulation,resultsDir)
        

        df_dataSimulation = pd.DataFrame(dataSimulation)
        df_dataSimulation.columns = dataFrameKeys
        df_dataSimulation.to_csv(
                                 resultsDir+"results.csv",
                                 sep = ",",
                                 encoding = "utf-8",
                                 header = True,
                                 index = False   
                                )

        dataSimulation = graphics.setDictionaryOfResults(dataSimulation)
        [SkmelCurveFit,HacatCurveFit,parameterSkmel,parameterHacat] = graphics.makeCurveFit(dataSimulation)
        C0.append(rangeHacat[loop] + (rangeHacat[loop]/10))
        rho_skmel.append(parameterSkmel[1])
        tau_skmel.append(parameterSkmel[2])
        rho_hacat.append(parameterHacat[1])
        tau_hacat.append(parameterHacat[2])
        paramsDict['C0'] = C0
        paramsDict['rho_skmel'] = rho_skmel
        paramsDict['tau_skmel'] = tau_skmel
        paramsDict['rho_hacat'] = rho_hacat
        paramsDict['tau_hacat'] = tau_hacat
        graphics.makePlots(dataSimulation,SkmelCurveFit,HacatCurveFit,resultsDir)
    
df = pd.DataFrame(paramsDict) 
df.to_csv(
          "C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/Hipo1/parameters.csv",
          sep='\t', 
          encoding='utf-8',
          index=False
         )
    
    # corrH, _ = pearsonr(HacatCurveFit,dataSimulation['dHdt'])
    # print("correlation model experiment hacat: ",corrH)
    # corrS, _ = pearsonr(SkmelCurveFit,dataSimulation['dSdt'])
    # print("correlation model experiment skmel: ",corrS)