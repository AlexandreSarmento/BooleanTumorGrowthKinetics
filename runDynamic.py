# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 15:39:35 2022

@author: Alexandre Sarmento
"""

'''
 This script is going to 
'''
import numpy as np
import matplotlib.pyplot as plt 
#import random
#import math
import pandas as pd
import os
import matplotlib.colors
from scipy.optimize import curve_fit
import neighbors,ABM
import models
from settingInput import squareSide,initialConditionSkmel,initialConditionHacat,\
                         numberOfSavedValues,dataFrameKeys,replicate

if __name__ == "__main__":
    
    os.chdir('C:\\Users\\Alexandre Sarmento\\Documents\\PYTHON\\UFRN\\BooleanKinetics')
    # C:\Users\Alexandre Sarmento\Documents\PYTHON\UFRN\BooleanKinetics

    # Generate a dicitionary of cells address and its neighbors address
    nghVertexDict = neighbors.makeNeighborsDicitionary(nrow = squareSide,ncol = squareSide)
    dataCube = np.empty((replicate,numberOfSavedValues,len(dataFrameKeys)))
    colors= ["white", "blue", "red"]
    cmap =  matplotlib.colors.ListedColormap(colors)
    framesDir = "C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/Test2/"
    time = list(range(1,9))
    for loopS in range(replicate):
        
        print(loopS)
        seedDict = neighbors.getCellsSeed(nghVertexDict,initialConditionSkmel,initialConditionHacat)
        [dataSimulation,framesSimulation] = ABM.CellularAutomata(seedDict,nghVertexDict)
        dataCube[loopS,:,:] = dataSimulation
            
        for loopF in range(len(framesSimulation)):
            
            traj = "traj"+str(loopS)+"/"
            framesPath = os.path.join(framesDir,traj) 
            if not os.path.exists(framesPath):
                os.makedirs(framesPath)
            else:
                pass

            
            fig, ax = plt.subplots()    
            plt.figure(figsize=(10,10))
            plt.imshow(framesSimulation[loopF],cmap=cmap,interpolation='none', vmin=0, vmax=2)
            plt.text(0,0,"t = "+ str('{:.1f}'.format(time[loopF])), fontsize=18)
            plt.axis('off')
            figsName = framesPath+"fig"+str(loopF)+".png"
            plt.savefig(figsName)
            plt.close()
            
            csvName = framesPath+"matrix"+str(loopF)+".csv"
            df = pd.DataFrame(framesSimulation[loopF],range(len(framesSimulation[loopF])))
            df.to_csv(
                csvName,
                sep=',',
                encoding='utf-8',
                decimal='.',
                float_format='%.4f',
                index=True
                )
        

    getDataMeans = np.mean(dataCube,axis=0)
    getDataStd = np.std(dataCube,axis=0)
    dataMeanDict = {}
    dataStdDict = {}


    for loopD in range(len(dataFrameKeys)):
        
        dataMeanDict[dataFrameKeys[loopD]] = getDataMeans[:,loopD]
        dataStdDict[dataFrameKeys[loopD]] = getDataStd[:,loopD]


    df = pd.DataFrame(dataMeanDict,range(len(dataMeanDict['time'])))
    df.to_csv(
        'C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/Test2/cytokinetics.csv',
         sep=',',
         encoding='utf-8',
         decimal='.',
         float_format='%.4f',
         index=True
         )

    plotsDir = "C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/Test2/"
    if not os.path.exists(plotsDir):
        os.makedirs(plotsDir)
    else:
        pass


    '''
    Curve fit
    '''
    # CC,rho,tau
    #time = [1,2,3,4,5,6,7,8]
    params0s = [0.8,1,4] # params0s: initial guess of parameter values to skmel (List of floats) 
    params0h = [0.2,1,4] # params0h: initial guess of parameter values to hacat (List of floats)
    parSrep = []
    parHrep = []
    models.Velhurst = np.vectorize(models.Velhurst) # here we shall vectorize the output of Velhust model
    # get the parameter values through curve fit with least square method to each subpopulation
    for kk in range(replicate): # dataCube[loopS,:,:]
        
        parsS,_ = curve_fit(models.Velhurst,time,dataCube[kk,:,0],params0s)
        parSrep.append(parsS)
        parsH,_ = curve_fit(models.Velhurst,time,dataCube[kk,:,1],params0h)
        parHrep.append(parsH)
    
    parSrepMean = np.mean(np.array(parSrep),axis=0)
    parSrepStd = np.std(np.array(parSrep),axis=0)
    print('Skmel - K: ',parSrepMean[0],'+/-',parSrepStd[0],' rho: ',
          parSrepMean[1],'+/-',parSrepStd[1],' tau: ',
          parSrepMean[2],'+/-',parSrepStd[2])
    parHrepMean = np.mean(np.array(parHrep),axis=0)
    parHrepStd = np.std(np.array(parHrep),axis=0)
    print('Hacat - K: ',parHrepMean[0],'+/-',parHrepStd[0],
          ' rho: ',parHrepMean[1],'+/-',parHrepStd[1],
          ' tau: ',parHrepMean[2],'+/-',parHrepStd[2])
    
    paramS,pcovS = curve_fit(models.Velhurst,time,dataMeanDict['dSdt'],params0s)
    paramH,pcovH = curve_fit(models.Velhurst,time,dataMeanDict['dHdt'],params0h)
    # get the output of adjusted model to each population
    popSkmelFit = models.Velhurst(time,*paramS)
    popHacatFit = models.Velhurst(time,*paramH)
    
    ''' 
    Plot Growth Curves
    '''
    
    plt.figure(figsize=(10,10))
    plt.errorbar(time,dataMeanDict['dSdt'],yerr = dataStdDict['dSdt'],
                 fmt = 'ob',markersize=10,label = "Skmel")
    plt.errorbar(time,dataMeanDict['dHdt'],yerr = dataStdDict['dHdt'],
                 fmt = 'or',markersize=10,label = "Hacat")
    plt.plot(time,popSkmelFit,'b--')
    # label= r'model fit: K=%5.3f, $\rho$=%5.3f, $\tau$=%5.3f' % tuple(paramS)
    plt.plot(time,popHacatFit,'r--')
    # ,label= r'model fit: K=%5.3f, $\rho$=%5.3f, $\tau$=%5.3f' % tuple(paramH)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(loc="upper left",fontsize=14)
    #plt.title('Co-culture',fontsize=14)
    plt.xlabel('time (days)', fontsize=14)
    plt.ylabel('cell density (A.U)', fontsize=14)
    plt.savefig(plotsDir+"GrowthCurveCurveFit.png")
    
    ''' 
    Plot Hacat/Skmel Ratio 
    '''
    plt.figure(figsize=(10,10))
    plt.errorbar(time,dataMeanDict['ratio'],yerr = dataStdDict['ratio'],
                 fmt = '--ok',linewidth=2,markersize=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.title('Cell Density Ratio',fontsize=14)
    plt.xlabel('time (days)', fontsize=14)
    plt.ylabel('density ratio(Hacat/Skmel)', fontsize=14)
    plt.savefig(plotsDir+"densityRatio.png")

    ''' 
    Plot Tumor Growth Kinetics (Skmel) 
    '''

    plt.figure(figsize=(10,10))
    plt.errorbar(time,dataMeanDict['prolS'],yerr = dataStdDict['prolS'],
                 fmt ='--bo',linewidth=2,markersize=10,markeredgecolor = 'black',label = "proliferation")
    plt.errorbar(time,dataMeanDict['deathS'],yerr = dataStdDict['deathS'],
                 fmt ='--bP',linewidth=2, markersize=10,markeredgecolor = 'black',label = "death")
    plt.errorbar(time,dataMeanDict['survS'],dataStdDict['survS'],
                 fmt ='--bs',linewidth=2, markersize=10,markeredgecolor = 'black',label = "survive")
    plt.errorbar(time,dataMeanDict['migS'],dataStdDict['migS'],
                 fmt ='--b>',linewidth=2,markersize=10,markeredgecolor = 'black',label = "migration")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(loc="upper right")
    #plt.title('Skmel Tumor Growth Kinetics',fontsize=14)
    plt.xlabel('time (days)', fontsize=14)
    plt.ylabel('proportion of kinetics (A.U)', fontsize=14)
    plt.savefig(plotsDir+"SkmelKinetics.png")


    ''' 
    Plot Tumor Growth Kinetics (hacat)
    '''

    plt.figure(figsize=(10,10))
    plt.errorbar(time,dataMeanDict['prolH'],yerr = dataStdDict['prolH'],fmt ='--ro',linewidth=2, 
                  markersize=10,markeredgecolor = 'black',label = "proliferation")
    plt.errorbar(time,dataMeanDict['deathH'],yerr = dataStdDict['deathH'],fmt ='--rP',linewidth=2, 
                  markersize=10,markeredgecolor = 'black',label = "death")
    plt.errorbar(time,dataMeanDict['survH'],dataStdDict['survH'],fmt ='--rs',linewidth=2, 
                  markersize=10,markeredgecolor = 'black',label = "survive")
    plt.errorbar(time,dataMeanDict['migH'],dataStdDict['migH'],fmt ='--r>',linewidth=2, 
                  markersize=10,markeredgecolor = 'black',label = "migration")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(loc="upper right")
    #plt.title('Hacat Tumor Growth Kinetics',fontsize=14)
    plt.xlabel('time (days)', fontsize=14)
    plt.ylabel('proportion of kinetics (A.U)', fontsize=14)
    plt.savefig(plotsDir+"HacatKinetics.png")