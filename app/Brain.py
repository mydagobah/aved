#! /usr/local/bin python
import os, sys, cv, time, threading
from Tkinter import *

# thread as central processing unit
class Brain(threading.Thread):
    def run(self):
        global on
        time.sleep(3)

        while ((t1.isAlive) and (t2.isAlive) and on):
            if ((t1.getRatio() > 0.4) or (t2.getRatio() > 0.4) or
                ((t1.getRatio() > 0.1 or t2.getRatio > 0.1) and ((t1.getSpeed() > 0.8) or (t2.getSpeed() > 0.8)))):
                app.face.itemconfig(app.fid, image=app.threat)
            else:
                app.face.itemconfig(app.fid, image=app.safe)

            time.sleep(0.05)
