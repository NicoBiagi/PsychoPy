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
import time
import keyboard as kb

# suppres sceintific notation
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# detect Operatying System
os_name = platform.system()

# define the path depending on the OS
if (os_name == 'Darwin'):
    path = "/Users/nico/Documents/GitHub/PsychoPy/RS2"
    screenXpix=1400
    screenYpix=900
    Xmultiplier=1400/1920
    Ymultiplier=900/1080
    
elif (os_name == 'Windows'):
    path = 'C:\\Users\\zj903545\\Documents\\GitHub\\PsychoPy\\RS2'
    screenXpix=1920
    screenYpix=1080
    Xmultiplier=1
    Ymultiplier=1
    
else:
    print('Error 404: os not found (?!)')

# change the current folder
os.chdir(path)

# load the csv file 
data = pd.read_csv('RS2-ID-1.csv')

final_filtering = pd.read_csv('RS2-filtering.csv')


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

response=[]
filtering =[]
pixPerDeg = 42.2238

for T in range(0,len(tms)):
    
    subset = data.loc[data['TMS_area'] == tms[T]]
    
    for S in range (0,len(session)):
        
        subset2 = subset.loc[subset['session'] == session[S]]
        
        trials = pd.unique(subset2['trial_num'])
        
        
        txt_id = "Participant {}, TMS: {}, session: {}".format(id[0], tms[T], session[S])
        
        
        for N in range(0, len(trials)):
            id_data = subset2.loc[subset2['trial_num'] == trials[N]]
            
            wing = pd.unique(id_data['wing_type'])[0]
            loc = pd.unique(id_data['stim_loc'])[0]
            shft_len = pd.unique(id_data['shft_len'])[0]
            
            if wing ==-1:
                wing_type = "outward"
            elif wing ==1:
                wing_type = "inward"
            elif wing==0:
                wing_type = "flat"
            
            end_xys = []
            endX = round(shft_len *2 * pixPerDeg)
            endY = 0.0
            if loc == -1:
                endX = -endX
            end_xys.append([endX, endY])
            
            X = id_data["xp"]
            Y = id_data["yp"]
            
            X = X.dropna()
            Y = Y.dropna()
            
            X1 = X[X.index % 3 == 0]
            Y1 = Y[Y.index % 3 == 0]
            
            
            z =0
            
            while True:
                
                if z >=len(X1):
                    break
                
                else:
                    dot_xys = []
                    dot_x = round(X1.iloc[z])
                    dot_x = round(dot_x * Xmultiplier)
                    dot_x = dot_x - (screenXpix/2)
                    dot_y = round(Y1.iloc[z])
                    dot_y = round(dot_y * Ymultiplier)
                    dot_y = dot_y - (screenYpix/2)
                    
                    
                    dot_xys.append([dot_x, dot_y])
                    z=z+1
                
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
                    
                    end_stim =visual.ElementArrayStim(
                        win=win,
                        units="pix",
                        nElements=1,
                        elementTex=None,
                        elementMask="circle",
                        xys=end_xys,
                        sizes=20,
                        colors='blue',
                        colorSpace='rgb'
                    )
                    
                    txt = "Trial n: {}, Wing type: {}".format(trials[N], wing_type)
                    
                    rsp_txt = "1: VALID, 2:MAYBE, 3: NOT VALID"
                    
                    # define text for trial number that goes at the top of the screen
                    text_trial = visual.TextStim(win=win, text=txt, pos=[0.0, 300])
                    
                    # define text for info about the task that goes at the bottom of the screen
                    text_id = visual.TextStim(win=win, text=txt_id, pos=[0.0, -300])
                    
                    # define text for response
                    rsp_text = visual.TextStim(win=win, text=rsp_txt, pos=[-(screenXpix/3), -300])
                    
                    # draw the fixation dot
                    fix_dot.draw()
                    
                    end_stim.draw()
                    
                    # draw the eye-movement dot
                    dot_stim.draw()
                    
                    # draw the trial number text
                    text_trial.draw()
                    
                    # draw the info text
                    text_id.draw()
                    
                    # draw the response info11
                    rsp_text.draw()
                    
                    # flip everything on the screen
                    win.flip()
            
                    try:
                        if kb.is_pressed('1'): # move forward
                            time.sleep(0.1)
                            response = response + ["valid"]
                            z=len(X1)
                            filtering.append([id[0], tms[T], session[S], trials[N], response[N]])
                            break
                        elif kb.is_pressed('2'): # move backwards
                            time.sleep(0.1)
                            response = response + ["maybe"]
                            z=len(X1)
                            filtering.append([id[0], tms[T], session[S], trials[N], response[N]])
                            break                        
                        elif kb.is_pressed('3'): # move backwards
                            time.sleep(0.1)
                            response = response + ["not_valid"]
                            z=len(X1)
                            filtering.append([id[0], tms[T], session[S], trials[N], response[N]])
                            break                        
                        elif kb.is_pressed('q'):
                            time.sleep(0.1)
                            break# quit
                            win.close()
                        elif kb.is_pressed('p'):
                            time.sleep(0.1)
                            while True:
                                try:
                                    if kb.is_pressed('p'):
                                        time.sleep(0.1)
                                        break
                                    else:
                                        pass
                                except:
                                    break
                        else:
                            pass
                    except:
                        break
# convert the list to a dataframe
df = pd.DataFrame(filtering)

# change the name of the columns
df.columns = ['ID', 'TMS_Area', 'Session', 'Trial_n', 'Validity']

# append the dataframe to the filtering dataframe
final_filtering = final_filtering.append(df)

# save the new filtering dataframe
final_filtering.to_csv('RS2-filtering.csv', index=False)

# close the screen
win.close()