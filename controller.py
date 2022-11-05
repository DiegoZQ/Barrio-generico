import numpy as np
import transformations as tr
import glfw
from OpenGL.GL import *
import constants as const
import copy

#Crea un controlador para la cámara con una posición viewPos y un lugar para mirar viewAt.
class Controller:
    def __init__(self):
        self.viewPos = np.array([0, 0, 1], np.float32)
        self.viewAt  = np.array([0, 1, 1], np.float32)
        self.angles = np.array([0,0], dtype=np.float32)
        self.fillPolygon = True
        self.projection = True #true significa en perspectiva y false ortogonal.
        self.isKeyPressed = np.zeros(342)

    #Revisa si una posición x,y está o no dentro de la escena. True si lo está;
    #False si no.
    def checkPos(self, x, y):
        #eje x
        boolX = x > -12.5 and x < 12.5
        #eje y
        boolY = y > -12.8 and y < 12.8
        #diagonal
        boolD = y - 1.6*x - 21 < 0
        return boolX and boolY and boolD

    #Permite a la cámara moverse una distancia específica en un eje específico.
    def move(self, distance, axis):
        vector = self.viewAt - self.viewPos
        #Testea la posición del viewPos antes de efectuar el cambio.
        viewPosTest = copy.deepcopy(self.viewPos) 
        #Move back and forward
        if axis == 'x':
            viewPosTest += vector * distance  
            if self.checkPos(viewPosTest[0], viewPosTest[1]):
                self.viewPos = viewPosTest
                self.viewAt += vector * distance
        #Strafe
        if axis == 'y':
            #hace que la magnitud del vector sea independiente del eje z.
            vector *= np.linalg.norm(vector) / np.linalg.norm([vector[0], vector[1]])
            viewPosTest[0] -= vector[1] * distance
            viewPosTest[1] += vector[0] * distance
            if self.checkPos(viewPosTest[0], viewPosTest[1]):
                self.viewPos = viewPosTest
                self.viewAt[0] -= vector[1] * distance
                self.viewAt[1] += vector[0] * distance

    #Rota la posición de la cámara con respecto al origen.
    def rotate(self): 
        self.viewAt[0] = np.sin(np.pi/2 - self.angles[1]) * np.cos(self.angles[0])
        self.viewAt[1] = np.sin(np.pi/2 - self.angles[1]) * np.sin(self.angles[0])
        self.viewAt[2] = np.cos(np.pi/2 - self.angles[1])
        self.viewAt += self.viewPos

    def checkPressedKeys(self):
        #Se mueve hacia la izquierda.
        if self.isKeyPressed[glfw.KEY_A]:
            self.move(const.SPEED, 'y')
        #Se mueve hacia la derecha.
        if self.isKeyPressed[glfw.KEY_D]:
            self.move(-const.SPEED, 'y')
        #Se mueve hacia adelante.
        if self.isKeyPressed[glfw.KEY_W]:
            self.move(const.SPEED, 'x')
        #Se mueve hacia atrás.
        if self.isKeyPressed[glfw.KEY_S]:
            self.move(-const.SPEED, 'x')
        
controller = Controller()

#Setea la posición de la cámara a partir de lo almacenado en el controlador y utiliza una
#proyección en perspectiva.
def setView1(pipeline):
    view = tr.lookAt(
        controller.viewPos, #eye
        controller.viewAt, #at
        np.array([0, 0, 1]) #up
    )
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    projection = tr.perspective(60, float(const.WIDTH)/float(const.HEIGHT), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1], controller.viewPos[2])
    
#Utiliza una proyección ortogonal desde un punto fijo.
def setView2(pipeline):
    view = tr.lookAt(
            np.array([0, 0, 5]), #eye
            np.array([0, 0.0001, 4]), #at
            np.array([0, 0, 1]) #up
    )
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    projection = tr.ortho(-20, 20, -20, 20, 1, 100)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), 0, 0, 5)
    
#Función para recibir el input del teclado y realizar determinadas acciones.
def on_key(window, key, scancode, action, mods):
    #Muestra los triángulos sin rellenar.
    if key == glfw.KEY_Q and action == glfw.PRESS:
        controller.fillPolygon = not controller.fillPolygon
    #Cierra la ventana.
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    #Cambia la proyección.
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        controller.projection = not controller.projection
    #Activa o desactiva las keys presionadas en el controlador.
    if action > 0:
        controller.isKeyPressed[key] = 1
    else:
        controller.isKeyPressed[key] = 0

#Función para recibir el input del cursor y realizar determinadas acciones.
def on_cursor(window, xpos, ypos):
    e = 0.01
    controller.angles[0] += (const.WIDTH/2 - xpos) * const.SENS
    controller.angles[1] += (const.HEIGHT/2 - ypos) * const.SENS
    if controller.angles[1] > np.pi/2 - e:
        controller.angles[1] = np.pi/2 - e
    if controller.angles[1] < -np.pi/2 + e:
        controller.angles[1] = -np.pi/2 + e 
    controller.rotate()
    glfw.set_cursor_pos(window, const.WIDTH/2, const.HEIGHT/2)