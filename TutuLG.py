#!/usr/bin/env python

EXPERIMENT = 'RSVPLG03test'
VERSION = '0.01'

########################################################################
# Settings
########################################################################

# Empty container for settings
class ExperimentSettings:
    pass
par = ExperimentSettings()

par.n_trials_per_cell = 20
par.n_trials_practice = 16
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
par.color_space = 'rgb255'
par.foreground_color = [0, 0, 0]
par.background_color = [200, 200, 200]
par.quit_key = 'escape'
par.responses = {
    'present': 'slash',
    'absent':  'z'
    }

# timing setup
par.dur_pre_trial = 0.5
par.dur_cue = 0.5
par.dur_fixation = 0.5
par.dur_post_fixation = 0.25
par.dur_stim = 0.35
par.dur_pre_mask = 0.5
par.dur_mask = 0.35
par.dur_response_gap = 0.1
par.dur_feedback = 0.5
par.dur_post_trial = 0.5

########################################################################
# Libraries
########################################################################

import psychopy
psychopy.useVersion('2024.2.4')
from psychopy import core, visual, data, gui, info
from psychopy.hardware import keyboard
import numpy as np
import math, os, random, re, time

########################################################################
# Support Classes
########################################################################

class Cue:
    def __init__(self, stim_images):
        self.cue_images = stim_images
        self.pos = [0, 2 * par.stim_size[1]]
        self.stim = None

    def set(self, stim):
        self.stim = stim

    def draw(self):
        img = self.cue_images[self.stim]
        img.setOri(0)
        img.setPos(self.pos)
        img.draw()

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
        self.TextBox = visual.TextBox2(
            win, '', font='Arial', letterHeight=18,
            alignment='center', autoDraw=False,
            colorSpace=par.color_space)

    def prepare(self, trial=None, accText=None, rt=None, color=None):
        text=''
        if trial != None:
            text += 'Trial {}'.format(trial)
        if accText != None:
            if text != '':
                text += '\n\n'
            text += accText
        if rt != None:
            if text != '':
                text += '\n\n'
            text += 'Response time = {} ms'.format(round(rt * 1000))
        self.TextBox.setText(text)
        if color != None:
            self.TextBox.setColor(color)

    def draw(self):
        self.TextBox.draw()

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
        'Participant': '',
        'Experimenter Initials': '',
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
    par.subject = int(dlg_info['Participant'])
    par.exp_initials = dlg_info['Experimenter Initials']
    par.block_type = dlg_info['Block Type']
    if dlg_info['Cue'] == 'Cue':
        par.show_cue = True
    else:
        par.show_cue = False

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
    AdjustDurations(par.win.monitorFramePeriod)

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
    par.cue = Cue(None)
    par.fixation = Fixation(par.win)
    par.feedback = Feedback(par.win)
    par.TextBox = visual.TextBox2(
        par.win, text='',
        font=par.font, letterHeight=par.font_size, alignment='center',
        colorSpace=par.color_space, color=par.foreground_color)

def InitializeResponses():
    global par
    par.kb = keyboard.Keyboard()

    # set up allowed responses
    allowed_responses = list()
    for k, v in par.responses.items():
        if len(v) == 1 and v.lower() != v.upper():
            allowed_responses.extend([v.lower(), v.upper()])
        else:
            allowed_responses.append(v)
    allowed_responses.append('escape')
    par.allowed_responses = allowed_responses

    # set up reversed responses for data recording
    r = {}
    for k, v in par.responses.items():
        if isinstance(v, (list, tuple)):
            for v1 in v:
                r[v1] = k
        else:
            r[v] = k
    par.rev_responses = r

def quit_on_error(str):
    print(str)
    core.quit()

########################################################################
# Block-Level Code
########################################################################

def CreateTrialHandler(n_reps):
    return data.TrialHandler(par.trial_handler_conditions,
                             nReps=n_reps, method='fullRandom')

def InitializeBlock():
    global par
    par.trial = 0
    par.present_t1 = True
    par.present_t2 = True
    if par.block_type.startswith('Practice'):
        par.warmup_trial_handler = None
        par.main_trial_handler = CreateTrialHandler(
            np.ceil(par.n_trials_practice / par.n_cells))
        par.n_trials_main = par.n_trials_practice
        par.n_trials = par.n_trials_main
        if par.block_type == 'Practice1':
            par.present_t2 = False
    else:
        par.warmup_trial_handler = CreateTrialHandler(
            np.ceil(par.n_trials_warmup / par.n_cells))
        par.main_trial_handler = CreateTrialHandler(par.n_trials_per_cell)
        par.n_trials_main = par.n_trials_per_cell * par.n_cells
        par.n_trials = par.n_trials_warmup + par.n_trials_main
    par.trial_count = {}
    par.correct_count = {}
    par.correct_rt_sum = {}

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
    completed_trials = 0
    for k, v in par.trial_count.items():
        completed_trials += v
    performance_summary = ''
    for k in par.trial_count:
        if k not in par.correct_count or k not in par.correct_rt_sum:
            continue
        acc = 100 * par.correct_count[k] / par.trial_count[k]
        if par.correct_count[k] > 0:
            rt = 1000 * par.correct_rt_sum[k] / par.correct_count[k]
        else:
            rt = 0
        performance_summary += \
          '\n\nTarget %s: Accuracy = %0.1f%%, Average RT = %0.0f ms' % (k, acc, rt)
    print(performance_summary)
    s = 'Completed %d trials\n' % (completed_trials)
    s += performance_summary
    s += '\n\n\nPlease let the experimenter know that you are done\n\n\nThank you!'
    par.TextBox.setText(s)
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
    PresentFixation()
    PresentStimSequence()
    if par.end_experiment:
        return
    PostTrialPause()
    CheckForBreak()
    EndTrial()
    if par.end_experiment:
        return

def InitializeTrial():
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

    mask1_file = '{}{}.{}'.format(
        par.mask_file_prefix,
        par.rng.choice(par.n_mask_files) + 1,
        par.mask_file_ext)
    mask2_file = '{}{}.{}'.format(
        par.mask_file_prefix,
        par.rng.choice(par.n_mask_files) + 1,
        par.mask_file_ext)

    par.stim1_image.setImage(os.path.join(par.stim_dir, stim1_file))
    par.stim2_image.setImage(os.path.join(par.stim_dir, stim2_file))
    par.mask1_image.setImage(os.path.join(par.stim_dir, mask1_file))
    par.mask2_image.setImage(os.path.join(par.stim_dir, mask2_file))

    par.data_handler.AddData('trial', par.trial)
    par.data_handler.AddData('trialtime', time.strftime("%Y%m%d-%H%M%S"))
    par.data_handler.AddData('t1_level', par.t1_level)
    par.data_handler.AddData('t2_level', par.t2_level)
    par.data_handler.AddData('t2_lag', par.t2_lag)
    par.data_handler.AddData('t1', target1)
    par.data_handler.AddData('t2', target2)
    par.data_handler.AddData('distractor1', distractor1)
    par.data_handler.AddData('distractor2', distractor2)
    par.data_handler.AddData('stimfile1', stim1_file)
    par.data_handler.AddData('stimfile2', stim2_file)
    par.data_handler.AddData('maskfile1', mask1_file)
    par.data_handler.AddData('maskfile2', mask2_file)

    # par.correct_response = par.responses[par.trial_target_status]

def PresentCue():
    par.win.clearBuffer()
    par.cue.draw()
    par.win.flip()
    core.wait(par.dur_cue)

def PresentFixation():
    par.stim1_image.draw()
    par.stim2_image.draw()
    par.mask1_image.draw()
    par.mask2_image.draw()
    par.win.clearBuffer()
    #if par.show_cue:
    #    par.cue.draw()
    par.fixation.draw()
    par.win.flip()
    par.win.clearBuffer()
    core.wait(par.dur_fixation)

def PresentStimSequence():
    # post fixation blank
    par.win.flip()
    # draw stim 1 to back buffer during post-fixation blank
    par.win.clearBuffer()
    par.stim1_image.draw()
    core.wait(par.dur_post_fixation)
    # reveal stim 1 and clear buffer in prep for post stim blank
    par.win.flip()
    par.win.clearBuffer()
    core.wait(par.dur_stim)
    # reveal post stim blank and draw mask
    par.win.flip()
    par.win.clearBuffer()
    par.mask1_image.draw()
    core.wait(par.dur_pre_mask)
    # reveal mask and clear buffer for post mask blank (lag)
    par.win.flip()
    par.win.clearBuffer()
    core.wait(par.dur_mask)
    # reveal post mask blank and draw stim 2
    par.win.flip()
    par.win.clearBuffer()
    par.stim2_image.draw()
    core.wait(par.t2_lag - (par.dur_stim + par.dur_pre_mask + par.dur_mask))
    # reveal stim 2 and pre draw post stim blank
    par.win.flip()
    par.win.clearBuffer()
    core.wait(par.dur_stim)
    # reveal post stim blank and draw mask
    par.win.flip()
    par.win.clearBuffer()
    par.mask2_image.draw()
    core.wait(par.dur_pre_mask)
    # reveal mask and clear buffer for post mask blank (lag)
    par.win.flip()
    par.win.clearBuffer()
    core.wait(par.dur_mask)
    # hide mask
    par.win.flip()
    core.wait(par.dur_response_gap)

def CollectResponse():
    global par
    par.kb.clock.reset()
    keys = par.kb.waitKeys(keyList=par.allowed_responses)
    par.response_dict = ProcessResponse(
        keys, par.correct_response, par.allowed_responses)
    par.data_handler.AddData('resp', par.response_dict['resp'])
    par.data_handler.AddData(
        'rresp',
        par.rev_responses.get(par.response_dict['resp'], 'none'))
    par.data_handler.AddData('acc', par.response_dict['acc'])
    par.data_handler.AddData('rt', par.response_dict['rt'])
    if par.end_experiment:
        return

def SaveData():
    par.data_handler.OutputLine()
    acc = par.response_dict['acc']
    rt = par.response_dict['rt']
    if par.trial_target in par.trial_count:
        # already started counting for this target
        par.trial_count[par.trial_target] += 1
    else:
        # first trial with this target
        par.trial_count[par.trial_target] = 1
        par.correct_count[par.trial_target] = 0
        par.correct_rt_sum[par.trial_target] = 0
    if acc == 1 and par.trial_target in par.correct_count:
        par.correct_count[par.trial_target] += 1
    if acc == 1 and par.trial_target in par.correct_rt_sum:
        par.correct_rt_sum[par.trial_target] += rt
    # pause
    core.wait(par.dur_response_gap)
    par.win.clearBuffer()

def PresentFeedback():
    rd = par.response_dict
    par.feedback.prepare(
        par.trial,
        rd['fdbk'],
        rd['rt'],
        rd['fdbk_color'])
    par.win.clearBuffer()
    par.feedback.draw()
    par.win.flip()
    core.wait(par.dur_feedback)

def PreTrialPause():
    par.win.clearBuffer()
    par.win.flip()
    core.wait(par.dur_pre_trial)

def PostTrialPause():
    par.win.clearBuffer()
    par.win.flip()
    core.wait(par.dur_post_trial)

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
# Drawing Routines
########################################################################

def DrawSearchDisplay(setsize, stim, xy, orientations):
    for i in range(setsize):
        s = par.stim_images[stim[i]]
        s.setPos(xy[i])
        s.setOri(orientations[i])
        s.draw()

########################################################################
# Support Functions
########################################################################

def AdjustDurations(frame_rate):
    global par
    for s in dir(par):
        if s.startswith('dur_'):
            n_frames = np.round(getattr(par, s) / frame_rate)
            setattr(par, s, frame_rate * (n_frames - .75))

def ProcessResponse(keys=None, correct_responses=None, allowed_responses=None):
    global par
    if keys == None:
        return {
            'acc': -5, 'rt': 0, 'resp': 'none',
            'fdbk': 'NO RESPONSE', 'fdbk_color': par.feedback_color_error}
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
# Test Code
########################################################################

Initialize()
RunExperiment()
if 'exp_handler' in dir(par):
    par.exp_handler.abort()
if 'win' in dir(par):
    par.win.close()
core.quit()
