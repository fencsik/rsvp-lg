#!/usr/bin/env python3

import psychopy
psychopy.useVersion('2024.2.4')
from psychopy import core, visual, clock, info
import numpy as np
import re

def AdjustDurations(x, win):
    frame_rate = win.monitorFramePeriod
    n_frames = max(np.round(x / frame_rate), 1)
    return frame_rate * (n_frames - .75)

wait_granularity = 0.001
wait_maximum = .010
def WaitUntil(t):
    pass

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

stimOn = 0.3
stimOff = 0.1

win = visual.Window(
    size=GetScreenResolution(), fullscr=True, screen=0,
    winType='pyglet', allowStencil=False, monitor='Default',
    color=[200, 200, 200], colorSpace='rgb255',
    backgroundImage=None, backgroundFit=None,
    blendMode='avg', useFBO=True, units='pix')

dot = visual.Circle(win, radius=100, lineColor=None, fillColor="purple",
    units='pix', colorSpace='rgb255')

stimOn = AdjustDurations(stimOn, win)
stimOff = AdjustDurations(stimOff, win)

n = 5
t = np.zeros(n)
win.clearBuffer()
dot.draw()
for i in range(n):
    clock.wait(stimOff)
    t[i] = win.flip()
    win.clearBuffer()
    clock.wait(stimOn)
    win.flip()
    dot.draw()

win.clearBuffer()
win.flip()

win.close()

print(t)
print(np.diff(t))