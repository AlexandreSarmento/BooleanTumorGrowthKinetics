"""

This is the script that call the functions that going to generate all of results presents in csv file, 
txt files and even the images in 6x6 inches and 300 dpi with arbitrary file
extensions. Below a general explanation of some importante variables. Further detail about the role of each 
function one might check the commentary into these functions scritps. Let me recall that I divided the code 
in a couple of modules harbouring some functions
 
1) nghVertexDict: dictionary where each focal cell address (tuple) are at key and the focal cell neighbors address (list of tuple) are at values
2) seedDict: dictionary of each seed cell adress (tuple) at keys and Skmel/Hacat object at value  
3) dataSimulation: two-dimensional numpy array where the columns represent the data bellows
dSdt: variation of skmel density over time
dHdt: variation of hacat density over time
N: variation of total population density over time
iter: arbitrary unit of time
prolS: skmel probability of proliferation
deathS: skmel probability of death
migS: skmel probability of migration
survSL skmel probability of survive
prolH: hacat probability of proliferation
deathH: hacat probability of death
migH: hacat probability of migration
survH: hacat probability of survive
4) framesSimulation: three dimensional numpy array which registrate the spatial dynamic of population over iterations
5) SkmelCurveFit: output of Skmel growth curve fit (list of floats)  
6) HacatCurveFit output of hacat growth curve fit (list of floats)
7) parameterSkmel: parameter estimated from skmel growth curve fit
8) parameterHacat: parameter estimated from hacat growth curve fit 
9) Coorelations among tumor growth dynamics:
    skmelPS: proliferation versus survival in skmel
    skmelPM: proliferation versus migration in skmel
    skmelPD: proliferation versus death in skmel
    hacatPS: proliferation versus survival in hacat
    hacatPM: proliferation versus migration in hacat
    hacatPD: proliferation versus death in hacat

10) df_dataSimulation: data frame with the simulation output data
11) the module settingInput are exporting to here entry variables to set simulation    
    
""" 

import os
import ABM
import graphics
import models
import neighbors
from settingInput import C0,nRowCols,dataFrameKeys,indexOfngh,paramsHacat,paramsSkmel,prolifCap
#import pandas as pd


if __name__ == "__main__":
    
    
    # let set working directory. Linux user shall be aware how to set the path which is different concerning to windows
    os.chdir(
            'C:\\Users\\Alexandre Sarmento\\Documents\\PYTHON\\UFRN\\BooleanKinetics'
            )
    # let set an specific directory to save results according to the parameters assigned to lambda 
    rootDir = "C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/"
    mainDir = "timeScale/alt/"
    paramsDir = ("C0_"+ str(C0)+
                 "_ngh_"+str(indexOfngh)+
                 "_rhoMaxMEL_"+str(prolifCap[0])+
                 "_rhoMaxKCT_"+str(prolifCap[1])+
                 "/")
    resultsDir = rootDir+mainDir+paramsDir
    # generate cell address and neighborhood cells address
    nghVertexDict = neighbors.makeNeighborsDicitionary(nrow = nRowCols,
                                                       ncol = nRowCols,
                                                       d = indexOfngh)
    # seed the cells at random through domain
    seedDict = neighbors.getCellsSeed(nghVertexDict,C0,prolifCap)
    # start the simulation and release the output
    [dataSimulation,framesSimulation,framesRhoMax] = ABM.CellularAutomata(seedDict,nghVertexDict)
    # make a numpy array and make a dictionary to ease the plots production
    dataSimulation = graphics.setDictionaryOfResults(dataSimulation,dataFrameKeys)
    # get the growth curve coming from simulation proceed with curve fit    
    [SkmelCurveFit,HacatCurveFit,parameterSkmel,parameterHacat] = graphics.makeCurveFit(dataSimulation,paramsHacat,paramsSkmel)
    # make the heatmap of spation dynamic
    graphics.makeHeatmap(dataSimulation,framesSimulation,framesRhoMax,prolifCap,resultsDir)
    # get all of data about probabilities, cells density and parameters estimated and make plots
    graphics.makePlots(dataSimulation,SkmelCurveFit,HacatCurveFit,resultsDir)
    # get the probabilities and calculate correlation among them
    [skmelPS,skmelPM,skmelPD,hacatPS,hacatPM,hacatPD] = models.getCorrelation(dataSimulation)
    # get the data about curve fit and correlation and save inside a txt file
    with open(resultsDir+"params.txt", "w") as file:
        
        file.write('Skmel - K: ' + str(parameterSkmel[0]) + ' rho: ' + str(parameterSkmel[1]) + ' tau: ' + str(parameterSkmel[2]) + "\n")
        file.write('Hacat - K: ' + str(parameterHacat[0]) + ' rho: ' + str(parameterHacat[1]) + ' tau: ' + str(parameterHacat[2]) + "\n")
        file.write('ratio K = ' + str(parameterHacat[0]/parameterSkmel[0]) +"\n")
        file.write('correlation proliferation versus survival in skmel: ' + str(skmelPS) + '\n')
        file.write('correlation prolifertion versus migration in skmel: ' + str(skmelPM) + '\n')
        file.write('correlation proliferation versus death in skmel: ' + str(skmelPD) + '\n')
        file.write('correlation proliferation versus survival in hacat: ' + str(hacatPS) + '\n')
        file.write('correlation prolifertion versus migration in hacat: ' + str(hacatPM) + '\n')
        file.write('correlation proliferation versus death in hacat: ' + str(hacatPD) + '\n')
    
    file.close()
    
    # # # convert a dictionary to a data frame and save all simulation data in a csv 
    # df_dataSimulation = pd.DataFrame(dataSimulation)
    # df_dataSimulation.columns = dataFrameKeys
    # df_dataSimulation.to_csv(
    #                          resultsDir+"timeserie.csv",
    #                          sep = ",",
    #                          encoding = "utf-8",
    #                          header = True,
    #                          index = False   
    #                         )