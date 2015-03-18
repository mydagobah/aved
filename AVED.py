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

# thread class to generate GUI ##
class GUI:
    def __init__(self,window):
        root = Frame(window, width=825, height=690, bg='black')
        root.pack()    
        
        # title
        title = Label(root, text="Animal Vision and Event Detection Simulation", 
                      bg='black', fg='#f2f9fc', font=("Comic Sans MS", '24'))
        title.pack_propagate(0)
        title.place(x=65, y=0) 
        
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
     

# thread to do plot
class Plot(wx.Frame):  
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

# thread class left eye #####################################
class Eye1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.threshold_fd = 30;
        self.filt = 5;
        self.height = 96;
        self.width = 128;
        self.s = self.height * self.width; # screen size
        self.dt = 0.05; # interval of calculation
        self.ffg1=np.zeros(shape=(self.height,self.width))
        self.p_ratio1=0
        self.p_sm1=np.array([0.0,0.0,0.0,0.0])
        self.v_sm1=np.array([0.0,0.0,0.0])        
            
    #function to gray scale
    def to_gray(self, arr):
        if len(arr.shape)==3:
            return (0.2989*arr[:,:,0]+0.5870*arr[:,:,1]+0.1140*arr[:,:,2])
        else:
            return arr    
    
    def setBackground(self,bw1):
        bw1=bw1.scale(self.height,self.width)
        self.bg_bw1=bw1.getNumpy()
        self.bg_bw1=self.to_gray(self.bg_bw1.astype('float'))
            
    def calculate(self, fr1):
        fr1=fr1.scale(self.height,self.width)
        fr_bw1=fr1.getNumpy()
        fr_bw1=self.to_gray(fr_bw1.astype('float'))
        fr_diff1=np.abs(fr_bw1-self.bg_bw1)
	# extract objects
        for j in range(0,self.width):
            for k in range(0,self.height):
                if (fr_diff1[k,j]>self.threshold_fd):
                    self.ffg1[k,j]=255
                else:
                    self.ffg1[k,j]=0
        #filter noise
        ffg1f=signal.medfilt(self.ffg1,[self.filt,self.filt])
        self.deye1 = ffg1f
        count1=0
        for k in range(0,self.height):
            rowindex=np.where(ffg1f[k,:]!=0)
            if (len(rowindex[0])>1):
                count1=count1+max(rowindex[0])-min(rowindex[0])
        self.p_sm1[0]=self.p_sm1[1]
        self.p_sm1[1]=self.p_sm1[2]
        self.p_sm1[2]=self.p_sm1[3]
        self.p_sm1[3]=count1
        count1=mean(self.p_sm1)
        self.ratio1=count1/self.s
        self.v_sm1[0]=self.v_sm1[1]
        self.v_sm1[1]=self.v_sm1[2]
        self.v_sm1[2]=(self.ratio1-self.p_ratio1)/self.dt
        self.v1=mean(self.v_sm1)
        self.p_ratio1=self.ratio1
        self.bg_bw1=fr_bw1
            
    def getRatio(self):
        return self.ratio1
        
    def getSpeed(self):
        return self.v1    
    
    def run(self):       
        global on
        cam = Camera()
        bg = cam.getImage()
        self.setBackground(bg)
        while on:
            f = cam.getImage()
            self.calculate(f)
            app.drawLeye(self.deye1)
            time.sleep(0.05)
              
# thread class right eye #####################################
class Eye2(threading.Thread):
    def __init__(self):
        #Parameter setup
        threading.Thread.__init__(self)
        self.threshold_fd = 30;
        self.filt = 5;
        self.height = 96;
        self.width = 128;
        self.s = self.height * self.width; # screen size
        self.dt = 0.05; # interval of calculation
        self.ffg1=np.zeros(shape=(self.height,self.width))
        self.p_ratio1=0
        self.p_sm1=np.array([0.0,0.0,0.0,0.0])
        self.v_sm1=np.array([0.0,0.0,0.0])        
            
    #function to gray scale
    def to_gray(self, arr):
        if len(arr.shape)==3:
            return (0.2989*arr[:,:,0]+0.5870*arr[:,:,1]+0.1140*arr[:,:,2])
        else:
            return arr    
    
    def setBackground(self,bw1):
        bw1=bw1.scale(self.height,self.width)
        self.bg_bw1=bw1.getNumpy()
        self.bg_bw1=self.to_gray(self.bg_bw1.astype('float'))
            
    def calculate(self, fr1):#input self, foreground
        fr1=fr1.scale(self.height,self.width)
        fr_bw1=fr1.getNumpy()
        fr_bw1=self.to_gray(fr_bw1.astype('float'))
        fr_diff1=np.abs(fr_bw1-self.bg_bw1)
        for j in range(0,self.width):
            for k in range(0,self.height):
                if (fr_diff1[k,j]>self.threshold_fd):
                    self.ffg1[k,j]=255
                else:
                    self.ffg1[k,j]=0
        #filter noise
        ffg1f=signal.medfilt(self.ffg1,[self.filt,self.filt])
        self.deye2 = ffg1f
        count1=0
        for k in range(0,self.height):
            rowindex=np.where(ffg1f[k,:]!=0)
            if (len(rowindex[0])>1):
                count1=count1+max(rowindex[0])-min(rowindex[0])
        self.p_sm1[0]=self.p_sm1[1]
        self.p_sm1[1]=self.p_sm1[2]
        self.p_sm1[2]=self.p_sm1[3]
        self.p_sm1[3]=count1
        count1=mean(self.p_sm1)
        self.ratio1=count1/self.s
        self.v_sm1[0]=self.v_sm1[1]
        self.v_sm1[1]=self.v_sm1[2]
        self.v_sm1[2]=(self.ratio1-self.p_ratio1)/self.dt
        self.v1=mean(self.v_sm1)
        self.p_ratio1=self.ratio1
        self.bg_bw1=fr_bw1
            
    def getRatio(self):
        return self.ratio1
        
    def getSpeed(self):
        return self.v1    
    
    def run(self):      
        global on
        cam = Camera()
        bg = cam.getImage()
        self.setBackground(bg)
        while on:
            f = cam.getImage()
            self.calculate(f)
            app.drawReye(self.deye2)
            time.sleep(0.05)

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

# main #######################
window = Tk()
window.geometry("825x690")
window.title('Animal Vision Simulation')
window.pack_propagate(0)
app = GUI(window)
on = False
t1 = Eye1()
t2 = Eye2()
t3 = Brain()

TIMER_ID = wx.NewId() 
plotapp = wx.PySimpleApp()
frame = Plot()  
t = wx.Timer(frame, TIMER_ID)  

window.mainloop()
