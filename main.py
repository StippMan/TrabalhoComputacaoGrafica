from __future__ import division
from tkinter import *
import tkinter.scrolledtext as tkst 
from math import sqrt, pi, cos, sin
import numpy as np
class DrawnShape():
	def __init__(self):
		self.coordinates = [(0,0)]

	def draw(self, canvas):
		canvas.create_polygon(self.coordinates,width=2,fill='',outline="black")


class Line(DrawnShape):
	def __init__(self, coord1,coord2):
		self.coordinates = [coord1, coord2]

	def __repr__(self):
		return '\nLine({})'.format(self.coordinates)

class Triangle(DrawnShape):
	def __init__(self, coord1,coord2,coord3):
		self.coordinates = [coord1,coord2,coord3]
	def __repr__(self):
		return '\nTriangle({})'.format(self.coordinates)

class Rectangle(DrawnShape):
	def __init__(self, coord1,coord2):
		self.coordinates = [coord1, (coord2[0],coord1[1]), coord2, (coord1[0],coord2[1])]
	def __repr__(self):
		return '\nRectangle({})'.format(self.coordinates)

class Circle(DrawnShape):
	def __init__(self, coord1, coord2):
		self.coordinates = [coord1]
		self.radius = sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)
	def __repr__(self):
		return '\nCircle({},{})'.format(self.coordinates[0],self.radius)

	def draw(self, canvas):
		x1 = self.coordinates[0][0] - self.radius
		y1 = self.coordinates[0][1] - self.radius
		x2 = self.coordinates[0][0] + self.radius
		y2 = self.coordinates[0][1] + self.radius
		canvas.create_oval(x1, y1, x2, y2, width=2,outline="black")


class MainApp():
	def __init__(self):
		self.shapes = []
		self.clickNumber = 0
		self.clickCoords = []

		self.window = Tk()
		self.window.title("Visualizer")
		self.root = Frame(self.window,bg="grey") 
		self.createToolbar()
		self.createStatusbar()
		self.createShapebar()
		self.createCanvas()
		self.root.pack()

		self.inputFieldText = StringVar(self.window)
		self.print("Aperte um dos botoes a esquerda para comecar",'system')

	def createToolbar(self):
		self.toolbar = Frame(self.root, bg="")
		
		self.centralizeButton = Button(self.toolbar,text="CENTRALIZE",command=self.centralizeCanvas)
		self.zoomButton = Button(self.toolbar,text="ZOOM",command=self.changeToZoom)
		self.moveButton = Button(self.toolbar,text="MOVE",command=self.changeToTranslate)
		self.scaleButton = Button(self.toolbar,text="SCALE",command=self.changeToScale)	
		self.rotateButton = Button(self.toolbar,text="ROTATE",command=self.changeToRotate)
		self.clearButton = Button(self.toolbar,text="CLEAR",command=self.clearCanvas)
		self.undoButton = Button(self.toolbar,text="UNDO",command=self.undoAction)
		filler = Frame(self.toolbar,width=100, bg="")
		filler.pack(side=LEFT, padx=2, pady=2)
		self.clearButton.pack(side=LEFT, padx=2, pady=2)
		self.moveButton.pack(side=LEFT, padx=2, pady=2)
		self.rotateButton.pack(side=LEFT, padx=2, pady=2)
		self.scaleButton.pack(side=LEFT, padx=2, pady=2)
		self.zoomButton.pack(side=LEFT, padx=2, pady=2)
		self.centralizeButton.pack(side=LEFT, padx=2, pady=2)
		self.undoButton.pack(side=LEFT, padx=2, pady=2)

		self.toolbar.grid(row=0,column=0, columnspan=2, sticky=NSEW)

	def createStatusbar(self):
		self.statusbar = Frame(self.root,bg="gray")

		self.log = tkst.ScrolledText(self.statusbar,height = 5,fg="white",bg = "black")
		self.log.tag_configure('system',foreground="lawn green")
		self.log.tag_configure('error',foreground="red")
		self.log.tag_configure('input',foreground="white")
		self.log.pack(fill=X)

		self.inputField = Entry(self.statusbar,fg="white",bg = "black")
		self.inputField.bind('<Return>', self.getEntry)
		self.inputField.bind('<KP_Enter>', self.getEntry,'+')
		self.inputField.pack(fill=X)
		
		self.statusbar.grid(row=3,column=0, columnspan=2, sticky=NSEW)

	def createShapebar(self):
		self.shapebar = Frame(self.root, bg="grey")


		# self.lbl1 = Label(self.shapebar, text="DESENHOS",height=3, bg="grey")
		# self.lbl1.pack(side=TOP, padx=2, pady=2)

		lineImage = PhotoImage(file="line.png")
		triangleImage = PhotoImage(file="triangle.png")
		rectangleImage = PhotoImage(file="rectangle.png")
		circleImage = PhotoImage(file="circle.png")

		self.lineButton = Button(self.shapebar,image=lineImage,command=self.changeToLineMode)
		self.triangleButton = Button(self.shapebar,image=triangleImage,command=self.changeToTriangleMode)
		self.rectangleButton = Button(self.shapebar,image=rectangleImage,command=self.changeToRectangleMode)
		self.circleButton = Button(self.shapebar,image=circleImage,command=self.changeToCircleMode)

		self.lineButton.image = lineImage
		self.triangleButton.image = triangleImage
		self.rectangleButton.image = rectangleImage
		self.circleButton.image = circleImage

		self.lineButton.pack(side=TOP, padx=2, pady=2, fill=X)
		self.triangleButton.pack(side=TOP, padx=2, pady=2, fill=X)
		self.rectangleButton.pack(side=TOP, padx=2, pady=2, fill=X)
		self.circleButton.pack(side=TOP, padx=2, pady=2, fill=X)

		self.shapebar.grid(row=1,column=0, sticky=NSEW)

	def createCanvas(self):
		self.canvas = Canvas(self.root, height=384, width=683, bg="white")
		self.canvas.grid(row=1,column=1,sticky=NSEW)

	def doNothing(self,event):
		pass

	def print(self,txt,tag):
		self.log.config(state=NORMAL)
		self.log.insert(END,'\n'+txt,tag)
		self.log.config(state=DISABLED)
		self.log.see(END)

	def getEntry(self,event):
		txt = self.inputField.get()
		self.inputFieldText.set(txt)
		self.inputField.delete(0, END)
		self.print(txt,'input')

	def getSelfText(self):
		self.window.wait_variable(self.inputFieldText)
		return self.inputFieldText.get()

		
	def addShape(self):
		self.shapes.append(shape)

	def update(self):
		# print(self.shapes)
		self.canvas.delete("all")
		for shape in self.shapes:
			shape.draw(self.canvas)


	def changeToRotate(self):	
		self.canvas.bind("<Button-1>", self.rotateCanvas)
		self.update()
		
	def changeToScale(self):
		self.canvas.bind("<Button-1>", self.scaleCanvas)
		self.update()

	def changeToTranslate(self):
		self.canvas.bind("<Button-1>", self.translateCanvas)
		self.update()

	def changeToZoom(self):
		self.canvas.bind("<Button-1>", self.zoomCanvas)
		self.update()
	
	def changeToLineMode(self):
		self.canvas.bind("<Button-1>", self.drawLine)
		self.update()

	def changeToTriangleMode(self):
		self.canvas.bind("<Button-1>", self.drawTriangle)
		self.update()

	def changeToRectangleMode(self):
		self.canvas.bind("<Button-1>", self.drawRectangle)
		self.update()

	def changeToCircleMode(self):
		self.canvas.bind("<Button-1>", self.drawCircle)
		self.update()


	def clearCanvas(self):
		self.shapes.clear()
		self.update()

	def undoAction(self):
		pass

	def getClicks(self,event):
		self.clickNumber += 1
		self.clickCoords.append((event.x,event.y))

	def selectPoint(self,coord):
		currDist = 9999999
		for shape in self.shapes:
			for shapeCoord in shape.coordinates:
				dist = sqrt((shapeCoord[0] - coord[0])**2 + (shapeCoord[1] - coord[1])**2)
				if dist < currDist:
					currDist = dist
					currShape = shapeCoord
		if currDist <= 5:
			return currShape
		else:
			return coord

	def selectShapes(self,coord1,coord2):
		
		if coord1[0] <= coord2[0]:
			smallX = coord1[0]
			bigX = coord2[0]
		else:
			smallX = coord2[0]
			bigX = coord1[0]

		if coord1[1] <= coord2[1]:
			smallY = coord1[1]
			bigY = coord2[1]
		else:
			smallY = coord2[1]
			bigY = coord1[1]

		selectedShapes = []
		for eachShape in self.shapes:
			for shapeCoord in eachShape.coordinates:
				if smallX <= shapeCoord[0] <= bigX \
        		 and smallY <= shapeCoord[1] <= bigY \
               	 and eachShape not in selectedShapes:
					selectedShapes.append(eachShape)
		if len(selectedShapes) == 0:
			self.print("Nenhum objeto selecionado",'error')
		return selectedShapes

	def translate(self, selected,dx,dy):
		translationMatrix = np.array([[1, 0, dx],
									  [0, 1, dy],
									  [0, 0, 1 ]])				
		for shape in selected:
			for i in range(len(shape.coordinates)):
				pointMatrix = np.array([shape.coordinates[i][0],
										shape.coordinates[i][1],
										1])
				result = translationMatrix.dot(pointMatrix)
				shape.coordinates[i] = (result[0],result[1])

	def translateCanvas(self,event):
		if self.clickNumber < 1:
			self.getClicks(event)
		else:
			self.getClicks(event)
			self.clickNumber = 0
			coord2 = self.clickCoords.pop()
			coord1 = self.clickCoords.pop()

			selected = self.selectShapes(coord1,coord2)
			# print("selected: " + str(selected))
			if len(selected) > 0:
				# self.inputField.bind('<Return>', self.getEntry)
				self.print("Dx:",'system')
				dx = self.getSelfText()
				while not dx.isnumeric():
					self.print("O valor deve ser um numero",'error')
					self.print("Dx:",'system')
					dx = self.getSelfText()

				self.print("Dy:",'system')
				dy = self.getSelfText()
				while not dy.isnumeric():
					self.print("O valor deve ser um numero",'error')
					self.print("Dy:",'system')
					dy = self.getSelfText()				# self.inputField.bind('<Return>', self.doNothing)

				self.translate(selected,int(dx),int(dy))
			self.update()

	def scale(self,selected,anchor,sx,sy):
		scaleMatrix = np.array([[sx, 0, anchor[0]-anchor[0]*sx],
								[0, sy, anchor[1]-anchor[1]*sy],
								[0,	0, 1]])	
		for shape in selected:
			for i in range(len(shape.coordinates)):
				pointMatrix = np.array([shape.coordinates[i][0],
										shape.coordinates[i][1],
										1])
				result = scaleMatrix.dot(pointMatrix)
				shape.coordinates[i] = (result[0],result[1])
	def scaleCanvas(self,event):
		if self.clickNumber == 0:
			self.getClicks(event)
		elif self.clickNumber == 1:
			self.getClicks(event)
			self.print("Clique em um ponto servir de ancora para a escala",'system')
		else:
			anchor = self.selectPoint((event.x,event.y))
			self.clickNumber = 0
			coord2 = self.clickCoords.pop()
			coord1 = self.clickCoords.pop()
			selected = self.selectShapes(coord1,coord2)
			if len(selected) > 0:
				self.print("Sx:",'system')
				sx = self.getSelfText()
				
				while not isfloat(sx):
					self.print("O valor deve ser um numero",'error')
					self.print("Sx:",'system')
					sx = self.getSelfText()
				self.print("Sy:",'system')
				sy = self.getSelfText()
				while not isfloat(sy):
					self.print("O valor deve ser um numero",'error')
					self.print("Sy:",'system')
					sy = self.getSelfText()
				self.scale(selected,anchor,float(sx),float(sy))
			self.update()

	def rotate(self,selected,anchor,t):
		x = anchor[0]
		y = anchor[1]
		rotationMatrix = np.array([ [cos(t), -1*sin(t), y*sin(t)-x*cos(t)+x],
									[sin(t), cos(t), -1*x*sin(t)-y*cos(t)+y],
									[0,	0, 1]])	
		for shape in selected:
			for i in range(len(shape.coordinates)):
				pointMatrix = np.array([shape.coordinates[i][0],
										shape.coordinates[i][1],
										1])
				result = rotationMatrix.dot(pointMatrix)
				shape.coordinates[i] = (result[0],result[1])

	def rotateCanvas(self,event):
		if self.clickNumber == 0:
			self.getClicks(event)
		elif self.clickNumber == 1:
			self.getClicks(event)
			self.print("Clique em um ponto servir de ancora para a rotacao",'system')
		else:
			anchor = self.selectPoint((event.x,event.y))
			self.clickNumber = 0
			coord2 = self.clickCoords.pop()
			coord1 = self.clickCoords.pop()

			selected = self.selectShapes(coord1,coord2)
			if len(selected) > 0:
				self.print("Angulo em graus para a rotacao: ",'system')
				t = self.getSelfText()
				while not isfloat(t):
					self.print("O valor deve ser um numero",'error')
					t = self.getSelfText()
				t = -1*float(t)*pi/180		#transformando em radian
				self.rotate(selected,anchor,t)
			self.update()

	def zoom(self, coord1,coord2):
		if coord1[0] <= coord2[0]:
			smallX = coord1[0]
			bigX = coord2[0]
		else:
			smallX = coord2[0]
			bigX = coord1[0]

		if coord1[1] <= coord2[1]:
			smallY = coord1[1]
			bigY = coord2[1]
		else:
			smallY = coord2[1]
			bigY = coord1[1]
		
		
		rw = self.canvas.winfo_width()/self.canvas.winfo_height()
		rv = (bigX - smallX)/(bigY - smallY)

		sx = self.canvas.winfo_width()/(bigX - smallX)
		sy = self.canvas.winfo_height()/(bigY - smallY)

		if rw > rv:
			newbigY = (bigX - smallX)/rw + smallY		
			sy = self.canvas.winfo_height()/(newbigY - smallY)
		else:
			newbigX = (bigY - smallY)*rw + smallX
			sx = self.canvas.winfo_width()/(newbigX - smallX)
			

		
		if len(self.shapes) > 0:
			# if rw > rv:
			# 	zoomMatrix = np.array([[sx, 0, -1*sx*smallX],
			# 							[0, sy, -1*sy*smallY-(bigY-newbigY)/2],#
			# 							[0,	0, 1]])	
			# else:
			# 	zoomMatrix = np.array([[sx, 0, -1*sx*smallX-(bigX-newbigX)/2],#
			# 							[0, sy, -1*sy*smallY],
			# 							[0,	0, 1]])	
			zoomMatrix = np.array([[sx, 0, -1*sx*smallX],
									[0, sy, -1*sy*smallY],
									[0,	0, 1]])	
			for shape in self.shapes:
				for i in range(len(shape.coordinates)):
					pointMatrix = np.array([shape.coordinates[i][0],
											shape.coordinates[i][1],
											1])
					result = zoomMatrix.dot(pointMatrix)
					shape.coordinates[i] = (result[0],result[1])
	
	def zoomCanvas(self,event):
		if self.clickNumber == 0:
			self.getClicks(event)
		else:
			self.getClicks(event)
			self.clickNumber = 0
			coord2 = self.clickCoords.pop()
			coord1 = self.clickCoords.pop()
			self.zoom(coord1,coord2)
			self.update()



	def centralizeCanvas(self):
		bigCoord = (-9999999,-9999999)
		smallCoord = (9999999,9999999)
		for shape in self.shapes:
			for coord in shape.coordinates:
				if coord[0] > bigCoord[0]:
					bigCoord[0] = coord[0]
				if coord[0] < smallCoord[0]:
					smallCoord[0] = coord[0]
				if coord[1] > bigCoord[1]:
					bigCoord[1] = coord[1]
				if coord[1] < smallCoord[1]:
					smallCoord[1] = coord[1]
		
		

	def drawLine(self,event):
		if self.clickNumber < 1:
			self.getClicks(event)
		else:
			self.getClicks(event)
			self.clickNumber = 0
			coord2 = self.clickCoords.pop()
			coord1 = self.clickCoords.pop()
			self.shapes.append(Line(coord1, coord2))
			self.update()

	def drawTriangle(self,event):
		if self.clickNumber < 2:
			self.getClicks(event)
		else:
			self.getClicks(event)
			self.clickNumber = 0
			coord3 = self.clickCoords.pop()
			coord2 = self.clickCoords.pop()
			coord1 = self.clickCoords.pop()
			self.shapes.append(Triangle(coord1,coord2,coord3))
			self.update()
	
	def drawRectangle(self,event):
		if self.clickNumber < 1:
			self.getClicks(event)
		else:
			self.getClicks(event)
			self.clickNumber = 0
			coord2 = self.clickCoords.pop()
			coord1 = self.clickCoords.pop()
			self.shapes.append(Rectangle(coord1,coord2))
			self.update()

	def drawCircle(self,event):
		if self.clickNumber < 1:
			self.getClicks(event)
		else:
			self.getClicks(event)
			self.clickNumber = 0
			coord2 = self.clickCoords.pop()
			coord1 = self.clickCoords.pop()
			self.shapes.append(Circle(coord1,coord2))
			self.update()

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def runApp():
	shapes = []
	mainApp = MainApp()
	mainApp.window.mainloop()

runApp()