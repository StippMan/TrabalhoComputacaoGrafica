from tkinter import *
from math import sqrt

# from PIL import ImageTk, Image

class DrawnShape():
	def __init__(self):
		self.coordinates = [(0,0)]

	def draw(self, canvas):
		for pos in range(len(self.coordinates)):
			point1 = self.coordinates[pos]
			point2 = self.coordinates[pos-1]
			canvas.create_line(point1[0],point1[1], point2[0],point2[1], fill="black", width=2)


class Line(DrawnShape):
	def __init__(self, x1,y1, x2,y2):
		self.coordinates = [(x1,y1), (x2,y2)]

class Triangle(DrawnShape):
	def __init__(self, x1,y1, x2,y2, x3,y3):
		self.coordinates = [(x1,y1), (x2,y2), (x3,y3)]

class Rectangle(DrawnShape):
	def __init__(self, x1,y1, x2,y2):
		self.coordinates = [(x1,y1), (x2,y1), (x2,y2), (x1,y2)]

class Circle(DrawnShape):
	def __init__(self, x1,y1, radius):
		self.coordinates = (x1,y1)
		self.radius = radius
		# self.radius = sqrt((x1 - x2)**2 + (y1 - y2)**2)

	def draw(self, canvas):
		x1 = self.coordinates[0] - self.radius
		y1 = self.coordinates[1] - self.radius
		x2 = self.coordinates[0] + self.radius
		y2 = self.coordinates[1] + self.radius
		canvas.create_oval(x1, y1, x2, y2, width=2,outline="black")


def addShape(shapes, shape):
	shapes.append(shape)

def drawShapes(canvas, shapes):
	for shape in shapes:
		shape.draw(canvas)

def createCanvas(root):
	canvas = Canvas(root, bg="white")
	canvas.grid(row=1,column=1)

	return canvas

def createToolbar(root):
	toolbar = Frame(root, relief=SUNKEN)

	clearButton = Button(toolbar,text="CLEAR")
	rotateButton = Button(toolbar,text="ROTATE")
	scaleButton = Button(toolbar,text="SCALE")	
	moveButton = Button(toolbar,text="MOVE")
	zoomButton = Button(toolbar,text="ZOOM")

	clearButton.pack(side=LEFT, padx=2, pady=2)
	rotateButton.pack(side=LEFT, padx=2, pady=2)
	scaleButton.pack(side=LEFT, padx=2, pady=2)
	moveButton.pack(side=LEFT, padx=2, pady=2)
	zoomButton.pack(side=LEFT, padx=2, pady=2)

	toolbar.grid(row=0,column=0, columnspan=2, sticky=NSEW)

	return toolbar

def createStatusbar(root):
	statusbar = Label(root, text="", bd=1, relief=SUNKEN, anchor=W)
	statusbar.grid(row=2,column=0, columnspan=2, sticky=NSEW)

	return statusbar

def createShapebar(root):

	shapebar = Frame(root, bg="grey")

	lbl1 = Label(shapebar, text="SHAPES", bg= "grey")
	lbl1.pack(side=TOP, padx=2, pady=2)

	lineButton = Button(shapebar,text="LINE")
	triangleButton = Button(shapebar,text="TRIANGLE")
	rectangleButton = Button(shapebar,text="RECTANGLE")
	circleButton = Button(shapebar,text="CIRCLE")

	lineButton.pack(side=TOP, padx=2, pady=2, fill=X)
	triangleButton.pack(side=TOP, padx=2, pady=2, fill=X)
	rectangleButton.pack(side=TOP, padx=2, pady=2, fill=X)
	circleButton.pack(side=TOP, padx=2, pady=2, fill=X)

	shapebar.grid(row=1,column=0, sticky=NSEW)

	return shapebar

def runApp():
	shapes = []

	root = Tk() 
	root.title("Visualizer")

	toolbar = createToolbar(root)
	statusbar = createStatusbar(root)
	shapebar = createShapebar(root)
	canvas = createCanvas(root)
	shapes.append(Circle(100,100,50))
	drawShapes(canvas,shapes)
	
	root.mainloop()

runApp()