
import matplotlib as matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm



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
ax2 = fig.add_subplot(122,projection = '3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
v=StringVar()

grid_size = 120 * um
N=200

wave = 120*nm
W = 5 * um
H = 5 * um


D=DoubleVar()
energy=DoubleVar()
HoleSeparation= DoubleVar()
plankC = 6.626e-34
velocityC= 3e8
kev = 1.6e-16

def propagateField(event):
    global I
    energyK=energy.get()

    wave = (plankC * velocityC)/(kev * energyK)
    print ("wavelenght in nm is : ", wave/nm)
    #z=D.get()*um
    z=D.get()
    hole_d = HoleSeparation.get()*um
    theField = Begin(grid_size,wave,N)

    #F1= RectAperture(theField,W,H,-hole_d/2,0,0)
    F1= CircAperture(theField,5*um,0*um, 20*um)
    F2= CircAperture(theField,5*um,0*um,-18*um)
    #F3= RectAperture(theField,W,H,0,-hole_d/2,0)

    
    
    #F = BeamMix(BeamMix(F1,F2),F3)
    F = BeamMix(F1,F2)
    
    
    #F= RowOfFields(F, Fhole, Nholes, hole_d)
    F = Propagate (F, z)
    I = Intensity(F,1)
    x = []
    y = []
    for i in range(N):
        x.append((-grid_size/2+i*grid_size/N)/mm)
        y.append((-grid_size/2+i*grid_size/N)/mm)
    X,Y = np.meshgrid(x,y)
    ax1.clear()
    ax1.contourf(np.log10(I),50,cmap='rainbow'); ax1.axis('on'); ax1.axis('equal')
    ax1.set_title('Intensity distribution') 
    ax2.clear()
    ax2.scatter(X,Y,I)
    ax2.set_xlabel('x [mm]')
    ax2.set_ylabel('y [mm]')
    ax2.set_zlabel('Intensity [a.u.]')
    ax2.grid('on')
    canvas.draw()
    
    
    
    
    
def motion(event):
    x=event.xdata;y=event.ydata
    if (x is not None and y is not None and 0<x<N and 0<y<N):
        v.set('x=%3.2f um, y=%3.2f um\n I=%3.4f [a.u.]' %((-grid_size/2+x*grid_size/N)/um,(-grid_size/2+y*grid_size/N)/um,I[int(x)][int(y)]))
        root.configure(cursor='crosshair')
    else:
        v.set('')
        root.configure(cursor='arrow')
        

def _quit():
    root.quit()

    
'''    
def fieldGenerator(numberHole):
    resultField = Begin(grid_size,wave,N)
    for i in range (numberHole):
        holeType = input ('Aperture type for hole number ' + str(i+1)+' (C for circle and R for rectangle): ')
        if holeType == "C":
            circleRadius = np.int64(input ("Type the circle radius in um: "))
            xShift = np.int64(input ("Type the circle offset in x axis in um: "))
            yShift = np.int64(input ("Type the circle offset in y axis in um: "))
            tempField = CircAperture(circleRadius,xShift,yShift,resultField)
        elif holeType == "R":
            squareWidth = np.int64(input ("Type the width of the square in um: "))/um
            squareHeight = np.int64(input ("Type the height of the square in um: "))/um
            xShift = np.int64(input ("Type the square offset in x axis in um: "))/um
            yShift = np.int64(input ("Type the square offset in y axis in um: "))/um
            squareAngle = np.int64(input ("Type the angle of the square in degrees: "))
            tempField = RectAperture(resultField,squareWidth,squareHeight,xShift,yShift,squareAngle)
        if i == 0:
            resultField = tempField
        else:
            resultField = BeamMix(resultField,tempField)
    return resultField
'''    






Scale(  root,
        takefocus = 1,
        orient='horizontal',
        #label = 'distance [um]',
        label = 'distance [m]',

        length = 200,
        #from_=40, to=5000,
        from_=1.4, to=1.45,

        resolution = 0.001,
        variable = D,
        cursor="hand2",
        command = propagateField).pack()

Scale(  root,
        takefocus = 1,
        orient='horizontal',
        label = 'Beam energy [kev]',
        length = 200,
        from_=6, to=16,
        resolution = 1,
        variable = energy,
        cursor="hand2",
        command = propagateField).pack()

Scale(  root,
        takefocus = 1,
        orient='horizontal',
        label = 'hole separation [um]',
        length = 200,
        from_=40, to=0,
        resolution = 0.01,
        variable = HoleSeparation,
        cursor="hand2",
        command = propagateField).pack()


Button( root,
        width = 24,
        text='Quit',
        cursor="hand2",
        command=_quit).pack(pady=10)


Label(root, textvariable=v).pack()

#cid = fig.canvas.mpl_connect('motion_notify_event', motion)

#propagateField(0)
#root.mainloop()
#root.destroy()


def main():
    #numberHole = input("Type the number of holes wanted :  ")
    #theField = fieldGenerator (int(numberHole))
    cid = fig.canvas.mpl_connect('motion_notify_event', motion)
    propagateField(0)

    root.mainloop()
    root.destroy()




if __name__ == "__main__":
    main()