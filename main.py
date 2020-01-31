from __future__ import division
from tkinter import *
import tkinter.scrolledtext as tkst 
from math import sqrt, pi, cos, sin
import numpy as np
class Polygon():
	def __init__(self,coords):
		self.coordinates = coords

	def draw(self, canvas):
		canvas.create_polygon(self.coordinates,width=2,fill='',outline="black")

	def __repr__(self):
		return '\nPolygon({})'.format(self.coordinates)


class Line(Polygon):
	def __init__(self, coord1,coord2):
		self.coordinates = [coord1, coord2]

	def __repr__(self):
		return '\nLine({})'.format(self.coordinates)

class Triangle(Polygon):
	def __init__(self, coord1,coord2,coord3):
		self.coordinates = [coord1,coord2,coord3]
	def __repr__(self):
		return '\nTriangle({})'.format(self.coordinates)

class Rectangle(Polygon):
	def __init__(self, coord1,coord2):
		self.coordinates = [coord1, (coord2[0],coord1[1]), coord2, (coord1[0],coord2[1])]
	def __repr__(self):
		return '\nRectangle({})'.format(self.coordinates)

class Circle(Polygon):
	def __init__(self, coord1, coord2):
		self.radius = sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)
		self.center = coord1
		ne = (coord1[0] + self.radius, coord1[1] + self.radius)
		nw = (coord1[0] - self.radius, coord1[1] + self.radius)
		sw = (coord1[0] - self.radius, coord1[1] - self.radius)
		se = (coord1[0] + self.radius, coord1[1] - self.radius)
		
		self.coordinates = [nw,ne,sw,se]
	def __repr__(self):
		return '\nCircle({}, {}, {})'.format(self.center,self.radius,self.coordinates)

	def draw(self, canvas):
		canvas.create_oval(self.coordinates[0],self.coordinates[3], width=2,outline="black")


class MainApp():
	def __init__(self):
		self.shapes = []
		self.clickNumber = 0
		self.clickCoords = []

		self.window = Tk()
		self.window.title("Visualizer")
		self.root = Frame(self.window,bg="light grey") 
		self.createToolbar()
		self.createStatusbar()
		self.createShapebar()
		self.createCanvas()
		self.root.pack()

		self.inputFieldText = StringVar(self.window)
		self.print("Aperte um dos botoes a esquerda para comecar",'system')

	def createToolbar(self):
		self.toolbar = Frame(self.root, bg="light gray")
		

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
		self.window.bind('<Control-z>',self.undoAction)

	def createStatusbar(self):
		self.statusbar = Frame(self.root,bg="light gray")

		self.log = tkst.ScrolledText(self.statusbar,height = 5,fg="white",bg = "black")
		self.log.tag_configure('system',foreground="lawn green")
		self.log.tag_configure('error',foreground="red")
		self.log.tag_configure('input',foreground="white")
		self.log.tag_configure('wip',foreground="light gray")
		self.log.pack(fill=X)

		self.inputField = Entry(self.statusbar,fg="white",bg = "black")
		self.inputField.bind('<Return>', self.getEntry)
		self.inputField.bind('<KP_Enter>', self.getEntry,'+')
		self.inputField.pack(fill=X)
		
		self.statusbar.grid(row=3,column=0, columnspan=2, sticky=NSEW)

	def createShapebar(self):
		self.shapebar = Frame(self.root, bg="light grey")


		# self.lbl1 = Label(self.shapebar, text="DESENHOS",height=3, bg="grey")
		# self.lbl1.pack(side=TOP, padx=2, pady=2)

		lineImage = PhotoImage(file="line.png")
		triangleImage = PhotoImage(file="triangle.png")
		rectangleImage = PhotoImage(file="rectangle.png")
		circleImage = PhotoImage(file="circle.png")
		polygonImage = PhotoImage(file="polygon.png")

		self.lineButton = Button(self.shapebar,bg="white",image=lineImage,command=self.changeToLineMode)
		self.triangleButton = Button(self.shapebar,bg="white",image=triangleImage,command=self.changeToTriangleMode)
		self.rectangleButton = Button(self.shapebar,bg="white",image=rectangleImage,command=self.changeToRectangleMode)
		self.circleButton = Button(self.shapebar,bg="white",image=circleImage,command=self.changeToCircleMode)
		self.polygonButton = Button(self.shapebar,bg="white",image=polygonImage,command=self.changeToPolygonMode)

		self.lineButton.image = lineImage
		self.triangleButton.image = triangleImage
		self.rectangleButton.image = rectangleImage
		self.circleButton.image = circleImage
		self.polygonButton.image = polygonImage

		self.lineButton.pack(side=TOP, padx=2, pady=2, fill=X)
		self.triangleButton.pack(side=TOP, padx=2, pady=2, fill=X)
		self.rectangleButton.pack(side=TOP, padx=2, pady=2, fill=X)
		self.circleButton.pack(side=TOP, padx=2, pady=2, fill=X)
		self.polygonButton.pack(side=TOP, padx=2, pady=2, fill=X)

		self.posLbl = Label(self.shapebar,text="X, Y",width=8,bg="light grey")
		self.posLbl.pack(side=BOTTOM, padx=2, pady=2, fill=X)

		self.shapebar.grid(row=1,column=0, sticky=NSEW)

	def createCanvas(self):
		self.canvas = Canvas(self.root, height=384, width=683, bg="white")
		self.canvas.bind("<Motion>",self.updPos)
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

	def updPos(self,event):
		self.posLbl.config(text= "{}, {}".format(event.x,event.y))

	def changeToRotate(self):	
		self.print("Selecione o ponto inicial da selecao",'system')
		self.canvas.bind("<Button-1>", self.rotateCanvas)
		self.update()
		
	def changeToScale(self):
		self.print("Selecione o ponto inicial da selecao",'system')
		self.canvas.bind("<Button-1>", self.scaleCanvas)
		self.update()

	def changeToTranslate(self):
		self.print("Selecione o ponto inicial da selecao",'system')
		self.canvas.bind("<Button-1>", self.translateCanvas)
		self.update()

	def changeToZoom(self):
		self.print("Selecione o ponto inicial da selecao",'system')
		self.canvas.bind("<Button-1>", self.zoomCanvas)
		self.update()
	
	def changeToLineMode(self):
		self.print("Selecione o primeiro ponto",'system')
		self.canvas.bind("<Button-1>", self.drawLine)
		self.update()

	def changeToTriangleMode(self):
		self.print("Selecione o primeiro ponto",'system')
		self.canvas.bind("<Button-1>", self.drawTriangle)
		self.update()

	def changeToRectangleMode(self):
		self.print("Selecione o primeiro ponto",'system')
		self.canvas.bind("<Button-1>", self.drawRectangle)
		self.update()

	def changeToPolygonMode(self):
		self.print("Selecione o primeiro ponto",'system')
		self.canvas.bind("<Button-1>", self.drawPolygon)
		self.canvas.bind("<Button-3>", self.drawPolygon)
		self.update()

	def changeToCircleMode(self):
		self.print("Selecione o centro do circulo",'system')
		self.canvas.bind("<Button-1>", self.drawCircle)
		self.update()


	def clearCanvas(self):
		self.shapes.clear()
		self.update()
		self.print("Tela limpada",'system')

	def undoAction(self,event):                        # Precisa criar um historico de estado para a implementacao de toda a funcionalidade desta func.
		if len(self.shapes)>0:
			self.canvas.delete(self.shapes.pop())
			self.update()

	def getClicks(self,event):
		self.clickNumber += 1
		self.clickCoords.append((event.x,event.y))
		self.print("({}, {})".format(event.x,event.y),'input')

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
		if self.clickNumber == 0:
			self.getClicks(event)
			self.print("Selecione o ponto final da selecao",'system')
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
			self.print("Objeto(s) transladado(s) {} no sentido X e {} no sentido Y".format(dx,dy),'system')

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
			self.print("Selecione o ponto final da selecao",'system')
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
			self.print("Objeto(s) escalado(s) por {} no sentido X e por {} no sentido Y".format(sx,sy),'system')

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
			self.print("Selecione o ponto final da selecao",'system')
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
			self.print("Objeto(s) rotacionado(s) em {} graus".format(sx,sy),'system')

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
		
		midX = (bigX + smallX)/2
		midY = (bigY + smallY)/2
		
		if (bigX - smallX) > (bigY - smallY):
			s = self.canvas.winfo_width()/(bigX - smallX)
		else:
			s = self.canvas.winfo_height()/(bigY - smallY)


		self.scale(self.shapes,(midX,midY),s,s)
		self.print(str(self.shapes),'wip')
	
	def zoomCanvas(self,event):
		if self.clickNumber == 0:
			self.getClicks(event)
			self.print("Selecione o ponto final da selecao",'system')
		else:
			self.getClicks(event)
			self.clickNumber = 0
			coord2 = self.clickCoords.pop()
			coord1 = self.clickCoords.pop()
			self.zoom(coord1,coord2)
			self.print("Zoom realizado com sucesso",'system')
			self.update()



	def centralizeCanvas(self):
		bigCoord = None
		smallCoord = None
		for shape in self.shapes:
			for coord in shape.coordinates:
				if bigCoord != None and smallCoord != None:
					if coord[0] > bigCoord[0]:
						bigCoord[0] = coord[0]
					if coord[0] < smallCoord[0]:
						smallCoord[0] = coord[0]
					if coord[1] > bigCoord[1]:
						bigCoord[1] = coord[1]
					if coord[1] < smallCoord[1]:
						smallCoord[1] = coord[1]
				else:
					bigCoord = list(coord)
					smallCoord = list(coord)

		midX = (bigCoord[0] + smallCoord[0])/2
		midY = (bigCoord[1] + smallCoord[1])/2

		midScreenX = self.canvas.winfo_width()/2
		midScreenY = self.canvas.winfo_height()/2
		dx = midScreenX - midX
		dy = midScreenY - midY


		self.translate(self.shapes,dx,dy)

		smallCoord[0] += dx-100
		smallCoord[1] += dy-100
		bigCoord[0] += dx+100
		bigCoord[1] += dy+100

		self.zoom(smallCoord,bigCoord)
		self.print("Objetos centralizados com sucesso",'system')	
		self.update()		

	def drawPolygon(self,event):
		if event.num == 1:
			self.getClicks(event)
			self.print("Selecione o proximo ponto (Botao direito para finalizar)",'system')
		elif event.num == 3:
			self.clickNumber = 0
			coords = []
			coords.extend(self.clickCoords)
			self.clickCoords.clear()
			self.shapes.append(Polygon(coords))
			self.update()
			self.print("Poligono finalizado",'system')
			
	def drawLine(self,event):
		if self.clickNumber < 1:
			self.getClicks(event)
			self.print("Selecione o segundo ponto",'system')
		else:
			self.getClicks(event)
			self.clickNumber = 0
			coord2 = self.clickCoords.pop()
			coord1 = self.clickCoords.pop()
			self.shapes.append(Line(coord1, coord2))
			self.update()

	def drawTriangle(self,event):
		if self.clickNumber == 0:
			self.getClicks(event)
			self.print("Selecione o segundo ponto",'system')
		elif self.clickNumber == 1:
			self.getClicks(event)
			self.print("Selecione o terceiro ponto",'system')
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
			self.print("Selecione o segundo ponto",'system')
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
			self.print("Selecione um ponto na circunferencia a ser desenhada",'system')
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