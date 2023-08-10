#!/usr/bin/env python

EXPERIMENT = 'RSVPLG01'
VERSION = '0.01'

# Basic setup
rsvp_stream_frames = 12
distractor_letters = 'ABCDEFGJKLMNOPRTUVWXYZ'
t1_letters = 'HS'
t2_letters = '48'
t1_pos_list = [3, 4, 5]
stim_size = [360, 360]
n_trials_per_cell = 1
conditions_file = 'RSVPTrials.csv'
feedback_color_correct = 'green'
feedback_color_error = 'red'
font = 'Arial'
font_size = 20

from psychopy import core, visual, data, gui, info
from psychopy.hardware import keyboard
import numpy as np
import math, os, random, time

# Set up stim dir
stim_dir_options = [
    'stim',
    os.path.join(os.path.expanduser('~'), 'NavonStim', 'navon')
    ]
stim_dir = None
for d in stim_dir_options:
    if os.path.isfile(os.path.join(d, 'A-A.png')):
        stim_dir = d
        break
if stim_dir == None:
    print('Stimulus directory not found')
    core.quit()
    
# initialize random number generator
rng = np.random.default_rng()

# timestamps: time at which this run started and the modification time of
# this file
RUNTIME = data.getDateStr()
try:
    MODTIME = time.strftime('%Y-%m-%d-%H:%M:%S',
                            time.gmtime(os.path.getmtime(__file__)))
except OSError:
    MODTIME = 'No mtime'

def quit_on_error(str):
    print(str)
    core.quit()

class RSVP_Stream:
    def __init__(self, win, stim_dir, stim_size, max_nframes):
        self.win = win
        self.stim_dir = stim_dir
        self.frames = []
        for i in range(max_nframes):
            f = visual.ImageStim(win, size=stim_size)
            f.setAutoDraw(False)
            self.frames.append(f)
        self.frame_index = None

    def initializeStream(self, global_letters, local_letters):
        self.stream_length = len(global_letters)
        for i in range(self.stream_length):
            self.frames[i].setImage(os.path.join(
                self.stim_dir,
                '{}-{}.png'.format(global_letters[i], local_letters[i])))
        self.frame_index = 0

    def preLoadStream(self, clear=True):
        # draw all the frames on top off one another to preload them, presumably clearing the 
        for i in range(self.stream_length):
            self.frames[i].draw()
        if clear:
            self.win.clearBuffer()

    def drawCurrent(self):
        if self.frame_index < len(self.frames):
            self.frames[self.frame_index].draw()
            return True
        else:
            return False

    def nextFrame(self):
        self.frame_index += 1
        if self.frame_index < len(self.frames):
            return True
        else:
            return False

class Fixation:
    def __init__(self, win):
        self.center = [0, 0]
        self.half_length = 20
        thickness = 5
        color = 'black'
        cx = self.center[0]
        cy = self.center[1]
        h = self.half_length
        self.lines = []
        # vertical
        self.lines.append(visual.Line(win, [cx, cy - h], [cx, cy + h],
                                      lineWidth=thickness, lineColor=color))
        # horizontal
        self.lines.append(visual.Line(win, [cx - h, cy], [cx + h, cy],
                                      lineWidth=thickness, lineColor=color))

    def draw(self):
        for line in self.lines:
            line.draw()

    def bottom(self):
        return self.center[1] + self.half_length

class Feedback:
    def __init__(self, win):
        font = 'Arial'
        font_size = 18
        self.default_color='black'
        spacing = 100
        self.titleBox = visual.TextBox2(
            win, '', pos=(0, spacing),
            font=font, letterHeight=font_size, color=self.default_color,
            alignment='center', autoDraw=False)
        self.t1Box = visual.TextBox2(
            win, '', pos=(0, 0),
            font=font, letterHeight=font_size, color=self.default_color,
            alignment='center', autoDraw=False)
        self.t2Box = visual.TextBox2(
            win, '', pos=(0, -spacing),
            font=font, letterHeight=font_size, color=self.default_color,
            alignment='center', autoDraw=False)

    def prepare(self, trial=None,
            t1AccText=None, t1Color=None,
            t2AccText=None, t2Color=None):
        if trial == None:
            self.titleBox.setText('')
        else:
            self.titleBox.setText('Trial {}'.format(trial))
        if t1AccText == None:
            self.t1Box.setText('')
        else:
            self.t1Box.setText('Target 1: {}'.format(t1AccText))
        if t2AccText == None:
            self.t2Box.setText('')
        else:
            self.t2Box.setText('Target 2: {}'.format(t2AccText))
        if t1Color == None:
            t1Color = self.default_color
        if t2Color == None:
            t2Color = self.default_color
        self.t1Box.setColor(t1Color)
        self.t2Box.setColor(t2Color)

    def draw(self):
        self.titleBox.draw()
        self.t1Box.draw()
        self.t2Box.draw()

# Present dialog box and process responses
dlg_info = {
    'Participant': '',
    'Session': '1',
    'Block Type': ['practice', 'experiment'],
    'Version': VERSION
    }
dlg = gui.DlgFromDict(
    dlg_info, title=EXPERIMENT,
    order=['Participant', 'Session', 'Block Type'],
    fixed='Version')
if not dlg.OK:
    print('Dialog box canceled')
    core.quit()

SUBJECT = int(dlg_info['Participant'])
SESSION = int(dlg_info['Session'])
BLOCK_TYPE = dlg_info['Block Type']

data_file_basename = os.path.join('data', u'%s-Data-%03d-%02d-%s' %
                                  (EXPERIMENT, SUBJECT, SESSION, RUNTIME))
extraInfo = {
    'exp': EXPERIMENT,
    'ver': VERSION,
    'mod-utc': MODTIME,
    'sub': SUBJECT,
    'sess': SESSION,
    'blocktyp': BLOCK_TYPE,
    'datetime': RUNTIME}

# open experiment handler
exp_handler = data.ExperimentHandler(name=EXPERIMENT, version=VERSION,
                                     extraInfo=extraInfo,
                                     saveWideText=True,
                                     dataFileName=data_file_basename)

# set up trial handler
trial_handler = data.TrialHandler(
    data.importConditions(conditions_file),
    nReps=n_trials_per_cell,
    method='fullRandom')
exp_handler.addLoop(trial_handler)

# set up stimuli
distractor_letters = list(distractor_letters)
t1_letters = list(t1_letters)
t2_letters = list(t2_letters)

# set up screen based on computer
rti = info.RunTimeInfo(win=False, refreshTest=None)
comp = rti['systemHostName']
if 'Yesun' in comp:
    screen_size = [1920, 1080]
elif 'GoldenChild' in comp:
    screen_size = [1792, 1120]
else:
    # default; need to add testing computer
    screen_size = [800, 600]

# open window and set up
win = visual.Window(
    size=screen_size, fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='Default', color=[1, 1, 1], colorSpace='rgb',
    backgroundImage=None, backgroundFit=None,
    blendMode='avg', useFBO=True,
    units='pix')
win.mouseVisible = False
keyboard = keyboard.Keyboard()

# set up other objects
rsvp_stream = RSVP_Stream(win, stim_dir, stim_size, np.max(rsvp_stream_frames))
fixation = Fixation(win)
feedback = Feedback(win)

trial = 0
for thisTrial in trial_handler:
    trial += 1
    # set factor levels for this trial
    t1_level = thisTrial['t1_level']
    t2_level = thisTrial['t2_level']
    t2_lag = int(thisTrial['t2_lag'])

    if type(rsvp_stream_frames) in (list, tuple):
        n_frames = rng.choice(rsvp_stream_frames)
    else:
        n_frames = rsvp_stream_frames

    # set up stimuli
    global_letters = rng.permutation(distractor_letters)[:n_frames]
    local_letters = rng.permutation(distractor_letters)[:n_frames]
    t1 = rng.choice(t1_letters)
    t2 = rng.choice(t2_letters)
    t1_pos = rng.choice(t1_pos_list)
    if t1_level == 'global':
        global_letters[t1_pos - 1] = t1
    else:
        local_letters[t1_pos - 1] = t1
    if t2_level == 'global':
        global_letters[t1_pos + t2_lag - 1] = t2
    else:
        local_letters[t1_pos + t2_lag - 1] = t2
    t1_resp = [t1.lower(), t1]
    t2_resp = [t2.lower(), t2]

    rsvp_stream.initializeStream(global_letters, local_letters)
    
    # load stimuli and do pre-trial pause
    rsvp_stream.preLoadStream(clear=True)
    win.flip()
    core.wait(0.25)

    # draw fixation
    win.clearBuffer()
    fixation.draw()
    win.flip()
    core.wait(0.5)

    # RSVP stream
    while True:
        win.clearBuffer()
        rsvp_stream.drawCurrent()
        core.wait(.125) # isi
        t = win.flip()
        win.clearBuffer()
        core.wait(.092)
        win.flip()
        if not rsvp_stream.nextFrame():
            break

    # response
    keys = keyboard.waitKeys()

    # post-trial pause
    win.clearBuffer()
    win.flip()
    core.wait(0.25)

    # advance trials
    exp_handler.nextEntry()

    if trial >= 2:
        break

exp_handler.saveAsWideText(data_file_basename, delim=',')
exp_handler.abort()
win.close()
core.quit()
