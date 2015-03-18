#! /usr/local/bin python
import os, sys, cv, time, random, threading, matplotlib
from SimpleCV import *
from Tkinter import *
from scipy import misc, average, signal, mean
from scipy.linalg import norm
from numpy import arange, sin, pi
from PIL import Image
import numpy as np

class Eye(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.threshold = 30;
        self.filter = 5;
        self.interval = 0.05;
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
        global on
        while on:
            f = self.cam.getImage()
            ff = self.calculate(f)
            app.drawLeye(ff)
            time.sleep(self.interval)

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
