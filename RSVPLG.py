#!/usr/bin/env python

EXPERIMENT = 'RSVPLG01'
VERSION = '0.92'

# Basic setup
rsvp_stream_frames = 15
distractor_letters = 'EFHLNSTUYZ'
# t1_letters = 'HS'
t1_color = 'white'
distractor_color = 'black'
t2_letters = 'X'
t1_pos_list = [3, 4, 5, 6]
stim_size = [204, 238]
n_trials_per_cell = 1
conditions_file = 'RSVPTrials.csv'
feedback_color_correct = 'green'
feedback_color_error = 'red'
foreground_color = 'black'
font = 'Arial'
font_size = 24

# timing setup
dur = {
    'pre_trial': 0.25,
    'cue': 0.5,
    'fixation': 0.5,
    'stim': 0.05,
    'isi': 0.10,
    'response_gaps': 0.10,
    'feedback': 1.0,
    'post_trial': 0.25}

from psychopy import core, visual, data, gui, info
from psychopy.hardware import keyboard
import numpy as np
import math, os, random, time

# Set up stim dir
stim_dir_options = [
    'stim',
    os.path.join('..', 'Navon', 'WongChang'),
    os.path.join('..', 'Navon', 'Hermann'),
    os.path.join(os.path.expanduser('~'), 'NavonStim', 'navon')
    ]
stim_dir = None
for d in stim_dir_options:
    if (os.path.isfile(os.path.join(d, 'E-E-black.jpg')) or
        os.path.isfile(os.path.join(d, 'E-E-black.png'))):
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

    def initializeStream(self, global_letters, local_letters, colors):
        self.stream_length = len(global_letters)
        for i in range(self.stream_length):
            self.frames[i].setImage(os.path.join(
                self.stim_dir,
                '{}-{}-{}.png'.format(global_letters[i], local_letters[i], colors[i])))
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

class Cue:
    def __init__(self, win):
        center = [0, 0]
        global_height = 200
        local_height = 50
        color = foreground_color
        thickness = 5
        # global
        self.globalCue = visual.Rect(
            win, pos=center, size=(global_height / 2, global_height),
            lineWidth=thickness, lineColor=color, fillColor=None)
        # local
        self.localCue = visual.Rect(
            win, pos=center, size=(local_height / 2, local_height),
            lineWidth=thickness, lineColor=color, fillColor=None)

    def draw(self, cue):
        if cue[0].lower() == 'g':
            self.globalCue.draw()
        else:
            self.localCue.draw()

class Fixation:
    def __init__(self, win):
        self.center = [0, 0]
        self.half_length = 20
        thickness = 5
        color = foreground_color
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
        self.default_color=foreground_color
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

# function to process responses
def ProcessResponse(keys, correct_responses, allowed_responses):
    rt = keys[0].rt
    resp = keys[0].name
    fdbk_color = feedback_color_error
    if resp == 'escape':
        core.quit()
    if len(keys) > 1:
        # multiple keys pressed
        acc = -2
        resp = 'multiple'
        fdbk = 'MULTIPLE KEYS PRESSED'
    elif resp in correct_responses:
        # correct
        acc = 1
        fdbk = 'CORRECT'
        fdbk_color = feedback_color_correct
    elif resp in allowed_responses:
        # error
        acc = 0
        fdbk = 'ERROR'
    else:
        # some other non-allowed response
        acc = -1
        fdbk = 'BAD KEY PRESS'
    return {'acc': acc, 'rt': rt, 'resp': resp,
        'fdbk': fdbk, 'fdbk_color': fdbk_color}

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

# set up stimuli and responses
distractor_letters = list(distractor_letters)
t2_letters = list(t2_letters)
t1_allowed_responses = list()
for c in distractor_letters:
    t1_allowed_responses.append(c)
    if c.isalpha() and c.isupper():
        t1_allowed_responses.append(c.lower())
t2_allowed_responses = list('yYnN')
t1_allowed_responses.append('escape')
t2_allowed_responses.append('escape')

# set up screen based on computer
rti = info.RunTimeInfo(win=False, refreshTest=None)
comp = rti['systemHostName']
if 'Yesun' in comp or 'A122580' in comp:
    screen_size = [1920, 1080]
elif 'GoldenChild' in comp:
    screen_size = [1792, 1120]
else:
    # default
    print('COMPUTER NOT IDENTIFIED: DEFAULT RESOLUTION SET')
    screen_size = [800, 600]

# open window and set up
win = visual.Window(
    size=screen_size, fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='Default', color=[0.29411] * 3, colorSpace='rgb',
    backgroundImage=None, backgroundFit=None,
    blendMode='avg', useFBO=True,
    units='pix')
win.mouseVisible = False
keyboard = keyboard.Keyboard()

# update timings to get as close to frame rate as possible
frame_rate = win.monitorFramePeriod
for k, d in dur.items():
    nFrames = np.round(d / frame_rate)
    dur[k] = frame_rate * (nFrames - .75)

# set up other objects
rsvp_stream = RSVP_Stream(win, stim_dir, stim_size, np.max(rsvp_stream_frames))
trial_cue = Cue(win)
fixation = Fixation(win)
feedback = Feedback(win)
t1_response_prompt = visual.TextBox2(
    win, text='Which white letter did you see?',
    font=font, letterHeight=font_size, alignment='center',
    color=foreground_color)
t1_response_prompt.setAutoDraw(False)
t2_response_prompt = visual.TextBox2(
    win, text='Did you see ' + ' or '.join(t2_letters),
    font=font, letterHeight=font_size, alignment='center',
    color=foreground_color)
t2_response_prompt.setAutoDraw(False)

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
    t1_pos = rng.choice(t1_pos_list)
    # select t1 from distractors, making sure to get 2 different letters
    t1_list = rng.choice(distractor_letters, 2, replace=False)
    t1_global = t1_list[0]
    t1_local = t1_list[1]
    # remove t1 letters from rest of stream
    trial_letters = np.array(distractor_letters)
    trial_letters = trial_letters[
        (trial_letters != t1_global) & (trial_letters != t1_local)]
    # extend letters if needed
    if len(trial_letters) < n_frames:
        trial_letters = np.tile(
            trial_letters, math.ceil(n_frames / len(trial_letters)))
    global_letters = rng.permutation(trial_letters)[:n_frames]
    local_letters = rng.permutation(trial_letters)[:n_frames]
    # insert T1
    global_letters[t1_pos - 1] = t1_global
    local_letters[t1_pos - 1] = t1_local
    # set up colors
    stream_colors = ['black'] * n_frames
    stream_colors[t1_pos - 1] = 'white'
    # store stimuli and responses
    if t1_level == 'global':
        t1 = t1_global
    else:
        t1 = t1_local
    t1_correct_resp = [t1.lower(), t1]
    if t2_lag > 0:
        t2 = rng.choice(t2_letters)
        t2_correct_resp = list('yY')
        if t2_level == 'global':
            global_letters[t1_pos + t2_lag - 1] = t2
        else:
            local_letters[t1_pos + t2_lag - 1] = t2
    else:
        t2 = 'absent'
        t2_correct_resp = list('nN')
    trial_handler.addData('global_letters', ''.join(global_letters))
    trial_handler.addData('local_letters', ''.join(local_letters))
    trial_handler.addData('t1_pos', t1_pos)
    trial_handler.addData('t1', t1)
    trial_handler.addData('t2', t2)
    trial_handler.addData('t1_corr', ''.join(t1_correct_resp))
    trial_handler.addData('t2_corr', ''.join(t2_correct_resp))

    rsvp_stream.initializeStream(global_letters, local_letters, stream_colors)

    # load stimuli and do pre-trial pause
    rsvp_stream.preLoadStream(clear=True)
    win.flip()
    core.wait(dur['pre_trial'])

    # draw cue
    win.clearBuffer()
    trial_cue.draw(t1_level)
    win.flip()
    core.wait(dur['cue'])

    # draw fixation
    win.clearBuffer()
    fixation.draw()
    win.flip()
    core.wait(dur['fixation'])

    # RSVP stream
    while True:
        win.clearBuffer()
        rsvp_stream.drawCurrent()
        core.wait(dur['isi']) # isi
        t = win.flip()
        win.clearBuffer()
        core.wait(dur['stim']) # stim dur
        win.flip()
        if not rsvp_stream.nextFrame():
            break

    # pause before response collection
    core.wait(dur['response_gaps'])
    win.clearBuffer()

    # T1 response
    t1_response_prompt.draw()
    win.flip()
    keyboard.clock.reset()
    keys = keyboard.waitKeys(keyList=t1_allowed_responses)
    t1_response_dict = ProcessResponse(
        keys, t1_correct_resp, t1_allowed_responses)
    trial_handler.addData('t1_resp', t1_response_dict['resp'])
    trial_handler.addData('t1_acc', t1_response_dict['acc'])
    trial_handler.addData('t1_rt', t1_response_dict['rt'])

    # pause before response 2 collection
    core.wait(dur['response_gaps'])
    win.clearBuffer()

    # T2 response
    t2_response_prompt.draw()
    win.flip()
    keyboard.clock.reset()
    keys = keyboard.waitKeys(keyList=t2_allowed_responses)
    t2_response_dict = ProcessResponse(
        keys, t2_correct_resp, t2_allowed_responses)
    trial_handler.addData('t2_resp', t2_response_dict['resp'])
    trial_handler.addData('t2_acc', t2_response_dict['acc'])
    trial_handler.addData('t2_rt', t2_response_dict['rt'])

    # feedback
    feedback.prepare(trial,
        t1AccText=t1_response_dict['fdbk'],
        t1Color=t1_response_dict['fdbk_color'],
        t2AccText=t2_response_dict['fdbk'],
        t2Color=t2_response_dict['fdbk_color'])
    win.clearBuffer()
    feedback.draw()
    win.flip()
    core.wait(dur['feedback'])

    # post-trial pause
    win.clearBuffer()
    win.flip()
    core.wait(dur['post_trial'])

    # advance trials
    exp_handler.nextEntry()

    if trial >= 5:
        break

exp_handler.saveAsWideText(data_file_basename, delim=',')
exp_handler.abort()
win.close()
core.quit()
