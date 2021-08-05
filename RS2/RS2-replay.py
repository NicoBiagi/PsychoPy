#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 11:17:27 2021

@author: nicobiagi
"""

try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass
# Import modules
import os, re
import glob
import pandas as pd
import numpy as np
import matplotlib as mpl
from psychopy import visual, core, event
import statistics, math
import platform
from psychopy.hardware import keyboard

key_resp = keyboard.Keyboard()
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []

# suppres sceintific notation
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# detect Operatying System
os_name = platform.system()

# define the path depending on the OS
if (os_name == 'Darwin'):
    path = "/Users/nico/Documents/GitHub/PsychoPy/RS2"
    screenXpix=1400
    screenYpix=900
    
elif (os_name == 'Windows'):
    path = 'C:\\Users\\zj903545\\Documents\\GitHub\\PsychoPy\\RS2'
    screenXpix=1920
    screenYpix=1080
    
else:
    print('Error 404: os not found (?!)')

# change the current folder
os.chdir(path)

# load the csv file 
data = pd.read_csv('RS2-ID-8.csv')


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

# get the id 
id = pd.unique(data['ID'])

# get the tms location
tms = pd.unique(data['TMS_area'])

# get the session
session = pd.unique(data['session'])

responses=[]

for T in range(0,1):
    
    subset = data.loc[data['TMS_area'] == tms[T]]
    
    for S in range (0,1):
        
        subset2 = subset.loc[subset['session'] == session[S]]
        
        trials = pd.unique(subset2['trial_num'])
        txt_id = "Participant {}, TMS: {}, session: {}".format(id, tms[T], session[S])
        
        for N in range(0, 2):
            id_data = subset2.loc[subset2['trial_num'] == trials[N]]
            
            X = id_data["xp"]
            Y = id_data["yp"]
            
            X = X.dropna()
            Y = Y.dropna()
            
            X1 = X[X.index % 3 == 0]
            Y1 = Y[Y.index % 3 == 0]


            for z in range(0,len(X1)):
                
                dot_xys = []
                dot_x = round(X1.iloc[z])
                dot_x = (screenXpix/2)-dot_x
                dot_y = round(Y1.iloc[z])
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
                
                fix_dot =visual.ElementArrayStim(
                    win=win,
                    units="pix",
                    nElements=1,
                    elementTex=None,
                    elementMask="circle",
                    xys=[[0,0]],
                    sizes=20,
                    colors='red',
                    colorSpace='rgb'
                )
                
                txt = "Trial n: {}".format(trials[N])
                
                # define text for trial number that goes at the top of the screen
                text_trial = visual.TextStim(win=win, text=txt, pos=[0.0, 500.0])
                
                # define text for info about the task that goes at the bottom of the screen
                text_id = visual.TextStim(win=win, text=txt_id, pos=[0.0, -500.0])
                
                # draw the fixation dot
                fix_dot.draw()
                
                # draw the eye-movement dot
                dot_stim.draw()
                
                # draw the trial number text
                text_trial.draw()
                
                # draw the info text
                text_id.draw()
                
                # flip everything on the screen
                win.flip()
                
                continueRoutine = True
                while continueRoutine:    
                # wait for keypresses here
                    theseKeys = key_resp.getKeys(keyList=['left', 'right', 'q', 'space'], waitRelease=False)
                    _key_resp_allKeys.extend(theseKeys)
                    if len(_key_resp_allKeys):
                        key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                        key_resp.rt = _key_resp_allKeys[-1].rt 
                        responses.append(key_resp.keys)
                        continueRoutine= False
    
# close the screen
win.close()

