#! /usr/local/bin python
import os, sys, cv, time, random, threading, time, matplotlib, ImageTk
from SimpleCV import *
from Tkinter import *
from scipy import misc, average, signal, mean
from scipy.linalg import norm
from numpy import arange, sin, pi
from PIL import Image
import numpy as np
import wx
from matplotlib.figure import Figure
import matplotlib.font_manager as font_manager
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

# thread to do plot
class Dashboard(wx.Frame):
    """Matplotlib wxFrame with animation effect"""
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, size=(400, 300))
        # Matplotlib Figure
        self.fig = Figure((4, 3), 100)
        # bind the Figure to the backend specific canvas
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.fig)

        # add a subplot
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim([0, 100])
        self.ax.set_ylim([0, 1])
        self.ax.set_xticks(range(0, 101, 10))
        self.ax.grid(True)
        self.ax.set_autoscale_on(False)

        # generates first "empty" plots
        self.r1 = [None] * 100
        self.pr1,=self.ax.plot(range(100),self.r1,label='LD')
        self.v1 = [None] * 100
        self.pv1,=self.ax.plot(range(100),self.v1,label='LV')
        self.r2=[None] * 100
        self.pr2,=self.ax.plot(range(100),self.r2,label='RD')
        self.v2=[None] * 100
        self.pv2,=self.ax.plot(range(100),self.v2,label='RV')
        # add the legend
        self.ax.legend(loc='upper center',
                           ncol=4,
                           prop=font_manager.FontProperties(size=8))

        # force a draw on the canvas()
        # trick to show the grid and the legend
        self.canvas.draw()
        # save the clean background - everything but the line
        # is drawn and saved in the pixel buffer background
        self.bg = self.canvas.copy_from_bbox(self.ax.bbox)
        # bind events coming from timer with id = TIMER_ID
        # to the onTimer callback function
        wx.EVT_TIMER(self, TIMER_ID, self.onTimer)

    def onTimer(self, evt):
        """callback function for timer events"""
        # restore the clean background, saved at the beginning
        self.canvas.restore_region(self.bg)
        # update the data
        self.r1 = self.r1[1:] + [t1.getRatio()]
        self.r2 = self.r2[1:] + [t2.getRatio()]
        self.v1 = self.v1[1:] + [t1.getSpeed()]
        self.v2 = self.v2[1:] + [t2.getSpeed()]

        # update the plot
        self.pr1.set_ydata(self.r1)
        self.pr2.set_ydata(self.r2)
        self.pv1.set_ydata(self.v1)
        self.pv2.set_ydata(self.v2)
        # just draw the "animated" objects
        self.ax.draw_artist(self.pr1)
        self.ax.draw_artist(self.pr2)
        self.ax.draw_artist(self.pv1)
        self.ax.draw_artist(self.pv2)
        self.canvas.blit(self.ax.bbox)
