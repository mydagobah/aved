#! /usr/local/bin python
import config
import cv, time
from threading import Thread
from SimpleCV import *
from Tkinter import *
from scipy import signal, mean
import numpy as np

'''
The central processing unit
All decision making should be made here
'''
class Brain(Thread):
    def __init__(self, face, eye1, eye2):
        self.face = face
        self.eye1 = eye1
        self.eye2 = eye2

    def run(self):
        time.sleep(3) # wait for camera to load
        self.observe()

    def observe(self):
        while (self.is_up()):
            if (self.is_danger(self.eye1) or self.is_danger(self.eye2)):
                self.face.displayDanger()
            else:
                self.face.displaySafe()
            time.sleep(config.interval)

    def is_danger(self, monitor):
        danger = False
        danger |= monitor.getRatio() > 0.4
        danger |= monitor.getRatio() > 0.1 and monitor.getSpeed() > 0.8
        return danger

    def is_up(self):
        return self.eye1.isAlive() and self.eye2.isAlive and config.status == 'on'

'''
Robot Eye
'''
class Eye(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.threshold = 30;
        self.filter = 5;
        self.height = 96;
        self.width = 128;
        self.area = self.height * self.width; # screen size
        self.speed = 0
        self.ratio = 0
        self.p_ratio = 0
        self.p_sm = np.array([0.0, 0.0, 0.0, 0.0])
        self.v_sm = np.array([0.0, 0.0, 0.0])
        self.cam = Camera()
        self.bg = self.formatFrame(self.cam.getImage())
        self.ffg = np.zeros(shape = (self.height, self.width))

    def run(self):
        while config.status == 'on':
            f = self.cam.getImage()
            ff = self.calculate(f)
            app.drawLeye(ff)
            time.sleep(config.interval)

    # function to gray scale
    def toGray(self, arr):
        if len(arr.shape) == 3:
            return (0.2989 * arr[:,:,0] + 0.5870 * arr[:,:,1] + 0.1140 * arr[:,:,2])
        else:
            return arr

    def formatFrame(self, frame):
        frame = frame.scale(self.height, self.width)
        frame = frame.getNumpy()
        return self.toGray(frame.astype('float'))

    def getRatio(self):
        return self.ratio

    def getSpeed(self):
        return self.speed

    def calculate(self, frame):
        fg = self.formatFrame(frame);
        diff = np.abs(fg - self.bg)
	# extract objects
        for j in range(0, self.width):
            for k in range(0, self.height):
                if (diff[k,j] > self.threshold):
                    self.ffg[k,j] = 255
                else:
                    self.ffg[k,j] = 0
        #filter noise
        ffgf = signal.medfilt(self.ffg, [self.filter, self.filter])

        count = 0
        for k in range(0, self.height):
            rowindex = np.where(ffgf[k,:] != 0)
            if (len(rowindex[0]) > 1):
                count = count + max(rowindex[0]) - min(rowindex[0])
        self.p_sm[0] = self.p_sm[1]
        self.p_sm[1] = self.p_sm[2]
        self.p_sm[2] = self.p_sm[3]
        self.p_sm[3] = count
        self.ratio = mean(self.p_sm) / self.area

        self.v_sm[0] = self.v_sm[1]
        self.v_sm[1] = self.v_sm[2]
        self.v_sm[2] = (self.ratio - self.p_ratio) / self.interval
        self.speed = mean(self.v_sm)

        self.p_ratio = self.ratio
        self.bg = fg # update background
        return ffgf
