
import matplotlib as matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
import numpy as np
import sys

if sys.version_info[0] < 3:
    from Tkinter import *
    import Tkinter as Tk
else:
    from tkinter import *
    import tkinter as Tk
from LightPipes import *


root = Tk.Tk()
root.wm_title("X-Ray spot simulation")
root.wm_protocol("WM_DELETE_WINDOW", root.quit)

fig=plt.figure(figsize=(6,4))
ax1 = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
v=StringVar()

grid_size = 100 * um
N=200

z=20*cm
wave = 100*nm
W = 6 * um
H = 6 * um


D=DoubleVar()
wavelenght=DoubleVar()


N2=int(N/2)

HoleSeparation=10*mm
z=300*cm
Nholes=2
size_hole=1*mm
Nhole=15
Fhole=Begin(size_hole,wave,Nhole)
Fhole=RectAperture(Fhole,W,H)




def propagateField(event):
    global I
    wave=wavelenght.get()*nm
    z=D.get()*cm
    F=Begin(grid_size,wave,N)
    #F= RectAperture(F,W,H)
    F= RowOfFields(F, Fhole, Nholes, HoleSeparation)
    F = Propagate (F, z)
    I = Intensity(F)
    ax1.clear()
    ax1.contourf(I,50,cmap='hot'); ax1.axis('on'); ax1.axis('equal')
    ax1.set_title('Intensity distribution') 
    canvas.draw()


#def holeGenerator():
 #   Fhole=Begin(grid_size,wave,N)
  #  Fhole= RectAperture(Fhole,W,H)
   # return Fhole

    
    
    
    
    
def motion(event):
    x=event.xdata;y=event.ydata
    if (x is not None and y is not None and 0<x<N and 0<y<N):
        v.set('x=%3.2f um, y=%3.2f um\n I=%3.3f [a.u.]' %((-grid_size/2+x*grid_size/N)/um,(-grid_size/2+y*grid_size/N)/um,I[int(x)][int(y)]))
        root.configure(cursor='crosshair')
    else:
        v.set('')
        root.configure(cursor='arrow')
        

def _quit():
    root.quit()
    


Scale(  root,
        takefocus = 1,
        orient='horizontal',
        label = 'distance [cm]',
        length = 200,
        from_=0.005, to=10,
        resolution = 0.001,
        variable = D,
        cursor="hand2",
        command = propagateField).pack()

Scale(  root,
        takefocus = 1,
        orient='horizontal',
        label = 'wavelenght [nm]',
        length = 200,
        from_=1, to=100,
        resolution = 0.01,
        variable = wavelenght,
        cursor="hand2",
        command = propagateField).pack()

Button( root,
        width = 24,
        text='Quit',
        cursor="hand2",
        command=_quit).pack(pady=10)


Label(root, textvariable=v).pack()

cid = fig.canvas.mpl_connect('motion_notify_event', motion)

propagateField(0)
root.mainloop()
root.destroy()
