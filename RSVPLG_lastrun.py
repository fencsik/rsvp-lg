#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.2),
    on Thu Aug  3 15:07:37 2023
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from experiment_setup
from math import floor

# define stimuli and stream characteristics
letters = ['E', 'F', 'H', 'L', 'N', 'S', 'T',
           'U', 'Y', 'Z']
t2letter = 'X'
t1pos_list = [3, 4, 5] # specified in frames not array index
t2lag_list = [2, 3, 4] # lag of 1 would be right after T1
global_local_list = ['global', 'local']

# constants for managing RSVP stream
RSVP_STIM_START = 0
RSVP_STIM_END = 1
RSVP_ISI_START = 2
RSVP_ISI_END = 3
RSVP_DONE = 4

# random number generator
rng = np.random.default_rng()


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.2'
expName = 'RSVPLG'  # from the Builder filename that created this script
expInfo = {
    'participant': '999',
    'session': '001',
}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/fencsik/PsychoPy/RSVPLG/RSVPLG_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1792, 1120], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=True,
    monitor='Default', color=[0,0,0], colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "start_experiment" ---
# Run 'Begin Experiment' code from stim_setup
# timing
stim_duration = 10 * 1/60
isi_duration = 10 * 1/60

# set up Navon letters
localHeight = .02
localWidth = .015
globalHeight = .25 # originally .2
globalWidth = .2 # originally .15
nY = 9
localHeight = globalHeight/nY

class NavonLetter:
    def __init__(self, letter, responses, positions):
        self.name = letter
        self.responses = responses
        self.pos = positions

    def GetName(self):
        return self.name

    def GetResponses(self):
        return self.responses

    def GetPositions(self):
        return self.pos

    def PositionLength(self):
        return len(self.pos)

navon_letters = dict()

name = 'A'
responses = ['a','A']
positions = []
for Idx in range(0,nY):
    positions.append([(1+Idx-nY)/2/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])
for Idx in range(0,nY-1):
    positions.append([-(1+Idx-nY)/2/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])
for Idx in range(int(nY/3),nY-int(nY/3)):
    positions.append([(.5+Idx-nY/2)/(nY-3)*globalWidth,-globalHeight/6])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'C'
responses = ['c','C']
positions = []
for Idx in range(nY):
    positions.append([-sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
for Idx in range(1,int(nY/3)):
    positions.append([sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
for Idx in range(int(2*nY/3),nY-1):
    positions.append([sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
Idx = .25
positions.append([sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
positions.append([-sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
positions.append([sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,-(1+Idx-nY/2)/nY*globalHeight])
positions.append([-sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,-(1+Idx-nY/2)/nY*globalHeight])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'D'
responses = ['d','D']
positions = []
for Idx in range(nY):
    positions.append([-globalWidth/2,(Idx-nY/2)/nY*globalHeight])
for Idx in range(1,floor(nY/2)):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,globalHeight/2-localHeight])
for Idx in range(1,floor(nY/2)):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,-globalHeight/2])
for Idx in range(0,nY):
    positions.append([sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
Idx = .25
positions.append([sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
positions.append([sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,-(1+Idx-nY/2)/nY*globalHeight])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'E'
responses = ['e','E']
positions = []
for Idx in range(nY):
    positions.append([-globalWidth/2,(Idx-nY/2)/nY*globalHeight])
for Idx in range(1,nY):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,globalHeight/2-localHeight])
for Idx in range(1,nY-1):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,-localHeight/2])
for Idx in range(1,nY):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,-globalHeight/2])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'F'
responses = ['f','F']
positions = []
for Idx in range(nY):
    positions.append([-globalWidth/2,(Idx-nY/2)/nY*globalHeight])
for Idx in range(1,nY):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,globalHeight/2-localHeight])
for Idx in range(1,nY-2):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,-localHeight/2])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'H'
responses = ['h','H']
positions = []
for Idx in range(nY):
    positions.append([-globalWidth/2,(Idx-nY/2)/nY*globalHeight])
for Idx in range(1,nY-1):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,-localHeight/2])
for Idx in range(nY):
    positions.append([globalWidth/2,(Idx-nY/2)/nY*globalHeight])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'L'
responses = ['l','L']
positions = []
for Idx in range(nY):
    positions.append([-globalWidth/2,(Idx-nY/2)/nY*globalHeight])
for Idx in range(1,nY):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,-globalHeight/2])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'M'
responses = ['m','M']
positions = []
for Idx in range(nY):
    positions.append([-globalWidth/2-globalWidth/2/nY,(Idx-nY/2)/nY*globalHeight])
for Idx in range(0,nY-1):
    positions.append([Idx/2/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])
for Idx in range(1,nY-1):
    positions.append([-Idx/2/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])
for Idx in range(nY):
    positions.append([globalWidth/2+globalWidth/2/nY,(Idx-nY/2)/nY*globalHeight])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'N'
responses = ['n','N']
positions = []
for Idx in range(nY):
    positions.append([-globalWidth/2,(Idx-nY/2)/nY*globalHeight])
for Idx in range(1,nY-1):
    positions.append([-(.5+Idx-nY/2)/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])
for Idx in range(nY):
    positions.append([globalWidth/2,(Idx-nY/2)/nY*globalHeight])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'O'
responses = ['o','O']
positions = []
for Idx in range(0,nY):
    positions.append([sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
for Idx in range(nY-1):
    positions.append([-sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
Idx = .25
positions.append([sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
positions.append([-sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,(Idx-nY/2)/nY*globalHeight])
positions.append([sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,-(1+Idx-nY/2)/nY*globalHeight])
positions.append([-sqrt(.25-((.5+Idx-nY/2)/(nY-1))**2)*globalWidth,-(1+Idx-nY/2)/nY*globalHeight])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'T'
responses = ['t','T']
positions = []
for Idx in range(nY):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,globalHeight/2-localHeight])
for Idx in range(nY-1):
    positions.append([0,(Idx-nY/2)/nY*globalHeight])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'V'
responses = ['v','V']
positions = []
for Idx in range(0,nY):
    positions.append([Idx/2/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])
for Idx in range(1,nY):
    positions.append([-Idx/2/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])
navon_letters[name] = NavonLetter(name, responses, positions)

name = 'X'
responses = ['x','X']
positions = []
for Idx in range(0,nY):
    positions.append([-(.5+Idx-nY/2)/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])
for Idx in range(0,nY):
    positions.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])
navon_letters[name] = NavonLetter(name, responses, positions)


longestN = 0
longestLetter = ''
allowed_response_list = []
for k in iter(navon_letters):
    n = navon_letters[k].PositionLength()
    if n > longestN:
        longestN = n
        longestLetter = k
    allowed_response_list.extend(navon_letters[k].GetResponses())
print('longest letter is \"%s\" with %d positions' % (longestLetter, longestN))
print(allowed_response_list)

letters = ''.join(list(navon_letters))
print(letters)

local_letter_stim = list()
for i in range(longestN):
    local_letter_stim.append(visual.TextBox2(
        win=win, name='local%02d' % i,
        text='+', pos=[0, 0],
        font='Arial', letterHeight=localHeight,
        alignment='center',
        color='red', opacity=1,
        autoDraw=False))

# letterX = ['x','X']
# for Idx in range(0,nY):
#     letterX.append([-(.5+Idx-nY/2)/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])
# for Idx in range(0,nY):
#     letterX.append([(.5+Idx-nY/2)/(nY-1)*globalWidth,(Idx-nY/2)/nY*globalHeight])

# elementX = visual.TextStim(
#     win=win, name='elementX',
#     text='Q', font='Arial',
#     pos=


# --- Initialize components for Routine "start_trial" ---
trial_cue = visual.TextBox2(
     win, text='', placeholder='Type here...', font='Arial',
     pos=(0, 0),     letterHeight=0.04,
     size=(0.5, 0.5), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.5, speechPoint=None,
     padding=0.0, alignment='center',
     anchor='center', overflow='visible',
     fillColor=None, borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=False,
     name='trial_cue',
     depth=-1, autoLog=True,
)
trial_cue_response = keyboard.Keyboard()

# --- Initialize components for Routine "trial_fixation" ---
fixation = visual.TextStim(win=win, name='fixation',
    text='+',
    font='Open Sans',
    pos=(0, 0), height=0.04, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# --- Initialize components for Routine "rsvp_stream" ---
stim1 = visual.TextStim(win=win, name='stim1',
    text=None,
    font='Open Sans',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
    color=None, colorSpace='rgb', opacity=0.0, 
    languageStyle='LTR',
    depth=-1.0);

# --- Initialize components for Routine "t1_response" ---
t1_response_prompt = visual.TextBox2(
     win, text='', placeholder='Type here...', font='Arial',
     pos=(0, 0),     letterHeight=0.03,
     size=(0.5, 0.5), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0, speechPoint=None,
     padding=0.0, alignment='center',
     anchor='center', overflow='visible',
     fillColor=None, borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=False,
     name='t1_response_prompt',
     depth=0, autoLog=True,
)
t1_response_entry = keyboard.Keyboard()

# --- Initialize components for Routine "t1_feedback" ---
feedback = visual.TextBox2(
     win, text='', placeholder='Type here...', font='Arial',
     pos=(0, 0),     letterHeight=0.05,
     size=(0.5, 0.5), borderWidth=2.0,
     color='white', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0, speechPoint=None,
     padding=0.0, alignment='center',
     anchor='center', overflow='visible',
     fillColor=None, borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=False,
     name='feedback',
     depth=0, autoLog=True,
)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "start_experiment" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
start_experimentComponents = []
for thisComponent in start_experimentComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "start_experiment" ---
routineForceEnded = not continueRoutine
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in start_experimentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "start_experiment" ---
for thisComponent in start_experimentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "start_experiment" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=2.0, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "start_trial" ---
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from code
    # trial setup code
    n_rsvp_frames = 9
    t1pos = rng.choice(t1pos_list)
    t2lag = rng.choice(t2lag_list)
    stream_global_letters = list(navon_letters)
    stream_local_letters = stream_global_letters.copy()
    shuffle(stream_global_letters)
    shuffle(stream_local_letters)
    stream_global_letters = stream_global_letters[0:n_rsvp_frames]
    stream_local_letters = stream_local_letters[0:n_rsvp_frames]
    print(stream_global_letters)
    print(stream_local_letters)
    stream_colors = ['black'] * n_rsvp_frames
    stream_colors[t1pos] = 'white'
    t1_status = rng.choice(global_local_list)
    if t1_status == 'local':
        print('T1 local')
        t1_status_plural = 's'
        t1_status_verb = 'were'
        correct_t1_response = navon_letters[stream_local_letters[t1pos]].GetResponses()
    else:
        print ('T1 global')
        t1_status_plural = ''
        t1_status_verb = 'was'
        correct_t1_response = navon_letters[stream_global_letters[t1pos]].GetResponses()
    
    rsvp_frame = -1
    rsvp_status = RSVP_ISI_START
    next_event_time = core.getTime() # start ISI now
    print('started at %f' % (core.getTime()))
    print(correct_t1_response)
    trial_cue.reset()
    trial_cue.setText('Report the ' + t1_status + ' letter' + t1_status_plural + '\nof the white stimulus\n\nPress any key to begin trial')
    trial_cue_response.keys = []
    trial_cue_response.rt = []
    _trial_cue_response_allKeys = []
    # keep track of which components have finished
    start_trialComponents = [trial_cue, trial_cue_response]
    for thisComponent in start_trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "start_trial" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *trial_cue* updates
        
        # if trial_cue is starting this frame...
        if trial_cue.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            trial_cue.frameNStart = frameN  # exact frame index
            trial_cue.tStart = t  # local t and not account for scr refresh
            trial_cue.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_cue, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'trial_cue.started')
            # update status
            trial_cue.status = STARTED
            trial_cue.setAutoDraw(True)
        
        # if trial_cue is active this frame...
        if trial_cue.status == STARTED:
            # update params
            pass
        
        # *trial_cue_response* updates
        waitOnFlip = False
        
        # if trial_cue_response is starting this frame...
        if trial_cue_response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            trial_cue_response.frameNStart = frameN  # exact frame index
            trial_cue_response.tStart = t  # local t and not account for scr refresh
            trial_cue_response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(trial_cue_response, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'trial_cue_response.started')
            # update status
            trial_cue_response.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(trial_cue_response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(trial_cue_response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if trial_cue_response.status == STARTED and not waitOnFlip:
            theseKeys = trial_cue_response.getKeys(keyList=None, waitRelease=False)
            _trial_cue_response_allKeys.extend(theseKeys)
            if len(_trial_cue_response_allKeys):
                trial_cue_response.keys = _trial_cue_response_allKeys[-1].name  # just the last key pressed
                trial_cue_response.rt = _trial_cue_response_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in start_trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "start_trial" ---
    for thisComponent in start_trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "start_trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "trial_fixation" ---
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    trial_fixationComponents = [fixation]
    for thisComponent in trial_fixationComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "trial_fixation" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 0.5:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        
        # if fixation is starting this frame...
        if fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fixation.frameNStart = frameN  # exact frame index
            fixation.tStart = t  # local t and not account for scr refresh
            fixation.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fixation, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fixation.started')
            # update status
            fixation.status = STARTED
            fixation.setAutoDraw(True)
        
        # if fixation is active this frame...
        if fixation.status == STARTED:
            # update params
            pass
        
        # if fixation is stopping this frame...
        if fixation.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fixation.tStartRefresh + 0.5-frameTolerance:
                # keep track of stop time/frame for later
                fixation.tStop = t  # not accounting for scr refresh
                fixation.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fixation.stopped')
                # update status
                fixation.status = FINISHED
                fixation.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trial_fixationComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "trial_fixation" ---
    for thisComponent in trial_fixationComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-0.500000)
    
    # --- Prepare to start Routine "rsvp_stream" ---
    continueRoutine = True
    # update component parameters for each repeat
    stim1.setColor('', colorSpace='rgb')
    # keep track of which components have finished
    rsvp_streamComponents = [stim1]
    for thisComponent in rsvp_streamComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "rsvp_stream" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # Run 'Each Frame' code from rsvpController
        #if rsvp_frame < n_rsvp_frames
        if rsvp_status == RSVP_STIM_START and core.getTime() >= next_event_time:
            # at the start of each stim
            print('started frame %d at %f' % (rsvp_frame, win.lastFrameT))
            rsvp_status = RSVP_STIM_END
            next_event_time = win.lastFrameT + stim_duration
        elif rsvp_status == RSVP_STIM_END and core.getTime() >= next_event_time:
            # end of each stim
            for i in range(len(local_letter_stim)):
                local_letter_stim[i].setAutoDraw(False)
            rsvp_status = RSVP_ISI_START
            print('ended frame %d at %f' % (rsvp_frame, core.getTime()))
            # don't reset time so we switch to the next step on the next loop
        elif rsvp_status == RSVP_ISI_START and core.getTime() >= next_event_time:
            # start of each ISI, stim are invisible so set up for next stim
            print('starting ISI after frame %d at %f' % (rsvp_frame, core.getTime()))
            rsvp_frame += 1
            if rsvp_frame < n_rsvp_frames:
                frame_global_letter = stream_global_letters[rsvp_frame]
                frame_local_letter = stream_local_letters[rsvp_frame]
                local_letter_pos = navon_letters[frame_global_letter].GetPositions()
                responses = navon_letters[frame_global_letter].GetResponses()
                for i in range(len(local_letter_pos)):
                    local_letter_stim[i].setPos(local_letter_pos[i])
                    local_letter_stim[i].setText(frame_local_letter)
                    local_letter_stim[i].setColor(stream_colors[rsvp_frame])
                rsvp_status = RSVP_ISI_END
            else:
                rsvp_status = RSVP_DONE
            next_event_time = win.lastFrameT + isi_duration
        elif rsvp_status == RSVP_ISI_END and core.getTime() >= next_event_time:
            # at the end of each ISI
            print('ending ISI beforeframe %d at %f' % (rsvp_frame, core.getTime()))
            for i in range(len(local_letter_pos)):
                local_letter_stim[i].setAutoDraw(True)
            rsvp_status = RSVP_STIM_START
            # don't reset time so we switch to the next step on the next loop
        elif rsvp_status == RSVP_DONE and core.getTime() >= next_event_time:
            print('Finishing at %f after %d stimuli' % (core.getTime(), rsvp_frame))
            continueRoutine = False
        
        
        # *stim1* updates
        
        # if stim1 is active this frame...
        if stim1.status == STARTED:
            # update params
            pass
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in rsvp_streamComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "rsvp_stream" ---
    for thisComponent in rsvp_streamComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "rsvp_stream" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "t1_response" ---
    continueRoutine = True
    # update component parameters for each repeat
    t1_response_prompt.reset()
    t1_response_prompt.setText('What ' + t1_status_verb + ' the ' + t1_status + ' letter' + t1_status_plural + ' in the white stimulus\n\nType your answer\n(don\'t worry about upper or lower case)')
    t1_response_entry.keys = []
    t1_response_entry.rt = []
    _t1_response_entry_allKeys = []
    # keep track of which components have finished
    t1_responseComponents = [t1_response_prompt, t1_response_entry]
    for thisComponent in t1_responseComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "t1_response" ---
    routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *t1_response_prompt* updates
        
        # if t1_response_prompt is starting this frame...
        if t1_response_prompt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            t1_response_prompt.frameNStart = frameN  # exact frame index
            t1_response_prompt.tStart = t  # local t and not account for scr refresh
            t1_response_prompt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(t1_response_prompt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 't1_response_prompt.started')
            # update status
            t1_response_prompt.status = STARTED
            t1_response_prompt.setAutoDraw(True)
        
        # if t1_response_prompt is active this frame...
        if t1_response_prompt.status == STARTED:
            # update params
            pass
        
        # *t1_response_entry* updates
        waitOnFlip = False
        
        # if t1_response_entry is starting this frame...
        if t1_response_entry.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            t1_response_entry.frameNStart = frameN  # exact frame index
            t1_response_entry.tStart = t  # local t and not account for scr refresh
            t1_response_entry.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(t1_response_entry, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 't1_response_entry.started')
            # update status
            t1_response_entry.status = STARTED
            # AllowedKeys looks like a variable named `allowed_response_list`
            if not type(allowed_response_list) in [list, tuple, np.ndarray]:
                if not isinstance(allowed_response_list, str):
                    logging.error('AllowedKeys variable `allowed_response_list` is not string- or list-like.')
                    core.quit()
                elif not ',' in allowed_response_list:
                    allowed_response_list = (allowed_response_list,)
                else:
                    allowed_response_list = eval(allowed_response_list)
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(t1_response_entry.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(t1_response_entry.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if t1_response_entry.status == STARTED and not waitOnFlip:
            theseKeys = t1_response_entry.getKeys(keyList=list(allowed_response_list), waitRelease=False)
            _t1_response_entry_allKeys.extend(theseKeys)
            if len(_t1_response_entry_allKeys):
                t1_response_entry.keys = _t1_response_entry_allKeys[-1].name  # just the last key pressed
                t1_response_entry.rt = _t1_response_entry_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in t1_responseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "t1_response" ---
    for thisComponent in t1_responseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if t1_response_entry.keys in ['', [], None]:  # No response was made
        t1_response_entry.keys = None
    trials.addData('t1_response_entry.keys',t1_response_entry.keys)
    if t1_response_entry.keys != None:  # we had a response
        trials.addData('t1_response_entry.rt', t1_response_entry.rt)
    # Run 'End Routine' code from process_t1_response
    if len(t1_response_entry.keys) != 1:
        # no response or multiple responses
        correct = -1
        feedback_text = 'BAD RESPONSE'
        feedback_color = 'yellow'
    elif t1_response_entry.keys in correct_t1_response:
        # response is in list of possible correct responses
        correct = 1
        feedback_text = 'CORRECT'
        feedback_color = 'green'
    else:
        # incorrect response
        correct = 0
        feedback_text = 'ERROR'
        feedback_color = 'red'
    
    # the Routine "t1_response" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "t1_feedback" ---
    continueRoutine = True
    # update component parameters for each repeat
    feedback.reset()
    feedback.setColor(feedback_color, colorSpace='rgb')
    feedback.setText(feedback_text)
    # keep track of which components have finished
    t1_feedbackComponents = [feedback]
    for thisComponent in t1_feedbackComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "t1_feedback" ---
    routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *feedback* updates
        
        # if feedback is starting this frame...
        if feedback.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            feedback.frameNStart = frameN  # exact frame index
            feedback.tStart = t  # local t and not account for scr refresh
            feedback.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(feedback, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'feedback.started')
            # update status
            feedback.status = STARTED
            feedback.setAutoDraw(True)
        
        # if feedback is active this frame...
        if feedback.status == STARTED:
            # update params
            pass
        
        # if feedback is stopping this frame...
        if feedback.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > feedback.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                feedback.tStop = t  # not accounting for scr refresh
                feedback.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'feedback.stopped')
                # update status
                feedback.status = FINISHED
                feedback.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in t1_feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "t1_feedback" ---
    for thisComponent in t1_feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
# completed 2.0 repeats of 'trials'


# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
