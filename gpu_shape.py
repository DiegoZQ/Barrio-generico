from OpenGL.GL import *
import numpy as np
from constants import SIZE_IN_BYTES

#La clase GPUShape es la encargada de contener información de VAO, VBO y texturas
#para guardarlas en la memoria GPU.
class GPUShape:
    def __init__(self):
        self.vao = None
        self.vbo = None
        self.ebo = None
        self.texture = None
        self.size = None

    #Inicializa los buffers de OpenGL en vao, vbo, ebo y se retorna a sí mismo.
    def initBuffers(self):
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        return self

    #Rellena los buffers usando la información de vertexData e indexData proporcionadas por
    #una shape. 
    def fillBuffers(self, vertexData, indexData, usage):
        vertexData = np.array(vertexData, dtype=np.float32)
        indexData = np.array(indexData, dtype=np.uint32)
        self.size = len(indexData)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(vertexData) * SIZE_IN_BYTES, vertexData, usage) #
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indexData) * SIZE_IN_BYTES, indexData, usage) #
  
    #Libera la memoria GPU de la gpuShape
    def clear(self):
        if self.vao != None:
            glDeleteVertexArrays(1, [self.vao])
        if self.vbo != None:
            glDeleteBuffers(1, [self.vbo])
        if self.ebo != None:
            glDeleteBuffers(1, [self.ebo])
        if self.texture != None:
            glDeleteTextures(1, [self.texture])