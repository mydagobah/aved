#! /usr/local/bin python
import os, sys, cv, time, random, threading, matplotlib, ImageTk
from SimpleCV import *
from Tkinter import *
import wx

# main #######################
window = Tk()
window.geometry("825x690")
window.title('Animated Vision Motion Detection')
window.pack_propagate(0)
app = Dashboard(window)

on = False
t1 = Eye1()
t2 = Eye2()
t3 = Brain()

TIMER_ID = wx.NewId()
plotapp = wx.PySimpleApp()
frame = Dashboard()
t = wx.Timer(frame, TIMER_ID)

window.mainloop()
