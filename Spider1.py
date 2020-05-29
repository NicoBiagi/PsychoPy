# =============================================================================
# Template for an exmperiment
# =============================================================================
from psychopy import visual, core, event
# create a new window in fullscreen
win = visual.Window(fullscr=True, color='black', units="pix", screen = 1)

# ake the mouse invisible
win.mouseVisible = False

# text we want to present 
text = visual.TextStim(win, text='Press spacebar to start the trial', color='red', height=30)

# draw the text
text.draw()

# flip it on the screen
win.flip()

# wait for the key press
event.waitKeys(keyList=['space'])
 
# 60 frames per second, 120 for 2 seconds
nframes = 120

# Empty the keypresses list
keys = None

# create the circle
bubble = visual.Circle(win, lineColor='white', radius=30, pos=[0,0])

# get the time
clock = core.Clock()

# reset the time
clock.reset()

# set a variable equal to 0, to see how many times the circle is presented
tit = 0
# =============================================================================
# # in case we want to use the clock
# while clock.getTime() < 2:
# =============================================================================
# in case we want the number of frames to control the timings of the presentation
for x in range(nframes):
        # update the coordinates of the circle
        bubble.pos = [x+1 for x in bubble.pos]
      
        # draw the circle
        bubble.draw()
        
        # flip it on the screen
        win.flip()
        
        # update the number of frames
        tit = tit+1
        
# =============================================================================
#         # in case we want to use the key-press
#         keys = event.waitKeys(keyList=['space', 'escape'])
# =============================================================================
 
# close the window
win.close()

# make the mouse visible again
win.mouseVisible = True