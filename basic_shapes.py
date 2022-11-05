import numpy as np
import copy

#La clase Shape es la encargada de servir como contenedor para almacenar información sobre
#los vértices, su cantidad de atributos (strideSize) y valores correspondientes tales como
#posición, color rgb, etc. Además contiene los índices de los vértices que se usarán para 
#formar los triángulos que posteriormente se dibujarán. 
class Shape:
    def __init__(self, vertexData, vertexStride, indexData):
        self.vertexData = vertexData
        self.indexData = indexData
        self.vertexStride = vertexStride

    #Mezcla otra shape con la Shape actual.
    def merge(self, anotherShape):
        #desplazamiento del índice de los vértices de la otra Shape que se va a mezclar.
        offset = len(self.vertexData)/self.vertexStride
        self.vertexData += anotherShape.vertexData
        self.indexData += [offset + index for index in anotherShape.indexData]
        return self

    #Traslada todos los vértices de la Shape usando un vector de traslación x, y, z.
    def translate(self, translation):
        for i in range(0, len(self.vertexData), self.vertexStride):
            self.vertexData[i] += translation[0]
            self.vertexData[i+1] += translation[1]
            self.vertexData[i+2] += translation[2]
        return self

    #Escala todos los vértices de la Shape usando un vector de escalamiento x, y, z.
    def scale(self, scaleFactor):
        for i in range(0, len(self.vertexData), self.vertexStride):
            self.vertexData[i] *= scaleFactor[0]
            self.vertexData[i+1] *= scaleFactor[1]
            self.vertexData[i+2] *= scaleFactor[2]
        return self

    #Rota verticalmente la figura usando un ángulo.
    def verticalRotate(self, angle):
        for i in range(0, len(self.vertexData), self.vertexStride):
            y = self.vertexData[i+1]
            z = self.vertexData[i+2]
            self.vertexData[i+1] = y*np.cos(angle) - z*np.sin(angle)
            self.vertexData[i+2] = y*np.sin(angle) + z*np.cos(angle)
            normY = self.vertexData[i+6]
            normZ = self.vertexData[i+7]
            self.vertexData[i+6] = normY*np.cos(angle) - normZ*np.sin(angle)
            self.vertexData[i+7] = normY*np.sin(angle) + normZ*np.cos(angle)
        return self

    #Rota horizontalmente la figura usando un ángulo.
    def horizontalRotate(self, angle):
        for i in range(0, len(self.vertexData), self.vertexStride):
            x = self.vertexData[i]
            y = self.vertexData[i+1]
            self.vertexData[i] = x*np.cos(angle) - y*np.sin(angle)
            self.vertexData[i+1] = x*np.sin(angle) + y*np.cos(angle)
            normX = self.vertexData[i+5]
            normY = self.vertexData[i+6]
            self.vertexData[i+5] = normX*np.cos(angle) - normY*np.sin(angle)
            self.vertexData[i+6] = normX*np.sin(angle) + normY*np.cos(angle)
        return self

    #Encuentra el cuadrante de textura de una figura
    def findTextureMaxMin(self):
        nxMax, nxMin = 0, 10
        nyMax, nyMin = 0, 10
        for i in range(0, len(self.vertexData), self.vertexStride):
            if self.vertexData[i+3] > nxMax:
                nxMax = self.vertexData[i+3]
            if self.vertexData[i+3] < nxMin:
                nxMin = self.vertexData[i+3]
            if self.vertexData[i+4] > nyMax:
                nyMax = self.vertexData[i+4]
            if self.vertexData[i+4] < nyMin:
                nyMin = self.vertexData[i+4]
        return [nxMin, nxMax], [nyMin, nyMax]
        
    #Estira en el eje Z una cantidad específica una determinada figura PLANA (1 cara).
    def stretch(self, stretch):
        secondShape = copy.deepcopy(self)
        secondShape.translate([0,0,stretch])
        size = len(self.vertexData)
        stride = self.vertexStride 
        nx, ny = self.findTextureMaxMin()
        #Se agregan todas las shapes perpendiculares al eje z.
        for i in range(0, size, stride):
            actualVertices = len(self.vertexData)/stride
            j = (i+stride)%size
            v1 = np.array(self.vertexData[i:i+2]+[0])
            v2 = np.array(self.vertexData[j:j+2]+[0])
            v = v1-v2
            u = np.array([0,0,1])
            n = np.cross(u,v).tolist() #vector normal al plano
            self.vertexData+=self.vertexData[i:i+3]+[nx[0]]+[ny[0]] + n #primer vertice de abajo
            self.vertexData+=self.vertexData[j:j+3]+[nx[1]]+[ny[0]] + n #primer vertice de arriba
            self.vertexData+=self.vertexData[i:i+2]+[self.vertexData[i+2]+stretch]+[nx[0]]+[ny[1]] + n #segundo vértice de abajo
            self.vertexData+=self.vertexData[j:j+2]+[self.vertexData[j+2]+stretch]+[nx[1]]+[ny[1]] + n #segundo vértice de arriba
        
            #se unen los triángulos del paralelogramo
            self.indexData+=[actualVertices, actualVertices+1, actualVertices+2,
                            actualVertices+1, actualVertices+2, actualVertices+3]

        #La normal en z de la figura plana inicial
        normalZ = self.vertexData[7]
        #Determina cuál cara en el eje z de la actual figura estirada debe ser Z+ y cuál Z-.
        for i in range(0, size, stride):
            if ((stretch>=0 and normalZ>=0) or (stretch<0 and normalZ<0)):
                self.vertexData[i+5:i+8] =  (np.array(self.vertexData[i+5:i+8])*-1).tolist() 
            if ((stretch>=0 and normalZ<0) or (stretch<0 and normalZ>=0)):
                secondShape.vertexData[i+5:i+8] = (np.array(self.vertexData[i+5:i+8])*-1).tolist() 
        
        self.merge(secondShape)
        return self

#Crea un cuadrado utilizando las coordenadas a un bloque de textura de un asset específico.
def createTextureQuad(nx, ny): 
    #bloque de textura de la forma: [(nxStart, nyStart), (nxEnd, nyEnd)]; nx,ny entre 0 y 1.
    #partiendo en la esquina superior izquierda y terminando en la esquina inferior derecha del asset.
    vertexData = [
    #   positions        texture         #normals
        -0.5, -0.5, 0.0,  nx[0], ny[1],  0,0,1,#nxStart, nyEnd
         0.5, -0.5, 0.0, nx[1], ny[1],   0,0,1, #nxEnd, nyEnd
         0.5,  0.5, 0.0, nx[1], ny[0],   0,0,1, #nxEnd, nyStart
        -0.5,  0.5, 0.0,  nx[0], ny[0],  0,0,1] #nxStart, nyStart
    indexData = [
         0, 1, 2,
         2, 3, 0]
    return Shape(vertexData, 8, indexData)

#Crea un triángulo con textura.
def createTextureTriangle(nx, ny):
    vertexData = [
    #   positions        texture                         #normals
        -0.5, -0.5, 0.0,  nx[0], ny[1],                   0,0,1,
         0.5, -0.5, 0.0,  nx[1], ny[1],                   0,0,1,
         0.0,  0.5, 0.0,  nx[0] + (nx[1]-nx[0])/2, ny[0], 0,0,1]  
    indexData = [0, 1, 2]
    return Shape(vertexData, 8, indexData)

#Crea un triángulo rectángulo con textura.
def createTextureTriangleRectangle(nx,ny):   
    vertexData = [
    #   positions        texture          normals
        -0.5, -0.5, 0.0,  nx[0], ny[1],    0,0,1, 
         0.5, -0.5, 0.0,  nx[1], ny[1],    0,0,1,
         0.5,  0.5, 0.0,  nx[1], ny[0],    0,0,1] 
    indexData = [0, 1, 2]
    return Shape(vertexData, 8, indexData)

#Crea un trapecio con textura.
def createTextureTrapecio(nx,ny):
    vertexData = [
    #   positions        texture                            normals
        -0.25, -0.5, 0.0, nx[0]+(nx[1]-nx[0])*0.25, ny[1],  0,0,1, 
         0.25, -0.5, 0.0, nx[0]+(nx[1]-nx[0])*0.75, ny[1],  0,0,1,
         0.5,  0.5, 0.0, nx[1], ny[0],                      0,0,1,
        -0.5,  0.5, 0.0, nx[0], ny[0],                      0,0,1] 
    indexData = [
         0, 1, 2,
         2, 3, 0]
    return Shape(vertexData, 8, indexData)    

#Crea un tubo rectangular con textura (cubo sin tapas horizontales).
def createTextureRectangularPipe(nx,ny):
    pipe = createTextureQuad(nx,ny).verticalRotate(-np.pi/2).translate([0,0.5,0]) #Y+
    pipe.merge(createTextureQuad(nx,ny).verticalRotate(np.pi/2).translate([0,-0.5,0])) #Y-
    pipe.merge(createTextureQuad(nx,ny).verticalRotate(np.pi/2).horizontalRotate(np.pi/2).translate([0.5,0,0])) #X+
    pipe.merge(createTextureQuad(nx,ny).verticalRotate(np.pi/2).horizontalRotate(-np.pi/2).translate([-0.5,0,0])) #X-
    return pipe

#Cre un cubo con textura.
def createTextureCube(nx, ny):
    cube = createTextureRectangularPipe(nx,ny)
    cube.merge(createTextureQuad(nx,ny).verticalRotate(np.pi).translate([0,0,-0.5])) #Z-
    cube.merge(createTextureQuad(nx,ny).translate([0,0,0.5])) #Z+
    return cube

#Crea un marco con textura de un grosor específico.
def createTextureFrame(nx,ny, width):
    frame = createTextureCube([nx[0],nx[1]],[ny[0],ny[1]]).scale([width,1+width,0.02]).translate([0.5,0,0])
    frame.merge(createTextureCube([nx[0],nx[1]],[ny[0],ny[1]]).scale([width,1+width,0.02]).translate([-0.5,0,0]))
    frame.merge(createTextureCube([nx[0],nx[1]],[ny[0],ny[1]]).scale([1-width,width,0.02]).translate([0,0.5,0]))
    frame.merge(createTextureCube([nx[0],nx[1]],[ny[0],ny[1]]).scale([1-width,width,0.02]).translate([0,-0.5,0]))
    return frame

#Crea un marco con textura de un grosor específico con una cruz al medio. 
def createTextureCrossFrame(nx,ny, widht):
    frame = createTextureFrame(nx,ny, widht)
    frame.merge(createTextureCube([nx[0],nx[1]],[ny[0],ny[1]]).scale([1-widht,widht,0.02]))
    frame.merge(createTextureCube([nx[0],nx[1]],[ny[0],ny[1]]).scale([widht,1-widht,0.02]))
    return frame

#Crea un slice con textura, ángulo y número de puntos que tendrá (para suavizar la curva).
def createTextureSlice(nx, ny, angulo, N):
    nxM = (nx[0]+nx[1])/2
    nyM = (ny[0]+ny[1])/2
    nxR = nx[1] - nxM
    nyR = ny[1] - nyM
    #centro
    vertexData = [
        # posición     # texture
        0.0, 0.0, 0.0, nxM, nyM, 0, 0, 1
    ]
    indexData = []
    deltaAngulo = angulo/N
    for i in range(0, N+1):
        vertexData += [np.cos(i*deltaAngulo), np.sin(i*deltaAngulo), 0, nxM + nxR*np.cos(i*deltaAngulo), nyM + nyR*np.sin(-i*deltaAngulo), 0, 0, 1]
        if (i!=N):
            indexData += [0, i+1, i+2]

    return Shape(vertexData, 8, indexData)

#Crea un círculo con textura y número de puntos que tendrá (para suavizar la curva).
def createTextureCircle(nx,ny, N):
    return createTextureSlice(nx,ny,2*np.pi, N)