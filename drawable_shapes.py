from gpu_shape import GPUShape
from OpenGL.GL import *
import transformations as tr
from basic_shapes import *
from easy_shaders import textureSimpleSetup
from path import getAssetPath, getInstructionPath

#Módulo encargado de simplificar las tareas de crear
#un gpuShape y dibujarlo.

#Crea un gpuShape a partir de un pipeline y un shape.
def createGPUShape(pipeline, shape, usage):
    gpuShape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertexData, shape.indexData, usage)
    return gpuShape

#Dibuja un gpuShape usando transformaciones y un pipeline.
def draw(pipeline, gpuShape, transformations):
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,
        tr.matmul(transformations)
    )
    pipeline.drawCall(gpuShape)

#Clase abstracta encargada de servir como base para la posterior creación de figuras
#complejas con texturas.
class AbstractShape():
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.assets = None
        self.baseShape = Shape([], 8, [])
        self.gpuShape = None

    #Añade otra figura a la figura base.
    def addShape(self, anotherShape):
        self.baseShape.merge(anotherShape)

    #Setea la gpuShape de la figura luego de haber armado por completo la baseShape.
    def setGPUShape(self):
        self.gpuShape = createGPUShape(self.pipeline, self.baseShape, GL_STATIC_DRAW)
        self.gpuShape.texture = textureSimpleSetup(getAssetPath(self.assets), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    #Obtiene la forma final de la figura y la deja lista para ser dibujada.
    def getGPUShape(self):
        #Hace algo
        #...
        self.setGPUShape()

    #Dibuja la figura en una posición y rotación específica en el mapa.
    def draw(self, location, rotation):
        x,y,z = location 
        draw(self.pipeline, self.gpuShape, [tr.matmul([tr.translate(x,y,z), tr.rotationZ(rotation)])])

    #Limpia la gpuShape.
    def clear(self):
        self.gpuShape.clear()

#Permite crear figuras avanzadas de manera simple haciendo uso de un set de instrucciones localizado
#en la carpeta instructions.
class AdvancedShape(AbstractShape):
    def __init__(self, pipeline, assets, instructions):
        super().__init__(pipeline)
        self.assets = assets
        self.instructions = instructions
        self.getGPUShape()

    #Ejecuta las instrucciones para obtener la GPUShape.
    def getGPUShape(self):
        exec(open(getInstructionPath(self.instructions)).read())