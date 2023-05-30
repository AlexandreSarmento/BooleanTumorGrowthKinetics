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


def makeHeatmap(dataSimulation,framesSimulation,resultsDir): 
    
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


def makePlots(dataSimulation,SkmelCurveFit,HacatCurveFit,resultsDir):
    
    
    if not os.path.exists(resultsDir):
        os.makedirs(resultsDir)
    else:
        pass

    prol = mlines.Line2D([],[],color='black',marker='o',markersize=8,label='proliferation')
    die = mlines.Line2D([],[],color='black',marker='P',markersize=8,label='death')
    mig = mlines.Line2D([],[],color='black',marker='>',markersize=8,label='migration')
    surv = mlines.Line2D([],[],color='black',marker='s',markersize=8,label='survive')
    legend_elements = [prol,die,mig,surv]


    ''' 
    Plot Tumor Growth Kinetics (Skmel) 
    '''
    
    plt.figure(figsize=(6,6),dpi=300)
    plt.plot(dataSimulation['iter'],dataSimulation['prolS'],'--bo',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['deathS'],'--bP',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['migS'],'--b>',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['survS'],'--bs',linewidth=2,markersize=10,markeredgecolor = 'black')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(handles=legend_elements,loc="best")
    plt.xlabel('time (A.U.)', fontsize=8)
    plt.ylabel('Probability of SK-MEL-147 Growth Dynamics', fontsize=8)
    plt.savefig(resultsDir+"SkmelKinetics.png")
    
    '''
    Plot correlation among probabilities SK-MEL-147
    '''
    
    plt.figure(figsize=(6,6),dpi=300)
    plt.plot(dataSimulation['prolS'],dataSimulation['survS'],'--ko',linewidth=0.5,
             markersize=10,markeredgecolor = 'black',label = "proliferation vs survival")
    plt.plot(dataSimulation['prolS'],dataSimulation['deathS'],'--kP',linewidth=0.5,
             markersize=10,markeredgecolor = 'black',label = "proliferation vs death")
    plt.plot(dataSimulation['prolS'],dataSimulation['migS'],'--k>',linewidth=0.5,
             markersize=10,markeredgecolor = 'black',label = "proliferation vs migration")
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(loc="best")
    plt.xlabel('Probability of Proliferation', fontsize=10)
    plt.ylabel('Probability Migration,Survival,Death', fontsize=10)
    plt.savefig(resultsDir+"SkmelCorrelation.png")
    
    '''
    Plot correlation among probabilities HaCaT
    '''
    
    plt.figure(figsize=(6,6),dpi=300)
    plt.plot(dataSimulation['prolH'],dataSimulation['survH'],'--ko',linewidth=0.5,
             markersize=10,markeredgecolor = 'black',label = "proliferation vs survival")
    plt.plot(dataSimulation['prolH'],dataSimulation['deathH'],'--kP',linewidth=0.5,
             markersize=10,markeredgecolor = 'black',label = "proliferation vs death")
    plt.plot(dataSimulation['prolH'],dataSimulation['migH'],'--k>',linewidth=0.5,
             markersize=10,markeredgecolor = 'black',label = "proliferation vs migration")
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(loc="best")
    plt.xlabel('Probability of Proliferation', fontsize=10)
    plt.ylabel('Probability of Migration,Survival,Death', fontsize=10)
    plt.savefig(resultsDir+"HaCaTCorrelation.png")
    
    ''' 
    Plot Tumor Growth Kinetics (Hacat) 
    '''
    
    plt.figure(figsize=(6,6),dpi=300)
    plt.plot(dataSimulation['iter'],dataSimulation['prolH'],'--ro',linewidth=1,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['deathH'],'--rP',linewidth=1,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['migH'],'--r>',linewidth=1,markersize=10,markeredgecolor = 'black')
    plt.plot(dataSimulation['iter'],dataSimulation['survH'],'--rs',linewidth=1,markersize=10,markeredgecolor = 'black')
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(handles=legend_elements,loc="best")
    plt.xlabel('time (A.U.)', fontsize=10)
    plt.ylabel('Probability of HaCaT Growth Dynamics', fontsize=8)
    plt.savefig(resultsDir+"HacatKinetics.png")


    ''' 
    Plot Growth Curves
    '''

    plt.figure(figsize=(6,6),dpi=300)
    plt.plot(dataSimulation['iter'],dataSimulation['dSdt'],'bo',linewidth=1,
                 markersize=10,markeredgecolor = 'black',label = "SK-MEL-147")
    plt.plot(dataSimulation['iter'],dataSimulation['dHdt'],'ro',linewidth=1,
                 markersize=10,markeredgecolor = 'black',label = "HaCaT")
    plt.plot(dataSimulation['iter'],dataSimulation['N'],'--ko',linewidth=1,
                 markersize=10,markeredgecolor = 'black',label = "HaCaT+SK-MEL-147")
    plt.plot(dataSimulation['iter'],SkmelCurveFit,'b--',label = "model fit to Skmel Curve")
    plt.plot(dataSimulation['iter'],HacatCurveFit,'r--',label = "model fit to Hacat Curve")
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend(loc="best",fontsize=8)
    plt.xlabel('time (A.U)', fontsize=8)
    plt.ylabel('Density of cells (A.U)', fontsize=8)
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


# ''' 
# Plot Hacat/Skmel Ratio 
# '''
# plt.figure(figsize=(6,3.7),dpi=300)
# plt.plot(time,dataSimulation['ratio'],'--ok',linewidth=2,markersize=10)
# plt.xticks(fontsize=8)
# plt.yticks(fontsize=8)
# plt.title('Cell Frequency Ratio',fontsize=8)
# plt.xlabel('time (days)', fontsize=8)
# plt.ylabel('Frequency ratio(Hacat/Skmel)', fontsize=8)
# plt.savefig(resultsDir+"densityRatio.tiff")

# getMean = np.mean(datacube,axis=0)
# getStd = np.std(datacube,axis=0)
    # print('Skmel - K: ',parameterSkmel[0],' rho: ', parameterSkmel[1],' tau: ', parameterSkmel[2])
    # print('Hacat - K: ',parameterHacat[0],' rho: ',parameterHacat[1],' tau: ',parameterHacat[2])
    # print('ratio K = ',parameterHacat[0]/parameterSkmel[0])

#mig = mlines.Line2D([],[],color='black',marker='s',markersize=6,label='survive')
# red_patch = mpatches.Patch(color='red', label='HaCaT')
# blue_patch = mpatches.Patch(color='blue', label='SK-MEL-147')
# legend_elements = [red_patch,blue_patch,prol,die,mig]