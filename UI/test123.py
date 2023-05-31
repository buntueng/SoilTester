import tkinter as tk
from PIL import Image, ImageTk

app = tk.Tk()
img = Image.open('test.jpg')

tk_img = ImageTk.PhotoImage(img)
img_width, img_height = img.size

canvas = tk.Canvas(app, width=img_width, height=img_height)      # Creating an image display area
canvas.pack()
canvas.create_image(0, 0 , anchor = tk.NW, image=tk_img)        # image display

canvas.postscript(file="test.ps", colormode='color') # Save image

app.mainloop()