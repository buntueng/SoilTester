from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

class testme:
    def __init__(self,frame1):
        self.frame1=frame1     
        self.button=Button(self.frame1,text="DRAWME",command=self.plot) 
        self.button1=Button(self.frame1,text="CLEARME",command=self.clearme)
        self.button.pack()       
        self.button1.pack()      

    def plot(self):                   
        f=Figure(figsize=(5,1)) 
        aplt=f.add_subplot(111)       
        aplt.plot([1,2,3,4]) 
        self.wierdobject = FigureCanvasTkAgg(f, master=self.frame1) 
        self.wierdobject.get_tk_widget().pack() 
        self.wierdobject.draw()                

    def clearme(self):       
       self.wierdobject.get_tk_widget().pack_forget()     

root=Tk()
aframe=Frame(root)
testme(aframe)
aframe.pack()  #packs a frame which given testme packs frame 1 in testme
root.mainloop()