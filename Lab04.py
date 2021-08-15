# Grafica de Computadoras

# -----------------------------------------------------------------------
# DISCLAIMER: Dado que no contamos con tanto espacio de memoria
# he de aclarar que se evadio la programación defensiva, esto con el 
# proposito de parecerse lo mas posible a una libreria y no un programa
# -----------------------------------------------------------------------

from vecTools import VecTools
import struct
from collections import namedtuple
vt = VecTools()

def char(c): # 1 bit
  return struct.pack('=c', c.encode('ascii'))

def word(w): # 2 bits
  return struct.pack('=h', w)

def dword(dw): # 4 bits
  return struct.pack('=l', dw)

def color(b, g, r): # generador de colores
  return bytes([b, g, r])

bk = color(0, 0, 0)
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

class renderer():
	def __init__(self):
		self.currentColor = bk
		self.frBff = []
		self.glInit()
		
	def glCreatorWindow(self, width, height): # Crea la ventana, ancho x alto
		fb = [
			[0 for x in range(width)] # Inicializa el framebuffer con ceros
			for y in range(height)
			]
		return fb

	def glViewPort(self, x, y, width, height): # Crea delimitantes a partir de limites
		width = round(width/2,1)
		height = round(height/2,1)
		xMin = x - width
		xMax = x + width
		yMin = y - height
		yMax = y + height

		return xMin, xMax, yMin, yMax

	def glClear(self): # Limpia el framebuffer aplicandole color rojo
		self.frBff =  [
		[color(0,0,255) for x in range(len(self.frBff))]
		for y in range(len(self.frBff[0]))
		]
		return self.frBff

	def glClearColor(self, r, g, b): # Personaliza el color del framebuffer
		lgt = self.frBff
		self.frBff =  [
		[color(round(r*255), round(g*255), round(b*255)) for x in range(len(lgt))]
		for y in range(len(lgt[0]))
		]
		return self.frBff

	def vertex(self,x,y): # Ubica un punto dentro del viewPort
		try:
			self.frBff[x][y] = self.currentColor
		except:
			pass
 
	def line(self,start,end): # Traza líneas de manera más eficiente
		x1, y1 = start
		x2, y2 = end

		dy = abs(y2 - y1)
		dx = abs(x2 - x1)
		steep = dy > dx

		if steep:
			x1, y1 = y1, x1
			x2, y2 = y2, x2

		if x1 > x2:
			x1, x2 = x2, x1
			y1, y2 = y2, y1

		dy = abs(y2 - y1)
		dx = abs(x2 - x1)

		offset = 0
		threshold = dx

		y = y1
		for x in range(x1, x2 + 1):
			if steep:
				self.vertex(y, x)
			else:
				self.vertex(x, y)
			
			offset += dy * 2
			if offset >= threshold:
				y += 1 if y1 < y2 else -1
				threshold += dx * 2

	def write(self, filename, width, height, framebuffer): # Escribe el .bmp
		
		f = open(filename, 'bw')

		# file header 14
		f.write(char('B'))
		f.write(char('M'))
		f.write(dword(14 + 40 + 3*(width*height)))
		f.write(dword(0))
		f.write(dword(54))

		# info header 40
		f.write(dword(40))
		f.write(dword(width))
		f.write(dword(height))
		f.write(word(1))
		f.write(word(24))
		f.write(dword(0))
		f.write(dword(3*(width*height)))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))

		# bitmap
		for y in range(height):
			for x in range(width):
				f.write(framebuffer[x][y])

		f.close()

	def glColor(self, r, g, b): # Cambia el color recurrente
		self.currentColor = color(round(r*255), round(g*255), round(b*255))

	def glFinish(self): # Ejecuta la inscripcion del bitmap
		self.write('renderedObj.bmp', len(self.frBff), len(self.frBff[0]), self.frBff)

	def normalXY(self, x0, y0, x1, y1): # Convierte las coordenadas normalizadas a normales
		
		xMin, xMax, yMin, yMax = self.glViewPort(
			self.width/2, self.height/2, self.width, self.height
			)
			# Traduccion de los puntos ingresados
		points = [x0, y0, x1, y1]
		values = points
		# Posible cancelacion de valores normalizados
		"""
		mid = 0
		currentMin = 0
		currentMax = 0

		for i in values: # Establece los valores segun el eje
			index = values.index(i)
			if (index%2 == 0): 
				mid = round((xMax-xMin)*0.5)
				currentMin = xMin
				currentMax = xMax
			else:
				mid = round((yMax-yMin)*0.5)
				currentMin = yMin
				currentMax = yMax
			if ((i >= -2 and i <= 2)): # Si esta en rango
				# Casos 
				if (i < 0 and i >= -2):
					i += 2
					i = i*0.5
					i = currentMin + round(i*mid)
				elif (i > 0 and i <= 2):
					i = 2 - i
					i = i*0.5
					i = currentMax - round(i*mid)
				elif i == 0:
					i = currentMin + mid
				values[index] = int(i)
			else:
				return None
		"""
		return values
	
	# ---------------------------------------------------------------
	# IMPROVABLE FUNCTIONAL GLINE FUNCTION
	# ---------------------------------------------------------------

	def largeSlope(self, currentX, finalX, currentY, finalY, slope, sign): # Ejecuta para pendientes empinadas
		
		# Identifica direccion de la pendiente
		adder = 0
		if sign == '-':
			adder = -1
		elif sign == '+':
			adder = 1

		self.vertex(currentX, currentY) # Rellena
		flag = round(currentX + slope)
		for i in range(currentX+adder, flag, adder):
			if (adder == -1): 
				if ((currentX >= finalX) and (currentY <= finalY)):
					self.vertex(i, currentY) # Rellena
					currentX += adder
			elif (adder == 1):
				if ((currentX <= abs(finalX)) and (currentY <= abs(finalY))):
					self.vertex(i, currentY) # Rellena
					currentX += adder
		return flag

	def glLine(self, x0, y0, x1, y1): # Pinta una linea

		currentColor = self.currentColor
		values = self.normalXY(x0, y0, x1, y1)
		currentX = values[0]
		currentY = values[1]
		finalX = values[2]
		finalY = values[3]
		
		if (finalY - currentY) != 0: # Si la linea no es sobre el mismo punto Y
			slope = (finalX - currentX)/(finalY - currentY)
			# Pendientes Negativas
			if slope < 0:
				# Permite la reversibilidad de las coordenadas
				if ((finalX > currentX) and (finalY < currentY)):
					finalX, currentX = currentX, finalX
					finalY, currentY = currentY, finalY
				# Pendientes muy inclinadas
				if slope <= -1:
					# Mientras no sobrepase los limites
					while ((currentX >= finalX) and (currentY <= finalY)):
						# Suma el valor del slope por cada iteracion
						currentX = self.largeSlope(currentX, finalX, currentY, finalY, slope, '-')
						currentY += 1
				# Pendientes menores a los 45 grados
				if slope > -1:
					while ((currentX >= finalX) and (currentY <= finalY)):
						self.vertex(round(currentX), currentY)
						currentX += slope
						currentY += 1
			# Permite la reversibilidad de las coordenadas
			if ((finalX < currentX) and (finalY < currentY)):
				finalX, currentX = currentX, finalX
				finalY, currentY = currentY, finalY
			# Pendientes Positivas
			absX = abs(finalX)
			absY = abs(finalY)
			# Pendientes Arriba de los 45 grados
			if slope >= 1:
				while ((currentX <= absX) and (currentY <= absY)):
					# Suma el valor del slope por cada iteracion
					currentX = self.largeSlope(currentX, finalX, currentY, finalY, slope, '+')
					currentY += 1
			# Pendientes Abajo de los 45 grados
			elif slope < 1:
				while ((currentX <= absX) and (currentY <= absY)):
					self.vertex(round(currentX), currentY)
					currentX += slope
					currentY += 1
		elif (finalY - currentY) == 0:
			absX = abs(finalX)
			if (finalX < currentX):
				finalX, currentX = currentX, finalX

			while ((currentX <= absX)):
				for i in range(currentX, finalX+1):
					self.vertex(i, currentY) # Rellena
					currentX += 1
	"""
	def polygonOne():

		# Raw coordinates are been submitted 
		glLine(165, 380,185, 360)
		glLine(185, 360,180, 330)
		glLine(180, 330,207, 345)
		glLine(207, 345,233, 330)
		glLine(233, 330,230, 360)
		glLine(230, 360,250, 380) 
		glLine(250, 380,220, 385) 
		glLine(220, 385,205, 410) 
		glLine(205, 410,193, 383) 
		glLine(193, 383,165, 380)

		masterFill("polygonOne")

	def polygonTwo():

		# Raw coordinates are been submitted 
		glLine(321, 335,288, 286)
		glLine(288, 286,339, 251)
		glLine(339, 251,374, 302)
		glLine(374, 302,321, 335)

		masterFill("polygonTwo")

	def polygonThree():

		# Raw coordinates are been submitted 
		glLine(377, 249,411, 197)
		glLine(411, 197,436, 249)
		glLine(436, 249,377, 249)

		masterFill("polygonThree")

	def polygonFour():

		# Raw coordinates are been submitted 
		glLine(413, 177,448, 159)
		glLine(448, 159,502, 88)
		glLine(502, 88,553, 53)
		glLine(553, 53,535, 36)
		glLine(535, 36,676, 37)
		glLine(676, 37,660, 52)
		glLine(660, 52,750, 145)
		glLine(750, 145,761, 179)
		glLine(761, 179,672, 192)
		glLine(672, 192,659, 214)
		glLine(659, 214,615, 214)
		glLine(615, 214,632, 230)
		glLine(632, 230,580, 230)
		glLine(580, 230,597, 215)
		glLine(597, 215,552, 214)
		glLine(552, 214,517, 144)
		glLine(517, 144,466, 180)
		glLine(466, 180,413, 177)

		masterFill("polygonFour")

	def polygonFive():

		# Raw coordinates are been submitted 
		glLine(682, 175,708, 120)
		glLine(708, 120,735, 148)
		glLine(735, 148,739, 170)
		glLine(739, 170,682, 175)

		masterFill("polygonFive")
	
	def masterFill(name):

		name = name + ".bmp"
		for x in range(len(frBff)):
			inter = []
			flag = True
			flag_2 = 0
			for y in range(len(frBff[x])):
				if frBff[y][x] == currentColor:
					if flag == True:
						inter.append([x,y])
						flag = False
					elif flag == False:
						if y != inter[flag_2][1]+1:
							inter.append([x,y])
							flag_2 += 1
					
			if len(inter) == 2:
				glLine(inter[0][0], inter[0][1], inter[1][0], inter[1][1])
		
			if len(inter) == 4:
				glLine(inter[0][0], inter[0][1], inter[1][0], inter[1][1])
				glLine(inter[2][0], inter[2][1], inter[3][0], inter[3][1])

		write(name, len(frBff), len(frBff[0]), frBff)
	"""
	def obj(self,filename): # Realiza la lectura del obj
		with open(filename) as f:
			self.lines = f.read().splitlines()
			self.vertices = []
			self.verticesT = []
			self.verticesN = []
			self.faces = []
			self.read()

	def read(self): # Realiza la lectura del obj, parte 2
		for line in self.lines:
			if line:
				prefix, value = line.split(' ', 1)
				if prefix == 'v':
					self.vertices.append(list(map(float, value.split(' '))))
				elif prefix == 'vt':
					self.verticesT.append(list(map(float, value.split(' '))))
				elif prefix == 'vn':
					self.verticesN.append(list(map(float, value.split(' '))))
				elif prefix == 'f':
					self.faces.append([list(map(int , face.split('/'))) for face in value.split(' ')])
	
	def triangle(self, A, B, C, color=None):
		bbox_min, bbox_max = vt.bbox(A, B, C)

		for x in range(bbox_min.x, bbox_max.x + 1):
			for y in range(bbox_min.y, bbox_max.y + 1):
				w, v, u = vt.barycentric(A, B, C, V2(x, y))
				if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
					continue
			
			self.vertex(x, y)

	def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
		# returns a vertex 3, translated and transformed
		return V3(
		round((vertex[0] + translate[0]) * scale[0]),
		round((vertex[1] + translate[1]) * scale[1]),
		round((vertex[2] + translate[2]) * scale[2])
		)

	def load_dennis(self, filename, translate=(0, 0, 0), scale=(1, 1, 1)):
		"""
		Loads an obj file in the screen
		wireframe only
		Input: 
		filename: the full path of the obj file
		translate: (translateX, translateY) how much the model will be translated during render
		scale: (scaleX, scaleY) how much the model should be scaled
		"""
		self.obj(filename)

		light = V3(0,0,1)

		for face in self.faces:
			vcount = len(face)

			if vcount == 3:
				f1 = face[0][0] - 1
				f2 = face[1][0] - 1
				f3 = face[2][0] - 1

				a = self.transform(self.vertices[f1], translate, scale)
				b = self.transform(self.vertices[f2], translate, scale)
				c = self.transform(self.vertices[f3], translate, scale)

				normal = vt.normal(vt.cross(vt.sub(b, a), vt.sub(c, a)))
				intensity = vt.dot(normal, light)
				grey = round(255 * intensity)
				if grey < 0:
					continue  
			
				self.triangle(a, b, c, color(grey, grey, grey))
			else:
				# assuming 4
				f1 = face[0][0] - 1
				f2 = face[1][0] - 1
				f3 = face[2][0] - 1
				f4 = face[3][0] - 1   

			vertices = [
				self.transform(self.vertices[f1], translate, scale),
				self.transform(self.vertices[f2], translate, scale),
				self.transform(self.vertices[f3], translate, scale),
				self.transform(self.vertices[f4], translate, scale)
			]

			normal = vt.normal(vt.cross(vt.sub(vertices[0], vertices[1]), vt.sub(vertices[1], vertices[2])))  # no necesitamos dos normales!!
			intensity = vt.dot(normal, light)
			grey = round(255 * intensity)
			if grey < 0:
				continue # dont paint this face

			# vertices are ordered, no need to sort!
			# vertices.sort(key=lambda v: v.x + v.y)
	
			A, B, C, D = vertices 
			
			self.triangle(A, B, C, color(grey, grey, grey))
			self.triangle(A, C, D, color(grey, grey, grey))


	def load(self, filename, translate, scale):
		self.obj(filename)
		
		for face in self.faces:
			vcount = len(face)

			for j in range(vcount):
				f1 = face[j][0]
				f2 = face[(j + 1) % vcount][0]

				v1 = self.vertices[f1 - 1]
				v2 = self.vertices[f2 - 1]
				
				x1 = round((v1[0] + translate[0]) * scale[0])
				y1 = round((v1[1] + translate[1]) * scale[1])
				x2 = round((v2[0] + translate[0]) * scale[0])
				y2 = round((v2[1] + translate[1]) * scale[1])
				self.line((x1, y1), (x2, y2))

	def glInit(self): # Inicializa el programa
		
		self.currentColor = color(1,0,0)
		self.width = 1024
		self.height =  1024
		self.frBff = self.glCreatorWindow(self.width, self.height) # Framebuffer
		self.frBff = self.glClear() # Pinta el bg de un color
		self.frBff = self.glClearColor(0,0,1) # Modifica color de bg
		self.glColor(0,0,0)
		self.load_dennis("face.obj", [25,25,25], [5,5,5])

		"""
		if polygon == "polygonOne":
			polygonOne() # 70% completed
		elif polygon == "polygonTwo":
			polygonTwo() # 100% completed
		elif polygon == "polygonThree":
			polygonThree() # 90% completed
		elif polygon == "polygonFour":
			polygonFour() # 75% completed
		elif polygon == "polygonFive":
			polygonFive() # 80% completed

		# LAB 1 -----------------------------------------------
		# vertex(1,1)
		# vertex(0,0)
		# vertex(-1,-1)

		# LAB 2 -----------------------------------------------
		"""

		self.glFinish()

renderer()
