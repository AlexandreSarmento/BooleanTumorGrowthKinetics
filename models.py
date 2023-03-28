# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 14:07:38 2022

@author: Alexandre Sarmento
"""

import numpy as np

def Velhurst(t,CC,rho,tau):
    
    return CC/(1 + np.exp(-rho*(t-tau))) 

