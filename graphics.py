"""

This module contain functions that generates heatmaps, plot the growth curves of
populations, probabilities of population growth dynamic and make curve fit


"""

import numpy as np
import pandas as pd
import os
import matplotlib.colors
from scipy.optimize import curve_fit
import models
import matplotlib.lines as mlines
import matplotlib.pyplot as plt


def makeHeatmap(dataSimulation,framesSimulation,framesRhoMax,prolifCap,resultsDir): 
    
    colors= ["white", "blue", "red"]
    cmap =  matplotlib.colors.ListedColormap(colors)
    tempo = dataSimulation['iter']
    
    for loop in range(len(framesSimulation)):
        
        if not os.path.exists(resultsDir):
            os.makedirs(resultsDir)
        else:
            pass

        fig, ax = plt.subplots()    
        plt.figure(figsize=(6,6),dpi=300)
        plt.imshow(framesSimulation[loop],cmap=cmap,interpolation='none', vmin=0, vmax=2)
        plt.text(2,25,"t = "+ str('{:}'.format(tempo[loop])), fontsize=16)
        plt.axis('off')
        plt.grid()
        figsName = resultsDir+"fig"+str(loop+1)+".png"
        plt.savefig(figsName)
        plt.close()
    
        csvName = resultsDir+"matrix"+str(loop)+".csv"
        df = pd.DataFrame(framesSimulation[loop],
                          range(len(framesSimulation[loop]))).astype(int)
        df.to_csv(
                  csvName,
                  sep=",",
                  encoding='utf-8',
                  header=False,
                  index= False   
                  )
        
        fig, ax = plt.subplots()    
        plt.figure(figsize=(6,6),dpi=300)
        plt.imshow(framesRhoMax[loop],cmap='PiYG',interpolation='none', vmin=-1, vmax=max(prolifCap))
        plt.text(2,25,"t = "+ str('{:}'.format(tempo[loop])), fontsize=16)
        plt.axis('off')
        plt.grid()
        plt.colorbar()
        figsName = resultsDir+"RhoMax"+str(loop+1)+".png"
        plt.savefig(figsName)
        plt.close()
    

def makePlots(dataSimulation,SkmelCurveFit,HacatCurveFit,resultsDir):
    
    # dataSimulation,SkmelCurveFit,HacatCurveFit,resultsDir
    
    if not os.path.exists(resultsDir):
        os.makedirs(resultsDir)
    else:
        pass

    prol = mlines.Line2D([],[],
                         color='black',
                         marker='o',
                         markersize=8,
                         label='proliferation')
    die = mlines.Line2D([],[],
                        color='black',
                        marker='P',
                        markersize=8,
                        label='death')
    mig = mlines.Line2D([],[],
                        color='black',
                        marker='>',
                        markersize=8,
                        label='migration')
    surv = mlines.Line2D([],[],
                         color='black',
                         marker='s',
                         markersize=8,
                         label='survive')
    legend_elements = [prol,die,mig,surv]


    ''' 
    Plot Tumor Growth Probabilities (Skmel) 
    '''
    
    plt.figure(figsize=(6,6),dpi=300)
    plt.plot(dataSimulation['iter'],dataSimulation['prolS'],'--bo',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['deathS'],'--bP',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['migS'],'--b>',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['survS'],'--bs',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(handles=legend_elements,loc="best")
    plt.xlabel('time (A.U.)', fontsize=12)
    plt.ylabel('Probability of MEL growth dynamics',fontsize=12)
    plt.savefig(resultsDir+"SkmelKinetics.png")
    
    ''' 
    Plot Tumor Growth Probabilities (Hacat) 
    '''
    
    plt.figure(figsize=(6,6),dpi=300)
    plt.plot(dataSimulation['iter'],dataSimulation['prolH'],'--ro',linewidth=1,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['deathH'],'--rP',linewidth=1,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['migH'],'--r>',linewidth=1,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['survH'],'--rs',linewidth=1,markersize=10,markeredgecolor = 'black')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(handles=legend_elements,loc="best")
    plt.xlabel('time (A.U.)', fontsize=12)
    plt.ylabel('Probability of KCT growth dynamics', fontsize=12)
    plt.savefig(resultsDir+"HacatKinetics.png")

    ''' 
    Plot Growth Curves
    '''

    plt.figure(figsize=(6,6),dpi=300)
    plt.plot(dataSimulation['iter'],dataSimulation['dSdt'],'bo',linewidth=1,
                  markersize=10,markeredgecolor = 'black',label = "MEL")
    plt.plot(dataSimulation['iter'],dataSimulation['dHdt'],'ro',linewidth=1,
                  markersize=10,markeredgecolor = 'black',label = "KCT")
    plt.plot(dataSimulation['iter'],SkmelCurveFit,'b--',label = "model fit to MEL Curve")
    plt.plot(dataSimulation['iter'],HacatCurveFit,'r--',label = "model fit to KCT Curve")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(loc="best",fontsize=12)
    plt.xlabel('time (A.U)', fontsize=12)
    plt.ylabel('Density of cells (A.U)', fontsize=12)
    plt.grid()
    plt.savefig(resultsDir+"GrowthCurveCurveFit.png")
    

def setDictionaryOfResults(dataS,dataFrameKeys):
    
    output = dict()
    count = 0
    for loop in dataFrameKeys: 
        output[loop] = dataS[:,count]
        count += 1
        
    return output


def makeCurveFit(dataSimulation,paramsHacat,paramsSkmel):
    
    models.Velhurst = np.vectorize(models.Velhurst) # here we shall vectorize the output of Velhust model
    # get the parameter values through curve fit with least square method to each subpopulation
    
    parameterSkmel = []
    parameterHacat = []
    parameterSkmel,_ = curve_fit(models.Velhurst,dataSimulation['iter'],dataSimulation['dSdt'],paramsHacat) 
    parameterHacat,_ = curve_fit(models.Velhurst,dataSimulation['iter'],dataSimulation['dHdt'],paramsSkmel)
                   
    return models.Velhurst(dataSimulation['iter'],*parameterSkmel), models.Velhurst(dataSimulation['iter'],*parameterHacat),parameterSkmel,parameterHacat
