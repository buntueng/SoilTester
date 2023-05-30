from tkinter import *

from tkinter.filedialog import asksaveasfile

ws = Tk()
ws.geometry('200x200')
ws.title("Python Guides")


def save():
	Files = [('All Files', '*.*'),
			('Python Files', '*.py'),
			('Text Document', '*.txt')]
	file = asksaveasfile(filetypes = Files, defaultextension = Files)

button = Button(ws, text = 'Save', command = lambda : save())
button.pack(side = TOP, pady = 20)

ws.mainloop()