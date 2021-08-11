#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:36:33 2021

@author: nicobiagi
"""
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

import os, re
import glob
import pandas as pd
import numpy as np
import matplotlib as mpl
import statistics, math
import platform

# suppres sceintific notation
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# detect Operatying System
os_name = platform.system()

# define the path depending on the OS
if (os_name == 'Darwin'):
    path = "/Users/nico/Documents/GitHub/PsychoPy/RS2"

    
elif (os_name == 'Windows'):
    path = 'C:\\Users\\zj903545\\Documents\\GitHub\\PsychoPy\\RS2'

    
else:
    print('Error 404: os not found (?!)')

# change the current folder
os.chdir(path)

extension  = 'csv'

myOnDict = []
result = glob.glob('*.{}'.format(extension))

res = [x for x in result if re.search('ID', x)]

res.sort()

final = pd.DataFrame()

for x in range(0,len(res)):
    
    # select the
    file = res[x]

    # load the csv file 
    data = pd.read_csv(file)
    
    print(file)
    
    # get the id 
    id = pd.unique(data['ID'])
    
    # get the tms location
    tms = pd.unique(data['TMS_area'])
    
    # get the session
    session = pd.unique(data['session'])
    
    
    response=pd.DataFrame() 
    filtering =[]
    pixPerDeg = 42.2238
    xCenter = 960
    yCenter = 540
    
    for T in range(0,len(tms)):
        
        subset = data.loc[data['TMS_area'] == tms[T]]
        
        for S in range (0,len(session)):
            
            subset2 = subset.loc[subset['session'] == session[S]]
            
            trials = pd.unique(subset2['trial_num'])
            
            for N in range(0, len(trials)):
                id_data = subset2.loc[subset2['trial_num'] == trials[N]]
                
                wing = pd.unique(id_data['wing_type'])[0]
                loc = pd.unique(id_data['stim_loc'])[0]
                shft_len = pd.unique(id_data['shft_len'])[0]
                
                
                end_xys = []
                endX = round(shft_len *2 * pixPerDeg)
                endY = yCenter
                Y_range_min = endY - pixPerDeg
                Y_range_max = endY + pixPerDeg
                
                
                if wing == 0: # flat |-|
                    if loc == -1:
                        endX = xCenter-endX
                        range_min = endX - pixPerDeg
                        range_max = endX + pixPerDeg
                        end_xys = id_data[(id_data['xp'] >= range_min) & (id_data['xp'] <= range_max)]
                        end_xys = end_xys[(end_xys['yp'] >= Y_range_min) & (end_xys['yp'] <= Y_range_max)]
                        
                    elif loc == 0:
                        endX = xCenter + endX
                        range_min = endX - pixPerDeg
                        range_max = endX + pixPerDeg
                        end_xys = id_data[(id_data['xp'] >= range_min) & (id_data['xp'] <= range_max)]
                        end_xys = end_xys[(end_xys['yp'] >= Y_range_min) & (end_xys['yp'] <= Y_range_max)]
    
                
                elif wing ==-1: #inward <->
                    if loc ==-1: # left
                        endX = xCenter-endX
                        range_min = endX - pixPerDeg
                        range_max = endX + (2*pixPerDeg)
                        end_xys = id_data[(id_data['xp'] >= range_min) & (id_data['xp'] <= range_max)]
                        end_xys = end_xys[(end_xys['yp'] >= Y_range_min) & (end_xys['yp'] <= Y_range_max)]
    
                        
                    elif loc ==0: # right
                        endX = xCenter + endX
                        range_min = endX - (2*pixPerDeg)
                        range_max = endX + pixPerDeg
                        end_xys = id_data[(id_data['xp'] > (endX-(2*pixPerDeg))) & (id_data['xp'] < (endX+pixPerDeg))]
                        end_xys = end_xys[(end_xys['yp'] >= Y_range_min) & (end_xys['yp'] <= Y_range_max)]
    
                        
                elif wing == 1: # outward >-<
                    if loc == -1: # left
                        endX = xCenter-endX
                        range_min = endX - (2*pixPerDeg)
                        range_max = endX + pixPerDeg
                        end_xys = id_data[(id_data['xp'] >= range_min) & (id_data['xp'] <= range_max)]
                        
                    elif loc == 0:
                        endX = xCenter + endX
                        range_min = endX - pixPerDeg
                        range_max = endX + (2*pixPerDeg)
                        end_xys = id_data[(id_data['xp'] > (endX-(2*pixPerDeg))) & (id_data['xp'] < (endX+pixPerDeg))]
                
            
                        
                # append the dataframe to the filtering dataframe
                response = response.append(end_xys)
                
    final = final.append(response)
                
    # save the new filtering dataframe
final.to_csv('RS2-filtering_new.csv', index=False)


                
                

          
