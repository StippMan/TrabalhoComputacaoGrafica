from tkinter import *

window = Tk() 
window.title("Visualizer")

clearButton = Button(window,text="CLEAR")
clearButton.grid(column = 1, row = 0)

rotateButton = Button(window,text="ROTATE")
rotateButton.grid(column = 2, row = 0)

scaleButton = Button(window,text="SCALE")
scaleButton.grid(column = 3, row = 0)

moveButton = Button(window,text="MOVE")
moveButton.grid(column = 4, row = 0)

zoomButton = Button(window,text="ZOOM")
zoomButton.grid(column = 4, row = 0)

lbl1 = Label(window, text="DESENHOS")
lbl1.grid(column=0, row=1)

lineButton = Button(window,text="LINE")
lineButton.grid(column = 0, row = 2)

triangleButton = Button(window,text="TRIANGLE")
triangleButton.grid(column = 0, row = 3)

rectangleButton = Button(window,text="RECTANGLE")
rectangleButton.grid(column = 0, row = 4)

circleButton = Button(window,text="CIRCLE")
circleButton.grid(column = 0, row = 5)

canvas = Canvas(window, width = 500, height = 500, background = "black")
canvas.grid_configure(column=1, row=1, columnspan=10, rowspan=10)

window.mainloop()