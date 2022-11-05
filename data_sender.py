from OpenGL.GL import *

#Clase encargada de enviar información relevante a las variables almacenadas en el programa 
#escrito en C++ el cual maneja los shaders.
class Data_Sender():
    def __init__(self, pipeline):
        self.pipeline = pipeline

    #Setea el número de pointLights.
    def setNumberOfPointLights(self, N):
        glUniform1i(glGetUniformLocation(self.pipeline.shaderProgram, "point_lights"), N) 
    
    #Setea el número de spotLights.
    def setNumberOfSpotLights(self, N):
        glUniform1i(glGetUniformLocation(self.pipeline.shaderProgram, "spot_lights"), N)

    #Setea la luz ambiente (r,g,b).
    def setAmbientLight(self, ambientLight):
        glUniform3f(glGetUniformLocation(self.pipeline.shaderProgram, "ambientLight"), ambientLight[0], ambientLight[1], ambientLight[2])

    #Setea el brillo.
    def setShininess(self, shininess):
        glUniform1f(glGetUniformLocation(self.pipeline.shaderProgram, "shininess"), shininess)

    #Setea un punto de luz ubicado en un índice específico del arreglo pointLights.
    #data = [position[3], constant, linear, cuadratic, ambient[3], diffuse[3], specular[3]].
    #position: posición del punto de luz.
    #constant, linear y cuadratic: constantes de atenuación de la luz en general.
    #diffuse y specular intensidades de las reflexiones difusa y especular en rgb.
    def setPointLight(self, data, index):
        pointLight = "pointLights["+str(index)+"]."
        glUniform3f(glGetUniformLocation(self.pipeline.shaderProgram, pointLight+"position"), data[0][0], data[0][1], data[0][2])
        glUniform1f(glGetUniformLocation(self.pipeline.shaderProgram, pointLight+"constants"), data[1])
        glUniform1f(glGetUniformLocation(self.pipeline.shaderProgram, pointLight+"linear"), data[2])
        glUniform1f(glGetUniformLocation(self.pipeline.shaderProgram, pointLight+"cuadratic"), data[3])
        glUniform3f(glGetUniformLocation(self.pipeline.shaderProgram, pointLight+"diffuse"), data[4][0], data[4][1], data[4][2])
        glUniform3f(glGetUniformLocation(self.pipeline.shaderProgram, pointLight+"specular"), data[5][0], data[5][1], data[5][2])

    #Setea un spot de luz ubicado en un índice específico del arreglo spotLights.
    #data = [position[3], direction[3], cutOff, outerCutOff, constant, linear, cuadratic, diffuse[3], specular[3]].
    #position: posición de la fuente.
    #direction: dirección de la luz.
    #cutOff y outerCutOff: constantes que determinan el ángulo de iluminación.
    #constant, linear y cuadratic: constantes de atenuación de la luz en general.
    #diffuse y specular intensidades de las reflexiones difusa y especular en rgb.
    def setSpotLight(self, data, index):
        spotLight = "spotLights["+str(index)+"]."
        glUniform3f(glGetUniformLocation(self.pipeline.shaderProgram, spotLight+"position"), data[0][0], data[0][1], data[0][2])
        glUniform3f(glGetUniformLocation(self.pipeline.shaderProgram, spotLight+"direction"), data[1][0], data[1][1], data[1][2])
        glUniform1f(glGetUniformLocation(self.pipeline.shaderProgram, spotLight+"cutOff"), data[2])
        glUniform1f(glGetUniformLocation(self.pipeline.shaderProgram, spotLight+"outerCutOff"), data[3])
        glUniform1f(glGetUniformLocation(self.pipeline.shaderProgram, spotLight+"constants"), data[4])
        glUniform1f(glGetUniformLocation(self.pipeline.shaderProgram, spotLight+"linear"), data[5])
        glUniform1f(glGetUniformLocation(self.pipeline.shaderProgram, spotLight+"cuadratic"), data[6])
        glUniform3f(glGetUniformLocation(self.pipeline.shaderProgram, spotLight+"diffuse"), data[7][0], data[7][1], data[7][2])
        glUniform3f(glGetUniformLocation(self.pipeline.shaderProgram, spotLight+"specular"), data[8][0], data[8][1], data[8][2])