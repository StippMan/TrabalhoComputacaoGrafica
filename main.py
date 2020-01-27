from __future__ import division
from tkinter import *
from math import sqrt, pi

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


class MainApp():
	def __init__(self):
		self.shapes = []
		self.clickNumber = 0
		self.clickCoords = []

		self.root = Tk() 
		self.root.title("Visualizer")
		self.createToolbar()
		self.createStatusbar()
		self.createShapebar()
		self.createCanvas()

	def createToolbar(self):
		self.toolbar = Frame(self.root, relief=SUNKEN)
		
		self.zoomButton = Button(self.toolbar,text="ZOOM",command=self.zoomCanvas)
		self.moveButton = Button(self.toolbar,text="MOVE",command=self.moveCanvas)
		self.scaleButton = Button(self.toolbar,text="SCALE",command=self.scaleCanvas)	
		self.rotateButton = Button(self.toolbar,text="ROTATE",command=self.rotateCanvas)
		self.clearButton = Button(self.toolbar,text="CLEAR",command=self.clearCanvas)

		self.zoomButton.pack(side=RIGHT, padx=2, pady=2)
		self.moveButton.pack(side=RIGHT, padx=2, pady=2)
		self.scaleButton.pack(side=RIGHT, padx=2, pady=2)
		self.rotateButton.pack(side=RIGHT, padx=2, pady=2)
		self.clearButton.pack(side=RIGHT, padx=2, pady=2)

		self.toolbar.grid(row=0,column=0, columnspan=2, sticky=NSEW)

	def createStatusbar(self):
		self.statusbar = Label(self.root, text="test", bd=1, relief=SUNKEN, anchor=W)
		self.statusbar.grid(row=2,column=0, columnspan=2, sticky=NSEW)

	def createShapebar(self):
		self.shapebar = Frame(self.root, bg="grey")

		self.lbl1 = Label(self.shapebar, text="SHAPES", bg= "grey")
		self.lbl1.pack(side=TOP, padx=2, pady=2)

		self.lineButton = Button(self.shapebar,text="LINE",command=self.changeToLineMode)
		self.triangleButton = Button(self.shapebar,text="TRIANGLE",command=self.changeToTriangleMode)
		self.rectangleButton = Button(self.shapebar,text="RECTANGLE",command=self.changeToRectangleMode)
		self.circleButton = Button(self.shapebar,text="CIRCLE",command=self.changeToCircleMode)

		self.lineButton.pack(side=TOP, padx=2, pady=2, fill=X)
		self.triangleButton.pack(side=TOP, padx=2, pady=2, fill=X)
		self.rectangleButton.pack(side=TOP, padx=2, pady=2, fill=X)
		self.circleButton.pack(side=TOP, padx=2, pady=2, fill=X)

		self.shapebar.grid(row=1,column=0, sticky=NSEW)

	def createCanvas(self):
		self.canvas = Canvas(self.root, bg="white")
		self.canvas.grid(row=1,column=1)

	def addShape(self):
		self.shapes.append(shape)

	def drawShapes(self):
		for shape in self.shapes:
			shape.draw(canvas)

	def clearCanvas(self):
		self.canvas.delete("all")
		self.clickNumber = 0
		self.clickCoords = []
	def rotateCanvas(self):
		self.canvas.delete("all")
	def scaleCanvas(self):
		self.canvas.delete("all")
	def moveCanvas(self):
		self.canvas.delete("all")
	def zoomCanvas(self):
		self.canvas.delete("all")


	def changeToLineMode(self):
		self.canvas.bind("<Button-1>", self.drawLine)
	def changeToTriangleMode(self):
		self.canvas.bind("<Button-1>", self.drawTriangle)
	def changeToRectangleMode(self):
		self.canvas.bind("<Button-1>", self.drawRectangle)
	def changeToCircleMode(self):
		self.canvas.bind("<Button-1>", self.drawCircle)
	
	def drawLine(self,event):
		if self.clickNumber == 0:
			self.clickNumber = 1
			self.clickCoords.append((event.x,event.y))
		elif self.clickNumber == 1:
			self.clickNumber = 0
			firstCoords = self.clickCoords.pop()
			self.canvas.create_line(firstCoords[0],firstCoords[1], event.x,event.y, fill="black", width=2)

	def drawTriangle(self,event):
		if self.clickNumber == 0:
			self.clickNumber = 1
			self.clickCoords.append((event.x,event.y))
		elif self.clickNumber == 1:
			self.clickNumber = 2
			self.clickCoords.append((event.x,event.y))
		elif self.clickNumber == 2:
			self.clickNumber = 0
			x2,y2 = self.clickCoords.pop()
			x1,y1 = self.clickCoords.pop()
			self.canvas.create_polygon(x1,y1, x2,y2, event.x,event.y, outline="black", fill="", width=2)
	
	def drawRectangle(self,event):
		if self.clickNumber == 0:
			self.clickNumber = 1
			self.clickCoords.append((event.x,event.y))
		elif self.clickNumber == 1:
			self.clickNumber = 0
			x1,y1 = self.clickCoords.pop()
			self.canvas.create_rectangle(x1,y1, event.x,event.y, outline="black", width=2)

	def drawCircle(self,event):
		if self.clickNumber == 0:
			self.clickNumber = 1
			self.clickCoords.append((event.x,event.y))
		elif self.clickNumber == 1:
			self.clickNumber = 0
			x1,y1 = self.clickCoords.pop()
			x2,y2 = event.x, event.y
			r = sqrt((x2 - x1)**2 + (y2 - y1)**2)
			self.canvas.create_oval(x1-r, y1-r, x1+r, y1+r, width=2, outline="black")

def runApp():
	shapes = []
	mainApp = MainApp()
	mainApp.root.mainloop()

runApp()