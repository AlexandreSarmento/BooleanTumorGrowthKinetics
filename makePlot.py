# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 16:07:59 2022

@author: Alexandre Sarmento
"""
import numpy as np
import panda as pd
from runDynamic import dataCube,dataKeys
import os
from scipy.optimize import curve_fit
import models
import matplotlib.pyplot as plt 

    
getDataMeans = np.mean(dataCube,axis=0)
getDataStd = np.std(dataCube,axis=0)
dataMeanDict = {}
dataStdDict = {}


for loopD in range(len(dataKeys)):
    
    dataMeanDict[dataKeys[loopD]] = getDataMeans[:,loopD]
    dataStdDict[dataKeys[loopD]] = getDataStd[:,loopD]


df = pd.DataFrame(dataMeanDict,range(len(dataMeanDict['time'])))
df.to_csv('C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/Alelopatia/cytokinetics.csv',sep=',',
           encoding='utf-8',decimal='.',float_format='%.4f',index=True)

plotsDir = "C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/Alelopatia/Testes6/"
if not os.path.exists(plotsDir):
    os.makedirs(plotsDir)
else:
    pass


''' 
Plot Growth Curves and curve fit
'''

# CC,rho,t,tau
time = dataMeanDict['time']
params0 = [0.3,0.1,0.1]
models.Velhurst = np.vectorize(models.Velhurst)
paramS,pcovS = curve_fit(models.Velhurst,time,dataMeanDict['dSdt'],params0)
paramH,pcovH = curve_fit(models.Velhurst,time,dataMeanDict['dHdt'],params0)
popSkmelFit = models.Velhurst(time,*paramS)
popHacatFit = models.Velhurst(time,*paramH)

plt.figure(figsize=(10,10))
plt.errorbar(time,dataMeanDict['dSdt'],yerr = dataStdDict['dSdt'],fmt = 'ob',markersize=10,label = "Skmel")
plt.errorbar(time,dataMeanDict['dHdt'],yerr = dataStdDict['dHdt'],fmt = 'or',markersize=10,label = "Hacat")
plt.plot(time,popSkmelFit,'b--',label= r'model fit: K=%5.3f, $\rho$=%5.3f, $\tau$=%5.3f' % tuple(paramS))
plt.plot(time,popHacatFit,'r--',label= r'model fit: K=%5.3f, $\rho$=%5.3f, $\tau$=%5.3f' % tuple(paramH))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc="center right",fontsize=14)
plt.title('Co-culture',fontsize=14)
plt.xlabel('time (A.U)', fontsize=14)
plt.ylabel('cell density (A.U)', fontsize=14)
plt.savefig(plotsDir+"GrowthCurveCurveFit.png")


''' 
Plot Hacat/Skmel Ratio 
'''
plt.figure(figsize=(10,10))
plt.errorbar(time,dataMeanDict['ratio'],yerr = dataStdDict['ratio'],fmt = '--ok',linewidth=2,markersize=10)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title('Cell Density Ratio',fontsize=14)
plt.xlabel('time (A.U)', fontsize=14)
plt.ylabel('density ratio(Hacat/Skmel)', fontsize=14)
plt.savefig(plotsDir+"densityRatio.png")

''' 
Plot Tumor Growth Kinetics (Skmel) 
'''

plt.figure(figsize=(10,10))
plt.errorbar(time,dataMeanDict['prolS'],yerr = dataStdDict['prolS'],fmt ='--bo',linewidth=2,
             markersize=10,markeredgecolor = 'black',label = "proliferation")
plt.errorbar(time,dataMeanDict['deathS'],yerr = dataStdDict['deathS'],fmt ='--bP',linewidth=2, 
             markersize=10,markeredgecolor = 'black',label = "death")
plt.errorbar(time,dataMeanDict['survS'],dataStdDict['survS'],fmt ='--bs',linewidth=2, 
             markersize=10,markeredgecolor = 'black',label = "survive")
plt.errorbar(time,dataMeanDict['migS'],dataStdDict['migS'],fmt ='--b>',linewidth=2, 
             markersize=10,markeredgecolor = 'black',label = "migration")
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc="upper right")
plt.title('Skmel Tumor Growth Kinetics',fontsize=14)
plt.xlabel('time (A.U)', fontsize=14)
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
plt.title('Hacat Tumor Growth Kinetics',fontsize=14)
plt.xlabel('time (A.U)', fontsize=14)
plt.ylabel('proportion of kinetics (A.U)', fontsize=14)
plt.savefig(plotsDir+"HacatKinetics.png")