# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 15:10:44 2023

@author: Alexandre Sarmento
"""

import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import os
import matplotlib.colors
from scipy.optimize import curve_fit
import models
from settingInput import time,initialGuessHacat,initialGuessSkmel,dataFrameKeys
import matplotlib.patches as mpatches
import matplotlib.lines as mlines


def makeHeatmap(framesSimulation,resultsDir): 
    
    colors= ["white", "blue", "red"]
    cmap =  matplotlib.colors.ListedColormap(colors)
      
    for loop in range(len(framesSimulation)):
        
        if not os.path.exists(resultsDir):
            os.makedirs(resultsDir)
        else:
            pass

        
        fig, ax = plt.subplots()    
        plt.figure(figsize=(6,3.7),dpi=300)
        plt.imshow(framesSimulation[loop],cmap=cmap,interpolation='none', vmin=0, vmax=2)
        plt.text(0,0,"t = "+ str('{:.1f}'.format(time[loop])), fontsize=10)
        plt.axis('off')
        figsName = resultsDir+"fig"+str(loop)+".tiff"
        plt.savefig(figsName)
        plt.close()
    
        csvName = resultsDir+"matrix"+str(loop)+".csv"
        df = pd.DataFrame(framesSimulation[loop],range(len(framesSimulation[loop]))).astype(int)
        df.to_csv(
                 csvName,
                 sep=",",
                 encoding='utf-8',
                 header=False,
                 index= False   
                 )


def makePlots(dataSimulation,SkmelCurveFit,HacatCurveFit,resultsDir):
    
    
    if not os.path.exists(resultsDir):
        os.makedirs(resultsDir)
    else:
        pass

    prol = mlines.Line2D([],[],color='black',marker='o',markersize=4,label='proliferation')
    die = mlines.Line2D([],[],color='black',marker='P',markersize=4,label='death')
    mig = mlines.Line2D([],[],color='black',marker='>',markersize=4,label='migration')
    red_patch = mpatches.Patch(color='red', label='HaCaT')
    blue_patch = mpatches.Patch(color='blue', label='SK-MEL-147')
    legend_elements = [red_patch,blue_patch,prol,die,mig]

    ''' 
    Plot Hacat/Skmel Ratio 
    '''
    plt.figure(figsize=(6,3.7),dpi=300)
    plt.plot(time,dataSimulation['ratio'],'--ok',linewidth=2,markersize=10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.title('Cell Frequency Ratio',fontsize=8)
    plt.xlabel('time (days)', fontsize=8)
    plt.ylabel('Frequency ratio(Hacat/Skmel)', fontsize=8)
    plt.savefig(resultsDir+"densityRatio.tiff")

    ''' 
    Plot Tumor Growth Kinetics (Skmel) 
    '''
   
    plt.figure(figsize=(6,3.7),dpi=300)
    plt.plot(time,dataSimulation['prolS'],'--bo',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.plot(time,dataSimulation['deathS'],'--bP',linewidth=2, markersize=10,markeredgecolor = 'black')
    plt.plot(time,dataSimulation['migS'],'--b>',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.plot(time,dataSimulation['prolH'],'--ro',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.plot(time,dataSimulation['deathH'],'--rP',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.plot(time,dataSimulation['migH'],'--r>',linewidth=2, markersize=10,markeredgecolor = 'black')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(handles=legend_elements,loc="center left")
    plt.xlabel('time (days)', fontsize=8)
    plt.ylabel('Probability of Tumor Growth Kinetics', fontsize=8)
    plt.savefig(resultsDir+"Kinetics.tiff")


    ''' 
    Plot Growth Curves
    '''

    plt.figure(figsize=(6,3.7),dpi=300)
    plt.plot(time,dataSimulation['dSdt'],'ob',markersize=10,label = "Skmel")
    plt.plot(time,dataSimulation['dHdt'],'or',markersize=10,label = "Hacat")
    plt.plot(time,SkmelCurveFit,'b--',label = "model fit to Skmel Curve")
    # ,label= r'model fit: K=%5.3f, $\rho$=%5.3f, $\tau$=%5.3f' % tuple(paramS)
    plt.plot(time,HacatCurveFit,'r--',label = "model fit to Hacat Curve")
    # ,label= r'model fit: K=%5.3f, $\rho$=%5.3f, $\tau$=%5.3f' % tuple(paramH)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend(loc="upper left",fontsize=8)
    #plt.title('Co-culture',fontsize=14)
    plt.xlabel('time (days)', fontsize=8)
    plt.ylabel('cells frequency', fontsize=8)
    plt.savefig(resultsDir+"GrowthCurveCurveFit.tiff")


def setDictionaryOfResults(dataSimulation):
    
    
    newDict = dict()
    count = 0
    for loop in dataFrameKeys: 
        newDict[loop] = dataSimulation[:,count]
        count = count + 1
        
    
    return newDict



def makeCurveFit(dataSimulation):
    
    models.Velhurst = np.vectorize(models.Velhurst) # here we shall vectorize the output of Velhust model
    # get the parameter values through curve fit with least square method to each subpopulation
    
    parameterSkmel = []
    parameterHacat = []
    parameterSkmel,_ = curve_fit(models.Velhurst,time,dataSimulation['dSdt'],initialGuessSkmel) 
    parameterHacat,_ = curve_fit(models.Velhurst,time,dataSimulation['dHdt'],initialGuessHacat)
    print('Skmel - K: ',parameterSkmel[0],' rho: ', parameterSkmel[1],' tau: ', parameterSkmel[2])
    print('Hacat - K: ',parameterHacat[0],' rho: ',parameterHacat[1],' tau: ',parameterHacat[2])
    print('ratio K = ',parameterHacat[0]/parameterSkmel[0])
    
               
    return models.Velhurst(time,*parameterSkmel), models.Velhurst(time,*parameterHacat),parameterSkmel,parameterHacat