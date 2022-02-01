
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
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
v=StringVar()

grid_size = 0.1 * mm
N=200

z=20*cm
wave = 100*nm
W = 5 * um
H = 5 * um


D=DoubleVar()
wavelenght=DoubleVar()


def propagateField(event):
    global I
    wave=wavelenght.get()*nm*mm
    z=D.get()*um
    F=Begin(grid_size,wave,N)
    F= RectAperture(F,W,H)
    F = Propagate (F, z)
    I = Intensity(F)
    x = []
    for i in range(N):
        x.append((-grid_size/2+i*grid_size/N)/mm)
    ax1.clear()
    ax1.contourf(I,50,cmap='hot'); ax1.axis('on'); ax1.axis('equal')
    ax1.set_title('Intensity distribution') 
    ax2.plot(x,I[int(N/2)])
    ax2.set_xlabel('x [mm]')
    ax2.set_ylabel('Intensity [a.u.]')
    ax2.grid('on')
    canvas.draw()
    ax2.clear()


def motion(event):
    x=event.xdata;y=event.ydata
    if (x is not None and y is not None and 0<x<N and 0<y<N):
        v.set('x=%3.2f mm, y=%3.2f mm\n I=%3.3f [a.u.]' %((-grid_size/2+x*grid_size/N)/mm,(-grid_size/2+y*grid_size/N)/mm,I[int(x)][int(y)]))
        root.configure(cursor='crosshair')
    else:
        v.set('')
        root.configure(cursor='arrow')
        

def _quit():
    root.quit()
    


Scale(  root,
        takefocus = 1,
        orient='horizontal',
        label = 'distance [um]',
        length = 200,
        from_=50, to=10000,
        resolution = 0.001,
        variable = D,
        cursor="hand2",
        command = propagateField).pack()

Scale(  root,
        takefocus = 1,
        orient='horizontal',
        label = 'wavelenght [pm]',
        length = 200,
        from_=1, to=10000,
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
