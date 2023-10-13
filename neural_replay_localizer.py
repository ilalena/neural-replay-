#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from psychopy import locale_setup, gui, visual, core, data, event, logging, clock, constants, parallel
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import os  # handy system and path functions
import sys  # to get file system encoding
import random
from numpy.random import random, randint, normal, shuffle
import numpy as np
import fpstimer

path = os.getcwd()
timer = fpstimer.FPSTimer(120)


def wait(x):
  dur = int(x * 120)
  for i in range(dur):
    timer.sleep()
    
#def rest():
    #here is where code will live
    
triggerDict = {
           "eegStart": int(254),
           "eegEnd": int(255),
           "building": int(1),
           "animal": int(2),
           "furniture" : int(3),
           "tree": int(4),
           "bodypart2":int(5),
           "automobile":int(6),
           "handheldobj":int(7),
           "resp_up": int(31),
           "resp_down": int(32),
            "fix_ISI": int(50),
           "fix_ITI": int(51),
           "restStart": int(250),
           "restEnd": int(251)
           }
useTriggers = True #for debugging at home

if useTriggers is True:
    p_port = parallel.ParallelPort(address="0x4FF8")
    print("EEG trigger active.")
    
def eegTrigger(triggerType):
        """ Send trigger for EEG """
        #Tie to frame rate
        if useTriggers is True:
            parallel.setPortAddress(address="0x4FF8")
            p_port.setData(triggerType)
            wait(0.1)
            #core.wait(0.1) #changed from 0.001 to 0.1 ms
            p_port.setData(0)



# Store info about the experiment session
expName = u'eeg-localizer'  # from the Builder filename that created this script
expInfo = {'a. session': '01', 'b. participant': '', 'c. run': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = path + '/' + expInfo['b. participant'] + '/' + expInfo['b. participant'] + '_' + expName + '_' + expInfo['c. run'] + '_' + expInfo['date']
# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=path + u'/eeg_localizer.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# clocks
globalClock = core.Clock()
trialClock = core.Clock()
taskClock = core.Clock()
frameTolerance = 0.001 #just added
# Setup the Window
win = visual.Window(
    size=(1920, 1080), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=u'grey', colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 25.0  # could not measure, so guess

### image stimuli
images = [path + '/task_images/building.png',
                    path + '/task_images/animal.png',
                    path + '/task_images/furniture.png',
                    path + '/task_images/tree.png',
                    path + '/task_images/body_part.png',
                    path + '/task_images/automobile.png',
                    path + '/task_images/handheldobj.png'];
                    #path + '/stim/chair/chair_08s.jpg',
                    #path + '/stim/chair/chair_09s.jpg',
                    #path + '/stim/chair/chair_10sjpg'];
                    
image_names = ['building',
                                'animal',
                                'furniture',
                                'tree',
                                'body part',
                                'automobile',
                                'handheld object',];
                                #'chair_08',
                                #'chair_09',
                                #'chair_10'];

image_idx = [0,1,2,3,4,5,6];
###some task things
Instructions = visual.TextStim(win=win, name='Start',
    text=u'In this task you will see a series of images. Keep your eyes on the cross in the center of the screen. Each image will belong to a cateogry: animals, plants, buildings, body parts, handheld objects, furniture, or automobiles. Using the up and down arrow keys, indicate what category the image belongs to. \n\n When you are ready, press space to continue',
    font=u'Arial',
    pos=(0, 0), height=0.09, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

fixation = visual.TextStim(win=win, name='fixation',
    text=u'+',
    font=u'Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);
    
pathImage = visual.ImageStim(
    win=win, image= path + '/task_images/building',
    units='deg', pos=(0, 0), flipHoriz=False, 
    flipVert=False, name='outcome_low', autoLog=None)
    
response_one = visual.TextStim(win=win, name='response_up',
    text=u'response_one',
    font=u'Arial',
    pos=(0, 0.2), height=0.09, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);
    
response_two = visual.TextStim(win=win, name='response_dn',
    text=u'response_two',
    font=u'Arial',
    pos=(0, -0.2), height=0.09, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);
    
rest = visual.TextStim(win=win, name='response_dn',
    text=u'Take a short break',
    font=u'Arial',
    pos=(0, -0.2), height=0.09, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);
    
fin = visual.TextStim(win=win, name='response_dn',
    text=u'Thank you!',
    font=u'Arial',
    pos=(0, -0.2), height=0.09, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);
    
# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
#routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 
# set up handler to look after randomisation of conditions etc
#nTrials = 10
nTrials = 1

conditions=[]
for Idx in range (840): #trials
    conditions.append("chair")

trials = data.TrialHandler(nReps=nTrials, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=conditions,
    seed=None, name='trials')
    
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values

### INSTRUCTIONS ###
Instructions.draw()
win.flip()
paused = True # stop right here
while paused:
    if event.getKeys(keyList=['space']):
        paused = False
        taskClock.reset()
        T=0
        k = 0
    else:
        wait(0.05)

### DISPLAY FIXATION CROSS ###
for frame in range (120):
    fixation.draw()
    win.flip()


g = 0
start=core.getTime()
### TRIAL LOOP ###
for i in range(trials.nTotal):
    fixation.draw()
    win.flip()
    currentLoop = trials

    t = 0
    trialClock.reset()  
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_2 = event.BuilderKeyResponse()
    # keep track of which components have finished
    trialComponents = [p_port,key_resp_2, pathImage, fixation, response_one, response_two]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    pathImage.tStart = -1
    v = -1
    a = np.arange(7)
    shuffle(a)
    image_idx=a[0]
    other_idx=a[1]
    # -------Start Routine "trial"-------
    #while continueRoutine and routineTimer.getTime() > 0:
    if(core.getTime() -  start > 120): #breaks every 2 minutes
        print("2 mins") 
        rest.draw()
        win.flip()
        wait(30)
        start=core.getTime()
        i=i-1
        continueRoutine=False
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        
        tThisFlip = win.getFutureFlipTime(clock=trialClock) 
        tThisFlipGlobal = win.getFutureFlipTime(clock=None) 
        frameN = frameN + 1 

        timeLeft = 0
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        if p_port.status == NOT_STARTED and pathImage.status==STARTED: 
            # keep track of start time/frame for later
            p_port.frameNStart = frameN  # exact frame index
            p_port.tStart = t  # local t and not account for scr refresh
            p_port.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(p_port, 'tStartRefresh')  # time at next scr refresh
            p_port.status = STARTED
            win.callOnFlip(p_port.setData(1))
            print("Send trigger: 1 on line 166")
        if p_port.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > p_port.tStartRefresh + 0.1-frameTolerance:
                # keep track of stop time/frame for later
                p_port.tStop = t  # not accounting for scr refresh
                p_port.frameNStop = frameN  # exact frame index
                win.timeOnFlip(p_port, 'tStopRefresh')  # time at next scr refresh
                p_port.status = FINISHED
                win.callOnFlip(p_port.setData(0))
                print("Send trigger: 0 on line 176")
        if t >= 0.0 and (pathImage.status == NOT_STARTED):

            if pathImage.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance: # at least one key was pressed 
                pathImage.image = images[image_idx]
                pathImage.tStart = taskClock.getTime() 
                pathImage.status = STARTED

                pathImage.frameNStart = frameN  # exact frame index
                imgTime = int(round(np.random.uniform(200,400)/1000*120))
                print("img time" + str(imgTime))
                for frame in range(imgTime):
                    pathImage.draw()
                    timer.sleep()
                    if frame < 1 : #if frame is 0
                        #if port.status == NOT_STARTED and pathImage.status == STARTED:
                        if pathImage.status == STARTED:
                            if (pathImage.image == images[0]):
                                eegTrigger(triggerDict.get('building'))
                                print(triggerDict.get('building'))
                            elif (pathImage.image == images[1]):
                                eegTrigger(triggerDict.get('animal'))
                                print(triggerDict.get('animal'))
                            elif(pathImage.image == images[2]):
                                eegTrigger(triggerDict.get('furniture'))
                                print(triggerDict.get('furniture'))
                            elif (pathImage.image == images[3]):
                                eegTrigger(triggerDict.get('tree'))
                                print(triggerDict.get('tree'))
                            elif (pathImage.image == images[4]):
                                eegTrigger(triggerDict.get('bodypart2'))
                                print(triggerDict.get('bodypart2'))
                            elif (pathImage.image == images[5]):
                                eegTrigger(triggerDict.get('automobile'))
                                print(triggerDict.get('automobile'))
                            elif (pathImage.image == images[6]):
                                eegTrigger(triggerDict.get('handheldobj'))
                                print(triggerDict.get('handheldobj'))
                    win.flip()

                pathImage.status == STOPPED
                g +=1
        isiTime = int(round(np.random.uniform(600,800)/1000*120))
        print("isi: "+str(isiTime))
        for i in range (isiTime): #minimum of 200 ms max 400ms// creates a random ISI between 20-50 frames (aforementionped ms)
                    fixation.draw()
                    win.flip()
                    timer.sleep()
        response_one.text = image_names[other_idx]
        response_one.tStart = taskClock.getTime()
        response_two.text = image_names[image_idx]
        response_two.tStart = taskClock.getTime()
        position_choice = [-0.2,0.2]
        shuffle(position_choice)
        response_one.pos=(0,position_choice[0])
        response_two.pos=(0,position_choice[1])
        
        responseDr = ['up','down']
        #respKey = event.waitKeys(keyList=responseDr)
### INPUT ###
        response_paused = True # stop right here
        #while response_paused:
        for j in range(int(round(2*120))):
            theseKeys = event.getKeys(responseDr)
            #if event.getKeys(keyList=['up', 'down']):
            if theseKeys: 
                choice = theseKeys[-1]
                choice = choice + "| up |" + response_one.text + " | down |" + response_two.text
                key_resp_2.keys = choice  # just the last key pressed
                key_resp_2.rt = key_resp_2.clock.getTime()
                k = taskClock.getTime()
                response_paused = False
                taskClock.reset()
                T=0
                k = 0
                break
            else:
                response_one.draw()
                fixation.draw()
                response_two.draw()
                win.flip()
        
            # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
            
        event.clearEvents(eventType='keyboard')

        #win.flip()
        #wait(0.2)
        #fixation.draw()
        #win.flip()      
        if event.getKeys('p'):
            paused = True # stop right here
            paused_trial.append(trials.thisN) 
            while paused:
                if event.getKeys('space'):
                    paused = False
                else:
                    wait(0.01)
            else:
                break

            # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys=None
    thisExp.addData('key_resp_2.keys',key_resp_2.keys)
    if key_resp_2.keys != None:  # we had a response
        thisExp.addData('key_resp_2.rt', key_resp_2.rt)
        thisExp.addData('button_press', k)
    thisExp.addData('path_time', pathImage.tStart)
    thisExp.addData('path_Image', pathImage.image)
    #thisExp.addData('outcomeImage', outcomeImage.image)
    #thisExp.addData('condition', condition) 
    #thisExp.addData('paused_trial', paused_trial)
    thisExp.nextEntry()
    time=np.random.uniform(200,600)/1000
    fixation.draw()
    win.flip()
    wait(time)
    print(time)
    
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
fin.draw() 
win.flip()
paused = True # stop right here
while paused:
    if event.getKeys(keyList=['space']):
        paused = False
        taskClock.reset()
        T=0
        k = 0
    else:
        wait(0.05)

for frame in range (10):
    print(taskClock.getTime())
wait(1.0)

logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
