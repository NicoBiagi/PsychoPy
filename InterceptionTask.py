# =============================================================================
# Intercept task: a moving-dot starts at the right side of the screen (random offset from the center of the screen)
# and moves towards the left side of the screen. A red dot sits in the left side of the screen (random offset from the center)
# Aim of the task is to make the moving-dot stop on top of the red square (by pressing any key).
# Extra thing: when the dot is closer than 10 pixel to the red square, it is not presented on the screen anymore
# =============================================================================
from psychopy import visual, core, event
from psychopy.hardware import keyboard
from random import randint
import pandas as pd
import numpy as np
from pandas import DataFrame
import psychopy.gui
from psychtoolbox import *


gui = psychopy.gui.Dlg()

gui.addField("Subject ID:")
gui.addField("Condition Num:")

gui.show()

sub_id = gui.data[0]
cond_num = int(gui.data[1])

screenXpix = 800
screenYpix = 600 


# create a new window in fullscreen
win = visual.Window(size = [screenXpix, screenYpix], color='black', units="pix", screen = 1, fullscr = False, allowGUI = False)

# ake the mouse invisible
win.mouseVisible = False

FINAL = []

#
kb = keyboard.Keyboard()

# text we want to present 
text = visual.TextStim(win, text='Welcome to the Interception task!\n Press spacebar to start the task', color='red', height=30, pos = [0,0])

# draw the text
text.draw()

# flip it on the screen
win.flip()

# wait for the key press
event.waitKeys(keyList=['space'])


win.flip()
#display it for 1 s
core.wait(1)

# reset the keyboard
keys= None
 
# 60 frames per second, 120 for 2 seconds
nframes = 120

# set the number of trials for this task
trials = 5

# create the starting offset for the dot
offset = [randint(1, 25) for p in range(trials)]

# create the offset for the square
offset_rect = [randint((screenXpix*0.7/2), ((screenXpix/2)-50)) for p in range(trials)]

# create a bunch of velocities for the dot
# velocity = [randint(1, 25) for p in range(trials)]
velocity = [2, 2, 2, 2, 2]

# get the time
clock = core.Clock()  

# set a variable equal to 0, to see how many times the circle is presented
tit = 0

# reset the time elapsed in each trial
time = []

# dot location at the end of the trial
dot_loc = []

square_loc =[]

square_coord =[]

fin_dist = []

dist_fin = []

trial_dist = []


for x in range(trials):
    
        
    # get the starting offest for the white dot
    tit =offset[x]
    
    # get the starting offset for the square
    rect_off = offset_rect[x]
    
    # get the velocity of the dot for this trial
    vel = velocity[x]
    
    # create the circle
    bubble = visual.Circle(win, lineColor='white',fillColor = "white", radius=7, pos=[(screenXpix/2)-(tit+7),0])
    
    # create the square
    square = visual.Rect(win=win, units="pix", width=bubble.radius*2, height=bubble.radius *2, fillColor="red", lineColor = "red", pos = [-rect_off, 0])
    
    # Empty the keypresses list
    keys = None
    
    # reset the time
    clock.reset()
    
    # this is the distnce between the moving-dot and the square
    distance = []

    # while keep_going:
    while not PsychHID('KbCheck')[0]:
        
        keys = None
        
        # update the x-ccordinate of the square, if the x-ccoridnate is not smaller than the screen
        if bubble.pos[0] >= ((-screenXpix/2)+bubble.radius):
    
            # update the coordinates of the circle
            bubble.pos[0] = bubble.pos[0]-vel
        # in case the x-ccordinate of the dot is smaller than the screen, 
        # we make it euqal to the screen and we make the dot go up       
        else:
            # make the x-ccordinate of the dot equal to the extreme left of the screen
            bubble.pos[0] = ((-screenXpix/2)+bubble.radius)
            
            # update the y-coordinate of the dot
            bubble.pos[1] = bubble.pos[1]+vel
            
            # if the y-coordinate is too big (i.e., is at the top of the screen),
            # we set the y-ccoridnate ot be equal to the top of the screen
            if bubble.pos[1] >= ((screenYpix/2)-bubble.radius):
                
                # make the y-coordinate of the dot be equal to the top of the screen
                bubble.pos[1] = ((screenYpix/2)-bubble.radius)
        
        # get the distance between the moving-dot and the square
        distance = bubble.pos[0] - square.pos[0]
        
        # convert the array back to a list
        bubble.pos = bubble.pos.tolist()
        
        # draw the square
        square.draw()
        
        # if the distance between the moving-dot and the square is smaller than 10 pix
        # we draw the square, otherwise we do not
        if not distance < 50:
        
            # draw the circle
            bubble.draw()
        
        # flip it on the screen
        win.flip()
        
        # check if the participant has pressed any key on the keyboard
        keys = kb.getKeys()
        
        if len(keys) > 0:
            keep_going = False
            keys = None
        
    # get the time elapsed in this trial
    time.append(clock.getTime())

    #draw the square
    square.draw()

    # give the feedback    
    bubble.draw()
    
    # get the final location of the dot
    dot_loc.append(bubble.pos)
    
    square_loc.append(square.pos[0])
    
    if bubble.pos[1] == 0 :
        if bubble.pos[0] >= 0:
            trial_dist = -bubble.pos[0] - square.pos[0]
        else:
             trial_dist = bubble.pos[0] - square.pos[0]
    else:
        trial_dist = bubble.pos[0] - square.pos[0] - bubble.pos[1]
    # pos value = early press, neg value= late press   
    fin_dist.append(trial_dist)
    
    # flip it on the screen
    win.flip()
    
    #display it for 1 s
    core.wait(1)
     
# flip on the screen
win.flip()
        
# close the window
win.close()

# make the mouse visible again
win.mouseVisible = True

ID = np.repeat(int(sub_id), trials, axis =0)

ID = DataFrame(ID, columns = ['ID'])

# convert the dot coordinates in a dataframe
dot_coordinates = DataFrame(dot_loc, columns = ['XCoordinate' , 'YCoordinate'])

velocity = DataFrame(velocity, columns =['Velocity'])

square_coord = DataFrame(square_loc, columns = ['SquareX'])

dist_fin = DataFrame(fin_dist, columns ='FinalDistance')

FINAL = pd.concat([ID, dot_coordinates, square_coord, velocity, dist_fin], axis = 1)

FINAL.to_csv('Final.csv', sep = ',', float_format='%.2f', index=False)
