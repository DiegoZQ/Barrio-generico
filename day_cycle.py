from data_sender import *
import numpy as np

#Establece el ciclo día y noche usando un pipeline y el tiempo.
def setDayCycle(pipeline, time):

    data_sender = Data_Sender(pipeline)
    time = time%24

    sunSettings = [[40*np.cos((time-6)*np.pi/12), 0, 40*np.sin((time-6)*np.pi/12)], 
                    0.001, 0.01, 0.01, [1,1,1], [1,1,1]]
                    
    moonSettings = [[40*np.cos((time+6)*np.pi/12), 0, 40*np.sin((time+6)*np.pi/12)],
                    0.001, 0.01, 0.01, [0.13,0.13,0.13], [0.13,0.13,0.13]]

    data_sender.setPointLight(sunSettings, 0)
    data_sender.setPointLight(moonSettings, 1)

    dia = np.array([64/255, 207/255, 1])
    noche = np.array([25/255, 28/255, 50/255])
    dif = dia-noche
    if time < 12:
        r, g, b = noche + dif * (time/12) 
        glClearColor(r, g, b, 1.0)  
    else:
        time = time%12
        r, g, b = dia - dif * (time/12) 
        glClearColor(r, g, b, 1.0)  