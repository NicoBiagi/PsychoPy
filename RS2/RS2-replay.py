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

# clear the console
os.system('clear')

# suppres sceintific notation
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# load the csv file 
data = pd.read_csv('RS2-ID-8.csv')
#data = pd.read_csv('RS2-replay.csv')

X = data["xp"]

remove = round(len(X)*0.75)

X = X[:-remove]
X = X[X.index % 3 == 0]  # Selects every 3rd raw starting from 0

Y = data["yp"]
Y = Y[:-remove]
Y = Y[Y.index % 3 == 0]


screenXpix=1920
screenYpix=1080
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

for z in range(1,200):
    
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

