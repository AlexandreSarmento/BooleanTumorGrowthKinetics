# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 08:58:44 2023

@author: Alexandre Sarmento
"""

import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
#from scipy.stats import pearsonr,spearmanr

from scipy.stats import stats
#from scipy.stats import shapiro,kstest
#from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from bioinfokit.analys import stat


df_h1 = pd.read_csv(
    "C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/Hipo1/paramsH1.csv",
                )

df_h2 = pd.read_csv(
    "C:/Users/Alexandre Sarmento/Documents/PYTHON/UFRN/BooleanKinetics/Hipo2/paramsH2.csv",
                )

rho_df = pd.concat([df_h1[['rho_skmel_h1','rho_hacat_h1']].copy(),
                    df_h2[['rho_skmel_h2','rho_hacat_h2']].copy()], axis=1)
rho_df.columns=['rho_skmel_h1','rho_hacat_h1','rho_skmel_h2','rho_hacat_h2'] 


rho_melt = pd.melt(rho_df.reset_index(), 
                   id_vars=['index'], 
                   value_vars=['rho_skmel_h1','rho_hacat_h1','rho_skmel_h2','rho_hacat_h2'])
# replace column names
rho_melt.columns = ['index', 'treatments', 'value']

# 'rho_skmel_h1','rho_hacat_h1','rho_skmel_h2','rho_hacat_h2'

f, pvalue = stats.f_oneway(rho_df['rho_skmel_h1'], 
                                rho_df['rho_hacat_h1'],
                                rho_df['rho_skmel_h2'],
                                rho_df['rho_hacat_h2'])


# Ordinary Least Squares (OLS) model
model = ols('value ~ C(treatments)', data=rho_melt).fit()
anovaTable = sm.stats.anova_lm(model, typ=2)
print(anovaTable)

res = stat()
res.anova_stat(df=rho_melt, 
               res_var='value', 
               anova_model='value ~ C(treatments)')
print(res.anova_summary)


# perform multiple pairwise comparison (Tukey's HSD)
# unequal sample size data, tukey_hsd uses Tukey-Kramer test
res = stat()
res.tukey_hsd(df=rho_melt, 
              res_var='value', 
              xfac_var='treatments', 
              anova_model='value ~ C(treatments)')
print(res.tukey_summary)