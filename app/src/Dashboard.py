#! /usr/local/bin python
import config
import cv, matplotlib, ImageTk
from SimpleCV import *
from Tkinter import *
from PIL import Image
import numpy as np
import wx
from matplotlib.figure import Figure
import matplotlib.font_manager as font_manager
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

# generate Dashboard
class Dashboard:
    def __init__(self, window):
        root = Frame(window, width = 825, height = 690, bg = 'black')
        root.pack()

        # title
        title = Label(root, text = "Animated Vision and Event Detection Simulation",
                      bg = 'black', fg = '#f2f9fc', font = ("Comic Sans MS", '24'))
        title.pack_propagate(0)
        title.place(x = 65, y = 0)

        # buttons
        ctrBtn = Button(root, text= 'Start', width=10, command=self.start, bg='black', fg='blue')
        ctrBtn.place(x=280, y=658)
        quitBtn = Button(root, text='Quit', width=10, command=self._quit, bg='black', fg='red')
        quitBtn.place(x=465, y=658)

        # window frames
        # eyes
        leyeFr = Frame(root, width=400, height=300, bd=-2, bg='black')
        leyeFr.pack_propagate(0)
        leyeFr.place(x=10, y=45)
        reyeFr = Frame(root, width=400, height=300, bd=-2, bg='black')
        reyeFr.pack_propagate(0)
        reyeFr.place(x=415, y=45)

        # left eye and right eye
        leye = Canvas(leyeFr, width=404, height=304, bg='light green')
        reye = Canvas(reyeFr, width=404, height=304, bg='light green')
        leye.place(x=-3, y=-3)
        reye.place(x=-3, y=-3)
        # eye frame
        leye.create_oval(50, 60, 350, 240, fill='black')
        reye.create_oval(50, 60, 350, 240, fill='black')
        # initial eyes
        self.imgTk1 = ImageTk.PhotoImage(Image.fromarray(np.zeros([96,128])))
        self.leye_id = leye.create_image(135, 103, anchor=NW, image=self.imgTk1)
        self.leye = leye
        self.imgTk2 = ImageTk.PhotoImage(Image.fromarray(np.zeros([96,128])))
        self.reye_id = reye.create_image(135, 103, anchor=NW, image=self.imgTk2)
        self.reye = reye

        # plot area
        plotFr = Frame(root, width=400, height=300, bg='white')
        plotFr.place(x=10, y=350)

        # expression area
        dispFr = Frame(root, width=400, height=300, bg='black')
        dispFr.pack_propagate(0)
        dispFr.place(x=415, y=350)
        disp = Canvas(dispFr, width=404, height=304, bg='white')
        disp.place(x=-3, y=-3)
        # initial expression
        self.safe = PhotoImage(file='safe.gif')
        self.threat = PhotoImage(file='threat.gif')
        self.sleep = PhotoImage(file='sleep.gif')
        fid = disp.create_image(80, 20, anchor=NW, image=self.sleep)

        # attributes
        self.root = root
        self.btn = ctrBtn
        self.face = disp
        self.fid = fid

        root.update()

    def start(self):
        global on
        if (on):
            on = False
            self.btn.configure(text='Start')
            self.face.itemconfigure(self.fid, image=self.sleep)
            t.Stop()
        else:
            on = True
            self.btn.configure(text='Stop')
            t1.start()
            t2.start()
            t3.start()
            t.Start(50)
            frame.Show()

    def drawLeye(self, data):
        np.transpose(data)
        self.imgTk1 = ImageTk.PhotoImage(Image.fromarray(data))
        self.leye.itemconfigure(self.leye_id, image=self.imgTk1)

    def drawReye(self, data):
        self.imgTk2 = ImageTk.PhotoImage(Image.fromarray(data))
        self.reye.itemconfigure(self.reye_id, image=self.imgTk2)

    def _quit(self):
        window.quit()
        window.destroy()

    def displayDanger(self):
        self.face.itemconfig(self.fid, image=app.threat)

    def displaySafe(self):
        self.face.itemconfig(self.fid, image=app.safe)
