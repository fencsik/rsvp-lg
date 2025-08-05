#!/usr/bin/env python

EXPERIMENT = 'RSVPLG03test'
VERSION = '0.90'

########################################################################
# Settings
########################################################################

# Empty container for settings
class ExperimentSettings:
    pass
par = ExperimentSettings()

par.n_trials_per_cell = 20
par.n_trials_practice = 8
par.n_trials_warmup = 5
par.break_every = 25

par.stim_size = [190, 250]
par.mask_size = par.stim_size
par.target_letters = 'HS'
par.distractor_letters = 'AE'
par.conditions_file = 'TrialList.csv'
par.stim_dir = 'stim'
par.stim_file_ext = 'png'
par.n_mask_files = 4
par.mask_file_prefix = 'mask-'
par.mask_file_ext = 'png'

par.font = 'Arial'
par.font_size = 24

par.feedback_color_correct = 'green'
par.feedback_color_error = 'red'
par.feedback_spacing = 100
par.color_space = 'rgb255'
par.foreground_color = [0, 0, 0]
par.background_color = [200, 200, 200]
par.quit_key = 'escape'

# timing setup
par.dur_pre_trial = 0.5
par.dur_cue = 0.5
par.dur_fixation = 0.5
par.dur_post_fixation = 0.25
par.dur_stim = 0.033
par.dur_pre_mask = 0.05
par.dur_mask = 0.033
par.dur_response_gap = 0.1
par.dur_feedback = 0.5
par.dur_post_trial = 0.5

########################################################################
# Libraries
########################################################################

import psychopy
psychopy.useVersion('2024.2.4')
from psychopy import core, visual, clock, data, gui, info
from psychopy.hardware import keyboard
import numpy as np
import os, re, time

########################################################################
# Support Classes
########################################################################

class Cue:
    """
    Mode can be 1 (show cue for T1 only), 2 (show cue for T2 only),
    or 3 (show cues for both)
    """
    def __init__(self, win, mode):
        self.global_size = par.stim_size
        self.local_size = [28, 36]
        self.color = par.foreground_color
        self.thickness = 5

        if mode == 1:
            self.CreateOneCue(win)
            self.draw = self.draw1
        elif mode == 2:
            self.CreateOneCue(win)
            self.draw = self.draw2
        elif mode == 3:
            self.CreateTwoCues(win)
            self.draw = self.draw3
        else:
            s = 'invalid cue mode request ({})'.format(mode)
            raise ValueError(s)

    def CreateOneCue(self, win):
        self.cue = {}
        self.cue['global'] = visual.Rect(
            win, pos=[0, self.global_size[1]], size=self.global_size,
            lineWidth=self.thickness, lineColor=self.color, fillColor=None,
            colorSpace=par.color_space)
        self.cue['local'] = visual.Rect(
            win, pos=[0, 2 * self.local_size[1]], size=self.local_size,
            lineWidth=self.thickness, lineColor=self.color, fillColor=None,
            colorSpace=par.color_space)

    def CreateTwoCues(self, win):
        self.cue1 = {}
        self.cue2 = {}
        self.cue1['global'] = visual.Rect(
            win, pos=[-self.global_size[0], self.global_size[1]],
            size=self.global_size, lineWidth=self.thickness,
            lineColor=self.color, fillColor=None,
            colorSpace=par.color_space)
        self.cue1['local'] = visual.Rect(
            win, pos=[-self.global_size[0], self.global_size[1]],
            size=self.local_size, lineWidth=self.thickness,
            lineColor=self.color, fillColor=None,
            colorSpace=par.color_space)
        self.cue2['global'] = visual.Rect(
            win, pos=[self.global_size[0], self.global_size[1]],
            size=self.global_size, lineWidth=self.thickness,
            lineColor=self.color, fillColor=None,
            colorSpace=par.color_space)
        self.cue2['local'] = visual.Rect(
            win, pos=[self.global_size[0], self.global_size[1]],
            size=self.local_size, lineWidth=self.thickness,
            lineColor=self.color, fillColor=None,
            colorSpace=par.color_space)

    def draw1(self, level1, level2):
        self.cue[level1.lower()].draw()

    def draw2(self, level1, level2):
        self.cue[level2.lower()].draw()

    def draw3(self, level1, level2):
        self.cue1[level1.lower()].draw()
        self.cue2[level2.lower()].draw()

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
                                      lineWidth=thickness, lineColor=color,
                                      colorSpace=par.color_space))
        # horizontal
        self.lines.append(visual.Line(win, [cx - h, cy], [cx + h, cy],
                                      lineWidth=thickness, lineColor=color,
                                      colorSpace=par.color_space))

    def draw(self):
        for line in self.lines:
            line.draw()

    def bottom(self):
        return self.center[1] + self.half_length

class Feedback:
    def __init__(self, win):
        self.default_color = par.foreground_color
        self.titleBox = visual.TextBox2(
            win, '', pos=(0, par.feedback_spacing),
            font=par.font, letterHeight=par.font_size,
            color=self.default_color, colorSpace=par.color_space,
            alignment='center', autoDraw=False)
        self.t1Box = visual.TextBox2(
            win, '', pos=(0, 0),
            font=par.font, letterHeight=par.font_size,
            color=self.default_color, colorSpace=par.color_space,
            alignment='center', autoDraw=False)
        self.t2Box = visual.TextBox2(
            win, '', pos=(0, -par.feedback_spacing),
            font=par.font, letterHeight=par.font_size,
            color=self.default_color, colorSpace=par.color_space,
            alignment='center', autoDraw=False)

    def prepare(self, trial=None,
                    t1AccText=None, t1Color=None,
                    t2AccText=None, t2Color=None):
        self.titleBox.setText('')
        self.t1Box.setText('')
        self.t2Box.setText('')
        self.titleBox.setColor(self.default_color)
        self.t1Box.setColor(self.default_color)
        self.t2Box.setColor(self.default_color)
        if trial != None:
            self.titleBox.setText('Trial {}'.format(trial))
        if t1AccText != None:
            self.t1Box.setText('Target 1: {}'.format(t1AccText))
        if t2AccText != None:
            self.t2Box.setText('Target 2: {}'.format(t2AccText))
        if t1Color != None:
            self.t1Box.setColor(t1Color)
        if t2Color != None:
            self.t2Box.setColor(t2Color)

    def draw(self):
        self.titleBox.draw()
        self.t1Box.draw()
        self.t2Box.draw()

class DataHandler:
    def __init__(self, filename, output_type="csv"):
        self.filename = filename
        self.data = {}
        if output_type == "csv":
            self.sep = ','
        else:
            raise ValueError("data file output type not recognized")

    def AddData(self, name, value):
        self.data[name] = str(value)

    def InitializeDataDirectory(self):
        # check if the data directory exists, and if not create it
        dirname = os.path.dirname(self.filename)
        if os.path.exists(dirname) and os.path.isdir(dirname):
            return
        elif os.path.exists(dirname) and not os.path.isdir(dirname):
            s = "data directory '%s' is an existing file" % dirname
            raise NotADirectoryError(s)
        else:
            os.makedirs(dirname)
            return

    def InitializeDataFile(self):
        # check if the data file exists, and if not create it with its header
        if os.path.exists(self.filename) and os.path.isfile(self.filename):
            return
        elif os.path.exists(self.filename) and not os.path.isfile(self.filename):
            s = "data file '%s' is an existing directory" % self.filename
            raise IsADirectoryError(s)
        else:
            header = list()
            for k, v in self.data.items():
                header.append(k)
            if len(header) > 0:
                with open(self.filename, 'w') as f:
                    f.write(self.sep.join(header) + '\n')

    def OutputLine(self):
        self.InitializeDataDirectory()
        self.InitializeDataFile()
        line = list()
        for k, v in self.data.items():
            line.append(v)
        if len(line) > 0:
            with open(self.filename, 'a') as f:
                f.write(self.sep.join(line) + '\n')

########################################################################
# Initialization/Shutdown functions
########################################################################

def Initialize():
    InitializeGeneral()
    PresentDialog()
    InitializeDataFile()
    InitializeGraphics()
    InitializeStimuli()
    InitializeResponses()

def InitializeGeneral():
    global par
    par.experiment = EXPERIMENT
    par.version = VERSION
    par.runtime = time.strftime("%Y%m%d-%H%M%S")
    try:
        par.modtime = time.strftime('%Y%m%d-%H%M%S',
                                     time.localtime(os.path.getmtime(__file__)))
    except OSError:
        par.modtime = 'No mtime'
    par.rng = np.random.default_rng()

    par.end_experiment = False

def PresentDialog():
    dlg_info = {
        'Participant': '999',
        'Experimenter Initials': 'DEF',
        'Block Type': ['Practice1', 'Practice2', 'Experiment'],
        'Cue': ['Cue One', 'Cue Both', 'No Cues'],
        'Version': par.version
        }
    dlg = gui.DlgFromDict(
        dlg_info, title=EXPERIMENT,
        order=['Participant', 'Experimenter Initials', 'Block Type', 'Cue'],
        fixed='Version')
    if not dlg.OK:
        print('Dialog box canceled')
        core.quit()
    ProcessDialog(dlg_info)

def ProcessDialog(dlg_info):
    global par
    try:
        par.subject = int(dlg_info['Participant'])
    except ValueError as ve:
        print('\n\n***** Participant ID must be an integer ({}) *****'.format(
            dlg_info['Participant']))
        core.quit()
    par.exp_initials = dlg_info['Experimenter Initials']
    par.block_type = dlg_info['Block Type']
    c = dlg_info['Cue']
    if c == 'Cue One':
        par.cue_type = 1
    elif c == 'Cue Both':
        par.cue_type = 2
    else:
        par.cue_type = 0

def GetDataFileName():
    return os.path.join('data', u'%s-Data-%03d.csv' %
                        (par.experiment,
                         par.subject))

def GetExperimentHandler():
    extraInfo = {
        'exp': par.experiment,
        'ver': par.version,
        'sub': par.subject,
        'runtime': par.runtime}
    return data.ExperimentHandler(
        name=par.experiment, version=par.version,
        extraInfo=extraInfo,
        saveWideText=True,
        dataFileName=par.data_file_name + '-psychopy')

def InitializeDataFile():
    global par
    par.data_file_name = GetDataFileName()
    par.data_handler = DataHandler(par.data_file_name)
    # create experiment handlers
    par.exp_handler = GetExperimentHandler()
    # load file with trial conditions
    par.trial_handler_conditions = data.importConditions(par.conditions_file)
    par.n_cells = len(par.trial_handler_conditions)

    # store experiment-level data
    par.data_handler.AddData('exp', par.experiment)
    par.data_handler.AddData('exp_initials', par.exp_initials)
    par.data_handler.AddData('runtime', par.runtime)
    par.data_handler.AddData('ver', par.version)
    par.data_handler.AddData('modtime', par.modtime)
    par.data_handler.AddData('sub', par.subject)
    par.data_handler.AddData('blocktyp', par.block_type)
    par.data_handler.AddData('cuetype', par.cue_type)

def GetScreenResolution():
    # identify screen resolution based on the computer
    default_res = [1920, 1080]
    rti = info.RunTimeInfo(win=False, refreshTest=None)
    comp = rti['systemHostName']
    if re.match('A[0-9]{6}', comp) != None or 'Yesun' in comp:
        # this is a computer with a CSUEB asset tag, usually one of our
        # testing computers, or my smaller work laptop
        return default_res
    elif 'GoldenChild' in comp:
        # larger laptop
        return [1792, 1120]
    else:
        # default
        print('COMPUTER NOT IDENTIFIED: DEFAULT RESOLUTION SET')
        return [800, 600]

def InitializeGraphics():
    # open window and set up
    global par
    par.win = visual.Window(
        size=GetScreenResolution(), fullscr=True, screen=0,
        winType='pyglet', allowStencil=False, monitor='Default',
        color=par.background_color, colorSpace=par.color_space,
        backgroundImage=None, backgroundFit=None,
        blendMode='avg', useFBO=True, units='pix')
    par.win.mouseVisible = False

    # update timings to get as close to frame rate as possible
    AdjustDurationSettings()
    par.pre_flip_window = par.win.monitorFramePeriod * 0.5

def InitializeStimuli():
    global par

    # set up stimuli
    par.target_letters = list(par.target_letters)
    par.distractor_letters = list(par.distractor_letters)

    par.stim1_image = visual.ImageStim(
        par.win, size=par.stim_size, autoLog=False)
    par.stim2_image = visual.ImageStim(
        par.win, size=par.stim_size, autoLog=False)
    par.mask1_image = visual.ImageStim(
        par.win, size=par.mask_size, autoLog=False)
    par.mask2_image = visual.ImageStim(
        par.win, size=par.mask_size, autoLog=False)
    par.stim1_image.autoDraw = False
    par.stim2_image.autoDraw = False
    par.mask1_image.autoDraw = False
    par.mask2_image.autoDraw = False

    # set up other trial objects
    par.fixation = Fixation(par.win)
    par.feedback = Feedback(par.win)
    par.TextBox = visual.TextBox2(
        par.win, text='',
        font=par.font, letterHeight=par.font_size, alignment='center',
        colorSpace=par.color_space, color=par.foreground_color)
    par.t1_response_prompt = visual.TextBox2(
        par.win, text='1st target: Did you see ' + ' or '.join(par.target_letters) + '?',
        font=par.font, letterHeight=par.font_size, alignment='center',
        colorSpace=par.color_space, color=par.foreground_color,
        autoDraw=False)
    par.t2_response_prompt = visual.TextBox2(
        par.win, text='2nd target: Did you see ' + ' or '.join(par.target_letters) + '?',
        font=par.font, letterHeight=par.font_size, alignment='center',
        colorSpace=par.color_space, color=par.foreground_color,
        autoDraw=False)

def InitializeResponses():
    global par
    par.kb = keyboard.Keyboard()

    # set up allowed responses
    par.t1_allowed_responses = list()
    par.t2_allowed_responses = list()
    for c in par.target_letters:
        if c.lower() != c.upper():
            x = [c.lower(), c.upper()]
        else:
            x = [c]
        par.t1_allowed_responses.extend(x)
        par.t2_allowed_responses.extend(x)
    par.t1_allowed_responses.append(par.quit_key)
    par.t2_allowed_responses.append(par.quit_key)

    par.t1_correct_count = 0
    par.t2_correct_count = 0

########################################################################
# Block-Level Code
########################################################################

def CreateTrialHandler(n_reps):
    return data.TrialHandler(par.trial_handler_conditions,
                             nReps=n_reps, method='fullRandom')

def InitializeBlock():
    global par
    par.trial = 0
    par.test_t1 = True
    par.test_t2 = True
    if par.block_type.startswith('Practice'):
        par.warmup_trial_handler = None
        par.main_trial_handler = CreateTrialHandler(
            np.ceil(par.n_trials_practice / par.n_cells))
        par.n_trials_main = par.n_trials_practice
        par.n_trials = par.n_trials_main
        if par.block_type == 'Practice1':
            par.test_t2 = False
    else:
        par.warmup_trial_handler = CreateTrialHandler(
            np.ceil(par.n_trials_warmup / par.n_cells))
        par.main_trial_handler = CreateTrialHandler(par.n_trials_per_cell)
        par.n_trials_main = par.n_trials_per_cell * par.n_cells
        par.n_trials = par.n_trials_warmup + par.n_trials_main

    # initialize cues, which depend the tasks being run
    if par.cue_type == 2 and par.test_t1 and par.test_t2:
        # only present two cues if it was requested and both targets are being tested
        par.cue = Cue(par.win, 3)
    elif par.cue_type == 1 or (par.cue_type == 2 and par.test_t1):
        # either just 1 cue requested, or both cues but only T1 is being tested
        par.cue = Cue(par.win, 1)
    else:
        par.cue = None

def PresentStartMessages():
    par.TextBox.setText('Press any button to begin %d trials' % (par.n_trials))
    par.win.clearBuffer()
    par.TextBox.draw()
    par.win.flip()
    keys = par.kb.waitKeys()
    if keys[0].name == par.quit_key:
        par.end_experiment = True
        return

def PresentFinalMessages():
    performance_summary = ''
    if par.trial > 0:
        performance_summary += 'Completed {} trials'.format(par.trial)
    if par.test_t1:
        performance_summary += '\n\n\nTarget 1 Accuracy = {}%'.format(
            np.round(1000 * par.t1_correct_count / par.trial) / 10.0)
    if par.test_t2:
        performance_summary += '\n\n\nTarget 2 Accuracy = {}%'.format(
            np.round(1000 * par.t2_correct_count / par.trial) / 10.0)
    print(performance_summary)
    performance_summary += '\n\n\nPlease let the experimenter know you are done.\n\n\nThank you!'
    par.TextBox.setText(performance_summary)
    par.win.clearBuffer()
    par.TextBox.draw()
    par.win.flip()
    while True:
        keys = par.kb.waitKeys()
        if keys[0].name == par.quit_key:
            break
    par.win.clearBuffer()
    par.win.flip()

def RunTrialGroup(trial_handler, n_trials = None):
    global par
    if trial_handler == None:
        return
    par.exp_handler.addLoop(trial_handler)

    par.trial_within_phase = 0
    for this_trial in trial_handler:
        par.trial += 1
        par.trial_within_phase += 1
        par.t1_level = this_trial['t1_level']
        par.t2_level = this_trial['t2_level']
        par.t2_lag = this_trial['t2_lag']
        RunTrial()
        if n_trials != None and par.trial_within_phase >= n_trials:
            break
        if par.end_experiment:
            break
        par.exp_handler.nextEntry()

    par.exp_handler.loopEnded(trial_handler)

def RunExperiment():
    InitializeBlock()
    # welcome message
    PresentStartMessages()
    if par.end_experiment:
        return

    # run warmup trials
    par.data_handler.AddData('trialtyp', 'warmup')
    RunTrialGroup(par.warmup_trial_handler, par.n_trials_warmup)

    if par.end_experiment:
        return

    # run experimental trials
    par.data_handler.AddData('trialtyp', 'main')
    RunTrialGroup(par.main_trial_handler, par.n_trials_main)

    PresentFinalMessages()

########################################################################
# Trial-Level Code
########################################################################

def RunTrial():
    InitializeTrial()
    PreTrialPause()
    PresentCue()
    PresentFixation()
    PresentStimSequence()
    CollectResponses()
    SaveData()
    if par.end_experiment:
        return
    PresentFeedback()
    PostTrialPause()
    CheckForBreak()
    EndTrial()
    if par.end_experiment:
        return

def InitializeTrial():
    par.data_handler.AddData('trial', par.trial)
    par.data_handler.AddData('trialtime', time.strftime("%Y%m%d-%H%M%S"))
    par.data_handler.AddData('t1_level', par.t1_level)
    par.data_handler.AddData('t2_level', par.t2_level)
    par.data_handler.AddData('t2_lag', par.t2_lag)

    InitializeTrialStimuli()
    InitializeTrialMasks()

def InitializeTrialStimuli():
    global par
    target1 = par.rng.choice(par.target_letters)
    target2 = par.rng.choice(par.target_letters)
    distractor1 = par.rng.choice(par.distractor_letters)
    distractor2 = par.rng.choice(par.distractor_letters)

    if par.t1_level.lower() == 'local':
        stim1_file = '{}-{}.{}'.format(
            distractor1, target1, par.stim_file_ext)
    else:
        stim1_file = '{}-{}.{}'.format(
            target1, distractor1, par.stim_file_ext)

    if par.t2_level.lower() == 'local':
        stim2_file = '{}-{}.{}'.format(
            distractor2, target2, par.stim_file_ext)
    else:
        stim2_file = '{}-{}.{}'.format(
            target2, distractor2, par.stim_file_ext)

    par.stim1_image.setImage(os.path.join(par.stim_dir, stim1_file))
    par.stim2_image.setImage(os.path.join(par.stim_dir, stim2_file))

    par.data_handler.AddData('t1', target1)
    par.data_handler.AddData('t2', target2)
    par.data_handler.AddData('distractor1', distractor1)
    par.data_handler.AddData('distractor2', distractor2)
    par.data_handler.AddData('stimfile1', stim1_file)
    par.data_handler.AddData('stimfile2', stim2_file)

    InitializeTrialResponses(target1, target2)

def InitializeTrialResponses(target1, target2):
    global par
    if target1.lower() != target1.upper():
        par.t1_correct_response = [target1.lower(), target1.upper()]
    else:
        par.t1_correct_response = target1
    if target2.lower() != target2.upper():
        par.t2_correct_response = [target2.lower(), target2.upper()]
    else:
        par.t2_correct_response = target2

    par.data_handler.AddData('t1_corr', ''.join(par.t1_correct_response))
    par.data_handler.AddData('t2_corr', ''.join(par.t2_correct_response))

def InitializeTrialMasks():
    global par
    mask1_file = '{}{}.{}'.format(
        par.mask_file_prefix,
        par.rng.choice(par.n_mask_files) + 1,
        par.mask_file_ext)
    mask2_file = '{}{}.{}'.format(
        par.mask_file_prefix,
        par.rng.choice(par.n_mask_files) + 1,
        par.mask_file_ext)

    par.mask1_image.setImage(os.path.join(par.stim_dir, mask1_file))
    par.mask2_image.setImage(os.path.join(par.stim_dir, mask2_file))

    par.data_handler.AddData('maskfile1', mask1_file)
    par.data_handler.AddData('maskfile2', mask2_file)

def DrawCue():
    if par.cue is not None:
        par.cue.draw(par.t1_level, par.t2_level)

def PresentCue():
    if par.dur_cue == 0:
        return
    par.win.clearBuffer()
    DrawCue()
    par.win.flip()
    clock.wait(par.dur_cue - par.pre_flip_window)

def PresentFixation():
    par.stim1_image.draw()
    par.stim2_image.draw()
    par.mask1_image.draw()
    par.mask2_image.draw()
    par.win.clearBuffer()
    DrawCue()
    par.fixation.draw()
    par.win.flip()
    par.win.clearBuffer()
    clock.wait(par.dur_fixation - par.pre_flip_window)

def PresentStimSequence():
    # post fixation blank
    par.win.flip()

    # set up timing
    t0 = clock.getTime()
    tStartT1 = t0 + par.dur_post_fixation
    tEndT1 = tStartT1 + par.dur_stim
    tStartMask1 = tEndT1 + par.dur_pre_mask
    tEndMask1 = tStartMask1 + par.dur_mask
    tStartT2 = tStartT1 + AdjustDuration(par.t2_lag / 1000)
    tEndT2 = tStartT2 + par.dur_stim
    tStartMask2 = tEndT2 + par.dur_pre_mask
    tEndMask2 = tStartMask2 + par.dur_mask
    tEndStimuli = tEndMask2 + par.dur_response_gap
    # T1
    par.win.clearBuffer()
    par.stim1_image.draw()
    WaitUntil(tStartT1 - par.pre_flip_window)
    par.actual_t1_onset = par.win.flip()
    # clear T1
    par.win.clearBuffer()
    WaitUntil(tEndT1 - par.pre_flip_window)
    par.actual_t1_offset = par.win.flip()
    # mask1
    par.win.clearBuffer()
    par.mask1_image.draw()
    WaitUntil(tStartMask1 - par.pre_flip_window)
    par.actual_mask1_onset = par.win.flip()
    # clear mask1
    par.win.clearBuffer()
    WaitUntil(tEndMask1 - par.pre_flip_window)
    par.win.flip()
    # T2
    par.win.clearBuffer()
    par.stim2_image.draw()
    WaitUntil(tStartT2 - par.pre_flip_window)
    par.actual_t2_onset = par.win.flip()
    # clear T2
    par.win.clearBuffer()
    WaitUntil(tEndT2 - par.pre_flip_window)
    par.actual_t2_offset = par.win.flip()
    # mask2
    par.win.clearBuffer()
    par.mask2_image.draw()
    WaitUntil(tStartMask2 - par.pre_flip_window)
    par.actual_mask2_onset = par.win.flip()
    # clear mask2
    par.win.clearBuffer()
    WaitUntil(tEndMask2 - par.pre_flip_window)
    par.win.flip()
    # pre-response pause
    WaitUntil(tEndStimuli - par.pre_flip_window)

def CollectResponses():
    global par
    if par.test_t1:
        rd = CollectResponse(
            par.t1_response_prompt,
            par.t1_correct_response,
            par.t1_allowed_responses)
        par.t1_response_dict = rd
        if rd['acc'] == 1:
            par.t1_correct_count += 1
    else:
        par.t1_response_dict = ProcessResponse(None)
    if par.test_t2:
        rd = CollectResponse(
            par.t2_response_prompt,
            par.t2_correct_response,
            par.t2_allowed_responses)
        par.t2_response_dict = rd
        if rd['acc'] == 1:
            par.t2_correct_count += 1
    else:
        par.t2_response_dict = ProcessResponse(None)

    par.data_handler.AddData('t1_resp', par.t1_response_dict['resp'])
    par.data_handler.AddData('t1_acc', par.t1_response_dict['acc'])
    par.data_handler.AddData('t1_rt', par.t1_response_dict['rt'])
    par.data_handler.AddData('t2_resp', par.t2_response_dict['resp'])
    par.data_handler.AddData('t2_acc', par.t2_response_dict['acc'])
    par.data_handler.AddData('t2_rt', par.t2_response_dict['rt'])

    if par.end_experiment:
        return

def CollectResponse(prompt, correct_response, allowed_responses):
    par.win.clearBuffer()
    prompt.draw()
    par.win.flip()
    par.kb.clock.reset()
    keys = par.kb.waitKeys(keyList=allowed_responses)
    response_dict = ProcessResponse(
        keys, correct_response, allowed_responses)
    par.win.clearBuffer()
    par.win.flip()
    return response_dict

def SaveData():
    # save timing data
    par.data_handler.AddData('t1_dur', par.actual_t1_offset - par.actual_t1_onset)
    par.data_handler.AddData('t2_dur', par.actual_t2_offset - par.actual_t2_onset)
    par.data_handler.AddData('t1mask_soa', par.actual_mask1_onset - par.actual_t1_onset)
    par.data_handler.AddData('t2mask_soa', par.actual_mask2_onset - par.actual_t2_onset)
    par.data_handler.AddData('t1t2_soa', par.actual_t2_onset - par.actual_t1_onset)

    # output line
    par.data_handler.OutputLine()
    # pause
    clock.wait(par.dur_response_gap - par.pre_flip_window)

def PresentFeedback():
    rd1 = par.t1_response_dict
    rd2 = par.t2_response_dict
    par.feedback.prepare(
        par.trial,
        rd1['fdbk'], rd1['fdbk_color'],
        rd2['fdbk'], rd2['fdbk_color'])
    par.win.clearBuffer()
    par.feedback.draw()
    par.win.flip()
    clock.wait(par.dur_feedback - par.pre_flip_window)

def PreTrialPause():
    par.win.clearBuffer()
    par.win.flip()
    clock.wait(par.dur_pre_trial - par.pre_flip_window)

def PostTrialPause():
    par.win.clearBuffer()
    par.win.flip()
    clock.wait(par.dur_post_trial - par.pre_flip_window)

def CheckForBreak():
    if par.trial % par.break_every == 0 and par.n_trials - par.trial > 5:
        s = "You have completed {} out of {} trials".format(par.trial, par.n_trials)
        s += "\n\n\nPlease take a short break\n\n\nPress any button to continue"
        par.TextBox.setText(s)
        par.win.clearBuffer()
        par.TextBox.draw()
        par.win.flip()
        keys = par.kb.waitKeys()
        if keys[0].name == par.quit_key:
            par.end_experiment = True
        par.win.clearBuffer()
        par.win.flip()

def EndTrial():
    pass

########################################################################
# Support Functions
########################################################################

def WaitUntil(t):
    """WaitUntil(t)

    Wait until clock.getTime() gets to t. Uses clock.wait().
    """

    twait = t - clock.getTime()
    clock.wait(twait)

def AdjustDuration(t):
    frame_rate = par.win.monitorFramePeriod
    return frame_rate * np.round(t / frame_rate)

def AdjustDurationSettings():
    global par
    frame_rate = par.win.monitorFramePeriod
    for s in dir(par):
        if not s.startswith('dur_'):
            continue
        x = getattr(par, s)
        if x == 0:
            continue
        setattr(par, s, frame_rate * np.round(x / frame_rate))

def ProcessResponse(keys=None, correct_responses=None, allowed_responses=None):
    global par
    if keys == None:
        return {
            'acc': -5, 'rt': 0, 'resp': 'none',
            'fdbk': None, 'fdbk_color': None}
    elif keys[0].name == par.quit_key:
        par.end_experiment = True
        return {
            'acc': -6, 'rt': 0, 'resp': 'none',
            'fdbk': None, 'fdbk_color': None}
    rt = keys[0].rt
    resp = keys[0].name
    fdbk_color = par.feedback_color_error
    if len(keys) > 1:
        # multiple keys pressed
        acc = -2
        resp = 'multiple'
        fdbk = 'MULTIPLE KEYS PRESSED'
    elif resp in correct_responses:
        # correct
        acc = 1
        fdbk = 'CORRECT'
        fdbk_color = par.feedback_color_correct
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

########################################################################
# Set up and run experiment, then quit cleanly
########################################################################

Initialize()
RunExperiment()
if 'exp_handler' in dir(par):
    par.exp_handler.abort()
if 'win' in dir(par):
    par.win.close()
core.quit()
