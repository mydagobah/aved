#! /usr/local/bin python
from Tkinter import Tk
import wx
from dashboard import Dashboard
import config

class App:
    def __init__(self):
        window = Tk()
        window.geometry("825x690")
        window.title('Animated Vision Motion Detection')
        window.pack_propagate(0)
        app = Dashboard(window)

        #on = False
        #t1 = Eye1()
        #t2 = Eye2()
        #t3 = Brain(app, t1, t2)
        #
        #TIMER_ID = wx.NewId()
        #plotapp = wx.PySimpleApp()
        #frame = Dashboard(t1, t2)
        #t = wx.Timer(frame, TIMER_ID)

        window.mainloop()
