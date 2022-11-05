import glfw
from OpenGL.GL import *
import easy_shaders as es
from drawable_shapes import *
import constants as const
from controller import *
from drawable_houses import *
from drawable_terrain import *
from data_sender import *
import time
from day_cycle import *
from drawable_light_shapes import *
from curvas import getCircuito, getAngle

def main():

    if not glfw.init():
        glfw.set_window_should_close(window, True)
    window = glfw.create_window(const.WIDTH, const.HEIGHT, "Tarea 2.1", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)
    #Setea las funciones on_key y on_cursor para recibir input del usuario.
    glfw.set_key_callback(window, on_key)
    glfw.set_cursor_pos_callback(window, on_cursor)
    #Oculta el cursor.
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
    #Asigna el pipeline usando un shader de textura y modelViewProjection simple.
    pipeline = es.MultipleLightTexturePhongShaderProgram()
    #Le dice a OpenGL que use el shader.
    glUseProgram(pipeline.shaderProgram)
    #Permite que se vean primero las figuras que están más cerca de la cámara.
    glEnable(GL_DEPTH_TEST) 
    #Crea el camino y el terreno.
    road = Road(pipeline)
    land = Land(pipeline)
    #Crea las distintas variantes de casas disponibles.
    houseVariants = getHouseVariants(pipeline)
    #Crea una lista con la distribución de dichas casas en una lista.
    listOfRandomHouseVariants = getListOfRandomHouseVariants(40)
    #Crea un data_sender e inicializa algunos valores.
    data_sender = Data_Sender(pipeline)
    data_sender.setAmbientLight([0.1,0.1,0.1])   
    data_sender.setNumberOfPointLights(2)
    data_sender.setNumberOfSpotLights(6)
    data_sender.setShininess(100)
    #Crea las figuras con luz.
    postes = getPostes(pipeline) #4 postes, 1 spotlight por poste
    auto = Car(pipeline) #2 spotlights
    #Genera el circuito que debe recorrer el auto.
    circuito = getCircuito()
    #Índice del punto actual del auto en el circuito
    circuitoIndex = 0
    #Variable que indica cuál fue la última hora registrada.
    lastHour = -1
    #Tiempo en previo al while.
    start = time.time()

    while not glfw.window_should_close(window):
        #Checkea los input events.
        glfw.poll_events()
        #Limpia la pantalla en color y profundidad
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
        #Determina si el controlador está en opción fillPolygon para mostrar
        #la figura completa o sólo las líneas que unen sus vértices
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        #Setea la vista usando el pipeline
        if (controller.projection):
            setView1(pipeline)
        else:
            setView2(pipeline)
        #Revisa las keys presionadas para ver si la cámara debe hacer algún movimiento.
        controller.checkPressedKeys()
        #time
        hour = (time.time()-start)/2
        intHour = int(hour)
        #permite imprimer la hora cada hora sin repetir.
        if (lastHour!=intHour):
            print(str(intHour%24) + ":00")
            lastHour=hour//1 
        #Dibuja las figuras.
        drawHouses(houseVariants, listOfRandomHouseVariants, [9.5,-10.25])
        road.draw([0,0,0],0)
        land.draw([0,0,0],0)
        drawPostes(postes, hour)
        auto.draw(circuito[circuitoIndex], getAngle(circuito[circuitoIndex-2], circuito[(circuitoIndex)]), hour)
        circuitoIndex = (circuitoIndex+1)%len(circuito)
        #Día y noche.
        setDayCycle(pipeline, hour)
    
        #Intercambia los buffers.
        glfw.swap_buffers(window)

    #Libera la memoria de la GPU.
    clearHouseVariants(houseVariants)
    road.clear()
    land.clear()
    clearPostes(postes)
    auto.clear()

    glfw.terminate()

if __name__ == "__main__":
    main()