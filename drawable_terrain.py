from basic_shapes import *
from drawable_shapes import *
from drawable_light_shapes import AdvancedShapeWithLight

#Clase encargada de crear el terreno.
class Land(AdvancedShape):
    def __init__(self, pipeline):
        super().__init__(pipeline, "pasto.jpg", "land.instructions")

#Clase encargada de crear la calle.
class Road(AdvancedShape):
    def __init__(self, pipeline):
        super().__init__(pipeline, "road.jpg", "road.instructions")

#Clase encargada de crear los postes.
class Poste(AdvancedShapeWithLight):
    def __init__(self, pipeline):
        #1 spotlight
        data = [ [[0, 0.85, 0.88], [0,0.08,-1], 0.4, 0.4, 0.2, 0.3, 0.2, [1,1,1],[1,1,1]] ]
        super().__init__(pipeline,"Poste.jpg", "poste.instructions", data)
 
#Obtiene una lista con 4 instancias de la clase poste.
def getPostes(pipeline):
    result = []
    for i in range(4):
        result += [Poste(pipeline)]
    return result

#Dibuja cada poste de una lista con postes.
def drawPostes(postes, time):
    postes[0].draw([3,6,0],-np.pi/2, time)
    postes[1].draw([3,-6,0],-np.pi/2, time)
    postes[2].draw([-3,6,0],np.pi/2, time)
    postes[3].draw([-3,-6,0],np.pi/2, time)

#Limpia la gpuShape de los postes en una lista con postes.
def clearPostes(postes):
    for i in range(len(postes)):
        postes[i].clear()