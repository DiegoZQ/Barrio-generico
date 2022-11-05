from basic_shapes import *
from drawable_shapes import *
from data_sender import Data_Sender

#Clase capaz de crear figuras integrado con un dataSender para manipular
#spotlights a voluntad, además de una lista llamada data con la información de cada
#una de las spotLights y un lightIndex, que representa EL MAYOR índice de los spotlights
#pertenecientes a la figura. 
class AdvancedShapeWithLight(AdvancedShape):

    #variable estática
    lightIndex = -1
    #spotLight apagada, usada para dar efecto de encendido/apagado
    spotLightOff = [[1,1,1], [1,1,1], 1,1,1,1,1, [0,0,0], [0,0,0]]

    #Se invoca con un pipeline y una lista con data.
    def __init__(self, pipeline, assets, instructions, data):
        super().__init__(pipeline, assets, instructions)
        self.data = data
        self.dataSender = Data_Sender(pipeline)
        #si es True, enciende; si no, apaga.
        self.on = True
        #El índice aumenta con las invocaciones y su valor de aumento depende 
        #únicamente de la cantidad de spotlights en la figura.
        AdvancedShapeWithLight.lightIndex+=len(self.data)
        self.lightIndex = AdvancedShapeWithLight.lightIndex

    #Ajusta una luz de la figura usando el índice de dicha luz y una data específica.
    def setLights(self, data, lightIndex):
        self.dataSender.setSpotLight(data, lightIndex)

    #Dibuja las luces usando una matriz de transformación
    def drawLights(self, location, rotation):
        x,y,z = location
        tMatrix = tr.matmul([tr.translate(x,y,z), tr.rotationZ(rotation)])
        lightIndex = self.lightIndex
        #Aplica las mismas transformaciones sobre las luces
        for i in range(len(self.data)):
            if self.on:
                data = self.data[i]
                newData0 = np.transpose([data[0]+[1]])
                newData1 = np.transpose([data[1]+[1]])
                lightPos = np.transpose(tr.matmul([tMatrix, newData0]))[0][:3]
                lightDir = np.transpose(tr.matmul([tr.rotationZ(rotation), newData1]))[0][:3]
                transformedData = [lightPos.tolist()] + [lightDir.tolist()] + data[2:]
                self.setLights(transformedData, lightIndex)
            else:
                self.setLights(AdvancedShapeWithLight.spotLightOff, lightIndex)
            lightIndex-=1

    #Dibuja la figura en una rotaciónZ y posición específica del mapa. También realiza 
    #las mismas transformaciones sobre las luces, para que vayan a la par con la figura.
    def draw(self, location, rotation, time):
        super().draw(location, rotation)
        self.drawLights(location, rotation)
        self.turnLights(time)
        
    #Apaga o enciende las luces, dependiendo el tiempo. Por defecto, si es entre las 8 y 16 hrs, 
    #las apaga; si no, las enciende.
    def turnLights(self, time):
        time = time%24
        if time > 8 and time < 18:
            self.on = False
        else:
            self.on = True

#Lo mismo que AdvancedShapeWithLight, sólo que ahora existe la posibilidad de agregar más de un gpuShape.
#Esto con el fin de aplicar ciertas transformaciones sobre subconjuntos de la figura, para simular movimiento.
class AdvancedMultiShapeWithLight(AdvancedShapeWithLight):
    def __init__(self, pipeline, assets, instructions, data):
        #Ahora hay más de 1 gpuShape
        self.gpuShapes = []
        super().__init__(pipeline, assets, instructions, data)
   
    #Ahora cada setGPUShape añade una gpuShape a la lista de gpuShapes, le asigna la textura
    #y vacía la baseShape para posteriormente añadir otra gpuShape.   
    def setGPUShape(self):
        self.gpuShapes += [createGPUShape(self.pipeline, self.baseShape, GL_STATIC_DRAW)]
        self.gpuShapes[-1].texture = textureSimpleSetup(getAssetPath(self.assets), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
        self.baseShape = Shape([], 8, [])

    #Dibuja cada gpuShape con su respectiva matriz del método move.
    def draw(self, location, rotation, time):
        x,y,z = location
        for i in range(len(self.gpuShapes)):
            draw(self.pipeline, self.gpuShapes[i], [tr.translate(x,y,z), tr.rotationZ(rotation)] + self.move(i, time))
        self.drawLights(location, rotation)
        self.turnLights(time)


    #Limpia todos los gpuShapes de la figura
    def clear(self):
        for shape in self.gpuShapes:
            shape.clear()

    #Retorna una o varias matrices de transformación dependiendo del índice de la figura
    #Se determina según la clase
    def move(self, index, time):
        return tr.identity()

#Crea un auto con 2 luces y movimiento en sus ruedas.
class Car(AdvancedMultiShapeWithLight):
    def __init__(self, pipeline):
        #2 spotlights
        data = [ [[-0.16, -0.34, 0.31], [0,-1,0], 0.7, 0.7, 0.4, 0.5, 0.3, [1,1,1],[1,1,1]] ,
                 [[0.16, -0.34, 0.31], [0,-1,0], 0.7, 0.7, 0.4, 0.5, 0.3, [1,1,1],[1,1,1]] ]
        super().__init__(pipeline,"car.jpg", "car.instructions", data)
        self.moveShapes = [1]

    #Si la gpuShape es una rueda, le aplica una rotación en el tiempo para
    #simular movimiento y una traslación específica dependiendo del índice.
    def move(self, index, time):
        time *= 8
        if index == 1:
            return [tr.translate(-0.22,-0.29,0.135), tr.rotationX(time)] 
        if index == 2:
            return [tr.translate(-0.22,0.29,0.135), tr.rotationX(time)] 
        if index == 3:
            return [tr.translate(0.22,-0.29,0.135), tr.rotationX(time)] 
        if index == 4:
            return [tr.translate(0.22,0.29,0.135), tr.rotationX(time)] 
        else:
            return [tr.identity()]