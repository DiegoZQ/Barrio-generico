import numpy as np

#Módulo con todas las funciones necesarias para modelar el circuito requerido para el movimiento
#del auto.

#Retorna un arreglo con los N puntos equiespaciados correspondientes a la recta que une
#P1 con P2
def evalRecta(P1, P2, N):
    P1 = P1.T
    P2 = P2.T
    ts = np.linspace(0.0, 1.0, N)
    dif = P2-P1
    recta = np.ndarray(shape=(N, 3), dtype=float)
    for i in range(len(ts)):
        recta[i, 0:3] = P1 + dif*ts[i]
    return recta

#Crea el vector necesario para evaluar una curva.
def generateT(t):
    return np.array([[1, t, t ** 2, t ** 3]]).T

#Matriz Hermite
def hermiteMatrix(P1, P2, T1, T2):
    # Generate a matrix concatenating the columns
    G = np.concatenate((P1, P2, T1, T2), axis=1)

    # Hermite base matrix is a constant
    Mh = np.array([[1, 0, -3, 2], [0, 0, 3, -2], [0, 1, -2, 1], [0, 0, -1, 1]])

    return np.matmul(G, Mh)

#Retorna un arreglo con los N puntos equiespaciados correspondientes a la curva obtenida
#a partir de la matriz M.
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)

    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)

    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T # x, y, z

    return curve
    
#Retorna una curva usando una matriz de Hermite.
def hermiteCurve(P1, P2, T1, T2, N):
    M = hermiteMatrix(P1, P2, T1, T2)
    return evalCurve(M, N)


#Obtiene el ángulo entre la recta vertical a un punto la obtenida por la resta entre 2
#puntos de la curva.
def getAngle(point1, point2):
    dif = point2-point1
    dif = dif/np.linalg.norm(dif) #se normaliza
    #Soluciona bugs respecto a la rotación
    if dif[0] > 0:
        return np.arccos(-dif[1]/np.linalg.norm(dif))
    else: 
        return -np.arccos(-dif[1]/np.linalg.norm(dif))

#Concatena una lista con curvas.
def concatenateCurve(curves):
    result = []
    for curve in curves:
        result += curve.tolist()
    return np.array(result)

#Obtiene un arreglo con todos los puntos del circuito necesarios para simular
#el movimiento del vehículo
def getCircuito():
    #excentricidad de la curva
    e= 1
    #puntos
    P1 = np.array([[4, 0, 0]]).T
    P2 = np.array([[4, -12.5+e, 0]]).T
    P3 = np.array([[4-e, -12.5, 0]]).T
    P4 = np.array([[-4+e, -12.5, 0]]).T
    P5 = np.array([[-4, -12.5+e, 0]]).T
    #derivadas
    T1 = np.array([[0, -2, 0]]).T
    T2 = np.array([[-2, 0, 0]]).T

    #rectas del circuito
    R1 = evalRecta(P1, P2, 800)
    R2 = evalRecta(P3, P4, 400)
    R3 = evalRecta(P5, -P2, 1600)
    R4 = evalRecta(-P3, -P4, 400)
    R5 = evalRecta(-P5, P1, 800)
    #curvas del circuito
    C1 = hermiteCurve(P2, P3, T1, T2, 400)
    C2 = hermiteCurve(P4, P5, T2, -T1, 400)
    C4 = hermiteCurve(-P2, -P3, -T1, -T2, 400)
    C5 = hermiteCurve(-P4, -P5, -T2, T1, 400)

    curvas = [R1,C1,R2,C2,R3,C4,R4,C5,R5]

    return concatenateCurve(curvas)