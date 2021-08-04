#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 11:17:27 2021

@author: nicobiagi
"""

# clear the variable explorer
#%reset -f

# Import modules
import os, re
import glob
import pandas as pd
import numpy as np
import matplotlib as mpl
from psychopy import visual, core, event
import statistics, math
import platform

# clear the console
os.system('clear')

# suppres sceintific notation
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# detect Operatying System
os_name = platform.system()

# define the path depending on the OS
if (os_name == 'Darwin'):
    path = '/Users/nico/OneDrive - University of Reading/PhD/Undergraduate Project/2nd Project/Script'
    screenXpix=1400
    screenYpix=900
    
elif (os_name == 'Windows'):
    path = 'C:\\Users\\zj903545\\Documents\\GitHub\\PsychoPy\\RS2'
    screenXpix=1920
    screenYpix=1080
    
else:
    print('Error 404 os not found (?!)')

# change the current folder
os.chdir(path)

# load the csv file 
data = pd.read_csv('RS2-ID-8.csv')

X = data["xp"]

remove = round(len(X)*0.75)

X = X[:-remove]
X = X[X.index % 3 == 0]  # Selects every 3rd raw starting from 0

Y = data["yp"]
Y = Y[:-remove]
Y = Y[Y.index % 3 == 0]

# create a new window in fullscreen
win = visual.Window(
    size = [screenXpix, screenYpix], 
    color='black', 
    units="pix", 
    screen = 1, 
    fullscr = True, 
    allowGUI = False)


# make the mouse invisible
win.mouseVisible = False

# get the tms location
tms = pd.unique(data['TMS_area'])

# get the session
session = pd.unique(data['session'])


for T in range(0,1):
    
    subset = data.loc[data['TMS_area'] == tms[T]]
    
    for S in range (0,1):
        
        subset2 = subset.loc[subset['session'] == session[S]]
        
        trials = pd.unique(subset2['trial_num']) 
        
        for N in range(0, 1):
            
            id_data = subset2.loc[subset2['trial_num'] == trials[N]]
    

            for z in range(0,len(id_data)):
                
                dot_xys = []
                dot_x = round(X.iloc[z])
                dot_x = (screenXpix/2)-dot_x
                dot_y = round(Y.iloc[z])
                dot_y = (screenYpix/2)-dot_y
                
                dot_xys.append([dot_x, dot_y])
            
                dot_stim = visual.ElementArrayStim(
                    win=win,
                    units="pix",
                    nElements=len(dot_xys),
                    elementTex=None,
                    elementMask="circle",
                    xys=dot_xys,
                    sizes=20,
                    colors='white',
                    colorSpace='rgb'
                )
            
                dot_stim.draw()
                # flip to the screen
                win.flip()
                #wait 1 second

    
    
# close the screen
win.close()

