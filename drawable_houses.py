from basic_shapes import *
from drawable_shapes import *
import random
import math

#Casa básica.
class House1(AdvancedShape):
    def __init__(self, pipeline, assets="house1.jpg"):
        super().__init__(pipeline, assets, "house1.instructions")
    
#Casa mediana. 
class House2(AdvancedShape):
    def __init__(self, pipeline, assets="house2.jpg"):
        super().__init__(pipeline, assets, "house2.instructions")
    
#Casa mediana. 
class House3(AdvancedShape):
    def __init__(self, pipeline, assets="house3.jpg"):
        super().__init__(pipeline, assets, "house3.instructions")

#Obtiene una matriz con las 9 variantes posibles para una casa, mezclando los 3 modelos y los 3 assets,
#con el modelo i en la fila i y el asset j en la columna j.
def getHouseVariants(pipeline):
    return [[House1(pipeline), House1(pipeline, "House2.jpg"), House1(pipeline, "House3.jpg")],
            [House2(pipeline, "House1.jpg"), House2(pipeline), House2(pipeline, "House3.jpg")],
            [House3(pipeline, "House1.jpg"), House3(pipeline, "House2.jpg"), House3(pipeline)]]

#Libera la memoria almacenada en gpu de las distintas variantes de casas almacenadas en una matriz.
def clearHouseVariants(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j].clear()

#Obtiene la casa cuyo número corresponde a N[0] y cuyo asset a N[1] en la matriz 
#de nombre houseVariants.
def getHouse(N, houseVariants):
    return houseVariants[N[0]-1][N[1]-1]

#Obtiene una lista de tamaño N cuyos valores son tuplas i,j que oscilan aleatoriamente entre 1 y 3,
#cuyos valores corresponden al modelo de la casa i y el asset j. 
def getListOfRandomHouseVariants(N):
    list = []
    for i in range(N):
        list+=[[random.randint(1, 3), random.randint(1, 3)]]
    return list

#Dibuja varias hileras de, a lo más, 8 casas usando una matriz con las distintas variantes de casas
#y la distribución de dichas variantes en una lista, partiendo en una posicion x, y.
def drawHouses(houseVariants, distribution, pos):
    x, y = pos
    N = math.ceil(len(distribution)/16)
    for i in range(N):
        for j in range(8):
            for k in range(2):
                if k==0:
                    rotation = -np.pi/2
                else:
                    rotation = np.pi/2
                try:
                    house = getHouse(distribution[k+2*j+16*i], houseVariants)
                    house.draw([x,y,0.5], rotation)
                    x-=3
                except:
                    return   
            x=pos[0]
            y+=3
        y=pos[1]
        pos[0]=x-8
        x=pos[0]