# =============================================================================
# Template for an exmperiment
# =============================================================================
from psychopy import visual, core, event
from random import randint

# create a new window in fullscreen
win = visual.Window(size = [1920, 1080], color='black', units="pix", screen = 1, fullscr = False, allowGUI = False)

# ake the mouse invisible
win.mouseVisible = False

# text we want to present 
text = visual.TextStim(win, text='Press spacebar to start the trial', color='red', height=30, pos = [0,0])

# draw the text
text.draw()

# flip it on the screen
win.flip()

# wait for the key press
event.waitKeys(keyList=['space'])
 
# 60 frames per second, 120 for 2 seconds
nframes = 120

offset = [randint(1, 25) for p in range(0, 10)]
offset_rect = [randint(-940,-920) for p in range(0, 10)]



# get the time
clock = core.Clock()  



# set a variable equal to 0, to see how many times the circle is presented
tit = 0
# =============================================================================
# # in case we want to use the clock
# while clock.getTime() < 2:
# =============================================================================
# in case we want the number of frames to control the timings of the presentation
#for x in range(nframes):
    
keep_going = True



trials = 2

time = []

a = [1,2,3]

for x in range(trials):
    
    tit =offset[x]
    rect_off = offset_rect[x]
    
    # create the circle
    bubble = visual.Circle(win, lineColor='white', radius=7, pos=[0,0])
    square = visual.Rect(win=win, units="pix", width=bubble.radius *2, height=bubble.radius *2, fillColor=[1, -1, -1], lineColor = [1, -1,-1], pos = [rect_off, 0])
    
    # Empty the keypresses list
    keys = None
    
    # reset the time
    clock.reset()

    while keys == None:
        
        if bubble.pos[0] > ((-1920/2)+bubble.radius):
    
            # update the coordinates of the circle
            bubble.pos[0] = bubble.pos[0]-tit
                
        else:
            bubble.pos[0] = ((-1920/2)+bubble.radius)
            bubble.pos[1] = bubble.pos[1]+tit            
            if bubble.pos[1] > ((1920/2)-bubble.radius):
                bubble.pos[1] = ((1920/2)+bubble.radius)
        
        # convert the array back to a list
        bubble.pos = bubble.pos.tolist()
        
        # draw the square
        square.draw()
        
        # draw the circle
        bubble.draw()
            
        # flip it on the screen
        win.flip()
        
        keys = event.waitKeys(maxWait=0.05)
        
    # get the time elapsed in this trial
    time.append(clock.getTime())

    #draw the square
    square.draw()

    # give the feedback    
    bubble.draw()
    
    #display it for 0.5 s
    core.wait(0.5)
    
    # flip it on the screen
    win.flip()
     
# flip on the screen
win.flip()
        
# close the window
win.close()

# make the mouse visible again
win.mouseVisible = True